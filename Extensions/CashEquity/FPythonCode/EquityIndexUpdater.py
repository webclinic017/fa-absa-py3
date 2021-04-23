
"""-----------------------------------------------------------------------------
Date:                   2014-08-11
Purpose:                ABITFA-2610
                        A spreadsheet / scripting tool that enables 
                        mass updating of all equity indices.
                        Equity index can be exported to and read from a csv file.
Department and Desk:    Cash Equities
Requestor:              Irfaan Karim
Developer:              Ondrej Bahounek
CR Number:              2173016
-----------------------------------------------------------------------------"""

import acm
import FUxCore
import csv
import re
import FLogger


logger = FLogger.FLogger()
CAPTION_EI = "EQUITY INDEX"
CAPTION_FACTOR = "INDEX FACTOR"
CAPTION_INSTR = "INSTRUMENT"
CAPTION_WEIGHT = "WEIGHT"

"""
UPGRADE 2016.5 (H)
"""
TODAY = acm.Time().DateNow()


def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    customDlg = EI_CustomDialog()
    builder = customDlg.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, customDlg )

   
class EI_CustomDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.m_eqindexObj = None
        self.m_fuxDlg = 0
        self.m_list = 0
        
        self.m_btnLoadEI = 0
        self.m_btnSelectEI = 0
        self.m_btnFromFile = 0
        self.m_btnExport = 0
        self.m_btnUpdateIns = 0
        self.m_btnAddIns = 0
        self.m_btnDeleteIns = 0
        self.m_btnSave = 0
        self.m_btnClose = 0
        self.m_btnLoadUndIns = 0
        
        self.m_inptIndex = 0
        self.m_inptFactor = 0
        self.m_inptInstr = 0
        self.m_inptWeight = 0
        
    def HandleApply( self ):
        return 1
    
    def SetEquityIndex(self, eqIndexObj):
        self.ClearData()
        self.m_eqindexObj = eqIndexObj
        self.PopulateData()
        
    def SetEquityIndexFromName(self, indexname):
        eq_index = EquityIndex.get_equity_index_from_db(indexname)
        if eq_index:
            self.SetEquityIndex(eq_index)
        
    def CheckAndSetFactorFull(self):
        """ Check if factor is correctly set and valid number and save it. """
        factor = toFloat(self.m_inptFactor.GetData().strip())
        msg = ""
        if not factor:
            msg = "Wrong factor format: a positive number expected."
        elif factor <= 0:
            msg = "Factor must be a positive number."
        if msg:
            self.ShowInformation(msg)
            return None
        self.m_eqindexObj.factor = factor
        return factor
    
    def CheckAndSetFactor(self):
        """ Check if factor is a valid number and save it. 
        Warn only if it is not a positive number.
        """
        if not self.m_eqindexObj:
            return None
        
        factor = toFloat(self.m_inptFactor.GetData().strip())
        if not factor:
            return None
        if factor <= 0:
            self.ShowInformation("Factor must be a positive number.")
            return None
        self.m_eqindexObj.factor = factor
        return factor
        
    def PopulateData(self):
        """ Fill form with data from the current equity index object. """
        if not self.m_eqindexObj:
            return
        
        self.m_inptIndex.SetData(self.m_eqindexObj.name)
        self.m_inptFactor.SetData(self.m_eqindexObj.factor)
        self.m_inptInstr.SetData('')
        self.m_inptWeight.SetData('')
        
        self.m_list.RemoveAllItems()
        rootItem = self.m_list.GetRootItem()
        for i, ins in enumerate(sorted(self.m_eqindexObj.get_all_instruments())):
            child = rootItem.AddChild()
            child.Label(i+1)
            child.Label(ins.name, 1)
            child.Label(ins.weight, 2)
            child.SetData(ins)
        
        self.m_list.AdjustColumnWidthToFitItems(0)
        self.m_list.AdjustColumnWidthToFitItems(1)
        
        self.m_btnExport.Enabled(True)
        self.m_btnAddIns.Enabled(True)
        self.m_btnLoadUndIns.Enabled(True)
        self.m_btnSave.Enabled(True)
    
    def SetDefaults(self):
        """ Set default values to all controls. """
        self.m_inptIndex.SetData('')
        self.m_inptFactor.SetData('')
        self.m_inptInstr.SetData('')
        self.m_inptWeight.SetData('')
        
        self.m_list.RemoveAllItems()
        
        self.m_btnDeleteIns.Enabled(False)
        self.m_btnUpdateIns.Enabled(False)
        self.m_btnExport.Enabled(False)
        self.m_btnAddIns.Enabled(False)
        self.m_btnLoadUndIns.Enabled(False)
        self.m_btnSave.Enabled(False)
        
    def ClearData(self):
        """ Clear whole form from all values. """
        self.SetDefaults()
        self.m_eqindexObj = None
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Equity Index Updater')
        
        self.m_list = layout.GetControl("instruments")
        
        self.m_btnLoadEI = layout.GetControl("btn_load_index")
        self.m_btnSelectEI = layout.GetControl("btn_select_index")
        self.m_btnFromFile = layout.GetControl("btn_fromfile")
        self.m_btnUpdateIns = layout.GetControl("btn_update_ins")
        self.m_btnAddIns = layout.GetControl("btn_add_ins")
        self.m_btnDeleteIns = layout.GetControl("btn_del_ins")
        self.m_btnExport = layout.GetControl("btn_export")
        self.m_btnSave = layout.GetControl("btn_save")
        self.m_btnClose = layout.GetControl("btn_close")
        self.m_btnLoadUndIns = layout.GetControl("btn_load_instr")
        
        self.m_btnDeleteIns.Enabled(False)
        self.m_btnUpdateIns.Enabled(False)
        self.m_btnExport.Enabled(False)
        self.m_btnAddIns.Enabled(False)
        self.m_btnLoadUndIns.Enabled(False)
        self.m_btnSave.Enabled(False)
        
        self.m_inptIndex = layout.GetControl("input_index_name")
        self.m_inptFactor = layout.GetControl("input_index_factor")
        self.m_inptInstr = layout.GetControl("input_instr")
        self.m_inptWeight = layout.GetControl("input_weight")
        
        self.m_list.ShowGridLines()
        self.m_list.ShowColumnHeaders()
        self.m_list.AddColumn('#', -1, "Line Number")
        self.m_list.AddColumn('Name', -1, "Name of the instrument")
        self.m_list.AddColumn('Weight', -1, "Weight of the instrument")
        
        self.m_list.AdjustColumnWidthToFitItems(0)
        self.m_list.AdjustColumnWidthToFitItems(1)
        
        self.m_list.AddCallback("SelectionChanged", self.OnListSelectionChanged, None)
        
        self.m_inptFactor.AddCallback("Changing", self.OnFactorInputChanging, None)
        
        self.m_btnLoadEI.AddCallback("Activate", self.OnLoadEIButtonPressed, None)
        self.m_btnSelectEI.AddCallback("Activate", self.OnSelectEIButtonPressed, None)
        self.m_btnExport.AddCallback("Activate", self.OnExportButtonPressed, None)
        self.m_btnUpdateIns.AddCallback("Activate", self.OnUpdateInsButtonPressed, None)
        self.m_btnAddIns.AddCallback("Activate", self.OnAddInsButtonPressed, None)
        self.m_btnDeleteIns.AddCallback("Activate", self.OnDeleteInsButtonPressed, None)
        self.m_btnSave.AddCallback("Activate", self.OnSaveButtonPressed, None)
        self.m_btnClose.AddCallback("Activate", self.OnCloseButtonPressed, None)
        self.m_btnFromFile.AddCallback("Activate", self.OnLoadFromFileButtonPressed, None)
        self.m_btnLoadUndIns.AddCallback("Activate",
                                         self.OnLoadUnderlyingInsButtonPressed, None)
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.    AddInput('input_index_name', 'Eq Index Name')
        b.    AddButton('btn_load_index', 'Load')
        b.    AddButton('btn_select_index', '...', False, True)
        b.    AddButton('btn_fromfile', 'From File...')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddInput('input_index_factor', 'Factor', 20, 20)
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Instruments')
        b.    AddList('instruments', 15, -1, 100, -1)
        b.    BeginHorzBox('None')
        b.      AddInput('input_instr', 'Instrument', 60)
        b.      AddButton('btn_load_instr', '...', False, True)
        b.    EndBox()
        b.    AddInput('input_weight', 'Weight', 20, 20)
        b.    AddSpace(10)
        b.    BeginHorzBox('None')
        b.      AddButton('btn_update_ins', 'Update')
        b.      AddSpace(10)
        b.      AddButton('btn_add_ins', 'Add')
        b.      AddSpace(10)
        b.      AddButton('btn_del_ins', 'Delete')
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddButton('btn_export', 'Export...', 5, 5)
        b.    AddFill()
        b.    AddButton('btn_save', 'Save')
        b.    AddButton('btn_close', 'Close')
        b.  EndBox()
        b.EndBox()
        return b

    def OnFactorInputChanging(self, cd, data):
        """ Factor input field changed.
        
        If valid factor number is set in the textfield,
        it will be saved in the index object.
        """
        self.CheckAndSetFactor()
    
    
    def OnListSelectionChanged(self, cd, data):
        item = self.m_list.GetSelectedItem()
        if not item:
            self.m_inptInstr.SetData('')
            self.m_inptWeight.SetData('')
            self.m_btnDeleteIns.Enabled(False)
            self.m_btnUpdateIns.Enabled(False)
            return
            
        instrument = item.GetData() 
        self.m_inptInstr.SetData(instrument.name)
        self.m_inptWeight.SetData(instrument.weight)
        self.m_btnDeleteIns.Enabled(True)
        self.m_btnUpdateIns.Enabled(True)
    
    
    def OnLoadEIButtonPressed(self, cd, data):
        """ Load equity index set in input field. """
        inputEqName = self.m_inptIndex.GetData().strip()
        self.SetEquityIndexFromName(inputEqName)
        self.m_inptIndex.SetData(inputEqName)
    
    
    def OnSelectEIButtonPressed(self, cd, data):
        """ Display dialog for selection of equity index from DB. """
        index = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Equity Index',
                                                'Equity Index',
                                                acm.FEquityIndex.Select(''),
                                                None)
        if index:
            self.SetEquityIndexFromName(index.Name())
        
        
    def OnLoadFromFileButtonPressed(self, cd, data):
        """ Load equity index from file. """
        selection = acm.FFileSelection()
        selection.PickDirectory(False)
        selection.FileFilter('CSV Files (*.csv)|*.csv|All Files (*.*)|*.*|')
        selection.PickExistingFile(True)
        if acm.UX().Dialogs().BrowseForFile(self.m_fuxDlg.Shell(), selection):
            outfilepath = selection.SelectedFile().Text()
            eqindex = EquityIndex.get_equity_index_from_file(outfilepath)
            if not eqindex:
                self.ShowInformation("Index could not be loaded from file.")
                return
            self.SetEquityIndex(eqindex)
            print 'Equity index {0} was successfully read from file {1}' \
                    .format(eqindex.name, outfilepath)
    
    
    def OnLoadUnderlyingInsButtonPressed(self, cd, data):
        """ Display dialog for selection of an underlying instrument from DB. """
        instrument = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                     'Select Underlying Instrument',
                                                     'Stock',
                                                     acm.FStock.Select(''),
                                                     None)
        if not instrument:
            return
        self.m_list.RemoveAllSelectedItems(False)
        self.m_inptInstr.SetData(instrument.Name())
        self.m_inptWeight.SetData('')
    
    
    def OnExportButtonPressed(self, cd, data):
        """ Export equity index into a file. """
        factor = self.CheckAndSetFactorFull()
        if not factor:
            return
        
        selection = acm.FFileSelection()
        selection.SelectedDirectory = 'c:\\'
        selection.PickExistingFile(False)
        selection.FileFilter('CSV Files (*.csv)|*.csv|All Files (*.*)|*.*|')
        if acm.UX().Dialogs().BrowseForFile(self.m_fuxDlg.Shell(), selection):
            outfilepath = selection.SelectedFile()
            self.m_eqindexObj.export_to_csv(outfilepath.AsString())
            print "Successfully exported to {0}" .format(outfilepath) 
    
        
    def OnUpdateInsButtonPressed(self, cd, data):
        """ Update weight of existing underlying instrument. """
        ins_selected = self.m_list.GetSelectedItem().GetData()
        ins_name = self.m_inptInstr.GetData().strip()
        
        if not ins_name:
            msg = "Instrument name not set correctly."
            self.ShowInformation(msg)
            return    
    
        ins_new = acm.FInstrument[ins_name]
        ins_weight = toFloat(self.m_inptWeight.GetData().strip())
        msg = ""
        if not ins_new:
            msg = "Instrument '{0}' not found.".format(ins_name)
        elif ins_selected.name != ins_new.Name():
            msg = "Instruments' names do not match."
        elif not ins_weight:
            msg = "Wrong weight format: a positive number expected."
        elif ins_weight <= 0:
            msg = "Instrument weight must be a positive number."
        if msg:
            self.ShowInformation(msg)
            return
        ins_selected.weight = ins_weight
        self.SetDefaults()
        self.PopulateData()
        print "Instrument ({0}: {1}) successfully updated." \
                .format(ins_name, ins_weight)
    
        
    def OnAddInsButtonPressed(self, cd, data):
        """ Insert new underlying instrument into the equity index. """
        ins_name = self.m_inptInstr.GetData().strip()
        if not ins_name:
            msg = "Instrument name not set correctly."
            self.ShowInformation(msg)
            return
        
        ins_new = acm.FInstrument[ins_name]
        ins_weight = toFloat(self.m_inptWeight.GetData().strip())
        msg = ""
        if not ins_new:
            msg = "Instrument '{0}' not found.".format(ins_name)
        elif not ins_weight:
            msg = "Wrong weight format: a positive number expected."
        elif ins_weight <= 0:
            msg = "Instrument weight must be a positive number."
        if msg:
            self.ShowInformation(msg)
            return
        
        existing_instrument = self.m_eqindexObj.get_instrument(ins_name)
        if existing_instrument != None:
            msg = "Could not insert instrument {0}: already present in equity index." \
                        .format(ins_name)
            self.ShowInformation(msg)
            return
        
        self.m_eqindexObj.add_instrument(ins_name, ins_weight)
        self.PopulateData()
        print "Instrument ({0}: {1}) successfully added.".format(ins_name, ins_weight)
    
    
    def OnDeleteInsButtonPressed(self, cd, data):
        """ Delete instrument from index object and remove it from the list. """
        item = self.m_list.GetSelectedItem()
        instr = item.GetData()
        result = acm.UX().Dialogs().MessageBoxYesNo(self.m_fuxDlg.Shell(),
                                    'Question',
                                    'Are you sure you want to remove Instrument {0}?' \
                                        .format(instr.name))
        if result != 'Button1':
            return
        
        self.m_eqindexObj.remove_instrument(instr.name)
        self.SetDefaults()
        self.PopulateData()
        print 'Instrument ({0}: {1}) deleted.'.format(instr.name, instr.weight)
    
    
    def OnSaveButtonPressed(self, cd, data):
        """ Save current equity index object into DB. """
        if not self.m_eqindexObj:
            self.ShowInformation("No equity index loaded")
            return
        
        factor = self.CheckAndSetFactorFull()
        if not factor:
            return
        
        logger.LOG('Saving equity index {0}...' .format(self.m_eqindexObj.name))
        self.m_eqindexObj.save_equity_index()
        logger.LOG('Equity Index was successfully saved.')
    
    
    def OnCloseButtonPressed(self, cd, data):
        """ Close main dialog. """
        self.m_fuxDlg.CloseDialogOK()
    
    
    def ShowInformation(self, msg):
        """ Show message in information dialog. """
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), msg)


