# from sax import SAX
# from sequitur import Grammar
# from util import Rule
# from util import SaxTerminal
from motif import Motif
from rra import RRA
import numpy as np

timeseries = np.loadtxt('ecg0606_1.csv', delimiter="\n")


m = Motif(timeseries, 200, 4, 4)
m.buildMotifs()
anonamly = RRA(timeseries, m)
nndist, span = anonamly.getAnomalies(4)

print("nearest neighbor dist = {} span = ({},{}) distance calls = {}".format(nndist, span[0], span[1], anonamly.distCalls))
# motif = m.getMotif(1)
# for k in motif:
# 	print(k)


# a = [SaxTerminal("ug",(-1,3), 0), SaxTerminal("ug",(0,4), 1), SaxTerminal("hi",(1,5), 2), SaxTerminal("yo",(2,6), 3), SaxTerminal("ga",(3,7), 4), SaxTerminal("hi",(4,8), 5),SaxTerminal("yo",(5,9), 6),SaxTerminal("bo",(6,10), 7)]


# testG = Grammar()
# testG.train_string(a)
# #print(testG.print_grammar())
# rules = testG.getRules()
# for rule in rules:
# 	print(rule)
# 	for k in rule.positions:
# 		# so i can get the start and then length of the expanded rule and that is how I can get the 
# 		print("first:")
# 		print(a[k].string)
# 		print("last")
# 		print(a[k + len(rule.expanded) - 1])




# timeseries = np.loadtxt('ecg0606_1.csv', delimiter="\n")
# s = SAX(4, 4)
# print('Time series length = {}'.format(len(timeseries)))

# saxterms = s.sliding_window(timeseries, 100)

# g = Grammar()
# g.train_string(saxterms)
# # #print(g.print_grammar())

# myrules = g.getRules()

# newlist = sorted(myrules[1:], key=lambda x: x.refCount, reverse=True)
# for rule in newlist:
# 	print(rule)
# 	for k in rule.positions:
# 		# so i can get the start and then length of the expanded rule and that is how I can get the 
# 		if not k == None:
# 			print("first:")
# 			print(len(saxterms))
# 			print(k)
# 			print(saxterms[k].string)
# 			print("last")
# 			print(len(saxterms))
# 			print(k + len(rule.expanded) - 1)
# 			print(saxterms[k + len(rule.expanded) - 1])




#s.numerosity_reductio	n(timeseries, 100)
#print(strings)
#print("now indices")
#print(indices)

## now do sequitur to get the grammar
# g = Grammar()
# #print(strings)
# g.train_string(strings)
# #print(g.print_grammar())
# print("now i am going to try stuff")

# rule_set = [g.root_production]
# i = 0

# myrules = []
# for rule in rule_set:
	
# 	print('expanded:')
# 	output_array = []
# 	# needed to generate the next 
# 	rule.print_rule(rule_set, output_array, 0)
# 	print(rule.reference_count)
# 	outputExpanded_array = []
# 	if i > 0:

# 		line_length = rule.print_rule_expansion(rule_set, outputExpanded_array, 0)
# 		print(outputExpanded_array)
# 		startIndices = []
# 		# first find all the matches
# 		for x in range(len(strings)):
# 			match = True
# 			for j in range(len(outputExpanded_array)):
# 				match &= (x+j < len(strings)) and (strings[x + j] == outputExpanded_array[j])
# 			if match == True:
# 				startIndices.append(x)
# 		myrules.append(Rule(i, rule.reference_count, output_array, outputExpanded_array))
# 		print("start indices:")
# 		print(startIndices)
# 		print("from strings:")
# 		## now expand it further since the strings was actually the numerosity reduction form
# 		for i in startIndices:
# 			actualString = []
# 			for k in range(len(outputExpanded_array)):
# 				reps = indices[i + k + 1] - indices[i + k]
# 				for j in range(reps):
# 					actualString.append(strings[i + k])
# 			myrules[len(myrules) - 1].addMatch(actualString)
		

# 		# now I can match to the original time series the expanded rule from the numerosity reduction form
# 		for x in range(len(myrules)):
# 			myrules[x].buildMatches(original, originalIndices)

# 		print("end from strings")

# 		print(len(startIndices))
# 		print('\n')
# 	print(i)
# 	i+=1

