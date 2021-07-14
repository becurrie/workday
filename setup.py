from setuptools import (
    setup,
)

APP = ["src/workday.py"]
DATA_FILES = [
    "src/_AppIcon.png",
]
OPTIONS = {
    "iconfile": "src/_AppIcon.icns",
    "plist": {
        "CFBundleIdentifier": "com.becurrie.workday",
        "LSUIElement": True,
    },
}

setup(
    name="Workday",
    version="0.0.1",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
