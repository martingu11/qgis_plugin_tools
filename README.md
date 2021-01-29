# QGIS Plugin tools
![](https://github.com/GispoCoding/qgis_plugin_tools/workflows/Tests/badge.svg)


**Warning: The API is not stable yet. Function and files may move between commits.**

As it's a submodule, you can configure your GIT to auto update the submodule commit by running:

`git config --global submodule.recurse true`

The module is helping you with:
* [creating plugin from scratch](./README.md#For-new-plugin)
* [setting up some logging](docs/usage.md#Logging) (QgsMessageLog, file log, remote logs...)
* [fetching resources](docs/usage.md#Resource-tools) in `resources` or other folders
* [fetching compiled UI file](docs/usage.md#Resource-tools) in `resources/ui` folder
* fetching compiled translation file in `resources/i18n` folder
* removing QRC resources file easily
* translate using the `i18n.tr()` function.
* managing the release process : zip, upload on plugins.qgis.org, tag, GitHub release
* providing some common widgets/code for plugins
* [setting up a debug server](docs/usage.md#Debug-server)

## How to install it

### For new plugin
This will create needed structure for your plugin

1. Create new repository in Github (here using: https://github.com/GispoCoding/test-plugin-name)
2. Follow these steps
    ```shell script
    mkdir test-plugin-name
    cd test-plugin-name
    git init
    git remote add origin git@github.com:GispoCoding/test-plugin-name
    mkdir TestPlugin
    cd TestPlugin
    git submodule add https://github.com/GispoCoding/qgis_plugin_tools
    cp qgis_plugin_tools/infrastructure/creator.py .
    python creator.py -o GispoCoding -r test-plugin-name # Replace with your information
    rm creator.py
    ```
3. Now edit metadata.txt with description etc. and commit changes.

### For existing plugin
1. Go to the root folder of your plugin code source
2. `git submodule add https://github.com/GispoCoding/qgis_plugin_tools.git`


## How to use it

Refer to [usage](docs/usage.md) documentation.


## Plugin tree example

The plugin should follow the following file tree to get most out of this module.

Plugin `Foo` root folder:
* `plugin_repo` # **no '-' character!**
    * **`.gitmodules`**
    * `.gitattributes`
    * `.gitignore`
    * `.qgis-plugin-ci` # to use [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci)
        * `plugin_name` # **no '-' character!**
            * `.gitignore`
          * `qgis_plugins_tools/` # submodule
          * **`resources/`**
            * `i18n/` # Alternatively translations could use [Transifex](infrastructure/template/root/docs/development.md#Translating)
              * `fi.ts`
              * `fi.qm`
            * `ui/`
              * `main_dialog.ui`
            * `icons/`
              * `my_icon.svg`
          * `test/`
          * `__init__.py`
          * `foo.py`
          * `metadata.txt`
          * `build.py`
