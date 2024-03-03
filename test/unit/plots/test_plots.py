import unittest
from unittest.mock import MagicMock, patch
from src.plots.plotter import Plotter


class TestPlotter(unittest.TestCase):

    def setUp(self):
        self.logger_mock = MagicMock()

    @patch('src.plots.plotter.DataParser')
    @patch('src.plots.plotter.plt.show')
    def test_plot_linear_region(self, plt_show_mock, data_parser_mock):
        data_parser_mock.return_value.parse_xlsx.return_value = ([1, 2, 3], [4, 5, 6])
        plotter = Plotter(self.logger_mock)
        plotter.plot_linear_region()

        plt_show_mock.assert_called_once()

    @patch('src.plots.plotter.DataParser')
    @patch('src.plots.plotter.plt.show')
    def test_plot_motor_response(self, plt_show_mock, data_parser_mock):
        data_parser_mock.return_value.parse_csv.return_value = ([1, 2, 3], [4, 5, 6], [7, 8, 9])
        plotter = Plotter(self.logger_mock)
        plotter.plot_motor_response()

        plt_show_mock.assert_called_once()

    @patch('src.plots.plotter.DataParser')
    @patch('src.plots.plotter.plt.show')
    def test_plot_armature_tachometer(self, plt_show_mock, data_parser_mock):
        data_parser_mock.return_value.parse_xlsx.return_value = ([1, 2, 3], [4, 5, 6])
        plotter = Plotter(self.logger_mock)
        plotter.plot_armature_tachometer()

        plt_show_mock.assert_called_once()

    @patch('src.plots.plotter.DataParser')
    @patch('src.plots.plotter.plt.show')
    def test_plot_tachometer_speed(self, plt_show_mock, data_parser_mock):
        data_parser_mock.return_value.parse_xlsx.return_value = ([1, 2, 3], [4, 5, 6])
        plotter = Plotter(self.logger_mock)
        plotter.plot_tachometer_speed()

        plt_show_mock.assert_called_once()
