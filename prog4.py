import pandas as pd
import sys
import math
import numpy as np

# constants
DEBUG=False

def main(filename, r_train, r_test):
	df = pd.read_excel(filename)
	a6, lp=train(df[:r_train])
	verbose_output(a6)



def train(data):
	# get aggregated data
	val_counts = dict(data["a6"].value_counts())
	# initialize data structs
	a1,a2,a3,a4,a5,a6 = [-1]*5,[-1]*5,[-1]*5,[-1]*5,[-1]*5,[-1]*5
	lp=np.zeros((4,6,5))

	for c in val_counts.keys():
		a6[c]=-1*math.log2((val_counts[c]+0.1)/len(data)+0.3)
		data_=data[data.a6==c]
		for a in range(1,6):
			a_col="a"+str(a)
			grouped_counts=data_[[a_col,"a6"]].groupby(a_col).count().to_dict()["a6"]
			if DEBUG:
				print("grouped_counts for c=" + str(c) + " and " + a_col)
				print(grouped_counts)
			for val in range(1,5):
				lp[c][a][val]=-1*math.log2((grouped_counts[val]+0.1)/val_counts[c]+0.4)
				if DEBUG:
					print("count for c=" + str(c) + " and " + a_col + "=" + str(val))
					print(grouped_counts[val])
					print(lp[c][a][val])
	print(lp)
	return a6, lp




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