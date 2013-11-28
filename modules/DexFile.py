class DexStruct:
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

	# class DexOptHeader:
	# class DexFieldId:


class DexFile(object):
	def __init__(self, file = None):
		self.__file = file
		self.__filename = None
		self.valid = False
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
			
			for i in xrange(self.header.string_ids_off,self.header.string_ids_size*4,4):
				offset = int(self.__file[i:i+4][::-1].encode('hex'), 16)
				limit, size = leb128_decode(self.__file[offset:offset+4])
				self.strings_table.append(self.__file[offset + size: offset + limit + size])

			self.__decoded = True
			self.valid = True

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		info = '<DexFile'
		if self.__valid:
			info += ' size=' + str(len(self.__file))
		elif self.__decode:
			info += ' NOT-VALID-DEX-FILE'
			
		info += ' |>'
		return info

	


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