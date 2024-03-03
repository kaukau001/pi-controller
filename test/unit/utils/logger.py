import unittest
import logging

from src.utils.logger import AppLogger


class TestAppLogger(unittest.TestCase):

    def setUp(self):
        self.logger = AppLogger.get_instance()
        self.log_buffer = self.logger.get_log_buffer()

    def test_logger_instance(self):
        self.assertIsInstance(self.logger, AppLogger)

    def test_logger_level(self):
        self.assertEqual(self.logger.logger.level, logging.INFO)

    def test_debug_log(self):
        self.logger.logger.setLevel(logging.DEBUG)
        self.logger.debug("Debug message")
        self.assertTrue("DEBUG" in self.log_buffer.getvalue())

    def test_info_log(self):
        self.logger.logger.setLevel(logging.INFO)
        self.logger.info("Info message")
        self.assertTrue("INFO" in self.log_buffer.getvalue())

    def test_warning_log(self):
        self.logger.logger.setLevel(logging.WARNING)
        self.logger.warning("Warning message")
        self.assertTrue("WARNING" in self.log_buffer.getvalue())

    def test_error_log(self):
        self.logger.logger.setLevel(logging.ERROR)
        self.logger.error("Error message")
        self.assertTrue("ERROR" in self.log_buffer.getvalue())

    def test_critical_log(self):
        self.logger.logger.setLevel(logging.CRITICAL)
        self.logger.critical("Critical message")
        self.assertTrue("CRITICAL" in self.log_buffer.getvalue())

    def test_log_format(self):
        self.logger.error("Test error message")
        log_output = self.log_buffer.getvalue()
        self.assertTrue(
            "- ERROR - Test error message" in log_output)