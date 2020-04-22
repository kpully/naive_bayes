import pandas as pd
import sys
import math
import numpy as np
import argparse
import random

# constants
debug=False
verbose=False


def main(filename, r_train, r_test, v, d):
	# set global variables
	global verbose, debug
	verbose = v
	debug = d

	# read data
	df = pd.read_excel(filename)

	# train
	a6, lp=train(df[:r_train])

	# test
	test(df[r_train:r_train+r_test],lp)

	# output
	if verbose:
		verbose_output(a6, lp)
	output()


def train(data):
	if debug:
		print(data)
	# get aggregated data
	val_counts = dict(data["a6"].value_counts())
	if debug:
		print(val_counts)
	# initialize data structs
	a1,a2,a3,a4,a5 = [-1]*5,[-1]*5,[-1]*5,[-1]*5,[-1]*5
	a6=[-1]*4
	lp=np.zeros((4,6,5))

	for c in range(1,4):
		val_counts_c = val_counts[c] if c in val_counts.keys() else 0
		numerator=val_counts_c+0.1
		denominator=len(data)+0.3
		a6[c]=-1*math.log2(numerator/denominator)

	for c in range(1,4):
		data_=data[data.a6==c]
		for a in range(1,6):
			a_col="a"+str(a)
			grouped_counts=data_[[a_col,"a6"]].groupby(a_col).count().to_dict()["a6"]
			for val in range(1,5):
				if val in grouped_counts.keys():
					v = grouped_counts[val]
				else:
					v=0
				val_counts_c = val_counts[c] if c in val_counts.keys() else 0
				numerator = v+0.1
				denominator = val_counts_c+0.4
				lp[c][a][val]=-1*math.log2(numerator/denominator)
	if debug:
		print(lp)
	return a6, lp


def test(data, lp):
	if debug:
		print(data)
	inferences = []
	for i, row in data.iterrows():
		inference = get_inference(row[0], row[1], row[2], row[3], row[4], lp) + 1
		inferences.append(inference)
	if debug:
		print(inferences)
	accuracy = evaluate_model(inferences, data["a6"])


def get_inference(a1_val, a2_val, a3_val, a4_val, a5_val, lp):
	sums = []
	for c in range(1,4):
		s = lp[c][1][a1_val] \
			+ lp[c][2][a2_val] \
			+ lp[c][3][a3_val] \
			+ lp[c][4][a4_val] \
			+ lp[c][5][a5_val]
		sums.append(s)
	if debug:
		print(sums)
	return get_max_index(sums)


def evaluate_model(guesses, correct):
	print(guesses)
	print(correct)
	a = [i for i, j in zip(guesses, correct) if i == j]
	accuracy=len(a)/len(guesses)
	print(accuracy)
	return 0.0


def get_max_index(lst):
	"""
	Get max value of lst
	Break ties arbitrarily
	"""
	max_vals=[lst[0]]
	max_is=[0]
	for i in range(1,len(lst)):
		if (lst[i]>max_vals[0]):
			max_vals=[lst[i]]
			max_is=[i]
		elif (lst[i]==max_vals[0]):
			max_vals.append(lst[i])
			max_is.append(i)
	i = random.randint(0,len(max_vals)-1)
	max_i=max_is[i]
	return max_i


def verbose_output(a6, lp):
	# format string skeletongs
	s1 = "lp(X.a6={c})={val_count:.4f}"
	s2 = "{lp_:.4f}"

	# loop and print results
	for c in range(1,4):
		print(s1.format(c=c, val_count=a6[c]), end = '\t')
	print()
	print()
	for a in range(1,6):
		for c in range(1,4):
			for a_val in range(1,5):
				# print(s2.format(a=a, a_val=a_val, c=c), end = '\t')
				print(s2.format(lp_=lp[c][a][a_val]), end='\t')
			print()
		print()
	print()


def output():
	s="Accuracy=%.2f. Precision=%.2f. Recall=%.2d"
	print(s)


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Naive Bayes')
	parser.add_argument('-v', help='verbose output', action='store_true')
	parser.add_argument('-d', help='debug mode', action='store_true')
	parser.add_argument("filename", help="file containing data")
	parser.add_argument("r_train", help="number of rows for training")
	parser.add_argument("r_test", help="number of rows for testing")

	args = parser.parse_args()

	main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), args.v, args.d)