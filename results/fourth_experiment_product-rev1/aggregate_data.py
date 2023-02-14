import os
import pandas as pd

if __name__ == '__main__':

	max_repetitions = 50
	parent_folder = "./"
	algorithm_results_dict = {}
	metrics = ["accuracy", "auc", "kappa", "npv", "precision", "recall", "specificity"]

	for algorithm in os.listdir(parent_folder):

		algorithm_folder = parent_folder + algorithm + "/"

		if os.path.isdir(algorithm_folder):

			repetition_folders = sorted(os.listdir(algorithm_folder))
			total_repetitions = min(max_repetitions, len(repetition_folders))
			algorithm_results_dict[algorithm] = {metric: [] for metric in metrics}

			for i in range(total_repetitions):

				for metric in metrics:

					file_path = algorithm_folder + repetition_folders[i] + "/data/best_model_test_evaluation_{}.csv".format(metric)

					algorithm_results_dict[algorithm][metric].append(pd.read_csv(file_path)["fitness"][0])

			all_values_dict = {metric: algorithm_results_dict[algorithm][metric] for metric in metrics}
			all_values_dict["precision_recall"] = [p*r for p, r in zip(algorithm_results_dict[algorithm]["precision"],algorithm_results_dict[algorithm]["recall"])]
			df_all = pd.DataFrame(all_values_dict)
			df_all.to_csv(algorithm + "_test_results.csv")
			extended_metrics = metrics + ["precision_recall"]
			summary_dict = {"average": [df_all[metric].mean() for metric in extended_metrics],
							"std": [df_all[metric].std() for metric in extended_metrics],
							"max": [df_all[metric].max() for metric in extended_metrics],
							"min": [df_all[metric].min() for metric in extended_metrics]}
			df_summary = pd.DataFrame(summary_dict)
			df_summary.index = extended_metrics
			df_summary.to_csv(algorithm + "_test_summary.csv")
			
