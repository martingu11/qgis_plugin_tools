"""Setting up logging using QGIS, file, Sentry..."""

import logging
from enum import Enum, unique
from logging.handlers import RotatingFileHandler
from typing import Optional, Any, Dict

from PyQt5.QtCore import QSettings
from qgis.core import QgsMessageLog, Qgis
from qgis.gui import QgisInterface

from .i18n import tr
from .resources import plugin_name, plugin_path
from .settings import setting_key

PLUGIN_NAME = plugin_name()

__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"


@unique
class LogTarget(Enum):
    """ Log target with default logging level as value """
    STREAM = {'id': 'stream', 'default': 'INFO'}
    FILE = {'id': 'file', 'default': 'INFO'}
    BAR = {'id': 'bar', 'default': 'INFO'}

    @property
    def id(self):
        return self.value['id']

    @property
    def default_level(self):
        return self.value['default']


def qgis_level(logging_level):
    """Check for the corresponding QGIS Level according to Logging Level.

    For QGIS:
    https://qgis.org/api/classQgis.html#a60c079f4d8b7c479498be3d42ec96257

    For Logging:
    https://docs.python.org/3/library/logging.html#levels

    :param logging_level: The Logging level
    :target logging_level: basestring

    :return: The QGIS Level
    :rtype: Qgis.MessageLevel
    """
    if logging_level == "CRITICAL":
        return Qgis.Critical
    elif logging_level == "ERROR":
        return Qgis.Critical
    elif logging_level == "WARNING":
        return Qgis.Warning
    elif logging_level == "INFO":
        return Qgis.Info
    elif logging_level == "DEBUG":
        return Qgis.Info

    return Qgis.Info


def bar_msg(details: Any = "", duration: Optional[int] = None, success: bool = False) -> Dict[str, str]:
    """
    Helper function to construct extra arguments for message bar logger message

    :param details: Longer body of the message. Can be set to empty string.
    :param duration: can be used to specify the message timeout in seconds. If ``duration``
        is set to 0, then the message must be manually dismissed by the user.
    :param success: Whether the message is success message or not
    """
    args = {'details': str(details), 'success': success}
    if duration is not None:
        args['duration'] = duration
    return args


class QgsLogHandler(logging.Handler):
    """A logging handler that will log messages to the QGIS logging console."""

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self)

    def emit(self, record):
        """Try to log the message to QGIS if available, otherwise do nothing.

        :param record: logging record containing whatever info needs to be
                logged.
        """
        try:
            # noinspection PyCallByClass,PyTypeChecker
            QgsMessageLog.logMessage(
                record.getMessage(), PLUGIN_NAME, qgis_level(record.levelname)
            )
        except MemoryError:
            message = tr(
                "Due to memory limitations on this machine, the plugin {} can not "
                "handle the full log"
            ).format(PLUGIN_NAME)
            # print(message)
            # noinspection PyCallByClass,PyTypeChecker
            QgsMessageLog.logMessage(message, PLUGIN_NAME, Qgis.Critical)


class QgsMessageBarFilter(logging.Filter):
    """
    A logging filter to decide whether the message should be passed and
    to QgsMessageBarHandler as enriched

    Description of keys:
        details: Longer body of the message. Can be set to empty string.
        duration: can be used to specify the message timeout in seconds. If ``duration``
            is set to 0, then the message must be manually dismissed by the user.
        success: boolean, defaults to False. Whether the message is success message or not
    """

    def filter(self, record: logging.LogRecord):
        args = record.__dict__
        if "details" not in args:
            return False

        record.qgis_level = qgis_level(record.levelname) if not args.get("success", False) else Qgis.Success
        record.duration = args.get("duration", self.bar_msg_duration(record.levelname))
        return True

    @staticmethod
    def bar_msg_duration(logging_level: str) -> int:
        """Check default duration for messages in message bar based on level.

        :param logging_level: The Logging level
        :return: duration in seconds
        """
        if logging_level == "CRITICAL":
            return 12
        elif logging_level == "ERROR":
            return 10
        elif logging_level == "WARNING":
            return 6
        elif logging_level == "INFO":
            return 4
        elif logging_level == "DEBUG":
            return 4

        return 4


