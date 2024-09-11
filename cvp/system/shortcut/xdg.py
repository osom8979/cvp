# -*- coding: utf-8 -*-

_CONTENT = """
#!/usr/bin/env xdg-open

[Desktop Entry]
Version=1.0

Type=Application
Categories=Development;Video;Utility;
Keywords=OpenCV;
Name=cvp
Name[ko]=cvp
GenericName=Computer Vision Player
GenericName[ko]=Computer Vision Player
Comment=Computer Vision Player
Comment[ko]=Computer Vision Player

TryExec=%HOME%/.cvp.app/run
Exec=%HOME%/.cvp.app/run
Path=%HOME%/.cvp.app
Icon=%HOME%/.cvp.app/icon.svg
MimeType=application/yaml

Terminal=false
Hidden=false
NoDisplay=false

StartupNotify=true
# StartupWMClass=cvp

X-LXQt-Need-Tray=true
X-GNOME-Autostart-enabled=true
"""
