__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 2"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import logging

from .custom_logging import bar_msg
from .exceptions import QgsPluginException
from .i18n import tr
from .resources import plugin_name

LOGGER = logging.getLogger(plugin_name())


def log_if_fails(fn):
    """
    Use this as a decorator with class methods that might throw uncaught exceptions
    """
    from functools import wraps

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except QgsPluginException as e:
            LOGGER.exception(str(e), extra=e.bar_msg)
        except Exception as e:
            LOGGER.exception(tr('Unhandled exception occurred'), extra=bar_msg(e))

    return wrapper
