""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./../AM_common/FOperationsManagerWorkbench.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FOperationsManagerWorkbench

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FUxCore


def StartOperationsManagerWorkbench(defaultObjects=None, sheetTemplate=None,
        additionalColumnIds=None, grouperName=None, expandAllRows=False,
        expandedRowFilter=None, sheetType='BusinessProcessSheet',
        grouperSubjectClass=acm.FBusinessProcessGrouperSubject):
    """Start an Operations Manager based workbench.
    
    Opens the Operations Manager, initialising it with an optional sheet
    template and additional sheet columns before inserting the passed default
    objects into the sheet. A grouper may then be a applied with rows optionally
    being fully expanded if not filtered out by the row filter.

    """
    operationsMgr = acm.StartApplication('Operations Manager', sheetTemplate)
    if not sheetTemplate:
        operationsMgr.ActiveWorkbook().NewSheet(sheetType)

    sheet = operationsMgr.ActiveWorkbook().ActiveSheet()
    if additionalColumnIds:
        columnIds = acm.FArray().AddAll(additionalColumnIds)
        columnCreators = sheet.ColumnCreators()
        if not sheetTemplate:
            columnCreators.Clear()
        requiredColumnCreators = acm.GetColumnCreators(columnIds, acm.GetDefaultContext())
        for i in range(requiredColumnCreators.Size()):
            columnCreators.Add(requiredColumnCreators.At(i))
    if defaultObjects:
        for obj in defaultObjects:
            sheet.InsertObject(obj, 'IOAP_LAST')
    if grouperName:
        grouper = acm.Risk().GetGrouperFromName(grouperName, grouperSubjectClass)
        row = sheet.RowTreeIterator(True).FirstChild()
        if row:
            row.Tree().ApplyGrouper(grouper)
            sheet.GridBuilder().Refresh()
            if expandAllRows:
                expandedRowFilter = set(expandedRowFilter or [])
                child = sheet.RowTreeIterator(True).FirstChild()
                while child:
                    tree = child.Tree()
                    if (tree.Item().StringKey() not in expandedRowFilter and
                        not tree.Item().IsKindOf(acm.FLimit)):
                        tree.Expand(True)
                    child = child.NextUsingDepthFirst()


class WorkbenchPanel(FUxCore.LayoutPanel):
    """Base class for workbench panels.

    Workbench bench panels are dockable windows in a trading sheet frame, and
    consist of one or more WorkbenchControls.

    """
    def __init__(self):
        self._controls = []

    def AddControl(self, ctrl):
        """All WorkbenchControls contained within the panel must be added
        using this method."""
        self._controls.append(ctrl)
        return ctrl

    def HandleCreate(self):
        """Called on the creation of the panel. All child WorkbenchControls
        will subsequently be called for creation and initialisation."""
        layout = self.SetLayout(self.CreateLayout())
        for c in self._controls:
            try:
                c.HandleCreate(layout)
            except Exception as e:
                self._LogError('handling creation', c, e)

    def HandleDestroy(self):
        """Called on the destruction of the panel. All child WorkbenchControls
        will subsequently be called for cleanup."""
        for c in self._controls:
            try:
                c.HandleDestroy()
            except Exception as e:
                self._LogError('handling destruction', c, e)

    def CreateLayout(self):
        """Create the layout of the panel. All child WorkbenchControls
        will subsequently be called to create their layout."""
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        for c in self._controls:
            c.CreateLayout(b)
        b.EndBox()
        return b

    def Enabled(self, enabled):
        """Enable or disable the panel (including all child controls)."""
        for c in self._controls:
            try:
                c.Enabled(enabled)
            except Exception as e:
                self._LogError('setting enabled state', c, e)

    @classmethod
    def IsPanelSupported(cls, eii):
        """Returns whether or not this panel is supported or applicable for the current
        Operations Manager environment (e.g. currently selected row object). If the
        panel is not supported, it will be hidden from view."""
        return True

    def OnSelectedItemChanged(self):
        """Callback for when the selected item in the main trading sheet
        frame is changed. Only enabled child WorkbenchControls will
        receive a subsequent notification.

        """
        for c in self._controls:
            try:
                if c.Enabled():
                    c.OnSelectedItemChanged()
            except Exception as e:
                self._LogError('handling selection change', c, e)

    def OnSelectedItemUpdated(self):
        """Callback for when the currently selected item in the main
        trading sheet frame is updated. Only enabled child WorkbenchControls
        will receive a subsequent notification.

        """
        for c in self._controls:
            try:
                if c.Enabled():
                    c.OnSelectedItemUpdated()
            except Exception as e:
                self._LogError('handling selected item update', c, e)

    @staticmethod
    def _LogError(action, control, exception):
        # Attempted updates during grid changes can result in an RuntimeError thrown
        # by FUxProxy when accessing the control subject. This can't be checked and
        # avoided in advance, so instead avoid outputing to the log as further updates
        # will address the problem anyway.
        if 'FUxProxy::GetValidSubject' not in str(exception):
            print('Error %s for control type %s: (%s) %s' % (action, 
                    control.__class__.__name__, exception.__class__.__name__, exception))


