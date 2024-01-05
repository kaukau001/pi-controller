import numpy as np
from numpy.polynomial import polynomial

from src.utils.logger import AppLogger


class SimulationParamsCalculator:
    def __init__(self, voltage: list, tachometer: list, rotation: list, logger=None):
        if logger is None:
            logger = AppLogger().get_logger()
        self.voltage = voltage
        self.tachometer = tachometer
        self.rotation = rotation
        self.logger = logger

    def calculate_k_mmq(self) -> float:
        mmq_coefficients = polynomial.polyfit(self.voltage, self.tachometer, 1)
        angle_coefficient = float(mmq_coefficients[1])
        self.logger.info(f"The angular coefficient (K) obtained by least squares: {angle_coefficient:.4f}\n")
        return angle_coefficient

    def calculate_kt(self):
        mmq_coefficients = polynomial.polyfit(self.rotation, self.voltage, 1)
        angle_coefficient = float(mmq_coefficients[1]) * (2 * np.pi / 60)
        self.logger.info(f"The angular coefficient (Kt) obtained by least squares:\n"
                         f"(rad/s)/V -> {angle_coefficient:.4f} (rad/s)/V\n"
                         f"rpm/V -> {mmq_coefficients[1]: .4f} rpm/V\n")
        return angle_coefficient
