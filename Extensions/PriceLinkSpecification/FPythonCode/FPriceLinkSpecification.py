""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkSpecification.py"
from __future__ import print_function
"""--------------------------------------------------------------------
MODULE

    PriceLinkSpecification - creates a Price Link Specification GUI

DESCRIPTION

    This script creates the Price Link Specification GUI using FAUx.
    It displays Price Links present in the database for selected
    distributor. It displays attributes of the selected Price Link.
    It also enables the updating, adding and removing of Price Links.

--------------------------------------------------------------------"""

import acm
import ael
import FUxCore

import time
from time import gmtime, strftime

import FPriceLinkApplication as CB
from FPriceLinkApplication import PriceLinkApplication
from FPriceLinkApplication import PriceServicesChangeHandler

import FPriceDistributor as PriceDistributorApplication
import FPriceSemantic as PriceSemanticApplication
import FPriceLinkMenu as Menu
import FTimeStampsCustomDialog as TimeStampsDialog
import FProtectionCustomDialog as ProtectionDialog
import FPriceLinkToolTips as ToolTips
import FPriceLinkSpecificationUtils as Utils

from FPriceLinkApplicationStates import PriceLinkSpecificationStates as States
from FPriceLinkSpecificationUtils import ButtonOptions
from FPriceLinkDefinitionListHandler import PriceLinkDefinitionListHandler as PLDListHandler
from FPriceLinkApplicationStates import MandatoryColumns
from FPriceLinkApplicationStates import AvailableColumns
from FPriceLinkApplicationStates import CurrentColumns


APPLICATION_NAME    = "PriceLinkSpecification"

def OnColumnSettingsSelected(PriceLinkDlg, arg):

    allPLDs = []
    root = PriceLinkDlg.pld_list.GetRootItem()
    for child in root.Children():
      pld = PriceLinkDlg.pldList.GetPLDObject(child)
      allPLDs.append(pld)


    currentItems = acm.FArray()

    for column in CurrentColumns:
        currentItems.Add(column)
        #CurrentColumns.append(column)

    selectedItems = acm.UX().Dialogs().SelectSubset(PriceLinkDlg.Shell(), AvailableColumns, 'Select Columns', True, currentItems)
    if selectedItems != None:
        idx = 0
        while idx < len(CurrentColumns):
            PriceLinkDlg.pld_list.RemoveColumn(len(MandatoryColumns)+idx)
            CurrentColumns.remove(CurrentColumns[idx])
            
        for selItem in selectedItems:
            if selItem not in CurrentColumns:
                PriceLinkDlg.pld_list.AddColumn(selItem, -1, selItem)
                CurrentColumns.append(selItem)

        PriceLinkDlg.pld_list.Clear()
        PriceLinkDlg.pldList.Populate(allPLDs)
        PriceLinkDlg.SetState(States.PLDPopulated)
        PriceLinkDlg.pldList.SetCountCol(len(CurrentColumns)+len(MandatoryColumns)+1)
        PriceLinkDlg.pldList.AdjustColumnWidth()


def AddColumnsToGrid(PriceLinkDlg, columns):
    for column in columns:
        if column not in CurrentColumns:
           PriceLinkDlg.pld_list.AddColumn(column, -1, column)
           CurrentColumns.append(column)

def GetPLDFromDB(priceDistributor):
    return acm.FPriceLinkDefinition.Select('priceDistributor=%s' %(priceDistributor.Name()))


def OnInsertItemsSelected(PriceLinkDlg, arg):

    pldList = PriceLinkDlg.SelectObjectsInsertItems()

    if not pldList:
        return

    if pldList[0].IsKindOf('FPriceLinkDefinition'):

        if PriceLinkDlg.priceDistributor:
            for pld in pldList:
                clone = pld.Clone()
                clone.PriceDistributor = PriceLinkDlg.priceDistributor
                PriceLinkDlg.pldList.Add(clone)

            PriceLinkDlg.price_distributor.SetData(PriceLinkDlg.priceDistributor)
            PriceLinkDlg.SetState(States.PLDAdded)

        else:
            PriceLinkDlg.pldList.Populate(pldList)
            PriceLinkDlg.SetState(States.PLDPopulated)

    else:
        if PriceLinkDlg.priceDistributor:
            for pld in pldList:
                pld_obj = acm.FPriceLinkDefinition()
                pld_obj.PriceDistributor = PriceLinkDlg.priceDistributor
                pld_obj.Instrument = pld.Instrument()
                pld_obj.Currency = pld.Currency()
                pld_obj.MultiplicationFactor(1.0)
                pld_obj.UpdateInterval(-1)
                PriceLinkDlg.pldList.Add(pld_obj)

            PriceLinkDlg.price_distributor.SetData(PriceLinkDlg.priceDistributor)

        else:
            for pld in pldList:
                pld_obj = acm.FPriceLinkDefinition()
                pld_obj.Instrument = pld.Instrument()
                pld_obj.Currency = pld.Currency()
                pld_obj.MultiplicationFactor(1.0)
                pld_obj.UpdateInterval(-1)
                PriceLinkDlg.pldList.Add(pld_obj)

def SetIDPLabel(PriceLinkDlg, priceDistributor):
    idp_lbl_dict = {"Bloomberg":"Ticker", "Reuters":"RIC", "MarketMap":"Alpha Code", "AMS":"Market Code"}
    idp_lbl = idp_lbl_dict.get(priceDistributor.DistributorType(), 'Market Code')
    PriceLinkDlg.idp_code.Label(idp_lbl)

def OnListSelectionChanged(PriceLinkDlg, arg):
    rows = PriceLinkDlg.pldList.GetSelectedRows()
    if not rows:
        clear_fields(PriceLinkDlg)
        PriceLinkDlg.priceDistributor = PriceLinkDlg.price_distributor.GetData()
        return

    if PriceLinkDlg.pldList.IsMultiSelect():
        clear_fields(PriceLinkDlg)
        PriceLinkDlg.SetState(States.PLDMultiSelected)
    else:
        row = rows[0]
        pld = PriceLinkDlg.pldList.GetPLDObject(row)
        clear_fields(PriceLinkDlg)
        PriceLinkDlg.priceDistributor = PriceLinkDlg.price_distributor.GetData()
        set_pld_attributes(PriceLinkDlg, pld)

        if pld.PriceDistributor():
            SetIDPLabel(PriceLinkDlg, pld.PriceDistributor())

        PriceLinkDlg.SetState(States.PLDSelected)

    for aRow in rows:
        opType = PriceLinkDlg.pldList.GetOperationType(aRow)
        if opType in ["U", "R"]:
            PriceLinkDlg.SetState(States.PLDUpdated)
        elif opType == 'A':
            PriceLinkDlg.SetState(States.PLDAdded)

def set_pld_attributes(PriceLinkDlg, pld):
    """sets values of Price link fields in GUI"""
    if not pld:
        return

    PriceLinkDlg.instrument.Clear()
    PriceLinkDlg.instrument.AddItem(pld.Instrument().Name())
    PriceLinkDlg.instrument.SetData(pld.Instrument().Name())
    PriceLinkDlg.ins_curr.SetData(pld.Currency())
    PriceLinkDlg.market.SetData(pld.Market())

    if pld.PriceDistributor():
        PriceLinkDlg.price_distributor.SetData(pld.PriceDistributor())
        PriceLinkDlg.priceDistributor = pld.PriceDistributor()

    #Set attributes on Prameters Pane
    PriceLinkDlg.idp_code.SetData(pld.IdpCode())
    PriceLinkDlg.inactive.Checked(pld.NotActive())

    SetServiceAndSemantic(PriceLinkDlg, pld)

    startTime = pld.StartTime()
    #if Utils.NegativeToBlank(startTime) or Utils.ZeroToBlank(startTime):
    time_hm_start = Utils.IntToTime(startTime)
    PriceLinkDlg.start_time.SetData(time_hm_start)

    stopTime = pld.StopTime()
    #if Utils.NegativeToBlank(stopTime) or Utils.ZeroToBlank(startTime):
    time_hm_stop = Utils.IntToTime(stopTime)
    PriceLinkDlg.stop_time.SetData(time_hm_stop)

    if startTime or stopTime:
        PriceLinkDlg.start_time.Enabled(True)
        PriceLinkDlg.stop_time.Enabled(True)
        PriceLinkDlg.m_IsContinuousSubscription.Checked(False)
    else:
        PriceLinkDlg.m_IsContinuousSubscription.Checked(True)
        PriceLinkDlg.start_time.Enabled(False)
        PriceLinkDlg.stop_time.Enabled(False)

    PriceLinkDlg.update_interval.SetData(Utils.NegativeToBlank(pld.UpdateInterval()))
    PriceLinkDlg.addition_addend.SetData(Utils.ZeroToBlank(pld.AdditionAddend()))
    PriceLinkDlg.multiplication_factor.SetData(Utils.OneToBlank(pld.MultiplicationFactor()))
    PriceLinkDlg.last_follow_interval.Checked(pld.LastFollowInterval())

    PriceLinkDlg.discard_zero_price.SetData(Utils.NoneToBlank(pld.DiscardZeroPrice()))
    PriceLinkDlg.discard_zero_quantity.SetData(Utils.NoneToBlank(pld.DiscardZeroQuantity()))
    PriceLinkDlg.discard_negative_price.SetData(Utils.NoneToBlank(pld.DiscardNegativePrice()))
    PriceLinkDlg.is_delayed.SetData(Utils.NoneToBlank(pld.IsDelayed()))
    PriceLinkDlg.ignore_clear_price.SetData(Utils.NoneToBlank(pld.IgnoreClearPrice()))
    PriceLinkDlg.force_update.SetData(Utils.NoneToBlank(pld.ForceUpdate()))

    PriceLinkDlg.error_msg.SetData(pld.ErrorMessage())

    PriceLinkDlg.log_price.Checked(pld.LogPrice())
    SetDetailsPane(PriceLinkDlg, pld)
    PriceLinkDlg.xml_data.SetData(pld.XmlData())
    PriceLinkDlg.protection = pld.Protection()
    PriceLinkDlg.owner = pld.Owner()

