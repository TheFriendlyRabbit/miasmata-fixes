Miscellaneous Tools
==============

This directory contains miscellaneous standalone tools to aid in the parsing and analysis of Miasmata's files.

The files in this directory are not used by any other scripts in the repository.

interpret.py
---------
A script to help analyze unknown data in different formats.

**Usage:**  

``python interpret.py [format]``

``format``should be a [struct format string](https://docs.python.org/3/library/struct.html#format-strings).

**Additional notes:**
- Starting with floats seems to work well.
- Numbers in the range [0.0, 8192.0) may be map coordinates.
- Infinitesimally small numbers are probably not floats.

plot_inst_nodes.py
---------
This script reads the list of inst nodes that the game uses and plots their
bounding box on the game's map. This visually shows how the game breaks up its
data structures that list all the items found in the game (where items also
includes grass, trees, rocks, etc).

_Currently it requires certain files to have already been extracted into
specific locations - TODO is the ability to read them directly from main.rs5._