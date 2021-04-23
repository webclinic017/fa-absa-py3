""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FViewCallbacks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FViewCallbacks

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    FUiEventCallback functions for views.
-------------------------------------------------------------------------------------------------------"""
import FIntegratedWorkbench
import ViewLauncher
import acm

from FIntegratedWorkbenchLogging import creationLogger
from FPanelCreator import PanelCreator
from FViewCreator import GetPanels
from FViewUtils import ViewParameterSettings

VIEW_KEY = 'integratedWorkbenchView'


def OnFrameCreate(eii):
    application = eii.ExtensionObject()
    RegisterViewPanels(application)

def OnSavingWorkbook(eii):
    workbook = eii.ExtensionObject().StoredWorkbook()
    frame = eii.Parameter('Frame')
    view = FIntegratedWorkbench.GetView(frame)
    if view:
        workbook.ToArchive(VIEW_KEY, view.Name())

def OnWorkbookCreate(eii):

    def ViewName(workbook):
        viewName = workbook.FromArchive(VIEW_KEY)
        if viewName is None:
            # backwards compatibility
            viewName = ViewNameFromAddInfo(workbook)
        return viewName

    def ViewNameFromAddInfo(workbook):
        try:
            return workbook.AdditionalInfo().View()
        except Exception:
            return None

    workbook = eii.ExtensionObject().StoredSourceWorkbook()
    if workbook is not None:
        viewName = ViewName(workbook)
        if viewName is not None:
            frame = eii.Parameter('Frame')
            ViewLauncher.LaunchViewFromExistingApplication(viewName, frame)

def RegisterViewPanels(application):
    for settings in GetViewPanels(application):
        RegisterPanel(settings, application)

def RegisterPanel(settings, application):
    try:
        creator = PanelCreator.FromSettings(None, settings)
        createFunction = creator.CreateFunction()           
        createFunctionName = ''.join((settings.Name(), 'CreationFunction'))
        application.RegisterDockWindowType(settings.Name(), '.'.join((__name__, createFunctionName)))
        setattr(__import__(__name__), createFunctionName, createFunction)
    except Exception as e:
        creationLogger.debug('Error while trying to register panel on view: %s', e)

def GetViewPanels(application):
    for settings in ViewParameterSettings():
        if application.Name() == settings.Application():
            for panel in GetPanels(settings):
                yield panel