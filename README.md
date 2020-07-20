## QGIS Plugin core tools

## The API is not stable yet. Function and files may move between commits.

As it's a submodule, you can configure your GIT to auto update the submodule commit by running:

`git config --global submodule.recurse true`

### How to use it

The module is helping you with:
* setting up some logging (QgsMessageLog, file log, remote logs...)
* fetching resources in `resources` folder
* fetching compiled UI file in `resources/ui` folder
* fetching compiled translation file in `resources/i18n` folder
* removing QRC resources file easily
* translate using the `i18n.tr()` function.
* launching tests on Travis
* managing the release process : zip, upload on plugins.qgis.org, tag, GitHub release
* running pylint checks
* providing some common widgets/code for plugins

### How to install it

* Go to the root folder of your plugin code source
* `git submodule add https://github.com/GispoCoding/qgis_plugin_tools.git`

### How to use it

For setting up the logging (usually in main plugin file):
```python
from .qgis_plugin_tools.tools.resources import plugin_name
from .qgis_plugin_tools.tools.custom_logging import setup_logger

# Setup without message bar support
# setup_logger(plugin_name())

# Setup with QGIS interface to add message bar support
setup_logger(plugin_name(), iface)
```

To use the logging system:
```python
import logging
from .qgis_plugin_tools.tools.resources import plugin_name
from .qgis_plugin_tools.tools.custom_logging import bar_msg

# Top of the file
LOGGER = logging.getLogger(plugin_name())

# Later in the code
LOGGER.debug('Log some debug messages')
LOGGER.info('Log some info here')
LOGGER.warning('Log a warning here')
LOGGER.error('Log an error here')
LOGGER.critical('Log a critical error here')

# These are logged to the message bar in addition to normal logging
LOGGER.info('Msg bar message', extra=bar_msg("some details here"))
LOGGER.info('Msg bar message', extra=bar_msg("some details here", success=True))
LOGGER.warning('Msg bar message', extra={'details:': "some details here"})
LOGGER.error('Msg bar message', extra=bar_msg("some details here", duration=10))
```

For setting up the translation file:
```python
from qgis.PyQt.QtCore import QCoreApplication, QTranslator

from .qgis_plugin_tools.tools.i18n import setup_translation

locale, file_path = setup_translation()
if file_path:
    self.translator = QTranslator()
    self.translator.load(file_path)
    QCoreApplication.installTranslator(self.translator)

```

* Using the plugin upload function, check the `--help` of the `plugin_upload.py` file.
For instance, you can setup environment variable in your bash for your credentials.

## Plugin tree example

Plugin `Foo` root folder:
* `.docker`
* `plugin_name`
  * `qgis_plugins_tools/` submodule
  * `resources/`
    * `i18n/`
      * `fr.ts`
      * `fr.qm`
    * `ui/`
      * `main_dialog.ui`
    * `icons/`
      * `my_icon.svg`
  * `test/`
  * `__init__.py`
  * `foo.py`
  * `metadata.txt`
* `.gitattributes
* `.gitmodules`
* `.gitignore`
* `Makefile`
