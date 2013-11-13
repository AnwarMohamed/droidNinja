from termcolor import colored
from colorama import init, Fore, Back, Style

import sys, os
import readline


class Interpreter(object):
	def __init__(self, modHandler):
		self.setPrompt()
		self.__HISTORY_FILENAME = '.console_history'
		self.__modHandler = modHandler

		self.__module = None

		readline.parse_and_bind("tab: complete")
		readline.set_completer(self.tab_completer)

		if os.path.exists(self.__HISTORY_FILENAME):
			readline.read_history_file(self.__HISTORY_FILENAME)

		self.commands = {
		'help'			:[self.help, False],
		'clear_history'	:[readline.clear_history, False],
		'exit'			:[self.exit, False],
		'use'			:[self.use, True],
		'back'			:[self.back, False],
		'info'			:[self.info, True],
		}
	
	def processCmd(self, cmd):
		if cmd.split(' ')[0] in self.commands.keys():
			if self.commands[cmd.split(' ')[0]][1]:
				self.commands[cmd.split(' ')[0]][0](cmd)
			else:
				self.commands[cmd.split(' ')[0]][0]()

		elif cmd:
			self.printError('[!] Unknown command \''+ cmd.split(' ')[0] +'\', Use help')
	
	def start(self):
		while(True):
			try:
				command  = raw_input(self.__prompt)
				self.processCmd(command)
			except KeyboardInterrupt:
				self.printError('\n[!] Ctrl-C detected, use exit command to quit')	

	def help(self):
		print ""
		print "General Commands"
		print "================\n"
		print "     Command         Description"
		print "     -------         -----------"
		print "     back            Deattach current module"
		print "     exit            Exits the framework"		
		print "     help            Brings you this help menu"
		print "     info            Get info about current module or loaded modules"
		print "     update          Updates the framework to latest version"
		print "     use             Set a module to be used"
		print ""

		if self.__module:
			self.__modHandler.modules[self.__module]['help']()

	def tab_completer(self, text, state):
		options = [i for i in self.commands if i.startswith(text)]
		if state < len(options):
			return options[state]
		else:
			return None

	def exit(self):
		readline.write_history_file(self.__HISTORY_FILENAME)
		print Fore.GREEN + '\n[*] Thank you for using droidNinja!' + Style.RESET_ALL
		sys.exit(0)

	def use(self, argsStr):
		args = argsStr.split(' ')[1:]
		if len(args) == 1 and args[0] in self.__modHandler.modules.keys():
			self.__module = args[0]
			self.setPrompt(self.__module)
		else:
			self.printError('[!] Select a valid module to be used')

	def printError(self, msg):
		print Fore.RED + msg + Style.RESET_ALL

	def setPrompt(self, module=None):
		if module:
			self.__prompt = Style.BRIGHT + Fore.BLUE + 'dninja' + \
			Style.NORMAL + Fore.YELLOW + ':' + module + Style.RESET_ALL + ' > '
		else:
			self.__prompt = Style.BRIGHT + Fore.BLUE + 'dninja' + Style.RESET_ALL + ' > '

	def back(self):
		self.__module = None
		self.setPrompt()

	def info(self, module):
		module = module.split(' ')[1:]
		if len(module) > 0:
			if module[0] in self.__modHandler.modules.keys():
				self.__modHandler.modules[module[0]]['info']()
			else:
				self.printError('[!] \'' + module[0] +'\' module not found')
		elif self.__module:
			self.__modHandler.modules[self.__module]['info']()
		else:
			self.printError('[!] No module selected')