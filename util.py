


class Rule(object):
	def __init__(self, ruleNum, refCount, production, expanded, positions):
		self.ruleNum = ruleNum
		self.production = production
		self.expanded = expanded
		self.refCount = refCount
		self.positions = positions

	def __str__(self):
		return "{} --({})-->{} {} [{}]".format(self.ruleNum, self.refCount, "".join([str(x) for x in self.production]), "".join([str(x) for x in self.expanded]), " ".join([str(x) for x in self.positions]))
		

class SaxTerminal(object):

	
	"""
	A SaxTerminal is a PAA string
	"""
	def __init__(self, string, window, id):
		super(SaxTerminal, self).__init__()
		## this is the string
		self.string = string
		## this is an array with the start and end indices for where in the time series the string corresponds to
		self.windows = []
		self.windows.append(window)
		self.id = id
	
	def __str__(self):
		return self.string


	def getStringRep(self):
		return self.string

	def addWindow(self, window):
		self.windows.append(window)

	def getNumWindows(self):
		return len(self.windows)

	def getSpan(self):
		return (self.windows[0][0], self.windows[-1][1])

	def getID(self):
		return self.id

	def __len__(self):
		return len(self.string)

	def __eq__(self, RHS):
		if (type(self) == type(RHS)):
			print("equal comp")
			print(self.string)
			print(RHS.string)
			print("end equ comp")
			return self.string == RHS.string
		return False
	def __ne__(self, RHS):
		if (type(self) == type(RHS)):
			return self.string != RHS.string
		return True