#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src import opc_obj, opc_vars


class Gen_OPC_Obj(opc_obj.Generic):
	def test(self):
		print('Is ' + self.__class__.__name__)
		
	def _transform(self, diag=False):
		if diag: print("Already transformed into " + str(self.__class__))
		return self
	
class Boolean8(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.B0 = opc_vars.Bool(opc_path + '.B0', description=description + u'LSB in the parameter used for type conversion ')
			self.B1 = opc_vars.Bool(opc_path + '.B1', description=description)
			self.B2 = opc_vars.Bool(opc_path + '.B2', description=description)
			self.B3 = opc_vars.Bool(opc_path + '.B3', description=description)
			self.B4 = opc_vars.Bool(opc_path + '.B4', description=description)
			self.B5 = opc_vars.Bool(opc_path + '.B5', description=description)
			self.B6 = opc_vars.Bool(opc_path + '.B6', description=description)
			self.B7 = opc_vars.Bool(opc_path + '.B7', description=description + u'MSB in the parameter used for type conversion ')
			self.opc_children = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class Boolean16(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.B0 = opc_vars.Bool(opc_path + '.B0', description=description + u'LSB in the parameter used for type conversion ')
			self.B1 = opc_vars.Bool(opc_path + '.B1', description=description)
			self.B2 = opc_vars.Bool(opc_path + '.B2', description=description)
			self.B3 = opc_vars.Bool(opc_path + '.B3', description=description)
			self.B4 = opc_vars.Bool(opc_path + '.B4', description=description)
			self.B5 = opc_vars.Bool(opc_path + '.B5', description=description)
			self.B6 = opc_vars.Bool(opc_path + '.B6', description=description)
			self.B7 = opc_vars.Bool(opc_path + '.B7', description=description)
			self.B8 = opc_vars.Bool(opc_path + '.B8', description=description)
			self.B9 = opc_vars.Bool(opc_path + '.B9', description=description)
			self.B10 = opc_vars.Bool(opc_path + '.B10', description=description)
			self.B11 = opc_vars.Bool(opc_path + '.B11', description=description)
			self.B12 = opc_vars.Bool(opc_path + '.B12', description=description)
			self.B13 = opc_vars.Bool(opc_path + '.B13', description=description)
			self.B14 = opc_vars.Bool(opc_path + '.B14', description=description)
			self.B15 = opc_vars.Bool(opc_path + '.B15', description=description + u'MSB in the parameter used for type conversion ')
			self.opc_children = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class Boolean32(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.B0 = opc_vars.Bool(opc_path + '.B0', description=description + u'LSB in the parameter used for type conversion ')
			self.B1 = opc_vars.Bool(opc_path + '.B1', description=description)
			self.B2 = opc_vars.Bool(opc_path + '.B2', description=description)
			self.B3 = opc_vars.Bool(opc_path + '.B3', description=description)
			self.B4 = opc_vars.Bool(opc_path + '.B4', description=description)
			self.B5 = opc_vars.Bool(opc_path + '.B5', description=description)
			self.B6 = opc_vars.Bool(opc_path + '.B6', description=description)
			self.B7 = opc_vars.Bool(opc_path + '.B7', description=description)
			self.B8 = opc_vars.Bool(opc_path + '.B8', description=description)
			self.B9 = opc_vars.Bool(opc_path + '.B9', description=description)
			self.B10 = opc_vars.Bool(opc_path + '.B10', description=description)
			self.B11 = opc_vars.Bool(opc_path + '.B11', description=description)
			self.B12 = opc_vars.Bool(opc_path + '.B12', description=description)
			self.B13 = opc_vars.Bool(opc_path + '.B13', description=description)
			self.B14 = opc_vars.Bool(opc_path + '.B14', description=description)
			self.B15 = opc_vars.Bool(opc_path + '.B15', description=description)
			self.B16 = opc_vars.Bool(opc_path + '.B16', description=description)
			self.B17 = opc_vars.Bool(opc_path + '.B17', description=description)
			self.B18 = opc_vars.Bool(opc_path + '.B18', description=description)
			self.B19 = opc_vars.Bool(opc_path + '.B19', description=description)
			self.B20 = opc_vars.Bool(opc_path + '.B20', description=description)
			self.B21 = opc_vars.Bool(opc_path + '.B21', description=description)
			self.B22 = opc_vars.Bool(opc_path + '.B22', description=description)
			self.B23 = opc_vars.Bool(opc_path + '.B23', description=description)
			self.B24 = opc_vars.Bool(opc_path + '.B24', description=description)
			self.B25 = opc_vars.Bool(opc_path + '.B25', description=description)
			self.B26 = opc_vars.Bool(opc_path + '.B26', description=description)
			self.B27 = opc_vars.Bool(opc_path + '.B27', description=description)
			self.B28 = opc_vars.Bool(opc_path + '.B28', description=description)
			self.B29 = opc_vars.Bool(opc_path + '.B29', description=description)
			self.B30 = opc_vars.Bool(opc_path + '.B30', description=description)
			self.B31 = opc_vars.Bool(opc_path + '.B31', description=description + u'MSB in the parameter used for type conversion ')
			self.opc_children = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class BoolIO(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Bool(opc_path + '.Value', description=description + u'Value in the application ')
			self.IOValue = opc_vars.Bool(opc_path + '.IOValue', description=description + u'Value from I/O before forcing ')
			self.Forced = opc_vars.Bool(opc_path + '.Forced', description=description + u'Tells if the input is forced or not ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Error status ')
			self.opc_children = ['Value', 'IOValue', 'Forced', 'Status']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class CalendarStruct(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Year = opc_vars.Dint(opc_path + '.Year', description=description + u'Year 1980 -> ')
			self.Month = opc_vars.Dint(opc_path + '.Month', description=description + u'Month 1 - 12 ')
			self.Day = opc_vars.Dint(opc_path + '.Day', description=description + u'Day 1 - 31 ')
			self.Hour = opc_vars.Dint(opc_path + '.Hour', description=description + u'Hour 0 - 23 ')
			self.Minute = opc_vars.Dint(opc_path + '.Minute', description=description + u'Minute 0 - 59 ')
			self.Second = opc_vars.Dint(opc_path + '.Second', description=description + u'Second 0 - 59 ')
			self.MilliSecond = opc_vars.Dint(opc_path + '.MilliSecond', description=description + u'Millisecond 0 - 999 ')
			self.WeekDayNo = opc_vars.Dint(opc_path + '.WeekDayNo', description=description + u'1=Monday, 2=Tuesday, ..., 7=Sunday ')
			self.WeekNo = opc_vars.Dint(opc_path + '.WeekNo', description=description + u'Week number 1 - 53 ')
			self.IsLeapYear = opc_vars.Bool(opc_path + '.IsLeapYear', description=description + u'Indicates if Year is leap year ')
			self.opc_children = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'MilliSecond', 'WeekDayNo', 'WeekNo', 'IsLeapYear']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class DintIO(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Dint(opc_path + '.Value', description=description + u'Value in the application ')
			self.IOValue = opc_vars.Dint(opc_path + '.IOValue', description=description + u'Value from I/O before forcing ')
			self.Forced = opc_vars.Bool(opc_path + '.Forced', description=description + u'Tells if the input is forced or not ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Error status ')
			self.opc_children = ['Value', 'IOValue', 'Forced', 'Status']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class DwordIO(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Dword(opc_path + '.Value', description=description + u'Value in the application ')
			self.IOValue = opc_vars.Dword(opc_path + '.IOValue', description=description + u'Value from I/O before forcing ')
			self.Forced = opc_vars.Bool(opc_path + '.Forced', description=description + u'Tells if the input is forced or not ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Error status ')
			self.opc_children = ['Value', 'IOValue', 'Forced', 'Status']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class HwStatus(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.HwState = opc_vars.Dint(opc_path + '.HwState', description=description + u'Indicates errors or warnings on HW unit ')
			self.HwStateChangeTime = opc_vars.Date_And_Time(opc_path + '.HwStateChangeTime', description=description + u'Time for error change ')
			self.ErrorsAndWarnings = opc_vars.Dword(opc_path + '.ErrorsAndWarnings', description=description + u'Describes actual errors or warnings on HW unit ')
			self.ExtendedStatus = opc_vars.Dword(opc_path + '.ExtendedStatus', description=description + u'Additional information on HW unit ')
			self.LatchedErrorsAndWarnings = opc_vars.Dword(opc_path + '.LatchedErrorsAndWarnings', description=description + u'Actual errors or warnings since last acknowledge ')
			self.LatchedExtendedStatus = opc_vars.Dword(opc_path + '.LatchedExtendedStatus', description=description + u'Additional information since last acknowledge ')
			self.opc_children = ['HwState', 'HwStateChangeTime', 'ErrorsAndWarnings', 'ExtendedStatus', 'LatchedErrorsAndWarnings', 'LatchedExtendedStatus']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class SignalPar(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Max = opc_vars.Real(opc_path + '.Max', description=description + u'Max value ')
			self.Min = opc_vars.Real(opc_path + '.Min', description=description + u'Min value ')
			self.Inverted = opc_vars.Bool(opc_path + '.Inverted', description=description + u'Tells if input is inverted ')
			self.Fraction = opc_vars.Dint(opc_path + '.Fraction', description=description + u'Signal fraction ')
			self.Unit = opc_vars.String(opc_path + '.Unit', description=description + u'Unit of the signal ')
			self.opc_children = ['Max', 'Min', 'Inverted', 'Fraction', 'Unit']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class RealIO(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'Value in the application ')
			self.IOValue = opc_vars.Real(opc_path + '.IOValue', description=description + u'Value from I/O before forcing ')
			self.Forced = opc_vars.Bool(opc_path + '.Forced', description=description + u'Tells if the input is forced or not ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Error status ')
			self.Parameters = SignalPar(opc_path + '.Parameters', description=description + u'Measuring range ')
			self.opc_children = ['Value', 'IOValue', 'Forced', 'Status', 'Parameters']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class TimeZoneInfo(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.TimeZoneDiff = opc_vars.Dint(opc_path + '.TimeZoneDiff', description=description + u'Specifies the difference between local time and UTC time in minutes. ')
			self.StandardName = opc_vars.String(opc_path + '.StandardName', description=description + u'Associates a name for the standard time. ')
			self.StandardDT = CalendarStruct(opc_path + '.StandardDT', description=description + u'Specifies the date and time when the transition from daylight time to standard time occurs. ')
			self.StandardDiff = opc_vars.Dint(opc_path + '.StandardDiff', description=description + u'Specifies a difference (in minutes) to be used for local time translation during standard time. ')
			self.DaylightName = opc_vars.String(opc_path + '.DaylightName', description=description + u'Associates a name for the daylight time. ')
			self.DaylightDT = CalendarStruct(opc_path + '.DaylightDT', description=description + u'Specifies the date and time when the transition from standard time to daylight time occurs. ')
			self.DaylightDiff = opc_vars.Dint(opc_path + '.DaylightDiff', description=description + u'Specifies a difference to be used for local time translation during daylight time. ')
			self.opc_children = ['TimeZoneDiff', 'StandardName', 'StandardDT', 'StandardDiff', 'DaylightName', 'DaylightDT', 'DaylightDiff']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				