# encoding: utf-8
from __future__ import print_function
import os, sys, inspect, re
import typing
from http.client import NotConnected

from . import settings, opc_vars, visualize
from importlib import reload, import_module
from inspect import isfunction
from typing import Self, Callable, TypeVar


global opc_client
global guid_registry

tGeneric = TypeVar('tGeneric', bound='Generic')
tPlasticParent = TypeVar('tPlasticParent', bound='PlasticParent')
tOpcVariable = TypeVar('tOpcVariable', bound='opc_vars.OpcVariable')

def is_type_of(first,second,or_inherited=True) -> bool:
	"""Compare if first is instance of second
	with no regards of reloads
	"""
	if str(first.__class__) == str(second.__class__):
		return True
	elif or_inherited:
		for base in first.__class__.__bases__:
			if str(second.__class__) == str(base):
				return True
	return False

def check_write_type(value_to_write, canonical_data_type: int) -> bool:
	""" Checking the type of value_to_write compared to the OPC Canonical data type
	according to https://support.softwaretoolbox.com/app/answers/detail/a_id/3849/~/opc-canonical-data-types

	:value_to_write: The value that is prepared for writing with the OPC client
	:canonical_data_type: A number that translate to a OPC datatype
	:return: Boolean answering if write is possible to the type
	"""
	if type(value_to_write) is bool and canonical_data_type == 11:
		"Bool"
		return True
	if type(value_to_write) is int and 0 <= value_to_write <= 255 and canonical_data_type == 17:
		"Byte"
		return True
	if type(value_to_write) is int and -128 <= value_to_write <= 127 and canonical_data_type in [2,16]:
		"Short/Int or Char"
		return True
	if type(value_to_write) is int and 0 <= value_to_write < 2**16 and canonical_data_type == 18:
		"Word/Unit possible BCD"
		return True
	if type(value_to_write) is int and 0 <= value_to_write < 2**32 and canonical_data_type == 19:
		"DWord/DUint"
		return True
	if type(value_to_write) is float and canonical_data_type in [4,5]:
		"Float"
		return True
	if type(value_to_write) is int and canonical_data_type in [4,5]:
		"Int to Float/Double also works"
		return True
	if type(value_to_write) is int and 0 <= value_to_write < 2**64 and canonical_data_type in [20,21]:
		"Int to LLong/QWord"
		return True
	if type(value_to_write) is str and canonical_data_type == 8:
		"String"
		return True
	if canonical_data_type > 8000:
		raise NotImplemented("The possibility to write to Arrays isn't implemented.")
	return False

def bcd_to_int(n: int) -> int:
	"""Converts a binary-coded decimal to a int value
	:n: The BCD value to convert to int
	:return: The int value result
	"""
	return int(('%x' % n), base=10)

def int_to_bcd(n: int) -> int:
	"""Converts an int value to binary-coded decimal value
		:n: The int value to convert to BCD
		:return: The BCD value result
		"""
	return int(str(n), base=16)

def approve_opc_child_name(obj: tGeneric, item_name:str) -> str:
	"""Transforms the item_name to a string that can be used as an attribute name for obj. If the name already is used
	as an attribute name for the object is an underscore _ added to the name.
	:obj: The object that should get the new item_name as attribute
	:item_name: Name of item that should become an attribute
	:return: approved attribute name
	"""
	item_name = re.sub('[^0-9a-zA-Z_]+', '', item_name)
	if item_name[0].isnumeric(): item_name = '_' + item_name
	if hasattr(obj, item_name):
		if isinstance(getattr(obj, item_name), Generic):
			return item_name
		elif isinstance(getattr(obj, item_name), opc_vars.OpcVariable):
			return item_name
		elif item_name in obj.opc_children:
			# Item can fail check above if upgraded
			return item_name
		else:
			item_name = approve_opc_child_name(obj, '_' + item_name)
	return item_name

