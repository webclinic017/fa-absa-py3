""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceDistributor.py"
from __future__ import print_function
"""--------------------------------------------------------------------
MODULE

    PriceDistributor - creates a Price Distributor GUI.

DESCRIPTION

    This script creates the Price Distributor GUI using FAUx.
    It displays attributes of the stored price distributor.
    It also enables the updating, adding and deleting
    of Price Distributor.

--------------------------------------------------------------------"""

import acm
import FUxCore

import FPriceLinkApplication as CB
from FPriceLinkApplication import PriceLinkApplication
from FPriceLinkApplication import PriceServicesChangeHandler
import FPriceLinkMenu as Menu
import FTimeStampsCustomDialog as TimeStampsDialog
import FProtectionCustomDialog as ProtectionDialog
import FPriceLinkToolTips as ToolTips
import FPriceLinkSpecificationUtils as Utils
from FPriceLinkApplicationStates import PriceDistributorStates as States
from FPriceLinkApplicationStates import PermittedDistributorTypes as DistributorTypes
from FPriceLinkSpecificationUtils import ButtonOptions, SYMBOL_PLUSMINUS

APPLICATION_NAME =  "Price Distributor"

def OnProtectionSelected(PriceDistDlg, arg):
    """Action when Protection is clicked"""
    oldOwner = PriceDistDlg.owner
    oldProtection = PriceDistDlg.protection
    shell = PriceDistDlg.Shell()
    newOwner, newProtection = ProtectionDialog.StartDialog(shell, oldOwner, oldProtection)
    if (oldOwner.Name() != newOwner.Name()) or (oldProtection != newProtection):
        PriceDistDlg.owner = newOwner
        PriceDistDlg.protection = newProtection
        OnAnyFieldSelected(PriceDistDlg, None)

def OnTimeStampsSelected(PriceDistDlg, arg):
    """Action when Time Stamps is clicked"""
    pdist_obj = acm.FPriceDistributor[PriceDistDlg.price_dist.GetData()]
    TimeStampsDialog.StartDialog(PriceDistDlg.Shell(), pdist_obj)

def OnSelectAllSelected(PriceDistDlg, arg):
    """Action when Select All is checked"""
    if PriceDistDlg.select_all.Checked():
        PriceDistDlg.CheckAllResetFields()
        PriceDistDlg.SetForceResetForAMSDistributor()
    else:
        PriceDistDlg.UnCheckAllResetFields()

def OnUseUTCOffset(PriceDistDlg, arg):
    if PriceDistDlg.use_utc_offset.Checked():
        PriceDistDlg.utc_offset.Enabled(True)
        price_dist_name = PriceDistDlg.price_dist.GetData()
        price_dist_obj = acm.FPriceDistributor[price_dist_name]
        if price_dist_obj:
            PriceDistDlg.utc_offset.SetData(price_dist_obj.UtcOffset())
    else:
        PriceDistDlg.utc_offset.Clear()
        PriceDistDlg.utc_offset.Enabled(False)

def OnSaveNewSelected(PriceDistDlg, arg):
    """Action when Save New is clicked"""
    priceDistributorName = PriceDistDlg.price_dist.GetData()
    if not priceDistributorName:
        PriceDistDlg.ShowError('Please enter distributor name')
        return

    priceDistributor = acm.FPriceDistributor[priceDistributorName]
    if priceDistributor:
        message = 'Distributor %s already exists.\n' %(priceDistributorName)\
                    + 'Do you want to update it?'
        choice = PriceDistDlg.ShowQuestion(message)
        if choice == ButtonOptions.CANCEL:
            return
    else:
        priceDistributor = acm.FPriceDistributor()
        priceDistributor.Name = priceDistributorName

    try:
        update_price_distributor(PriceDistDlg, priceDistributor)
        priceDistributor.Commit()
        PriceDistDlg.SetCaption(priceDistributorName)
        PriceDistDlg.price_dist.AddItem(priceDistributorName)
        set_price_dist_attributes(PriceDistDlg)
        OnPriceDistributorSelected(PriceDistDlg, arg)
        PriceDistDlg.SetState(States.PDSelected)
    except ValueError as e:
        PriceDistDlg.ShowError(str(e))
    except Exception as e:
        message = "Failed to Commit. Error_Description : " + str(e)
        PriceDistDlg.ShowError(message)

def OnDeleteSelected(PriceDistDlg, arg):
    """Action when Delete is clicked"""
    priceDistributorName = PriceDistDlg.price_dist.GetData()
    if not priceDistributorName:
        PriceDistDlg.ShowError('Please select a valid Price Distributor.')
        return

    priceDistributor = acm.FPriceDistributor[priceDistributorName]
    if not priceDistributor:
        PriceDistDlg.ShowError('Please select a valid Price Distributor.')
        return

    message = 'Do you want to delete Price Distributor %s?' % priceDistributorName
    choice = PriceDistDlg.ShowQuestion(message)
    if choice == ButtonOptions.CANCEL:
        return

    try:
        priceDistributor.Delete()
        clear_fields(PriceDistDlg)
        PriceDistDlg.SetCaption('')
        PriceDistDlg.SetState(States.PDOpened)
        PriceDistDlg.price_dist.RemoveItem(priceDistributorName)
    except Exception as e:
        message = "Failed to Commit. \nError_Description : " + str(e)
        PriceDistDlg.ShowError(message)

