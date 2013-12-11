#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anwar Mohamed"
__copyright__ = "Copyright (C) 2013 Anwar Mohamed"
__license__ = "Public Domain"
__version__ = "1.0"

from core.interpreter.interpreter import Interpreter
from core.interpreter import banner 
import os, argparse, sys
from gui.GuiApp import GuiApp

sys.path.append('core/thirdparty/axmlparser/')

import ConfigParser
config = ConfigParser.ConfigParser()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interactive",help="interactive mode",action="store_true", default=1)
parser.add_argument("-g", "--gui",help="gui mode",action="store_true", default=0)
args = parser.parse_args()

if args.gui:
	gui = GuiApp();
	gui.run()

elif args.interactive:
	interpreter = Interpreter()
	os.system('clear')
	print banner.randomGraphic()
	print banner.devInfo()
	interpreter.start()