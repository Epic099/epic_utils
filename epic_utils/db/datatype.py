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
	
TYPELIST = [DB_Byte, DB_UByte, DB_Short, DB_UShort, DB_Int, DB_UInt, DB_Float, DB_Long, DB_ULong, DB_Str]

