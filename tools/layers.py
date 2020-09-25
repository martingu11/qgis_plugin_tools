import enum

__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from typing import Set

from qgis.core import QgsWkbTypes, QgsVectorLayer

POINT_TYPES = {
    QgsWkbTypes.Point, QgsWkbTypes.PointGeometry, QgsWkbTypes.PointM,
    QgsWkbTypes.Point25D, QgsWkbTypes.PointZ, QgsWkbTypes.PointZM,
    QgsWkbTypes.MultiPoint, QgsWkbTypes.MultiPoint25D, QgsWkbTypes.MultiPointM,
    QgsWkbTypes.MultiPointZ, QgsWkbTypes.MultiPointZM,
}

LINE_TYPES = {
    QgsWkbTypes.LineGeometry, QgsWkbTypes.LineString, QgsWkbTypes.LineString25D, QgsWkbTypes.LineStringM,
    QgsWkbTypes.LineStringZ, QgsWkbTypes.LineStringZM, QgsWkbTypes.MultiLineString,
    QgsWkbTypes.MultiLineString25D, QgsWkbTypes.MultiLineStringM, QgsWkbTypes.MultiLineStringZ,
    QgsWkbTypes.MultiLineStringZM
}

POLYGON_TYPES = {
    QgsWkbTypes.Polygon, QgsWkbTypes.Polygon25D, QgsWkbTypes.PolygonGeometry, QgsWkbTypes.PolygonM,
    QgsWkbTypes.PolygonZ, QgsWkbTypes.PolygonZM, QgsWkbTypes.MultiPolygon, QgsWkbTypes.CurvePolygon
}


@enum.unique
class LayerType(enum.Enum):
    Point = {'wkb_types': POINT_TYPES}
    Line = {'wkb_types': LINE_TYPES}
    Polygon = {'wkb_types': POLYGON_TYPES}

    @staticmethod
    def from_layer(layer: QgsVectorLayer) -> 'LayerType':
        for l_type in LayerType:
            if layer.geometryType() in l_type.wkb_types:
                return l_type

    @property
    def wkb_types(self) -> Set[QgsWkbTypes.GeometryType]:
        return self.value['wkb_types']
