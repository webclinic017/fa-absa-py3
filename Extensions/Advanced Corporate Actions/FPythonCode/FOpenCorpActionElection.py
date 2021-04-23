""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FOpenCorpActionElection.py"
"""----------------------------------------------------------------------------
MODULE
    FOpenCorpActionElection - GUI Module to open to a corporate action 
    Election definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FCorpActionElectionStatesSetup
import FBusinessProcessUtils
import FBDPCommon
from FPositionUtils import GetAttributeValue
from FCorpActionUtils import positionBusinessProcessTransition, StateTransitionFromElectedQuantity
from FCorpActionUtils import get_elections_for_position, find_total_percentage
import FCAElectionColumns
import math
import locale


infoSpecs = acm.FAdditionalInfoSpec.Select("recType=CorpActionElection")

def get_shell():
    apps = acm.UX().SessionManager().RunningApplications()
    index = apps.FindString('Modify Corporate Action Election')
    corp_act = acm.UX().SessionManager().RunningApplications()[index]
    return corp_act.Shell()

#check if we have elected more than we should for this option
#All elections are a number of shares!
def validate_election(election, quantity):
    shell = get_shell()
    cash_entitlement = FCAElectionColumns.caCashEntitlement(election, election.CaChoice().CaPayouts())
    stock_entitlement = FCAElectionColumns.caStockEntitlement(election, election.CaChoice().CaPayouts())
    eligible_position =  FCAElectionColumns.caEligiblePosition(election, None)
    
    if (abs(eligible_position + quantity) != abs(eligible_position) + abs(quantity) or 
            abs(quantity) > abs(eligible_position)):
        msg = 'Please elect a valid quantity.'
        acm.UX().Dialogs().MessageBoxInformation(shell, msg) 
        return False
    if math.fabs(eligible_position) > 0:
        #check if we have elected more than we should for all options
        elections = get_elections_for_position(election, election.PositionInstance())
        elections.remove(election)
        total = find_total_percentage(elections)
        percentage = math.fabs(100.0 * quantity / eligible_position)
        if total + percentage > 100.0:
            msg = 'The total elected is greater than the entitlement. Please reduce other election quantities first.'
            acm.UX().Dialogs().MessageBoxInformation(shell, msg)
            return False
    
    return True

def run_main(d, election, newElection = 0):
    oldQuantity = election.Quantity()
    if validate_election(election, float(d['Quantity'][0])) == False:
        return False
    election.Name = d['Name']
    election.Portfolio = None
    election.TradeFilter = None
    election.Price = d['Price']
    election.CaChoice = d['CaChoice']
    d['Quantity'] = ''.join(d['Quantity'])
    locale.setlocale(locale.LC_ALL, '')    
    election.Quantity = locale.atof(d['Quantity'])
    eligible_position =  FCAElectionColumns.caEligiblePosition(election, None)
    if d['Elected'] != 1:
        election.Percentage = 0.0 # initialise
        election.Quantity = 0.0
    else:
        #Set the percentage to 100 for NOACs
        #or other actions to quickly elect 100%
        #without needing to enter the quantity
        election.Percentage = 100.0
        if election.Quantity() == 0.0:
            election.Quantity = eligible_position
    election.ReplyDate = acm.Time.UtcToLocal(FBDPCommon.toDateTime(d['ReplyDate']))
    election.Deadline = acm.Time.UtcToLocal(FBDPCommon.toDateTime(d['Deadline']))
    election.Party = d['Party']
    if math.fabs(eligible_position) > 0:
        election.Percentage = math.fabs(100.0 * election.Quantity() / eligible_position)

    customText = election.TextInfo()
    if not customText:
        customText = acm.FCustomTextObject()
        customText.Name(str(election.Oid()) + election.Name())
    customText.Text(d['TextInfo'])
    customText.Commit()
    election.TextInfo(customText)

    existingAddInfoSpec = []
    addinfo = election.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        existingAddInfoSpec.append(name)
        if name in list(d.keys()):
            i.FieldValue(d[name])
    election.Commit()

    addinfo = election.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        if name in list(d.keys()) and name not in existingAddInfoSpec:
            existingAddInfoSpec.append(name)
            i.FieldValue(d[name])
            i.Commit()
    
    for spec in infoSpecs:
        name = spec.Name()
        if name in existingAddInfoSpec:
            continue

        if name in list(d.keys()) and d[name]:
            newAddInfo = acm.FAdditionalInfo()
            newAddInfo.AddInf(spec)
            newAddInfo.Parent(election)
            newAddInfo.FieldValue(d[name])
            newAddInfo.Commit()

    if FCorpActionElectionStatesSetup.CorporateActionUsingBusinessProcess():
        FCorpActionElectionStatesSetup.CreateCorporateActionElectionStateChart()
        if newElection:
            print('Create BP.................')
            bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(election,
                                    'CorpActionElectionStateChart')
            bp.Commit()
        
        newQuantity = election.Quantity()
        if oldQuantity != newQuantity and (oldQuantity == 0.0 or newQuantity == 0.0):
            StateTransitionFromElectedQuantity(election, oldQuantity, eligible_position)
        else:
            toState = d['Status']
            positionBusinessProcessTransition(election, toState)
