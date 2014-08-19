import cjson
import networkx as nx
import collections
import copy
import math

def isSame(hash1,hash2): # to see if the hub / authority values has converged
	if(len(hash1) != len(hash2)):
		return False
	for key in hash1.keys():
		if(hash1[key]-hash2[key] > 0.00001):
			return False
	return True

def print_ouptut(tuples, header): # prints top 20 hubs and authorities
	print ""
	print "Top 20", header
	print "====================================================================="
	for a in tuples:
		print a[0]

filename = "./files/part1/tweets.txt"
G=nx.DiGraph()
with open(filename, 'r') as f:
    for line in f:
        data = cjson.decode(line)
        G.add_node(data['user']['screen_name'])
        for mention in data['entities']['user_mentions']:
        	if(data['user']['screen_name'] != mention['screen_name']):
        		G.add_edge(data['user']['screen_name'], mention['screen_name'])

maximal_weak_subgraph =  nx.weakly_connected_component_subgraphs(G)[0]

hubs = collections.defaultdict(lambda: 1.0)
hubs2 = collections.defaultdict(lambda: 1.0)
authorities = collections.defaultdict(lambda: 1.0)
authorities2 = collections.defaultdict(lambda: 1.0)

in_and_out = collections.defaultdict(lambda: {"successors":[], "predecessors":[]}) #structure that stores hubs and authorities of each node

for node in maximal_weak_subgraph.nodes():
	in_and_out[node]["successors"] = maximal_weak_subgraph.successors(node)
	in_and_out[node]["predecessors"] = maximal_weak_subgraph.predecessors(node)
	hubs[node] = 1.0 #initialize to 1
	authorities[node] = 1.0 #initialize to 1

i = 0 # to count number of iterations before converging
while(1):
	for node in maximal_weak_subgraph.nodes(): #compute hubs and authorities in batch
		hubs2[node] = sum([authorities[a] for a in in_and_out[node]["successors"]])
		authorities2[node] = sum([hubs[a] for a in in_and_out[node]["predecessors"]])

	max_hub_val = max(hubs2.values())
	max_authority_val = max(authorities2.values())

	for node in maximal_weak_subgraph.nodes():
		hubs2[node] /= max_hub_val
		authorities2[node] /= max_authority_val

	if(isSame(hubs,hubs2) and isSame(authorities, authorities2)):
		break
	hubs = copy.deepcopy(hubs2)
	authorities = copy.deepcopy(authorities2)
	i += 1

print ""
print i, "iterations to converge"
top_hubs = sorted(hubs2.items(), key=lambda x: (x[1], x[0]), reverse=True) #sort on the score and then equal scores are sorted on the name of nodes
top_authorities = sorted(authorities2.items(), key=lambda x: (x[1], x[0]), reverse=True) #sort on the score and then equal scores are sorted on the name of nodes

print_ouptut(top_hubs[:20], "Hubs")
print_ouptut(top_authorities[:20], "Authorities")