def OnSaveSelected(PriceDistDlg, arg):
    """Action when Save is clicked"""
    priceDistributorName = PriceDistDlg.price_dist.GetData()
    if not priceDistributorName:
        PriceDistDlg.ShowError('Please enter distributor name')
        return

    priceDistributor = acm.FPriceDistributor[priceDistributorName]
    isPriceDistributorRenamed = False
    if not priceDistributor:
        #Create new Price Distributor
        message = 'Distributor %s does not exist.\n' %(priceDistributorName)\
                + 'Do you want to rename existing price distributor?'
        choice = PriceDistDlg.ShowQuestion(message)
        if choice == ButtonOptions.CANCEL:
            return

        priceDistributor = acm.FPriceDistributor[PriceDistDlg.distributor]
        priceDistributor.Name = priceDistributorName
        isPriceDistributorRenamed = True
    else:
        #Changing Price Distributor parameters, display linked no of price links.
        refCount = acm.FPriceLinkDefinition.Select('priceDistributor=%s' %(priceDistributor.Name()))
        if refCount.Size() > 20:
            message = "Price Distributor %s is linked with " %(priceDistributorName)\
                + "%d " %(refCount.Size())\
                + "price links.\nIf the APH is currently running, "\
                + "a re-subscription will be sent to all linked price links. "\
                + "Do you still want to update it ?"
            choice = PriceDistDlg.ShowQuestion(message)
            if choice == ButtonOptions.CANCEL:
                return
            
    try:
        update_price_distributor(PriceDistDlg, priceDistributor)
        priceDistributor.Commit()
        PriceDistDlg.SetCaption(priceDistributorName)
        if isPriceDistributorRenamed:
            PriceDistDlg.price_dist.RemoveItem(PriceDistDlg.distributor)
            PriceDistDlg.price_dist.AddItem(priceDistributorName)
        set_price_dist_attributes(PriceDistDlg)
        OnPriceDistributorSelected(PriceDistDlg, arg)
        PriceDistDlg.SetState(States.PDSelected)
    except ValueError as e:
        PriceDistDlg.ShowError(str(e))
    except Exception as e:
        message = "Failed to Commit. \nError_Description : " + str(e)
        PriceDistDlg.ShowError(message)

def OnClearSelected(PriceDistDlg, arg):
    """Actions when New is clicked"""
    clear_fields(PriceDistDlg)

def OnRevertSelected(PriceDistDlgObj, arg):
    """ Action when Revert is selected """
    priceDistributorName = PriceDistDlgObj.distributor
    if not priceDistributorName:
        return

    priceDistributor = acm.FPriceDistributor[priceDistributorName]
    if priceDistributor and priceDistributor.Name() == priceDistributorName:
        PriceDistDlgObj.distributor = priceDistributorName
        PriceDistDlgObj.owner = priceDistributor.Owner()
        PriceDistDlgObj.protection = priceDistributor.Protection()
        PriceDistDlgObj.price_dist.SetData(priceDistributorName)
        set_price_dist_attributes(PriceDistDlgObj)
        PriceDistDlgObj.SetState(States.PDSelected)
    else:
        PriceDistDlgObj.SetState(States.PDChanged)
    
def clear_fields(PriceDistDlg):
    """clears all fields"""
    #Set attributes on Prameters Pane
    PriceDistDlg.price_dist.SetData("")
    PriceDistDlg.service.SetData("")
    PriceDistDlg.semantic.SetData("")
    PriceDistDlg.start_time.Clear()
    PriceDistDlg.stop_time.Clear()
    PriceDistDlg.distributor_type.SetData("")
    PriceDistDlg.use_entitlement.Clear()
    PriceDistDlg.utc_offset.Clear()
    PriceDistDlg.use_utc_offset.Clear()
    PriceDistDlg.utc_offset.Enabled(False)
    PriceDistDlg.is_delayed.Clear()
    PriceDistDlg.ignore_clear_price.Clear()
    PriceDistDlg.update_interval.Clear()
    PriceDistDlg.last_follow_interval.Clear()
    PriceDistDlg.discard_zero_price.Clear()
    PriceDistDlg.discard_zero_quantity.Clear()
    PriceDistDlg.discard_negative_price.Clear()
    PriceDistDlg.force_update.Clear()
    PriceDistDlg.error_msg.Clear()
    PriceDistDlg.select_all.Clear()

    #Set attributes on Details Pane
    PriceDistDlg.force_reset.Clear()
    PriceDistDlg.force_reset.Enabled(True)
    PriceDistDlg.SetResetFields(0)
    PriceDistDlg.xml_data.SetData("")
    PriceDistDlg.SetCaption('')
    PriceDistDlg.SetState(States.PDOpened)

def OnAnyFieldSelected(PriceDistDlg, arg):
    """Action when Any Field is changed"""
    PriceDistDlg.SetState(States.PDChanged)

def OnDistTypeSelected(PriceDistDlgObj, arg):
    """Action when Distributor Type is changed"""
    distributorType = PriceDistDlgObj.distributor_type.GetData()
    distributorName = PriceDistDlgObj.price_dist.GetData()
    if distributorName:
        distributor = acm.FPriceDistributor[distributorName]
        SetInfoByDistributorType(PriceDistDlgObj, distributor, distributorType)

