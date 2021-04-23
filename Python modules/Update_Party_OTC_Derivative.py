"""-----------------------------------------------------------------------------------
MODULE                  :       Update_Party_OTC_Derivative
PURPOSE                 :       Update Party Free5ChoiceList value from an excel file

HISTORY
======================================================================================
Date            change no       Developer            Description
--------------------------------------------------------------------------------------
2021-01-27                      Teboho Lepele        Initial Implementation
"""

import acm
from at_feed_processing import SimpleXLSFeedProcessor
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import FRunScriptGUI

LOGGER = getLogger(__name__)

fileFilter = "XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
outputFile = FRunScriptGUI.OutputFileSelection(FileFilter=fileFilter)


class EditPartyFromXLS(SimpleXLSFeedProcessor):

    def __init__(self, file_path, sheet_index, value):
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=sheet_index, sheet_name=None)
        self.input_errors = False
        self.value = value
        self.failed = []
        self.updated = []
        self.sdsids = []
        self.repeat_ids = []
        self.party = []

    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        self.record = record_data
        self.sdsids.append(self.get_sdsids(self.record))

    def process_ids(self):
        repeat_sdsids = []
        # check if any of the ids appears twice on the file
        for id in self.sdsids:
            count = self.sdsids.count(id)
            if count > 1:
                self.failed.append({'id': id, 'reason': 'duplicate ids on provided file, appears {} times on file'.
                                   format(count)})
                repeat_sdsids.append(id)
        self.sdsids = set(self.sdsids)
    
        # check if multiple duplicates in  front arena use that id
        for id in self.sdsids:
            if self.check_duplicate(id):
                self.repeat_ids.append(str(id))

    def process_party_update(self):
        for id in self.sdsids:
            self.search_value = id
            self.party = self.get_party()
            self.assign_value()

    @staticmethod
    def check_duplicate(id):
        count = 0
        for party in acm.FParty.Select(''):
            if party.AddInfoValue('BarCap_SMS_CP_SDSID') == str(id):
                count += 1
            if count > 1:
                return True
        return False

    def get_sdsids(self, record_data):
        if record_data.get('BarCap_SMS_CP_SDSID'):
            return int(record_data.get('BarCap_SMS_CP_SDSID'))
        elif record_data.get('SDSID'):
            return int(record_data.get('SDSID'))
    
    def get_party(self):
        parties = acm.FParty.Select('')
        parties_update = []
        for party in parties:
            if party.AddInfoValue('BarCap_SMS_CP_SDSID') == str(self.search_value):
                if str(self.search_value) in self.repeat_ids:
                    if party.AddInfoValue('BarCap_SMS_LE_SDSID') != str(self.search_value):
                        continue
                if party.NotTrading():
                    self.failed.append({'id': self.search_value, 'name': party.Name(), 'reason': 'not trading'})
                    continue
                parties_update.append(party)
        if parties_update:
            return parties_update
        else:
            self.failed.append({'id': self.search_value, 'reason': 'SDSID not found'})
            
    def assign_value(self):
        if self.party:
            for party in self.party:
                try:
                    party_clone = party.Clone()
                    party_clone.Free5ChoiceList(self.value)
                    party.Apply(party_clone)
                    party.Commit()
                    self.updated.append({'id': self.search_value, 'name': party.Name()})
                except Exception as e:
                    LOGGER.error('Could not update Party {0}\t{1}'.format(party.Name(), e))

    def display_failed_updates(self):
        LOGGER.info('Failed updates:')
        for result in self.failed:
            if 'SDSID not found' in list(result.values()):
                LOGGER.info('id: {0}, reason: {1}'.format(result.get('id'), result.get('reason')))
            else:
                LOGGER.info('id: {0}, name: {1}, reason: {2}'.format(result.get('id'), result.get('name'),
                                                                     result.get('reason')))
        LOGGER.info('Total failed updated: {}'.format(len(self.failed)))

    def display_successful_updates(self):
        LOGGER.info('Successfully updates')
        for result in self.updated:
            LOGGER.info('id: {0}, name: {1}'.format(result.get('id'), result.get('name')))
        LOGGER.info('Total  updated parties: {}'.format(len(self.updated)))


choice_list = acm.FChoiceList.Select01("list = 'MASTER' and name = 'OTC Derivatives Provider Category'",
                                       "Choice List not found")

ael_variables = AelVariableHandler()

ael_variables.add('input_file',
                  label='File',
                  cls=inputFile,
                  default='Select File Here',
                  mandatory=True,
                  multiple=True,
                  alt='Input file in CSV or XLS format.')

ael_variables.add('sheet_index',
                  label='Input Sheet Index',
                  mandatory=True,
                  default=0)

ael_variables.add('value',
                  label='OTC Derivative Value',
                  mandatory=True,
                  collection=choice_list.Choices(),
                  default=choice_list.Choices()[0])


def ael_main(ael_dict):
    file_name = ael_dict['input_file']
    sheet_index = int(ael_dict['sheet_index'])
    value = ael_dict['value']
    LOGGER.info('Starting update')
    xls_reader = EditPartyFromXLS(str(file_name), sheet_index, value)
    xls_reader.process(False)
    xls_reader.process_ids()
    xls_reader.process_party_update()
    xls_reader.display_failed_updates()
    xls_reader.display_successful_updates()
