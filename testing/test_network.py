__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import pytest

from ..tools.exceptions import QgsPluginNetworkException
from ..tools.network import fetch, download_to_file


def test_fetch(new_project):
    data_model = fetch('https://www.gispo.fi/')
    assert len(data_model) > 10000


def test_fetch_invalid_url(new_project):
    with pytest.raises(QgsPluginNetworkException):
        fetch('invalidurl')


def test_download_to_file(new_project, tmpdir):
    path_to_file = download_to_file('https://twitter.com/gispofinland/status/1324599933337567232/photo/1', tmpdir,
                                    'test_file')
    assert path_to_file.exists()


def test_download_to_file_without_requests(new_project, tmpdir):
    path_to_file = download_to_file('https://twitter.com/gispofinland/status/1324599933337567232/photo/1', tmpdir,
                                    'test_file', use_requests_if_available=False)
    assert path_to_file.exists()


def test_download_to_file_invalid_url(new_project, tmpdir):
    with pytest.raises(QgsPluginNetworkException):
        download_to_file('invalidurl', tmpdir)


def test_download_to_file_invalid_url_without_requests(new_project, tmpdir):
    with pytest.raises(QgsPluginNetworkException):
        download_to_file('invalidurl', tmpdir)
