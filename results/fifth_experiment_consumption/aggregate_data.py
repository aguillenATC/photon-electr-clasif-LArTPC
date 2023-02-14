import os
import pandas as pd

if __name__ == '__main__':

	max_repetitions = 5
	parent_folder = "./"
	algorithm_time_dict, algorithm_energy_dict = {}, {}

	for algorithm in os.listdir(parent_folder):

		algorithm_folder = parent_folder + algorithm + "/"

		if os.path.isdir(algorithm_folder):

			repetition_folders = sorted(os.listdir(algorithm_folder))
			total_repetitions = min(max_repetitions, len(repetition_folders))
			algorithm_time_dict[algorithm] = []
			algorithm_energy_dict[algorithm] = []

			for i in range(total_repetitions):

				time_file_path = algorithm_folder + repetition_folders[i] + "/data/time_elapsed.csv"
				energy_file_path = algorithm_folder + repetition_folders[i] + "/data/energy_consumption.csv"
				algorithm_time_dict[algorithm].append(pd.read_csv(time_file_path)["time"][0])
				algorithm_energy_dict[algorithm].append(pd.read_csv(energy_file_path)["acc_energy"][0])

			df = pd.DataFrame({"time": algorithm_time_dict[algorithm],
								"acc_energy": algorithm_energy_dict[algorithm]})

			print(algorithm + " average time: " + str(df["time"].mean()))
			print(algorithm + " std time: " + str(df["time"].std()))
			print(algorithm + " max time: " + str(df["time"].max()))
			print(algorithm + " min time: " + str(df["time"].min()))

			print(algorithm + " average energy: " + str(df["acc_energy"].mean()))
			print(algorithm + " std energy: " + str(df["acc_energy"].std()))
			print(algorithm + " max energy: " + str(df["acc_energy"].max()))
			print(algorithm + " min energy: " + str(df["acc_energy"].min()))

			df.to_csv(algorithm + "_time_energy_results.csv")