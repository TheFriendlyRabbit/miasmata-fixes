Miaspatch Binary Patches
==============

This directory contains scripts that describe and apply binary patches for Miasmata. These scripts are loaded by Miaspatch.

A valid patch should contain the following methods:

- ``apply_patch``: Attempts to apply the patch. Raises a ``PatchFailed`` exception on failure.
- ``check_status``: Returns whether a patch is installed (``STATUS_INSTALLED``), is not installed (``STATUS_NOT_INSTALLED``), or cannot be installed (``STATUS_NOT_INSTALLABLE``). 
- ``remove_patch``: Attempts to revert the patch. Raises a ``PatchFailed`` exception on failure.

4gb.py
---------
Allows the game to use 4 gigabytes of memory, fixing some crashes.

botanical.py
---------
Fixes the broken ``Botanical Bad A**`` Steam achievement.
