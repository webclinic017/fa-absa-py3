""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkMenu.py"
"""--------------------------------------------------------------------
MODULE

    MenuSupportForPriceLinkSpecification - Provides the functionality
    in price link specification needed for supporting menus

DESCRIPTION

    This module contains all the funtionality needed for supporting menu.
    The Menu contains different panels and commands. The handlers for the all
    the commands is imported from PriceLinkSpecification module.

--------------------------------------------------------------------"""
import FUxCore

from FPriceLinkApplicationStates import PriceLinkSpecificationStates as PLSStates
from FPriceLinkApplicationStates import PriceDistributorStates as PDStates
from FPriceLinkApplicationStates import PriceSemanticStates as PSStates

#*****************************************BASE CLASSES*****************************#

class MenuEnabledCommandHandler(FUxCore.MenuItem):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB = None):
        self.m_ApplicationObject = p_ParentApplication
        self.m_CommandName = p_CommandName
        self.m_CommandCB   = p_CommandCB

    def Invoke(self, cd):
        self.m_CommandCB()

    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

    def Instance(self):
        return self

class MenuDisabledCommandHandler(MenuEnabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB = None):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Enabled(self):
        return False

#*****************************************DERIVED CLASSES*****************************#

class PriceLinkPanelCommandsHandler(MenuDisabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuDisabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

    def Enabled(self):
        state = self.m_ApplicationObject.GetState()
        if self.m_CommandName == 'Add':
            state = state & PLSStates.PLDChanged
        elif self.m_CommandName == 'Delete':
            state = (state & PLSStates.PLDSelected and not state & PLSStates.PLDAdded) \
            or state & PLSStates.PLDMultiSelected
        elif self.m_CommandName == 'Update':
            state = (state & PLSStates.PLDSelected or state & PLSStates.PLDMultiSelected) \
             and state & PLSStates.PLDChanged
        elif self.m_CommandName == 'Clear':
            state = self.m_ApplicationObject.GetState()
        elif self.m_CommandName == 'Clear Selection':
            state = state & PLSStates.PLDSelected or state & PLSStates.PLDMultiSelected \
            or state & PLSStates.PLDChanged
        elif self.m_CommandName in ('Save', 'Revert'):
            state = (state & PLSStates.PLDUpdated) or (state & PLSStates.PLDAdded)
        elif self.m_CommandName == 'Revert All':
            state = self.m_ApplicationObject.pldList.rowsModified

        return bool(state)


class ColumnSettingsPanelCommandsHandler(MenuEnabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

class DistributorSettingsPanelCommandsHandler(MenuEnabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

class SemanticSettingsPanelCommandsHandler(MenuEnabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

class InsertItemsPanelCommandsHandler(MenuEnabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

class ToolsPanelCommandsHandler(MenuEnabledCommandHandler):
    def __init__(self,  p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

    def Enabled(self):
        return bool(self.m_ApplicationObject.GetState() & PLSStates.PLDSelected)

class OpenPanelCommandsHandler(MenuDisabledCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuDisabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

    def Enabled(self):
        return bool(self.m_ApplicationObject.GetState() & PLSStates.PLDSelected)

'''**************************Menu support for Price Distributor*****************'''
class PriceDistributorEditPanelCommandsHandler(MenuEnabledCommandHandler):
    """Command Handler class for PD Edit panel"""
    def __init_(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Enabled(self):
        state = self.m_ApplicationObject.GetState()
        if self.m_CommandName == 'Save New':
            state = state & PDStates.PDChanged
        if self.m_CommandName == 'Clear':
            state = (state & PDStates.PDSelected) or (state & PDStates.PDChanged)
        if self.m_CommandName == 'Delete':
            state = state & PDStates.PDSelected
        if self.m_CommandName == 'Revert':
            state = state & PDStates.PDChanged
        return bool(state)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

class PriceDistributorToolsPanelCommandsHandler(MenuEnabledCommandHandler):
    """Command Handler class for PD Tools panel"""
    def __init_(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

    def Enabled(self):
        return True

'''**************************Menu support for Price Semantic*****************'''
class PriceSemanticEditPanelCommandsHandler(MenuEnabledCommandHandler):
    """Command Handler class for PS Edit panel"""
    def __init_(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Enabled(self):
        state = self.m_ApplicationObject.GetState()
        if self.m_CommandName == 'Save New':
            state = state & PSStates.PSChanged
        if self.m_CommandName == 'Clear':
            state = (state & PSStates.PSSelected) or (state & PSStates.PSChanged)
        if self.m_CommandName == 'Delete':
            state = state & PSStates.PSSelected
        return bool(state)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)


class PriceSemanticToolsPanelCommandsHandler(MenuEnabledCommandHandler):
    """Command Handler class for PS Tools panel"""
    def __init_(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuEnabledCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

    def Enabled(self):
        state = self.m_ApplicationObject.GetState()
        if self.m_CommandName == 'Add':
            state = state & PSStates.PSChanged
        elif self.m_CommandName == 'Delete':
            state = (state & PSStates.PSSelected and not state & PSStates.PSAdded and not state & PSStates.PSUpdated) \
            or state & PSStates.PSMultiSelected
        elif self.m_CommandName == 'Update':
            state = (state & PSStates.PSSelected or state & PSStates.PSMultiSelected) \
             and state & PSStates.PSChanged
        elif self.m_CommandName == 'Clear':
            state = self.m_ApplicationObject.GetState()
        elif self.m_CommandName == 'Clear Selection':
            state = state & PSStates.PSSelected or state & PSStates.PSMultiSelected \
            or state & PSStates.PSChanged
        elif self.m_CommandName in ('Save', 'Revert'):
            state = (state & PSStates.PSUpdated) or (state & PSStates.PSAdded)

        return bool(state)
