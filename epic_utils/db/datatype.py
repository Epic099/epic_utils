import struct

class DB_Value:
	DB_IDENT = None
	FORMAT = None
	
	def get(self):
		return self.value

	def getBytes(self):
		return struct.pack(self.FORMAT, self.get())
		
	
	def getAllocation(self):
		return [struct.calcsize(self.FORMAT), self.FORMAT]
	
	@staticmethod
	def getType(ident):
		for type in TYPELIST:
			if type.DB_IDENT == ident:
				return type

	def __str__(self):
		return f"{type(self).__name__}({self.get()})"

class DB_Byte(DB_Value):
	DB_IDENT = 0x0a
	FORMAT = ">b"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
	
	def set(self, value: int):
		if value < -128 or value > 127:
			raise ValueError("Value out of range (min: -128, max: 127)")
		self.value = int(value)

class DB_UByte(DB_Value):
	DB_IDENT = 0x09
	FORMAT = ">B"
	def __init__(self, value: int = 0):
		self.value = 0 #default to 0 needed if invalid input is entered the value must still exist
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 255:
			raise ValueError("Value out of range (min: 0, max: 255)")
		self.value = int(value)

class DB_Short(DB_Value):
	DB_IDENT = 0x08
	FORMAT = ">h"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
	
	def set(self, value: int):
		if value < -32768 or value > 32767:
			raise ValueError("Value out of range (min: -32768, max: 32767)")
		self.value = int(value)

class DB_UShort(DB_Value):
	DB_IDENT = 0x07
	FORMAT = ">H"
	def __init__(self, value: int = 0):
		self.value = 0 #default to 0 needed if invalid input is entered the value must still exist
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 65535:
			raise ValueError("Value out of range (min: 0, max: 65535)")
		self.value = int(value)

class DB_Int(DB_Value):
	DB_IDENT = 0x01
	FORMAT = ">i"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
	
	def set(self, value: int):
		if value < -2147483648 or value > 2147483647:
			raise ValueError("Value out of range (min: -2147483648, max: 2147483647)")
		self.value = int(value)
		
class DB_UInt(DB_Value):
	DB_IDENT = 0x02
	FORMAT = ">I"
	def __init__(self, value: int = 0):
		self.value = 0 #default to 0 needed if invalid input is entered the value must still exist
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 4294967295:
			raise ValueError("Value out of range (min: 0, max: 4294967295)")
		self.value = int(value)

class DB_Float(DB_Value):
	DB_IDENT = 0x03
	FORMAT = ">f"
	def __init__(self, value: float = 0.0):
		self.value = float(value)
		
	def set(self, value: float):
		self.value = float(value)
						
class DB_Long(DB_Value):
	DB_IDENT = 0x04
	FORMAT = ">q"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
		
	def set(self, value: int):
		if value < -9223372036854775808 or value > 9223372036854775807:
			raise ValueError("Value out of range (min: -9223372036854775808, max: 9223372036854775807)")
		self.value = int(value)
		
class DB_ULong(DB_Value):
	DB_IDENT = 0x05
	FORMAT = ">Q"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 18446744073709551615:
			raise ValueError("Value out of range (min: 0, max: 18446744073709551615)")
			return
		self.value = int(value)

class DB_Str(DB_Value):
	DB_IDENT = 0x06
	FORMAT = None
	def __init__(self, value: str = ""):
		self.value = ""
		self.set(value)
		
	def set(self, value: str):
		self.value = str(value)
	
	def getBytes(self):
		return self.get().encode("utf-8")
		
	def getAllocation(self):
		return [len(self.get()), self.FORMAT]
	
class DB_Array(DB_Value):
	DB_IDENT = 0x0b
	FORMAT = None

	def __init__(self, typ: DB_Value, values: list = None):
		self.typ = typ
		self.values: list[DB_Value] = []
		if getattr(typ, "FORMAT", -1) == -1:
			raise TypeError("Invalid Type for DB_Array")
		if values != None:
			for i in range(0, len(values)):
				self.append(values[i])

	@property
	def length(self):
		return len(self.values)
	
	def validIndex(self, index):
		if not isinstance(index, int):
			return False
		if index < 0 or index >= self.length:
			return False
		return True
	
	def append(self, value):
		if not isinstance(value, self.typ):
			raise TypeError(f"Type of object ({type(value).__name__}) doesnt match Array type ({self.typ.__name__})")
		self.values.append(value)

	def removeIndex(self, index: int):
		if not self.validIndex(index):
			raise IndexError(f"Index {index} is invalid")
		self.values.pop(index)
	
	def remove(self, value):
		if isinstance(value, self.typ):
			value = value.get()
		for i in range(0, self.length):
			if self.values[i].get() == value:
				self.values.remove(self.values[i])
				return
			
	def getAllocation(self):
		amount = 0
		for i in range(0, self.length):
			amount += self.values[i].getAllocation()[0]
		return [amount, None]

	def __getitem__(self, index):
		return self.values[index]
	
	def __setitem__(self, index, value):
		if not isinstance(value, self.typ):
			raise TypeError(f"DB_Array expected {self.typ.__name__} got {type(value).__name__}")
		if not self.validIndex(index):
			raise IndexError(f"Index {index} is invalid")
		self.values[index] = value

	def get(self):
		return self.values

	def __str__(self):
		return f"DB_Array({self.typ.__name__}, {self.length}, [{", ".join(str(self.values[i].get()) for i in range(0, self.length))}])"
	
TYPELIST = [DB_Byte, DB_UByte, DB_Short, DB_UShort, DB_Int, DB_UInt, DB_Float, DB_Long, DB_ULong, DB_Str, DB_Array]