def SetServiceAndSemantic(Dlg, pld):
    priceDistributor = Dlg.price_distributor.GetData()
    if priceDistributor:
        distributorType = priceDistributor.DistributorType()
        defaultSetting = (True, '', True, None)

        if distributorType  == "MarketMap":
            defaultSetting = (False, '', True, pld.SemanticSeqNbr())
        elif distributorType in ('Bloomberg', 'Reuters'):
            defaultSetting = (True, pld.Service(), True, pld.SemanticSeqNbr())
        elif distributorType == "AMS":
            defaultSetting = (False, '', True, pld.SemanticSeqNbr())
        elif distributorType == "Open Price Feed":
            defaultSetting = (False, '', True, pld.SemanticSeqNbr())

        Dlg.service.Enabled(defaultSetting[0])
        Dlg.service.SetData(defaultSetting[1])
        Dlg.semantic.Enabled(defaultSetting[2])
        Dlg.semantic.SetData(defaultSetting[3])

def SetDetailsPane(Dlg, pld):
    if pld.DonotResetFields() == -1:
        #-1 represents default settings
        Dlg.default_settings.Checked(True)
        OnDefaultSettingsSelected(Dlg, None)
    else:
        Dlg.default_settings.Checked(False)
        Dlg.EnableAllResetFields()
        Dlg.SetResetFields(pld.DonotResetFields())
        Dlg.SetForceResetForAMSDistributor()

def clear_fields(PriceLinkDlg):
    PriceLinkDlg.instrument.Clear()
    PriceLinkDlg.instrument.Enabled(True)
    PriceLinkDlg.ins_curr.SetData("")
    PriceLinkDlg.ins_curr.Enabled(True)
    PriceLinkDlg.price_distributor.SetData("")
    PriceLinkDlg.price_distributor.Enabled(True)
    PriceLinkDlg.market.SetData("")
    PriceLinkDlg.market.Enabled(True)


    #Set attributes on Prameters Pane
    PriceLinkDlg.idp_code.Clear()
    PriceLinkDlg.inactive.Clear()
    PriceLinkDlg.service.SetData("")
    PriceLinkDlg.semantic.SetData("")
    PriceLinkDlg.start_time.Clear()
    PriceLinkDlg.stop_time.Clear()
    PriceLinkDlg.start_time.Enabled(True)
    PriceLinkDlg.stop_time.Enabled(True)
    PriceLinkDlg.m_IsContinuousSubscription.Clear()
    PriceLinkDlg.update_interval.Clear()
    PriceLinkDlg.last_follow_interval.Clear()
    PriceLinkDlg.discard_zero_price.SetData("")
    PriceLinkDlg.discard_zero_quantity.SetData("")
    PriceLinkDlg.discard_negative_price.SetData("")
    PriceLinkDlg.is_delayed.SetData("")
    PriceLinkDlg.ignore_clear_price.SetData("")
    PriceLinkDlg.force_update.SetData("")
    PriceLinkDlg.addition_addend.Clear()
    PriceLinkDlg.multiplication_factor.Clear()
    PriceLinkDlg.error_msg.Clear()
    PriceLinkDlg.log_price.Clear()

    #Set attributes on Details Pane
    PriceLinkDlg.select_all.Clear()
    PriceLinkDlg.select_all.Enabled(False)
    PriceLinkDlg.force_reset.Clear()
    PriceLinkDlg.force_reset.Enabled(False)
    PriceLinkDlg.default_settings.Checked(True)
    PriceLinkDlg.UnCheckAllResetFields()
    PriceLinkDlg.DisableAllResetFields()
    PriceLinkDlg.xml_data.SetData("")

    PriceLinkDlg.SetState(States.PLDPopulated)

def OnDescendSelected(PriceLinkDlg, arg):
    OnSortBySelected(PriceLinkDlg, arg)

def OnSortBySelected(PriceLinkDlg, arg):
    PriceLinkDlg.pldList.Sort(PriceLinkDlg.sort_by, PriceLinkDlg.isDescending)
    clear_fields(PriceLinkDlg)

def OnOpenPriceEntrySelected(PriceLinkDlg, arg):
    pld = PriceLinkDlg.pldList.GetSelectedPLD()
    if pld != None:
        acm.UX().SessionManager().StartApplication('Price Entry', pld.Instrument())

def OnOpenInstrumentSelected(PriceLinkDlg, arg):
    pld = PriceLinkDlg.pldList.GetSelectedPLD()
    if pld != None:
        acm.UX().SessionManager().StartApplication('', pld.Instrument())

def OnOpenPartyDefinitionSelected(PriceLinkDlg, arg):
    pld = PriceLinkDlg.pldList.GetSelectedPLD()
    if pld != None:
        acm.UX().SessionManager().StartApplication('Party Definition', pld.Market())


def OnFetchSelected(PriceLinkDlg, arg):
    instrumentList = PriceLinkDlg.SelectObjectsInsertInstruments()

    if not instrumentList:
        return

    PriceLinkDlg.instrument.Clear()
    PriceLinkDlg.instrument.AddItem(instrumentList[0])
    PriceLinkDlg.instrument.SetData(instrumentList[0])
    PriceLinkDlg.ins_curr.SetData(instrumentList[0].Currency())
    PriceLinkDlg.SetState(States.PLDChanged)


def OnInstrumentSelected(PriceLinkDlg, arg):
    if PriceLinkDlg.instrument.GetData():
        PriceLinkDlg.SetState(States.PLDChanged)
        instrumentObject = acm.FInstrument[PriceLinkDlg.instrument.GetData()]
        if instrumentObject:
            PriceLinkDlg.ins_curr.SetData(instrumentObject.Currency())
        else:
            message = 'Instrument <'+ PriceLinkDlg.instrument.GetData() + '> is not found. Please correct the instrument name and try again!'
            shell = PriceLinkDlg.Shell()
            acm.UX().Dialogs().MessageBox(shell, 'Error', message, 'Ok',  '', '', 'None', 'None')

def OnInstrumentChanged(PriceLinkDlg, arg):
    if PriceLinkDlg.instrument.GetData():
        PriceLinkDlg.SetState(States.PLDChanged)
        instrumentObject = acm.FInstrument[PriceLinkDlg.instrument.GetData()]
        if instrumentObject:
            PriceLinkDlg.ins_curr.SetData(instrumentObject.Currency())


def OnPriceDistributorChanged(PriceLinkDlg, arg):
    if PriceLinkDlg.price_distributor.GetData():
        PriceLinkDlg.SetState(States.PLDChanged)
        distributorObject = PriceLinkDlg.price_distributor.GetData()
        if distributorObject:
            PriceLinkDlg.price_distributor.SetData(distributorObject)
            PriceLinkDlg.priceDistributor = distributorObject

def OnPriceSemanticChanged(PriceLinkDlg, arg):
    if PriceLinkDlg.semantic.GetData():
        PriceLinkDlg.SetState(States.PLDChanged)
        semanticObject = PriceLinkDlg.semantic.GetData()
        if semanticObject:
            PriceLinkDlg.semantic.SetData(semanticObject)

def OnTimeStampsSelected(PriceLinkDlg, arg):
    pld = PriceLinkDlg.pldList.GetSelectedPLD()
    TimeStampsDialog.StartDialog(PriceLinkDlg.Shell(), pld)

def OnProtectionSelected(PriceLinkDlg, arg):
    oldOwner = PriceLinkDlg.owner
    oldProtection = PriceLinkDlg.protection
    shell = PriceLinkDlg.Shell()
    newOwner, newProtection = ProtectionDialog.StartDialog(shell, oldOwner, oldProtection)
    if (oldOwner.Name() != newOwner.Name()) or (oldProtection != newProtection):
        PriceLinkDlg.owner = newOwner
        PriceLinkDlg.protection = newProtection
        OnAnyFieldSelected(PriceLinkDlg, arg)

