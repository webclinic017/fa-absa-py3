""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FPanelCreator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FPanelCreator

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Internal classes for creating handlers and panels.
-------------------------------------------------------------------------------------------------------"""

import acm
from FWorkbookPanel import DefaultWorkbookPanel
from FMainPanel import DefaultMainPanel
from FSheetPanel import DefaultSheetPanel
from FIntegratedWorkbenchLogging import creationLogger
from FIntegratedWorkbenchUtils import GetAttributeInModule, ClassFactory


def CreatePanel(app, panelSettings):
    try:
        creator = PanelCreator.FromSettings(app, panelSettings)
        panel = creator.CreatePanel()
        return panel
    except AttributeError:
        creationLogger.debug('Failed to create panel from settings %s', panelSettings.Name())

def CreateMainPanel(app, settings):
    return MainPanelCreator(app, settings).CreatePanel()


class Creator(object):

    def __init__(self, settings):
        self._settings = settings

    def Settings(self):
        return self._settings

    def GetModuleName(self):
        name = None
        try:
            name = self.Settings().Module()
            if not isinstance(name, str):
                name = name.Name()
            return name
        except AttributeError:
            pass
        if name is None:
            raise ValueError

    def GetClassName(self):
        if self.HasExtends(self.Settings()):
            try:
                return self.Settings().Extends().Name()
            except AttributeError:
                return self.Settings().Extends()
        return self.Settings().Name()

    def GetClass(self, moduleName, className):
        theClass = GetAttributeInModule(self.ClassPath(moduleName, className))
        if className != self.Settings().Name():
            theClass = ClassFactory(self.Settings().Name(), theClass)
        return theClass

    def CreateFunction(self):
        try:
            moduleName = self.GetModuleName()
            className = self.GetClassName()
            theClass = self.GetClass(moduleName, className)
            return getattr(theClass, 'Create')
        except AttributeError:
            creationLogger.debug("Unable to get class '%s' "
                                 "in module '%s'" % (className, moduleName))
        except ImportError:
            creationLogger.debug("Unable to get module '%s' "
                                 "for item '%s'" % (moduleName, className))
        except ValueError:
            return None
            
    @staticmethod
    def HasExtends(settings):
        return hasattr(settings, 'Extends') and settings.Extends()

    @staticmethod
    def ClassPath(moduleName, panelClassName):
        return  '.'.join((moduleName, panelClassName))


class PanelCreator(Creator):


    def __init__(self, app, settings):
        super(PanelCreator, self).__init__(settings)
        self._app = app

    def Name(self):
        return self._settings.Name()

    def CreatePanel(self, relativeTo=None, showInitially=None, autoHidden=None):
        try:
            if showInitially is None and hasattr(self.Settings(), "ShowInitially"):
                showInitially = self.Settings().ShowInitially()
            if autoHidden is None and hasattr(self.Settings(), "AutoHidden"):
                autoHidden = self.Settings().AutoHidden()
            return self._CreatePanel(relativeTo=relativeTo,
                                     showInitially=showInitially,
                                     autoHidden=autoHidden)
        except (AttributeError, TypeError):
            return self._CreatePanel()

    def _DefaultPanelFactory(self):
        if self.Settings().Type() == 'SheetPanel':
            return ClassFactory(self.Name(), DefaultSheetPanel)

    def _CreatePanel(self, relativeTo=None, showInitially=None, autoHidden=False):
        raise NotImplementedError

    @classmethod
    def FromSettings(cls, app, panelSettings):
        if not cls.IsValid(panelSettings):
            creationLogger.warn("Failed to create panel '{0}'. Expected "
                        "FParameter '{0}' describing the panel not found.".format(panelSettings))
            return None
        if panelSettings.Type() == 'TabbedPanel':
            return DockPanelTabCreator(app, panelSettings)
        return DockPanelCreator(app, panelSettings)

    @classmethod
    def IsValid(cls, settings):
        return not isinstance(settings, str)


class MainPanelCreator(PanelCreator):

    def _CreateMainPanel(self):
        try:
            mainPanelFunction = self.CreateFunction()
            if mainPanelFunction:
                return mainPanelFunction(self._app)
        except StandardError as exc:
            creationLogger.error("Failed to create main panel {0}, Reason: {1}".format(self.Name(), exc))
            creationLogger.debug(exc)

    def _CreateDefaultMainPanel(self):
        panelCls = self._DefaultPanelFactory()
        return panelCls.Create(self._app)

    def _CreatePanel(self, relativeTo=None, showInitially=None, autoHidden=False):
        mainPanel = self._CreateMainPanel()
        if mainPanel is None:
            creationLogger.debug("Falling back to default main panel")
            return self._CreateDefaultMainPanel()
        return mainPanel

    def _DefaultPanelFactory(self):
        if self._app.IsKindOf(acm.FManagerBaseFrame):
            baseClass = DefaultWorkbookPanel
        else:
            baseClass = DefaultMainPanel
        return ClassFactory(self.Name(), baseClass)



class DockPanelCreator(PanelCreator):

    def __init__(self, app, settings):
        super(DockPanelCreator, self).__init__(app, settings)

    def _DockOnSameRowCol(self, position):
        if (hasattr(self.Settings(), 'PositionRelativeTo') and
                self.Settings().PositionRelativeTo()):
            self._app.DockOnSameRowCol(self.Settings().PositionRelativeTo().Name(),
                                                       self.Name(),
                                                       position)

    def _CreateDockPanel(self, name, position, showInitially, autoHidden):
        panelFunction = self.CreateFunction() or self._DefaultPanelFactory()
        if panelFunction:
            dockPanel = self._app.CreateRegisteredDockWindow(
                                                                type=name,
                                                                key=name,
                                                                caption=self.Settings().Caption(),
                                                                dockBar=position,
                                                                stretch=False,
                                                                showInitially=showInitially,
                                                                autoHidden=autoHidden,
                                                                canToggleVisibility=True
                                                                )
            self._DockOnSameRowCol(position)
            return dockPanel

    def _CreatePanel(self, relativeTo=None, showInitially=True, autoHidden=False):
        name = self.Name()
        position = relativeTo or self.Settings().Position()
        if autoHidden is None and hasattr(self.Settings(), "AutoHidden"):
            autoHidden = self.Settings().AutoHidden()        
        try:
            return self._CreateDockPanel(name, position, showInitially, autoHidden)
        except StandardError as exc:
            creationLogger.error("Unable to create panel {0}, Reason: {1}".format(name, exc))
            creationLogger.debug(exc, exc_info=True)

class DockPanelTabCreator(DockPanelCreator):

    def DockPanels(self):
        return self.Settings().DockWindows()

    def _CreatePanel(self, relativeTo=None, showInitially=None, autoHidden=False):
        panels = []
        if autoHidden is None and hasattr(self.Settings(), "AutoHidden"):
            autoHidden = self.Settings().AutoHidden()
        for name in self.DockPanels():
            panels.append(DockPanelCreator.FromSettings(self._app, name).CreatePanel(
                relativeTo=self.Settings().Position(),
                showInitially=False,
                autoHidden=autoHidden))
        self._DockInSameTab()
        self._ShowDockPanels()
        return panels

    def _DockInSameTab(self):
        dockPanelsIter = iter(self.DockPanels())
        basePanelSettings = next(dockPanelsIter)
        for panelSettings in dockPanelsIter:
            try:
                self._app.DockInSameTab(
                    basePanelSettings.Name(), panelSettings.Name())
            except RuntimeError as exc:
                creationLogger.error("Unable to dock panel {0}, Reason: {1}".format(self.Settings().Name(), exc))
                creationLogger.debug(exc, exc_info=True)

    def _ShowDockPanels(self):
        try:
            self._app.ShowDockWindow(
                self.Settings().DefaultPanel().Name())
        except StandardError:
            for panelSettings in reversed(list(self.DockPanels())):
                self._app.ShowDockWindow(
                    panelSettings.Name())
                break
