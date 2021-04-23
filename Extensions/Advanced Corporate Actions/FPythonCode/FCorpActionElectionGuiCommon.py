""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionElectionGuiCommon.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionElectionGuiCommon 

DESCRIPTION
----------------------------------------------------------------------------"""

tt_Name = 'The name of the election.'
tt_Portfolio = 'The portfolio of the position.'
tt_Party = 'The party making the election.'
tt_Instrument = 'The instrument of the position.'
tt_Position = 'The position instance.'
tt_Price = 'The price submitted for tender offers or buybacks.'
tt_Quantity = 'The number of shares to elect this option.'
tt_StockEntitlement = 'The number of shares this position is entitled to.'
tt_CashEntitlement = 'The amount of cash this position is entitled to.'
tt_EligiblePosition = 'The quantity of shares eligible for this corporate action.'
tt_CaChoice = 'The corporate action option of the election.'
tt_ReplyDate = 'The reply date.'
tt_Deadline = 'The deadline for making an election.'
tt_text = 'Further text can be entered here.'
tt_Status = 'The state of processing this position.'
tt_Elected = 'Indicates if the corporate action option has been elected'
tt_Oid = 'The oid of the election'

import locale
import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActionElection
import FBDPCommon
import FCAElectionColumns
import FCorpActionElectionStatesSetup

ael_variables = None
ADDITIONALINFO_RECORDTYPE = "CorpActionElection"
addInfoNames = FBDPCommon.getAdditionalInfoNames(ADDITIONALINFO_RECORDTYPE)


def _formatNumber(val):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format("%.*f", (2, val), grouping=True)


def populateGuiFromElection(election, fieldValues):    
    for var in ael_variables:
        if var.varName == 'CaChoice':
            fieldValues[var.sequenceNumber] = election.CaChoice().Oid()
        elif var.varName == 'CashEntitlement':
            fieldValues[var.sequenceNumber] = FCAElectionColumns.caCashEntitlement(election, election.CaChoice().CaPayouts())
        elif var.varName == 'StockEntitlement':
            fieldValues[var.sequenceNumber] = FCAElectionColumns.caStockEntitlement(election, election.CaChoice().CaPayouts())
        elif var.varName == 'EligiblePosition':
            fieldValues[var.sequenceNumber] = _formatNumber(FCAElectionColumns.caEligiblePosition(election, None))
        elif var.varName == 'Instrument':
            fieldValues[var.sequenceNumber] = FCAElectionColumns.caElectionInstrument(election)
        elif var[0] in addInfoNames:
            addinfo = election.AddInfos()
            for i in addinfo:
                spec = i.AddInf()
                name = spec.FieldName()
                if name == var[0]:
                    fieldValues[var.sequenceNumber] = i.FieldValue()
        elif var.varName == 'Elected':
            percentage = election.GetProperty('Percentage')
            if percentage != 0.0:
               fieldValues[var.sequenceNumber] = 1
        elif var.varName == 'Status':
            bp = FBDPCommon.GetBusinessProcess(election.Oid(), 'CorpActionElection')
            if bp:
                fieldValues[var.sequenceNumber] = bp.CurrentStep().State().Name()
            else:
                fieldValues[var.sequenceNumber] = ''
        else:
            val = election.GetProperty(var.varName)
            if var.varName in ['ReplyDate', 'Deadline']:
                val = acm.Time().LocalToUtc(val) 
                if val == '1970-01-01 00:00:00':
                    val = ''
            elif var.varName == 'TextInfo' and val:
                val = val.Text()
            elif var.varName == 'Quantity' and val:
                val = _formatNumber(val)
            fieldValues[var.sequenceNumber] = val
        
    return fieldValues


def oid_cb(index, fieldValues):
    if isinstance(fieldValues[index], (int, long)):
        election = acm.FCorporateActionElection[fieldValues[index]]
        if election:
            fieldValues = populateGuiFromElection(election, fieldValues)
    return fieldValues

def _createCorpActionPositionStatus(variables):
    if FCorpActionElectionStatesSetup.CorporateActionUsingBusinessProcess():
        electionStates = [s for s in acm.FStateChart['CorpActionElectionStateChart'
                                ].StatesByName().Keys() if s != 'Processed']
        variables.createVariable(['Status',
                'Status',
                'string', electionStates, None,
                0, None, tt_Status, None, 1],)

ael_variables = FBDPGui.AelVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Name',
                'Name',
                'string', None, None,
                None, 1, tt_Name, None, 1],
        ['Party',
                'Party',
                'FParty', None, None,
                None, 1, tt_Party, None, 0],
        ['Instrument',
                'Instrument',
                'FInstrument', None, None,
                None, 1, tt_Instrument, None, 0],
        ['EligiblePosition',
                'Eligible Position',
                'string', None, None,
                None, 1, tt_EligiblePosition, None, 0],
        ['StockEntitlement',
                'Stock Entitlement',
                'string', None, None,
                None, 1, tt_StockEntitlement, None, 0],
        ['CashEntitlement',
                'Cash Entitlement',
                'string', None, None,
                None, 1, tt_CashEntitlement, None, 0],
        ['Quantity',
                'Elected Quantity',
                'string', None, None,
                None, 1, tt_Quantity, None, 1],
        ['Price',
                'Price',
                'string', None, None,
                None, 1, tt_Price, None, 1],
        ['CaChoice',
                'Choice_hidden',
                'FCorporateActionChoice', None, None,
                0, 1, tt_CaChoice, None, 0],
        ['ReplyDate',
                'Reply Date',
                'string', ['Today', 'Next banking day'], None,
                0, None, tt_ReplyDate, None],
        ['Deadline',
                'Deadline',
                'string', ['Today', 'Next banking day'], None,
                0, None, tt_Deadline, None],
        ['TextInfo',
                'Text Information',
                'string', None, None,
                None, None, tt_text],
        ['Elected',
                'Elected',
                'int', [1, 0], 0,
                0, 0, tt_Elected, None, None],
        #['Percentage',
        #        'Percentage',
        #        'string', None, None,
        #        None, 1, '', None, 1],
        ['Oid',
                'Oid_hidden',
                'string', None, None,
                None, None, tt_Oid, oid_cb])

_createCorpActionPositionStatus(ael_variables)
#FBDPGui.createAdditionalInfoVariables(ael_variables, ADDITIONALINFO_RECORDTYPE, ['Position'])