def OnDefaultSettingsSelected(PriceLinkDlg, arg):
    if PriceLinkDlg.default_settings.Checked():
        PriceLinkDlg.DisableAllResetFields()
        PriceLinkDlg.UnCheckAllResetFields()
    else:
        PriceLinkDlg.EnableAllResetFields()
        PriceLinkDlg.SetForceResetForAMSDistributor()

def OnSelectAllSelected(PriceLinkDlg, arg):
    if PriceLinkDlg.select_all.Checked():
        PriceLinkDlg.CheckAllResetFields()
        PriceLinkDlg.SetForceResetForAMSDistributor()
    else:
        PriceLinkDlg.UnCheckAllResetFields()

def OnDistSettingsSelected(PriceLinkDlg, arg):
    priceDistributorName = ''
    if PriceLinkDlg.price_distributor.GetData():
        priceDistributorName = PriceLinkDlg.price_distributor.GetData().Name()
    PriceDistributorApplication.OpenPriceDistributorApplication(priceDistributorName)

def OnSemanticSettingsSelected(PriceLinkDlg, arg):
    priceSemanticName = ''
    if PriceLinkDlg.semantic.GetData():
        priceSemanticName = PriceLinkDlg.semantic.GetData().Name()
        
    PriceSemanticApplication.OpenPriceSemanticApplication(priceSemanticName)
	
def ValidateMandatoryFields(values):
    mandatoryFields = ('PriceDistributor', 'Instrument', 'Currency', 'Market', 'IdpCode')
    missingFields = []

    for field in mandatoryFields:
        if not values[field]:
            if field == 'IdpCode':
                field = values['IdpCodeLabel']
            missingFields.append(field)

    if missingFields:
        missingFields = '\n\t'.join(missingFields)
        message = 'This price link definition is invalid. \n' +\
                'Please select the following and try again: \n\t' + missingFields
        raise ValueError(message)

def OnAddSelected(PriceLinkDlg, arg):
    try:
        if PriceLinkDlg.instrument.GetData():
            instrumentObject = acm.FInstrument[PriceLinkDlg.instrument.GetData()]
            if not instrumentObject:
                message = 'Instrument <' + PriceLinkDlg.instrument.GetData() + '> is not found. Please correct the instrument name and try again!'
                shell = PriceLinkDlg.Shell()
                acm.UX().Dialogs().MessageBox(shell, 'Error', message, 'Ok',  '', '', 'None', 'None')
                return

        if PriceLinkDlg.pldList.IsMultiSelect():
            AddMultiSelect(PriceLinkDlg)
        else:
            AddSingleSelect(PriceLinkDlg)

        PriceLinkDlg.SetState(States.PLDAdded)
    except ValueError as e:
        PriceLinkDlg.ShowError(str(e))

def AddMultiSelect(PriceLinkDlg):
    values = PriceLinkDlg.GetAttributeValues()
    values['Protection']            =  acm.FPriceLinkDefinition().Protection()
    ValidateAttributeValues(values)
    selectedPLDs = PriceLinkDlg.pldList.GetSelectedPLDs()
    PriceLinkDlg.pldList.SelectAllItems(False)
    for pld in selectedPLDs:
        clone = pld.Clone()
        ApplyPartialUpdate(values, clone)
        PriceLinkDlg.pldList.Add(clone)

def AddSingleSelect(PriceLinkDlg):
    values = PriceLinkDlg.GetAttributeValues()
    values['Protection']            =  acm.FPriceLinkDefinition().Protection()
    ValidateMandatoryFields(values)
    ValidateAttributeValues(values)

    pld = acm.FPriceLinkDefinition()
    ApplyFullUpdate(values, pld)
    PriceLinkDlg.pldList.SelectAllItems(False)
    PriceLinkDlg.pldList.Add(pld)

def ValidateAttributeValues(values):
    Utils.ValidateStartTime(values['StartTime'])
    Utils.ValidateStopTime(values['StopTime'])
    Utils.ValidateUpdateInterval(values['UpdateInterval'])
    Utils.ValidateAdditionAddend(values['AdditionAddend'])
    Utils.ValidateMultiplicationFactor(values['MultiplicationFactor'])

def ApplyPartialUpdate(values, pld_obj):

    noValidationFields = ('Instrument', 'Currency', 'Market', 'IdpCode', 'PriceDistributor', 'NotActive',
        'Service', 'SemanticSeqNbr', 'LastFollowInterval', 'DiscardZeroPrice',
        'DiscardZeroQuantity', 'DiscardNegativePrice',
         'ForceUpdate', 'LogPrice', 'XmlData', 'IsDelayed', 'IgnoreClearPrice')

    for field in noValidationFields:
        if values[field]:
            getattr(pld_obj, field)(values[field])

    if not values['DefaultSettings']:
        pld_obj.DonotResetFields = values['DonotResetFields']

    startTime = values['StartTime']
    if startTime:
        pld_obj.StartTime = Utils.TimeToInt(startTime)

    stopTime = values['StopTime']
    if stopTime:
        pld_obj.StopTime = Utils.TimeToInt(stopTime)

    updateInterval = values['UpdateInterval']
    if updateInterval:
        pld_obj.UpdateInterval = updateInterval

    additionAddend = values['AdditionAddend']
    if additionAddend:
        pld_obj.AdditionAddend = float(additionAddend)


    multiplicationFactor = values['MultiplicationFactor']
    if multiplicationFactor:
        pld_obj.MultiplicationFactor = float(multiplicationFactor)

def ApplyFullUpdate(values, pld_obj):
    pld_obj.PriceDistributor = values['PriceDistributor']
    pld_obj.Instrument = values['Instrument']
    pld_obj.Currency = values['Currency']
    pld_obj.Market = values['Market']
    pld_obj.IdpCode = values['IdpCode']
    pld_obj.NotActive = values['NotActive']
    pld_obj.Service = Utils.BlankToNone(values['Service'])
    pld_obj.SemanticSeqNbr(Utils.BlankToNone(values['SemanticSeqNbr']))
    pld_obj.IsDelayed = Utils.ValidateBooleanValue(values['IsDelayed'])
    pld_obj.IgnoreClearPrice = Utils.ValidateBooleanValue(values['IgnoreClearPrice'])
    
    startTime = values['StartTime']
    pld_obj.StartTime = Utils.TimeToInt(startTime)

    stopTime = values['StopTime']
    pld_obj.StopTime = Utils.TimeToInt(stopTime)

    updateInterval = values['UpdateInterval']
    if updateInterval:
        pld_obj.UpdateInterval = updateInterval
    else:
        pld_obj.UpdateInterval = -1

    additionAddend = values['AdditionAddend']
    if additionAddend:
        pld_obj.AdditionAddend = float(additionAddend)
    else:
        pld_obj.AdditionAddend = 0

    multiplicationFactor = values['MultiplicationFactor']
    if multiplicationFactor:
        pld_obj.MultiplicationFactor = float(multiplicationFactor)
    else:
        pld_obj.MultiplicationFactor = 1

    pld_obj.LastFollowInterval = values['LastFollowInterval']
    pld_obj.DiscardZeroPrice = Utils.ValidateBooleanValue(values['DiscardZeroPrice'])
    pld_obj.DiscardZeroQuantity = Utils.ValidateBooleanValue(values['DiscardZeroQuantity'])
    pld_obj.DiscardNegativePrice = Utils.ValidateBooleanValue(values['DiscardNegativePrice'])
    pld_obj.ForceUpdate = Utils.ValidateBooleanValue(values['ForceUpdate'])
    pld_obj.LogPrice = values['LogPrice']
    if values['DefaultSettings']:
        pld_obj.DonotResetFields = -1
    else:
        pld_obj.DonotResetFields = values['DonotResetFields']

    pld_obj.XmlData = values['XmlData']
    pld_obj.Owner = values['Owner']
    pld_obj.Protection = values['Protection']


def GetPrice(insName, currName, marketName):
    ins = acm.FInstrument[insName]
    curr = acm.FCurrency[currName]
    market = acm.FParty[marketName]
    prices = ins.Prices()
    for p in prices:
        if p.Currency() == curr  and p.Market() == market:
            return p
    return None

def OnUpdateSelected(PriceLinkDlg, arg):
    try:

        if PriceLinkDlg.instrument.GetData():
            instrumentObject = acm.FInstrument[PriceLinkDlg.instrument.GetData()]
            if not instrumentObject:
                message = 'Instrument <' + PriceLinkDlg.instrument.GetData() + '> is not found. Please correct the instrument name and try again!'
                shell = PriceLinkDlg.Shell()
                acm.UX().Dialogs().MessageBox(shell, 'Error', message, 'Ok',  '', '', 'None', 'None')
                return

        values = PriceLinkDlg.GetAttributeValues()
        ValidateAttributeValues(values)

        if PriceLinkDlg.pldList.IsMultiSelect():
            UpdateMultiSelect(PriceLinkDlg, values)
        else:
            UpdateSingleSelect(PriceLinkDlg, values)

        PriceLinkDlg.SetState(States.PLDUpdated)
    except ValueError as e:
        PriceLinkDlg.ShowError(str(e))

