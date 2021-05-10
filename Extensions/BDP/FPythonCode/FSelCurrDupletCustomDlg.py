""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FSelCurrDupletCustomDlg.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FSelCurrDupletCustomDlg.py - Custom dialog for select currency duplets.

    (c) Copyright 2012 by SunGard Front Arena AB. All rights reserved.

DESCRIPTION

NOTE
    Currency Duplets - refers to a pair of two arbitrarily selected
            currencies arranged in no particular order, which may or may not
            be one of the defined currency pair
ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm


import FUxCore


CURRPAIR_ANNOTATION = '[*]'
CURRDUPLET_SEPARATOR = '/'


class SelectCurrDupletCustomDlg(FUxCore.LayoutDialog):

    LIST_VAL_CURR1 = 'lstValueCurr1'
    LIST_VAL_CURR2 = 'lstValueCurr2'
    LIST_SEL_CURRDUPLET = 'lstSelectedCurrDuplet'
    LABEL_VAL_CURR1 = 'labelValueCurr1'
    LABEL_VAL_CURR2 = 'labelValueCurr2'
    LABEL_SEL_CURRDUPLET = 'labelSelectedCurrDuplet'
    LABEL_CURRDUPLET_NOTE = 'labelCurrDupletNote'
    BUTTON_ADD = 'buttonAdd'
    BUTTON_REMOVE = 'buttonRemove'
    BUTTON_REMOVE_ALL = 'buttonRemoveAll'
    CAPTION = 'Select Pairs of Currencies'
    LABEL_VAL_CURR1_TEXT = 'Currency 1'
    LABEL_VAL_CURR2_TEXT = 'Currency 2'
    LABEL_SEL_CURRDUPLET_TEXT = 'Selected pairs of currencies'
    LABEL_CURRDUPLET_NOTE_TEXT = CURRPAIR_ANNOTATION + ' Defined Currency Pair'

    BUTTON_ADD_TEXT = 'Add'
    BUTTON_REMOVE_TEXT = 'Remove'
    BUTTON_REMOVE_ALL_TEXT = 'Remove All'

    def __init__(self, params):
        self.selected = params['selected']
        self.__currNameList = sorted([curr.Name() for curr in
                acm.FCurrency.Select('')])
        self.__defCurrPairNameList = sorted([currPair.Name() for currPair in
                acm.FCurrencyPair.Select('')])
        self.__shadowSelCurrDupletList = []
        # The following are to be created in HandleCreate
        self.m_fuxDlg = None
        self.m_lstValCurr1 = None
        self.m_lstValCurr2 = None
        self.m_lstSelCurrDuplet = None
        self.m_btnAdd = None
        self.m_btnRemove = None
        self.m_btnRemoveAll = None
        # The above are to be created in HandleCreate

    def HandleApply(self):
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', self.__shadowSelCurrDupletList)
        return resultDic

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.CAPTION)
        self.m_lstValCurr1 = layout.GetControl(self.LIST_VAL_CURR1)
        self.m_lstValCurr2 = layout.GetControl(self.LIST_VAL_CURR2)
        self.m_lstValCurr2.EnableMultiSelect(True)
        self.m_lstSelCurrDuplet = layout.GetControl(self.LIST_SEL_CURRDUPLET)
        self.m_btnAdd = layout.GetControl(self.BUTTON_ADD)
        self.m_btnAdd.AddCallback('Activate',
                self.onAddClicked.__func__, self)
        self.m_btnRemove = layout.GetControl(self.BUTTON_REMOVE)
        self.m_btnRemove.AddCallback('Activate',
                self.onRemoveClicked.__func__, self)
        self.m_btnRemoveAll = layout.GetControl(self.BUTTON_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate',
                self.onRemoveAllClicked.__func__, self)
        self.__populateData()
        self.__updateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel(self.LABEL_VAL_CURR1, self.LABEL_VAL_CURR1_TEXT)
        b.   AddList(self.LIST_VAL_CURR1, 10, -1, 20, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddLabel(self.LABEL_VAL_CURR1, self.LABEL_VAL_CURR2_TEXT)
        b.   AddList(self.LIST_VAL_CURR2, 10, -1, 20, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BUTTON_ADD, self.BUTTON_ADD_TEXT)
        b.   AddButton(self.BUTTON_REMOVE, self.BUTTON_REMOVE_TEXT)
        b.   AddSpace(3)
        b.   AddButton(self.BUTTON_REMOVE_ALL, self.BUTTON_REMOVE_ALL_TEXT)
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel(self.LABEL_SEL_CURRDUPLET,
                    self.LABEL_SEL_CURRDUPLET_TEXT)
        b.   AddList(self.LIST_SEL_CURRDUPLET, 10, -1, 30, -1)
        b.   AddLabel(self.LABEL_CURRDUPLET_NOTE,
                    self.LABEL_CURRDUPLET_NOTE_TEXT)
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

    def __populateData(self):
        self.m_lstValCurr1.Populate(self.__currNameList)
        self.m_lstValCurr2.Populate(self.__currNameList)
        validCurrDupletNames = []
        for currDupletName in self.selected:
            curr1Name, curr2Name = currDupletName.split(
                    CURRDUPLET_SEPARATOR)[0:2]
            if curr1Name not in self.__currNameList:
                continue
            if curr2Name not in self.__currNameList:
                continue
            currDupletName = self.__getOrderedCurrDupletName(curr1Name,
                    curr2Name)
            if currDupletName in self.__shadowSelCurrDupletList:
                continue
            reversedCurrDupletName = self.__getReversedCurrDupletName(
                    currDupletName)
            if reversedCurrDupletName in self.__shadowSelCurrDupletList:
                continue
            validCurrDupletNames.append(currDupletName)
        # Setup up the shadow list to be pupulated during 'update'
        self.__shadowSelCurrDupletList = sorted(validCurrDupletNames)

    def __updateControls(self):
        self.__updateListSelCurrDuplet()

    def __updateListSelCurrDuplet(self):
        annotatedCurrDupletNameList = [
                self.__getAnnotatedCurrDupletName(currDupletName) for
                currDupletName in self.__shadowSelCurrDupletList]
        self.m_lstSelCurrDuplet.Clear()
        self.m_lstSelCurrDuplet.Populate(annotatedCurrDupletNameList)

    def __getReversedCurrDupletName(self, currDupletName):
        return CURRDUPLET_SEPARATOR.join(currDupletName.split(
                CURRDUPLET_SEPARATOR)[::-1])

    def __getAnnotatedCurrDupletName(self, currDupletName):
        if currDupletName in self.__defCurrPairNameList:
            annotatedCurrDupletName = (currDupletName +
                    ' ' + CURRPAIR_ANNOTATION)
        else:
            annotatedCurrDupletName = currDupletName
        return annotatedCurrDupletName

    def __getDeAnnotatedCurrDupletName(self, annotatedCurrDupletName):
        currDupletName = annotatedCurrDupletName.split(
                ' ' + CURRPAIR_ANNOTATION)[0]
        return currDupletName

    def __getOrderedCurrDupletName(self, curr1Name, curr2Name):
        # Test if the reverse duplet is a defined currency pair first.
        currDupletName = curr2Name + CURRDUPLET_SEPARATOR + curr1Name
        if currDupletName in self.__defCurrPairNameList:
            return currDupletName
        # Return direct duplet
        return curr1Name + CURRDUPLET_SEPARATOR + curr2Name

    def __makeCurrDupletNames(self, curr1Name, curr2NameList):
        # Remove if curr2NameList contains curr1Name
        curr2NameSet = [currName for currName in set(curr2NameList)
                if currName != curr1Name]
        # Return the ordered currency duplet name made from curr1Name and every
        # one of the curr2Name.
        return sorted([self.__getOrderedCurrDupletName(curr1Name, curr2Name)
                for curr2Name in curr2NameSet])

    def onAddClicked(self, _cd):
        # Populate/de-populate controls' data
        curr1Item = self.m_lstValCurr1.GetSelectedItem()
        curr2Items = self.m_lstValCurr2.GetSelectedItems()
        if not curr1Item or not curr2Items:
            return
        curr1Name = curr1Item.GetData()
        curr2NameList = [curr2Item.GetData() for curr2Item in curr2Items]
        currDupletNames = [currDupletName for currDupletName in
                self.__makeCurrDupletNames(curr1Name, curr2NameList)
                if currDupletName not in self.__shadowSelCurrDupletList and
                self.__getReversedCurrDupletName(currDupletName) not in
                self.__shadowSelCurrDupletList]
        self.__shadowSelCurrDupletList = sorted(
                self.__shadowSelCurrDupletList + currDupletNames)
        # Update controls
        self.__updateControls()

    def onRemoveClicked(self, _cd):
        # Populate/de-populate controls' data
        currDupletItem = self.m_lstSelCurrDuplet.GetSelectedItem()
        if not currDupletItem:
            return
        annotatedCurrDupletName = currDupletItem.GetData()
        currDupletName = self.__getDeAnnotatedCurrDupletName(
                annotatedCurrDupletName)
        self.__shadowSelCurrDupletList.remove(currDupletName)
        # Update controls
        self.__updateControls()

    def onRemoveAllClicked(self, _cd):
        # Populate/de-populate controls' data
        self.__shadowSelCurrDupletList = []
        # Update controls
        self.__updateControls()
