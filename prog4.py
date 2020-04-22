import pandas as pd
import sys
import math
import numpy as np

# constants
DEBUG=True

def main(filename, r_train, r_test):
	df = pd.read_excel(filename)
	a6, lp=train(df[:r_train])
	test(df[r_train:r_test],lp)
	verbose_output(a6)



def train(data):
	if DEBUG:
		print(data)
	# get aggregated data
	val_counts = dict(data["a6"].value_counts())
	if DEBUG:
		print(val_counts)
	# initialize data structs
	a1,a2,a3,a4,a5,a6 = [-1]*5,[-1]*5,[-1]*5,[-1]*5,[-1]*5,[-1]*5
	lp=np.zeros((4,6,5))
	# print(lp)

	for c in val_counts.keys():
		numerator=val_counts[c]+0.1
		denominator=len(data)+0.3
		a6[c]=-1*math.log2(numerator/denominator)
		data_=data[data.a6==c]
		for a in range(1,6):
			a_col="a"+str(a)
			grouped_counts=data_[[a_col,"a6"]].groupby(a_col).count().to_dict()["a6"]
			for val in range(1,5):
				if val in grouped_counts.keys():
					v = grouped_counts[val]
				else:
					v=0
				numerator = v+0.1
				denominator = val_counts[c]+0.4
				lp[c][a][val]=-1*math.log2(numerator/denominator)
				if DEBUG:
					print("count for c=" + str(c) + " and " + a_col + "=" + str(val) + ": " + "grouped_counts[v]=" + str(v))
			print()
		print("<------>")


	print(lp)
	return a6, lp


def test(data, lp):
	if DEBUG:
		print(data)
	inferences = []
	for i, row in data.iterrows():
		get_inference(row[0], row[1], row[2], row[3], row[4], lp)

def get_inference(a1_val, a2_val, a3_val, a4_val, a5_val, lp):
	if DEBUG:
		print("get_inference")
	sums = []
	for c in range(1,4):
		s = lp[c][1][a1_val] \
			+ lp[c][2][a2_val] \
			+ lp[c][3][a3_val] \
			+ lp[c][4][a4_val] \
			+ lp[c][5][a5_val]
		sums.append(s)
	if DEBUG:
		print(sums)




def verbose_output(a6):
	s1 = "lp(X.a6={c})={val_count}"
	s2 = "lp(X.a%d=%d|X.a6=%d)"
	for c in range(1,len(a6)-1):
		print(s1.format(c=c, val_count=a6[c]))

def output():
	s="Accuracy=%.2f. Precision=%.2f. Recall=%.2d"

if __name__=="__main__":
	if (len(sys.argv)<4):
		print("usage: python prog4.py filename r_train r_test")
		sys.exit(1)
	main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))