def UpdateMultiSelect(PriceLinkDlg, values):
    selectedRows = PriceLinkDlg.pldList.GetSelectedRows()
    for row in selectedRows:
        pld = PriceLinkDlg.pldList.GetPLDObject(row)
        clone = pld.Clone()
        ApplyPartialUpdate(values, clone)

        operation = "U"
        if "A" == PriceLinkDlg.pldList.GetOperationType(row):
            operation = "A"

        PriceLinkDlg.pldList.Update(operation, clone, row)
        row.EnsureVisible()

def UpdateSingleSelect(PriceLinkDlg, values):
    ValidateMandatoryFields(values)
    row = PriceLinkDlg.pldList.GetSelectedRow()
    pld = PriceLinkDlg.pldList.GetPLDObject(row)
    clone = pld.Clone()
    ApplyFullUpdate(values, clone)

    operation = "U"
    if "A" == PriceLinkDlg.pldList.GetOperationType(row):
        operation = "A"

    PriceLinkDlg.pldList.Update(operation, clone, row)
    row.EnsureVisible()

def OnRemoveSelected(PriceLinkDlg, arg):
    PriceLinkDlg.pldList.Remove()
    PriceLinkDlg.SetState(States.PLDUpdated)

def OnClearSelected(PriceLinkDlg, arg):
    PriceLinkDlg.pldList.SelectAllItems(False)
    clear_fields(PriceLinkDlg)
    PriceLinkDlg.pld_list.Clear()
    PriceLinkDlg.priceDistributor = PriceLinkDlg.price_distributor.GetData()

def OnClearSelectionSelected(PriceLinkDlg, arg):
    PriceLinkDlg.pldList.SelectAllItems(False)
    clear_fields(PriceLinkDlg)
    PriceLinkDlg.priceDistributor = PriceLinkDlg.price_distributor.GetData()

def OnAnyFieldSelected(PriceLinkDlg, arg):
    PriceLinkDlg.SetState(States.PLDChanged)

def set_tooltip_pld(obj):
    obj.instrument.ToolTip(ToolTips.instrument)
    obj.instrument_fetch.ToolTip(ToolTips.instrument_fetch)
    obj.ins_curr.ToolTip(ToolTips.currency)
    obj.price_distributor.ToolTip(ToolTips.distributor)
    obj.market.ToolTip(ToolTips.market)
    obj.service.ToolTip(ToolTips.service)
    obj.semantic.ToolTip(ToolTips.semantic)
    obj.start_time.ToolTip(ToolTips.start_time_pld)
    obj.stop_time.ToolTip(ToolTips.stop_time_pld)
    obj.update_interval.ToolTip(ToolTips.update_interval_pld)
    obj.discard_zero_price.ToolTip(ToolTips.discard_zero_price_pld)
    obj.discard_zero_quantity.ToolTip(ToolTips.discard_zero_quantity_pld)
    obj.discard_negative_price.ToolTip(ToolTips.discard_negative_price_pld)
    obj.is_delayed.ToolTip(ToolTips.is_delayed_pld)
    obj.ignore_clear_price.ToolTip(ToolTips.ignore_clear_price_pld)
    obj.force_update.ToolTip(ToolTips.force_update_pld)
    obj.idp_code.ToolTip(ToolTips.idp_code)
    obj.inactive.ToolTip(ToolTips.not_active)
    obj.m_IsContinuousSubscription.ToolTip(ToolTips.contineous_subscription)
    obj.last_follow_interval.ToolTip(ToolTips.last_follow_interval_pld)
    obj.addition_addend.ToolTip(ToolTips.addition_addend)
    obj.multiplication_factor.ToolTip(ToolTips.multiplication_factor)
    obj.log_price.ToolTip(ToolTips.log_price)
    obj.xml_data.ToolTip(ToolTips.xml_data)
    obj.error_msg.ToolTip(ToolTips.error_msg)
    obj.default_settings.ToolTip(ToolTips.use_default_setting)
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

def OnContinuousSubscriptionClick(p_PriceLinkDlg, p_arg):
    if p_PriceLinkDlg.m_IsContinuousSubscription.Checked():
        p_PriceLinkDlg.start_time.SetData("00:00")
        p_PriceLinkDlg.start_time.Enabled(False)
        p_PriceLinkDlg.stop_time.SetData("00:00")
        p_PriceLinkDlg.stop_time.Enabled(False)
    else:
        p_PriceLinkDlg.start_time.Enabled(True)
        p_PriceLinkDlg.stop_time.Enabled(True)
        row = p_PriceLinkDlg.pldList.GetSelectedRow()
        if row:
            pld = p_PriceLinkDlg.pldList.GetPLDObject(row)
            time_hm_start = Utils.IntToTime(pld.StartTime())
            p_PriceLinkDlg.start_time.SetData(time_hm_start)
            time_hm_stop = Utils.IntToTime(pld.StopTime())
            p_PriceLinkDlg.stop_time.SetData(time_hm_stop)
        else:
            p_PriceLinkDlg.start_time.SetData("")
            p_PriceLinkDlg.stop_time.SetData("")

def OnHyperLinkClicked(PriceLinkDlg, arg):
    OnDistSettingsSelected(PriceLinkDlg, arg)

