# Setting up Transifex translations with qgis_plugin_tools

This document describes how to setup and configure translations on Transifex with qgis_plugin_tools.

## Prerequisites

Read [this](https://github.com/GispoCoding/qgis_plugin_tools/blob/master/infrastructure/template/root/docs/development.md#Translating) for more condensed info and resources on translation.

First, install Transifex CLI, qgis-plugin-ci, and check pylupdate5 is in path (works on command line).
See above link for links/installation information.

Create a public repository on GitHub for your translation test project.

Setup a new test plugin with qgis_plugin tools according to [this](https://github.com/GispoCoding/qgis_plugin_tools#for-new-plugin). 

Add some `print(tr('Translate this text'))` statements inside the `plugin.Plugin.__init__` method.
Commit your changes, and push your code to the GitHub repository.

Create a Transifex account and a new organization, generate a token/key from Transifex settings.
No need to create a new project, it will be generated automatically.

Open the settings of your GitHub repository, go to Secrets and add a new *Repository secret*
(**not** environment secret) called TRANSIFEX_TOKEN and give it the value of your Transifex key.


## Configuration

After doing the setup, edit the .qgis_plugin_ci in your plugin (generated by qgis_plugin_tools creator.py).

Change github_organization to your GitHub username, project_slug to your GitHub repository name, transifex_coordinator
to your Transifex username, and transifex_organization to your Transifex organization name. 

**Note**: If you have issues with pushing to Transifex, verify the organization name by logging in to transifex.com,
open your organization and check the URL. I created an organization called test but the actual name is test-1245!

Finally, verify the repository value in metadata.txt points to your GitHub repository. Also check the homepage and tracker
values here.

## Pushing and pulling

Now you can push translations to Transifex by running the command `qgis-plugin-ci push-translation <transifex_token>`.

After pushing the translations, go to Transifex and open the newly generated project. First add a new language to
translate from the languages tab, and then click on Translate to start translating.

After doing some translations, pull the translations by running the command
`qgis-plugin-ci pull-translation --compile <transifex_token>`.

You should now have some .qm and .ts files in your PluginName/i18n directory.

## Deploying and testing

### Manual

To see your new translations in action, edit the build.py script and add 'i18n' to the extra_dirs list.
Also, check the suffix of the files in the i18n directory. Add the locale id to the list of locales in build.py,
e.g. if there's a PluginName_fi.ts file then add 'fi' to the list of locales in build.py.

Next, deploy the plugin to QGIS by running python build.py deploy. Now open QGIS and verify you have the same profile
as defined in build.py. Enable the plugin from the QGIS plugins menu, and open the QGIS Python console.

Click on Plugins -> PluginName from the menu. You should see your print statements in the Python console. Next, open
QGIS settings and change the language to the locale that you have created translations for.

Restart QGIS, open QGIS Python console and open the plugin. The print statements should now be translated.

### Automatic

Move push_translations.yml from the docs folder to the .github/workflows directory.

Edit release.yml from .github/workflows and add `--transifex-token ${{ secrets.TRANSIFEX_TOKEN }}` to the last line of
code. Also uncomment the two lines below "Needed if the plugin is using Transifex".

Translations are now pushed to Transifex whenever you push code to the master branch. Translations are automatically
pulled and compiled from Transifex when creating a release. For instructions on creating a release, read
[here](https://github.com/GispoCoding/qgis_plugin_tools/blob/master/infrastructure/template/root/docs/development.md#creating-a-release).
After creating a release on GitHub (open tags, then the releases tab and create a new release) the release workflow
will run and automatically add a .zip file to the release. Download the zip, install it from the QGIS plugins menu
(under the install from zip-tab) and test that the translations are working.