def approve_name_and_register_guid(parent: tGeneric, obj: typing.Optional[typing.Union[tGeneric,tOpcVariable]], item_name: str) -> str:
	"""Checks if the name can be used as attribute
	If there is an uuid in the name is it removed and
	registered in the global guid_registry, pointing
	to the child. It the inputted name is ok then is
	that return otherwise is an underscore added in
	the beginning.
	:Return: An approved name
	"""
	find_result = re.findall('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-5][0-9a-fA-F]{3}-[089ab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}', item_name)
	if len(find_result) == 0:
		return approve_opc_child_name(parent, item_name)
	else:
		global guid_registry
		if not 'guid_registry' in globals(): guid_registry = {}
		guid_registry[find_result[-1]] = obj
		for idx in range(len(find_result)):
			item_name = item_name.replace(find_result[idx],'')
		new_name = approve_opc_child_name(parent, item_name)
		return new_name


def restore(file_name: str=None, working_dir=None) -> None:
	import pickle
	file_dir = working_dir if not working_dir is None else settings.WORKING_DIR
	file_path = os.path.join(file_dir, file_name + '.pickle') if not file_name is None else os.path.join(file_dir,
																										 'opc_obj.pickle')
	with open(file_path, 'rb') as pickle_file:
		return pickle.load(pickle_file)