class PriceLinkSpecificationApplication(PriceLinkApplication):
    def __init__(self):
        PriceLinkApplication.__init__(self)
        self.binder               = None
        self.tableName = 'PriceLinkDefinition'
        self.priceDistributor = ""
        self.state = States.PLDOpen
        self.SavedColumns = []

        self.priceLinkDefinitionTableChangeHandler = PriceLinkDefinitionTableChangeHandler(self)
        self.priceServicesChangeHandler = PriceServicesChangeHandler(self)
        self.priceSemanticsTableChangeHandler = PriceSemanticsTableChangeHandler(self)
        self.priceDistributorTableChangeHandler = PriceDistributorTableChangeHandler(self)

    #Always use @FUxCore.aux_cb when executing code in an event handler to handle exceptions.
    @FUxCore.aux_cb
    def OnContextMenuCB(self, ud, dictionary):
        menuBuilder = dictionary.At('menuBuilder')

        openPriceEntryMenuContext = Menu.OpenPanelCommandsHandler(self, 'Price Entry', OnOpenPriceEntrySelected).Instance
        openInstrumentMenuContext = Menu.OpenPanelCommandsHandler(self, 'Instrument', OnOpenInstrumentSelected).Instance
        openPartyMenuContext = Menu.OpenPanelCommandsHandler(self, 'Party Definition', OnOpenPartyDefinitionSelected).Instance


        commands = [
                    ['Instrument', '', 'Open With/Instrument', '', '', '', openInstrumentMenuContext, False ],
                    ['PartyDefinition', '', 'Open With/Party', '', '', '', openPartyMenuContext, False ],
                    ['PriceEntry', '', 'Open With/Price Entry', '', '', '', openPriceEntryMenuContext, False ]
                   ]


        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def HandleSaveLayout(self, contents):
        ''' Override this function to handle the save layout callback '''
        contents.AtPut("plsListColumns", CurrentColumns)


    def HandleLoadLayout(self, contents):
        ''' Override this function to handle the load layout callback '''
        if contents != None:
            if contents.IsKindOf('FDictionary'):
                self.SavedColumns = contents.At('plsListColumns')

                if self.SavedColumns != None:
                    AddColumnsToGrid(self, self.SavedColumns)

    def HandleGetContents(self):
        dict = acm.FDictionary()
        dict.AtPut("plsListColumns", CurrentColumns)
        return dict

    def HandleSetContents(self, contents):
        if contents != None:
            if type(contents) == str:
                self.setPriceDefinitionName(contents)
            elif contents.IsKindOf('FDictionary'):
                self.SavedColumns = contents.At('plsListColumns')
            else:
                self.InstrumentName = contents.At('instrument')
                self.Currency = contents.At('currency')
                self.Market = contents.At('market')
                self.Distributor = contents.At('distributor')
                self.Code = contents.At('marketCode')


    def HandleRegisterCommands(self, builder):
        addMenu         = Menu.PriceLinkPanelCommandsHandler(self, 'Add', OnAddSelected).Instance
        updateMenu      = Menu.PriceLinkPanelCommandsHandler(self, 'Update', OnUpdateSelected).Instance
        deleteMenu      = Menu.PriceLinkPanelCommandsHandler(self, 'Delete', OnRemoveSelected).Instance
        clearMenu       = Menu.PriceLinkPanelCommandsHandler(self, 'Clear', OnClearSelected).Instance
        clearSelectionMenu       = Menu.PriceLinkPanelCommandsHandler(self, 'Clear Selection', OnClearSelectionSelected).Instance
        saveMenu        = Menu.PriceLinkPanelCommandsHandler(self, 'Save', PriceLinkSpecificationApplication.OnSaveSelected).Instance
        saveAllMenu     = Menu.PriceLinkPanelCommandsHandler(self, 'Save All', PriceLinkSpecificationApplication.OnSaveAllSelected).Instance
        revertMenu      = Menu.PriceLinkPanelCommandsHandler(self, 'Revert', PriceLinkSpecificationApplication.OnRevert).Instance
        revertAllMenu   = Menu.PriceLinkPanelCommandsHandler(self, 'Revert All', PriceLinkSpecificationApplication.OnRevertAll).Instance

        openPriceEntryMenu = Menu.OpenPanelCommandsHandler(self, 'Price Entry', OnOpenPriceEntrySelected).Instance
        openInstrumentMenu = Menu.OpenPanelCommandsHandler(self, 'Instrument', OnOpenInstrumentSelected).Instance
        openPartyMenu = Menu.OpenPanelCommandsHandler(self, 'Party Definition', OnOpenPartyDefinitionSelected).Instance

        protectionMenu = Menu.ToolsPanelCommandsHandler(self, 'Protection', OnProtectionSelected).Instance
        timeStampsMenu = Menu.ToolsPanelCommandsHandler(self, 'Time Stamps', OnTimeStampsSelected).Instance

        distributorSettingsMenu = Menu.DistributorSettingsPanelCommandsHandler(self, 'Distributor', OnDistSettingsSelected).Instance
        semanticSettingsMenu = Menu.SemanticSettingsPanelCommandsHandler(self, 'Semantic', OnSemanticSettingsSelected).Instance
        columnSettingsMenu = Menu.ColumnSettingsPanelCommandsHandler(self, 'Column', OnColumnSettingsSelected).Instance
        insertItemMenu  = Menu.InsertItemsPanelCommandsHandler(self, 'Insert Items', OnInsertItemsSelected).Instance

        ListOfSupportedCommands =\
        [#Name         , parent, Display Name  , tooltiptext                                        , accelerator, mnemonic, callback                , default
        #Price Link Panel Commands
        ['Add', 'Edit', 'Add', 'Adds a Price link to the selected distributor', 'Ctrl+N', 'N', addMenu, False ],
        ['Update', 'Edit', 'Update', 'Update the selected price link', 'Ctrl+U', 'U', updateMenu, False ],
        ['Delete', 'Edit', 'Delete', 'Remove the selected price link', 'Ctrl+Delete', 'X', deleteMenu, False ],
        ['Clear', 'Edit', 'Clear', 'Clear all fields', 'Ctrl+Shift+C', 'C', clearMenu, False ],
        ['Clear Selection', 'Edit', 'Clear Selection', 'Clear selected fields', 'Ctrl+Alt+C', 'A', clearSelectionMenu, False ],
        ['Save', 'Edit', 'Save', 'Save the selected price link', 'Ctrl+S', 'S', saveMenu, False ],
        ['Save All', 'Edit', 'Save All', 'Save All the price links', 'Ctrl+Shift+S', 'V', saveAllMenu, False ],
        ['Revert', 'Edit', 'Revert', 'Revert the selected price link', 'Ctrl+Z', 'R', revertMenu, False ],
        ['Revert All', 'Edit', 'Revert All', 'Revert All the price links Changes', 'Ctrl+Shift+Z', 'Z', revertAllMenu, False ],

        #Open Panel commands
        ['Price Entry', 'Tools', 'Open/Price Entry', 'Opens Price Entry window', 'Ctrl+Shift+P', 'P', openPriceEntryMenu, False ],
        ['Instrument', 'Tools', 'Open/Instrument', 'Opens Instrument window', 'Ctrl+Shift+T', 'T', openInstrumentMenu, False ],
        ['Party Definition', 'Tools', 'Open/Party', 'Opens Party Definition window', 'Ctrl+Shift+M', 'M', openPartyMenu, False ],
        #Version Panel Commands
        ['Protection', 'Special', 'Protection', 'Show the protection assigned to current user', 'Shift+P', 'Q', protectionMenu, False ],
        ['Time Stamps', 'Special', 'Time Stamps', 'Time stamp of the last changes made', 'Shift+T', 'W', timeStampsMenu, False ],
        # Distributor setting
        ['Distributor', 'Tools', 'Distributor/Distributor Setting', 'Opens the distributor settings window', 'Ctrl+Shift+D', 'D', distributorSettingsMenu, False ],
        # Column Settings
        ['Column', 'Tools', 'Columns', 'Opens the select column settings window to be Able to add or remove Columns', 'Ctrl+Shift+L', 'L', columnSettingsMenu, False ],
        # Semantic Settings
        ['Semantic', 'Tools', 'Semantic/Semantic Setting', 'Opens the semantic settings window', 'Alt+S', 'S', semanticSettingsMenu, False ],
        # Insert Items
        ['Insert Items', 'Tools', 'Insert/Insert Items', 'Insert a Price link or Instrument to the selected distributor', 'Ctrl+Shift+I', 'T', insertItemMenu, False ],
        ]

        fileCommands = acm.FSet()
        fileCommands.Add('FileSave')
        fileCommands.Add('FileSaveAll')

        builder.RegisterCommands(FUxCore.ConvertCommands(ListOfSupportedCommands), fileCommands)

    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileSave':
            PriceLinkSpecificationApplication.OnSaveSelected(self, None)
        elif commandName == 'FileSaveAll':
            PriceLinkSpecificationApplication.OnSaveAllSelected(self, None)
        return False

    def HandleStandardFileCommandEnabled(self, commandName):
        if commandName == 'FileSave':
            return bool(self.state & States.PLDUpdated)
        elif commandName == 'FileSaveAll':
            return bool(self.pldList.rowsModified)
        return False

    def InitControls(self):
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)

    def SetState(self, state):
        self.state = self.state | state
        if state == States.PLDPopulated:
            self.state = state
        elif state == States.PLDSelected:
            self.state = self.state & ~States.PLDAdded
            self.state = self.state & ~States.PLDChanged
            self.state = self.state & ~States.PLDUpdated
            self.state = self.state & ~States.PLDMultiSelected
        elif state == States.PLDUpdated:
            self.state = self.state & ~States.PLDChanged
        elif state == States.PLDMultiSelected:
            self.state = self.state & ~States.PLDSelected

    def GetState(self):
        return self.state

    def SelectObjectsInsertItems(self):
        insertItems = acm.FArray()
        insertItems.Add(acm.FPriceLinkDefinition)
        insertItems.Add(acm.FInstrument)
        result = acm.UX().Dialogs().SelectObjectsInsertItemsWithProviders(self.Shell(), insertItems, True)
        return result

    def SelectObjectsInsertInstruments(self):
        result = acm.UX().Dialogs().SelectObjectsInsertItems(self.Shell(), acm.FInstrument, True)
        return result

    def SetForceResetForAMSDistributor(self):
        priceDistributor = self.price_distributor.GetData()
        if priceDistributor:
            if priceDistributor.DistributorType() == "AMS":
                self.force_reset.Enabled(False)
                self.force_reset.Checked(False)

    def PopulateDefaultsDataInPLDFields(self):
        self.price_distributor.Populate(acm.FPriceDistributor.Select(''))

        markets = acm.FArray()
        markets.AddAll(acm.FParty.Select("type='Market'"))
        markets.AddAll(acm.FParty.Select("type='Broker'"))
        self.market.Populate(markets.SortByProperty('Name', True))

        self.ins_curr.Populate(acm.FCurrency.Select(''))

        self.PopulateParametersData()
        self.DefaultData()
        self.SetCaption()

    def SetCaption(self):
        priceDistributor = self.price_distributor.GetData()
        if priceDistributor:
            self.SetContentCaption(priceDistributor.Name())

    def UpdateParameters(self):
        OnListSelectionChanged(self, None)
        
    def DefaultData(self):
        set_tooltip_pld(self)

        self.sort_by = 'Instrument'
        self.isDescending = False
        self.start_time.MaxTextLength(5)
        self.stop_time.MaxTextLength(5)
        self.update_interval.MaxTextLength(9)
        self.addition_addend.MaxTextLength(9)
        self.multiplication_factor.MaxTextLength(9)
        self.service.Enabled(True)
        self.semantic.Enabled(True)
        self.select_all.Clear()
        self.select_all.Enabled(False)
        self.force_reset.Clear()
        self.force_reset.Enabled(False)
        self.default_settings.Checked(True)
        self.UnCheckAllResetFields()
        self.DisableAllResetFields()
        self.xml_data.SetData("")

    def PopulateParametersData(self):
        for val in ["", "True", "False"]:
            self.discard_zero_price.AddItem(val)
            self.discard_zero_quantity.AddItem(val)
            self.discard_negative_price.AddItem(val)
            self.force_update.AddItem(val)
            self.is_delayed.AddItem(val)
            self.ignore_clear_price.AddItem(val)
                    
        self.service.Populate(self.GetPriceServices())
        self.semantic.Populate(acm.FPriceSemantic.Select(''))
        self.semantic.AddItem("")
        self.error_msg.Editable(False)

    def CreateLayout(self):
        self.createTopLayout()
        self.createParametersTab()

    def createTopLayout(self):
        self.topLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.topLayoutBuilderObject.BeginVertBox('Invisible')
        self.topLayoutBuilderObject.BeginHorzBox('Invisible', '', 'colorBox')
        self.topLayoutBuilderObject.    AddIcon('warnIcon')
        self.topLayoutBuilderObject.    AddHyperLink('hyperLink', -1, -1)
        self.topLayoutBuilderObject.EndBox()
        self.topLayoutBuilderObject.    BeginHorzBox('None')
        self.topLayoutBuilderObject.    AddFill()
        self.topLayoutBuilderObject.EndBox()
        self.topLayoutBuilderObject.        AddList("price_link_definitions", 10, -1, 123, -1)
        self.topLayoutBuilderObject.EndBox()

    def createParametersTab(self):
        '''Create parameters tab'''
        self.createParametersTabTopLayout()
        self.createParametersTabBottomLayout()
        self.createResetTabLayout()

    def createParametersTabTopLayout(self):
        '''Create parameters tab top layout'''
        self.parametersTabLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.parametersTabLayoutBuilderObject.BeginVertBox('None')
        self.parametersTabLayoutBuilderObject.BeginHorzBox('EtchedIn', '', 'instrumentbox')
        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddOption('price_distributor', 'Distributor', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddInput('instrument', 'Instrument', -1)
        self.parametersTabLayoutBuilderObject.AddInput('idp_code', 'Market Code', -1)
        self.parametersTabLayoutBuilderObject.EndBox()

        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddOption('ins_curr', '                Currency', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddButton('instrument_fetch', ' Select... ', False, True)
        self.parametersTabLayoutBuilderObject.AddOption('market', '                Market', -1, -1, 'Default')

        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()


    def createParametersTabBottomLayout(self):
        '''Create parameters tab bottom layout'''
        self.parametersTabLayoutBuilderObject.BeginHorzBox('None', '')

        self.parametersTabLayoutBuilderObject.BeginHorzBox('EtchedIn', '', 'parameterbox')
        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddOption('semantic', 'Semantic', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddInput('start_time', 'Start Time (HH:MM)', -1)
        self.parametersTabLayoutBuilderObject.AddInput('update_interval', 'Update Interval (Sec)', -1)
        self.parametersTabLayoutBuilderObject.AddOption('discard_zero_price', 'Discard Zero Price', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddOption('discard_negative_price', 'Discard Negative Price', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddInput('addition_addend', 'Addition Addend', -1)
        self.parametersTabLayoutBuilderObject.AddInput('multiplication_factor', 'Multiplication Factor', -1)
        self.parametersTabLayoutBuilderObject.EndBox()

        self.parametersTabLayoutBuilderObject.AddSpace(10)
        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddOption('service', 'Service', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddInput('stop_time', 'Stop Time (HH:MM)', -1)
        self.parametersTabLayoutBuilderObject.AddOption('force_update', 'Force Update', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddOption('discard_zero_quantity', 'Discard Zero Quantity', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddOption('is_delayed', 'Is Delayed', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddOption('ignore_clear_price', 'Ignore Clear Price', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.EndBox()

        self.parametersTabLayoutBuilderObject.AddSpace(10)
        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddCheckbox('is_inactive', 'Inactive')
        self.parametersTabLayoutBuilderObject.AddCheckbox('is_continuous_subscription', 'Continuous Subscription')
        self.parametersTabLayoutBuilderObject.AddCheckbox('last_follow_interval', 'Last Follow Interval')
        self.parametersTabLayoutBuilderObject.AddLabel('emptylbl', '')
        self.parametersTabLayoutBuilderObject.AddLabel('emptylbl', '')
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()

        self.parametersTabLayoutBuilderObject.BeginHorzBox('EtchedIn', '', 'errorbox')
        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddInput('error_msg', 'Error Message', -1)
        self.parametersTabLayoutBuilderObject.EndBox()

        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddCheckbox('is_log_price', 'Log Price')
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()

    def createResetTabLayout(self):
        self.detailsTabLayoutBuilderObject = acm.FUxLayoutBuilder()

        self.detailsTabLayoutBuilderObject.BeginVertBox('None')
        self.detailsTabLayoutBuilderObject.BeginHorzBox('None')
        self.detailsTabLayoutBuilderObject.BeginHorzBox('None')
        self.detailsTabLayoutBuilderObject.BeginVertBox('None')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_select_all', 'Select All')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_bid', 'Reset Bid')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_ask_size', 'Reset Ask Size')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_low', 'Reset Low')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_diff', 'Reset Diff')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_volume_number', 'Reset Volume Number')
        self.detailsTabLayoutBuilderObject.EndBox()

        self.detailsTabLayoutBuilderObject.BeginVertBox('None')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_force_reset', 'Force Reset')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_ask', 'Reset Ask')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_last', 'Reset Last')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_open', 'Reset Open')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_time_last', 'Reset Time Last')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_available', 'Reset Available')
        self.detailsTabLayoutBuilderObject.EndBox()

        self.detailsTabLayoutBuilderObject.BeginVertBox('None')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_bid_size', 'Reset Bid Size')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_high', 'Reset High')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_settle', 'Reset Settle')
        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_volume_last', 'Reset Volume Last')
        self.detailsTabLayoutBuilderObject.EndBox()
        self.detailsTabLayoutBuilderObject.EndBox()

        self.detailsTabLayoutBuilderObject.      AddCheckbox('is_default_settings', 'Use Default Settings')
        self.detailsTabLayoutBuilderObject.EndBox()
        self.detailsTabLayoutBuilderObject.BeginHorzBox('None', None)
        self.detailsTabLayoutBuilderObject.      AddLabel('xml_data_lbl', 'XML Data:  ')
        self.detailsTabLayoutBuilderObject.AddText('xml_data', -1, 60, -1, -1)
        self.detailsTabLayoutBuilderObject.EndBox()
        self.detailsTabLayoutBuilderObject.EndBox()

    def getAllControlsObectFromGUI(self):
        self.getTopLayoutControlsObject()
        self.getParametersTabLayoutControlsobject()
        self.getDetailsTabLayoutControlsobject()

    def getTopLayoutControlsObject(self):
        """get top layout controls object"""
        self.colorBox               = self.topLayoutObject.GetControl("colorBox")
        self.icon                   = self.topLayoutObject.GetControl("warnIcon")
        self.hyperlink              = self.topLayoutObject.GetControl("hyperLink")

        self.pld_list               = self.topLayoutObject.GetControl("price_link_definitions")

    def getParametersTabLayoutControlsobject(self):
        """get parameters tab layout controls object"""
        self.ins_curr                   = self.parametersTabLayoutObject.GetControl("ins_curr")
        self.price_distributor          = self.parametersTabLayoutObject.GetControl("price_distributor")
        self.instrument                 = self.parametersTabLayoutObject.GetControl("instrument")
        self.market                     = self.parametersTabLayoutObject.GetControl("market")
        self.idp_code                   = self.parametersTabLayoutObject.GetControl("idp_code")
        self.inactive                   = self.parametersTabLayoutObject.GetControl("is_inactive")
        self.semantic                   = self.parametersTabLayoutObject.GetControl("semantic")
        self.service                    = self.parametersTabLayoutObject.GetControl("service")
        self.start_time                 = self.parametersTabLayoutObject.GetControl("start_time")
        self.stop_time                  = self.parametersTabLayoutObject.GetControl("stop_time")
        self.m_IsContinuousSubscription = self.parametersTabLayoutObject.GetControl("is_continuous_subscription")
        self.update_interval            = self.parametersTabLayoutObject.GetControl("update_interval")
        self.last_follow_interval       = self.parametersTabLayoutObject.GetControl("last_follow_interval")
        self.discard_zero_price         = self.parametersTabLayoutObject.GetControl("discard_zero_price")
        self.discard_zero_quantity      = self.parametersTabLayoutObject.GetControl("discard_zero_quantity")
        self.is_delayed                 = self.parametersTabLayoutObject.GetControl("is_delayed")
        self.ignore_clear_price         = self.parametersTabLayoutObject.GetControl("ignore_clear_price")
        self.discard_negative_price     = self.parametersTabLayoutObject.GetControl("discard_negative_price")
        self.force_update               = self.parametersTabLayoutObject.GetControl("force_update")
        self.addition_addend            = self.parametersTabLayoutObject.GetControl("addition_addend")
        self.multiplication_factor      = self.parametersTabLayoutObject.GetControl("multiplication_factor")
        self.log_price                  = self.parametersTabLayoutObject.GetControl("is_log_price")
        self.error_msg                  = self.parametersTabLayoutObject.GetControl("error_msg")
        self.instrument_fetch           = self.parametersTabLayoutObject.GetControl("instrument_fetch")

    def getDetailsTabLayoutControlsobject(self):
        """get details tab layout controls object"""
        self.default_settings = self.detailsTabLayoutObject.GetControl("is_default_settings")
        self.select_all       = self.detailsTabLayoutObject.GetControl("is_select_all")
        self.force_reset      = self.detailsTabLayoutObject.GetControl("is_force_reset")
        self.bid              = self.detailsTabLayoutObject.GetControl("is_bid")
        self.ask              = self.detailsTabLayoutObject.GetControl("is_ask")
        self.bid_size         = self.detailsTabLayoutObject.GetControl("is_bid_size")
        self.ask_size         = self.detailsTabLayoutObject.GetControl("is_ask_size")
        self.last             = self.detailsTabLayoutObject.GetControl("is_last")
        self.high             = self.detailsTabLayoutObject.GetControl("is_high")
        self.low              = self.detailsTabLayoutObject.GetControl("is_low")
        self.open             = self.detailsTabLayoutObject.GetControl("is_open")
        self.settle           = self.detailsTabLayoutObject.GetControl("is_settle")
        self.diff             = self.detailsTabLayoutObject.GetControl("is_diff")
        self.time_last        = self.detailsTabLayoutObject.GetControl("is_time_last")
        self.volume_last      = self.detailsTabLayoutObject.GetControl("is_volume_last")
        self.volume_number    = self.detailsTabLayoutObject.GetControl("is_volume_number")
        self.available        = self.detailsTabLayoutObject.GetControl("is_available")
        self.xml_data         = self.detailsTabLayoutObject.GetControl("xml_data")

    def registerCallbacksForControls(self):
        """Register callbacks for all the controls of price link specification dialog"""
        self.hyperlink.AddCallback       ('Activate', OnHyperLinkClicked, self)
        self.registerCallbacksForTopLayoutControls()
        self.registerCallbacksForParametersTabLayoutControls()
        self.registerCallbacksForDetailsTabLayoutControls()

    def registerCallbacksForTopLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        self.pld_list.AddCallback              ("SelectionChanged", OnListSelectionChanged, self)
        self.pld_list.AddCallback              ('ContextMenu',      self.OnContextMenuCB, None)

    def registerCallbacksForParametersTabLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        self.instrument.AddCallback                ('Changed', OnInstrumentChanged, self)
        self.instrument.AddCallback                ('Activate', OnInstrumentSelected, self)
        self.price_distributor.AddCallback         ('Changed', OnPriceDistributorChanged, self)
        self.semantic.AddCallback                  ('Changed', OnPriceSemanticChanged, self)
        self.instrument_fetch.AddCallback          ('Activate', OnFetchSelected, self)
        self.m_IsContinuousSubscription.AddCallback('Activate', OnContinuousSubscriptionClick, self)

        parametersTabControlsList = [self.inactive, self.last_follow_interval, \
                                     self.log_price, self.m_IsContinuousSubscription]

        for field in parametersTabControlsList:
            field.AddCallback('Activate', OnAnyFieldSelected, self)

        parametersTabControlsList = [self.ins_curr, self.market,
                                     self.idp_code, self.semantic, self.discard_zero_price,
                                     self.start_time, self.stop_time, self.multiplication_factor,
                                     self.service, self.force_update, self.discard_zero_quantity,
                                     self.xml_data, self.discard_negative_price,
                                     self.error_msg, self.update_interval, self.addition_addend,
                                     self.is_delayed, self.ignore_clear_price]

        for field in parametersTabControlsList:
            field.AddCallback('Changed', OnAnyFieldSelected, self)

    def registerCallbacksForDetailsTabLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        self.default_settings.AddCallback('Activate', OnAnyFieldSelected, self)
        self.default_settings.AddCallback('Activate', OnDefaultSettingsSelected, self)
        self.select_all.AddCallback      ('Activate', OnAnyFieldSelected, self)
        self.select_all.AddCallback      ('Activate', OnSelectAllSelected, self)

        for chkbox in self.GetResetFieldsAsTuple():
            chkbox.AddCallback('Activate', CB.OnCheckBoxSelected, self)
            chkbox.AddCallback('Activate', OnAnyFieldSelected, self)

    def DoChangeCreateParameters(self, createParams):
        """Override to be able to modify standard application parameters,
        such as splitters,resizing behaviour etc. This method is called before HandleCreate.
        """
        createParams.UseSplitter(True)
        createParams.LimitMinSize(True)

    def HandleCreate(self, creationContext):
        """This handler is called by Prime application container"""
        self.CreateLayout()
        self.InitControls()
		#Adding Layouts to the application
        self.topLayoutObject = creationContext.AddPane(self.topLayoutBuilderObject, "TOP_PANE")
        self.topLayoutObject.SetLayout(self.topLayoutBuilderObject, "TOP_PANE")

        parametersTabLayoutContext = creationContext.AddTabControlPane("PARAMETERS_PANE")
        self.parametersTabLayoutObject = parametersTabLayoutContext.AddLayoutPage\
                                               (self.parametersTabLayoutBuilderObject, "Parameters")
        self.detailsTabLayoutObject = parametersTabLayoutContext.AddLayoutPage\
                                                     (self.detailsTabLayoutBuilderObject, "Details")

        self.getAllControlsObectFromGUI()
        self.registerCallbacksForControls()
        self.InitializePDErrorPane()
        self.pld_list.EnableHeaderSorting()
        self.pldList = PLDListHandler(self.pld_list)

        for column in self.SavedColumns:
            if column not in CurrentColumns:
                CurrentColumns.append(column)


        self.pldList.Initialize()


        self.PopulateDefaultsDataInPLDFields()
        self.AddSubscriptions()

    def InitializePDErrorPane(self):
        self.colorBox.SetColor('Background', acm.UX().Colors().Create(250, 250, 210))
        self.hyperlink.SetData('Distributor error. Click here for Distributor Setting')
        self.icon.SetColor('Background', acm.UX().Colors().Create(250, 250, 210))
        self.icon.SetData('Warning')
        self.colorBox.Visible(False)
        self.hyperlink.Visible(False)
        self.icon.Visible(False)


    def AddSubscriptions(self):
        '''Adding subscription on FPriceLinkDefinition Table'''
        try:
            acm.FPriceLinkDefinition.Select('').AddDependent(self.priceLinkDefinitionTableChangeHandler)
            acm.FPriceDistributor.Select('').AddDependent(self.priceDistributorTableChangeHandler)
            acm.FPriceSemantic.Select('').AddDependent(self.priceSemanticsTableChangeHandler)
            acm.FChoiceList.Select('list="PriceServices"').AddDependent(self.priceServicesChangeHandler)
        except Exception as extraInfo:
            print('Exception:' + str(extraInfo))

    def RemoveSubscriptions(self):
        '''Adding subscription on FPriceLinkDefinition Table'''
        try:
            acm.FPriceLinkDefinition.Select('').RemoveDependent(self.priceLinkDefinitionTableChangeHandler)
            acm.FPriceDistributor.Select('').RemoveDependent(self.priceDistributorTableChangeHandler)
            acm.FPriceSemantic.Select('').RemoveDependent(self.priceSemanticsTableChangeHandler)
            acm.FChoiceList.Select('list="PriceServices"').RemoveDependent(self.priceServicesChangeHandler)
        except Exception as extraInfo:
            print(str(extraInfo))

    def HandleApply(self):
        """validates the dialog"""
        if self.HasUnsavedChanges():
            choice = self.ShowTableModifiedDialog()
            if choice == ButtonOptions.CANCEL:
                return False
        return True

    def HandleClose(self):
        """closes the dialog"""
        if self.HasUnsavedChanges():
            choice = self.ShowTableModifiedDialog()
            if choice == ButtonOptions.CANCEL:
                return False
        return True

    def HasUnsavedChanges(self):
        return self.pldList.rowsModified

    def HandleDestroy(self):
        """closes the dialog"""
        self.binder.RemoveDependent(self)
        self.RemoveSubscriptions()

    def GetAttributeValues(self):
        values = dict()
        values['PriceDistributor']      = self.price_distributor.GetData()
        values['Instrument']            = self.instrument.GetData()
        values['Currency']              = self.ins_curr.GetData()
        values['Market']                = self.market.GetData()
        values['IdpCode']               = self.idp_code.GetData()
        values['IdpCodeLabel']          = self.idp_code.Label()
        values['NotActive']             = self.inactive.Checked()
        values['Service']               = self.service.GetData()
        values['SemanticSeqNbr']        = self.semantic.GetData()
        values['StartTime']             = self.start_time.GetData()
        values['StopTime']              = self.stop_time.GetData()
        values['UpdateInterval']        = self.update_interval.GetData()
        values['AdditionAddend']        = self.addition_addend.GetData()
        values['MultiplicationFactor']  = self.multiplication_factor.GetData()
        values['LastFollowInterval']    = self.last_follow_interval.Checked()
        values['DiscardZeroPrice']      = self.discard_zero_price.GetData()
        values['DiscardZeroQuantity']   = self.discard_zero_quantity.GetData()
        values['IsDelayed']             = self.is_delayed.GetData()
        values['IgnoreClearPrice']      = self.ignore_clear_price.GetData()
        values['DiscardNegativePrice']  = self.discard_negative_price.GetData()
        values['ForceUpdate']           = self.force_update.GetData()
        values['LogPrice']              = self.log_price.Checked()
        values['DefaultSettings']       = self.default_settings.Checked()
        values['DonotResetFields']      = self.GetResetFields()
        values['XmlData']               = self.xml_data.GetData()
        values['Owner']                 = self.owner
        values['Protection']            = self.protection
        return values

    '''Static functions for all the call backs'''
    @staticmethod
    def OnRevertAll(self, arg):
        self.pldList.RevertAll()
        OnListSelectionChanged(self, None)

    @staticmethod
    def OnRevert(self, arg):
        self.pldList.Revert()
        OnListSelectionChanged(self, None)

    @staticmethod
    def OnSaveAllSelected(self, arg):
        rows = self.pldList.pldList.GetRootItem()
        for row in rows.Children():
            pld = self.pldList.GetPLDObject(row)
            pldOrig = self.pldList.GetOriginalPLDObject(pld)
            if pld.IdpCode() != pldOrig.IdpCode():
                price =  GetPrice(pldOrig.Instrument().Name(), pldOrig.Currency().Name(), pldOrig.Market().Name())
                if price:
                    price.Bits(0)
                    price.Commit()
            
        self.pldList.SaveAll()
        OnListSelectionChanged(self, None)

    @staticmethod
    def OnSaveSelected(self, arg):
        try:
            rows = self.pldList.GetSelectedRows()
            for row in rows:
                pld = self.pldList.GetPLDObject(row)
                pldOrig = self.pldList.GetOriginalPLDObject(pld)
                if pld.IdpCode() != pldOrig.IdpCode():
                    price =  GetPrice(pldOrig.Instrument().Name(), pldOrig.Currency().Name(), pldOrig.Market().Name())
                    if price:
                        price.Bits(0)
                        price.Commit()

            self.pldList.Save()
            OnListSelectionChanged(self, None)
        except RuntimeError as e:
            self.ShowError(str(e))

class PriceLinkDefinitionTableChangeHandler:
    def __init__(self, parent):
        self.parent = parent

    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) in ('update', 'insert'):
            self.parent.pldList.HandleServerUpdate(param)
        elif str(aspect) == 'remove':
            self.parent.pldList.HandleServerRemove(param)

class PriceDistributorTableChangeHandler:
    def __init__(self, parent):
        self.parent = parent

    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) in ('update', 'insert'):
            selectedDistributor = self.parent.price_distributor.GetData()
            self.parent.price_distributor.Populate(acm.FPriceDistributor.Select(''))
            self.parent.price_distributor.SetData(selectedDistributor)
            self.parent.SetCaption()

            if selectedDistributor:
               distributorErr = selectedDistributor.ErrorMessage()

               if distributorErr != "":
                   self.parent.colorBox.Visible(True)
                   self.parent.hyperlink.Visible(True)
                   self.parent.icon.Visible(True)
               else:
                   self.parent.colorBox.Visible(False)
                   self.parent.hyperlink.Visible(False)
                   self.parent.icon.Visible(False)
                   
            self.parent.pldList.HandleServerUpdateDist(param)
            self.parent.UpdateParameters()
        
        elif str(aspect) == 'remove':
            if self.parent.price_distributor.ItemExists(param):
                self.parent.price_distributor.RemoveItem(param)

class PriceSemanticsTableChangeHandler:
    def __init__(self, parent):
        self.parent = parent

    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) in ('update', 'insert'):
            selectedSemantic = self.parent.semantic.GetData()
            self.parent.semantic.Populate(acm.FPriceSemantic.Select(''))
            self.parent.semantic.AddItem("")
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

