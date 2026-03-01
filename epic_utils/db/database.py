import struct
from .datatype import DB_Str, DB_Array, DB_Value, DB_UInt
from datetime import datetime

MAGICNUMBER = "EPDB".encode("utf-8")
HEADER_IDENT = "HEAD".encode("utf-8")
DATA_IDENT = "DATA".encode("utf-8")
END_IDENT = "STOP".encode("utf-8")
DATEFORMAT = "%d%m%Y%H%M"
FORMAT_VERSION = 2 #Version 1 is simple format with only basic data types. Version 2 allows for more complex data types like arrays
		
class DBObject:
	def __init__(self):
		pass
		
	def get_values(self):
		"""
			return: Array -> [attribute_name, attribute_type, attribute_value]
		"""
		result = []
		children = vars(self)
		keys = list(children.keys())
		keys.sort()
		for name in keys:
			value = getattr(self, name)
			typ = type(value)
			try:
				_ = getattr(typ, "DB_IDENT")
				result.append([name, typ, value.get()])
			except AttributeError:
				pass
				#Not a valid value to store
		return result

class DBTable:
	def __init__(self, index, key_name, object):
		self.index = index
		self.key_name = key_name
		self.object = object
		_object = object()
		
		self.key_type = type(getattr(_object, self.key_name))
		_values = _object.get_values()
		self.columns = [[temp[0], temp[1].DB_IDENT] for temp in _values] # [name, type]
		
		self.values = {}
		
	def insert(self, object):
		if not isinstance(object, self.object):
			raise TypeError(f"Invalid type. Expected <{self.object.__name__}> got <{type(object).__name__}>")
			#return # can only store provided objects
		key = getattr(object, self.key_name)
		if key.get() in self.values.keys():
			raise IndexError(f"Key already exists in table")
		self.values[key.get()] = object

	def get(self, key):
		if getattr(type(key), "FORMAT", -1) == -1 or type(key).DB_IDENT != self.key_type.DB_IDENT:
			raise IndexError("Invalid key")
		return self.values[key.get()]
		
