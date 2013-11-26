#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.interpreter.interpreter import Interpreter
from core.interpreter import banner 
import os, argparse, sys

sys.path.append('core/thirdparty/axmlparser/')

import ConfigParser
config = ConfigParser.ConfigParser()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interactive",help="interactive mode",action="store_true", default=1)
args = parser.parse_args()

if args.interactive:
	interpreter = Interpreter()

	os.system('clear')
	print banner.randomGraphic()
	print banner.devInfo()
	interpreter.start()