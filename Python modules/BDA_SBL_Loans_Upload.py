"""----------------------------------------------------------------------------
PROJECT                 :   SBL ACS Migration
PURPOSE                 :   Generate security loan trade messages to be sent
                            to Global One
DEPATMENT AND DESK      :   Prime Services, Securities Lending
HISTORY
===============================================================================
Date          Change no    Developer              Description
-------------------------------------------------------------------------------
2020-01-01                 Jaysen Naicker         Initial development
----------------------------------------------------------------------------"""

import acm
import FLogger
import time
from at_time import to_date, acm_date, to_datetime
from datetime import datetime

from gen_fixed_length_record import DatetimeField
from gen_fixed_length_record import ImpliedDecimalField
from gen_fixed_length_record import IntField
from gen_fixed_length_record import IntRangeField
from gen_fixed_length_record import ListField
from gen_fixed_length_record import Record
from gen_fixed_length_record import StringField
from gen_fixed_length_record import YesNoField

LOGGER = FLogger.FLogger('BDA_SBL_Loans')
NEWLINE = '\n'
CURRENT_SCRIPT = acm.FAel["BDA_SBL_Loans_Upload"]


class UploadType:
    New = 'N'
    Update = 'U'
    Reverse = 'R'
    
class CreateMsg:
    No_Message  = 'N'
    Immediate  = 'Y'
    Later = 'L'

class CollateralType:
    Default  = 'S'
    Cash  = ''

class ReturnCash:
    None_  = ''
    Positive  = 'N'
    Negative  = 'Y'

AccountLookup = {
            'ACS123': [100081, 100990], 
            'ACS200': [100065, 100990],
            'ACS333': [100008, 100990],
            'ACS999': [100990, 100032],
            'ACSBR1': [100073, 100990],
            }


def GetSequenceNumber():
    try:
        sequence_number = CURRENT_SCRIPT.add_info("BDA_Sequence_Number")
        return int(sequence_number)
    except:
        return 0


def IncrementSequenceNumber(current):
    try:
        sequence_number = (current + 1)
        ai = CURRENT_SCRIPT.AddInfos()[0]
        ai.FieldValue(sequence_number)
        ai.Commit()
    except Exception as e:
        LOGGER.LOG('Failed with exception %s.', str(e))


def GetNextSequenceNumber():
    try:
        if CURRENT_SCRIPT:

            if CURRENT_SCRIPT.AddInfos():

                currentNumber = GetSequenceNumber()
                IncrementSequenceNumber(currentNumber)
                nextNumber = GetSequenceNumber()
                CURRENT_SCRIPT.Commit()

                if nextNumber > currentNumber:
                    return nextNumber
        else:
            LOGGER.WLOG("Missing AdditionalInfo BDA_Sequence_Number")
    except:
        return 0
    return 0

class BDAUploadHeaderRecord(Record):
    def __init__(self):
        Record.__init__(self, 'Header Record', [
            IntField('CardCode', False, 3, 0),
            IntField('Brk_Cde', False, 3, 142),
            StringField('Date', 8, str(datetime.strftime(to_datetime(datetime.today()), '%Y%m%d'))),
            StringField('Time', 6, str(datetime.strftime(to_datetime(datetime.today()), '%H%M%S'))),
            StringField('Prefix', 1),
            IntField('Seq_No', False, 7),
            StringField('Filler', 2, ' ')])

class BDAUploadTrailerRecord(Record):
    def __init__(self):
        Record.__init__(self, 'Trailer Record', [
            IntField('CardCode', False, 3, 999),
            IntField('Brk_Cde', False, 3, 142),
            StringField('Date', 8, str(datetime.strftime(to_datetime(datetime.today()), '%Y%m%d'))),
            StringField('Time', 6, str(datetime.strftime(to_datetime(datetime.today()), '%H%M%S'))),
            IntField('Total_Records', False, 9),
            IntField('Records_Processed', False, 9, 0),
            IntField('Records_Rejected', False, 9, 0),
            StringField('Filler', 3, ' ')])

