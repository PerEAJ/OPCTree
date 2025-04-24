from __future__ import print_function
import json
import typing

import OpenOPC
from . import opc_obj, settings
from .opc_obj import tGeneric

global opc_client


def initialize_opc_client():
	global opc_client
	opc_client = OpenOPC.client()
	if not settings.OPC_SERVER is None:
		opc_client.connect(settings.OPC_SERVER)
	else:
		opc_servers = opc_client.servers()
		if len(opc_servers) == 0:
			raise Exception("No OPC-servers available. Start the OPC-server before running this.")
		for idx, name in enumerate(opc_client.servers()):
			print(str(idx+1).ljust(5) + name)
		idx = -1
		while not 0 < int(idx) <= len(opc_servers):
			idx = input("Chose a OPC-server to connect to [1-" + str(len(opc_servers)) + "] input 'a' to abort:")
			if idx == r'a':
				raise Exception('User aborted')
		opc_client.connect(opc_servers[int(idx)-1])
	return opc_client

def connect_and_build(levels = -1):
	global opc_client
	initialize_opc_client()
	return opc_obj.Generic(settings.TOP_LEVEL).load_children(levels, opc_client)

def load_existing(file_name: str=None, working_dir=None):
	return opc_obj.restore(file_name, working_dir)

def connect_and_extract_variables():
	global nbr_loaded_vars
	nbr_loaded_vars = 0
	opc_client = OpenOPC.client()
	opc_client.connect(settings.OPC_SERVER)
	vars = _extract_variables(opc_client, settings.TOP_LEVEL)
	print()
	save_vars(vars)
	return vars

def _extract_variables(opc_client,opc_path):
	global nbr_loaded_vars
	variables = []
	result = opc_client.list(opc_path)
	for item in result:
		if opc_path in item:
			variable_properties = opc_client.properties(item)
			variables.append(variable_properties)
			nbr_loaded_vars += 1
			print('Loaded vars:' + str(nbr_loaded_vars).rjust(10) + '\t' + item + '\t\t\t\t', end="\r")
		else:
			new_path = '.'.join([opc_path,item])
			variables.extend(_extract_variables(opc_client,new_path))
	return variables
	
def load_vars():
	with open(settings.VARS_FILE, 'r') as input_file:
		data = input_file.read()
	# data = with_alias(data)
	return json.loads(data)
	
def save_vars(variables):
	data = json.dumps(variables,indent=4)
	# data = with_alias(data)
	with open(settings.VARS_FILE, 'w') as output_file:
		output_file.write(data)

def restore(file_name: typing.Optional[str]) -> tGeneric:
	return opc_obj.restore(file_name)
			
if __name__ == "__main__":
	# OPC_SERVER = 'ABB.AC800MC_OpcDaServer.3'
	# TOP_LEVEL = 'Applications.MA_SJRA_AA.App.HMI.C01'
	variables = connect_and_extract_variables()
	print(variables)