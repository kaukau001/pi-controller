import os
import pandas as pd
import numpy as np
from src.utils.exceptions import InvalidExtensionError
from src.utils.logger import AppLogger


class DataParser:
    def __init__(self, file_path: str, logger: None):
        if logger is None:
            logger = AppLogger().get_logger()
        self.file_path = file_path
        self.logger = logger

    def parse_csv(self) -> tuple:
        try:
            self._check_file_exists()
            file_extension = self._check_file_extension()

            if file_extension != '.csv':
                raise InvalidExtensionError('The file does not have a .csv extension')

            data = pd.read_csv(self.file_path)

            if data.empty:
                raise ValueError(f"The file {self.file_path} is empty.")

            x_axis, y_chanel_one_axis, y_chanel_two_axis = self._extract_data_columns(data)

            linearized_x_axis = self._linearize_data(x_axis)[0]
            linearized_y_chanel_one_axis = self._linearize_data(y_chanel_one_axis)[0]
            linearized_y_chanel_two_axis = self._linearize_data(y_chanel_two_axis)[0]

            return linearized_x_axis, linearized_y_chanel_one_axis, linearized_y_chanel_two_axis

        except InvalidExtensionError as e:
            self.logger.error(f"Error processing the file: {e}")
        except ValueError as e:
            self.logger.error(f"Error processing the file: {e}")

    def parse_xlsx(self, x_column: str, y_column: str, z_column: str or None = None) -> tuple:
        try:
            self._check_file_exists()
            file_extension = self._check_file_extension()

            if file_extension != '.xlsx':
                raise InvalidExtensionError('The file does not have a .xlsx extension')

            data = pd.read_excel(self.file_path)
            if data.empty:
                raise ValueError(f"The file {self.file_path} is empty.")

            if not all(col in data.columns for col in (x_column, y_column)):
                raise ValueError("The specified columns do not exist in the dataset.")

            if z_column is not None:
                if z_column not in data.columns:
                    raise ValueError("The specified z column does not exist in the dataset.")
                x_axis, y_axis, z_axis = data[x_column], data[y_column], data[z_column]
                return x_axis, y_axis, z_axis
            x_axis, y_axis = data[x_column], data[y_column]
            return x_axis, y_axis
        except InvalidExtensionError as e:
            self.logger.error(f"Error processing the file: {e}")
        except ValueError as e:
            self.logger.error(f"Error processing the file: {e}")

    def linearize_xlsx(self, x_column, y_column, z_column):
        try:
            x_axis, y_axis, z_axis = self.parse_xlsx(x_column, y_column, z_column)

            linearized_x = self._linearize_data(x_axis)[0]
            linearized_y = self._linearize_data(y_axis)[0]

            if z_column:
                linearized_z = self._linearize_data(z_axis)[0]
                return linearized_x, linearized_y, linearized_z

            return linearized_x, linearized_y
        except Exception as e:
            self.logger.error(f"Error linearizing the data: {e}")

    def _check_file_exists(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} was not found.")

    def _check_file_extension(self):
        try:
            file_name, file_extension = os.path.splitext(self.file_path)
            if file_extension not in ['.xlsx', '.csv']:
                raise InvalidExtensionError()
            return file_extension
        except InvalidExtensionError as e:
            self.logger.error(e.message)

    @staticmethod
    def _extract_data_columns(data):
        index_x = 0
        index_y_ch1 = 1
        index_y_ch2 = 2

        x_axis = data.iloc[:, index_x]
        y_chanel_one_axis = data.iloc[:, index_y_ch1]
        y_chanel_two_axis = data.iloc[:, index_y_ch2]

        return x_axis, y_chanel_one_axis, y_chanel_two_axis

    @staticmethod
    def _linearize_data(*axes):
        return tuple(np.array(axis) - np.array(axis.iloc[0]) for axis in axes)
