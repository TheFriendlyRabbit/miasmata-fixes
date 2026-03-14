#!/usr/bin/env python

import os
import struct
from mmap import mmap, ACCESS_WRITE, ACCESS_READ

from PySide6.QtWidgets import QApplication

import miaspatch

IMAGE_FILE_LARGE_ADDRESS_AWARE = 0x0020

name = QApplication.translate('4GB patch', '4GB patch', None)
txt_scanning = QApplication.translate('4GB patch', 'Scanning Miasmata.exe...',
                                      None)
txt_already_patched = QApplication.translate('4GB patch',
                                             'The game is already patched',
                                             None)
txt_bad_header = QApplication.translate('4GB patch', 'Invalid PE header', None)
txt_success = QApplication.translate('4GB patch', 'Patch successful', None)
txt_err = QApplication.translate('4GB patch', 'Error writing to Miasmata.exe',
                                 None)

version = '1.0'


class PatchFailed(Exception):
    pass


# Adapted from https://github.com/pyinstaller/pyinstaller/issues/1288
def _apply_patch(filename, print=print, apply=True):
    with open(filename, 'rb+') as f:
        m = mmap(f.fileno(), 0, access=ACCESS_WRITE)
        print(txt_scanning)
        # Get PE header location
        m.seek(0x3c, 0)
        (pe_header_loc,) = struct.unpack('<H', m.read(2))
        # Get PE header, check it
        m.seek(pe_header_loc, 0)
        if m.read(4) != b'PE\0\0':
            print(txt_bad_header)
            raise PatchFailed()
        # Get Characteristics, check if IMAGE_FILE_LARGE_ADDRESS_AWARE bit is
        # set
        charac_offset = pe_header_loc + 22
        m.seek(charac_offset, 0)
        (bits,) = struct.unpack('h', m.read(2))
        m.seek(charac_offset, 0)
        if (bits & IMAGE_FILE_LARGE_ADDRESS_AWARE) == \
                IMAGE_FILE_LARGE_ADDRESS_AWARE:
            # Patch is installed
            if apply:
                # Do nothing if requesting installation
                print(txt_already_patched)
            else:
                # Unapply patch if we are requesting uninstallation
                out_bytes = struct.pack('h',
                                        (bits ^ IMAGE_FILE_LARGE_ADDRESS_AWARE))
                m.write(out_bytes)
        else:
            m.seek(charac_offset)
            # Patch is not installed
            if apply:
                # Apply patch if requesting installation
                out_bytes = struct.pack('h',
                                        (bits | IMAGE_FILE_LARGE_ADDRESS_AWARE))
                m.write(out_bytes)
            else:
                # Do nothing if requesting uninstallation
                print(txt_already_patched)
        rc = m.flush()
        m.close()
    if os.name == 'nt' and rc == 0:
        print(txt_err)
        raise PatchFailed()
    print(txt_success)


def apply_patch(filename, print=print):
    return _apply_patch(filename, print)


def remove_patch(filename, print=print):
    return _apply_patch(filename, print, apply=False)


def check_status(filename):
    with open(filename, 'rb') as f:
        m = mmap(f.fileno(), 0, access=ACCESS_READ)
        # Get PE header location
        m.seek(0x3c, 0)
        (pe_header_loc,) = struct.unpack('<H', m.read(2))
        # Get PE header, check it
        m.seek(pe_header_loc, 0)
        if m.read(4) != b'PE\0\0':
            m.close()
            return miaspatch.STATUS_NOT_INSTALLABLE
        # Get Characteristics, check if IMAGE_FILE_LARGE_ADDRESS_AWARE bit is
        # set
        charac_offset = pe_header_loc + 22
        m.seek(charac_offset, 0)
        (bits,) = struct.unpack('h', m.read(2))
        m.close()
        if (bits & IMAGE_FILE_LARGE_ADDRESS_AWARE) == IMAGE_FILE_LARGE_ADDRESS_AWARE:
            return miaspatch.STATUS_INSTALLED
        return miaspatch.STATUS_NOT_INSTALLED


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    apply_patch(filename)
