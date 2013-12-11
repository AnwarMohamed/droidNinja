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
