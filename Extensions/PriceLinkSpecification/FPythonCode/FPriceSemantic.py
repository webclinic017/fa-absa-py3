""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceSemantic.py"
from __future__ import print_function
"""--------------------------------------------------------------------
MODULE

    PriceSemantic - creates a Price Semantic GUI.

DESCRIPTION

    This script creates the Price Semantic GUI using FAUx.
    It displays attributes of the stored price Semantic.
    It also enables the updating, adding and deleting
    of Price Semantic.

--------------------------------------------------------------------"""

import acm
import FUxCore

import FPriceLinkApplication as CB
from FPriceLinkApplication import PriceLinkApplication
import FPriceLinkMenu as Menu
import FPriceLinkToolTips as ToolTips
import FPriceLinkSpecificationUtils as Utils

import FTimeStampsCustomDialog as TimeStampsDialog
import FProtectionCustomDialog as ProtectionDialog

from FPriceLinkSpecificationUtils import ButtonOptions, SYMBOL_PLUSMINUS
from FPriceSemanticListHandler import FPriceSemanticListHandler as SemanticListHandler

from FPriceLinkApplicationStates import PriceSemanticStates as States
from FPriceLinkApplicationStates import SemanticColumns
from FPriceLinkApplicationStates import ADMFields
from FPriceLinkApplicationStates import PermittedDistributorTypes as DistributorType

APPLICATION_NAME =  "Price Semantic"
ApplicationObject = None

"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++                                                                ++
++      SEMANTIC OPERATIONS                                       ++
++                                                                ++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

def GetSemanticReferences(PriceSemanticDlg, pldRef, distRef):
    print('Unable to delete the semantic.')
    if pldRef:
        print('The Semantic ' + PriceSemanticDlg.price_semantic.GetData() + " has reference(s) in following price link(s):")
    for pld in pldRef:
        print("IDPCode:<"+ pld.IdpCode() + ">, Instrument:<" + pld.Instrument().Name() + ">, Currency:<" + pld.Currency().Name() + '> in DISTRIBUTOR:' + pld.PriceDistributor().Name())
    
    if distRef:
        print('The Semantic ' + PriceSemanticDlg.price_semantic.GetData() + " has reference(s) in following distributor(s):")
    for dist in distRef:
        print(dist.Name())
    return

def OnDeleteSemanticSelected(PriceSemanticDlg, arg):
    """Action when Delete is clicked"""
    priceSemanticName = PriceSemanticDlg.price_semantic.GetData()
    if not priceSemanticName:
        PriceSemanticDlg.ShowError('Please select a valid Price Semantic.')
        return

    priceSemantic = acm.FPriceSemantic[priceSemanticName]
    if not priceSemantic:
        PriceSemanticDlg.ShowError('Please select a valid Price Semantic.')
        return
    
    refCount = acm.FPriceLinkDefinition.Select('semanticSeqNbr="%d"'%(priceSemantic.Oid()))
    refDistCount = acm.FPriceDistributor.Select('semanticSeqNbr="%d"'%(priceSemantic.Oid()))
    if refCount.Size() + refDistCount.Size() > 20:
        message =  "Semantic <" + priceSemanticName + "> has references in:\n" + str(refCount.Size()) + " Price Link(s) and \n" + str(refDistCount.Size()) + " Distributor(s).\n"\
                   + "Remove these references and try again."
        PriceSemanticDlg.ShowError(message)
        return
    elif refCount.Size() + refDistCount.Size() > 0:
        message =  "Semantic <" + priceSemanticName + "> has references in:\n" + str(refCount.Size()) + " Price Link(s) and \n" + str(refDistCount.Size()) + " Distributor(s).\n"\
                   + "Remove these references and try again. Check the log for list of references."
        PriceSemanticDlg.ShowError(message)
        GetSemanticReferences(PriceSemanticDlg, refCount, refDistCount)
        return
    
    message = 'Do you want to delete Price Semantic %s?' % priceSemanticName
    choice = PriceSemanticDlg.ShowQuestion(message)
    if choice == ButtonOptions.CANCEL:
        return

    try:
        priceSemantic.Delete()
        clear_all_fields(PriceSemanticDlg)
        PriceSemanticDlg.price_semantic.RemoveItem(priceSemanticName)
        print('Semantic ' + priceSemanticName + ' has been successfully deleted!')
        PriceSemanticDlg.SetState(States.PSOpened)
    except Exception as e:
        message = "Failed to Commit. \nError_Description : " + str(e)
        PriceSemanticDlg.ShowError(message)
        

