""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleViewsMenuItem.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleViewsMenuItem

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Menu items to launch the two views from the session manager
-------------------------------------------------------------------------------------------------------"""
import FUxCore
import FIntegratedWorkbench


class ExampleViewsMenuItem(FUxCore.MenuItem, object):

    def __init__(self, extObj, view):
        self._view = view

    def Invoke(self, eii):
        FIntegratedWorkbench.LaunchView(self._view)

def CreateExampleView1MenuItem(eii):
    return ExampleViewsMenuItem(eii, 'ExampleView1')

def CreateExampleView2MenuItem(eii):
    return ExampleViewsMenuItem(eii, 'ExampleView2')

def CreateExampleView3MenuItem(eii):
    return ExampleViewsMenuItem(eii, 'ExampleView3')