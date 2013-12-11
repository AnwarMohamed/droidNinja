class DexCodeDisasm:
	def __init__(self, bin):
		self.__map = {}
		
		self.registers_size = int(bin[0:2  ][::-1].encode('hex'), 16)
		self.ins_size 		= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.outs_size 		= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.tries_size 	= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.debug_info_off = int(bin[0:2  ][::-1].encode('hex'), 16)
		self.insns_size 	= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.insns_off 		= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.padding		= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.tries_off 		= int(bin[0:2  ][::-1].encode('hex'), 16)
		self.handlers_off 	= int(bin[0:2  ][::-1].encode('hex'), 16)

	@property
	def map(self):
		return self.__map