class BDAUploadLoanRecord(Record):
    def __init__(self):
        Record.__init__(self, 'Global One Loan Detail', [
            IntField('CardCode', False, 3),
            IntField('Brk_Cde', False, 3),
            ListField('Upl_Typ', 1, ['N', 'U', 'R']),
            IntField('Lend_Acc', False, 7),
            IntField('Del_ID', False, 7),
            StringField('Ext_Ref', 11),
            ListField('Create_Msg', 1, ['N', 'Y', 'L']),
            StringField('Borr_Msg_Ref', 16),
            StringField('Borr_Msg_Sta', 9),
            ListField('Coll_Type', 1, ['S', '']),
            ListField('Ret_Csh', 1, [' ', 'Y', 'N']),
            IntField('Borw_Acc', False, 7),
            IntField('Borw_Del_ID', False, 7),
            StringField('Recv_Dte', 8),
            ListField('Recv_Sta', 1, ['']),
            StringField('Retn_Dte', 8),
            ListField('Retn_Sta', 1, ['']),
            ListField('Instr_Typ', 1, ['E']),
            StringField('Instr_Alpha', 6),
            IntField('Instr_Version', False, 3),
            IntField('Price', False, 7),
            IntField('Loan_Qty', False, 11),
            IntField('Loan_Rate', False, 5),
            IntField('Borw_Rate', False, 5),
            IntField('Loan_Coll', False, 15),
            IntField('Borw_Coll', False, 15),
            StringField('Prov_Bal_Cde', 2),
            StringField('Prov_Int_Cde', 2),
            StringField('Prov_Trn_Cde', 2),
            StringField('Brk_Bal_Cde', 2),
            StringField('Brk_Int_Cde', 2),
            StringField('Brk_Trn_Cde', 2),
            StringField('Trade_Dte', 8),
            StringField('Filler', 219, '')])

class BDAUploadFile():
    def __init__(self):
        self._header = BDAUploadHeaderRecord()
        self._footer = BDAUploadTrailerRecord()
        self._records = {}

    @property
    def Header(self):
        return self._header

    @property
    def Footer(self):
        return self._footer

    @property
    def Filename(self):
        return 'BBAP.SPRD.UPLOAD.142.LOANS' + '.txt'

    def CreateRecord(self, trade):
        _record = BDAUploadLoanRecord()
        if trade in self._records:
            self._records[trade].append(_record)
        else:
            self._records[trade] = [_record]
        return _record

    def WriteFile(self, filepath, backupPath = None, stampTrade = True):
        success = True

        if not self._records:
            if str(acm.Class()) == "FTmServer":
                func = acm.GetFunction('msgBox', 3)
                func('Warning', 'There are no records to write to the '
                    'BDA Upload File.\nNo file will be written.', 0)
            else:
                LOGGER.LOG('There are no records to write to the BDA Upload File.\nNo file will be written.')
            return success

        if backupPath:
            backup = True
        else:
            backup = False
            backupPath = filepath
        
        seqNumber = GetNextSequenceNumber()
        if not seqNumber:
            LOGGER.LOG('Could not generate sequence number.')
            return False
        self._header.Prefix.Value('S')
        self._header.Seq_No.Value(seqNumber)
        now = time.time()

        try:
            with open(backupPath, 'w') as reportFile:
                reportFile.write(str(self._header))
                counter = 0
                formatting = ''
                for trade in self._records:
                    try:
                        for _record in self._records[trade]:
                            recordStr = str(_record)
                            reportFile.write(NEWLINE + recordStr)
                            counter += 1
                    except Exception, ex:
                        line = "{0}Trade {1}: {2}".format(formatting, trade.Oid(), str(ex))
                        LOGGER.LOG(line)
                        formatting = NEWLINE
                        success = False
                self._footer.Time.Value(str(datetime.strftime(to_datetime(datetime.today()), '%H%M%S')))
                self._footer.Total_Records.Value(counter)
                reportFile.write(NEWLINE + str(self._footer))
        except Exception, ex:
            success = False
            raise ex
        LOGGER.LOG('Wrote secondary output file to: %s' % backupPath)
        return success