class PriceLinkSpecificationApplicationExtension\
                                         (PriceLinkSpecificationApplication):
    def __init__(self, pInstrumentName = None):
        PriceLinkSpecificationApplication.__init__(self)
        self.InstrumentName = pInstrumentName
        self.Currency = None
        self.Market = None
        self.Distributor = None
        self.Code = None

    def setPriceDefinitionName(self, pInstrumentName):
        """Set the selected price definition name"""
        self.InstrumentName = pInstrumentName

    def HandleCreate(self, creationContext):
        PriceLinkSpecificationApplication.HandleCreate(self, creationContext)
        if (self.InstrumentName and "Front Arena" not in self.InstrumentName):
            self.populateSelectedInstrument()

        if (self.InstrumentName and "Front Arena" not in self.InstrumentName):
            self.instrument.SetData(self.InstrumentName)
        if self.Currency:
            self.ins_curr.SetData(self.Currency)
        if self.Market:
            self.market.SetData(self.Market)
        if self.Code:
            self.idp_code.SetData(self.Code)
        if self.Distributor:
            self.price_distributor.SetData(self.Distributor)


    def populateSelectedInstrument(self):
        '''Populate pld grid with the selected instrument details'''
        pldList = acm.FPriceLinkDefinition.Select('instrument="%s"'%(self.InstrumentName))
        self.pldList.Populate(pldList)