def OnSaveSemanticSelected(PriceSemanticDlg, arg):
    """Action when Save is clicked"""
    priceSemanticName = PriceSemanticDlg.price_semantic.GetData().strip()
    if not priceSemanticName:
        PriceSemanticDlg.ShowError('Please enter semantic name')
        return

    isPriceSemanticRenamed = False
    priceSemantic = acm.FPriceSemantic[priceSemanticName]
    if not priceSemantic:
        #Create new Price Semantic
        message = 'Semantic %s does not exist.\n' %(priceSemanticName)\
                + 'Do you want to rename existing Price Semantic?'
        choice = PriceSemanticDlg.ShowQuestion(message)
        if choice == ButtonOptions.CANCEL:
            return

        priceSemantic = acm.FPriceSemantic[PriceSemanticDlg.semantic]
        if priceSemantic:
            priceSemantic.Name = priceSemanticName
            isPriceSemanticRenamed = True
        else:
            return

    try:
        update_price_semantic(PriceSemanticDlg, priceSemantic)
        priceSemantic.Commit()

        if isPriceSemanticRenamed:
            PriceSemanticDlg.price_semantic.RemoveItem(PriceSemanticDlg.semantic)
            PriceSemanticDlg.price_semantic.AddItem(priceSemanticName)

        PriceSemanticDlg.SetState(States.PSPopulated)

    except ValueError as e:
        PriceSemanticDlg.ShowError(str(e))
    except Exception as e:
        message = "Failed to Commit. \nError_Description : " + str(e)
        PriceSemanticDlg.ShowError(message)

def OnSaveNewSemanticSelected(PriceSemanticDlg, arg):
    """Action when Save New is clicked"""
    priceSemanticName = PriceSemanticDlg.price_semantic.GetData().strip()
    if not priceSemanticName:
        PriceSemanticDlg.ShowError('Please enter a semantic name')
        return
    
    values = PriceSemanticDlg.GetSemanticAttributeValues()
    validationError = ValidateMandatorySemanticFields(PriceSemanticDlg, values)
    if validationError:
        return
    
    priceSemantic = acm.FPriceSemantic[priceSemanticName]
    if priceSemantic:
        message = 'Semantic ' + priceSemanticName + ' already exists! \n Duplicates are not permitted!!'
        PriceSemanticDlg.ShowError(message)
        return

    try:
        newPriceSemantic = acm.FPriceSemantic()
        newPriceSemantic.Name = priceSemanticName
        update_price_semantic(PriceSemanticDlg, newPriceSemantic)
        newPriceSemantic.Commit()
        PriceSemanticDlg.price_semantic.AddItem(priceSemanticName)
        selectedFieldMappings = PriceSemanticDlg.semanticList.GetSelectedfieldMappings()
        PriceSemanticDlg.semantic_list.Clear()
        if selectedFieldMappings:
            for fieldMapping in selectedFieldMappings:
                row = acm.FPriceSemanticRow()
                row.SemanticSeqNbr(newPriceSemantic.Oid())
                row.AdmName(fieldMapping.AdmName())
                row.IdpName(fieldMapping.IdpName())
                row.Comment(fieldMapping.Comment())
                PriceSemanticDlg.semanticList.Add(row)
            
        print('Semantic ' + priceSemanticName + ' has been successfully created!')
        selectedRows = PriceSemanticDlg.semanticList.GetSelectedRows()
        if selectedRows:
            PriceSemanticDlg.SetState(States.PSMultiSelected)
        else:    
            PriceSemanticDlg.SetState(States.PSPopulated)
        
    except ValueError as e:
        PriceSemanticDlg.ShowError(str(e))
    except Exception as e:
        message = "Failed to Commit. Error_Description : " + str(e)
        PriceSemanticDlg.ShowError(message)

