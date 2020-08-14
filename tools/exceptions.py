__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 2"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"


class QgsPluginException(Exception):
    """ Use this as a base exception class in custom exceptions """


class QgsPluginNetworkException(QgsPluginException):
    pass


class QgsPluginNotImplementedException(QgsPluginException):
    pass