class WorkbenchControl(object):
    """Base class for a control in a workbench panel.

    Workbench controls consist of one or more FUx controls serving a
    common functional purpose.

    """
    def __init__(self, panel):
        self._panel = panel
        self._enabled = True
        self._fuxControls = []

    def RegisterFUxControl(self, ctrl):
        """All child FUx controls must be registered with this method."""
        self._fuxControls.append(ctrl)
        return ctrl

    def Panel(self):
        """Return the parent WorkbenchPanel of the control."""
        return self._panel

    def HandleCreate(self, layout):
        """Called on the creation of the control.

        Subclasses must perform creation and initialisation steps within
        this callback.

        """
        raise NotImplementedError()

    def HandleDestroy(self):
        """Called on the destruction of the control."""
        for c in self._fuxControls:
            try:
                c.HandleDestroy()
            except Exception:
                pass
        self._fuxControls = []

    def CreateLayout(self, builder):
        """Called on to provide the layout of the control.

        Subclasses must perform layout creation using the builder provided
        by this callback.

        """
        raise NotImplementedError()

    def OnSelectedItemChanged(self):
        """Callback for when the selected item in the main trading sheet
        frame is changed."""
        pass

    def OnSelectedItemUpdated(self):
        """Callback for when the selected item in the main trading sheet
        frame is updated."""
        pass

    def Enabled(self, enabled=None):
        """Return the enabled state of the control, or set to enable or
        disable the control."""
        if enabled == None:
            return self._enabled
        self._enabled = enabled
        for c in self._fuxControls:
            try:
                c.Visible(enabled)
            except RuntimeError:
                # FUxListControl sometimes throw on a FUxProxy::GetValidSubject assertion here
                pass


class BusinessProcessWorkbenchPanel(WorkbenchPanel):
    """A business process workbench panel.

    Represents a workbench panel, centred on the business process sheet in the Operations
    Manager, for managing the processing of business process related activities.

    """
    # The business process subject class type applicable for this panel
    SUBJECT_TYPE = None

    def __init__(self):
        WorkbenchPanel.__init__(self)
        self._businessProcess = None
        self._activeSheet = None

    def ActiveSheet(self):
        """Return the active sheet of the workbench."""        
        return self._activeSheet

    def BusinessProcess(self):
        """Return the currently selected business process."""
        return self._businessProcess
        
    def ReconciliationItem(self):
        """ Return the associated reconciliation item for the business process """
        return self.BusinessProcess().Subject()
        
    def StoredWildcardedQuery(self):
        """ Return the associated stored (wildcarded) query for the clicked row object """        
        return self.ReconciliationItem().Subject() if self.ReconciliationItem() else None

    @classmethod
    def SubjectType(cls):
        """Return the business process subject class type that this panel will process."""
        return cls.SUBJECT_TYPE

    @classmethod
    def IsPanelSupported(cls, eii):
        # The panel is only visible if a business process is currently selected 
        # which has a subject of the applicable type
        return bool(cls._GetBusinessProcess(eii))

    def OnBusinessProcessSelectionChanged(self, eii):
        """Callback for handling business process selection changes."""
        self._activeSheet = eii.ExtensionObject().ActiveSheet()
        bp = self._GetBusinessProcess(eii)
        if bp != self.BusinessProcess():
            self._SetBusinessProcess(bp)
            self.OnSelectedItemChanged()

    def ServerUpdate(self, _sender, _aspect, _param):
        # Called on business process update
        self.OnSelectedItemUpdated()

    def HandleCreate(self):
        WorkbenchPanel.HandleCreate(self)
        if not self.BusinessProcess():
            # Disable the panel until a selection is made
            self.Enabled(False)
        else:
            # Force a refresh of the panel. Multiple creation calls can occur 
            # when panels are docked or floated by the user.
            self.OnSelectedItemUpdated()

    def OnSelectedItemUpdated(self):
        # Treat business process updates as if a new one has been selected,
        # forcing controls to reinitialise and redraw.
        self.OnSelectedItemChanged()

    @classmethod
    def _GetBusinessProcess(cls, eii):
        try:
            sheet = eii.ExtensionObject().ActiveSheet()
            for row in sheet.Selection().SelectedRowObjects():
                if row.IsKindOf(acm.FBusinessProcess) and row.Subject():
                    if cls.SubjectType() and row.Subject().IsKindOf(cls.SubjectType()):
                        return row
        except AttributeError:
            pass
        return None

    def _SetBusinessProcess(self, bp):
        if self._businessProcess:
            self._businessProcess.RemoveDependent(self)
        self._businessProcess = bp
        if bp:
            self._businessProcess.AddDependent(self)


def OnBusinessProcessPanelSelectionChanged(eii, panels):
    """Helper function for handling the selection changed callback from the
    Operations Manager frame. Passes the notification on to any contained
    BusinessProcessWorkbenchPanel objects.

    """
    frame = eii.ExtensionObject()
    for panelKey, panelClass in panels:
        # Show/hide panels based if they are supported or not
        supported = panelClass.IsPanelSupported(eii)
        panel = frame.GetCustomDockWindow(panelKey)
        try:
            if not panel and supported:
                frame.ShowDockWindow(panelKey, True)
                panel = frame.GetCustomDockWindow(panelKey)
            elif panel and not supported:
                frame.ShowDockWindow(panelKey, False)
                panel = None
            elif panel and supported:
                frame.ShowDockWindow(panelKey, True)
        except RuntimeError as e:
            import traceback
            traceback.print_stack()

        # Process selection changes
        if not panel:
            continue
        func = getattr(panel.CustomLayoutPanel(), 'OnBusinessProcessSelectionChanged')
        if not func:
            continue
        try:
            func(eii)
        except Exception as e:
            print('Workbench panel failed to handle selection change:', str(e))
