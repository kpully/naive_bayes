	grouped_counts = dict()
	grouped_counts[2] = data[["a2","a6"]].groupby(by="a2").count().to_dict()["a6"]
	grouped_counts[3] = data[["a3","a6"]].groupby(by="a3").count().to_dict()["a6"]
	grouped_counts[4] = data[["a4","a6"]].groupby(by="a4").count().to_dict()["a6"]
		grouped_counts[1] = data[["a1","a6"]].groupby(by="a1").count().to_dict()["a6"]
