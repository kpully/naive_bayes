	grouped_counts = dict()
	grouped_counts[2] = data[["a2","a6"]].groupby(by="a2").count().to_dict()["a6"]
	grouped_counts[3] = data[["a3","a6"]].groupby(by="a3").count().to_dict()["a6"]
	grouped_counts[4] = data[["a4","a6"]].groupby(by="a4").count().to_dict()["a6"]
		grouped_counts[1] = data[["a1","a6"]].groupby(by="a1").count().to_dict()["a6"]
					print("-1*math.log2((" + str(v)+"+0.1)/val_counts[" +str(c)+"]+0.4)")
					# print("lp["+str(c)+"]["+str(a)+"][val]=" + str(lp[c][a][val]))

				print(numerator)
				print(denominator)

	if (len(sys.argv)<4):
		print("usage: python prog4.py filename r_train r_test")
		sys.exit(1)