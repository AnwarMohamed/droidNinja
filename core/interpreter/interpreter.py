from termcolor import colored
from colorama import init, Fore, Back, Style

import sys, os, code

import readline
import pkgutil
import sys

class Interpreter(object):
	def __init__(self):
		
		self.__HISTORY_FILENAME = '.console_history'
		if os.path.exists(self.__HISTORY_FILENAME):
			readline.read_history_file(self.__HISTORY_FILENAME)

		sys.ps1 = '\x01\033[01;34m\x02>>> \x01\033[00m\x02'
		self._modules = self.load_all_modules()
		self._console = code.InteractiveConsole(self._modules)
		
		import rlcompleter
		readline.set_completer(self.tab_completer)
		readline.parse_and_bind("tab: complete")
		
		import atexit
		atexit.register(self.exit)

	def load_all_modules(self):
		import modules
		modDict = {}
		for importer, package_name, _ in list(pkgutil.iter_modules(modules.__path__)):
			full_package_name = '%s.%s' % ("modules", package_name)
			if full_package_name not in sys.modules:
				modDict[package_name] = getattr(importer.find_module(package_name).load_module(full_package_name), package_name)
		return modDict

	def start(self):
		self._console.interact("")

	def tab_completer(self, text, state):
		options = [i for i in self._modules.keys() if i.startswith(text) and i != "__builtins__"]
		if state < len(options):
			return options[state]
		else:
			return None

	def exit(self):
		readline.write_history_file(self.__HISTORY_FILENAME)