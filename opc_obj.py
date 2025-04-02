# encoding: utf-8
from __future__ import print_function
import os, sys, inspect, re, settings
from importlib import reload, import_module
import opc_vars

global opc_client
global guid_registry

def is_type_of(first,second,or_inherited=True):
	"""Compare if first is instance of second
	with no regards of reloads"""
	if str(first.__class__) == str(second.__class__):
		return True
	elif or_inherited:
		for base in first.__class__.__bases__:
			if str(second.__class__) == str(base):
				return True
	return False

def check_write_type(value_to_write, canonical_data_type):
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
		"Word/Unit"
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
	return False

def bcd_to_int(n):
	return int(('%x' % n), base=10)

def int_to_bcd(n):
	return int(str(n), base=16)

def approve_opc_child_name(obj, item_name):
	item_name = re.sub('[^0-9a-zA-Z_]+', '', item_name)
	if item_name[0].isnumeric(): item_name = '_' + item_name
	if hasattr(obj, item_name):
		if isinstance(getattr(obj, item_name), Generic):
			return item_name
		elif isinstance(getattr(obj, item_name), opc_vars.OpcVariable):
			return item_name
		else:
			item_name = approve_opc_child_name(obj, '_' + item_name)
	return item_name

def approve_name_and_register_guid(parent, obj, item_name):
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

