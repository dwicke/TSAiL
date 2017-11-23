import numpy
import random
from sax import SAX



## the coverage of a rule is the number of intervals: rule.getRuleIntervals().size()
## 

class RRA(object):

	def __init__(self, timeseries, motifs):
		"""
		Need the timeseries and the grammar
		"""
		self.timeseries = timeseries
		self.motifs = motifs
		# get the rules sorted by ascending order of coverage
		self.rulesByCoverage = sorted(self.motifs.grammar.getRules()[1:], key=lambda x: len(x.positions), reverse=False)
		self.rules = self.motifs.grammar.getRules()

	def dist(self, p, q):
		s = SAX(wordSize=min(len(self.timeseries[p[0]:p[1]]), len(self.timeseries[q[0]:q[1]])))
		normp = s.normalize(self.timeseries[p[0]:p[1]])
		normq = s.normalize(self.timeseries[q[0]:q[1]])
		if len(self.timeseries[p[0]:p[1]]) > len(self.timeseries[q[0]:q[1]]):
			normp = s.normalize(s.to_PAA(self.timeseries[p[0]:p[1]])[0])
		elif len(self.timeseries[q[0]:q[1]]) > len(self.timeseries[p[0]:p[1]]):
			normq = s.normalize(s.to_PAA(self.timeseries[q[0]:q[1]])[0])
		return numpy.linalg.norm(normp - normq) / float(len(normp))

	def getAnomalies(self, number):
		best_so_far_dist = 0
		best_so_far_loc = None
		for outerRule in self.rulesByCoverage:
			for outerSpan in self.motifs.getMotif(outerRule.ruleNum):
				nearest_neighbor_dist = float("inf")
				# need to do a -1 to the ruleNum because that corresponds to a zero indexed array where 0 is the root of the grammar which was removed
				nearest_neighbor_dist = self.inner([self.rules[outerRule.ruleNum]], outerSpan, best_so_far_dist, nearest_neighbor_dist)
				if nearest_neighbor_dist >= best_so_far_dist:
					therest = self.rules[1:outerRule.ruleNum] + self.rules[outerRule.ruleNum  + 1:]
					therest = random.sample(therest, len(therest))
					nearest_neighbor_dist = self.inner(therest, outerSpan, best_so_far_dist, nearest_neighbor_dist)
					
				if nearest_neighbor_dist > best_so_far_dist:
					best_so_far_dist = nearest_neighbor_dist
					best_so_far_loc = outerSpan
				
				
				

		return (best_so_far_dist, best_so_far_loc)

	def inner(self, innerRules, outerSpan, best_so_far_dist, nearest_neighbor_dist):
		for innerRule in innerRules:
			for innerSpan in self.motifs.getMotif(innerRule.ruleNum):
				if abs(outerSpan[0] - innerSpan[0]) >= (outerSpan[1] - outerSpan[0]):
					current_dist = self.dist(outerSpan, innerSpan)
					# early breaking:
					if current_dist < best_so_far_dist:
						return current_dist
					if current_dist < nearest_neighbor_dist:
						nearest_neighbor_dist = current_dist
		return nearest_neighbor_dist