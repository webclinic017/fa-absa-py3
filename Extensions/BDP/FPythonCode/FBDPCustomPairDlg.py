""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPCustomPairDlg.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
Module
    FBDPCustomPairDlg - Module with customized dialog

DESCRIPTION
    A dialog for choosing key value pairs.
----------------------------------------------------------------------------"""

import collections
import datetime
import re


import acm
import FUxCore
import FBDPCommon

SEPARATOR = ' : '

def GetDictFromList(l):
    d = {}
    for s in l:
        par = s.partition(SEPARATOR)
        key = par[0]
        val = par[2]
        if key and val:
            d[key.strip()] = val.strip()
    return d


def OnAddClicked(self, cd):
    key = self.m_keys.GetData()
    value = self.m_values.GetData()
    if key and value:
        if self.ValidateAdd(key, value):
            if not isinstance(key, str):
                pair = str(key.Name() + SEPARATOR + value.Name())
            else:
                pair = str(key + SEPARATOR + value.Name())
            AddItem(self.pairList, self.m_pairs, pair)
            RemoveItem(self.keyList, self.m_keys, key)

def OnMultiplePairAddClicked(self, cd):
    key = self.m_keys.GetData()
    value = self.m_values.GetData()
    if key and value:
        if self.ValidateAdd(key, value):
            if not isinstance(key, str):
                pair = str(key.Name() + SEPARATOR + value.Name())
            else:
                pair = str(key + SEPARATOR + value.Name())
            AddItem(self.pairList, self.m_pairs, pair)
            #RemoveItem(self.keyList, self.m_keys, key)


def OnMultipleValueAddClicked(self, cd):
    value = self.m_values.GetData()
    if value:
        AddItem(self.pairList, self.m_pairs, value)
        RemoveItem([value], self.m_values, value)


def AddItem(objList, itemList, item):
    objList.append(item)
    objList.sort()
    itemList.Populate(objList)
    itemList.SetData(item)


def RemoveItem(objList, itemList, item):
    index = objList.index(item)
    objList.remove(item)
    itemList.RemoveItem(item)
    if objList:
        if len(objList) <= index:
            index -= 1
        newItem = objList[index]
        if newItem:
            itemList.SetData(newItem)


def OnRemoveClicked(self, cd):
    pair = self.m_pairs.GetData()
    key = GetKeyFromPair(self, pair)
    AddItem(self.keyList, self.m_keys, key)
    RemoveItem(self.pairList, self.m_pairs, pair)


def OnMultiplePairRemoveClicked(self, cd):
    pair = self.m_pairs.GetData()
    RemoveItem(self.pairList, self.m_pairs, pair)


def OnMultipleValueRemoveClicked(self, cd):
    value = self.m_pairs.GetData()
    if value:
        AddItem([], self.m_values, value)
        RemoveItem(self.pairList, self.m_pairs, value)


def OnUpdateSelectedKey(self, cd):
    self.UpdateSelectedKey()


def GetKeyFromPair(self, pair):
    key = pair.partition(SEPARATOR)[0]
    keyObj = key
    if key and hasattr(acm, self.keyObj):
        keyObj = getattr(acm, self.keyObj)[key]
    return keyObj


def OnRemoveAllClicked(self, cd):
    for pair in self.pairList:
        key = GetKeyFromPair(self, pair)
        self.keyList.append(key)
    self.pairList = []
    self.m_pairs.Clear()
    self.keyList.sort()
    self.m_keys.Populate(self.keyList)
    SelectFirstItem(self.keyList, self.m_keys)


def OnMultiplePairRemoveAllClicked(self, cd):
    self.pairList = []
    self.m_pairs.Clear()


def OnMultipleValueRemoveAllClicked(self, cd):
    key = self.m_keys.GetData()
    valList = list(self.pairList)
    for val in self.pairList:
        if key and key == self.GetKeyFromValue(val):
            valList.append(val)

    self.pairList = []
    self.m_pairs.Clear()
    valList.sort()
    self.m_values.Populate(valList)
    SelectFirstItem(valList, self.m_values)


def SelectFirstItem(objList, itemList):

    if objList:
        firstItem = objList[0]
        itemList.SetData(firstItem)


class SelectPairsCustomDialog(FUxCore.LayoutDialog):

    DICT_KEYS = 'dictKeys'
    DICT_VALUES = 'dictValues'
    DICT_PAIRS = 'dictPairs'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    def __init__(self, shell, params, keyObj=None, valObj=None,
            caption='Select Pairs', keyLbl='Key', valLbl='Value',
            pairLbl='Selected Pairs'):
        self.shell = shell
        self.choices = params['choices']
        self.selected = params['selected']
        self.keyObj = keyObj
        self.valObj = valObj
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl
        self.keyList = []
        self.pairList = []

    def HandleApply(self):
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', self.pairList)
        return resultDic

    def ValidateAdd(self, key, value):
        return True

    def SetControlData(self):
        for pair in self.selected:
            key = GetKeyFromPair(self, pair)
            self.keyList.remove(key)
            self.pairList.append(pair)
        self.m_keys.Populate(self.keyList)
        self.pairList.sort()
        self.m_pairs.Populate(self.pairList)
        SelectFirstItem(self.keyList, self.m_keys)
        SelectFirstItem(self.pairList, self.m_pairs)

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_keys = layout.GetControl(self.DICT_KEYS)
        self.m_keys.AddCallback('Changed', OnUpdateSelectedKey, self)
        self.m_values = layout.GetControl(self.DICT_VALUES)
        self.m_pairs = layout.GetControl(self.DICT_PAIRS)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate', OnAddClicked, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate', OnRemoveClicked, self)
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate', OnRemoveAllClicked, self)
        self.PopulateControls()
        self.SetControlData()

    def UpdateSelectedKey(self):
        pass

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel("lblKeys", self.keyLabel)
        b.   AddList(self.DICT_KEYS, 10, -1, 30, -1)
        b.  EndBox()
        b.  AddSpace(1)
        b.  BeginVertBox()
        b.   AddLabel("lblValues", self.valLabel)
        b.   AddList(self.DICT_VALUES, 10, -1, 40, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        b.   AddSpace(3)
        b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel("lblPairs", self.pairLabel)
        b.   AddList(self.DICT_PAIRS, 10, -1, 40, -1)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

    def PopulateControls(self):
        self.keyList = self.LoadData(self.keyObj)
        self.keyList.sort()
        self.m_keys.Populate(self.keyList)
        if self.keyList:
            self.m_keys.SetData(self.keyList[0])
        valList = self.LoadData(self.valObj)
        valList.sort()
        self.m_values.Populate(valList)
        if valList:
            self.m_values.SetData(valList[0])

    def LoadData(self, objName):
        l = []
        for obj in getattr(acm, objName).Select(''):
            if self.ValidObject(obj, objName):
                l.append(obj)
        return l

    def ValidObject(self, obj, objName):
        if str(obj.Name()).find(',') >= 0:
            print(('WARNING %s "%s" contains illegal char "," will be ignored' %
                    (objName, obj.Name())))
            return False
        return True


class SelectMultiplePairsCustomDialog(FUxCore.LayoutDialog):

    DICT_KEYS = 'dictKeys'
    DICT_VALUES = 'dictValues'
    DICT_PAIRS = 'dictPairs'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    def __init__(self, shell, params, keyObj=None, valObj=None,
            caption='Select Pairs', keyLbl='Key', valLbl='Value',
            pairLbl='Selected Pairs'):
        self.shell = shell
        self.choices = params['choices']
        self.selected = params['selected']
        self.keyObj = keyObj
        self.valObj = valObj
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl
        self.keyList = []
        self.pairList = []

    def HandleApply(self):
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', self.pairList)
        return resultDic

    def ValidateAdd(self, key, value):
        return True

    def SetControlData(self):
        for pair in self.selected:
            self.pairList.append(pair)
        self.m_keys.Populate(self.keyList)
        self.pairList.sort()
        self.m_pairs.Populate(self.pairList)
        SelectFirstItem(self.keyList, self.m_keys)
        SelectFirstItem(self.pairList, self.m_pairs)

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_keys = layout.GetControl(self.DICT_KEYS)
        self.m_keys.AddCallback('Changed', OnUpdateSelectedKey, self)
        self.m_values = layout.GetControl(self.DICT_VALUES)
        self.m_pairs = layout.GetControl(self.DICT_PAIRS)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate', OnMultiplePairAddClicked, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate',
            OnMultiplePairRemoveClicked, self)
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate',
            OnMultiplePairRemoveAllClicked, self)
        self.PopulateControls()
        self.SetControlData()

    def UpdateSelectedKey(self):
        pass

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel("lblKeys", self.keyLabel)
        b.   AddList(self.DICT_KEYS, 10, -1, 30, -1)
        b.  EndBox()
        b.  AddSpace(1)
        b.  BeginVertBox()
        b.   AddLabel("lblValues", self.valLabel)
        b.   AddList(self.DICT_VALUES, 10, -1, 40, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        b.   AddSpace(3)
        b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel("lblPairs", self.pairLabel)
        b.   AddList(self.DICT_PAIRS, 10, -1, 40, -1)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

    def PopulateControls(self):
        self.keyList = self.LoadData(self.keyObj)
        self.keyList.sort()
        self.m_keys.Populate(self.keyList)
        if self.keyList:
            self.m_keys.SetData(self.keyList[0])
        valList = self.LoadData(self.valObj)
        valList.sort()
        self.m_values.Populate(valList)
        if valList:
            self.m_values.SetData(valList[0])

    def LoadData(self, objName):
        l = []
        for obj in getattr(acm, objName).Select(''):
            if self.ValidObject(obj, objName):
                l.append(obj)
        return l

    def ValidObject(self, obj, objName):
        if str(obj.Name()).find(',') >= 0:
            print(('WARNING %s "%s" contains illegal char "," will be ignored' %
                    (objName, obj.Name())))
            return False
        return True

class SelectMultipleValuesCustomDialog(SelectMultiplePairsCustomDialog):
    """
    Holds any object type - i.e. no implicit type casting occurs
    To be used where each value has a unique identifier.
    N.B. self.pairList is just the value list
        (not a list of pairs as in SelectMultiplePairsCustomDialog)
        c.f. Add and Remove callbacks
    """
    def GetKeyChoices(self):
        """
        The method used to list left-most selection choices
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def GetValueChoices(self, key):
        """
        The method used to list second-order selection choices
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def LoadSourceData(self):
        self._preloaded_data = collections.OrderedDict()
        keys = self.GetKeyChoices()
        for key in keys:
            val = self.GetValueChoices(key)
            if len(val):
                self._preloaded_data[key] = [str(v) for v in val]

    def GetKeyFromValue(self, value):
        for k, v in self._preloaded_data.iteritems():
            if v == value:
                return k

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_keys = layout.GetControl(self.DICT_KEYS)
        self.m_keys.AddCallback('Changed',
            OnUpdateSelectedKey, self)
        self.m_values = layout.GetControl(self.DICT_VALUES)
        self.m_pairs = layout.GetControl(self.DICT_PAIRS)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate',
            OnMultipleValueAddClicked, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate',
            OnMultipleValueRemoveClicked, self)
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate',
            OnMultipleValueRemoveAllClicked, self)
        self.LoadSourceData()
        self.PopulateControls()
        self.SetControlData()

    def PopulateControls(self):
        self.keyList = self._preloaded_data.keys()
        self.m_keys.Populate(self.keyList)
        if len(self.keyList):
            self.m_keys.SetData(self.keyList[0])

        selected = []
        for selection in self.selected:
            found = False
            for known_values in self._preloaded_data.itervalues():
                if selection in known_values:
                    selected.append(selection)
                    break

        self.selected = selected

    def UpdateSelectedKey(self):
        key = self.m_keys.GetData()
        if key:
            valList = self._preloaded_data[key]
            valList = [v for v in valList if v not in self.pairList]
            self.m_values.Populate(valList)
            if valList:
                self.m_values.SetData(valList[0])

class SelectObjPortCustomDialog(SelectPairsCustomDialog):

    def ValidObject(self, obj, objName):
        if obj.IsKindOf(acm.FPhysicalPortfolio) and obj.Compound():
            return False
        return SelectPairsCustomDialog.ValidObject(self, obj, objName)


class SelectCurrPortCustomDialog(SelectObjPortCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
            keyLbl='Currency', valLbl='Portfolio', pairLbl='Selected Pairs'):
        SelectPairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FCurrency'
        self.valObj = 'FPhysicalPortfolio'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl


class SelectCurrpairPortCustomDialog(SelectObjPortCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
            keyLbl='Currency pair', valLbl='Portfolio',
            pairLbl='Selected Pairs'):
        SelectPairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FCurrencyPair'
        self.valObj = 'FPhysicalPortfolio'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl

    def ValidateAdd(self, key, value):
        if not value.CurrencyPair():
            return True
        if value.CurrencyPair().Currency1() == key.Currency1():
            return True
        if value.CurrencyPair().Currency1() == key.Currency2():
            return True
        if value.CurrencyPair().Currency2() == key.Currency1():
            return True
        if value.CurrencyPair().Currency2() == key.Currency2():
            return True
        msg = ('Portfolio %s has currency pair %s, and can NOT be paired with '
               '%s' % (value.Name(), value.CurrencyPair().Name(), key.Name()))
        acm.UX().Dialogs().MessageBoxInformation(self.shell, msg)
        return False


class SelectObjInstCustomDialog(SelectPairsCustomDialog):

    def ValidObject(self, obj, objName):
        if obj.IsKindOf(acm.FInstrument) and obj.InsType() != 'FxSwap':
            return False
        return SelectPairsCustomDialog.ValidObject(self, obj, objName)


class SelectCurrpairInstCustomDialog(SelectObjInstCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
            keyLbl='Currency pair', valLbl='Instrument',
            pairLbl='Selected Pairs'):
        SelectPairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FCurrencyPair'
        self.valObj = 'FFxSwap'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl

    def ValidateAdd(self, key, value):
        legs = value.Legs()
        for leg in legs:
            if (leg.Currency() != key.Currency1() and
                    leg.Currency() != key.Currency2()):
                msg = ('Fx Swap %s has currency %s, and cannot be paired with '
                        '%s' % (value.Name(), leg.Currency().Name(),
                        key.Name()))
                acm.UX().Dialogs().MessageBoxInformation(self.shell, msg)
                return False
        return True


class SelectObjAcqCustomDialog(SelectPairsCustomDialog):

    def LoadData(self, objName):
        if objName == 'FParty':
            l = []
            internalDepartments = acm.FInternalDepartment.Select('')
            for department in internalDepartments:
                if self.ValidObject(department, objName):
                    l.append(department)
            return l
        else:
            return SelectPairsCustomDialog.LoadData(self, objName)


class SelectCurrAcqCustomDialog(SelectObjAcqCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
                 keyLbl='Currency', valLbl='Acquirer',
                 pairLbl='Selected Pairs'):
        SelectPairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FCurrency'
        self.valObj = 'FParty'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl


class SelectCurrpairAcqCustomDialog(SelectObjAcqCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
            keyLbl='Currency pair', valLbl='Acquirer',
            pairLbl='Selected Pairs'):
        SelectPairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FCurrencyPair'
        self.valObj = 'FParty'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl


class SelectPortfolioCurrpairCustomDialog(SelectMultiplePairsCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
                 keyLbl='Portfolio', valLbl='Currency pair',
                 pairLbl='Selected Pairs'):
        SelectMultiplePairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FPhysicalPortfolio'
        self.valObj = 'FCurrencyPair'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl

    def ValidateAdd(self, key, value):
        portCurrPair = key.CurrencyPair()
        if not portCurrPair:
            return True
        elif portCurrPair == value:
            return True
        msg = ('Portfolio %s has currency pair %s, and can NOT use %s '
               'as its position pair '
               % (key.Name(), portCurrPair.Name(), value.Name()))
        acm.UX().Dialogs().MessageBoxInformation(self.shell, msg)
        return False


class SelectInstrumentTypeAndCurrencyToInstrumentCustomDialog(
        SelectPairsCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
            keyLbl='InstrumentType/Currency', valLbl='Instrument',
            pairLbl='Selected Pairs'):
        SelectPairsCustomDialog.__init__(self, shell, params)
        self.keyObj = 'FInstrumentTypeCurrency'
        self.valObj = 'FInstrument'
        self.caption = caption
        self.keyLabel = keyLbl
        self.valLabel = valLbl
        self.pairLabel = pairLbl
        self.insTypes = []

    def ValidObject(self, obj, objName):
        if obj.IsExpired():
            return False
        return SelectPairsCustomDialog.ValidObject(self, obj, objName)

    def LoadData(self, objName):
        l = []
        if not self.insTypes or objName == 'FInstrument':
            pass
        elif objName == 'FInstrumentTypeCurrency':
            for curr in acm.FCurrency.Select(''):
                for i in self.insTypes:
                    insTypeCurr = i + '/' + str(curr.Name())
                    l.append(insTypeCurr)
        return l

    def UpdateSelectedKey(self):
        key = self.m_keys.GetData()
        if key:
            insType = key.rsplit("/", 1)[0]
            curr = key.rsplit("/", 1)[1]
            valList = []
            query = ("insType = '%s' and currency = '%s' and generic = False" %
                    (insType, curr))
            objSet = getattr(acm, self.valObj).Select(query)
            for obj in objSet:
                if self.ValidObject(obj, self.valObj):
                    valList.append(obj)
            valList.sort()
            self.m_values.Populate(valList)
            if valList:
                self.m_values.SetData(valList[0])


class SelectMMInstrumentTypeAndCurrencyToInstrumentCustomDialog(
        SelectInstrumentTypeAndCurrencyToInstrumentCustomDialog):

    def __init__(self, shell, params, caption='Select Pairs',
            keyLbl='InstrumentType/Currency', valLbl='Instrument',
            pairLbl='Selected Pairs'):
        SelectInstrumentTypeAndCurrencyToInstrumentCustomDialog.__init__(self,
                shell, params)
        self.insTypes = ['Bill', 'Repo/Reverse', 'Deposit']


class SelectDealPackagesCustomDialog(SelectMultipleValuesCustomDialog):

    def __init__(
            self, shell, params,
            keyObj='FInstrumentPackage', valObj='',
            valLbl='Deal Packages'
    ):
        valLbl = valLbl.title()
        SelectMultipleValuesCustomDialog.__init__(
            self, shell=shell, params=params, keyObj=keyObj, valObj=valObj,
            caption='Select %s' % valLbl, keyLbl='Instrument Packages',
            valLbl=valLbl, pairLbl='Selected %s' % valLbl
    )

    def Create(self):
        dialog = acm.UX().Dialogs().ShowCustomDialogModal(
            self.shell, self.CreateLayout(), self
        )
        return dialog

    def GetKeyChoices(self):
        ins_pkgs = self.LoadData(self.keyObj)
        ins_pkgs.sort()
        return ins_pkgs

    def GetValueChoices(self, key):
        ins_pkg = key
        deal_pkgs = [str(dp.Oid()) for dp in ins_pkg.DealPackages()]
        deal_pkgs.sort()
        return deal_pkgs

class SelectArchivedDealPackagesCustomDialog(SelectDealPackagesCustomDialog):
    def __init__(self, shell, params, name_to_oid_map=None):
        self._name_to_oid_map = name_to_oid_map
        if self._name_to_oid_map is not None:
            self._name_to_oid_map.clear()

        SelectDealPackagesCustomDialog.__init__(
            self, shell=shell, params=params,
            keyObj='string', valLbl='Archived Deal Packages',
        )

    def GetKeyChoices(self):
        query = (
            'SELECT instrument_package.name FROM instrument_package'
        )
        selections = FBDPCommon.FBDPQuerySelection(
            name='Instrument Packages',
            query_expr=query
        ).Run()
        selections.sort()
        return selections

    def GetValueChoices(self, key):
        ins_pkg_name = key
        query = (
            'SELECT dp.optional_id, dp.seqnbr '
            'FROM deal_package as dp, instrument_package as ip '
            'WHERE '
            '(ip.name = \'%s\') '
            'AND '
            '(dp.ins_package_seqnbr = ip.seqnbr) '
            'AND '
            'dp.archive_status = 1'
        ) % ins_pkg_name
        selections = FBDPCommon.FBDPQuerySelection(
            name='Archived Deal Packages',
            query_expr=query,
            num_results_per_row=2
        ).Run()
        _selections = []
        for name, oid in selections:
            name = str(name)
            _selections.append(name)
            if self._name_to_oid_map is not None:
                self._name_to_oid_map[name] = int(oid)

        _selections.sort()
        return _selections

FX_TABLE = []


def OnPairSelectionChanged(args, cd):

    caller = args[0]
    index = args[1]
    pair = getattr(caller, 'pair%i' % index).GetData()
    if pair:
        pair = pair.split('/')
    dnear = caller.GetNearDate(pair)
    m_dnear = getattr(caller, 'dnear%i' % index).SetData(dnear)
    m_dfar = getattr(caller, 'dfar%i' % index).SetData(caller.GetFarDate(pair,
            dnear))
    if not getattr(caller, 'pair%i' % (index + 1)).Visible():
        caller.UpdateControls()


def OnClearPressed(args, cd):

    caller = args[0]
    index = args[1]
    caller.ResetControls(index)


def OnCalendarPressed(args, cd):

    caller = args[0]
    field = args[1]
    shell = caller.shell
    calendar = caller.AccountingCalendar()
    customDlg = TradingDateCustomDialog(shell, field, calendar)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


class BrokerRatesCustomDialog(FUxCore.LayoutDialog):

    CONTROLS = 20

    def __init__(self, shell, params, template):
        self.m_okBtn = None
        self.m_counter = 0
        self.out = []
        self.params = []
        self.shell = shell
        self.template = template
        self.today = acm.Time.DateValueDay()
        self.pairs = self.GetPairs()
        self.acquirers = self.GetAcquirers()
        self.counterparties = self.GetCounterparties()
        self.parameters = params
        self.ParseParams(params['selected'])
        for i in range(self.CONTROLS):
            setattr(self, 'pair%i' % i, None)
            setattr(self, 'acq%i' % i, None)
            setattr(self, 'cparty%i' % i, None)
            setattr(self, 'near%i' % i, None)
            setattr(self, 'far%i' % i, None)
            setattr(self, 'dnear%i' % i, None)
        self.m_fuxLayout = None

    def GetPairs(self):

        pairs = acm.FCurrencyPair.Select('').PropertiesText(
                'Name', '|').split('|')
        pairs.remove('')
        return sorted(list(set(pairs)))

    def GetCounterparties(self):

        party = acm.FParty.Select('type = "Counterparty"').PropertiesText(
                'Name', '|').split('|')
        party.remove('')
        party.extend(acm.FParty.Select('type = "Broker"').PropertiesText(
                'Name', '|').split('|'))
        party.remove('')
        return sorted(party)

    def GetAcquirers(self):

        acquirers = acm.FParty.Select('type = "Broker"').PropertiesText(
                'Name', '|').split('|')
        acquirers.remove('')
        return sorted(acquirers)

    def ParseParams(self, params):
        if params:
            for param in params:
                param = param[1:-1].split(',')
                pair = param[0]
                acq = param[1]
                self.params.append((pair, acq))

    def ValuationParameters(self):

        return acm.UsedValuationParameters()

    def GetAccountingCurr(self):

        params = self.ValuationParameters()
        return params.AccountingCurrency()

    def AccountingCalendar(self):

        acurr = self.GetAccountingCurr()
        return acurr.Calendar()

    def GetCurrObj(self, curr):

        return acm.FCurrency[curr]

    def GetCalendar(self, curr):

        curr_obj = self.GetCurrObj(curr)
        return curr_obj.Calendar()

    def GetBankingDate(self, pair, date):

        cal1, cal2 = (self.GetCalendar(curr) for curr in pair)
        while cal1.IsNonBankingDay(cal1, cal2, date):
            date = acm.Time.DateAddDelta(date, 0, 0, 1)
        return date

    def GetNearDate(self, pair):

        if 'CAD' in pair:
            return self.GetBankingDate(pair, self.today)
        date = acm.Time.DateAddDelta(self.today, 0, 0, 1)
        return self.GetBankingDate(pair, date)

    def GetFarDate(self, pair, dnear):

        fdate = acm.Time.DateAddDelta(dnear, 0, 0, 1)
        return self.GetBankingDate(pair, fdate)

    def SetControls(self):

        size = len(FX_TABLE)
        for i in range(size):
            self.UpdateControls()
            m_pair = getattr(self, 'pair%i' % i)
            m_broker = getattr(self, 'acq%i' % i)
            m_cparty = getattr(self, 'cparty%i' % i)
            m_near = getattr(self, 'near%i' % i)
            m_far = getattr(self, 'far%i' % i)
            m_dnear = getattr(self, 'dnear%i' % i)
            m_dfar = getattr(self, 'dfar%i' % i)
            m_pair.SetData(FX_TABLE[i][0])
            m_broker.SetData(FX_TABLE[i][1])
            m_cparty.SetData(FX_TABLE[i][2])
            m_near.SetData(FX_TABLE[i][3])
            m_far.SetData(FX_TABLE[i][4])
            m_dnear.SetData(FX_TABLE[i][5])
            m_dfar.SetData(FX_TABLE[i][6])
            m_clear = getattr(self, 'clear%i' % i)

    def ResetControls(self, i):

            m_pair = getattr(self, 'pair%i' % i)
            m_broker = getattr(self, 'acq%i' % i)
            m_cparty = getattr(self, 'cparty%i' % i)
            m_near = getattr(self, 'near%i' % i)
            m_far = getattr(self, 'far%i' % i)
            m_dnear = getattr(self, 'dnear%i' % i)
            m_dfar = getattr(self, 'dfar%i' % i)
            m_pair.SetData('')
            m_broker.SetData('')
            m_cparty.SetData('')
            m_near.SetData('')
            m_far.SetData('')
            m_dnear.SetData('')
            m_dfar.SetData('')
            self.HideControls(i)

    def InitControls(self):

        for i in range(1, self.CONTROLS):
            getattr(self, 'pair%i' % i).Visible(0)
            getattr(self, 'acq%i' % i).Visible(0)
            getattr(self, 'cparty%i' % i).Visible(0)
            getattr(self, 'near%i' % i).Visible(0)
            getattr(self, 'far%i' % i).Visible(0)
            getattr(self, 'dnear%i' % i).Visible(0)
            getattr(self, 'ddnear%i' % i).Visible(0)
            getattr(self, 'dfar%i' % i).Visible(0)
            getattr(self, 'ddfar%i' % i).Visible(0)
            getattr(self, 'clear%i' % i).Visible(0)

    def HideControls(self, index):

        if getattr(self, 'pair%i' % index).Visible():
            getattr(self, 'pair%i' % index).Visible(0)
            getattr(self, 'acq%i' % index).Visible(0)
            getattr(self, 'cparty%i' % index).Visible(0)
            getattr(self, 'near%i' % index).Visible(0)
            getattr(self, 'far%i' % index).Visible(0)
            getattr(self, 'dnear%i' % index).Visible(0)
            getattr(self, 'ddnear%i' % index).Visible(0)
            getattr(self, 'dfar%i' % index).Visible(0)
            getattr(self, 'ddfar%i' % index).Visible(0)
            getattr(self, 'clear%i' % index).Visible(0)

    def UnhideControls(self, index):

        if not getattr(self, 'pair%i' % index).Visible():
            getattr(self, 'pair%i' % index).Visible(1)
            getattr(self, 'acq%i' % index).Visible(1)
            getattr(self, 'cparty%i' % index).Visible(1)
            getattr(self, 'near%i' % index).Visible(1)
            getattr(self, 'far%i' % index).Visible(1)
            getattr(self, 'dnear%i' % index).Visible(1)
            getattr(self, 'ddnear%i' % index).Visible(1)
            getattr(self, 'dfar%i' % index).Visible(1)
            getattr(self, 'ddfar%i' % index).Visible(1)
            getattr(self, 'clear%i' % index).Visible(1)

    def UpdateCallbacks(self, index):

        getattr(self, 'pair%i' % index).AddCallback('Changed',
                OnPairSelectionChanged, [self, index])
        getattr(self, 'ddnear%i' % index).AddCallback('Activate',
                OnCalendarPressed, [self, getattr(self, 'dnear%i' % index)])
        getattr(self, 'ddfar%i' % index).AddCallback('Activate',
                OnCalendarPressed, [self, getattr(self, 'dfar%i' % index)])
        getattr(self, 'clear%i' % index).AddCallback('Activate',
                OnClearPressed, [self, index])

    def UpdateControls(self):

        self.m_counter += 1
        self.UnhideControls(self.m_counter)
        self.UpdateCallbacks(self.m_counter)

    def PopulateData(self):

        for i in range(0, self.CONTROLS):
            pairCtrl = getattr(self, 'pair%i' % i)
            acqCtrl = getattr(self, 'acq%i' % i)
            cpartyCtrl = getattr(self, 'cparty%i' % i)
            for c in self.pairs:
                pairCtrl.AddItem(c)
            for c in self.acquirers:
                acqCtrl.AddItem(c)
            for c in self.counterparties:
                cpartyCtrl.AddItem(c)

    def AddCallbacks(self):

        self.pair0.AddCallback('Changed', OnPairSelectionChanged,
                [self, self.m_counter])
        self.ddnear0.AddCallback('Activate', OnCalendarPressed,
                [self, self.dnear0])
        self.ddfar0.AddCallback('Activate', OnCalendarPressed,
                [self, self.dfar0])
        self.clear0.AddCallback('Activate', OnClearPressed,
                [self, self.m_counter])

    def GetControls(self, layout):

        self.m_okBtn = layout.GetControl("ok")
        for i in range(self.CONTROLS):
            setattr(self, 'pair%i' % i, layout.GetControl('pair%i' % i))
            setattr(self, 'acq%i' % i, layout.GetControl('acq%i' % i))
            setattr(self, 'cparty%i' % i, layout.GetControl('cparty%i' % i))
            setattr(self, 'near%i' % i, layout.GetControl('near%i' % i))
            setattr(self, 'far%i' % i, layout.GetControl('far%i' % i))
            setattr(self, 'dnear%i' % i, layout.GetControl('dnear%i' % i))
            setattr(self, 'ddnear%i' % i, layout.GetControl('ddnear%i' % i))
            setattr(self, 'dfar%i' % i, layout.GetControl('dfar%i' % i))
            setattr(self, 'ddfar%i' % i, layout.GetControl('ddfar%i' % i))
            setattr(self, 'clear%i' % i, layout.GetControl('clear%i' % i))

    def SetDefaultValues(self):

        defaultExt = acm.GetDefaultContext().GetExtension('FExtensionValue',
                'FObject', 'FxRoll_%s' % self.template)
        if defaultExt and defaultExt.Value():
            ctrls = ['pair%i', 'acq%i', 'cparty%i']
            i = 0
            for row in defaultExt.Value().split('\n'):
                has_value = 0
                for index, value in enumerate(row.split(';')):
                    if value:
                        getattr(self, ctrls[index] % i).SetData(value)
                        has_value = 1
                if has_value:
                    OnPairSelectionChanged([self, self.m_counter], None)
                    i += 1

    def HandleCreate(self, dlg, layout):

        self.m_fuxDlg = dlg
        self.m_fuxLayout = layout
        self.m_fuxDlg.Caption('Fx Rates per Custodian and Currency')
        self.GetControls(layout)
        self.PopulateData()
        self.InitControls()
        self.AddCallbacks()
        if self.params:
            self.SetControls()
        if not (self.parameters['selected'] and FX_TABLE):
            self.SetDefaultValues()

    def AddRow(self, b, index):

        b.  BeginHorzBox('None')
        b.    AddOption('pair%i' % index, '', 14, 14)
        b.    AddOption('acq%i' % index, '', 25, 25)
        b.    AddOption('cparty%i' % index, '', 25, 25)
        b.    AddInput('near%i' % index, '', 15, 15)
        b.    AddInput('far%i' % index, '', 15, 15)
        b.    AddInput('dnear%i' % index, '', 15, 15)
        b.    AddButton('ddnear%i' % index, '...', 1, 1)
        b.    AddInput('dfar%i' % index, '', 15, 15)
        b.    AddButton('ddfar%i' % index, '...', 1, 1)
        b.    AddButton('clear%i' % index, 'Clear', 1, 1)
        b.  EndBox()

    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. BeginVertBox('EtchedIn')
        b.  BeginHorzBox('None')
        b.    AddSpace(4)
        b.    AddLabel('m_cp', 'Currency Pair')
        b.    AddSpace(20)
        b.    AddLabel('m_broker', 'Custodian')
        b.    AddSpace(100)
        b.    AddLabel('m_cparty', 'Executing Broker')
        b.    AddSpace(70)
        b.    AddLabel('m_near', 'Rate Near')
        b.    AddSpace(40)
        b.    AddLabel('m_far', 'Rate Far')
        b.    AddSpace(46)
        b.    AddLabel('d_near', 'Date Near')
        b.    AddSpace(60)
        b.    AddLabel('d_far', 'Date Far')
        b.  EndBox()
        for i in range(self.CONTROLS):
            self.AddRow(b, i)
        b. EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def GetRatesPerBrokerAndCurrency(self):

        out = []
        global FX_TABLE
        FX_TABLE = []
        for i in range(0, self.CONTROLS):
            try:
                if getattr(self, 'pair%i' % i).Visible():
                    pair = getattr(self, 'pair%i' % i).GetData()
                    acq = getattr(self, 'acq%i' % i).GetData()
                    cparty = getattr(self, 'cparty%i' % i).GetData()
                    near = float(re.sub(',', '.', getattr(self,
                            'near%i' % i).GetData()))
                    far = float(re.sub(',', '.', getattr(self,
                            'far%i' % i).GetData()))
                    dnear = getattr(self, 'dnear%i' % i).GetData()
                    dfar = getattr(self, 'dfar%i' % i).GetData()
                    out.append((pair, acq, cparty, near, far, dnear, dfar))
                    FX_TABLE.append((pair, acq, cparty, near, far, dnear,
                            dfar))
            except (AttributeError, ValueError):
                pass
        return out

    def HandleApply(self):

        resultDic = acm.FDictionary()
        self.out = self.GetRatesPerBrokerAndCurrency()
        resultDic.AtPut('result', self.out)
        return resultDic


class TradingDateCustomDialog (FUxCore.LayoutDialog):

    TODAY = acm.Time().DateValueDay()

    def __init__(self, shell, field, calendar):

        year = int(self.__class__.TODAY[:4])
        month = int(self.__class__.TODAY[5:7])
        day = int(self.__class__.TODAY[8:10])
        self.value_day = datetime.date(year, month, day)
        self.calendar = calendar
        self.shell = shell
        self.field = field
        self.result = None

    def ValuationParameters(self):

        return acm.UsedValuationParameters()

    def HandleApply(self):

        if self.field:
            self.field.SetData(self.result)
            return 1
        else:
            resultDic = acm.FDictionary()
            resultDic.AtPut('result', list([self.result]))
            return resultDic

    def IsNonBankingDate(self, date):

        calendar = self.calendar
        return calendar.IsNonBankingDay(calendar, calendar, date)

    def UseDate(self, today):

        self.today = today
        fday = today - datetime.timedelta(today.day - 1)
        fdow = fday.weekday()
        day = fday - datetime.timedelta(fdow)
        self.dates = []
        for b in self.buttons:
            b.Label(str(day.day))
            if day == self.value_day:
                b.SetFocus()
                b.SetFont("", 10, 1, 0)
            else:
                b.SetFont("", 8, 0, 0)
            if self.IsNonBankingDate(day.isoformat()):
                b.SetFont("", 8, 1, 1)
            self.dates.append(day)
            if day.month == today.month:
                b.Enabled(True)
            else:
                b.Enabled(False)
            day = day + datetime.timedelta(1)
        self.lDate.Label(today.strftime('%B %Y'))

    def DatePressed(self, button, cd):

        self.result = None
        date = self.dates[button].isoformat()
        if not self.IsNonBankingDate(date):
            self.result = date
        else:
            msg = ('The date selected is a non banking day in %s calendar' %
                    self.calendar.Name())
            acm.UX().Dialogs().MessageBoxInformation(self.shell, msg)

    def DateDayStep(self, step, cd):

        today = self.today
        next_month = today.month + step
        if next_month is 0:
            next_month_date = datetime.date(today.year + step, 12, 1)
        elif next_month is 13:
            next_month_date = datetime.date(today.year + step, 1, 1)
        else:
            next_month_date = datetime.date(today.year, next_month, 1)
        self.UseDate(next_month_date)

    def HandleCreate(self, dlg, layout):

        dlg.Caption('%s Calendar' % self.calendar.Name())
        self.buttons = []
        for r in range(6):
            for c in range(7):
                db = layout.GetControl("b%d%d" % (r, c))
                db.SetFont("", 8, 0, 0)
                db.AddCallback("Activate", self.DatePressed, r * 7 + c)
                self.buttons.append(db)
        layout.GetControl("bnm").AddCallback("Activate", self.DateDayStep, 1)
        layout.GetControl("bpm").AddCallback("Activate", self.DateDayStep, -1)
        self.lDate = layout.GetControl("lDate")
        lsa = layout.GetControl("lsa")
        lsu = layout.GetControl("lsu")
        today = self.value_day
        self.UseDate(today)

    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. BeginVertBox('EtchedIn')
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton("bpm", "<", False, True)
        b.  AddSpace(20)
        b.  AddLabel('lDate', '')
        b.  AddButton("bnm", ">", False, True)
        b. EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        for day in ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']:
            b. AddLabel('l%s' % day, day)
            b. AddSpace(8)
        b.  EndBox()
        for r in range(6):
            b. BeginHorzBox('None')
            b.  AddFill()
            for c in range(7):
                b. AddButton("b%d%d" % (r, c), "%d%d" % (r, c), 1, 1)
            b. EndBox()
        b. EndBox()
        b. AddFill()
        b. BeginHorzBox('None')
        b. AddFill()
        b.  AddButton('ok', 'OK', False, False)
        b.  AddButton('cancel', 'Cancel', False, False)
        b. AddFill()
        b. EndBox()
        b.EndBox()
        return b


def SelectObjOnAddClicked(self, cd):

    key = self.m_keys.GetData()
    if key:
        SelectObjAddItem(self.valueList, self.m_values, key)
        SelectObjRemoveItem(self.keyList, self.m_keys, key)


def SelectObjAddItem(objList, itemList, item):

    objList.Add(item)
    objList.SortByProperty('Name')
    itemList.Populate(objList)
    itemList.SetData(item)


def SelectObjRemoveItem(objList, itemList, item):

    index = objList.IndexOf(item)
    objList.Remove(item)
    itemList.RemoveItem(item)
    if objList:
        if len(objList) <= index:
            index -= 1
        newItem = objList[index]
        if newItem:
            itemList.SetData(newItem)


def SelectObjOnRemoveClicked(self, cd):

    value = self.m_values.GetData()
    if value:
        SelectObjAddItem(self.keyList, self.m_keys, value)
        SelectObjRemoveItem(self.valueList, self.m_values, value)


def SelectObjOnRemoveAllClicked(self, cd):

    for key in self.valueList:
        self.keyList.Add(key)
    self.valueList = acm.FList()
    self.m_values.Clear()
    self.keyList.SortByProperty('Name')
    self.m_keys.Populate(self.keyList)
    SelectFirstItem(self.keyList, self.m_keys)


class SelectObjCustomDialog(FUxCore.LayoutDialog):

    KEYS = 'keys'
    VALUES = 'values'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    def __init__(self, shell, params, header):

        self.shell = shell
        self.choices = params['choices']
        self.selected = params['selected']
        self.caption = 'Select %s' % header
        self.keyLabel = header
        self.valueLbl = 'Selected %s' % header
        self.keyList = acm.FList()
        self.valueList = acm.FList()
        self.keyObj = None
        self.query = None
        self.m_keys = None
        self.m_fuxDlg = None
        self.m_values = None
        self.m_btnAdd = None
        self.m_btnRemove = None
        self.m_btnRemoveAll = None

    def HandleApply(self):

        resultDic = acm.FDictionary()
        resultDic.AtPut('result', list(self.valueList))
        return resultDic

    def HandleCreate(self, dlg, layout):

        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_keys = layout.GetControl(self.KEYS)
        self.m_values = layout.GetControl(self.VALUES)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate', SelectObjOnAddClicked, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate', SelectObjOnRemoveClicked,
                self)
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate',
                SelectObjOnRemoveAllClicked, self)
        self.PopulateControls()
        self.SetControlData()

    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel("lblKeys", self.keyLabel)
        b.   AddList(self.KEYS, 10, -1, 50, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        b.   AddSpace(3)
        b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel("lblValues", self.valueLbl)
        b.   AddList(self.VALUES, 10, -1, 50, -1)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

    def PopulateControls(self):

        self.keyList = self.LoadData(self.keyObj)
        if self.keyList:
            self.m_keys.Populate(self.keyList)
            self.m_keys.SetData(self.keyList.First())
        else:
            print(('The query "{0}" on FStoredASQLQuery did not produce any '
                    'result'.format(self.query)))

    def SetControlData(self):

        for key in self.selected:
            key = getattr(acm, self.keyObj)[key]
            self.keyList.Remove(key)
            self.valueList.Add(key)
        self.m_keys.Populate(self.keyList)
        self.valueList.SortByProperty('Name')
        self.m_values.Populate(self.valueList)
        SelectFirstItem(self.keyList, self.m_keys)
        SelectFirstItem(self.valueList, self.m_values)

    def LoadData(self, objName):

        collection = getattr(acm, objName).Select(self.query)
        return collection.SortByProperty('Name')


class SelectACMQueriesCustomDialog(SelectObjCustomDialog):

    def __init__(self, shell, params, queryPrefix='', subType='',
            header='ACM Queries'):

        SelectObjCustomDialog.__init__(self, shell, params, header)
        self.keyObj = 'FStoredASQLQuery'
        #subtype_str = 'and subType = "%s"' % subType if subType else ''
        #self.query = 'user = "" %s and name like %s' % (subtype_str,
        #        queryPrefix+'*')
        self.query = ''
