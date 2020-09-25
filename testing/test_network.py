__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import pytest

from ..tools.exceptions import QgsPluginNetworkException
from ..tools.network import fetch


def test_fetch(new_project):
    data_model = fetch('https://www.gispo.fi/')
    assert len(data_model) > 10000


def test_fetch_invalid_url(new_project):
    with pytest.raises(QgsPluginNetworkException):
        fetch('invalidurl')
