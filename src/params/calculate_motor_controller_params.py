import numpy as np

from src.utils.logger import AppLogger


class CalculateMotorControllerParams:
    def __init__(self, x_axis: list, y_ch1_axis: list, y_ch2_axis: list, logger=None):
        if logger is None:
            logger = AppLogger().get_logger()
        self.x_axis = x_axis
        self.y_ch1_axis = y_ch1_axis
        self.y_ch2_axis = y_ch2_axis
        self.y_infinity = np.mean(self.y_ch2_axis[1400:len(self.y_ch2_axis)])
        self.step_mean = np.mean(self.y_ch1_axis[1400:len(self.y_ch1_axis)])
        self.logger = logger

    def area_method(self) -> tuple:
        tau = self._calculate_tau()
        k = self._calculate_k()
        return tau, k

    def _calculate_tau(self) -> float:
        self.logger.info("CALCULATING tau:")
        self.logger.info(f"The value of y_infinity is: {self.y_infinity}\n")
        y_perm_point = 1513

        y_ch1_array = np.array(self.y_ch1_axis[0:y_perm_point])
        y_ch2_array = np.array(self.y_ch2_axis[0:y_perm_point])
        x_array = np.array(self.x_axis[0:y_perm_point])

        area_0 = np.trapz(y_ch2_array - y_ch1_array, x_array) * 10
        self.logger.info(f"The area between the response and y_infinity (A0) is: {area_0}\n")

        tau = area_0 / self.y_infinity
        self.logger.info(f"The value of tau is: {tau}\n")
        return tau

    def _calculate_k(self) -> float:
        self.logger.info(f"The value of the mean voltage of the step 'A' is: {self.step_mean} V")
        k = self.y_infinity / self.step_mean
        self.logger.info(f"The value of K is: {k}\n")
        return k

    def calculate_zeta(self, overshoot_percentage=0.1) -> float:
        overshoot_percentage = np.clip(overshoot_percentage, 1e-15, 1)
        zeta = -np.log(overshoot_percentage) / (np.sqrt(np.log(overshoot_percentage) ** 2 + np.pi ** 2))
        self.logger.info(f"The value of Zeta is: {zeta:.4f}\n")
        return zeta

    def calculate_omega_n(self, tau, zeta) -> float:
        omega_n = 1 / (tau * zeta)
        self.logger.info(f"The value of omega_n is: {omega_n:.4f}\n")
        return omega_n

    def calculate_kp(self, k, tau, zeta, omega_n) -> float:
        kp = ((2 * zeta * omega_n * tau) - 1) / k
        self.logger.info(f"The value of the Kp parameter is: {kp:.4f}\n")
        return kp

    def calculate_ti(self, k_mmq, tau, omega_n, kp) -> float:
        fi = ((omega_n ** 2) * tau) / (k_mmq * kp)
        self.logger.info(f"The value of the Fi parameter is: {fi:.4f}\n")
        ti = 1 / fi
        self.logger.info(f"The value of the Ti parameter is: {ti:.4f}\n")
        return ti
