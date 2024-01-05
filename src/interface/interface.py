import tkinter as tk
import pandas as pd
from pandas import DataFrame
from io import StringIO
from src.utils.constants import XLSX_PATH, ARMOR_VOLTAGE, TACOMETER_VOLTAGE, CSV_PATH, ENGINE_SPEED, ROTINE_PATH
from src.data.parser import DataParser
from src.plots.plotter import Plotter
import logging
from tkinter import scrolledtext
from tkinter import ttk
from src import rotine
from src.utils.logger import AppLogger


class DataAnalysisInterface:
    def __init__(self, window):

        style = tk.ttk.Style()
        style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 10 bold', background='#ccc')

        self.log_buffer = StringIO()
        logging.basicConfig(stream=self.log_buffer, level=logging.DEBUG)
        self.logger = AppLogger.get_instance()

        self.window = window
        self.plotter = Plotter(self.logger)

        self.window.title("Interface for Processing and Plotting Files")
        style = ttk.Style(self.window)

        style.configure('TButton', padding=(5, 2), font=('Helvetica', 12))

        self.label_xlsx = tk.Label(self.window, text="Experiment Data:")
        self.label_xlsx.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)

        self.entry_xlsx = tk.Entry(self.window)
        self.entry_xlsx.grid(row=0, column=1, columnspan=3, pady=5, padx=5)

        self.label_csv = tk.Label(self.window, text="Oscilloscope Data:")
        self.label_csv.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)

        self.entry_csv = tk.Entry(self.window)
        self.entry_csv.grid(row=1, column=1, columnspan=3, pady=5, padx=5)

        self.process_button = tk.Button(self.window, width=20, text="Process Files", command=self.process_files)
        self.process_button.grid(row=2, column=0, columnspan=4, pady=10, padx=5)

        self.plot_linear_region_button = tk.Button(self.window, width=20, text="Plot Linear Region",
                                                   command=self.plotter.plot_linear_region)
        self.plot_linear_region_button.grid(row=3, column=0, columnspan=4, pady=5, padx=5)

        self.plot_motor_response_button = tk.Button(self.window, width=20, text="Plot Motor Response",
                                                    command=self.plotter.plot_motor_response)
        self.plot_motor_response_button.grid(row=4, column=0, columnspan=4, pady=5, padx=5)

        self.plot_armature_tachometer_button = tk.Button(self.window, width=20, text="Plot Va x Vt",
                                                         command=self.plotter.plot_armature_tachometer)
        self.plot_armature_tachometer_button.grid(row=5, column=0, columnspan=4, pady=5, padx=5)

        self.plot_tachometer_speed_button = tk.Button(self.window, width=20, text="Plot Vt x ω",
                                                      command=self.plotter.plot_tachometer_speed)
        self.plot_tachometer_speed_button.grid(row=6, column=0, columnspan=4, pady=5, padx=5)

        self.generate_report_button = tk.Button(self.window, width=20, text="Generate Report",
                                                command=self.generate_report)
        self.generate_report_button.grid(row=7, column=0, columnspan=4, pady=10, padx=5)

        self.log_text = scrolledtext.ScrolledText(self.window, width=80, height=15, wrap=tk.WORD)
        self.log_text.grid(row=8, column=0, columnspan=4, pady=10, padx=5)

        self.log_text = scrolledtext.ScrolledText(self.window, width=80, height=15, wrap=tk.WORD)
        self.log_text.grid(row=8, column=0, columnspan=4, pady=10, padx=5, sticky=tk.NSEW)

        self.default_path_xlsx = XLSX_PATH
        self.default_path_csv = CSV_PATH

        self.entry_xlsx.insert(0, self.default_path_xlsx)
        self.entry_csv.insert(0, self.default_path_csv)
        self.window.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        width, height = event.width, event.height

        log_text_height = max(5, (height - 350) // 20)
        self.log_text.config(height=log_text_height)
        self.log_text.grid(row=8, column=0, columnspan=4, pady=(10, 0), padx=5, sticky=tk.NSEW)
        self.entry_xlsx.config(width=100)
        self.entry_csv.config(width=100)
        self.window.grid_rowconfigure(8, weight=1)

        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1 if i == 1 else 0)

    def process_files(self):
        try:
            self.log_text.delete('1.0', tk.END)
            self.logger.info('Processing files')
            path_xlsx = self.entry_xlsx.get() or self.default_path_xlsx
            path_csv = self.entry_csv.get() or self.default_path_csv

            data_parser_xlsx = DataParser(file_path=path_xlsx, logger=self.logger)
            data_parser_csv = DataParser(file_path=path_csv, logger=self.logger)

            armor, tachometer, engine_speed = data_parser_xlsx.parse_xlsx(x_column=ARMOR_VOLTAGE,
                                                                          y_column=TACOMETER_VOLTAGE,
                                                                          z_column=ENGINE_SPEED)
            x_axis, y_chanel_one_axis, y_chanel_two_axis = data_parser_csv.parse_csv()

            df_xlsx = pd.DataFrame({
                'Armor Voltage': armor,
                'Tachometer Voltage': tachometer,
                'Engine Speed': engine_speed
            })
            df_csv = pd.DataFrame({
                'Time': x_axis,
                'Chanel 1': y_chanel_one_axis,
                'Chanel 2': y_chanel_two_axis
            })

            self.show_data(df_xlsx, "Experiment Data")
            self.show_data(df_csv, "Oscilloscope Data")

            self.logger.info('Successfully processed files')
            log_output = self.logger.get_log_buffer().getvalue()
            self.log_text.insert(tk.END, log_output)
        except Exception as e:
            error_message = f"Error generating the report: {e}\n"
            self.log_text.insert(tk.END, error_message)
            self.logger.error(error_message)

    def show_data(self, dataframe: DataFrame, title: str):
        try:

            data_window = tk.Toplevel(self.window)
            data_window.title(title)

            window_height = min(500, len(dataframe) * 20)
            data_window.geometry(f"500x{window_height}")

            data_text = tk.Text(data_window, height=len(dataframe), width=60)
            data_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(data_window, command=data_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            data_text.config(yscrollcommand=scrollbar.set)

            data_text.insert(tk.END, dataframe.to_string(index=False))

        except Exception as e:
            error_message = f"Error generating the report: {e}\n"
            self.log_text.insert(tk.END, error_message)
            self.logger.error(error_message)

    def generate_report(self):
        try:
            self.log_text.delete('1.0', tk.END)
            rotine.rotine(self.entry_xlsx.get(), self.entry_csv.get(), self.logger)

            log_output = self.logger.get_log_buffer().getvalue()

            self.log_text.insert(tk.END, log_output)

        except Exception as e:
            error_message = f"Error generating the report: {e}\n"
            self.log_text.insert(tk.END, error_message)
            self.logger.error(error_message)


main_window = tk.Tk()

main_interface = DataAnalysisInterface(main_window)

main_window.mainloop()
