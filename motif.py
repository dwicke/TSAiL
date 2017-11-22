
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
		g = Grammar()
		g.train_string(saxterms)
		self.myrules = g.getRules()
		
