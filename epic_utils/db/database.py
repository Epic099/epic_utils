import struct
from .datatype import DB_ULong, DB_Str, DB_Float, DB_Value
from datetime import datetime

MAGICNUMBER = "EPDB".encode("utf-8")
HEADER_IDENT = "HEAD".encode("utf-8")
DATA_IDENT = "DATA".encode("utf-8")
END_IDENT = "STOP".encode("utf-8")
DATEFORMAT = "%d%m%Y%H%M"
FORMAT_VERSION = 1
		
class DBObject:
	def __init__(self):
		pass
		
	def get_values(self):
		"""
			return: Array -> [attribute_name, attribute_type, attribute_value]
		"""
		result = []
		children = dir(self)
		children.sort()
		for child in children:
			typ = type(getattr(self, child))
			try:
				_ = getattr(typ, "DB_IDENT")
				result.append([child, typ, getattr(self, child).value])
			except:
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
		self.coloumns = [[temp[0], temp[1].DB_IDENT] for temp in _values] # [name, type]
		
		self.values = {}
		
	def insert(self, object):
		if not isinstance(object, self.object):
			raise TypeError(f"Invalid type. Expected <{self.object.__name__}> got <{type(object).__name__}>")
			#return # can only store provided objects
		key = getattr(object, self.key_name)
		self.values[key.get()] = object
		
class Database():
	def __init__(self, filename):
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


	def register_table(self, index: int, key_name: str, object: any):
		for table in self.tables:
			if table.index == index:
				raise IndexError("Table indices must be unique")
		self.tables.append(DBTable(index, key_name, object))
	
	def save(self):
		with open(self.filename, "wb") as file:
			#struct types (for myself because i cant f*cking remember, B = 1Byte, H = 2Bytes. I=4Bytes)
			file.write(MAGICNUMBER) # identify file type
			file.write(struct.pack(">B", 0)) #Space
			
			file.write(HEADER_IDENT) # header
			file.write(struct.pack(">B", FORMAT_VERSION)) #format version (current v = 1)
			file.write(struct.pack(">I", len(self.tables))) #table count
			file.write(datetime.now().strftime(DATEFORMAT).encode("utf-8")) # save time
			
			file.write(DATA_IDENT) # data
			
			for table in self.tables:
				file.write(struct.pack(">I", table.index)) # table index -> later used to identify tables
				file.write(struct.pack(">B", table.key_type.DB_IDENT)) #key type
				file.write(struct.pack(">H", len(table.key_name))) # key length (maybe change to 1 Byte length?)
				file.write(table.key_name.encode("utf-8")) # key name
				file.write(struct.pack(">B", len(table.coloumns))) # number of attributes				
				file.write(struct.pack(">I", len(table.values.keys()))) # number of entries
				for col in table.coloumns:
					file.write(struct.pack(">B", col[1])) # attribute type
					file.write(struct.pack(">H", len(col[0]))) # name length of attribute (maybe also change to 1 Byte?)
					file.write(col[0].encode("utf-8")) # attribute name
					
				for key in table.values.keys():
					file.write(table.key_type(value=key).getBytes()) # key (only int/float allowed for now as I need to implement keys with variable length)
					object = table.values[key]
					for col in table.coloumns:
						if col[1] == DB_Str.DB_IDENT:
							file.write(struct.pack(">I", getattr(object, col[0]).getAllocation()[0])) # value length
							file.write(getattr(object, col[0]).getBytes())
						else:
							file.write(getattr(object, col[0]).getBytes()) # value of each coloumn (also no variable length now)
				
			
			file.write(END_IDENT)
			
	def read(self):
		with open(self.filename, "rb") as file:
			magic = file.read(len(MAGICNUMBER))
			file.read(1) # space

			head_ident = file.read(len(HEADER_IDENT))
			version = struct.unpack(">B", file.read(1))[0]
			print(magic, version)
			if version != FORMAT_VERSION:
				print("test")
				return # wrong file version. Avoid loading file to not corrupt it
			table_count = struct.unpack(">I", file.read(4))[0]
			if table_count != len(self.tables): # maybe remove later so more tables can be added after a file has been created
				raise MemoryError(f"Tables not correctly initialized. Expected {table_count} tables got {len(self.tables)}")
			date = datetime.strptime(file.read(12).decode("utf-8"), DATEFORMAT)
			data_ident = file.read(len(DATA_IDENT))
			for i in range(0, table_count, 1):
				table_index = struct.unpack(">I", file.read(4))[0]
				table = self.get_table(table_index)
				key_ident = struct.unpack(">B", file.read(1))[0]
				key_type = DB_Value.getType(key_ident)
				key_length = struct.unpack(">H", file.read(2))[0]
				key_name = file.read(key_length).decode("utf-8")

				attribute_count = struct.unpack(">B", file.read(1))[0]
				entry_count = struct.unpack(">I", file.read(4))[0]
				coloumns = []

				for i in range(0, attribute_count, 1):
					typ = DB_Value.getType(struct.unpack(">B", file.read(1))[0])
					name_length = struct.unpack(">H", file.read(2))[0]
					attribute_name = file.read(name_length).decode("utf-8")
					coloumns.append([attribute_name, typ])
				
				for i in range(0, entry_count, 1):
					key = struct.unpack(key_type.FORMAT, file.read(key_type().getAllocation()[0]))
					values = {}
					for k in range(0, attribute_count):
						value = None
						if coloumns[k][1].DB_IDENT == DB_Str.DB_IDENT:
							length = struct.unpack(">I", file.read(4))[0]
							value = file.read(length).decode("utf-8")
							values[coloumns[k][0]] = value
							continue
						value = struct.unpack(coloumns[k][1].FORMAT, file.read(coloumns[k][1]().getAllocation()[0]))[0]
						values[coloumns[k][0]] = value
					db.insert(table_index, table.object(**values))
					#table.object()
					pass # implement entry reading later but I will store them as dictionary and unpack them into the object provided by the pre registered table which is identified by its id
		
class User(DBObject):
	def __init__(self, userid=0, username="", cash=0):
		self.userid = DB_ULong(value=userid)
		self.username = DB_Str(value=username)
		self.cash = DB_Float(value=cash)
		
	

db = Database("test.epicdb")
db.register_table(0, "userid", User)
db.read()
"""db.insert(0, User(userid=15239, username="epic099", cash=200))
db.insert(0, User(userid=1248, username="frieske", cash=500))
db.save()"""


