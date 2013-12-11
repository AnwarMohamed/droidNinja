
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
