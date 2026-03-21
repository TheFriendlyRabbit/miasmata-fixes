Miasmod Library Files
==============
This directory contains miscellaneous files that contain helper functions for other scripts.

cterr_hmap.py
--------
Contains functions for reading and manipulating data from the game's ``cterr_hamp`` file, which is used to store the height map for the island.

imag.py
---------
Contains material related to loading [DirectDraw Surface texture files](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds), stored by Miasmata with the identifier ``IMAG``.


inst_header.py
---------
Contains functions related to parsing the ``inst_header`` portion of an RS5 file, which contains a list of instance nodes.


miasmap.py
---------
Contains helper functions related to visualizing data that relates to the game's map.


miasutil.py
---------
Contains helper functions related to cross-platform locating and loading of Miasmata's game files and save files.

smap.py
---------

Functions for decoding SMAP type files, and overlaying them on the game map image.

(The only known SMAP file is ``player_map_achievements``, which encodes the shoreline data for the achievement "The Bored Cartographer".)


ui_utils.py
---------
Contains helper functions used by UI-based tools.