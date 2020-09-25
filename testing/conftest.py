__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import pytest

from .utilities import get_qgis_app
from ..tools.custom_logging import setup_logger
from ..tools.resources import plugin_name

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()


@pytest.fixture
def new_project() -> None:
    """
    Initializes new iface project.
    Some of PyQGIS functionality does not work without this
    """
    yield IFACE.newProject()


@pytest.fixture(scope='session')
def initialize_logger():
    setup_logger(plugin_name(), IFACE)
