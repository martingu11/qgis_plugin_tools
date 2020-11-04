import logging
from typing import Tuple

from PyQt5.QtCore import QSettings, QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply
from qgis.core import Qgis, QgsBlockingNetworkRequest, QgsNetworkReplyContent

from .custom_logging import bar_msg
from ..tools.exceptions import QgsPluginNetworkException
from ..tools.i18n import tr
from ..tools.resources import plugin_name

__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

LOGGER = logging.getLogger(plugin_name())
ENCODING = "utf-8"
CONTENT_DISPOSITION = QByteArray(bytes("Content-Disposition", ENCODING))


def fetch(url: str, encoding: str = ENCODING) -> str:
    """
    Fetch resource from the internet. Similar to requests.get(url) but is
    recommended way of handling requests in QGIS plugin
    :param url: address of the web resource
    :return: encoded string of the content
    """
    content, _ = fetch_raw(url, encoding)
    return content.decode(ENCODING)


def fetch_raw(url, encoding: str = ENCODING) -> Tuple[bytes, str]:
    """
    Fetch resource from the internet. Similar to requests.get(url) but is
    recommended way of handling requests in QGIS plugin
    :param url: address of the web resource
    :return: bytes of the content and default name of the file or empty string
    """
    LOGGER.debug(url)
    req = QNetworkRequest(QUrl(url))
    # http://osgeo-org.1560.x6.nabble.com/QGIS-Developer-Do-we-have-a-User-Agent-string-for-QGIS-td5360740.html
    user_agent = QSettings().value("/qgis/networkAndProxy/userAgent", "Mozilla/5.0")
    user_agent += " " if len(user_agent) else ""
    # noinspection PyUnresolvedReferences
    user_agent += f"QGIS/{Qgis.QGIS_VERSION_INT}"
    user_agent += f" {plugin_name()}"
    # https://www.riverbankcomputing.com/pipermail/pyqt/2016-May/037514.html
    req.setRawHeader(b"User-Agent", bytes(user_agent, encoding))
    request_blocking = QgsBlockingNetworkRequest()
    _ = request_blocking.get(req)
    reply: QgsNetworkReplyContent = request_blocking.reply()
    reply_error = reply.error()
    if reply_error != QNetworkReply.NoError:
        raise QgsPluginNetworkException(tr('Request failed'), bar_msg=bar_msg(reply.errorString()))

    # https://stackoverflow.com/a/39103880/10068922
    default_name = ''
    if reply.hasRawHeader(CONTENT_DISPOSITION):
        header: QByteArray = reply.rawHeader(CONTENT_DISPOSITION)
        default_name = bytes(header).decode(encoding).split('filename=')[1]
        if default_name[0] in ['"', "'"]:
            default_name = default_name[1:-1]

    return bytes(reply.content()), default_name
