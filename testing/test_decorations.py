__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from qgis.core import Qgis

from .conftest import IFACE
from ..tools.custom_logging import bar_msg
from ..tools.decorations import log_if_fails
from ..tools.exceptions import QgsPluginNotImplementedException


class MockClass:

    @log_if_fails
    def method_that_fails(self):
        raise ValueError('Error message')

    @log_if_fails
    def method_that_shows_msg(self):
        raise QgsPluginNotImplementedException('Error message', bar_msg('Please implement'))


def test_logging_if_fails(initialize_logger):
    MockClass().method_that_shows_msg()

    messages = IFACE.messageBar().get_messages(Qgis.Critical)
    assert 'Error message:Please implement' in messages


def test_logging_if_fails_without_details(initialize_logger):
    MockClass().method_that_fails()

    messages = IFACE.messageBar().get_messages(Qgis.Critical)
    assert 'Unhandled exception occurred:Error message' in messages
