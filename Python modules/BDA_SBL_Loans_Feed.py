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

import acm, ael
import FBDPGui
import FRunScriptGUI
import os
import re
import sl_functions

from datetime import datetime
from at_time import to_date, acm_date, to_datetime
from at_ael_variables import AelVariableHandler
from BDA_SBL_Loans_Upload import UploadType
from BDA_SBL_Loans_Upload import BDAUploadFile
from BDA_SBL_Loans_Upload import CollateralType
from BDA_SBL_Loans_Upload import AccountLookup
from BDA_SBL_Loans_Upload import LOGGER

CALENDAR = acm.FCalendar['ZAR Johannesburg']

def FormatInstrumentName(name):
    """ Strip away 'ZAR/' from the instrument name to return the JSE ticker.
    """
    return name[4:]

def SetRecordFields(record, trade):

    instrument = trade.Instrument()
    leg = instrument.Legs().At(0)
    underlying = instrument.Underlying()
    quantity = abs(round(sl_functions.underlying_quantity(trade.Quantity(), instrument)))

    if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
        price = trade.AllInPrice()
    else:
        price = instrument.RefPrice()
    
    value = quantity * price * underlying.Quotation().QuotationFactor()

    borrower = getPartyCode(trade.add_info('SL_G1Counterparty1'), 'Borrower')
    lender = getPartyCode(trade.add_info('SL_G1Counterparty2'), 'Lender')
    
    borrower_account = 0
    lender_account = 0
    
    if AccountLookup.has_key(lender):
        lender_account = AccountLookup[lender][0] 
    else:
        if AccountLookup.has_key(borrower):
            lender_account = AccountLookup[borrower][0] 
            
    if AccountLookup.has_key(borrower):
        borrower_account = AccountLookup[borrower][1] 
    else:
        if AccountLookup.has_key(lender):
            borrower_account = AccountLookup[lender][1] 

    record.CardCode.Value(25)
    record.Brk_Cde.Value(142)
    record.Upl_Typ.Value('N')
    record.Lend_Acc.Value(lender_account)
    record.Del_ID.Value(0) 
    record.Ext_Ref.Value('')
    record.Create_Msg.Value('')
    record.Borr_Msg_Ref.Value('')
    record.Borr_Msg_Sta.Value('')
    record.Coll_Type.Value('')
    record.Ret_Csh.Value(' ')
    record.Borw_Acc.Value(borrower_account)
    record.Borw_Del_ID.Value(0)
    record.Recv_Dte.Value(str(datetime.strftime(to_date(instrument.StartDate()), '%Y%m%d')))
    record.Recv_Sta.Value('')
    record.Retn_Dte.Value('99991231')
    record.Retn_Sta.Value('')
    record.Instr_Typ.Value('E')
    record.Instr_Alpha.Value(FormatInstrumentName(underlying.Name())[:5] if underlying else '')
    record.Instr_Version.Value(getInstr_Version(underlying.Name()) if underlying else 0)
    record.Price.Value(0)
    record.Loan_Qty.Value(quantity)
    record.Loan_Rate.Value(0)
    record.Borw_Rate.Value(0)
    record.Loan_Coll.Value(0)
    record.Borw_Coll.Value(0)
    record.Prov_Bal_Cde.Value('')
    record.Prov_Int_Cde.Value('')
    record.Prov_Trn_Cde.Value('')
    record.Brk_Bal_Cde.Value('')
    record.Brk_Int_Cde.Value('')
    record.Brk_Trn_Cde.Value('')
    record.Trade_Dte.Value(str(datetime.strftime(to_date(trade.TradeTime()[:11]), '%Y%m%d')))
    
def isValidUpload(trade):
    """ Make sure that the trade is meant to be sent to Global One
    """
    # ABITFA-1572 - remove the restriction that forces only two instances
    # of a trade to feed down to global 1.
    # only the check is being removed - the warning will still come through
    # on the user log window.
    #if trade.SLGlobalOneTimeStampCount() >= 2:
    #    return False
    instrument = trade.Instrument()
    if (instrument.add_info('SL_ExternalInternal') == 'Internal' ):
        return False
    elif (not(trade.add_info('SL_G1Counterparty1') and
            trade.add_info('SL_G1Counterparty2'))):
        return False
    else:
        return True

def getPartyCode(party, partyType):
    if partyType == 'Fund':
        parties = acm.FChoiceList.Select("name = 'GlobalOneFunds'")[0]
    elif partyType == 'Borrower':
        parties = acm.FChoiceList.Select("name = 'GlobalOneBorrowers'")[0]
    elif partyType == 'Lender':
        parties = acm.FChoiceList.Select("name = 'GlobalOneLenders'")[0]

    if parties:
        for item in parties.Choices():
            if item.Name() == party:
                return item.Description()

    if partyType != "Fund":
        FAParty = acm.FParty[party]
        if FAParty:
            return FAParty.AdditionalInfo().SL_G1PartyCode()

def getInstr_Version(ins_name):
    alias = acm.FInstrumentAlias.Select('instrument = "%s" and type = "%s"' % (ins_name, "JSE_Instrument_Version"))
    if alias:
        val = re.findall('[0-9]{1,10}_([0-9]{1,3})', alias[0].Alias(), flags=re.S)
        if val:
            return val[0]
    return 0
    
def GenerateReport(trades, filepath, parameters):
    """ Generate a Global One trade report
    """
    report = BDAUploadFile()
    for trade in trades:
        if isValidUpload(trade):
            record = report.CreateRecord(trade)
            SetRecordFields(record, trade)
            
    filename = report.Filename
    fullPath = os.path.join(filepath, filename)

    if report.WriteFile(fullPath, None):
        LOGGER.LOG('Completed successfully.')
    else:
        raise RuntimeError("Errors occurred. Check error file")

outputSelection = FRunScriptGUI.DirectorySelection()
outputSelection.SelectedDirectory('/apps/services/frontnt/Task')

def getAelVariables():
    variables = AelVariableHandler()
    variables.add("trade_key",
            label="Trade Selection",
            cls=acm.FStoredASQLQuery,
            default="BDA_SBL_Loans",
            enabled=True)
    variables.add("folder_key",
            label="Folder",
            default=outputSelection,
            enabled=True)
    variables.extend(FBDPGui.LogVariables())
    return variables
    
ael_variables = getAelVariables()

def ael_main(parameters):
    if parameters["folder_key"]:
        trades = parameters["trade_key"].Query().Select()
        path = parameters["folder_key"]
        GenerateReport(trades, path, parameters)