def RunApplicationFromCreateOB(instrument = None, currency = None, market = None, distributor = None, marketCode = None):
    try:
        contentsDict = acm.FDictionary()

        contentsDict.AtPut('instrument', instrument)
        contentsDict.AtPut('currency', currency)
        contentsDict.AtPut('market', market)
        contentsDict.AtPut('distributor', distributor)
        contentsDict.AtPut('marketCode', marketCode)

        acm.UX().SessionManager().StartApplication(APPLICATION_NAME, contentsDict)
    except RuntimeError as extraInfo:
        print(str(extraInfo))
        raise extraInfo

#*******************************APPLICATION HANDLERS*********************#
def GetApplicationObject():
    """Returns application object"""
    myNewAppInstance = PriceLinkSpecificationApplicationExtension()
    return myNewAppInstance

def RunApplication(instrumentName = None):
    """Opens Price Link Specification Dialog"""
    try:
        acm.UX().SessionManager().StartApplication(APPLICATION_NAME, instrumentName)
    except RuntimeError as extraInfo:
        print(str(extraInfo))
        raise extraInfo

def StartApplicationFromInsDef(eii):
    """Action when Price Link Specification GUI
    is launched from any Instrument Definition Window"""
    extendedObject = eii.ExtensionObject()
    insName = getInstrumentName(extendedObject)
    return RunApplication(insName)