class Generic(object):
	opc_path = None
	opc_children = []

	def __init__(self,opc_path: typing.Optional[str],predecessor: tGeneric=None):
		self.opc_children = []
		self.opc_path = opc_path
		if not predecessor is None:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				if attribute in self.opc_children:
					old_child = getattr(predecessor,attribute)
					child_class = getattr(sys.modules[old_child.__class__.__module__],old_child.__class__.__name__)
					new_child = child_class(old_child.opc_path,old_child)
					setattr(self,attribute,new_child)
					print('\t+ Upgraded:' + str(new_child) + '\t\t\t\t', end="\r")
				else:
					setattr(self,attribute,getattr(predecessor,attribute))

	def upgrade(self) -> Self:
		"""Reload libraries and upgrade node
		The module reloads the libraries'
		version and upgrades the node and
		all children.
		:return: The upgraded version
		"""
		reload(sys.modules[__name__])
		reload(sys.modules[opc_vars.__name__])
		reload(sys.modules[visualize.__name__])
		reload(sys.modules[self.__class__.__module__])
		self_class = getattr(sys.modules[self.__class__.__module__],self.__class__.__name__)
		new_self = self_class(self.opc_path,self)
		for attribute in [a for a in dir(new_self) if a in self.opc_children]:
			setattr(new_self,attribute,getattr(new_self,attribute).upgrade())
		self.__dict__.update(new_self.__dict__)
		return new_self

	def test(self) -> None:
		print('Test7')

	def load_children(self, levels: int=-1, opc_cli=None, counter: int=None) -> Self:
		global opc_client
		if not 'opc_client' in globals():
			opc_client = opc_cli
		elif opc_cli is None:
			opc_cli = opc_client
		if levels == 0: return self if counter is None else self, counter
		result = opc_cli.list(self.opc_path)
		for old_child in self.opc_children:
			delattr(self,old_child)
		self.opc_children = []
		if counter is None: internal_counter = 0
		else: internal_counter = counter
		for item in result:
			if self.opc_path is None:
				new_path = item
				child, internal_counter = Generic(new_path).load_children(levels=levels-1,opc_cli=opc_cli,  counter=internal_counter)
				item_name = approve_name_and_register_guid(self,child,item)
				setattr(self, item_name, child)
				self.opc_children.append(item_name)
			elif self.opc_path in item:
				variable_properties = None
				# variable_properties = opc_cli.properties(item)
				# setattr(self,item.rsplit('.',1)[1],variable_properties)
				child = self._create_variable(item,variable_properties)
				var_name = item.rsplit('.',1)[1]
				var_name = approve_name_and_register_guid(self, child, var_name)
				self.opc_children.append(var_name)
				internal_counter += 1
				setattr(self,var_name,child)
				print(str(internal_counter).ljust(7) + 'Loaded var:' + item.ljust(os.get_terminal_size().columns-19), end="\r")
			else:
				new_path = '.'.join([self.opc_path,item])
				child, internal_counter = Generic(new_path).load_children(levels=levels-1,opc_cli=opc_cli,  counter=internal_counter)
				item_name = approve_name_and_register_guid(self, child, item)
				setattr(self,item_name,child)
				self.opc_children.append(item_name)
		if counter is None:
			print()
			return self
		return self, internal_counter

	def reload_children(self, levels: int=-1, opc_cli=None, counter: int=None, ignore_existing=False) -> Self:
		global opc_client
		if not 'opc_client' in globals():
			opc_client = opc_cli
		elif opc_cli is None:
			opc_cli = opc_client
		if levels == 0: return self if counter is None else self, counter
		result = opc_cli.list(self.opc_path)
		if counter is None:
			internal_counter = 0
		else:
			internal_counter = counter
		new_opc_children_names = [('.' + item_name).rsplit('.', 1)[1] for item_name in result]
		for item_name in [old_child for old_child in self.opc_children if not old_child in new_opc_children_names]:
			delattr(self,item_name)
			self.opc_children.remove(item_name)
		for item in result:
			child_name = ('.' + item).rsplit('.', 1)[1]
			if child_name in self.opc_children:
				# Item loaded before
				if ignore_existing or self.opc_path in item:
					continue
				child, internal_counter = getattr(self,child_name).reload_children(levels=levels-1,opc_cli=opc_cli,  counter=internal_counter)
			elif self.opc_path is None:
				new_path = item
				child, internal_counter = Generic(new_path).reload_children(levels=levels-1,opc_cli=opc_cli,  counter=internal_counter)
				item_name = approve_name_and_register_guid(self,child,item)
				setattr(self, item_name, child)
				self.opc_children.append(item_name)
			elif self.opc_path in item:
				variable_properties = None
				child = self._create_variable(item,variable_properties)
				var_name = approve_name_and_register_guid(self, child, child_name)
				self.opc_children.append(var_name)
				internal_counter += 1
				setattr(self,var_name,child)
				print(str(internal_counter).ljust(7) + 'Loaded var:' + item.ljust(os.get_terminal_size().columns-19), end="\r")
			else:
				new_path = '.'.join([self.opc_path,item])
				child, internal_counter = Generic(new_path).reload_children(levels=levels-1,opc_cli=opc_cli,  counter=internal_counter)
				item_name = approve_name_and_register_guid(self, child, item)
				setattr(self,item_name,child)
				self.opc_children.append(item_name)
		if counter is None:
			print()
			return self
		return self, internal_counter

	def _create_variable(self, opc_path: str, variable_properties: typing.Optional[str]) -> opc_vars.OpcVariable:
		return opc_vars.OpcVariable(opc_path, opc_properties=variable_properties)

	def transform(self, diag=False) -> Self:
		from src.OPCTree import opc_class_lib
		reload(opc_class_lib)
		for lib in opc_class_lib.__all__:
			print("Importing: " + lib)
			module = import_module('opc_class_lib.' + lib)
			reload(module)
		return self._transform(diag)

	def _transform(self,diag=False) -> Self:
		for child in self.opc_children:
			setattr(self,child,getattr(self,child)._transform(diag))
		# print('Loaded modules: ' + str(sys.modules))
		opc_class_libraries = [lib for lib in sys.modules if 'opc_class_lib.' in lib]
		# print('Upgrading with: ' + str(opc_class_libraries))
		new_classes = []
		for opc_class_lib in opc_class_libraries:
			new_classes.extend(inspect.getmembers(sys.modules[opc_class_lib], inspect.isclass))
		for opc_class_name, opc_class in new_classes:
			if self.compare_identity(opc_class('DummyPath'),diag=diag):
				print('Transforming ' + self.opc_path + ' into ' + opc_class_name + str(opc_class))
				new_self = opc_class(self.opc_path,predecessor=self)
				self.__dict__.update(new_self.__dict__)
				return new_self
		return self

	def compare_identity(self,other: tGeneric,diag=False) -> bool:
		# if [x for x in self.opc_children if x.title() != 'Dummy'] != [x for x in other.opc_children if x.title() != 'Dummy']:
		# 	return False
		if diag:
			print(self.opc_path)
			print("Compare " + str(self.opc_children) + " with " + str(other.opc_children))
		if len(self.opc_children) != len(other.opc_children):
			return False
		for attribute in [x for x in self.opc_children if x.title() != 'Dummy']:
			try:
				if not is_type_of(getattr(self,attribute),getattr(other,attribute)):
					return False
			except AttributeError:
				return False
		return True

	def all_of_class_as_set(self,re_class: str) -> set:
		result = set()
		for attribute in self.opc_children:
			result.update(getattr(self,attribute).all_of_class_as_set(re_class))
		if not re.search(re_class,str(self.__class__.__name__)) is None:
			result.add(self)
		return result

	def _all_of_class(self, re_class: str, filter_func=None, branches:bool=True) -> tPlasticParent:
		children = self.all_of_class_as_set(re_class)
		adopting_parent = PlasticParent('Adopting parent')
		for child in children:
			if not filter_func is None:
				if not filter_func(child): continue
			if (not branches) and hasattr(child, 'opc_children'): continue
			new_attr_name = approve_name_and_register_guid(adopting_parent, child, child.opc_path.replace('.','_'))
			adopting_parent.opc_children.append(new_attr_name)
			setattr(adopting_parent,new_attr_name,child)
		adopting_parent.opc_children.sort()
		return adopting_parent

	def all_with_path_as_set(self, re_path: str) -> set:
		result = set()
		for child_path in self.opc_children:
			result.update(getattr(self,child_path).all_with_path_as_set(re_path))
		if self.opc_path is None:
			pass
		elif re_path is None:
			result.add(self)
		elif not re.search(re_path,self.opc_path) is None:
			result.add(self)
		return result

	def _all_with_path(self, re_path: str, filter_func: Callable[[tGeneric],bool]=None, branches:bool=True) -> tPlasticParent:
		children = self.all_with_path_as_set(re_path)
		adopting_parent = PlasticParent('Adopting parent')
		for child in children:
			if not filter_func is None:
				if not filter_func(child): continue
			if (not branches) and hasattr(child, 'opc_children'): continue
			new_attr_name = approve_name_and_register_guid(adopting_parent, child, child.opc_path.replace('.', '_'))
			adopting_parent.opc_children.append(new_attr_name)
			setattr(adopting_parent,new_attr_name,child)
		adopting_parent.opc_children.sort()
		return adopting_parent

	def all(self,re_path: str=None,re_class: str=None,
			filter_func: Callable[[tGeneric],bool]=None, branches: bool=True) -> tPlasticParent:
		"""Returns all children with matching opc-path and class
		observe that the opc-path has dots '.' as separator between
		parent and child
		
		Keywords:
		:re_path: The regular expression string that should be matched against the opc-path
		:re_class: The regular expression string that should be matched against the class of the item
		:filter_func: A custom filter like the ones in example_filters.py
		:branches: Boolean value saying if branches (opc structs) should be included otherwise only leaves
		:return: An Adopting parent with all the filtered objects as children on first level
		"""
		if not (isinstance(re_path, str) or re_path is None):
			raise TypeError("re_path is of type " +str(type(re_path)) + " it should be a regex-string")
		if not (isinstance(re_class, str) or re_class is None):
			raise TypeError("re_class is of type " +str(type(re_class)) + " it should be a regex-string")
		if not (isfunction(filter_func) or filter_func is None):
			raise TypeError("filter is of type " +str(type(filter_func)) + " it should be a function")
		if (re_class is None) and (re_path is None):
			return self._all_with_path(re_path='', filter_func=filter_func, branches=branches)
		if re_class is None:
			return self._all_with_path(re_path, filter_func=filter_func, branches=branches)
		if re_path is None:
			return self._all_of_class(re_class, filter_func=filter_func, branches=branches)
		return self._all_with_path(re_path, filter_func=filter_func, branches=branches)._all_of_class(re_class)

	def all_as_list(self,re_path: str=None,re_class: str=None,
			filter_func: Callable[[tGeneric],bool]=None, branches: bool=True) -> list:
		adopting_parent = self.all(re_path,re_class,filter_func)
		if branches:
			return [getattr(adopting_parent,child_path) for child_path in adopting_parent.opc_children]
		else:
			return [getattr(adopting_parent,child_path) for child_path in adopting_parent.opc_children
					if not hasattr(getattr(adopting_parent,child_path),'opc_children')]

	def save(self, file_name: str=None, working_dir=None) -> None:
		import pickle
		file_dir = working_dir if not working_dir is None else settings.WORKING_DIR
		try:
			os.mkdir(file_dir)
		except FileExistsError:
			pass
		file_path = os.path.join(file_dir, file_name + '.pickle') if not file_name is None else os.path.join(file_dir, 'opc_obj.pickle')
		with open(file_path, 'wb') as pickle_file:
			# noinspection PyTypeChecker
			pickle.dump(self,pickle_file)
			print('Saved to: ' + file_path)

	def rename_child(self, name_now: str ,new_name: str) -> Self:
		"""Rename a child with new OPC name
		Changing the opc_path for all children below. Use in connection with
		renaming in the PLC
		:name_now: The old name
		:new_name: The new name
		:return: self
		"""
		if not name_now in self.opc_children:
			raise Exception("There's no child with the given name_now: " + str(name_now))
		child_to_rename = getattr(self, name_now)
		new_approved_name = approve_name_and_register_guid(self, child_to_rename, new_name)
		if new_approved_name != new_name:
			raise Exception("Proposed new name isn't appropriate, you can try: " + new_approved_name)
		self.opc_children.remove(name_now)
		self.opc_children.append(new_approved_name)
		delattr(self, name_now)
		setattr(self,new_approved_name, child_to_rename)
		child_to_rename._rename_in_opc_path(new_approved_name, level=0)
		return self

	def _rename_in_opc_path(self, new_name: str, level: int=0) -> Self:
		split_path = self.opc_path.split('.')
		split_path[level-1] = new_name
		self.opc_path = '.'.join(split_path)
		for child_name in self.opc_children:
			getattr(self,child_name)._rename_in_opc_path(new_name, level=level-1)
		return self

	def first_read(self, opc_cli=None, max_chunk=40) -> Self:
		global opc_client
		if opc_cli is None:
			try:
				opc_cli = opc_client
			except NameError:
				raise NotConnected("You have to initialize the OPC client first, try OPCTree.opc_fetch.initiate_opc_client()")
		parent_with_all = self.all()
		obj_to_read = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not ((hasattr(getattr(parent_with_all,child_path),'opc_children'))
							or (hasattr(getattr(parent_with_all,child_path),'name_prop')))]
		tags_to_read = [obj.opc_path for obj in obj_to_read]
		i = 0
		print("Read properties " + str(i).rjust(8) + " of " +str(len(tags_to_read)).rjust(8) + " items", end="\r")
		while len(tags_to_read) > i:
			try:
				loc_res = opc_cli.properties(tags_to_read[i:i+max_chunk])
				print("Read properties " + str(i).rjust(8) + " of "
					  +str(len(tags_to_read)).rjust(8) + " items", end="\r")
			except Exception:
				raise Exception("Couldn't read properties from: " + str(tags_to_read[i:i+max_chunk]))
			for (item, PropertyId,PropertyName,PropertyValue) in loc_res:
				obj = getattr(parent_with_all,item.replace('.','_'))
				if not hasattr(obj,'name_prop'):
					obj.name_prop = {PropertyName: PropertyValue}
					obj.idx_prop = {PropertyId: PropertyValue}
				else:
					obj.name_prop[PropertyName] = PropertyValue
					obj.idx_prop[PropertyId] = PropertyValue
				if PropertyName == 'Item Value':
					obj.value = PropertyValue
			i += max_chunk
		print("Read properties " + str(min(i,len(tags_to_read))).rjust(8)
			  + " of " +str(len(tags_to_read)).ljust(8) + " items")
		return self

	def read(self, opc_cli=None, max_chunk=1000, log: bool=True) -> Self:
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_read = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not hasattr(getattr(parent_with_all,child_path),'opc_children')]
		tags_to_read = [obj.opc_path for obj in obj_to_read]
		i = 0
		print("Read " + str(i).rjust(8) + " of " +str(len(tags_to_read)).rjust(8) + " items", end="\r")
		while len(tags_to_read) > i:
			try:
				loc_res = opc_cli.read(tags_to_read[i:i+max_chunk])
				print("Read " + str(i).rjust(8) + " of " +str(len(tags_to_read)).rjust(8) + " items", end="\r")
			except Exception:
				raise Exception("Couldn't read values from: " + str(tags_to_read[i:i+max_chunk]))
			for (item, value, quality, timestamp) in loc_res:
				obj = getattr(parent_with_all,item.replace('.','_'))
				obj.value = value
				if log:
					if hasattr(obj,'log'): obj.log.append((value,quality,timestamp))
					else: obj.log = [(value,quality,timestamp)]
			i += max_chunk
		print("Read " + str(min(i,len(tags_to_read))).rjust(8) + " of " +str(len(tags_to_read)).ljust(8) + " items")
		return self

	def clear_logs(self) -> Self:
		for obj in self.all_as_list(branches=False):
			obj.log = []
		return self

	def write_one_value(self, value, opc_cli=None, max_chunk: int=20, accept_fails: bool=False) -> Self:
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_write = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not hasattr(getattr(parent_with_all,child_path),'opc_children')]
		try:
			tags_write_data = [((obj.opc_path, value), obj.idx_prop[1], obj.idx_prop[5]) for obj in obj_to_write]
		except AttributeError:
			raise Exception('You have to read the properties of the values before trying to writing them')

		path_value = []
		for tags_to_write, data_type, access_right in tags_write_data:
			if access_right != 'Read/Write':
				if accept_fails:
					print("You don't have access right to Read/Write " + str(tags_to_write[0]) + " item is ignored.")
					continue
				else:
					raise Exception("You don't have access right to Read/Write " + str(tags_to_write[0]))
			if not check_write_type(value, data_type):
				if accept_fails:
					print("Value is of wrong data type " + str(tags_to_write[0]) + " is of type "
						  + str(type(value)) + " while the tag is canonical type: " + str(data_type))
					continue
				else:
					raise Exception("Value is of wrong data type " + str(tags_to_write[0]) + " is of type " + str(
						type(value)) + " while the tag is canonical type: " + str(data_type))
			path_value.append(tags_to_write)
		i = 0
		print("Write " + str(i).rjust(8) + " of " +str(len(path_value)).rjust(8) + " items", end="\r")
		while len(path_value) > i:
			try:
				opc_cli.write(path_value[i:i+max_chunk])
				print("Write " + str(i).rjust(8) + " of " +str(len(path_value)).rjust(8) + " items", end="\r")
			except Exception:
				raise Exception("Couldn't write values to: " + str(path_value[i:max_chunk]))
			i += max_chunk
		print("Write " + str(min(i,len(path_value))).rjust(8) + " of " +str(len(path_value)).rjust(8) + " items")
		return self

	def write(self, opc_cli=None, max_chunk: int=20, accept_fails: bool=False) -> Self:
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_write = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not hasattr(getattr(parent_with_all,child_path),'opc_children')]
		try:
			tags_write_data = [((obj.opc_path, obj.value), obj.idx_prop[1], obj.idx_prop[5]) for obj in obj_to_write]
		except AttributeError:
			raise Exception('You have to read the properties of the values before trying to writing them')
		path_value = []
		for data_to_write, data_type, access_right in tags_write_data:
			if access_right != 'Read/Write':
				if accept_fails:
					print("You don't have access right to Read/Write " + str(data_to_write[0]) + " item is ignored.")
					continue
				else:
					raise Exception("You don't have access right to Read/Write " + str(data_to_write[0]))
			if not check_write_type(data_to_write[1], data_type):
				if accept_fails:
					print("Value is of wrong data type " + str(data_to_write[0]) + " is of type "
						  + str(type(data_to_write[1])) + " while the tag is canonical type: " + str(data_type))
					continue
				else:
					raise Exception("Value is of wrong data type " + str(data_to_write[0]) + " is of type " + str(
						type(data_to_write[1])) + " while the tag is canonical type: " + str(data_type))
			path_value.append(data_to_write)
		i = 0
		print("Write " + str(i).rjust(8) + " of " +str(len(path_value)).rjust(8) + " items", end="\r")
		while len(path_value) > i:
			try:
				opc_cli.write(path_value[i:i+max_chunk])
				print("Write " + str(i).rjust(8) + " of " +str(len(path_value)).rjust(8) + " items", end="\r")
			except Exception:
				raise Exception("Couldn't write values to: " + str(path_value[i:max_chunk]))
			i += max_chunk
		print("Write " + str(min(i,len(path_value))).rjust(8) + " of " +str(len(path_value)).rjust(8) + " items")
		return self

	def changed(self, opc_cli=None, print_all: bool=False, max_chunk: int=200) -> tPlasticParent:
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_read = [getattr(parent_with_all, child_path) for child_path in parent_with_all.opc_children
					   if not hasattr(getattr(parent_with_all, child_path), 'opc_children')]
		tags_to_read = [obj.opc_path for obj in obj_to_read]
		i = 0
		adopting_parent = PlasticParent('Adopting parent')
		print("Live value".ljust(30) + "Saved value".ljust(30) + "Tag")
		while len(tags_to_read) > i:
			try:
				loc_res = opc_cli.read(tags_to_read[i:i + max_chunk])
				print("Compare " + str(i).rjust(8) + " of " + str(len(tags_to_read)).rjust(8) + " items", end="\r")
			except Exception:
				raise Exception("Couldn't read values from: " + str(tags_to_read[i:i + max_chunk]))
			for (item, value, quality, timestamp) in loc_res:
				obj = getattr(parent_with_all, item.replace('.', '_'))
				if obj.value != value or print_all:
					print(str(value).ljust(30) + str(obj.value).ljust(30) + obj.opc_path)
					new_attr_name = approve_name_and_register_guid(adopting_parent, obj,
																   obj.opc_path.replace('.', '_'))
					adopting_parent.opc_children.append(new_attr_name)
					setattr(adopting_parent, new_attr_name, obj)
			i += max_chunk
		return adopting_parent

	def visualize(self):
		visualize.generate_html_visualization(self)

