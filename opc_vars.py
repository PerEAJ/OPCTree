import sys, re
from importlib import reload



class OpcVariable(object):
	opc_path = None
	
	def __init__(self,opc_path,predecessor = None, description = '', opc_properties=None):
		self.opc_path = opc_path
		self.description = description
		if opc_properties is not None:
			self.name_prop = dict([(PropertyName,PropertyValue) for (PropertyId,PropertyName,PropertyValue) in opc_properties])
			self.idx_prop = dict([(PropertyId, PropertyValue) for (PropertyId, PropertyName, PropertyValue) in opc_properties])
			self.value = self.name_prop['Item Value']
		# self.opc_properties = opc_properties
		if not predecessor is None:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
	def upgrade(self):
		reload(sys.modules[self.__class__.__module__])
		self_class = getattr(sys.modules[self.__class__.__module__],self.__class__.__name__)
		new_self = self_class(self.opc_path,self)
		self.__dict__.update(new_self.__dict__)
		return new_self
		
	def _transform(self):
		if not hasattr(self, 'name_prop'):
			return self
		elif self.name_prop['Item Type Name'] == u'bool':
			return Bool(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'int':
			return Int(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'dint':
			return Dint(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'real':
			return Real(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'date_and_time':
			return Date_And_Time(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'time':
			return Time(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'uint':
			return Uint(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'string':
			return String(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'word':
			return Word(opc_path=self.opc_path, predecessor=self)
		elif self.name_prop['Item Type Name'] == u'dword':
			return Dword(opc_path=self.opc_path, predecessor=self)
		return self

	def _rename_in_opc_path(self, new_name: str, level: int):
		split_path = self.opc_path.split('.')
		split_path[level-1] = new_name
		self.opc_path = '.'.join(split_path)
		return self
		
	def all_of_class_as_set(self,re_class):
		if not re.search(re_class,str(self.__class__.__name__)) is None:
			return set([self])
		return set()
		
	def all_with_path_as_set(self,re_path):
		if re_path is None:
			return set([self])
		try:
			if not re.search(re_path,self.opc_path) is None:
				return set([self])
		except TypeError:
			print("re_path: " + str(re_path) + " , self.opc_path: " + str(self.opc_path))
			raise TypeError
		return set()
		
class AnalogVar(OpcVariable):

	def __init__(self,opc_path,predecessor = None, description = '', sig_range= {}, parameter=''):
		self.opc_path = opc_path
		self.description = description + ', ' + parameter if not parameter == '' else description
		self.description = self.description.replace(' ,',',').replace('  ',' ')
		self.min = sig_range['Min'] if not sig_range is None and 'Min' in sig_range else 0
		self.max = sig_range['Max'] if not sig_range is None and 'Max' in sig_range else 1000000
		self.unit = sig_range['Unit'] if not sig_range is None and 'Unit' in sig_range else ''
		if not predecessor is None:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))

class Bool(OpcVariable):

	def __init__(self,opc_path,predecessor = None, description = '', parameter=''):
		self.opc_path = opc_path
		self.description = description + ', ' + parameter if not parameter == '' else description
		self.description = self.description.replace(' ,',',').replace('  ',' ')
		if not predecessor is None:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))

class Int(AnalogVar):
	pass

class Dint(AnalogVar):
	pass
	
class Real(AnalogVar):
	pass
	
class Time(AnalogVar):
	pass

class Date_And_Time(OpcVariable):
	pass
	
class Uint(AnalogVar):
	pass

class String(OpcVariable):
	pass

class Word(OpcVariable):
	pass

class Dword(OpcVariable):
	pass