def OnPriceDistributorSelected(PriceDistDlgObj, arg):
    """Action when Price Distributor name is changed"""
    priceDistributorName = PriceDistDlgObj.price_dist.GetData()
    if not priceDistributorName:
        return

    priceDistributor = acm.FPriceDistributor[priceDistributorName]
    if priceDistributor and priceDistributor.Name() == priceDistributorName:
        PriceDistDlgObj.distributor = priceDistributorName
        PriceDistDlgObj.owner = priceDistributor.Owner()
        PriceDistDlgObj.protection = priceDistributor.Protection()
        set_price_dist_attributes(PriceDistDlgObj)
        PriceDistDlgObj.SetState(States.PDSelected)
    else:
        PriceDistDlgObj.SetState(States.PDChanged)

def update_price_distributor(PriceDistDlg, price_dist_obj):
    """updates Price Distributor attributes"""

    price_dist_obj.Name = PriceDistDlg.price_dist.GetData()
    price_dist_obj.Service = Utils.BlankToNone(PriceDistDlg.service.GetData())
    price_dist_obj.SemanticSeqNbr(PriceDistDlg.semantic.GetData())

    startTime = PriceDistDlg.start_time.GetData()
    if startTime and startTime != -1:
        try:
            Utils.ValidateTime(startTime)
        except ValueError as e:
            msg = 'Invalid Start Time. \n'
            e.args = (msg + str(e.args[0]),)
            raise
        price_dist_obj.StartTime = Utils.TimeToInt(startTime)
    else:
        price_dist_obj.StartTime = 0

    stopTime = PriceDistDlg.stop_time.GetData()
    if stopTime and stopTime != -1:
        try:
            Utils.ValidateTime(stopTime)
        except ValueError as e:
            msg = 'Invalid Stop Time. \n'
            e.args = (msg + str(e.args[0]),)
            raise
        price_dist_obj.StopTime = Utils.TimeToInt(stopTime)
    else:
        price_dist_obj.StopTime = 0

    if PriceDistDlg.distributor_type.GetData():
        price_dist_obj.DistributorType = PriceDistDlg.distributor_type.GetData()
    else:
        price_dist_obj.DistributorType = 'None'

    price_dist_obj.UseEntitlement = PriceDistDlg.use_entitlement.Checked()
    price_dist_obj.UseUtcOffset   = PriceDistDlg.use_utc_offset.Checked()

    utcTime = PriceDistDlg.utc_offset.GetData()
    if utcTime:
        Utils.ValidateUTCTime(utcTime)
        price_dist_obj.UtcOffset = Utils.UTCTimeToInt(utcTime)
    else:
        price_dist_obj.UtcOffset = ''

    updateInterval = PriceDistDlg.update_interval.GetData()
    if updateInterval and updateInterval != '-1':
        if not Utils.isfloat(updateInterval):
            message = "Invalid update interval. \n"\
            + "Enter time in sec or in millisecond or '-1' to disable the Update Interval!"
            raise ValueError(message)
        price_dist_obj.UpdateInterval = updateInterval
    else:
        price_dist_obj.UpdateInterval = '-1'

    price_dist_obj.IsDelayed = PriceDistDlg.is_delayed.Checked()
    price_dist_obj.LastFollowInterval = PriceDistDlg.last_follow_interval.Checked()
    price_dist_obj.IgnoreClearPrice = PriceDistDlg.ignore_clear_price.Checked()
    price_dist_obj.DiscardZeroPrice = PriceDistDlg.discard_zero_price.Checked()
    price_dist_obj.DiscardZeroQuantity = PriceDistDlg.discard_zero_quantity.Checked()
    price_dist_obj.DiscardNegativePrice = PriceDistDlg.discard_negative_price.Checked()
    price_dist_obj.ForceUpdate = PriceDistDlg.force_update.Checked()
    price_dist_obj.XmlData = PriceDistDlg.xml_data.GetData()

    price_dist_obj.DonotResetFields = PriceDistDlg.GetResetFields()
    price_dist_obj.Owner = PriceDistDlg.owner
    price_dist_obj.Protection = PriceDistDlg.protection
    return price_dist_obj

