#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src import opc_obj, opc_vars


class Gen_OPC_Obj(opc_obj.Generic):
	def test(self):
		print('Is ' + self.__class__.__name__)
		
	def _transform(self, diag=False):
		if diag: print("Already transformed into " + str(self.__class__))
		return self
	
class BoolConnectionBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Bool(opc_path + '.Value', description=description + u'Value in the application ')
			self.Backtracking = opc_vars.Bool(opc_path + '.Backtracking', description=description + u'Value forced after this module ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Set if connected ')
			self.opc_children = ['Value', 'Backtracking', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class BoolConnectionForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Bool(opc_path + '.Value', description=description + u'Value in the application ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Quality information for Value ')
			self.BacktrackingPossible = opc_vars.Bool(opc_path + '.BacktrackingPossible', description=description + u'Indicates if this or an earlier module can store a backtracked value ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Set if connected ')
			self.opc_children = ['Value', 'Status', 'BacktrackingPossible', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class BoolConnection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Forward = BoolConnectionForward(opc_path + '.Forward', description=description + u'Forward direction components ')
			self.Backward = BoolConnectionBackward(opc_path + '.Backward', description=description + u'Backward direction components ')
			self.opc_children = ['Forward', 'Backward']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class Range(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Max = opc_vars.Real(opc_path + '.Max', description=description + u'Max value ')
			self.Min = opc_vars.Real(opc_path + '.Min', description=description + u'Min value ')
			self.Valid = opc_vars.Bool(opc_path + '.Valid', description=description + u'The range is valid ')
			self.Changed = opc_vars.Dint(opc_path + '.Changed', description=description + u'Is incremented when Max or Min has changed. 0<=Changed<=32768 ')
			self.Unit = opc_vars.String(opc_path + '.Unit', description=description + u'Unit on signal ')
			self.opc_children = ['Max', 'Min', 'Valid', 'Changed', 'Unit']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class CCLocInBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'The back value when not other is specified ')
			self.Backtrack = opc_vars.Bool(opc_path + '.Backtrack', description=description + u'The previous module is requested to backtrack its output ')
			self.BacktrackValue = opc_vars.Real(opc_path + '.BacktrackValue', description=description + u'The value which the previous module is requested to backtrack ')
			self.UpperLimitActive = opc_vars.Bool(opc_path + '.UpperLimitActive', description=description + u'The previous module is requested to limit its output from above ')
			self.UpperLimit = opc_vars.Real(opc_path + '.UpperLimit', description=description + u'The value to which the previous module is requested to limit its output from above ')
			self.LowerLimitActive = opc_vars.Bool(opc_path + '.LowerLimitActive', description=description + u'The previous module is requested to limit its output from below ')
			self.LowerLimit = opc_vars.Real(opc_path + '.LowerLimit', description=description + u'The value to which the previous module is requested to limit its output from below ')
			self.Range = Range(opc_path + '.Range', description=description + u'The range which is suggested as output range to the previous module if Range.Valid=True ')
			self.opc_children = ['Value', 'Backtrack', 'BacktrackValue', 'UpperLimitActive', 'UpperLimit', 'LowerLimitActive', 'LowerLimit', 'Range']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class CCLocInForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'The value of the signal from the previous module ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'The status of the signal from the previous module. 16#C0=Good, 16#50=Uncertain, 16#C=Bad ')
			self.Continuous = opc_vars.Bool(opc_path + '.Continuous', description=description + u'Indicates if the signal from the previous module is expected to be continuous ')
			self.BacktrackingPossible = opc_vars.Bool(opc_path + '.BacktrackingPossible', description=description + u'The previous module allows backtracking and limiting of its output ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'There is a previous module connected to this input ')
			self.Range = Range(opc_path + '.Range', description=description + u'Signal range ')
			self.opc_children = ['Value', 'Status', 'Continuous', 'BacktrackingPossible', 'Connected', 'Range']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class CCLocOutBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'The back value from output or external input ')
			self.Backtrack = opc_vars.Bool(opc_path + '.Backtrack', description=description + u'This module is requested to backtrack its output ')
			self.BacktrackValue = opc_vars.Real(opc_path + '.BacktrackValue', description=description + u'The value which this module is requested to backtrack ')
			self.UpperLimitActive = opc_vars.Bool(opc_path + '.UpperLimitActive', description=description + u'This module is requested to limit its output from above ')
			self.UpperLimit = opc_vars.Real(opc_path + '.UpperLimit', description=description + u'The value to which this module is requested to limit its output from above ')
			self.LowerLimitActive = opc_vars.Bool(opc_path + '.LowerLimitActive', description=description + u'This module is requested to limit its output from below ')
			self.LowerLimit = opc_vars.Real(opc_path + '.LowerLimit', description=description + u'The value to which this module is requested to limit its output from below ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'There is a succeeding module connected to this output ')
			self.Range = Range(opc_path + '.Range', description=description + u'The range which is suggested as output range for this module if Range.Valid=True ')
			self.opc_children = ['Value', 'Backtrack', 'BacktrackValue', 'UpperLimitActive', 'UpperLimit', 'LowerLimitActive', 'LowerLimit', 'Connected', 'Range']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class CCLocOutForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'The value of the signal from the previous module ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'The status of the signal from the previous module. 16#C0=Good, 16#50=Uncertain, 16#C=Bad ')
			self.Continuous = opc_vars.Bool(opc_path + '.Continuous', description=description + u'Indicates if the signal from the previous module is expected to be continuous ')
			self.BacktrackingPossible = opc_vars.Bool(opc_path + '.BacktrackingPossible', description=description + u'The previous module allows backtracking and limiting of its output ')
			self.Range = Range(opc_path + '.Range', description=description + u'Signal range ')
			self.opc_children = ['Value', 'Status', 'Continuous', 'BacktrackingPossible', 'Range']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class Comm_Channel(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Valid = opc_vars.Bool(opc_path + '.Valid', description=description + u'Used to inform the connected Read/Write FBs that a connection is established ')
			self.opc_children = ['Valid']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ControlConnectionBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'The forced value (only used if Backtracking is true) ')
			self.Backtracking = opc_vars.Bool(opc_path + '.Backtracking', description=description + u'Value forced after this module ')
			self.MaxReached = opc_vars.Bool(opc_path + '.MaxReached', description=description + u'Informs previous modules that the signal may not be any higher ')
			self.MinReached = opc_vars.Bool(opc_path + '.MinReached', description=description + u'Informs previous modules that the signal may not be any lower ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Informs if the the output has a connected module ')
			self.Range = Range(opc_path + '.Range', description=description + u'Measuring range ')
			self.opc_children = ['Value', 'Backtracking', 'MaxReached', 'MinReached', 'Connected', 'Range']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ControlConnectionForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Real(opc_path + '.Value', description=description + u'Forward value ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Quality information for Value ')
			self.Forced = opc_vars.Bool(opc_path + '.Forced', description=description + u'Value forced before this module ')
			self.BacktrackingPossible = opc_vars.Bool(opc_path + '.BacktrackingPossible', description=description + u'Indicate if this or an earlier module can store a backtracked value ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Informs if the the input has a connected module ')
			self.Range = Range(opc_path + '.Range', description=description + u'Measuring range ')
			self.opc_children = ['Value', 'Status', 'Forced', 'BacktrackingPossible', 'Connected', 'Range']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ControlConnection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Forward = ControlConnectionForward(opc_path + '.Forward', description=description + u'Forward component in control loop internal connection ')
			self.Backward = ControlConnectionBackward(opc_path + '.Backward', description=description + u'Backward component in control loop internal connection ')
			self.opc_children = ['Forward', 'Backward']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class CVAckISPPar(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.ResetAllGroups = opc_vars.Bool(opc_path + '.ResetAllGroups', description=description + u'Reset of latched communication variables in all chained groups. Affected from the first group in chain ')
			self.ResetGroup = opc_vars.Bool(opc_path + '.ResetGroup', description=description + u'Reset of latched communication variables in the defined group ')
			self.opc_children = ['ResetAllGroups', 'ResetGroup']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ForcedSignalsPar(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.ResetAllApplForces = opc_vars.Bool(opc_path + '.ResetAllApplForces', description=description + u'Reset all forced I/O signals in the application ')
			self.ResetAllControllerForces = opc_vars.Bool(opc_path + '.ResetAllControllerForces', description=description + u'Reset all forced I/O signals in the controller ')
			self.opc_children = ['ResetAllApplForces', 'ResetAllControllerForces']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class IntegerConnectionBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Dint(opc_path + '.Value', description=description + u'Value in the application ')
			self.Backtracking = opc_vars.Bool(opc_path + '.Backtracking', description=description + u'Value forced after this module ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Set if connected ')
			self.opc_children = ['Value', 'Backtracking', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class IntegerConnectionForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Value = opc_vars.Dint(opc_path + '.Value', description=description + u'Value in the application ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'Quality information for Value ')
			self.BacktrackingPossible = opc_vars.Bool(opc_path + '.BacktrackingPossible', description=description + u'Indicates if this or an earlier module can store a backtracked value ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Set if connected ')
			self.opc_children = ['Value', 'Status', 'BacktrackingPossible', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class IntegerConnection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Forward = IntegerConnectionForward(opc_path + '.Forward', description=description + u'Forward direction components ')
			self.Backward = IntegerConnectionBackward(opc_path + '.Backward', description=description + u'Backward direction components ')
			self.opc_children = ['Forward', 'Backward']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class Level6Connection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.HHHrelative = opc_vars.Real(opc_path + '.HHHrelative', description=description)
			self.HHrelative = opc_vars.Real(opc_path + '.HHrelative', description=description)
			self.Hrelative = opc_vars.Real(opc_path + '.Hrelative', description=description)
			self.Lrelative = opc_vars.Real(opc_path + '.Lrelative', description=description)
			self.LLrelative = opc_vars.Real(opc_path + '.LLrelative', description=description)
			self.LLLrelative = opc_vars.Real(opc_path + '.LLLrelative', description=description)
			self.LevelLH = opc_vars.Bool(opc_path + '.LevelLH', description=description + u'Set if Hlimit or Llimit is reached ')
			self.LevelLLHH = opc_vars.Bool(opc_path + '.LevelLLHH', description=description + u'Set if HHlimit or LLlimit is reached ')
			self.LevelLLLHHH = opc_vars.Bool(opc_path + '.LevelLLLHHH', description=description + u'Set if HHHlimit or LLLlimit is reached ')
			self.opc_children = ['HHHrelative', 'HHrelative', 'Hrelative', 'Lrelative', 'LLrelative', 'LLLrelative', 'LevelLH', 'LevelLLHH', 'LevelLLLHHH']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ProcObjConnectionBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Ready = opc_vars.Bool(opc_path + '.Ready', description=description + u'The process object is ready in GroupStart mode ')
			self.Started = opc_vars.Bool(opc_path + '.Started', description=description + u'Feedback that the process object has started ')
			self.Stopped = opc_vars.Bool(opc_path + '.Stopped', description=description + u'Feedback that the process object has stopped ')
			self.AlarmInObject = opc_vars.Bool(opc_path + '.AlarmInObject', description=description + u'Any alarm exist in the process object ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'A process object is connected ')
			self.opc_children = ['Ready', 'Started', 'Stopped', 'AlarmInObject', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ProcObjConnectionForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.SelectGroupStart = opc_vars.Bool(opc_path + '.SelectGroupStart', description=description + u'Order the process object into GroupStart mode ')
			self.AlarmAck = opc_vars.Bool(opc_path + '.AlarmAck', description=description + u'Acknowledge of all alarms ')
			self.Start = opc_vars.Bool(opc_path + '.Start', description=description + u'Start order to the Process object ')
			self.EnableObjectAlarm = opc_vars.Bool(opc_path + '.EnableObjectAlarm', description=description + u'On edge update enable alarm in object ')
			self.EnableModeSwitch = opc_vars.Bool(opc_path + '.EnableModeSwitch', description=description + u'Mode switches are enabled in the process object ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'A process object is connected ')
			self.opc_children = ['SelectGroupStart', 'AlarmAck', 'Start', 'EnableObjectAlarm', 'EnableModeSwitch', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class ProcObjConnection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Forward = ProcObjConnectionForward(opc_path + '.Forward', description=description + u'Data to the process object ')
			self.Backward = ProcObjConnectionBackward(opc_path + '.Backward', description=description + u'Data from the process object ')
			self.opc_children = ['Forward', 'Backward']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class SetDTPar(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.UseAbsoluteDT = opc_vars.Bool(opc_path + '.UseAbsoluteDT', description=description + u'Select if the new absolute date and time should be used ')
			self.UseAbsLocalDT = opc_vars.Bool(opc_path + '.UseAbsLocalDT', description=description + u'The specified date and time is a local time if True otherwise it is a system time ')
			self.NewAbsDT = opc_vars.Date_And_Time(opc_path + '.NewAbsDT', description=description + u'Date and time to be set if UseAbsoluteDT is True ')
			self.NewRelDT = opc_vars.Time(opc_path + '.NewRelDT', description=description + u'Date and time difference to be set if UseAbsoluteDT is False ')
			self.opc_children = ['UseAbsoluteDT', 'UseAbsLocalDT', 'NewAbsDT', 'NewRelDT']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class SignalState(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Act = opc_vars.Bool(opc_path + '.Act', description=description + u'Indicates that the level limits are exceeded and that the signal differs from normal if a Boolean signal, enabled and not inhibited ')
			self.Enabled = opc_vars.Bool(opc_path + '.Enabled', description=description + u'Level enabled ')
			self.Inhibited = opc_vars.Bool(opc_path + '.Inhibited', description=description + u'Level inhibited ')
			self.ALState = opc_vars.Dint(opc_path + '.ALState', description=description + u'The state of the alarm point in the signal object (0-6) ')
			self.opc_children = ['Act', 'Enabled', 'Inhibited', 'ALState']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class SystemDiagnosticsSMPar(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.UpdateInterval = opc_vars.Time(opc_path + '.UpdateInterval', description=description + u'Update interval in minutes ')
			self.CyclicUpdate = opc_vars.Bool(opc_path + '.CyclicUpdate', description=description + u'Tells if cyclic update ')
			self.Update = opc_vars.Bool(opc_path + '.Update', description=description + u'Updates the interaction window ')
			self.Reset = opc_vars.Bool(opc_path + '.Reset', description=description + u'Resets the FDRT extream values ')
			self.opc_children = ['UpdateInterval', 'CyclicUpdate', 'Update', 'Reset']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class VoteConnectionBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.ResetOverride = opc_vars.Bool(opc_path + '.ResetOverride', description=description + u'Resets overrides upsteams ')
			self.ResetOverrideEnabled = opc_vars.Bool(opc_path + '.ResetOverrideEnabled', description=description + u'Indicates if overrides exists downsteams ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Flag used to determine connected output, set by connected module ')
			self.opc_children = ['ResetOverride', 'ResetOverrideEnabled', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class VoteConnectionForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Name = opc_vars.String(opc_path + '.Name', description=description + u'Name of connected Signal object ')
			self.GTHHH = SignalState(opc_path + '.GTHHH', description=description + u'Only relevant for connections of real type ')
			self.GTHH = SignalState(opc_path + '.GTHH', description=description + u'Only relevant for connections of real type ')
			self.GTH = SignalState(opc_path + '.GTH', description=description + u'Only relevant for connections of real type ')
			self.DiffNormal = SignalState(opc_path + '.DiffNormal', description=description + u'Only relevant for connections of boolean type ')
			self.LTL = SignalState(opc_path + '.LTL', description=description + u'Only relevant for connections of real type ')
			self.LTLL = SignalState(opc_path + '.LTLL', description=description + u'Only relevant for connections of real type ')
			self.LTLLL = SignalState(opc_path + '.LTLLL', description=description + u'Only relevant for connections of real type ')
			self.RealValue = opc_vars.Real(opc_path + '.RealValue', description=description + u'Value if connected Signal object is of type Real or RealIO ')
			self.Status = opc_vars.Dword(opc_path + '.Status', description=description + u'IO.Status from connected Signal object ')
			self.Forced = opc_vars.Bool(opc_path + '.Forced', description=description + u'IO.Forced from connected Signal object ')
			self.RealType = opc_vars.Dint(opc_path + '.RealType', description=description + u'Signal object type. 0: Bool, >0: Real (With number of RealType High/Low levels). ')
			self.ResetOverrideEnabled = opc_vars.Bool(opc_path + '.ResetOverrideEnabled', description=description + u'Indicates if overrides exists upsteams ')
			self.ResetOverride = opc_vars.Bool(opc_path + '.ResetOverride', description=description + u'Resets overrides downsteams ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Set if connected ')
			self.opc_children = ['Name', 'GTHHH', 'GTHH', 'GTH', 'DiffNormal', 'LTL', 'LTLL', 'LTLLL', 'RealValue', 'Status', 'Forced', 'RealType', 'ResetOverrideEnabled', 'ResetOverride', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class VoteConnection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Forward = VoteConnectionForward(opc_path + '.Forward', description=description + u'Forward direction components ')
			self.Backward = VoteConnectionBackward(opc_path + '.Backward', description=description + u'Backward direction components ')
			self.opc_children = ['Forward', 'Backward']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class VotedConnectionBackward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Reset = opc_vars.Bool(opc_path + '.Reset', description=description + u'Reset command ')
			self.ResetEnabled = opc_vars.Bool(opc_path + '.ResetEnabled', description=description + u'Indicates that latches in the SIS loop may be reset ')
			self.ResetOverride = opc_vars.Bool(opc_path + '.ResetOverride', description=description + u'Resets overrides upsteams ')
			self.ResetOverrideEnabled = opc_vars.Bool(opc_path + '.ResetOverrideEnabled', description=description + u'Indicates if overrides exists downsteams ')
			self.BrokenConnection = opc_vars.Dword(opc_path + '.BrokenConnection', description=description + u'Used to indicate a broken connection and a connection status ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Flag used to determine connected output, set by connected module ')
			self.opc_children = ['Reset', 'ResetEnabled', 'ResetOverride', 'ResetOverrideEnabled', 'BrokenConnection', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class VotedConnectionForward(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.LatchedCmd = opc_vars.Bool(opc_path + '.LatchedCmd', description=description + u'Latched command ')
			self.Cmd = opc_vars.Bool(opc_path + '.Cmd', description=description + u'Unlatched command ')
			self.CmdNumber = opc_vars.Dint(opc_path + '.CmdNumber', description=description + u'Command number for process state change ')
			self.Reset = opc_vars.Bool(opc_path + '.Reset', description=description + u'Reset command ')
			self.ResetEnabled = opc_vars.Bool(opc_path + '.ResetEnabled', description=description + u'Indicates that latches in the SIS loop may be reset ')
			self.ResetOverrideEnabled = opc_vars.Bool(opc_path + '.ResetOverrideEnabled', description=description + u'Indicates if overrides exists upsteams ')
			self.ResetOverride = opc_vars.Bool(opc_path + '.ResetOverride', description=description + u'Resets overrides downsteams ')
			self.BrokenConnection = opc_vars.Dword(opc_path + '.BrokenConnection', description=description + u'Used to indicate a broken connection and a connection status ')
			self.Connected = opc_vars.Bool(opc_path + '.Connected', description=description + u'Flag used to determine connected inputs, set by connected module ')
			self.opc_children = ['LatchedCmd', 'Cmd', 'CmdNumber', 'Reset', 'ResetEnabled', 'ResetOverrideEnabled', 'ResetOverride', 'BrokenConnection', 'Connected']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				
class VotedConnection(Gen_OPC_Obj):

	def __init__(self,opc_path, predecessor=None, description=u'', sig_range=None):
		self.opc_path = opc_path
		self.description = description
		self.sig_range = sig_range
		if predecessor is None:
			self.Forward = VotedConnectionForward(opc_path + '.Forward', description=description + u'Forward direction components ')
			self.Backward = VotedConnectionBackward(opc_path + '.Backward', description=description + u'Backward direction components ')
			self.opc_children = ['Forward', 'Backward']		
		else:
			for attribute in [a for a in dir(predecessor) if not a.startswith('__') and not callable(getattr(predecessor,a))]:
				setattr(self,attribute,getattr(predecessor,attribute))
				