"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++                                                                ++
++      SEMANTIC ROW OPERATIONS                                   ++
++                                                                ++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

def OnAddSelected(PriceSemanticDlg, arg):
    """Action when Save Add is clicked"""
    priceSemanticName = PriceSemanticDlg.price_semantic.GetData()
    priceSemantic = acm.FPriceSemantic[priceSemanticName]
    if priceSemantic:
        values = PriceSemanticDlg.GetRowsAttributeValues()
        validationError = ValidateMandatoryMappingFields(PriceSemanticDlg, values)
        if validationError:
            return
            
        row = acm.FPriceSemanticRow()
        row.SemanticSeqNbr(priceSemantic.Oid())
        ApplyFullRowUpdate(values, row)
        PriceSemanticDlg.semanticList.Add(row)
        PriceSemanticDlg.SetState(States.PSAdded)

def OnUpdateSelected(PriceSemanticDlg, arg):
    """Action when Save Add is clicked"""
    if PriceSemanticDlg.semanticList.IsMultiSelect():
        clear_fields(PriceSemanticDlg)
        message = 'Updating multiple field mappings together not allowed \nsince it may result in duplicate mappings!'
        PriceSemanticDlg.ShowError(message)
        return
    
    else:
        values = PriceSemanticDlg.GetRowsAttributeValues()
        validationError = ValidateMandatoryMappingFields(PriceSemanticDlg, values)
        if validationError:
            return
        
        row = PriceSemanticDlg.semanticList.GetSelectedRow()
        sem = PriceSemanticDlg.semanticList.GetSemanticObject(row)
        clone = sem.Clone()
        ApplyFullRowUpdate(values, clone)

        operation = "U"
        if "A" == PriceSemanticDlg.semanticList.GetOperationType(row):
            operation = "A"

        PriceSemanticDlg.semanticList.Update(operation, clone, row)
        row.EnsureVisible()
        PriceSemanticDlg.SetState(States.PSUpdated)

def OnDeleteSelected(PriceSemanticDlg, arg):
    """Action when Delete is clicked"""
    PriceSemanticDlg.semanticList.Remove()
    clear_fields(PriceSemanticDlg)
    PriceSemanticDlg.SetState(States.PSUpdated)
        
def OnRevertSelected(PriceSemanticDlg, arg):
    """Action when Delete is clicked"""
    PriceSemanticDlg.semanticList.Revert()
    clear_fields(PriceSemanticDlg)
    PriceSemanticDlg.SetState(States.PSSelected)

def OnSaveSelected(PriceSemanticDlg, arg):
    """Action when Save is clicked"""
    PriceSemanticDlg.semanticList.Save()
    clear_fields(PriceSemanticDlg)
    rows = PriceSemanticDlg.semanticList.GetSelectedRows()
    if not rows:
        clear_fields(PriceSemanticDlg)
        PriceSemanticDlg.SetState(States.PSPopulated)
    else:
        if PriceSemanticDlg.semanticList.IsMultiSelect():
            flag = 0
            for aRow in rows:
                if PriceSemanticDlg.semanticList.IsModified(aRow):
                    flag = 1
                    break
            if flag:
                PriceSemanticDlg.SetState(States.PSMultiSelected)
            else:
                PriceSemanticDlg.SetState(States.PSSelected)
        else:
            row = PriceSemanticDlg.semanticList.GetSelectedRow()
            opType = PriceSemanticDlg.semanticList.GetOperationType(row)
            if opType in ["U", "R"]:
                PriceSemanticDlg.SetState(States.PSUpdated)
            elif opType == 'A':
                PriceSemanticDlg.SetState(States.PSAdded)
            else:
                PriceSemanticDlg.SetState(States.PSSelected)
    
def OnClearSelected(PriceSemanticDlg, arg):
    """Actions when Clear is clicked"""
    clear_all_fields(PriceSemanticDlg)
    PriceSemanticDlg.SetState(States.PSPopulated)
	
