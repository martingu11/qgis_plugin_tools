## QGIS Plugin core tools

## The API is not stable yet. Function and files may move between commits.

As it's a submodule, you can configure your GIT to auto update the submodule commit by running:

`git config --global submodule.recurse true`

### How to use it

The module is helping you with:
* creating plugin from scratch
* setting up some logging (QgsMessageLog, file log, remote logs...)
* fetching resources in `resources` folder
* fetching compiled UI file in `resources/ui` folder
* fetching compiled translation file in `resources/i18n` folder
* removing QRC resources file easily
* translate using the `i18n.tr()` function.
* managing the release process : zip, upload on plugins.qgis.org, tag, GitHub release
* running pylint checks
* providing some common widgets/code for plugins
* setting up a debug server

### How to install it

#### To existing plugin
* Go to the root folder of your plugin code source
* `git submodule add https://github.com/GispoCoding/qgis_plugin_tools.git`

#### To new plugin

This will create needed structure for your plugin
```
git init
mkdir TestPlugin
cd TestPlugin
git submodule add https://github.com/GispoCoding/qgis_plugin_tools
cp qgis_plugin_tools/infrastructure/creator.py .
python creator.py -o githubOrganization -r repositoryProjectName
rm creator.py
```

Now edit metadata.txt with description etc. and commit changes.

### How to use it

#### Logging

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

### Translating
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

### Debug server
Plugin can connect to already running debug server with following code in the plugin's `__init__.py` file.

```python
from .qgis_plugin_tools.infrastructure.debugging import setup_pydevd

# It is a good idea to set up an environment variable to control this. Like:
# if os.environ.get('QGIS_PLUGIN_DEBUGGER') == 'pydevd':
setup_pydevd()
```

### Using PluginMaker
There is a script [plugin_maker.py](infrastructure/plugin_maker.py), which can
be used to replace Makefile and pb_tool in plugin build, deployment, translation and packaging processes.
To use it, create a python script (eg. build.py) in the root of the plugin and
populate it like following:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob

from qgis_plugin_tools.infrastructure.plugin_maker import PluginMaker

'''
#################################################
# Edit the following to match the plugin
#################################################
'''

locales = ['fi']
profile = 'foo'
py_files = [fil for fil in glob.glob("**/*.py", recursive=True) if "test/" not in fil]
ui_files = list(glob.glob("**/*.ui", recursive=True))
resources = list(glob.glob("**/*.qrc", recursive=True))
extra_dirs = ["resources", "logs"]
compiled_resources = ["resources.py"]


PluginMaker(py_files=py_files, ui_files=ui_files, resources=resources, extra_dirs=extra_dirs,
            compiled_resources=compiled_resources, locales=locales, profile=profile)
```
And use it like:
```shell script
python build.py -h # Show available commands
python build.py deploy
python build.py transup
# etc.
```


## Plugin tree example

Plugin `Foo` root folder:
* `plugin_name`
  * **`logs/`**
    * `.gitignore`
  * `qgis_plugins_tools/` submodule
  * **`resources/`**
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
* **`.gitattributes`**
* `.gitmodules`
* `.gitignore`
* `build.py`
