OPC_SERVER = 'ABB.AC800MC_OpcDaServer.3'
TOP_LEVEL = 'Applications'

WORKING_DIR = 'WorkingData//'
DATA_TYPES_FILE = WORKING_DIR + 'Data_Types.json'
VARS_FILE = WORKING_DIR + 'OPC_Variables.json'
IOINX_REG_FILE = WORKING_DIR + 'IOINX_Reg.json'
OPC_OBJ_PICKLE = WORKING_DIR + 'opc_obj.pickle'

CONNECTED_LIBS = {
    #Name of library:Location of Excel-file with library structs
    'opc_class_lib.new_lib_name':'input\\new_lib_name.xlsx'
}

ALIASES = [
("Automatically.identified.name","Alias")
]