def StartApplicationFromRightClick(eii):
    """Action when Price Link Specification GUI
    is launched from any Instrument based FObject"""
    for aInstrumentACMObj in eii.ExtensionObject():
        if aInstrumentACMObj.IsKindOf(acm.FInstrument):
            return RunApplication(aInstrumentACMObj.Name())
    return RunApplication()

def getInstrumentName(pExtensionObject):
    """Check if the Application extension object contains instrument name"""
    insName = ''
    object = pExtensionObject.CurrentObject()
    if object: 
        aClass = object.Class()
        if aClass.IncludesBehavior(acm.FInstrument) :
            insName = object.Name()
        elif aClass.IncludesBehavior(acm.FTrade) :
            insName = object.Instrument().Name()
    return insName

def StartApplication(eii):
    """Action when Price Link Specification GUI is installed as an
       Application"""
    instrumentName = getInstrumentName(eii.ExtensionObject())
    RunApplication(instrumentName)

def test():
    acm.UX().SessionManager().StartApplication(APPLICATION_NAME, None)

#test()

#*******************************EXTENDED FUNCTIONALITY TO USE FROM CREATE OB*********************#
class PriceLinkSpecificationApplicationExtensionFromCreateOB\
                                         (PriceLinkSpecificationApplicationExtension):
    def __init__(self):
        PriceLinkSpecificationApplicationExtension.__init__(self)
        self.InstrumentName = None
        self.Currency = None
        self.Market = None
        self.Distributor = None
        self.Code = None

    def setValues(self, instrument, currency, market, distributor, marketCode):
        """Set the selected price definition name"""
        self.InstrumentName = instrument
        self.Currency = currency
        self.Market = market
        self.Distributor = distributor
        self.Code = marketCode

    def HandleCreate(self, creationContext):
        PriceLinkSpecificationApplicationExtension.HandleCreate(self, creationContext)
        if self.InstrumentName:
            self.instrument.SetData(self.InstrumentName)
        if self.Currency:
            self.ins_curr.SetData(self.Currency)
        if self.Market:
            self.market.SetData(self.Market)
        if self.Code:
            self.idp_code.SetData(self.Code)
        if self.Distributor:
            self.price_distributor.SetData(self.Distributor)

def RunApplicationFromCreateOB(instrument = None, currency = None, market = None, distributor = None, marketCode = None):
    global ApplicationObject
    try:
        ApplicationObject = PriceLinkSpecificationApplicationExtensionFromCreateOB()
        ApplicationObject.setValues(instrument, currency, market, distributor, marketCode)
        acm.UX().SessionManager().StartApplication(APPLICATION_NAME, None)
    except RuntimeError as extraInfo:
        print(str(extraInfo))
        raise extraInfo
