#!/usr/bin/env python

from bbfreeze import Freezer
f = Freezer("miasmod")
f.addScript("miasmod.py", gui_only=True)
# f.addScript("miasmod.py", gui_only=False)
f()