def OnClearSelectionSelected(PriceSemanticDlg, arg):
    """Actions when Clear Selection is clicked"""
    PriceSemanticDlg.semanticList.SelectAllItems(False)
    clear_fields(PriceSemanticDlg)
    PriceSemanticDlg.SetState(States.PSPopulated)
    
def OnTimeStampsSelected(PriceSemanticDlg, arg):
    """Action when Time Stamps is clicked"""
    priceSemantic = acm.FPriceSemantic[PriceSemanticDlg.price_semantic.GetData()]
    priceSemantic = acm.FPriceSemantic.Select01('name="%s"' % PriceSemanticDlg.price_semantic.GetData(), None)
    TimeStampsDialog.StartDialog(PriceSemanticDlg.Shell(), priceSemantic)

def OnProtectionSelected(PriceSemanticDlg, arg):
    """Actions when Protection is clicked"""
    oldOwner = PriceSemanticDlg.owner
    oldProtection = PriceSemanticDlg.protection
    shell = PriceSemanticDlg.Shell()
    newOwner, newProtection = ProtectionDialog.StartDialog(shell, oldOwner, oldProtection)
    if (oldOwner.Name() != newOwner.Name()) or (oldProtection != newProtection):
        PriceSemanticDlg.owner = newOwner
        PriceSemanticDlg.protection = newProtection
        OnAnyFieldSelected(PriceSemanticDlg, None)

def OnPriceSemanticSelected(PriceSemanticDlg, arg):
    """Actions when New is clicked"""
    priceSemanticName = PriceSemanticDlg.price_semantic.GetData()
    priceSemantic = acm.FPriceSemantic[priceSemanticName]

    if priceSemantic and priceSemantic.Name() == priceSemanticName:
        PriceSemanticDlg.semantic = priceSemanticName
        PriceSemanticDlg.provider_type.SetData(priceSemantic.ProviderType())
        PriceSemanticDlg.semantic_comment.SetData(priceSemantic.Comment())
        PriceSemanticDlg.owner = priceSemantic.Owner()
        PriceSemanticDlg.protection = priceSemantic.Protection()
        populateSemanticGrid(PriceSemanticDlg, priceSemantic)
        clear_fields(PriceSemanticDlg)
        selectedRows = PriceSemanticDlg.semanticList.GetSelectedRows()
        if selectedRows:
            PriceSemanticDlg.SetState(States.PSMultiSelected)
        else:    
            PriceSemanticDlg.SetState(States.PSPopulated)
    else:
        PriceSemanticDlg.SetState(States.PSModified)

def OpenPriceSemantic(PriceSemanticDlg, priceSemanticName):
    priceSemantic = acm.FPriceSemantic[priceSemanticName]

    if priceSemantic and priceSemantic.Name() == priceSemanticName:
        PriceSemanticDlg.semantic = priceSemanticName
        PriceSemanticDlg.price_semantic.SetData(priceSemanticName)
        PriceSemanticDlg.provider_type.SetData(priceSemantic.ProviderType())
        PriceSemanticDlg.semantic_comment.SetData(priceSemantic.Comment())
        PriceSemanticDlg.owner = priceSemantic.Owner()
        PriceSemanticDlg.protection = priceSemantic.Protection()
        populateSemanticGrid(PriceSemanticDlg, priceSemantic)
        clear_fields(PriceSemanticDlg)
        PriceSemanticDlg.SetState(States.PSPopulated)
        
def OnSemanticListSelectionChanged(PriceSemanticDlg, arg):
    rows = PriceSemanticDlg.semanticList.GetSelectedRows()
    if not rows:
        clear_fields(PriceSemanticDlg)
        PriceSemanticDlg.SetState(States.PSPopulated)
        return

    if PriceSemanticDlg.semanticList.IsMultiSelect():
        clear_fields(PriceSemanticDlg)
        PriceSemanticDlg.SetState(States.PSMultiSelected)
    else:
        clear_fields(PriceSemanticDlg)
        row = rows[0]
        semantic = PriceSemanticDlg.semanticList.GetSemanticObject(row)
        set_semantic_attributes(PriceSemanticDlg, semantic)
        PriceSemanticDlg.SetState(States.PSSelected)

    for aRow in rows:
        opType = PriceSemanticDlg.semanticList.GetOperationType(aRow)
        if opType in ["U", "R"]:
            PriceSemanticDlg.SetState(States.PSUpdated)
        elif opType == 'A':
            PriceSemanticDlg.SetState(States.PSAdded)

