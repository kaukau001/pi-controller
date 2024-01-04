from unittest.mock import Mock
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

    def test_calculate_k(self, motor_params_instance):
        motor_params_instance.y_infinity = 2.0
        motor_params_instance.step_mean = 1.0
        expected_k = 2.0
        k = motor_params_instance.calculate_k()
        assert k == expected_k

    def test_calculate_zeta(self, motor_params_instance):
        expected_zeta = 0.5912
        zeta = motor_params_instance.calculate_zeta()
        assert round(zeta, 4) == expected_zeta

