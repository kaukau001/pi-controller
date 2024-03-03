import unittest
from unittest.mock import MagicMock
from src.params.simulation_params_calculator import SimulationParamsCalculator


class TestSimulationParamsCalculator(unittest.TestCase):

    def setUp(self):
        self.voltage = [1, 2, 3, 4, 5]
        self.tachometer = [10, 20, 30, 40, 50]
        self.rotation = [100, 200, 300, 400, 500]

    def test_calculate_k_mmq(self):
        logger_mock = MagicMock()
        calculator = SimulationParamsCalculator(self.voltage, self.tachometer, self.rotation, logger_mock)
        result = round(calculator.calculate_k_mmq(), 1)

        self.assertEqual(result, 10.0)

    def test_calculate_kt(self):
        logger_mock = MagicMock()
        calculator = SimulationParamsCalculator(self.voltage, self.tachometer, self.rotation, logger_mock)
        result = calculator.calculate_kt()

        expected_angle_coefficient = 0.0010471975511965977

        self.assertAlmostEqual(result, expected_angle_coefficient, places=4)
