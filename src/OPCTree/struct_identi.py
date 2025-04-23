import json
import settings

def with_alias(data_string):
	for complete_name, alias in settings.ALIASES:
		data_string = data_string.replace(complete_name,alias)
	return data_string
			
def load_known_structs():
	try:
		with open(settings.DATA_TYPES_FILE , 'r') as input_file:
			data = input_file.read()
		data = with_alias(data)
		return json.loads(data)
	except:
		return {}
	
def save_known_structs(struct_types):
	data = json.dumps(struct_types,indent=4, sort_keys=True)
	data = with_alias(data)
	with open(settings.DATA_TYPES_FILE, 'w') as output_file:
		output_file.write(data)
		
		
def get_structure(opc_variables):
	structs = []
	struct_types = load_known_structs()
	current_struct = []
	opc_id = settings.TOP_LEVEL
	old_opc_variable = None
	for opc_variable in opc_variables:
		old_opc_id = opc_id
		opc_id = opc_variable[0][2]
		length_compensation = len(opc_id.split('.')) - len(old_opc_id.split('.'))
		for idx in range(len(old_opc_id.split('.'))):
			if opc_id.rsplit('.',idx + length_compensation)[0] != old_opc_id.rsplit('.',idx)[0]:
				if idx < 1:
					if old_opc_variable is None:
						break
					data_type = old_opc_variable[7][2]
				else:
					complete_struct = str(tuple(current_struct[idx-1]))
					if not complete_struct in struct_types:
						new_name = old_opc_id.rsplit('.',idx)[0] + '_type'
						struct_types[complete_struct] = {'name': new_name}
					data_type = struct_types[complete_struct]['name']
					print(old_opc_id.rsplit('.',idx)[0] + '\t' + data_type)
					current_struct[idx-1] = []
					structs.append((old_opc_id.rsplit('.',idx)[0],data_type))
				try:
					current_struct[idx].append((old_opc_id.split('.')[-idx-1],data_type))
				except IndexError:
					try:
						current_struct.append([(old_opc_id.split('.')[-idx-1],data_type)])
					except IndexError:
						print("idx " + str(idx))
						print("opc_id" + opc_id)
						print("old_opc_id " + old_opc_id)
						exit()
			else:
				break
		old_opc_variable = opc_variable
	save_known_structs(struct_types)
	return structs
	