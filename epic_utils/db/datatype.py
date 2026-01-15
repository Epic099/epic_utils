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

class DB_Byte(DB_Value):
	DB_IDENT = 0xa0
	FORMAT = ">b"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
	
	def set(self, value: int):
		if value < -128 or value > 127:
			return
		self.value = int(value)

class DB_UByte(DB_Value):
	DB_IDENT = 0x09
	FORMAT = ">B"
	def __init__(self, value: int = 0):
		self.value = 0 #default to 0 needed if invalid input is entered the value must still exist
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 255:
			return
		self.value = int(value)

class DB_Short(DB_Value):
	DB_IDENT = 0x08
	FORMAT = ">h"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
	
	def set(self, value: int):
		if value < -32768 or value > 32767:
			return
		self.value = int(value)

class DB_UShort(DB_Value):
	DB_IDENT = 0x07
	FORMAT = ">H"
	def __init__(self, value: int = 0):
		self.value = 0 #default to 0 needed if invalid input is entered the value must still exist
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 65535:
			return
		self.value = int(value)

class DB_Int(DB_Value):
	DB_IDENT = 0x01
	FORMAT = ">i"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
	
	def set(self, value: int):
		if value < -2147483648 or value > 2147483647:
			return
		self.value = int(value)
		
class DB_UInt(DB_Value):
	DB_IDENT = 0x02
	FORMAT = ">I"
	def __init__(self, value: int = 0):
		self.value = 0 #default to 0 needed if invalid input is entered the value must still exist
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 4294967295:
			return
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
			return
		self.value = int(value)
		
class DB_ULong(DB_Value):
	DB_IDENT = 0x05
	FORMAT = ">Q"
	def __init__(self, value: int = 0):
		self.value = 0
		self.set(value)
		
	def set(self, value: int):
		if value < 0 or value > 18446744073709551615:
			return
		self.value = int(value)

class DB_Str(DB_Value):
	DB_IDENT = 0x06
	FORMAT = "STR"
	def __init__(self, value: str = ""):
		self.value = 0
		self.set(value)
		
	def set(self, value: int):
		self.value = str(value)
	
	def getBytes(self):
		return self.get().encode("utf-8")
		
	def getAllocation(self):
		return [len(self.get()), self.FORMAT]
	
TYPELIST = [DB_Byte, DB_UByte, DB_Short, DB_UShort, DB_Int, DB_UInt, DB_Float, DB_Long, DB_ULong, DB_Str]