def set_price_dist_attributes(obj):
    """sets attributes of distributor"""
    price_dist_name = obj.price_dist.GetData()
    if not price_dist_name:
        return False

    obj.price_dist.SetData(price_dist_name)
    price_dist_obj = acm.FPriceDistributor[price_dist_name]
    if not price_dist_obj:
        return False

    distributorType = price_dist_obj.DistributorType()
    SetInfoByDistributorType(obj, price_dist_obj, distributorType)

    if price_dist_obj.StartTime() or price_dist_obj.StartTime() == 0:
        time_hm_start = Utils.IntToTime(price_dist_obj.StartTime())
        obj.start_time.SetData(time_hm_start)
    if price_dist_obj.StopTime() or price_dist_obj.StopTime() == 0:
        time_hm_stop = Utils.IntToTime(price_dist_obj.StopTime())
        obj.stop_time.SetData(time_hm_stop)

    obj.use_entitlement.Checked(price_dist_obj.UseEntitlement())
    obj.use_utc_offset.Checked(price_dist_obj.UseUtcOffset())

    if obj.use_utc_offset.Checked():
        obj.utc_offset.Enabled(True)
        time_hm_utc = Utils.IntToUTCTime(price_dist_obj.UtcOffset())
        obj.utc_offset.SetData(time_hm_utc)
    else:
        obj.utc_offset.Enabled(False)
        obj.utc_offset.Clear()

    obj.update_interval.SetData(Utils.NegativeToBlank(price_dist_obj.UpdateInterval()))
    obj.is_delayed.Checked(price_dist_obj.IsDelayed())
    obj.ignore_clear_price.Checked(price_dist_obj.IgnoreClearPrice())
    obj.last_follow_interval.Checked(price_dist_obj.LastFollowInterval())
    obj.discard_zero_price.Checked(price_dist_obj.DiscardZeroPrice())
    obj.discard_zero_quantity.Checked(price_dist_obj.DiscardZeroQuantity())
    obj.discard_negative_price.Checked(price_dist_obj.DiscardNegativePrice())
    obj.force_update.Checked(price_dist_obj.ForceUpdate())
    obj.error_msg.SetData(price_dist_obj.ErrorMessage())
    obj.select_all.Clear()

    reset_fields_val = price_dist_obj.DonotResetFields()
    obj.SetResetFields(reset_fields_val)
    obj.xml_data.SetData(price_dist_obj.XmlData())

def SetInfoByDistributorType(obj, price_dist_obj, distributorType):
    if distributorType == "None" or not distributorType:
        obj.distributor_type.SetData('')
        return

    obj.service.Enabled(True)
    obj.semantic.Enabled(True)
    obj.force_reset.Enabled(True)
    
    if price_dist_obj:
        obj.service.SetData(price_dist_obj.Service())
        obj.semantic.SetData(price_dist_obj.SemanticSeqNbr())
    
    obj.distributor_type.SetData(distributorType)
    if distributorType == "MarketMap":
        obj.service.Enabled(False)
        obj.service.SetData("")

    elif distributorType == "AMS":
        obj.service.SetData("")
        obj.service.Enabled(False)
        obj.force_reset.Enabled(False)
        obj.force_reset.Checked(False)

    elif distributorType == "Open Price Feed":
        obj.service.SetData("")
        obj.service.Enabled(False)

def set_tooltip(obj):
    obj.price_dist.ToolTip(ToolTips.distributor)
    obj.semantic.ToolTip(ToolTips.semantic)
    obj.service.ToolTip(ToolTips.service)
    obj.start_time.ToolTip(ToolTips.start_time)
    obj.stop_time.ToolTip(ToolTips.stop_time)
    obj.distributor_type.ToolTip(ToolTips.distributor_type)
    obj.use_utc_offset.ToolTip(ToolTips.use_utc_offset)
    obj.use_entitlement.ToolTip(ToolTips.use_entitlement)
    obj.utc_offset.ToolTip(ToolTips.utc_offset)
    obj.update_interval.ToolTip(ToolTips.update_interval)
    obj.is_delayed.ToolTip(ToolTips.is_delayed)
    obj.ignore_clear_price.ToolTip(ToolTips.ignore_clear_price)
    obj.last_follow_interval.ToolTip(ToolTips.last_follow_interval)
    obj.discard_zero_price.ToolTip(ToolTips.discard_zero_price)
    obj.discard_zero_quantity.ToolTip(ToolTips.discard_zero_quantity)
    obj.discard_negative_price.ToolTip(ToolTips.discard_negative_price)
    obj.force_update.ToolTip(ToolTips.force_update)
    obj.xml_data.ToolTip(ToolTips.xml_data)
    obj.error_msg.ToolTip(ToolTips.error_msg)
    obj.select_all.ToolTip(ToolTips.select_all)
    obj.force_reset.ToolTip(ToolTips.force_reset)
    obj.bid.ToolTip(ToolTips.reset_bid)
    obj.ask.ToolTip(ToolTips.reset_ask)
    obj.bid_size.ToolTip(ToolTips.reset_bidsize)
    obj.ask_size.ToolTip(ToolTips.reset_asksize)
    obj.last.ToolTip(ToolTips.reset_last)
    obj.high.ToolTip(ToolTips.reset_high)
    obj.low.ToolTip(ToolTips.reset_low)
    obj.open.ToolTip(ToolTips.reset_open)
    obj.settle.ToolTip(ToolTips.reset_settle)
    obj.diff.ToolTip(ToolTips.reset_diff)
    obj.time_last.ToolTip(ToolTips.reset_timelast)
    obj.volume_last.ToolTip(ToolTips.reset_volumelast)
    obj.volume_number.ToolTip(ToolTips.reset_volumenumber)
    obj.available.ToolTip(ToolTips.reset_available)


"""***********************PriceSemanticsTableChangeHandler************************************"""
class PriceSemanticsTableChangeHandler:
    def __init__(self, parent):
        self.parent = parent

    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) in ('update', 'insert'):
            selectedSemantic = self.parent.semantic.GetData()
            self.parent.semantic.Populate(acm.FPriceSemantic.Select(''))
            self.parent.semantic.SetData(selectedSemantic)
            self.parent.SetCaption()

            if selectedSemantic:
               semanticErr = selectedSemantic.ErrorMessage()

               if semanticErr != "":
                   self.parent.colorBox.Visible(True)
                   self.parent.hyperlink.Visible(True)
                   self.parent.icon.Visible(True)
               else:
                   self.parent.colorBox.Visible(False)
                   self.parent.hyperlink.Visible(False)
                   self.parent.icon.Visible(False)
        elif str(aspect) == 'remove':
            if self.parent.semantic.ItemExists(param):
                self.parent.semantic.RemoveItem(param)