class Database():
	def __init__(self, filename, FORMAT = FORMAT_VERSION):
		if(FORMAT < 1 or FORMAT > FORMAT_VERSION or not isinstance(FORMAT, int)):
			raise ValueError("Invalid Database format")
		self.format = FORMAT
		self.tables: list[DBTable] = []
		self.filename = filename

	def get_table(self, index: int):
		for table in self.tables:
			if table.index == index:
				return table
	
	def insert(self, table_index, object):
		table = self.get_table(table_index)
		if table == None:
			raise IndexError("Table index doesnt exist")
		table.insert(object)

	def get(self, table_index: int, key: DB_Value):
		table = self.get_table(table_index)
		if table == None:
			raise Exception("Table index does not exist")
		return table.get(key)

	def register_table(self, index: int, key_name: str, object: any):
		for table in self.tables:
			if table.index == index:
				raise IndexError("Table indices must be unique")
		self.tables.append(DBTable(index, key_name, object))
	
	def save(self):
		#struct types (for myself because i cant f*cking remember, B = 1Byte, H = 2Bytes. I=4Bytes)
		with open(self.filename, "wb") as file:
			file.write(MAGICNUMBER) # identify file type
			file.write(struct.pack(">B", 0)) #Space
			file.write(HEADER_IDENT) # header
			file.write(struct.pack(">B", FORMAT_VERSION)) #format version (current v = 1)
			if self.format == 1:	
				file.write(struct.pack(">I", len(self.tables))) #table count
				file.write(datetime.now().strftime(DATEFORMAT).encode("utf-8")) # save time
				
				file.write(DATA_IDENT) # data
				
				for table in self.tables:
					file.write(struct.pack(">I", table.index)) # table index -> later used to identify tables
					file.write(struct.pack(">B", table.key_type.DB_IDENT)) #key type
					file.write(struct.pack(">H", len(table.key_name))) # key length (maybe change to 1 Byte length?)
					file.write(table.key_name.encode("utf-8")) # key name
					file.write(struct.pack(">B", len(table.columns))) # number of attributes				
					file.write(struct.pack(">I", len(table.values.keys()))) # number of entries
					for col in table.columns:
						file.write(struct.pack(">B", col[1])) # attribute type
						file.write(struct.pack(">H", len(col[0]))) # name length of attribute (maybe also change to 1 Byte?)
						file.write(col[0].encode("utf-8")) # attribute name
					for key in table.values.keys():
						file.write(table.key_type(value=key).getBytes()) # key (only int/float allowed for now as I need to implement keys with variable length)
						object = table.values[key]
						for col in table.columns:
							if col[1] == DB_Str.DB_IDENT:
								file.write(struct.pack(">I", getattr(object, col[0]).getAllocation()[0])) # value length
								file.write(getattr(object, col[0]).getBytes())
							else:
								file.write(getattr(object, col[0]).getBytes()) # value of each coloumn (also no variable length now)
				
			elif self.format == 2:
				file.write(struct.pack(">I", len(self.tables))) #table count
				file.write(datetime.now().strftime(DATEFORMAT).encode("utf-8")) # save time
				
				file.write(DATA_IDENT) # data
				
				for table in self.tables:
					file.write(struct.pack(">I", table.index)) # table index -> later used to identify tables
					file.write(struct.pack(">B", table.key_type.DB_IDENT)) #key type
					file.write(struct.pack(">H", len(table.key_name))) # key length (maybe change to 1 Byte length?)
					file.write(table.key_name.encode("utf-8")) # key name
					file.write(struct.pack(">B", len(table.columns))) # number of attributes				
					file.write(struct.pack(">I", len(table.values.keys()))) # number of entries
					for col in table.columns:
						file.write(struct.pack(">B", col[1])) # attribute type
						file.write(struct.pack(">H", len(col[0]))) # name length of attribute (maybe also change to 1 Byte?)
						file.write(col[0].encode("utf-8")) # attribute name
					for key in table.values.keys():
						file.write(table.key_type(value=key).getBytes()) # key (only int/float allowed for now as I need to implement keys with variable length)
						object = table.values[key]
						for col in table.columns:
							if col[1] == DB_Str.DB_IDENT:
								file.write(struct.pack(">I", getattr(object, col[0]).getAllocation()[0])) # value length
								file.write(getattr(object, col[0]).getBytes())
							elif col[1] == DB_Array.DB_IDENT:
								arr = getattr(object, col[0])
								file.write(struct.pack(">I", arr.length)) # Length of Array
								file.write(struct.pack(">B", arr.typ.DB_IDENT))
								if arr.typ.DB_IDENT == DB_Str.DB_IDENT:
									for i in range(0, arr.length):
										file.write(struct.pack(">I", arr[i].getAllocation()[0]))
										file.write(arr[i].getBytes())
								else:
									for i in range(0, arr.length):
										file.write(arr[i].getBytes())
							else:
								file.write(getattr(object, col[0]).getBytes()) # value of each coloumn (also no variable length now)
			file.write(END_IDENT)
			
	def read(self):
		for table in self.tables:
			table.values = {}
		with open(self.filename, "rb") as file:
			magic = file.read(len(MAGICNUMBER))
			if magic != MAGICNUMBER:
				raise Exception("Wrong file type")
			file.read(1) # space
			head_ident = file.read(len(HEADER_IDENT))
			version = struct.unpack(">B", file.read(1))[0]
			if version == 1:
				table_count = struct.unpack(">I", file.read(4))[0]
				if table_count != len(self.tables): # maybe remove later so more tables can be added after a file has been created
					raise Exception(f"Tables not correctly initialized. Expected {table_count} table{'s' if table_count > 1 else ''} got {len(self.tables)}")
				date = datetime.strptime(file.read(12).decode("utf-8"), DATEFORMAT)
				data_ident = file.read(len(DATA_IDENT))
				for i in range(0, table_count, 1):
					table_index = struct.unpack(">I", file.read(4))[0]
					table = self.get_table(table_index)
					key_ident = struct.unpack(">B", file.read(1))[0]
					key_type = DB_Value.getType(key_ident)
					key_length = struct.unpack(">H", file.read(2))[0]
					key_name = file.read(key_length).decode("utf-8")
					if table.key_name != key_name:
						raise Exception("Format Error. Table has wrong key name")

					attribute_count = struct.unpack(">B", file.read(1))[0]
					entry_count = struct.unpack(">I", file.read(4))[0]
					columns = []

					for i in range(0, attribute_count, 1):
						typ = DB_Value.getType(struct.unpack(">B", file.read(1))[0])
						name_length = struct.unpack(">H", file.read(2))[0]
						attribute_name = file.read(name_length).decode("utf-8")
						columns.append([attribute_name, typ])
					
					for i in range(0, entry_count, 1):
						key = struct.unpack(key_type.FORMAT, file.read(key_type().getAllocation()[0]))
						values = {}
						for k in range(0, attribute_count):
							value = None
							if columns[k][1].DB_IDENT == DB_Str.DB_IDENT:
								length = struct.unpack(">I", file.read(4))[0]
								value = file.read(length).decode("utf-8")
								values[columns[k][0]] = value
								continue
							value = struct.unpack(columns[k][1].FORMAT, file.read(columns[k][1]().getAllocation()[0]))[0]
							values[columns[k][0]] = value
						self.insert(table_index, table.object(**values))
			elif version == 2:
				table_count = struct.unpack(">I", file.read(4))[0]
				if table_count != len(self.tables): # maybe remove later so more tables can be added after a file has been created
					raise Exception(f"Tables not correctly initialized. Expected {table_count} table{'s' if table_count > 1 else ''} got {len(self.tables)}")
				date = datetime.strptime(file.read(12).decode("utf-8"), DATEFORMAT)
				data_ident = file.read(len(DATA_IDENT))
				for i in range(0, table_count, 1):
					table_index = struct.unpack(">I", file.read(4))[0]
					table = self.get_table(table_index)
					key_ident = struct.unpack(">B", file.read(1))[0]
					key_type = DB_Value.getType(key_ident)
					key_length = struct.unpack(">H", file.read(2))[0]
					key_name = file.read(key_length).decode("utf-8")
					if table.key_name != key_name:
						raise Exception("Format Error. Table has wrong key name")

					attribute_count = struct.unpack(">B", file.read(1))[0]
					entry_count = struct.unpack(">I", file.read(4))[0]
					columns = []

					for i in range(0, attribute_count, 1):
						typ = DB_Value.getType(struct.unpack(">B", file.read(1))[0])
						name_length = struct.unpack(">H", file.read(2))[0]
						attribute_name = file.read(name_length).decode("utf-8")
						columns.append([attribute_name, typ])
					
					for i in range(0, entry_count, 1):
						key = struct.unpack(key_type.FORMAT, file.read(key_type().getAllocation()[0]))
						values = {}
						for k in range(0, attribute_count):
							value = None
							if columns[k][1].DB_IDENT == DB_Str.DB_IDENT:
								length = struct.unpack(">I", file.read(4))[0]
								value = file.read(length).decode("utf-8")
								values[columns[k][0]] = value
								continue
							elif columns[k][1].DB_IDENT == DB_Array.DB_IDENT:
								array_length = struct.unpack(">I", file.read(4))[0]
								array_type = DB_Value.getType(struct.unpack(">B", file.read(1))[0])
								array_values = []
								if array_type.DB_IDENT == DB_Str.DB_IDENT:
									for i in range(0, array_length):
										string_length = struct.unpack(">I", file.read(4))[0]
										array_values.append(DB_Str(file.read(string_length).decode("utf-8")))
								else:
									for i in range(0, array_length):
										array_values.append(array_type(struct.unpack(array_type.FORMAT, file.read(array_type().getAllocation()[0]))[0]))
								values[columns[k][0]] = array_values
								continue
							value = struct.unpack(columns[k][1].FORMAT, file.read(columns[k][1]().getAllocation()[0]))[0]
							values[columns[k][0]] = value
						self.insert(table_index, table.object(**values))