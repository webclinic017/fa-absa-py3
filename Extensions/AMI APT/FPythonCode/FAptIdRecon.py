

import os
import re
import csv
import acm
import glob
import cStringIO
import FAptTest
import FAptReportCommon
import FAptReportUtils
import FLogger

logger = FLogger.FLogger.GetLogger('APT')



class FAptIdRecon(object):

    COLUMN_NAMES = ('APT_Compositions_00_AptReconIdType', 'APT_Compositions_19_AptExportType', 'APT_Universe_03_IdType', 'APT_Universe_02_Id', 'APT_Universe_65_ReconIdMessages')
    SHEET_NAME = "APT Id Recon"
    RECON_INS_TYPES = ('Stock', 'Bond', 'EquityIndex', 'Depositary Receipt', 'Convertible', 'Commodity', 'Curr')

    def __init__(self, extensionObject, sheet_type):
        ui_trd_manager = extensionObject
        self.active_wb = extensionObject.ActiveWorkbook()
        self.sheets = self.active_wb.Sheets()
        active_sheet = ui_trd_manager.ActiveSheet()
        self.selection = active_sheet.Selection().SelectedRowObjects()
        self.new_sheet_column_creators = None
        self.column_creators = self._get_column_creators()
        self.sheet_type = sheet_type
        self.apt_id_recon_sheet_index = -1
        self._instruments = []
        self._apt_ids = None
        self.fsize = None
        self.fname = self.get_id_file_name()
        
    def _get_column_creators(self):
        context = acm.GetDefaultContext()
        return acm.GetColumnCreators(self.__class__.COLUMN_NAMES, context)

    def _add_apt_id_recon_sheet_to_active_wb(self, sheet_type):
        new_sheet = self.active_wb.NewSheet(sheet_type, '')
        new_sheet.Name(self.__class__.SHEET_NAME)
        return new_sheet
        
    def _apt_id_recon_sheet_exists(self):
        for sheet in self.sheets:
            self.apt_id_recon_sheet_index += 1
            if sheet.Name() == self.__class__.SHEET_NAME: 
                return 1
        return 0
        
    def _get_existing_apt_id_recon_sheet(self):
        sheet = self.sheets.At(self.apt_id_recon_sheet_index)
        sheet.RemoveAllRows()
        return sheet
        
    def _add_column_creators_to_new_sheet(self, sheet):
        self.new_sheet_column_creators = sheet.ColumnCreators()
        self.new_sheet_column_creators.Clear()
        for i in range(self.column_creators.Size()):
            self.new_sheet_column_creators.Add(self.column_creators.At(i))
        
    def _insert_object_recursive(self, sheet, ins):
        if ins not in self._instruments:
            self._strip_apt_id_file()
            self._perform_id_recon(ins)
        sheet.InsertObject(ins, 0)
        und = ins.Underlying()
        if und: self._insert_object_recursive(sheet, und)
        
    @classmethod
    def get_id_file_name(cls):
        #removing dependency to UserPreferences
        #model_path = cls._get_database_files_path()
        model_path = FAptTest.AptTest._get_apt_models_path()
        model_name = FAptReportUtils.FAptReportParameters().get('DEFAULT_FACTOR_MODEL')
        model_name = re.sub(' ', '', model_name)
        try:
            os.chdir(model_path)
            try:
                fnames = [filename for filename in glob.glob('*.txt') if os.path.splitext(filename)[0][:-8] == model_name]
                if fnames and len(fnames)>1:
                    date = sorted([os.path.splitext(name)[0][-8:] for name in fnames])
                    fname = os.path.join(model_path, '%s%s%s') % (model_name, date[-1], '.txt')
                elif fnames:
                    fname = os.path.join(model_path, fnames[0])
                else:
                    ERROR = 'APT id file %s.txt not found in %s' % (model_name, model_path)
                    logger.error(ERROR)
                    raise TypeError(ERROR)
                return fname
            except IndexError as err:
                logger.error(err)
                raise IndexError(err)
        except WindowsError as err:
            logger.error(err)
            raise WindowsError(err)
            
    def _strip_apt_id_file(self):
        if not self.fsize:
            if self.fname:
                self.fsize = os.path.getsize(self.fname)
                if self.fsize/1000000 > 10:
                    with open(self.fname, 'r') as f:
                        isins = [row.split('\t')[1] for row in f]
                        f.close()
                    with open(self.fname, 'w') as f:
                        f.writelines((''.join((isin, '\n')) for isin in isins))
                        f.close()
            else: 
                ERROR = 'APT id file not found!'
                logger.error(ERROR)
                raise TypeError(EEROR)

            
    def _id_exists_in_apt(self, id):
        if self.fname:
            if not self._apt_ids:
                with open(self.fname) as f:
                    self._apt_ids = set([row for row in f])
            return bool(''.join((id, '\n')) in self._apt_ids)
        return False
    
    def _set_alias(self, ins, alias_type, value):
        alias = acm.FInstrumentAlias.Select01('instrument="%s" and type="%s' % (ins.Name(), alias_type), '')
        if alias:
            alias.Alias(value)
            alias.Commit()
        else:
                
            alias = acm.FInstrumentAlias()
            alias.Instrument(ins)
            alias.Type(alias_type)
            alias.Alias(value)
            alias.Commit()

    
    def _set_addinfo(self, obj, fieldVec, valueVec):
        for i in range(len(fieldVec)):
            field = fieldVec[i]
            value = valueVec[i]
            addSpec = acm.FAdditionalInfoSpec[field]
            a = addSpec.AddInfoContainer(obj)
            if a.Size() > 0:
                a.At(0).FieldValue = str(value)
                a.Commit()    
            elif value:
                ai = acm.FAdditionalInfo()
                ai.AddInf(addSpec)
                ai.FieldValue = str(value)            
                ai.Recaddr = obj.Oid()
                ai.Commit()
                
    def _set_id_type_add_info(self, ins, id_type):
        try:
            self._set_addinfo(ins, ["APT Recon Id Type"], [id_type])
        except Exception as err:
            logger.error("Failed to commit add info for instrument %s. Reason %s", ins.Name(), str(err))
    
    def _get_alias(self, ins, alias_type):
        return ins.Alias(alias_type)
    
    def _get_add_info(self, ins, ai_name):
        ais = acm.FAdditionalInfoSpec[ai_name]
        if ais is None:
            ai = None
        else:
            ai = acm.FAdditionalInfo.Select01('addInf=%d and recaddr=%d'
                                              % (ais.Oid(), ins.Oid()), '')
        return ai, ais
            
    def _delete_alias(self, ins, alias_type):
        alias = self._get_alias(ins.Name(), alias_type)
        if alias:
            logger.info('Removing "%s" on "%s"', alias, ins.Name())
            alias.Delete()
            
    def _delete_add_info(self, ins, ai_name):
        ai, ais = self._get_add_info(ins, ai_name)
        if ai is not None:
            logger.info('Removing "%s" on "%s"', ai_name, ins.Name())
            ai.Delete()
            
    def _get_mapping_table(self):
        mapping_source = FAptReportUtils.FAptReportParameters().get('ID_MAPPING_SOURCE')
        context = acm.GetDefaultContext()
        return context.GetExtension("FStringResource", "FObject", mapping_source).Value()
    
    def _get_ins_object(self, row):
        try:
            return acm.FInstrument[row[1]]
        except IndexError:
            return None
            
    def _set_apt_ids(self, mapping_table):
        logger.info("Performing APT mapping id")
        if mapping_table:
            reader = csv.reader(cStringIO.StringIO(mapping_table), delimiter='\t')
            for row in reader:
                try:
                    ins = self._get_ins_object(row)
                    if ins and not self._get_alias(ins, 'DATASTREAM'): 
                        self._set_alias(ins, "DATASTREAM", row[2])
                        logger.info('Setting DATASTREAM on instrument "%s" to "%s"', ins.Name(), row[2])
                except IndexError:
                    continue
                except RuntimeError as err:
                    logger.debug('Cannot set DATASTREAM on instrument "%s" to "%s". Reason "%s"', ins.Name(), row[2], err)
                    continue
            
    def _remove_apt_ids(self, mapping_table):
        logger.info("Removing APT mapping id")
        if mapping_table:
            reader = csv.reader(cStringIO.StringIO(mapping_table), delimiter='\t')
            for row in reader:
                try:
                    ins = self._get_ins_object(row)
                    if ins and self._get_alias(ins, 'DATASTREAM'): 
                        self._delete_alias(ins, "DATASTREAM")
                except IndexError:
                    continue
        
    def _perform_id_mapping(self):
        mapping_table = self._get_mapping_table()
        use_id_mapping = FAptReportUtils.FAptReportParameters().get('USE_ID_MAPPING')
        if use_id_mapping in ('YES'):
            self._set_apt_ids(mapping_table)
        else: self._remove_apt_ids(mapping_table)

    def _perform_id_recon(self, ins):
        ins_type = ins.InsType()
        if ins_type in self.RECON_INS_TYPES:
            datastream = self._get_alias(ins, 'DATASTREAM')
            id = ins.Isin() if ins_type not in ('Curr') else ins.Name()
            if datastream:
                self._set_id_type_add_info(ins, "DATASTREAM")
            elif id:
                id_in_apt = self._id_exists_in_apt(id)
                if not id_in_apt:
                    self._set_id_type_add_info(ins, "OTC")
                else:
                    self._set_id_type_add_info(ins, "ISIN")
            else:
                self._set_id_type_add_info(ins, "OTC")

    def start(self):
        self._perform_id_mapping()
        if self._apt_id_recon_sheet_exists():
            sheet = self._get_existing_apt_id_recon_sheet()
        else: 
            sheet = self._add_apt_id_recon_sheet_to_active_wb(self.sheet_type)
            self._add_column_creators_to_new_sheet(sheet)
        for i in self.selection:
            if i.IsKindOf('FMultiInstrumentAndTrades'):
                instruments = i.LiveInstruments()
                for ins in instruments:
                    self._insert_object_recursive(sheet, ins)
            else:
                ins = i.Instrument()
                self._insert_object_recursive(sheet, ins)


def aptIdRecon(eii):
    extensionObject = eii.ExtensionObject()
    sheet_type = "DealSheet"
    aptIdRecon = FAptIdRecon(extensionObject, sheet_type)
    aptIdRecon.start()