class Generic(object):
	opc_path = None
	opc_children = []
	
	def __init__(self,opc_path,predecessor=None):
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
					
	def upgrade(self):
		reload(sys.modules['opc_obj'])
		reload(sys.modules['opc_vars'])
		reload(sys.modules[self.__class__.__module__])
		self_class = getattr(sys.modules[self.__class__.__module__],self.__class__.__name__)
		new_self = self_class(self.opc_path,self)
		for attribute in [a for a in dir(new_self) if a in self.opc_children]:
			setattr(new_self,attribute,getattr(new_self,attribute).upgrade())
		self.__dict__.update(new_self.__dict__)
		return new_self
				
	def test(self):
		print('Test7')
				
	def load_children(self, levels=-1, opc_cli=None, counter=None):
		global opc_client
		if not 'opc_client' in globals():
			opc_client = opc_cli
		elif opc_cli is None:
			opc_cli = opc_client
		if levels == 0: return self if counter is None else self, counter
		result = opc_cli.list(self.opc_path)
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
				# variable_properties = None
				# variable_properties = opc_cli.properties(item)
				variable_properties = None
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

	def _create_variable(self, opc_path, variable_properties):
		return opc_vars.OpcVariable(opc_path, opc_properties=variable_properties)

	def transform(self, diag=False):
		import opc_class_lib
		reload(opc_class_lib)
		for lib in opc_class_lib.__all__:
			print("Importing: " + lib)
			module = import_module('opc_class_lib.' + lib)
			reload(module)
		return self._transform(diag)

	def _transform(self,diag=False):
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
		
	def compare_identity(self,other,diag=False):
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
		
	def all_of_class_as_set(self,re_class):
		result = set()
		for attribute in self.opc_children:
			result.update(getattr(self,attribute).all_of_class_as_set(re_class))
		if not re.search(re_class,str(self.__class__.__name__)) is None:
			result.add(self)
		return result
		
	def _all_of_class(self, re_class, filter_func=None):
		children = self.all_of_class_as_set(re_class)
		adopting_parent = PlasticParent('Adopting parent')
		for child in children:
			if not filter_func is None:
				if not filter_func(child): continue
			new_attr_name = approve_name_and_register_guid(adopting_parent, child, child.opc_path.replace('.','_'))
			adopting_parent.opc_children.append(new_attr_name)
			setattr(adopting_parent,new_attr_name,child)
		adopting_parent.opc_children.sort()
		return adopting_parent
		
	def all_with_path_as_set(self, re_path):
		result = set()
		for child_path in self.opc_children:
			result.update(getattr(self,child_path).all_with_path_as_set(re_path))
		try:
			if not re.search(re_path,self.opc_path) is None:
				result.add(self)
		except TypeError:
			print('Pattern')
			print(re_path)
			print('self.opc_path')
			print(self.opc_path)
			print(self.opc_children)
			print(self.__class__)
			raise TypeError
		return result
		
	def _all_with_path(self, re_path, filter_func=None):
		children = self.all_with_path_as_set(re_path)
		adopting_parent = PlasticParent('Adopting parent')
		for child in children:
			if not filter_func is None:
				if not filter_func(child): continue
			new_attr_name = approve_name_and_register_guid(adopting_parent, child, child.opc_path.replace('.', '_'))
			adopting_parent.opc_children.append(new_attr_name)
			setattr(adopting_parent,new_attr_name,child)
		adopting_parent.opc_children.sort()
		return adopting_parent

	def _all_that_pass_filter(self,filter_func):
		pass
		
	def all(self,re_path=None,re_class=None, filter_func=None):
		"""Returns all children with matching opc-path and class
		observe that the opc-path has dots '.' as separator between
		parent and child
		
		Keywords:
		re_path: The regular expression string that should be matched against the opc-path
		re_class: The regular expression string that should be matched against the class of the item
		"""
		if (re_class is None) and (re_path is None):
			return self._all_with_path('', filter_func)
		if re_class is None:
			return self._all_with_path(re_path, filter_func)
		if re_path is None:
			return self._all_of_class(re_class, filter_func)
		return self._all_with_path(re_path, filter_func)._all_of_class(re_class)
		
	def all_as_list(self,re_path=None,re_class=None, branches=True, filter_func=None):
		adopting_parent = self.all(re_path,re_class,filter_func)
		if branches:
			return [getattr(adopting_parent,child_path) for child_path in adopting_parent.opc_children]
		else:
			return [getattr(adopting_parent,child_path) for child_path in adopting_parent.opc_children
					if not hasattr(getattr(adopting_parent,child_path),'opc_children')]

	def save(self, file_name=None):
		import pickle
		file_path = settings.OPC_OBJ_PICKLE if file_name is None else settings.WORKING_DIR + file_name + '.pickle'
		with open(file_path, 'wb') as pickle_file:
			pickle.dump(self,pickle_file)

	def restore(self, file_name=None):
		import pickle
		file_path = settings.OPC_OBJ_PICKLE if file_name is None else settings.WORKING_DIR + file_name + '.pickle'
		with open(file_path, 'rb') as pickle_file:
			return pickle.load(pickle_file)

	def first_read(self, opc_cli=None, max_chunk=40):
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_read = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not ((hasattr(getattr(parent_with_all,child_path),'opc_children')) or (hasattr(getattr(parent_with_all,child_path),'name_prop')))]
		tags_to_read = [obj.opc_path for obj in obj_to_read]
		i = 0
		print("Read properties " + str(i).rjust(8) + " of " +str(len(tags_to_read)).rjust(8) + " items", end="\r")
		while len(tags_to_read) > i:
			try:
				loc_res = opc_cli.properties(tags_to_read[i:i+max_chunk])
				print("Read properties " + str(i).rjust(8) + " of " +str(len(tags_to_read)).rjust(8) + " items", end="\r")
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
		print("Read properties " + str(min(i,len(tags_to_read))).rjust(8) + " of " +str(len(tags_to_read)).ljust(8) + " items")
		return self

	def read(self, opc_cli=None, max_chunk=1000, log=True):
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

	def clear_logs(self):
		for obj in self.all_as_list(branches=False):
			obj.log = []

	def write_one_value(self, value, opc_cli=None, max_chunk=20, accept_fails=False):
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_write = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not hasattr(getattr(parent_with_all,child_path),'opc_children')]
		tags_write_data = []
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
					print("Value is of wrong data type " + str(tags_to_write[0]) + " is of type " + str(type(value)) + " while the tag is canonical type: " + str(data_type))
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

	def write(self, opc_cli=None, max_chunk=20, accept_fails=False):
		global opc_client
		if opc_cli is None:
			opc_cli = opc_client
		parent_with_all = self.all()
		obj_to_write = [getattr(parent_with_all,child_path) for child_path in parent_with_all.opc_children
					if not hasattr(getattr(parent_with_all,child_path),'opc_children')]
		tags_write_data = []
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
					print("Value is of wrong data type " + str(data_to_write[0]) + " is of type " + str(type(data_to_write[1])) + " while the tag is canonical type: " + str(data_type))
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

	def changed(self, opc_cli=None, print_all=False, max_chunk=200):
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


class PlasticParent(Generic):

	def combine_parent(self, other_parent):
		for new_child in [getattr(other_parent,child) for child in other_parent.opc_children]:
			if new_child.opc_path.replace('.','_') in self.opc_children: continue
			new_attr_name = approve_name_and_register_guid(self, new_child, new_child.opc_path.replace('.', '_'))
			self.opc_children.append(new_attr_name)
			setattr(self,new_attr_name,new_child)

	def print_values(self):
		for child in [getattr(self,path) for path in self.opc_children if not hasattr(getattr(self,path),'opc_children')]:
			print(str(child.value).ljust(15) + child.opc_path)