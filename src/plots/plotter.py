import numpy as np
import matplotlib.pyplot as plt
from src.data.parser import DataParser
from src.utils.constants import XLSX_PATH, ARMOR_VOLTAGE, TACOMETER_VOLTAGE, POLY_DEGREE, CSV_PATH, ENGINE_SPEED
from src.utils.logger import AppLogger


class Plotter:
    def __init__(self, logger=None):
        if logger is None:
            logger = AppLogger().get_logger()
        self.logger = logger

    def plot_linear_region(self):
        armor, tachometer = DataParser(XLSX_PATH, self.logger).parse_xlsx(ARMOR_VOLTAGE, TACOMETER_VOLTAGE)
        plt.figure('Linear Region')
        plt.plot(armor, tachometer, 'o', label='Experimental Data')

        mmq_adjust = np.polyfit(armor, tachometer, POLY_DEGREE)
        pol_adjust = np.polyval(mmq_adjust, armor)
        plt.plot(armor, pol_adjust, label='Polynomial Fit (7th Degree)')

        derivative_adjust = np.polyval(np.polyder(mmq_adjust), armor)
        derivative_adjust[0] = derivative_adjust[1]
        derivative_adjust[-1] = derivative_adjust[-2]
        plt.plot(armor, derivative_adjust, label='Derivative of Polynomial Fit')

        horizontal_line = np.mean(derivative_adjust[11:])
        plt.axhline(y=horizontal_line, color='r', linestyle='--', label='Mean (from 12th point onwards)')

        self._set_plot_properties('Linear Region', 'Armature Voltage [V]', 'Tachometer Voltage [V]')

    def plot_motor_response(self):
        x_axis, y_ch1_axis, y_ch2_axis = DataParser(CSV_PATH, self.logger).parse_csv()
        plt.figure('Engine Response')
        plt.plot(x_axis, y_ch1_axis, linestyle='-', label='Step Response')
        plt.plot(x_axis, y_ch2_axis, linestyle='-', label='Motor Response')
        plt.legend()

        self._set_plot_properties('Motor Graph with Step Response', 'Time [s]', 'Voltage [V]')

    def plot_armature_tachometer(self):
        plt.figure('Armature Voltage x Tachometer Voltage')
        x_axis, y_axis = DataParser(XLSX_PATH, self.logger).parse_xlsx(ARMOR_VOLTAGE, TACOMETER_VOLTAGE)

        plt.plot(x_axis, y_axis, marker='o', linestyle='-')
        self._set_plot_properties('Va x Vt', 'Armature Voltage Va [V]', 'Tachometer Voltage Vt [V]')

    def plot_tachometer_speed(self):
        plt.figure('Tachometer Voltage x Engine Speed')
        x_axis, y_axis = DataParser(XLSX_PATH, self.logger).parse_xlsx(TACOMETER_VOLTAGE, ENGINE_SPEED)

        plt.plot(x_axis, y_axis, marker='o', linestyle='-')
        self._set_plot_properties('Vt x ω', 'Tachometer Voltage Vt [V]', 'Speed ω [RPM]')

    @staticmethod
    def _set_plot_properties(title, xlabel, ylabel):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()
