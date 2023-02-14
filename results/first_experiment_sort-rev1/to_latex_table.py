import pandas as pd 

if __name__ == '__main__':
	
	metric = "accuracy"
	dataset_list = ["concat_hits_padding", "concat_random_hits_padding", "sorted_hits_padding"]

	for hits in dataset_list:

		measurements = pd.read_csv(str(hits)+"/results_val.csv", index_col = 0)
		print("\\cellcolor{EffiYellow} \\textbf{" +str(hits) + "}", end = " ")

		for row in measurements.index:

			value = measurements.loc[row][metric]
			std = measurements.loc[row][metric+"_std"]

			if std > 0.0001:
				
				print("& " + str(round(value, 4)) + " $\\pm$ " + str(round(std, 4)), end = " ")

			else:

				print("& " + str(round(value, 4)), end = " ")

		print("\\\\")
		print("\\hline")

		