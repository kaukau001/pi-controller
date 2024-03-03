import unittest
from unittest.mock import MagicMock
from src.plots.plotter import Plotter


class TestPlotter(unittest.TestCase):
    """
    Integration test suite for the Plotter class.

    These tests aim to validate the integration between the Plotter class's plotting functions and a database.

    """
    def setUp(self):
        self.logger_mock = MagicMock()

    def test_plot_linear_region(self):
        plotter = Plotter(self.logger_mock)
        plotter.plot_linear_region()

    def test_plot_motor_response(self):
        plotter = Plotter(self.logger_mock)
        plotter.plot_motor_response()

    def test_plot_armature_tachometer(self):
        plotter = Plotter(self.logger_mock)
        plotter.plot_armature_tachometer()

    def test_plot_tachometer_speed(self):
        plotter = Plotter(self.logger_mock)
        plotter.plot_tachometer_speed()

    def test_set_plot_properties(self):
        plotter = Plotter(self.logger_mock)
        plotter._set_plot_properties('title', 'x', 'y')
