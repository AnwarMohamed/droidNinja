__author__ = "Anwar Mohamed"
__copyright__ = "Copyright (C) 2013 Anwar Mohamed"
__license__ = "Public Domain"
__version__ = "1.0"

from struct import unpack

class DexStruct:

	NO_INDEX = 0xffffffff

	class DexHeader:
		def __init__(self, bin):
			self.magic 			= 	  bin[0:8    ]
			self.checksum 		= 	  bin[8:12   ][::-1].encode('hex')
			self.signature	 	= 	  bin[12:32  ].encode('hex')
			self.file_size  	= int(bin[32:36  ][::-1].encode('hex'), 16)
			self.header_size	= int(bin[36:40  ][::-1].encode('hex'), 16)
			self.endian_tag		= 	  bin[40:44  ].encode('hex')
			self.link_size		= int(bin[44:48  ][::-1].encode('hex'), 16)
			self.link_off		= int(bin[48:52  ][::-1].encode('hex'), 16)
			self.mapOff			= int(bin[52:56  ][::-1].encode('hex'), 16)
			self.string_ids_size= int(bin[56:60  ][::-1].encode('hex'), 16)
			self.string_ids_off	= int(bin[60:64  ][::-1].encode('hex'), 16)
			self.type_ids_size 	= int(bin[64:68  ][::-1].encode('hex'), 16)
			self.type_ids_off 	= int(bin[68:72  ][::-1].encode('hex'), 16)
			self.protoIdsSize	= int(bin[72:76  ][::-1].encode('hex'), 16)
			self.protoIdsOff	= int(bin[76:80  ][::-1].encode('hex'), 16)
			self.field_ids_size	= int(bin[80:84  ][::-1].encode('hex'), 16)
			self.field_ids_off 	= int(bin[84:88  ][::-1].encode('hex'), 16)
			self.method_ids_size= int(bin[88:92  ][::-1].encode('hex'), 16)
			self.method_ids_off = int(bin[92:96	 ][::-1].encode('hex'), 16)
			self.class_defs_size= int(bin[96:100 ][::-1].encode('hex'), 16)
			self.class_defs_off = int(bin[100:104][::-1].encode('hex'), 16)
			self.data_size		= int(bin[104:108][::-1].encode('hex'), 16)
			self.data_off 		= int(bin[108:112][::-1].encode('hex'), 16)

	class DexOptHeader:
		def __init__(self, bin):
			self.magic 			= 	  bin[0:8  ]
			self.dex_offset 	= int(bin[8:12 ][::-1].encode('hex'), 16)
			self.dex_length 	= int(bin[12:16][::-1].encode('hex'), 16)
			self.deps_offset	= int(bin[16:20][::-1].encode('hex'), 16)
			self.deps_length	= int(bin[20:24][::-1].encode('hex'), 16)
			self.opt_offset		= int(bin[24:28][::-1].encode('hex'), 16)
			self.opt_length		= int(bin[28:32][::-1].encode('hex'), 16)
			self.flags			= 	  bin[32:36][::-1].encode('hex')
			self.checksum		= 	  bin[36:40][::-1].encode('hex')

	class DexClassDef:
		def __init__(self, bin):
			self.classIdx 		= int(bin[0:4  ][::-1].encode('hex'), 16)
			self.accessFlags	= hex(int(bin[4:8  ][::-1].encode('hex'), 16))
			self.superclassIdx	= int(bin[8:12 ][::-1].encode('hex'), 16)
			self.interfacesOff	= int(bin[12:16][::-1].encode('hex'), 16)
			self.sourceFileIdx	= int(bin[16:20][::-1].encode('hex'), 16)
			self.annotationsOff	= int(bin[20:24][::-1].encode('hex'), 16)
			self.classDataOff	= int(bin[24:28][::-1].encode('hex'), 16)
			self.staticValuesOff= int(bin[28:32][::-1].encode('hex'), 16)


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
			self.header = DexStruct.DexHeader(self.__file[:114])		
			
			if self.header.file_size != len(self.__file): return False

			for i in xrange(self.header.string_ids_off,self.header.string_ids_off + self.header.string_ids_size*4,4):
				offset = int(self.__file[i:i+4][::-1].encode('hex'), 16)
				limit, size = leb128_decode(self.__file[offset:])
				self.strings_table.append(self.__file[offset + size: offset + limit + size])

			#print len(self.strings_table)
			for i in range(self.header.class_defs_size):
				defs = {}
				class_def = DexStruct.DexClassDef(self.__file[self.header.class_defs_off + i*32: self.header.class_defs_off + (i+1)*32])

				defs['superclass'] = self.strings_table[int(self.__file[self.header.type_ids_off + class_def.superclassIdx*4: self.header.type_ids_off + (class_def.superclassIdx + 1)*4][::-1].encode('hex'), 16)] if class_def.sourceFileIdx != DexStruct.NO_INDEX else None
				defs['descriptor'] = self.strings_table[int(self.__file[self.header.type_ids_off + class_def.classIdx*4: self.header.type_ids_off + (class_def.classIdx + 1)*4][::-1].encode('hex'), 16)]
				defs['access_flags'] = class_def.accessFlags
				defs['source_file'] = self.strings_table[class_def.sourceFileIdx] if class_def.sourceFileIdx != DexStruct.NO_INDEX else None

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