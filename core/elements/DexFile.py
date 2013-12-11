__author__ = "Anwar Mohamed"
__copyright__ = "Copyright (C) 2013 Anwar Mohamed"
__license__ = "Public Domain"
__version__ = "1.0"

from struct import unpack
from core.struct.dex.DexHeader import DexHeader
from core.struct.dex.DexCodeDisasm import DexCodeDisasm
from core.struct.dex.DexOptHeader import DexOptHeader
from core.struct.dex.DexClassDef import DexClassDef

NO_INDEX = 0xffffffff


class DexFile(object):
	def __init__(self, file = None):
		self.__file = file
		self.__filename = None
		self.__valid = False
		self.__decoded = False

		self.header = None
		self.strings_table = []
		self.classes = []

		if self.__file:
			self.__decode()

	def set_file(self, file):
		if len(file) > 0:
			self.__file = file
			self.__decode()

	def set_filename(self, filename):
		try:
			with open(filename, 'rb') as file:
				self.__file = file.read()
				self.__filename = filename
				self.__decode()

		except IOError:
			pass

	def __decode(self):
		if len(self.__file) >= 114 and self.__file[0:8] == 'dex\n035\x00':
			self.header = DexHeader(self.__file[:114])		
			
			if self.header.file_size != len(self.__file): return False

			for i in xrange(self.header.string_ids_off,self.header.string_ids_off + self.header.string_ids_size*4,4):
				offset = int(self.__file[i:i+4][::-1].encode('hex'), 16)
				limit, size = leb128_decode(self.__file[offset:])
				self.strings_table.append(self.__file[offset + size: offset + limit + size])

			#print len(self.strings_table)
			for i in range(self.header.class_defs_size):
				defs = {}
				class_def = DexClassDef(self.__file[self.header.class_defs_off + i*32: self.header.class_defs_off + (i+1)*32])

				defs['superclass'] = self.strings_table[int(self.__file[self.header.type_ids_off + class_def.superclassIdx*4: self.header.type_ids_off + (class_def.superclassIdx + 1)*4][::-1].encode('hex'), 16)] if class_def.sourceFileIdx != NO_INDEX else None
				defs['descriptor'] = self.strings_table[int(self.__file[self.header.type_ids_off + class_def.classIdx*4: self.header.type_ids_off + (class_def.classIdx + 1)*4][::-1].encode('hex'), 16)]
				defs['access_flags'] = class_def.accessFlags
				defs['source_file'] = self.strings_table[class_def.sourceFileIdx] if class_def.sourceFileIdx != NO_INDEX else None

				class_data = {}
				if class_def.classDataOff != 0:
					offset = class_def.classDataOff
					
					static_fields_size, size = leb128_decode(self.__file[offset:])
					offset += size
					instance_fields_size, size = leb128_decode(self.__file[offset:])
					offset += size
					direct_methods_size, size= leb128_decode(self.__file[offset:])
					offset += size
					virtual_methods_size, size= leb128_decode(self.__file[offset:])
					offset += size

					static_fields = []
					currIdx = 0
					for j in range(static_fields_size):
						static_field = {}
						index, step = leb128_decode(self.__file[offset:])
						currIdx += index
						offset += step
						index, step = leb128_decode(self.__file[offset:])
						offset += step

						type_index = int(self.__file[self.header.field_ids_off + currIdx * 8 + 2: self.header.field_ids_off + currIdx * 8 + 4][::-1].encode('hex'), 16)
						string_index = int(self.__file[self.header.type_ids_off + type_index*4: self.header.type_ids_off + type_index*4 + 4][::-1].encode('hex'), 16)
						static_field['type'] = self.strings_table[string_index] 
						static_field['name'] = self.strings_table[int(self.__file[self.header.field_ids_off + (currIdx * 8) + 4: self.header.field_ids_off + (currIdx * 8) + 8][::-1].encode('hex'), 16)]
						static_field['access_flags'] = hex(index) 
						static_fields.append(static_field)

					class_data['static_fields'] = static_fields

					instance_fields = []
					currIdx = 0
					for j in range(instance_fields_size):
						instance_field = {}
						index, step = leb128_decode(self.__file[offset:])
						currIdx += index
						offset += step
						index, step = leb128_decode(self.__file[offset:])
						offset += step

						type_index = int(self.__file[self.header.field_ids_off + currIdx * 8 + 2: self.header.field_ids_off + currIdx * 8 + 4][::-1].encode('hex'), 16)
						string_index = int(self.__file[self.header.type_ids_off + type_index*4: self.header.type_ids_off + type_index*4 + 4][::-1].encode('hex'), 16)
						instance_field['type'] = self.strings_table[string_index] 
						instance_field['name'] = self.strings_table[int(self.__file[self.header.field_ids_off + (currIdx * 8) + 4: self.header.field_ids_off + (currIdx * 8) + 8][::-1].encode('hex'), 16)]
						instance_field['access_flags'] = hex(index) 
						instance_fields.append(instance_field)

					class_data['instance_fields'] = instance_fields


					direct_methods = []
					currIdx = 0
					for j in range(direct_methods_size):
						direct_method = {}
						index, step = leb128_decode(self.__file[offset:])
						currIdx += index
						offset += step

						direct_method['name'] = self.strings_table[int(self.__file[self.header.method_ids_off + (currIdx * 8) + 4: \
							self.header.method_ids_off + (currIdx * 8) + 8][::-1].encode('hex'), 16)]
						
						proto_index = int(self.__file[self.header.method_ids_off + (currIdx * 8) + 2: \
							self.header.method_ids_off + (currIdx * 8) + 4][::-1].encode('hex'), 16)
						
						type_index = int(self.__file[self.header.proto_ids_off + proto_index * 12 + 4: \
							self.header.proto_ids_off + proto_index * 12 + 8][::-1].encode('hex'), 16)
						
						string_index = int(self.__file[self.header.type_ids_off + type_index*4: \
							self.header.type_ids_off + type_index*4 + 4][::-1].encode('hex'), 16)
												
						direct_method['return_type'] = self.strings_table[string_index] 

						#type_index = int(self.__file[self.header.method_ids_off + currIdx * 8: \
						#	self.header.method_ids_off + (currIdx * 8) + 2][::-1].encode('hex'), 16)

						#string_index = int(self.__file[self.header.type_ids_off + type_index*4: \
						#	self.header.type_ids_off + type_index*4 + 4][::-1].encode('hex'), 16)

						#direct_method['type'] = self.strings_table[string_index] 


						index, step = leb128_decode(self.__file[offset:])
						direct_method['access_flags'] = hex(index) 
						offset += step

						code_offset, step = leb128_decode(self.__file[offset:]) 
						offset += step

						#direct_method['code_disasm'] = \
						#DexCodeDisasm(code_offset).map \
						#if code_offset != 0 else None

						direct_methods.append(direct_method)

					class_data['direct_methods'] = direct_methods

					virtual_methods = []
					currIdx = 0
					for j in range(virtual_methods_size):
						virtual_method = {}
						index, step = leb128_decode(self.__file[offset:])
						currIdx += index
						offset += step

						virtual_method['name'] = self.strings_table[int(self.__file[self.header.method_ids_off + (currIdx * 8) + 4: \
							self.header.method_ids_off + (currIdx * 8) + 8][::-1].encode('hex'), 16)]
						
						proto_index = int(self.__file[self.header.method_ids_off + (currIdx * 8) + 2: \
							self.header.method_ids_off + (currIdx * 8) + 4][::-1].encode('hex'), 16)
						
						type_index = int(self.__file[self.header.proto_ids_off + proto_index * 12 + 4: \
							self.header.proto_ids_off + proto_index * 12 + 8][::-1].encode('hex'), 16)
						
						string_index = int(self.__file[self.header.type_ids_off + type_index*4: \
							self.header.type_ids_off + type_index*4 + 4][::-1].encode('hex'), 16)
												
						virtual_method['return_type'] = self.strings_table[string_index] 

						#type_index = int(self.__file[self.header.method_ids_off + currIdx * 8: \
						#	self.header.method_ids_off + (currIdx * 8) + 2][::-1].encode('hex'), 16)

						#string_index = int(self.__file[self.header.type_ids_off + type_index*4: \
						#	self.header.type_ids_off + type_index*4 + 4][::-1].encode('hex'), 16)

						#virtual_method['type'] = self.strings_table[string_index] 


						index, step = leb128_decode(self.__file[offset:])
						virtual_method['access_flags'] = hex(index) 
						offset += step

						code_offset, step = leb128_decode(self.__file[offset:]) 
						offset += step

						#virtual_method['code_disasm'] = \
						#DexCodeDisasm(code_offset).map \
						#if code_offset != 0 else None

						virtual_methods.append(virtual_method)

					class_data['virtual_methods'] = virtual_methods
				defs['data'] = class_data
				self.classes.append(defs)


			self.__decoded = True
			self.__valid = True
			return True

	@property
	def valid(self):
		return self.__valid

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		info = '<DexFile'
		if self.__valid:
			info += ' size=' + str(len(self.__file))
			info += ' strings_table_size=' + str(len(self.strings_table))
		elif self.__decode:
			info += ' NOT-VALID-DEX-FILE'
			
		info += ' |>'
		return info

	class __metaclass__(type):
		def __str__(self):
			return self.__repr__
		def __repr__(self):
			return "<DexFile 'decodes dex files into readable form' |>"
	

def leb128_decode(data):
	result = 0
	shift = 0
	size = 0
	while True:
		b = ord(data[size:size+1])
		
		size += 1
		result |= (b & 0x7f) << shift
		if b & 0x80 == 0:
			break
		shift += 7
	return result, size