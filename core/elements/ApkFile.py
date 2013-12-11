__author__ = "Anwar Mohamed"
__copyright__ = "Copyright (C) 2013 Anwar Mohamed"
__license__ = "Public Domain"
__version__ = "1.0"

import zipfile

class ApkFile(object):
	def __init__(self, filename=None):
		self.__file = None
		self.__filename = None
		self.__fileList = {}

		if filename is not None:
			self.set_apk(filename)


	def set_apk(self, filename):
		try:
			with open(filename, 'rb'):
				
				if self.__validateApk(filename):
					self.__file = zipfile.ZipFile(filename)
					self.__filename = filename

		except IOError:
			pass


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

	@property
	def files(self):
		if self.__file: return self.__file.namelist()
		else: return []
			
	class __metaclass__(type):
		def __str__(self):
			return self.__repr__
		def __repr__(self):
			return "<ApkManifest 'extracts android application files from apk archieve' |>"