class QgsMessageBarHandler(logging.Handler):
    """A logging handler that will log messages to the QGIS message bar."""

    def __init__(self, iface: Optional[QgisInterface]):
        self.iface = iface
        logging.Handler.__init__(self)

    def emit(self, record: logging.LogRecord):
        """
        Push info message to the QGIS message bar. Pass "extra" kwarg to logger to use with
        mandatory "details" key.

        :param record: logging record enriched with extra information from QgsMessageBarFilter
        """
        try:
            # noinspection PyUnresolvedReferences
            if self.iface is not None:
                self.iface.messageBar().pushMessage(title=record.message,
                                                    text=record.details,
                                                    level=record.qgis_level,
                                                    duration=record.duration)
            else:
                from qgis.utils import iface
                iface.messageBar().pushMessage(title=record.message,
                                               text=record.details,
                                               level=record.qgis_level,
                                               duration=record.duration)
        except MemoryError:
            pass  # This is handled in QgsLogHandler


def add_logging_handler_once(logger, handler) -> bool:
    """A helper to add a handler to a logger, ensuring there are no duplicates.

    :param logger: Logger that should have a handler added.
    :type logger: logging.logger

    :param handler: Handler instance to be added. It will not be added if an
        instance of that Handler subclass already exists.
    :type handler: logging.Handler

    :returns: True if the logging handler was added, otherwise False.
    :rtype: bool
    """
    class_name = handler.__class__.__name__
    for logger_handler in logger.handlers:
        if logger_handler.__class__.__name__ == class_name:
            return False

    logger.addHandler(handler)
    return True


def get_log_level_key(target: LogTarget) -> str:
    """Finds QSetting key for log level """
    return setting_key("log_level", target.id)


def get_log_level_name(target: LogTarget) -> str:
    """Finds the log level name of the target """
    return QSettings().value(get_log_level_key(target), target.default_level, str)


def get_log_level(target: LogTarget) -> int:
    """Finds log level of the target """
    return logging.getLevelName(get_log_level_name(target))


def setup_logger(logger_name: str, iface: Optional[QgisInterface] = None) -> logging.Logger:
    """Run once when the module is loaded and enable logging.

    :param logger_name: The logger name that we want to set up.
    :param iface: QGIS Interface. Add this to enable message bar support

    Borrowed heavily from this:
    http://docs.python.org/howto/logging-cookbook.html

    Now to log a message do::
       LOGGER.debug('Some debug message')

    And to a message bar::
       LOGGER.info('Some bar message', extra={'details': 'details'})
       LOGGER.info('Some bar message', extra=bar_msg('details')) # With helper function
    """

    stream_level = get_log_level(LogTarget.STREAM)
    file_level = get_log_level(LogTarget.FILE)
    bar_level = get_log_level(LogTarget.BAR)

    logger = logging.getLogger(logger_name)
    logger.setLevel(min(stream_level, file_level))

    if logger_name != 'test_plugin':
        file_formatter = logging.Formatter("%(asctime)s - [%(levelname)-7s] - %(filename)s:%(lineno)d : %(message)s",
                                           "%d.%m.%Y %H:%M:%S")
        file_handler = RotatingFileHandler(plugin_path("logs", f"{logger_name}.log"), maxBytes=1024 * 1024 * 2)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(file_level)
        add_logging_handler_once(logger, file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(stream_level)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d.%m.%Y %H:%M:%S")
    console_handler.setFormatter(console_formatter)
    add_logging_handler_once(logger, console_handler)

    qgis_handler = QgsLogHandler()
    qgis_formatter = logging.Formatter("[%(levelname)-7s]- %(message)s")
    qgis_handler.setFormatter(qgis_formatter)
    add_logging_handler_once(logger, qgis_handler)

    if iface is None:
        try:
            from qgis.utils import iface
        except ImportError:
            iface = None

    if iface is not None:
        qgis_msg_bar_handler = QgsMessageBarHandler(iface)
        qgis_msg_bar_handler.addFilter(QgsMessageBarFilter())
        qgis_msg_bar_handler.setLevel(bar_level)
        add_logging_handler_once(logger, qgis_msg_bar_handler)

    return logger


def setup_task_logger(logger_name: str) -> logging.Logger:
    """ Run once when the module is loaded and enable logging during tasks.

    :param logger_name: The logger name that we want to set up.
    """

    stream_level = get_log_level(LogTarget.STREAM)
    logger = logging.getLogger(f"{logger_name}_task")
    logger.setLevel(stream_level)
    logger.handlers = []

    qgis_handler = QgsLogHandler()
    qgis_formatter = logging.Formatter("[%(levelname)-7s]- %(message)s")
    qgis_handler.setFormatter(qgis_formatter)
    add_logging_handler_once(logger, qgis_handler)

    return logger
