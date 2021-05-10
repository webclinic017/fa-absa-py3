""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FCustomMainPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FCustomMainPanel

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Note that self.Application() will return the acm container that holds your
    python implementation. If you want to access it use it as below.
-----------------------------------------------------------------------------"""

from FMainPanel import DefaultMainPanel

class CustomMainPanel(DefaultMainPanel):

    def PythonApplication(self):
        return self.Application().CustomLayoutApplication()

    def HandleCreate(self):
        super(self.__class__, self).HandleCreate()
        pythonApp = self.Application().CustomLayoutApplication()
        pythonApp.AddDependent(self)

    def ServerUpdate(self, update):
        raise NotImplementedError
