#!/usr/bin/env python

from core.interpreter.interpreter import Interpreter
from core.interpreter import banner 
from core.modules import ModulesHandler
import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interactive",help="interactive mode",action="store_true", default=0)
args = parser.parse_args()

if args.interactive:
	modulesHandler = ModulesHandler()
	interpreter = Interpreter(modulesHandler)

	os.system('clear')
	print banner.randomGraphic()
	print banner.devInfo(modulesHandler.modulesCount)
	interpreter.start()