class QgsPluginException(Exception):
    """ Use this as a base exception class in custom exceptions """


class QgsPluginNetworkException(QgsPluginException):
    pass


class QgsPluginNotImplementedException(QgsPluginException):
    pass