class Instrument:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __lt__(self, other):
        return self.name < other.name


class EquityIndex:
    def __init__(self, name, factor):
        self.name = name
        self.factor = factor
        self.instruments = {}
    
    def add_instrument(self, name, weight):
        """ Add instrument_name, instrument_weight into equity index. """
        ins = self.instruments.get(name) 
        if ins:
            ins.name = name
            ins.weight = weight
            return ins
        self.instruments[name] = Instrument(name, weight)
        return self.instruments[name]
    
    def get_instrument(self, name):
        return self.instruments.get(name)
    
    def remove_instrument(self, name):
        ins = self.get_instrument(name)
        if ins:
            return self.instruments.pop(name)

    def get_all_instruments(self):
        return self.instruments.values()

    @staticmethod
    def get_equity_index_from_db(indexname):
        try:
            if not indexname:
                return None
            ins = acm.FInstrument[indexname]
            comb = acm.FCombination[ins.Oid()]
            eqindex = EquityIndex(ins.Name(), ins.Factor())
            for instr in comb.Instruments():
                """
                UPGRADE 2016.5 (H)
                
                Old code:
                eqindex.add_instrument(instr.Instrument().Name(), comb.FindInstrumentWeight(instr))
                
                Note: FindInstrumentWeight() takes 2 arguments instead of 1 now. Using today's date as the Valuation Date.
                """
                eqindex.add_instrument(instr.Instrument().Name(), comb.FindInstrumentWeight(instr, TODAY))
                
            return eqindex
        except:
            return None

    @staticmethod
    def get_equity_index_from_file(filename):
        try:
            with open(filename, "r") as csvfile:
                reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
                read_instruments = False
                eq_index = None
                for key, val in reader:
                    key = key.replace('"', '').replace("'", '').strip()
                    val = val.replace('"', '').replace("'", '').replace(',', '').strip()
                    if read_instruments:
                        instr = acm.FInstrument[key]
                        if not instr:
                            raise Exception("Incorrect Instrument name: {0}".format(key))
                        eq_index.add_instrument(key, float(val))
                        continue
                    if key.upper() == CAPTION_EI:
                        eq_in = acm.FEquityIndex[val]
                        if not eq_in:
                            raise Exception("Incorrect Index name: {0}".format(val))
                        name = val
                    elif key.upper() == CAPTION_FACTOR:
                        factor = float(val)
                    elif key.upper() == CAPTION_INSTR:
                        read_instruments = True
                        eq_index = EquityIndex(name, factor)
        except Exception as err:
            print "ERROR: Problems while reading input file: {0}".format(str(err))
            return None
        return eq_index


    @staticmethod            
    def get_3sets_of_instruments(eqindex1, eqindex2):
        """ Get 3 sets of instruments from 2 equity indices:
        same_instruments, only_in_eq1_instruments, only_in_eq2_instruments
        """
        same_instruments = []
        only_in_eqindex1 = []
        only_in_eqindex2 = []

        for ins in eqindex1.get_all_instruments():
            if eqindex2.get_instrument(ins.name):
                same_instruments.append(ins)
            else:
                only_in_eqindex1.append(ins)
        
        for ins in eqindex2.get_all_instruments():
            if not eqindex1.get_instrument(ins.name):
                only_in_eqindex2.append(ins)
        
        return (same_instruments, only_in_eqindex1, only_in_eqindex2)

    
    def save_equity_index(self):
        """ Save current equity index into DB. """
        eq_index_old = EquityIndex.get_equity_index_from_db(self.name)
        (to_update, to_add, to_del) = EquityIndex.get_3sets_of_instruments(self, eq_index_old)
        
        instr = acm.FInstrument[self.name]
        comb = acm.FCombination[instr.Oid()]
        
        print "*" * 80
        print "Updating Equity Index '{0}'".format(self.name)
        
        try:
            comb.Factor(self.factor)
            for ins in to_update:
                insobj = acm.FInstrument[ins.name]
                
                """
                UPGRADE 2016.5 (H)
                Old code:
                comb.SetInstrumentWeight(insobj, ins.weight)
                """
                comb.SetInstrumentWeight(insobj, ins.weight, TODAY)
                
            for ins in to_add:
                insobj = acm.FInstrument[ins.name]
                comb.AddInstrument(insobj, ins.weight)
            for ins in to_del:
                insobj = acm.FInstrument[ins.name]
                comb.Remove(insobj)
            comb.Commit()
        except Exception as err:
            print "ERROR: {0}".format(str(err))
            print "Index was not updated." 
            return
        
        print 'Following changes were made to underlying instruments:'
        print "\n"
        print "Updated:" + ",".join([i.name for i in to_update])
        print "Added:" + ",".join([i.name for i in to_add])
        print "Deleted:" + ",".join([i.name for i in to_del])
        print "*" * 80


    def export_to_csv(self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([CAPTION_EI, self.name])
            writer.writerow([CAPTION_FACTOR, self.factor])
            writer.writerow([CAPTION_INSTR, CAPTION_WEIGHT])
            for instr in sorted(self.get_all_instruments()):
                writer.writerow([instr.name, instr.weight])


def toFloat(number):
    """ Convert number to a float. """
    try:
        if type(number) == str and re.match("^\d+(?:\.\d+)?$", number) is None:
                return None
        return float(number)
    except:
        return None