def OnADMFieldChanged(PriceSemanticDlg, arg):
    PriceSemanticDlg.SetState(States.PSChanged)

def OnIDPFieldChanged(PriceSemanticDlg, arg):
    PriceSemanticDlg.SetState(States.PSChanged)

def OnMappingCommentChanged(PriceSemanticDlg, arg):
    PriceSemanticDlg.SetState(States.PSChanged)

def OnProviderTypeChanged(PriceSemanticDlg, arg):
    PriceSemanticDlg.SetState(States.PSModified)
    
def OnSemanticCommentChanged(PriceSemanticDlg, arg):
    PriceSemanticDlg.SetState(States.PSModified)

def populateSemanticGrid(PriceSemanticDlg, priceSemantic):
    semRowArray = getSemanticFromDB(priceSemantic)
    NewPriceSemanticName = PriceSemanticDlg.price_semantic.GetData().strip()
    PriceSemanticDlg.semanticList.Populate(semRowArray, NewPriceSemanticName)
    
def getSemanticFromDB(priceSemantic):
    semRowArray = acm.FPriceSemanticRow.Select('semanticSeqNbr="%d"' % (priceSemantic.Oid()))
    return semRowArray

"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++                                                                ++
++      COMMON FUNCTIONS                                          ++
++                                                                ++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

def set_semantic_attributes(PriceSemanticDlg, semantic):
    if not semantic:
        return
    else:
        PriceSemanticDlg.adm_field.SetData(semantic.AdmName())
        PriceSemanticDlg.idp_field.SetData(semantic.IdpName())
        PriceSemanticDlg.comments.SetData(semantic.Comment())

def clear_all_fields(priceSemanticDlg):
    priceSemanticDlg.semantic_list.Clear()
    priceSemanticDlg.price_semantic.SetData("")
    priceSemanticDlg.provider_type.SetData("")
    priceSemanticDlg.semantic_comment.SetData("")
    clear_fields(priceSemanticDlg)

def clear_fields(priceSemanticDlg):
    priceSemanticDlg.adm_field.SetData("")
    priceSemanticDlg.idp_field.SetData("")
    priceSemanticDlg.comments.SetData("")

def ValidateMandatoryMappingFields(priceSemanticDlg, values):
    mandatoryFields = ('AdmName', 'IdpName')
    missingFields = []

    for field in mandatoryFields:
        if not values[field]:
            missingFields.append(field)

    if missingFields:
        missingFields = '\n\t'.join(missingFields)
        message = 'This semantic mapping is invalid. \n' +\
                'Please update/add the following and try again: \n\t' + missingFields
        priceSemanticDlg.ShowError(str(message))
        return 1
    else:
        return 0
        
def ValidateMandatorySemanticFields(priceSemanticDlg, values):
    mandatoryFields = ('Name', 'ProviderType')
    missingFields = []

    for field in mandatoryFields:
        if not values[field]:
            missingFields.append(field)

    if missingFields:
        missingFields = '\n\t'.join(missingFields)
        message = 'This semantic is invalid. \n' +\
                'Please update/add the following and try again: \n\t' + missingFields
        priceSemanticDlg.ShowError(str(message))
        return 1
    else:
        return 0

def ApplyFullRowUpdate(values, sem_row):
    sem_row.AdmName = values['AdmName']
    sem_row.IdpName = values['IdpName']
    sem_row.Comment = values['Comment']

def update_price_semantic(PriceSemanticDlg, newPriceSemantic):
    newPriceSemantic.ProviderType = PriceSemanticDlg.provider_type.GetData()
    newPriceSemantic.Comment = PriceSemanticDlg.semantic_comment.GetData()
    newPriceSemantic.Owner = PriceSemanticDlg.owner
    newPriceSemantic.Protection = PriceSemanticDlg.protection
    return newPriceSemantic

