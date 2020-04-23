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
	a6, lp = train(df[:r_train])

	# test
	accuracy, precision = test(df[r_train:r_train+r_test],lp, a6)

	# output
	if verbose:
		verbose_output(a6, lp)
	output(accuracy, precision)


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


def test(data, lp, a6):
	if debug:
		print(data)
	inferences = []
	for i, row in data.iterrows():
		inference = get_inference(row[0], row[1], row[2], row[3], row[4], lp,a6) + 1
		inferences.append(inference)
	if debug:
		print(inferences)
	accuracy = evaluate_model(inferences, data["a6"])
	return accuracy


def get_inference(a1_val, a2_val, a3_val, a4_val, a5_val, lp, a6):
	sums = []
	for c in range(1,4):
		if debug:
			print("a1_val=" + str(a1_val))
			print(lp[c][1][a1_val])
			print("a2_val=" + str(a2_val))
			print(lp[c][2][a2_val])
			print("a3_val=" + str(a3_val))
			print(lp[c][3][a3_val])
			print("a4_val=" + str(a4_val))
			print(lp[c][4][a4_val])
			print("a5_val=" + str(a5_val))
			print(lp[c][5][a5_val])
		s = lp[c][1][a1_val] \
			+ lp[c][2][a2_val] \
			+ lp[c][3][a3_val] \
			+ lp[c][4][a4_val] \
			+ lp[c][5][a5_val] \
			+ a6[c]
		sums.append(s)
	if debug:
		print(sums)
	return get_min_index(sums)


def evaluate_model(guesses, correct):
	zipped=list(zip(guesses,correct))
	a=0
	p_truepos = 0
	p_falsepos = 0
	if debug:
		print(zipped)
	for i in range(len(zipped)):
		pair = zipped[i]
		if (pair[0]==pair[1]):
			a+=1
		if (pair[0]==3):
			if (pair[1]==3):
				p_truepos+=1
			else:
				p_falsepos+=1

	accuracy=a/len(zipped)
	precision=p_truepos/(p_truepos+p_falsepos)
	return accuracy, precision


def get_min_index(lst):
	"""
	Get max value of lst
	Break ties arbitrarily
	"""
	min_vals=[lst[0]]
	min_is=[0]
	for i in range(1,len(lst)):
		if (lst[i]<min_vals[0]):
			min_vals=[lst[i]]
			min_is=[i]
		elif (lst[i]==min_vals[0]):
			min_vals.append(lst[i])
			min_is.append(i)
	i = random.randint(0,len(min_vals)-1)
	min_i=min_is[i]
	return min_i


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


def output(accuracy, precision):
	s="Accuracy={accuracy:.4f}. Precision={precision:.4f}. Recall=%.2d"
	print(s.format(accuracy=accuracy, precision=precision))


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Naive Bayes')
	parser.add_argument('-v', help='verbose output', action='store_true')
	parser.add_argument('-d', help='debug mode', action='store_true')
	parser.add_argument("filename", help="file containing data")
	parser.add_argument("r_train", help="number of rows for training")
	parser.add_argument("r_test", help="number of rows for testing")

	args = parser.parse_args()

	main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), args.v, args.d)