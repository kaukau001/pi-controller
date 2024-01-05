import logging
from io import StringIO


class AppLogger:
    _instance = None

    @classmethod
    def get_instance(cls, logger_name=__name__, log_level=logging.INFO):
        if not cls._instance:
            cls._instance = cls(logger_name, log_level)
        return cls._instance

    def __new__(cls, logger_name=__name__, log_level=logging.INFO):
        if not cls._instance:
            cls._instance = super(AppLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(logger_name)
            cls._instance.logger.setLevel(log_level)
            cls._instance.log_buffer = StringIO()
            console_handler = logging.StreamHandler(cls._instance.log_buffer)
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            cls._instance.logger.addHandler(console_handler)
        return cls._instance

    def get_logger(self):
        return self._instance.logger

    def debug(self, msg, *args, **kwargs):
        self._instance.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._instance.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._instance.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._instance.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._instance.logger.critical(msg, *args, **kwargs)

    def get_log_buffer(self):
        return self._instance.log_buffer