"""***********************PriceDistributorApplication************************************"""
class PriceDistributorApplication(PriceLinkApplication):

    def __init__(self):

        PriceLinkApplication.__init__(self)
        self.m_fuxDlg    = 0
        self.binder      = None
        self.price_dist  = ""
        self.disid       = ""
        self.disnbr      = ""
        self.is_dist_name_changed = False
        self.distributor = None
        self.tableName = 'PriceDistributor'
        self.state = States.PDOpened

        self.priceServicesChangeHandler = PriceServicesChangeHandler(self)
        self.priceSemanticsTableChangeHandler = PriceSemanticsTableChangeHandler(self)

    def SetPriceDistributor(self, priceDistributorName):
        """Set Price link specification application object"""
        self.distributor = priceDistributorName

    def InitControls(self):
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)

    def HandleSetContents(self, contents):
        if contents != None:
            if type(contents) == str:
                self.SetPriceDistributor(contents)

    def HandleRegisterCommands(self, builder):
        """Register all the commands and its parameters"""

        saveMenu = Menu.PriceDistributorEditPanelCommandsHandler(self, 'Save', OnSaveSelected).Instance
        saveNewMenu = Menu.PriceDistributorEditPanelCommandsHandler(self, 'Save New', OnSaveNewSelected).Instance
        deleteMenu = Menu.PriceDistributorEditPanelCommandsHandler(self, 'Delete', OnDeleteSelected).Instance
        clearMenu = Menu.PriceDistributorEditPanelCommandsHandler(self, 'Clear', OnClearSelected).Instance
        revertMenu = Menu.PriceDistributorEditPanelCommandsHandler(self, 'Revert', OnRevertSelected).Instance
    
        protectionMenu = Menu.PriceDistributorToolsPanelCommandsHandler(self, 'Protection', OnProtectionSelected).Instance
        timeStampsMenu = Menu.PriceDistributorToolsPanelCommandsHandler(self, 'Time Stamp', OnTimeStampsSelected).Instance

        ListOfSupportedCommands =\
        [#Name         , parent, Display Name  , tooltiptext                                 , accelerator, mnemonic, callback  , default
        ['Save', 'Edit', 'Save', 'Save selected Price distributor', 'Ctrl+S', 'S', saveMenu, False ],
        ['Save New', 'Edit', 'Save New', 'save as new Price distributor', 'Ctrl+N', 'N', saveNewMenu, False ],
        ['Delete', 'Edit', 'Delete', 'Delete the selected Price distributor', 'Ctrl+Delete', 'D', deleteMenu, False ],
        ['Clear', 'Edit', 'Clear', 'Clear all fields', 'Ctrl+Shift+C', 'C', clearMenu, False ],
        ['Revert', 'Edit', 'Revert', 'Revert unsaved changes', 'Ctrl+Z', 'Z', revertMenu, False ],
        ['Protection', 'Tools', 'Protection', 'Protection', 'Shift+P', 'P', protectionMenu, False ],
        ['Time Stamp', 'Tools', 'Time Stamp', 'Time Stamp', 'Shift+T', 'T', timeStampsMenu, False ],
        ]
        fileCommands = acm.FSet()
        fileCommands.Add('FileSave')
        fileCommands.Add('FileSaveNew')
        fileCommands.Add('FileDelete')
        builder.RegisterCommands(FUxCore.ConvertCommands(ListOfSupportedCommands), fileCommands)

    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileSave':
            OnSaveSelected(self, None)
        elif commandName == 'FileSaveNew':
            OnSaveNewSelected(self, None)
        elif commandName == 'FileDelete':
            OnDeleteSelected(self, None)

    def HandleStandardFileCommandEnabled(self, commandName):
        if commandName == 'FileSave':
            return bool((self.state & States.PDSelected) and (self.state & States.PDChanged))
        if commandName == 'FileSaveNew':
            return bool((self.state & States.PDSelected) or (self.state & States.PDChanged))
        return True

    def start_dialog(self):
        self.result= acm.UX().Dialogs().ShowCustomDialog(self.shell, \
            self.CreateLayout(), self)

    def PopulateData(self):
        """populates the default data in GUI fields"""
        # set focus on the distributor name field
        self.price_dist.SetFocus()
        self.populatePriceDistributorComboList()
        self.PopulateParametersData()
        self.PopulateResetFieldsData()
        self.DefaultData()

    def populatePriceDistributorComboList(self):
        for priceDistributor in acm.FPriceDistributor.Select(''):
            self.price_dist.AddItem(priceDistributor.Name())

    def DefaultData(self):
        """sets default data for fields"""
        set_tooltip(self)
        self.error_msg.Editable(False)
        self.utc_offset.Enabled(False)
        self.utc_offset.MaxTextLength(6)
        self.start_time.MaxTextLength(5)
        self.stop_time.MaxTextLength(5)
        self.update_interval.MaxTextLength(9)
        self.price_dist.SetData("")
        self.service.Enabled(True)
        self.semantic.Enabled(True)
        self.distributor_type.Enabled(True)

    def PopulateParametersData(self):
        """populates data in Parameters pane"""
        self.service.Populate(self.GetPriceServices())
        self.semantic.Populate(acm.FPriceSemantic.Select(''))
        for distributor in acm.FEnumeration['enum(PrincipalType)'].Enumerators().Sort():
            if distributor in DistributorTypes:
                self.distributor_type.AddItem(distributor)
        
    def PopulateResetFieldsData(self):
        #populates data in Reset Fields pane
        pass

    def GetAllControlsObectFromGUI(self):
        """Get control object from all the GUI fields"""
        self.GetTopLayoutControlsObject()
        self.GetParametersLayoutControlsobject()
        self.GetDetailsTabLayoutControlsobject()

    def CreateTopLayout(self):
        """Create top layout"""
        self.TopLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.TopLayoutBuilderObject.BeginVertBox('None')
        self.TopLayoutBuilderObject.    BeginVertBox('Invisible', '')
        self.TopLayoutBuilderObject.        BeginHorzBox('None')
        self.TopLayoutBuilderObject.            AddComboBox('distributor_name', 'Distributor', -1, -1, 'Default')
        self.TopLayoutBuilderObject.        EndBox()
        self.TopLayoutBuilderObject.    EndBox()
        self.TopLayoutBuilderObject.EndBox()

    def CreateParametersLayout(self):
        """Create the layout of all the main parameters"""
        self.ParametersLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.ParametersLayoutBuilderObject.BeginVertBox('None')
        self.ParametersLayoutBuilderObject.BeginHorzBox('None', None)

        self.ParametersLayoutBuilderObject.BeginVertBox('Invisible')

        self.ParametersLayoutBuilderObject.AddOption('distributor_type', 'Distributor Type', -1, -1, 'Default')
        self.ParametersLayoutBuilderObject.AddOption('semantic', 'Semantic', -1, -1, 'Default')
        self.ParametersLayoutBuilderObject.AddInput('start_time', 'Start Time (HH:MM)', -1)
        self.ParametersLayoutBuilderObject.AddInput('utc_offset', 'UTC Offset (%sHH:MM)' % SYMBOL_PLUSMINUS, -1)
        self.ParametersLayoutBuilderObject.AddInput('update_interval', 'Update Interval (Sec)', -1)

        self.ParametersLayoutBuilderObject.AddCheckbox('is_delayed', 'Is Delayed')
        self.ParametersLayoutBuilderObject.AddCheckbox('discard_zero_price', 'Discard Zero Price')
        self.ParametersLayoutBuilderObject.AddCheckbox('discard_negative_price', 'Discard Negative Price')
        self.ParametersLayoutBuilderObject.EndBox()

        self.ParametersLayoutBuilderObject.BeginVertBox('Invisible')
        self.ParametersLayoutBuilderObject.AddCheckbox('use_entitlement', 'Use Entitlement')
        self.ParametersLayoutBuilderObject.AddOption('service', 'Service', -1, -1, 'Default')
        self.ParametersLayoutBuilderObject.AddInput('stop_time', 'Stop Time (HH:MM)', -1)
        self.ParametersLayoutBuilderObject.AddCheckbox('use_utc_offset', 'Use UTC Offset')
        self.ParametersLayoutBuilderObject.AddCheckbox('ignore_clear_price', 'Ignore Clear Price')
        self.ParametersLayoutBuilderObject.AddCheckbox('last_follow_interval', 'Last Follow Interval')
        self.ParametersLayoutBuilderObject.AddCheckbox('discard_zero_quantity', 'Discard Zero Quantity')
        self.ParametersLayoutBuilderObject.AddCheckbox('force_update', 'Force Update')

        self.ParametersLayoutBuilderObject.EndBox()

        self.ParametersLayoutBuilderObject.EndBox()
        self.ParametersLayoutBuilderObject.BeginHorzBox('Invisible', None)
        self.ParametersLayoutBuilderObject.AddLabel('error_msg_lbl', 'Error Message:')
        self.ParametersLayoutBuilderObject.AddInput('err_msg', '', -1)
        self.ParametersLayoutBuilderObject.EndBox()
        self.ParametersLayoutBuilderObject.EndBox()

    def CreateDetailsTabLayout(self):
        """Create the Details layout builder object"""
        self.DetailsTabLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.DetailsTabLayoutBuilderObject.BeginVertBox('None')

        self.DetailsTabLayoutBuilderObject.  AddFill()

        self.DetailsTabLayoutBuilderObject.BeginHorzBox('None', None)
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.BeginVertBox('None')
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_select_all', 'Select All       ')
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_bid',
                                    'Reset Bid                             ')
        self.DetailsTabLayoutBuilderObject.   AddCheckbox('is_ask_size',
                                        'Reset Ask Size                    ')
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_low',
                                    'Reset Low                           ')
        self.DetailsTabLayoutBuilderObject.    AddCheckbox('is_diff',
                                    'Reset Diff                            ')
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_volume_number',
                                            'Reset Volume Number        ')
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.EndBox()


        self.DetailsTabLayoutBuilderObject.BeginVertBox('None')
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_force_reset', 'Force Reset')
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_ask',
                                                'Reset Ask                 ')
        self.DetailsTabLayoutBuilderObject.   AddCheckbox('is_last', 'Reset Last                ')
        self.DetailsTabLayoutBuilderObject.    AddCheckbox('is_open', 'Reset Open              ')
        self.DetailsTabLayoutBuilderObject.    AddCheckbox('is_time_last',
                                                    'Reset Time Last        ')
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_available', 'Reset Available')
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.EndBox()


        self.DetailsTabLayoutBuilderObject.BeginVertBox('None')
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.      AddCheckbox('is_bid_size', 'Reset Bid Size')
        self.DetailsTabLayoutBuilderObject.   AddCheckbox('is_high', 'Reset High')
        self.DetailsTabLayoutBuilderObject.    AddCheckbox('is_settle', 'Reset Settle')
        self.DetailsTabLayoutBuilderObject.    AddCheckbox('is_volume_last', 'Reset Volume Last')
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.EndBox()
        self.DetailsTabLayoutBuilderObject.  AddFill()
        self.DetailsTabLayoutBuilderObject.EndBox()

        self.DetailsTabLayoutBuilderObject.  AddFill()


        self.DetailsTabLayoutBuilderObject.BeginHorzBox('None', None)
        self.DetailsTabLayoutBuilderObject.      AddLabel('xml_data_lbl', 'XML Data:  ')
        self.DetailsTabLayoutBuilderObject.      AddText('xml_data', -1, 60, -1, -1)
        self.DetailsTabLayoutBuilderObject.EndBox()

        self.DetailsTabLayoutBuilderObject.EndBox()

    def GetTopLayoutControlsObject(self):
        self.price_dist  =  self.TopLayoutObject.GetControl("distributor_name")

    def GetParametersLayoutControlsobject(self):
        self.semantic         =  self.ParametersTabLayoutObject.GetControl("semantic")
        self.service          =  self.ParametersTabLayoutObject.GetControl("service")
        self.start_time       =  self.ParametersTabLayoutObject.GetControl("start_time")
        self.stop_time        =  self.ParametersTabLayoutObject.GetControl("stop_time")
        self.distributor_type =  self.ParametersTabLayoutObject.GetControl("distributor_type")
        self.use_entitlement  =  self.ParametersTabLayoutObject.GetControl("use_entitlement")
        self.utc_offset       =  self.ParametersTabLayoutObject.GetControl("utc_offset")
        self.use_utc_offset   =  self.ParametersTabLayoutObject.GetControl("use_utc_offset")
        self.update_interval  =  self.ParametersTabLayoutObject.GetControl("update_interval")
        self.is_delayed       =  self.ParametersTabLayoutObject.GetControl("is_delayed")
        self.ignore_clear_price     =  self.ParametersTabLayoutObject.GetControl("ignore_clear_price")
        self.last_follow_interval   =  \
                            self.ParametersTabLayoutObject.GetControl("last_follow_interval")
        self.discard_zero_price     =  \
                            self.ParametersTabLayoutObject.GetControl("discard_zero_price")
        self.discard_zero_quantity  =  \
                        self.ParametersTabLayoutObject.GetControl("discard_zero_quantity")
        self.discard_negative_price =  \
                        self.ParametersTabLayoutObject.GetControl("discard_negative_price")
        self.force_update    =  self.ParametersTabLayoutObject.GetControl("force_update")
        self.error_msg       =  self.ParametersTabLayoutObject.GetControl("err_msg")


    def GetDetailsTabLayoutControlsobject(self):
        self.select_all    =  self.DetailsTabLayoutObject.GetControl("is_select_all")
        self.force_reset   =  self.DetailsTabLayoutObject.GetControl("is_force_reset")
        self.bid           =  self.DetailsTabLayoutObject.GetControl("is_bid")
        self.ask           =  self.DetailsTabLayoutObject.GetControl("is_ask")
        self.bid_size      =  self.DetailsTabLayoutObject.GetControl("is_bid_size")
        self.ask_size      =  self.DetailsTabLayoutObject.GetControl("is_ask_size")
        self.last          =  self.DetailsTabLayoutObject.GetControl("is_last")
        self.high          =  self.DetailsTabLayoutObject.GetControl("is_high")
        self.low           =  self.DetailsTabLayoutObject.GetControl("is_low")
        self.open          =  self.DetailsTabLayoutObject.GetControl("is_open")
        self.settle        =  self.DetailsTabLayoutObject.GetControl("is_settle")
        self.diff          =  self.DetailsTabLayoutObject.GetControl("is_diff")
        self.time_last     =  self.DetailsTabLayoutObject.GetControl("is_time_last")
        self.volume_last   =  self.DetailsTabLayoutObject.GetControl("is_volume_last")
        self.volume_number =  self.DetailsTabLayoutObject.GetControl("is_volume_number")
        self.available     =  self.DetailsTabLayoutObject.GetControl("is_available")
        self.xml_data      =  self.DetailsTabLayoutObject.GetControl("xml_data")


    def RegisterCallbacksForControls(self):
        """Register callbacks for all the controls of Price defintion"""
        self.RegisterCallbacksForTopLayoutControls()
        self.RegisterCallbacksForParametersLayoutControls()
        self.RegisterCallbacksForDetailsTabLayoutControls()

    def RegisterCallbacksForTopLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        self.price_dist.AddCallback('Changed', OnPriceDistributorSelected, self)

    def RegisterCallbacksForParametersLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        for field in [self.use_entitlement, self.use_utc_offset,
                    self.discard_zero_price, self.discard_zero_quantity,
                    self.discard_negative_price,
                    self.force_update, self.select_all,
                    self.last_follow_interval, self.is_delayed,
                    self.ignore_clear_price]:
            field.AddCallback('Activate', OnAnyFieldSelected, self)

        for field in [self.semantic, self.service, self.start_time,
                    self.stop_time, self.distributor_type, self.utc_offset,
                    self.update_interval, self.xml_data]:
            field.AddCallback('Changed', OnAnyFieldSelected, self)

    def RegisterCallbacksForDetailsTabLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        self.select_all.AddCallback('Activate', OnSelectAllSelected, self)
        self.use_utc_offset.AddCallback('Activate', OnUseUTCOffset, self)
        self.distributor_type.AddCallback('Changed', OnDistTypeSelected, self)

        for chkbox in self.GetResetFieldsAsTuple():
            chkbox.AddCallback('Activate', CB.OnCheckBoxSelected, self)
            chkbox.AddCallback('Activate', OnAnyFieldSelected, self)


    def InitAllcontrolsAndRegisterCallBacks(self):
        """1). Get control object from all the GUI fields\
           2). Register callbacks for each the controls"""
        self.GetAllControlsObectFromGUI()
        self.RegisterCallbacksForControls()

    def CreateLayout(self):
        """Create complete layout of price distributor"""
        self.CreateTopLayout()
        self.CreateParametersLayout()
        self.CreateDetailsTabLayout()

    def InitControls(self):
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)

    def HandleCreate( self, creationContext):
        self.CreateLayout()
        self.InitControls()
        self.TopLayoutObject = creationContext.AddPane(self.TopLayoutBuilderObject, "TOP_PANE")
        self.TopLayoutObject.SetLayout(self.TopLayoutBuilderObject, "TOP_PANE")

        parametersTabLayoutContext = creationContext.AddTabControlPane("PARAMETERS_PANE")
        self.ParametersTabLayoutObject = parametersTabLayoutContext.AddLayoutPage\
                                               (self.ParametersLayoutBuilderObject, "Parameters")

        self.DetailsTabLayoutObject = parametersTabLayoutContext.AddLayoutPage\
                                                     (self.DetailsTabLayoutBuilderObject, "Details")

        self.InitAllcontrolsAndRegisterCallBacks()
        self.PopulateData()
        self.addSubscriptionOnPDtable()

        if self.distributor:
            self.price_dist.SetData(self.distributor)
            OnPriceDistributorSelected(self, None)

    def SetState(self, state):
        self.state = self.state | state
        if state == States.PDOpened:
            self.state = state
        elif state == States.PDSelected:
            self.state = self.state & ~States.PDChanged

    def GetState(self):
        return self.state

    def addSubscriptionOnPDtable(self):
        '''Adding subscription on FChoiceList Table'''
        try:
            acm.FChoiceList.Select('list="PriceServices"').AddDependent(self.priceServicesChangeHandler)
            acm.FPriceSemantic.Select('').AddDependent(self.priceSemanticsTableChangeHandler)
        except Exception as extraInfo:
            print('Exception:' + str(extraInfo))

    def removeSubscriptionOnPDtable(self):
        '''Removing subscription on FChoiceList Table'''
        try:
            acm.FChoiceList.Select('list="PriceServices"').RemoveDependent(self.priceServicesChangeHandler)
            acm.FPriceSemantic.Select('').RemoveDependent(self.priceSemanticsTableChangeHandler)
        except Exception as extraInfo:
            print(str(extraInfo))

    def SetCaption(self, caption = ""):
        """Set the caption for the Price Distributor Dialog"""
        self.SetContentCaption(caption)

    def HasUnsavedChanges(self):
        return bool(self.state & States.PDChanged)

    def HandleApply(self):
        """validates the dialog"""
        if self.HasUnsavedChanges():
            choice = self.ShowTableModifiedDialog()
            if choice == ButtonOptions.CANCEL:
                return False
        return True

    def SetForceResetForAMSDistributor(self):
        if self.distributor_type.GetData() == "AMS":
            self.force_reset.Enabled(False)
            self.force_reset.Checked(False)

    def HandleDestroy(self):
        """closes the dialog"""
        self.binder.RemoveDependent(self)
        self.removeSubscriptionOnPDtable()

    def HandleClose(self):
        """closes the dialog"""
        if self.HasUnsavedChanges():
            choice = self.ShowTableModifiedDialog()
            if choice == ButtonOptions.CANCEL:
                return False
        return True

#*******************************APPLICATION HANDLERS*********************#
def GetApplicationObject():
    """Returns application object"""
    myNewAppInstance = PriceDistributorApplication()
    return myNewAppInstance

def OpenPriceDistributorApplication(priceDistributorName = ''):
    """Opens Price Link Specification Dialog"""
    try:
        acm.UX().SessionManager().StartApplication(APPLICATION_NAME, priceDistributorName)
    except RuntimeError as extraInfo:
        print(str(extraInfo))
        raise extraInfo
