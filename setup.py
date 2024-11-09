from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'pic.icns',
    'plist': {
        'CFBundleName': 'IDsteam',
        'CFBundleDisplayName': 'IDsteam',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'IDsteam',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)