__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import datetime
from pathlib import Path

import pytest
from qgis.core import QgsSingleBandGrayRenderer, QgsRasterLayer, QgsDateTimeRange

from ..tools.network import download_to_file
from ..tools.raster_layers import set_raster_renderer_to_singleband, set_band_based_on_range, set_fixed_temporal_range


@pytest.fixture
def netcdf_layer(tmpdir) -> QgsRasterLayer:
    path = download_to_file(
        'https://raw.githubusercontent.com/GispoCoding/FMI2QGIS/master/FMI2QGIS/test/data/aq_small.nc', tmpdir)
    return QgsRasterLayer(str(path))


@pytest.fixture
def t_range() -> QgsDateTimeRange:
    return QgsDateTimeRange(datetime.datetime(2020, 11, 2, 15, 0), datetime.datetime(2020, 11, 3, 11, 0))


@pytest.fixture
def configured_layer(netcdf_layer, t_range) -> QgsRasterLayer:
    set_raster_renderer_to_singleband(netcdf_layer)
    set_fixed_temporal_range(netcdf_layer, t_range)
    return netcdf_layer


def test_set_raster_renderer_to_singleband(netcdf_layer):
    set_raster_renderer_to_singleband(netcdf_layer)
    assert isinstance(netcdf_layer.renderer(), QgsSingleBandGrayRenderer)


def test_set_fixed_temporal_range(netcdf_layer, t_range):
    set_fixed_temporal_range(netcdf_layer, t_range)
    tprops = netcdf_layer.temporalProperties()
    assert tprops.isActive()
    assert tprops.fixedTemporalRange() == t_range


def test_set_fixed_temporal_range(configured_layer):
    t_range2 = QgsDateTimeRange(datetime.datetime(2020, 11, 2, 15, 0), datetime.datetime(2020, 11, 2, 16, 0))
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 1


def test_set_fixed_temporal_range2(configured_layer):
    t_range2 = QgsDateTimeRange(datetime.datetime(2020, 11, 2, 17, 0), datetime.datetime(2020, 11, 2, 18, 0))
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 3


def test_set_fixed_temporal_range3(configured_layer):
    t_range2 = QgsDateTimeRange(datetime.datetime(2020, 11, 2, 18, 0), datetime.datetime(2020, 11, 2, 22, 0))
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 4


def test_set_fixed_temporal_range4(configured_layer):
    t_range2 = QgsDateTimeRange(datetime.datetime(2020, 11, 3, 10, 0), datetime.datetime(2020, 11, 3, 11, 0))
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 20
