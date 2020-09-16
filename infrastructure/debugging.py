__copyright__ = "Copyright 2020, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"


def setup_pydevd(host: str = 'localhost', port: int = 5678) -> bool:
    """
    Setup pydevd degugging service

    Here is a sample (GlobeBuilder) Intellij Idea / PyCharm configuration for setting up the debug server in workspace.xml:

    <configuration name="Debug Server" type="PyRemoteDebugConfigurationType" factoryName="Python Remote Debug">
      <module name="QGIS Debug Server" />
      <option name="PORT" value="5678" />
      <option name="HOST" value="localhost" />
      <PathMappingSettings>
        <option name="pathMappings">
          <list>
            <mapping local-root="$PROJECT_DIR$/GlobeBuilder" remote-root="/home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/GlobeBuilder" />
          </list>
        </option>
      </PathMappingSettings>
      <option name="REDIRECT_OUTPUT" value="true" />
      <option name="SUSPEND_AFTER_CONNECT" value="true" />
      <method v="2" />
    </configuration>

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    try:
        import pydevd

        pydevd.settrace(host, port=port, stdoutToServer=True, stderrToServer=True)
        succeeded = True
    except Exception as e:
        print('Unable to create pydevd debugger: {}'.format(e))

    return succeeded


def setup_debugpy(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup debugpy degugging service

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    try:
        import debugpy
        debugpy.listen((host, port))
        succeeded = True
    except Exception as e:
        print('Unable to create debugpy debugger: {}'.format(e))
    return succeeded
