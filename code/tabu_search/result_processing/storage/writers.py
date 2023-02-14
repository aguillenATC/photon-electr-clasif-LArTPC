import pandas as pd
import joblib
from ..base import Writer

class CSVWriter(Writer):

    def __init__(self, save: dict, target_tracker: str):

        super().__init__(save = save, target_tracker = target_tracker)

    def write(self) -> None:

        dataframe: pd.DataFrame = self.get_target_tracker().to_dataframe()
        save_path: str = self.results_path + self.subfolder
        self.check_and_create_folder_path(save_path)

        self.save_params["path_or_buf"] = save_path + self.save_params["fname"] + ".csv"
        self.save_params.pop("fname", None)
        dataframe.to_csv(**self.save_params)

class ModelWriter(Writer):

    def __init__(self, save: dict, target_tracker = "post_processing/final_model"):

        super().__init__(save = save, target_tracker = target_tracker)

    def write(self) -> None:

        model = self.get_target_tracker().get_last()
        save_path: str = self.results_path + self.subfolder
        self.check_and_create_folder_path(save_path)

        self.save_params["filename"] = save_path + self.save_params["fname"] + ".gz"
        self.save_params.pop("fname", None)

        joblib.dump(value = model, **self.save_params)
