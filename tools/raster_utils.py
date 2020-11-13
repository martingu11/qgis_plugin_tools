__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from qgis.core import (QgsRasterLayer, QgsRasterDataProvider, QgsSingleBandGrayRenderer, QgsRasterBandStats,
                       QgsContrastEnhancement)


def set_raster_renderer_to_singleband(layer: QgsRasterLayer, band: int = 1) -> None:
    """
    Set raster renderer to singleband
    :param layer: raster layer
    """
    # https://gis.stackexchange.com/a/377631/123927 and https://gis.stackexchange.com/a/157573/123927
    provider: QgsRasterDataProvider = layer.dataProvider()
    renderer: QgsSingleBandGrayRenderer = QgsSingleBandGrayRenderer(layer.dataProvider(), band)

    stats: QgsRasterBandStats = provider.bandStatistics(band, QgsRasterBandStats.All, layer.extent(), 0)
    min_val = max(stats.minimumValue, 0)
    max_val = max(stats.maximumValue, 0)

    enhancement = QgsContrastEnhancement(renderer.dataType(band))
    contrast_enhancement = QgsContrastEnhancement.StretchToMinimumMaximum
    enhancement.setContrastEnhancementAlgorithm(contrast_enhancement, True)
    enhancement.setMinimumValue(min_val)
    enhancement.setMaximumValue(max_val)
    layer.setRenderer(renderer)
    layer.renderer().setContrastEnhancement(enhancement)
    layer.triggerRepaint()
