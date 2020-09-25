__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from ..tools.settings import set_setting, get_setting


def test_set_setting(new_project):
    set_setting('test_setting', 'test_value')
    assert get_setting('test_setting') == 'test_value'


def test_get_setting(new_project):
    assert get_setting('non-existent', 2, int) == 2


def test_get_setting2(new_project):
    assert get_setting('non-existent', 2, str) == '2'


def test_get_setting3(new_project):
    assert get_setting('non-existent', 2, bool) is True
