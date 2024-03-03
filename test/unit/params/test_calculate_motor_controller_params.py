from unittest.mock import Mock, patch
import numpy as np

from src.utils.logger import AppLogger
from src.params.calculate_motor_controller_params import CalculateMotorControllerParams
import pytest


class CustomLogger(Mock):
    def info(self, *args, **kwargs):
        pass


class TestCalculateMotorControllerParams:

    @pytest.fixture
    def motor_params_instance(self):
        x_axis = [1, 2, 3, 4, 5]
        y_ch1_axis = [2, 4, 6, 8, 10]
        y_ch2_axis = [1, 3, 5, 7, 9]
        logger = CustomLogger(spec=AppLogger)
        return CalculateMotorControllerParams(x_axis, y_ch1_axis, y_ch2_axis, logger)

    @patch.object(CalculateMotorControllerParams, '_calculate_tau', return_value=2.0)
    @patch.object(CalculateMotorControllerParams, '_calculate_k', return_value=3.0)
    def test_area_method(self, mock_calculate_k, mock_calculate_tau, motor_params_instance):
        expected_result = (2.0, 3.0)
        result = motor_params_instance.area_method()
        assert result == expected_result
        mock_calculate_k.assert_called_once()
        mock_calculate_tau.assert_called_once()

    def test_calculate_tau(self, motor_params_instance):
        motor_params_instance.x_axis = np.linspace(0, 10, 2000)
        motor_params_instance.y_ch1_axis = np.sin(motor_params_instance.x_axis)
        motor_params_instance.y_ch2_axis = np.cos(motor_params_instance.x_axis)
        expected_tau = 1
        motor_params_instance.y_infinity = 2.4432985183604927
        tau = motor_params_instance._calculate_tau()
        assert tau == expected_tau
        assert isinstance(tau, float)

    def test_calculate_k(self, motor_params_instance):
        motor_params_instance.y_infinity = 2.0
        motor_params_instance.step_mean = 1.0
        expected_k = 2.0
        k = motor_params_instance._calculate_k()
        assert k == expected_k
        assert isinstance(k, float)

    def test_calculate_zeta(self, motor_params_instance):
        expected_zeta = 0.5912
        zeta = motor_params_instance.calculate_zeta()
        assert round(zeta, 4) == expected_zeta
        assert isinstance(zeta, float)

    def test_calculate_omega_n(self, motor_params_instance):
        tau = 2.0
        zeta = 0.5
        expected_omega_n = 1 / (tau * zeta)
        omega_n = motor_params_instance.calculate_omega_n(tau, zeta)
        assert omega_n == expected_omega_n
        assert isinstance(omega_n, float)

    def test_calculate_kp(self, motor_params_instance):
        k = 2.0
        tau = 1.0
        zeta = 0.5
        omega_n = 2.0
        expected_kp = ((2 * zeta * omega_n * tau) - 1) / k
        kp = motor_params_instance.calculate_kp(k, tau, zeta, omega_n)
        assert kp == expected_kp
        assert isinstance(kp, float)

    def test_calculate_ti(self, motor_params_instance):
        k_mmq = 1.0
        tau = 2.0
        omega_n = 1.0
        kp = 0.5
        expected_ti = 1 / (((omega_n ** 2) * tau) / (k_mmq * kp))
        ti = motor_params_instance.calculate_ti(k_mmq, tau, omega_n, kp)
        assert ti == expected_ti
        assert isinstance(ti, float)
