#!/usr/bin/env python

import os


def is_windows():
    return os.name == 'nt'


if is_windows():
    import winpaths
    import winreg


def find_miasmata_install():
    if is_windows():
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             'SOFTWARE\\IonFX\\Miasmata', 0,
                             winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
        ret = winreg.QueryValueEx(key, 'Install_Path')[0]
        if not os.path.isdir(ret):
            raise IOError('Miasmata install path from registry does not exist')
    else:
        # default Steam installation location
        ret = (f'{os.getenv("HOME")}/.local/share/Steam/steamapps/common'
               f'/Miasmata')
        if not os.path.isdir(ret):
            raise IOError(
                'Miasmata not found in the default Steam installation path')
    return ret


def find_miasmata_save():
    if is_windows():
        return os.path.join(winpaths.get_appdata(), 'IonFx', 'Miasmata',
                            'saves.dat')
    else:
        # default Steam saves location
        return (f'{os.getenv("HOME")}/.local/share/Steam/steamapps/compatdata'
                f'/223510/pfx/drive_c/users/steamuser/AppData/Roaming/IonFx'
                f'/Miasmata/saves.dat')

# vi:noexpandtab:sw=8:ts=8