class PlasticParent(Generic):

	def combine_parent(self, other_parent: tGeneric):
		for new_child in [getattr(other_parent,child) for child in other_parent.opc_children]:
			if new_child.opc_path.replace('.','_') in self.opc_children: continue
			new_attr_name = approve_name_and_register_guid(self, new_child, new_child.opc_path.replace('.', '_'))
			self.opc_children.append(new_attr_name)
			setattr(self,new_attr_name,new_child)

	def print_values(self, nbr_to_print: int=None) -> None:
		"""Print child.value for all children on parent
		if nbr_to_print is specified is only the specified number
		of children printed.
		:return: None
		"""
		children_to_print = [getattr(self,path) for path in self.opc_children if not hasattr(getattr(self,path),'opc_children')]
		if nbr_to_print is None: nbr_to_print = len(children_to_print)
		for child in children_to_print[:nbr_to_print]:
			try:
				print(str(child.value).ljust(15) + child.opc_path)
			except AttributeError:
				print(str('Not read').ljust(15) + child.opc_path)

	def print_paths(self, nbr_to_print: int=None) -> None:
		paths_to_print = [getattr(self, path).opc_path for path in self.opc_children]
		if nbr_to_print is None: nbr_to_print = len(paths_to_print)
		print('Printing ' + str(min(nbr_to_print,len(paths_to_print))) + ' of ' + str(len(paths_to_print)) + ' paths')
		for path in paths_to_print[:nbr_to_print]:
			print(path)