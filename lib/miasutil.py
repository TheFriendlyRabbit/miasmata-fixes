#!/usr/bin/env python

import os

from lib import rs5archive


def is_windows():
    """
    Returns ``True`` if the system is Windows, ``False`` otherwise.
    :rtype: bool
    """
    return os.name == 'nt'


def find_miasmata_install():
    """
    Returns the Miasmata install location for this system.
    On Windows, searches the path described by a registry key;
    on Linux, searches the default Steam installation path.
    If Miasmata cannot be found, raises an ``IOError``.
    :return: The Miasmata install path for this system
    :rtype: str
    :raises IOError: Miasmata not found
    """
    if is_windows():
        import winreg
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
    """
    Returns the default path for the Miasmata saves.dat file on this system.
    On Windows, the file is located in the IonFx local ``AppData`` folder.
    On Linux, it's located in an equivalent folder in Steam's ``compatdata``
    folder for Miasmata.

    Unlike ``find_miasmata_install``, this method does not verify that a save
    file actually exists at the given location.
    :return: The default Miasmata saves.dat path for this system
    :rtype: str
    """
    if is_windows():
        import winpaths
        return os.path.join(winpaths.get_appdata(), 'IonFx', 'Miasmata',
                            'saves.dat')
    else:
        # default Steam saves location
        return (f'{os.getenv("HOME")}/.local/share/Steam/steamapps/compatdata'
                f'/223510/pfx/drive_c/users/steamuser/AppData/Roaming/IonFx'
                f'/Miasmata/saves.dat')


def load_rs5_file(filename, directory=None):
    """
    Loads a .rs5 archive into an ``Rs5ArchiveDecoder`` object.
    By default, the archive is loaded from the default Miasmata install path.
    Otherwise, if ``directory`` is specified, the file is loaded from the
    provided directory.
    :param filename: rs5 archive filename
    :type filename: str
    :param directory: (optional) Directory from which to load rs5 archive file
    :type directory: str
    :return: ``Rs5ArchiveDecoder`` object for the file at the provided path
    :rtype: ``rs5archive.Rs5ArchiveDecoder``
    """
    if directory:
        file_path = os.path.join(directory, filename)
    else:
        file_path = os.path.join(find_miasmata_install(), filename)
    try:
        return rs5archive.Rs5ArchiveDecoder(open(file_path, 'rb'))
    except Exception as e:
        print(f"ERROR loading RS5 archive file {file_path}!")
        raise Exception(e)

# vi:noexpandtab:sw=8:ts=8
