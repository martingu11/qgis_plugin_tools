# coding=utf-8
"""Common functionality used by regression tests."""

import logging
import os
import sys

from osgeo import gdal
from qgis.PyQt import Qt
from qgis.core import Qgis

from .mock_qgis_classes import MockMessageBar, MainWindow

LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
PARENT = None
IFACE = None


def pytest_report_header(config):
    """Used by PyTest and Unittest."""
    # noinspection PyUnresolvedReferences
    message = "QGIS : {}\n".format(Qgis.QGIS_VERSION_INT)
    message += "Python GDAL : {}\n".format(gdal.VersionInfo("VERSION_NUM"))
    message += "Python : {}\n".format(sys.version)
    # message += 'Python path : {}'.format(sys.path)
    message += "QT : {}".format(Qt.QT_VERSION_STR)
    return message


def get_qgis_app():
    """ Start one QGIS application to test against.

    :returns: Handle to QGIS app, canvas, new_project and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)

    If QGIS is already running the handle to that app will be returned.
    """

    try:
        from PyQt5 import QtCore, QtWidgets
        from qgis.core import QgsApplication
        from qgis.gui import QgsMapCanvas
        from .qgis_interface import QgisInterface
    except ImportError:
        return None, None, None, None

    global QGIS_APP  # pylint: disable=W0603

    if QGIS_APP is None:
        gui_flag = True  # All test will run qgis in gui mode
        # noinspection PyPep8Naming
        QGIS_APP = QgsApplication([bytes(arg, 'utf-8') for arg in sys.argv],
                                  gui_flag)
        # Make sure QGIS_PREFIX_PATH is set in your env if needed!
        QGIS_APP.initQgis()
        s = QGIS_APP.showSettings()
        LOGGER.debug(s)

    global PARENT  # pylint: disable=W0603
    if PARENT is None:
        # noinspection PyPep8Naming
        PARENT = QtWidgets.QWidget()

    global CANVAS  # pylint: disable=W0603
    if CANVAS is None:
        # noinspection PyPep8Naming
        CANVAS = QgsMapCanvas(PARENT)
        CANVAS.resize(QtCore.QSize(400, 400))

    global IFACE  # pylint: disable=W0603
    if IFACE is None:
        # QgisInterface is a stub implementation of the QGIS plugin interface
        # noinspection PyPep8Naming
        IFACE = QgisInterface(CANVAS, MockMessageBar(), MainWindow())

    # print(pytest_report_header(None))
    return QGIS_APP, CANVAS, IFACE, PARENT


def is_running_inside_ci() -> bool:
    """Tells whether the plugin is running in CI environment"""
    return int(os.environ.get("QGIS_PLUGIN_IN_CI", "0")) == 1


def is_running_in_tools_module_ci() -> bool:
    return is_running_inside_ci() and int(os.environ.get("QGIS_PLUGIN_TOOLS_IN_CI", "0")) == 1


def qgis_supports_temporal() -> bool:
    try:
        from qgis.core import QgsRasterLayerTemporalProperties
        return True
    except ImportError:
        return False
