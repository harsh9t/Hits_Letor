import collections
from sklearn import svm


data_set = []

def compute_row(data1, data2):
		if(data1[0] > data2[0]):
			output = [1]
		else:
			output = [-1]
		output.extend([a - b for a, b in zip(data1[1], data2[1])])
		return output

def compute_table(data):
	length = len(data)
	for i in range(0,length):
		for j in range(i+1,length):
			if(data[i][0] == data[j][0]):
				continue
			data_set.append(compute_row(data[i], data[j]))
			data_set.append(compute_row(data[j], data[i]))

def parse_input_file(filename):
	query_relevance = collections.defaultdict(lambda: [])

	with open(filename, 'r') as f:
	    for line in f:
	    	input_vector = line.split()
	    	relevance = float(input_vector[0])
	        qid = input_vector[1].split(":")[1]
	        query_relevance[qid].append([relevance, [float(a.split(":")[1]) for a in input_vector[2:]]])

	for query in query_relevance:
		compute_table(query_relevance[query])
	return data_set

def learn_to_rank(folder):
	folder_name = folder[0]
	C = folder[1]
	print "\nFolder name is", folder_name
	global data_set
	training_set = parse_input_file("./files/part2/"+folder_name+"/train.txt")
	data_set = []
	test_set = parse_input_file("./files/part2/"+folder_name+"/test.txt")
	data_set = []

	X1 = [a[1:] for a in training_set]
	Y1 = [a[0]  for a in training_set]

	X2 = [a[1:] for a in test_set]
	Y2 = [a[0]  for a in test_set]

	svc = svm.SVC(kernel='linear', C=C).fit(X1, Y1)

	Z = svc.predict(X2).tolist()

	accuracy_count = 0
	for i in range(0,len(Y2)):
		if(Y2[i] == Z[i]):
			accuracy_count += 1

	leng = len(Y2)
	print "\nAccuracy of the ranker is ", accuracy_count * 100.0 / leng
	print "Accuracy obtained at C = ", C

	weight_hash = {}
	i = 1
	for val in svc.coef_.tolist()[0]:
		weight_hash[i] = [val, abs(val)]
		i+=1
		if(i == 6):
			i = 11
		if(i == 43):
			i += 1

	weight_hash = sorted(weight_hash.items(), key=lambda x: x[1][1], reverse=True)

	print "\nTen most important weights for this folder"
	for val in weight_hash[:10]:
		print "feature", val[0], " - ", val[1][0]
	print "______________________________________________________________________________________\n"

for fold in [["fold1",0.04],["fold2",8.3],["fold3",0.003]]: #passing the folder name and best C found so far
	learn_to_rank(fold)