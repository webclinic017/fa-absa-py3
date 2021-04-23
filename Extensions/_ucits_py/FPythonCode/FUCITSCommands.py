""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSCommands.py"
from __future__ import print_function
import importlib
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSCommands

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

def reload_ucits_pycode(_eii):
    """ Reload UCITS FPythonCode extensions """
                        
    for mod in acm.GetDefaultContext().GetAllExtensions('FPythonCode', 'FObject', True, True, '', '', False):
        mod_name = str(mod.Name())
        if mod_name[0:6] in ["FUCITS",]:
            importlib.reload(__import__(mod_name))
            print("Reloaded " + mod_name)
    acm.AEF.RegisterCustomFunctions()
    acm.AEF.RegisterCustomMethods()