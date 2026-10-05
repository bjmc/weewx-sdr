# installer for the weewx-sdr driver
# Copyright 2016-2024 Matthew Wall
# Distributed under the terms of the GNU Public License (GPLv3)

from pathlib import Path

from weecfg.extension import ExtensionInstaller

EXTENSION_DIR = Path(__file__).resolve().parent
SOURCE_DIR = EXTENSION_DIR / 'bin/user'


def get_filenames():
    return sorted(p.relative_to(EXTENSION_DIR).as_posix() for p in SOURCE_DIR.glob('**/*.py'))


def loader():
    return SDRInstaller()


class SDRInstaller(ExtensionInstaller):
    def __init__(self):
        super(SDRInstaller, self).__init__(
            version='0.96b1',
            name='sdr',
            description='Capture data from rtl_433',
            author='Matthew Wall',
            author_email='mwall@users.sourceforge.net',
            files=[('bin/user', get_filenames())],
        )
