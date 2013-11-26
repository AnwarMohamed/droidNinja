import zipfile

class Apk(object):
	def __init__(self, filename=None):
		self.__file = None
		self.__filename = None
		self.__fileList = {}

		if filename != None:
			self.set_apk(filename)


	def set_apk(self, filename):
		try:
			with open(filename, 'rb'):
				
				if self.__validateApk(filename):
					self.__file = zipfile.ZipFile(filename)
					self.__filename = filename
					print '[*] Apk file set to: ' + filename
				else:
					print '[x] Not a valid Apk file'
		except IOError:
			print '[x] Apk file not exist'


	def __validateApk(self, file):
		return zipfile.is_zipfile(file)

	def list_files(self):
		if self.__file:
			print ''
			self.__file.printdir()

			print '\n[*] Total files: ' + str(len(self.__file.namelist()))
		else:
			print '[x] Apk file not set yet'

	def extract(self, key):
		if self.__file and key in self.__file.namelist():
			return self.__file.read(key)
 		return None

 	def compress_size(self, key):
 		if self.__file and key in self.__file.namelist():
 			return self.__file.getinfo(key).compress_size
 		return 0

  	def file_size(self, key):
 		if self.__file and key in self.__file.namelist():
 			return self.__file.getinfo(key).file_size
 		return 0
	
	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if self.__file:
			return '<Apk loaded=\'' + self.__filename + '\' files=' + str(len(self.__file.namelist())) + ' |>'
		return '<Apk |>'