"""***********************PriceSemanticApplication************************************"""
class PriceSemanticApplication(PriceLinkApplication):

    def __init__(self):

        PriceLinkApplication.__init__(self)
        self.m_fuxDlg    = 0
        self.binder      = None
        self.state = States.PSOpened
        self.ADMField = ""
        self.semantic = None

    def SetPriceSemantic(self, priceSemanticName):
        """Set Price link specification application object"""
        self.price_semantic = priceSemanticName
        self.semantic = priceSemanticName

    def InitControls(self):
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)
    
    def HandleGetContents(self):
        dict = acm.FDictionary()
        dict.AtPut("plsListColumns", SemanticColumns)
        return dict

    def HandleSetContents(self, contents):
        return

    def HandleRegisterCommands(self, builder):
        """Register all the commands and its parameters"""

        saveMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Save', OnSaveSelected).Instance
        saveNewMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Save New', OnSaveNewSemanticSelected).Instance
        deleteMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Delete', OnDeleteSelected).Instance
        revertMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Revert', OnRevertSelected).Instance
        addMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Add', OnAddSelected).Instance
        updateMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Update', OnUpdateSelected).Instance
        clearMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Clear', OnClearSelected).Instance
        clearSelectionMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Clear Selection', OnClearSelectionSelected).Instance
        protectionMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Protection', OnProtectionSelected).Instance
        timeStampsMenu = Menu.PriceSemanticToolsPanelCommandsHandler(self, 'Time Stamp', OnTimeStampsSelected).Instance

        ListOfSupportedCommands =\
        [#Name         , parent, Display Name  , tooltiptext                                 , accelerator, mnemonic, callback  , default
        ['Save', 'Edit', 'Save', 'Save selected Semantic mapping', 'Ctrl+S', 'S', saveMenu, False ],
        ['Save New', 'Edit', 'Save New', 'save as new Price Semantic', 'Ctrl+N', 'N', saveNewMenu, False ],
        ['Delete', 'Edit', 'Delete', 'Delete the selected Price Semantic Mapping', 'Ctrl+Delete', 'D', deleteMenu, False ],
        ['Revert', 'Edit', 'Revert', 'Revert the changes done to Price Semantic Mapping', 'Ctrl+Z', 'Z', revertMenu, False ],
        ['Clear', 'Edit', 'Clear', 'Clear all fields', 'Ctrl+Shift+C', 'C', clearMenu, False ],
        ['Clear Selection', 'Edit', 'Clear Selection', 'Clear selected fields', 'Ctrl+Alt+C', 'X', clearSelectionMenu, False ],
        ['Add', 'Edit', 'Add', 'Add Price Semantic Mapping', 'Ctrl+I', 'A', addMenu, False ],
        ['Update', 'Edit', 'Update', 'Update Price Semantic Mapping', 'Ctrl+U', 'U', updateMenu, False ],
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
            OnSaveSemanticSelected(self, None)
        elif commandName == 'FileSaveNew':
            OnSaveNewSemanticSelected(self, None)
        elif commandName == 'FileDelete':
            OnDeleteSemanticSelected(self, None)

    def HandleStandardFileCommandEnabled(self, commandName):
        if commandName == 'FileSave':
            return bool((self.state & States.PSPopulated) and (self.state & States.PSModified))
        if commandName == 'FileSaveNew':
            return bool((self.state & States.PSPopulated) or (self.state & States.PSChanged))
        if commandName == 'FileDelete':
            return bool((self.state & States.PSPopulated)) 
        return True

    def start_dialog(self):
        self.result= acm.UX().Dialogs().ShowCustomDialog(self.shell, \
            self.CreateLayout(), self)

    def PopulateADMFields(self):
        admFields = acm.FArray()
        for field in ADMFields:
            self.adm_field.AddItem(field)
        
    def PopulateData(self):
        """populates the default data in GUI fields"""
        self.DefaultData()
        for priceSemantic in acm.FPriceSemantic.Select(''):
            self.price_semantic.AddItem(priceSemantic.Name())
        

    def DefaultData(self):
        """sets default data for fields"""
        self.PopulateADMFields()
        for provider in acm.FEnumeration['enum(PrincipalType)'].Enumerators().Sort():
            if provider in DistributorType:
                self.provider_type.AddItem(provider)

    def GetRowsAttributeValues(self):
        values = dict()
        values['AdmName']      = self.adm_field.GetData()
        values['IdpName']      = self.idp_field.GetData()
        values['Comment']      = self.comments.GetData()
        return values
    
    def GetSemanticAttributeValues(self):
        values = dict()
        values['Name']          = self.price_semantic.GetData()
        values['ProviderType']  = self.provider_type.GetData()
        values['Comment']       = self.semantic_comment.GetData()
        return values

    def GetAllControlsObectFromGUI(self):
        """Get control object from all the GUI fields"""
        self.GetTopLayoutControlsObject()
        self.GetParameterLayoutControlsObject()

    def CreateTopLayout(self):
        """Create top layout"""
        self.TopLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.TopLayoutBuilderObject.BeginVertBox('None')
        self.TopLayoutBuilderObject.BeginVertBox('EtchedIn', '   Semantic Info   ')
        self.TopLayoutBuilderObject.AddSpace(5)
        self.TopLayoutBuilderObject.BeginHorzBox('None')
        self.TopLayoutBuilderObject.AddComboBox('semantic_name', 'Semantic Name', -1, -1, 'Default')
        self.TopLayoutBuilderObject.AddOption('provider_type', '   Provider Type', -1, -1, 'Default')
        self.TopLayoutBuilderObject.EndBox()
        self.TopLayoutBuilderObject.BeginVertBox('None', None)
        self.TopLayoutBuilderObject.AddSpace(2)
        self.TopLayoutBuilderObject.AddInput('semantic_comment', 'Semantic Comment', -1)
        self.TopLayoutBuilderObject.EndBox()
        self.TopLayoutBuilderObject.EndBox()
        self.TopLayoutBuilderObject.AddSpace(5)
        self.TopLayoutBuilderObject.AddList("price_semantic_list", 10, -1, 100, -1)
        self.TopLayoutBuilderObject.EndBox()
    
    def CreateParametersTabLayout(self):
        '''Create parameters tab top layout'''
        self.parametersTabLayoutBuilderObject = acm.FUxLayoutBuilder()
        self.parametersTabLayoutBuilderObject.BeginVertBox('None')
        self.parametersTabLayoutBuilderObject.BeginVertBox('EtchedIn', '   Field Mapping   ')
        self.parametersTabLayoutBuilderObject.AddSpace(5)
        self.parametersTabLayoutBuilderObject.BeginHorzBox('None', '')
        self.parametersTabLayoutBuilderObject.AddComboBox('adm_field', 'ADM Field', -1, -1, 'Default')
        self.parametersTabLayoutBuilderObject.AddInput('idp_field', '   IDP Field', -1)
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.BeginVertBox('None', None)
        self.parametersTabLayoutBuilderObject.AddSpace(2)
        self.parametersTabLayoutBuilderObject.AddInput('comments', 'Field Comment', -1)
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.AddSpace(10)

        self.parametersTabLayoutBuilderObject.EndBox()
        self.parametersTabLayoutBuilderObject.EndBox()

    def GetTopLayoutControlsObject(self):
        self.price_semantic     =       self.TopLayoutObject.GetControl("semantic_name")
        self.semantic_list      =       self.TopLayoutObject.GetControl("price_semantic_list")
        self.provider_type      =       self.TopLayoutObject.GetControl("provider_type")
        self.semantic_comment   =       self.TopLayoutObject.GetControl("semantic_comment")
    
    def GetParameterLayoutControlsObject(self):
        self.adm_field          =       self.parametersTabLayoutObject.GetControl("adm_field")
        self.idp_field          =       self.parametersTabLayoutObject.GetControl("idp_field")
        self.comments           =       self.parametersTabLayoutObject.GetControl("comments")

    def RegisterCallbacksForControls(self):
        """Register callbacks for all the controls of Price defintion"""
        self.RegisterCallbacksForTopLayoutControls()

    def RegisterCallbacksForTopLayoutControls(self):
        """Register callbacks for bottom layout controls"""
        self.price_semantic.AddCallback         ('Changed', OnPriceSemanticSelected, self)
        self.provider_type.AddCallback          ('Changed', OnProviderTypeChanged, self)
        self.semantic_comment.AddCallback       ('Changed', OnSemanticCommentChanged, self)  
        self.semantic_list.AddCallback          ('SelectionChanged', OnSemanticListSelectionChanged, self)
        self.adm_field.AddCallback              ('Changed', OnADMFieldChanged, self)
        self.idp_field.AddCallback              ('Changed', OnIDPFieldChanged, self)
        self.comments.AddCallback               ('Changed', OnMappingCommentChanged, self)
        
    def InitAllcontrolsAndRegisterCallBacks(self):
        """1). Get control object from all the GUI fields\
           2). Register callbacks for each the controls"""
        self.GetAllControlsObectFromGUI()
        self.RegisterCallbacksForControls()

    def CreateLayout(self):
        """Create complete layout of price semantic"""
        self.CreateTopLayout()
        self.CreateParametersTabLayout()

    def InitControls(self):
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)

    def HandleCreate( self, creationContext):
        self.CreateLayout()
        self.InitControls()
        self.TopLayoutObject = creationContext.AddPane(self.TopLayoutBuilderObject, "TOP_PANE")
        self.TopLayoutObject.SetLayout(self.TopLayoutBuilderObject, "TOP_PANE")
        
        parametersTabLayoutContext = creationContext.AddTabControlPane("PARAMETERS_PANE")
        self.parametersTabLayoutObject = parametersTabLayoutContext.AddLayoutPage\
                                               (self.parametersTabLayoutBuilderObject, "Add/Delete/Modify Semantic Mapping")
        self.InitAllcontrolsAndRegisterCallBacks()
        self.PopulateData()
        self.semanticList = SemanticListHandler(self.semantic_list)
        self.semanticList.Initialize()
        
    def DoChangeCreateParameters(self, createParams):
        """Override to be able to modify standard application parameters,
        such as splitters,resizing behaviour etc. This method is called before HandleCreate.
        """
        createParams.UseSplitter(True)
        createParams.LimitMinSize(True)

    def SetState(self, state):
        self.state = self.state | state
        if state == States.PSOpened:
            self.state = state
        elif state == States.PSPopulated:
            self.state = state
        elif state == States.PSSelected:
            self.state = self.state & ~States.PSAdded
            self.state = self.state & ~States.PSChanged
            self.state = self.state & ~States.PSUpdated
            self.state = self.state & ~States.PSMultiSelected
        elif state == States.PSUpdated:
            self.state = self.state & ~States.PSChanged
        elif state == States.PSMultiSelected:
            self.state = self.state & ~States.PSSelected
        elif state == States.PSModified:
            self.state = self.state & ~States.PSAdded
            self.state = self.state & ~States.PSChanged
            self.state = self.state & ~States.PSUpdated
            self.state = self.state & ~States.PSMultiSelected
            self.state = self.state & ~States.PSSelected
            self.state = self.state & ~States.PSOpened
            
    def GetState(self):
        return self.state

    def SetCaption(self, caption = ""):
        """Set the caption for the Price Semantic Dialog"""
        self.SetContentCaption(caption)

    def HasUnsavedChanges(self):
        return bool(self.state & States.PSChanged)

    def HandleApply(self):
        return True
    
    def HandleDestroy(self):
        """closes the dialog"""
        self.binder.RemoveDependent(self)

    def HandleClose(self):
        return True

#*******************************APPLICATION HANDLERS*********************#
def GetApplicationObject():
    """Returns application object"""
    return ApplicationObject

def OpenPriceSemanticApplication(priceSemanticName = ''):
    """Opens Price Link Specification Dialog"""
    try:
        global ApplicationObject
        ApplicationObject = PriceSemanticApplication()
        if priceSemanticName:
            ApplicationObject.SetPriceSemantic(priceSemanticName)
        acm.UX().SessionManager().StartApplication(APPLICATION_NAME, priceSemanticName)
        OpenPriceSemantic(ApplicationObject, priceSemanticName)
    except RuntimeError as extraInfo:
        print(str(extraInfo))
        raise extraInfo
