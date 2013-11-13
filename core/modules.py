import os
import importlib

class ModulesHandler(object):
	def __init__(self):
		files = [f for f in os.listdir('modules') \
		if os.path.isfile('modules/' + f) and f.startswith('mod') and f.endswith('.py')]
		
		self.__modules = {}

		for f in files:
			modObject = importlib.import_module('modules.' + f[:-3]).Module()
			self.__modules[modObject.codename] = {
			'help':		modObject.help,
			'info':		modObject.info,
			'desc':		modObject.description,
			'methods':	modObject.methods.keys(),
			}	

	@property
	def modulesCount(self):
		return len(self.__modules.keys())

	@property
	def modules(self):
		return self.__modules
