class Module(object):
	def __init__(self):
		pass

	@property
	def codename(self):
		return 'apk'

	@property
	def description(self):
		return 'apk module'

	def help(self):

		print "Apk Module Commands"
		print "===================\n"
		print "     Command         Description"
		print "     -------         -----------"
		print "     test            test description"
		print ""

	def info(self):
		print 'apk info'

	@property
	def methods(self):
		return {}