__author__ = "Anwar Mohamed"
__copyright__ = "Copyright (C) 2013 Anwar Mohamed"
__license__ = "Public Domain"
__version__ = "1.0"

import axmlprinter
from xml.dom import minidom
from bs4 import BeautifulSoup
import re

class ApkManifest(object):
	def __init__(self, file = None):
		self.__file = file
		self.__filename = None
		self.__decoded = None
		self.__xml = None

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

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if self.__file:
			info = '<ApkManifest'
			if self.min_sdk: info += " minSdKVersion=" + self.min_sdk
			if self.target_sdk: info += " targetSdKVersion=" + self.target_sdk
			if self.max_sdk: info += " maxSdKVersion=" + self.max_sdk
			info += ' permissions=' + str(len(self.permissions))
			info += ' |>'
			return info
		return '<ApkManifest |>'

	def print_xml(self):
		print self.__xml.prettify()

	def __decode(self):
		ap = axmlprinter.AXMLPrinter(self.__file)
		self.__decoded = minidom.parseString(ap.getBuff()).toxml()
		self.__xml = BeautifulSoup(self.__decoded, "xml")

	@property
	def permissions(self):
		perms = []
		if self.__xml:
			for p in self.__xml.find_all('uses-permission'):
				try:
					res = re.search('name=".*?"', str(p)).group().replace('"', '').replace("name=",'')
					if res: perms.append(res)
				except:
					pass
		return perms

	@property
	def min_sdk(self):
		try:
			return re.search('minSdkVersion=".*?"', str(self.__xml.find("uses-sdk")))\
			.group().replace('"', '').replace("minSdkVersion=",'')
		except:
			return None

	@property
	def target_sdk(self):
		try:
			return re.search('targetSdkVersion=".*?"', str(self.__xml.find("uses-sdk")))\
			.group().replace('"', '').replace("targetSdkVersion=",'')
		except:
			return None

	@property
	def max_sdk(self):
		try:
			return re.search('maxSdkVersion=".*?"', str(self.__xml.find("uses-sdk")))\
			.group().replace('"', '').replace("maxSdkVersion=",'')
		except:
			return None

	@property
	def package_name(self):
		try:
			return re.search('package=".*?"', str(self.__xml.find("manifest")))\
			.group().replace('"', '').replace("package=",'')
		except:
			return None

	@property
	def activities(self):
		activities = []
		if self.__xml:
			for p in self.__xml.find_all('activity'):
				try:
					res = re.search('name=".*?"', str(p)).group().replace('"', '').replace("name=",'')
					if res: activities .append(res)
				except:
					pass
		return activities

	@property
	def services(self):
		services = []
		if self.__xml:
			for p in self.__xml.find_all('service'):
				try:
					res = re.search('name=".*?"', str(p)).group().replace('"', '').replace("name=",'')
					if res: services.append(res)
				except:
					pass
		return services

	@property
	def receivers(self):
		receivers = []
		if self.__xml:
			for p in self.__xml.find_all('receiver'):
				try:
					res = re.search('name=".*?"', str(p)).group().replace('"', '').replace("name=",'')
					if res: receivers.append(res)
				except:
					pass
		return receivers

	@property
	def version_name(self):
		try:
			return re.search('versionName=".*?"', str(self.__xml.find("manifest")))\
			.group().replace('"', '').replace("versionName=",'')
		except:
			return None

	@property
	def version_code(self):
		try:
			return re.search('versionCode=".*?"', str(self.__xml.find("manifest")))\
			.group().replace('"', '').replace("versionCode=",'')
		except:
			return None

	class __metaclass__(type):
		def __str__(self):
			return self.__repr__
		def __repr__(self):
			return "<ApkManifest 'decodes AndroidManifest.xml files into readable form' |>"