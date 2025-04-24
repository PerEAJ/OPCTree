OPC_SERVER = None
TOP_LEVEL = None

WORKING_DIR = 'WorkingData'
DATA_TYPES_FILE = WORKING_DIR + 'Data_Types.json'
VARS_FILE = WORKING_DIR + 'OPC_Variables.json'
IOINX_REG_FILE = WORKING_DIR + 'IOINX_Reg.json'
OPC_OBJ_PICKLE = 'opc_obj.pickle'

CONNECTED_LIBS = {
    #Name of library:Location of Excel-file with library structs
    'opc_class_lib.new_lib_name':'input\\new_lib_name.xlsx'
}

ALIASES = [
("Automatically.identified.name","Alias")
]

USED_OPC_OBJ_ATTRIBUTE_NAMES = ['opc_children','opc_path','name_prop','idx_prop','upgrade','load_children',
                                '_create_variable','transform','_transform','compare_identity']