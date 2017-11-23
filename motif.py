
from sax import SAX
from sequitur import Grammar
class Motif(object):
	"""
	This class uses sax and sequitur to identify the motifs from a timeseries
	"""

	def __init__(self, timeseries, windowSize, wordSize, alphabetSize):
		self.timeseries = timeseries
		self.windowSize = windowSize
		self.wordSize = wordSize
		self.alphabetSize = alphabetSize

	def buildMotifs(self):
		s = SAX(self.wordSize, self.alphabetSize)
		self.saxterms = s.sliding_window(self.timeseries, self.windowSize)
		self.grammar = Grammar()
		self.grammar.train_string(self.saxterms)
		self.myrules = self.grammar.getRules()

	def getRules(self):
		return self.myrules

	def getMotif(self, ruleID):
		motif = []
		for k in self.myrules[ruleID].positions:
			# so i can get the start and then length of the expanded rule and that is how I can get the 
			if not k == None:
				motif.append([self.saxterms[k].getSpan()[0], self.saxterms[k + len(self.myrules[ruleID].expanded) - 1].getSpan()[1]])
		return motif