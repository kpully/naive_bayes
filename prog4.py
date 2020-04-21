import pandas as pd
import sys
import math

def main(filename, r_train, r_test):
	print("hello world")
	print(filename)
	df = pd.read_excel(filename);
	print(df.head())
	train(df[:r_train])


def train(data):
	value_counts = dict(data["a6"].value_counts())
	a6 = []
	# math.log2()


def verbose_output():
	s = "lp(X.a%d=%d|X.a6=%d)"

def output():
	s="Accuracy=%.2f. Precision=%.2f. Recall=%.2d"

if __name__=="__main__":
	if (len(sys.argv)<4):
		print("usage: python prog4.py filename r_train r_test")
		sys.exit(1)
	main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))