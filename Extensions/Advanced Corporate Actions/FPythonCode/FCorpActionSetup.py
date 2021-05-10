""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionSetup.py"
"""----------------------------------------------------------------------------
 MODULE
     FCorpActionSetup - Module which create the additional infos needed for the corporate
    action processing. 

 DESCRIPTION
     This module set up all the necessary additional infos for the advanced 
    corporate action processing.
 ---------------------------------------------------------------------------"""
import FBDPCommon
import acm
import FBDPCurrentContext
import FCorpActionElectionStatesSetup
    
def CreateAdditionalInfo():
    FBDPCommon.CreateAdditionalInfo('Position', 'CorpActionElection',
    'Standard', 'Integer', description='Reference to Position', subTypes=[])
    FBDPCommon.CreateAdditionalInfo('PositionInstance', 'CorpActionElection',
    'Standard', 'Integer', description='Position', subTypes=[])
    FBDPCommon.CreateAdditionalInfo('RollbackElection', 'CorpActionElection',
    'Standard', 'String', description='RollbackElection', subTypes=[])
    FBDPCommon.CreateAdditionalInfo('TaxRate', 'CorpActionElection',
    'Standard', 'Double', description='Tax Rate Applicable', 
    subTypes=[], defaultValue=1.0)
    FBDPCommon.CreateAdditionalInfo('SuggestedBy', 'CorpActionElection',
    'Standard', 'String', description='Suggested By Trader', subTypes=[])
    FBDPCommon.CreateAdditionalInfo('TraderElection', 'CorpActionElection',
    'Standard', 'String', description='Elected By Trader', subTypes=[], defaultValue='N/A')
    FBDPCommon.CreateAdditionalInfo('TraderInterestedIn', 'CorpAction',
    'Standard', 'String', description='Intererted By Trader', subTypes=[])
    FBDPCommon.CreateAdditionalInfo('MarkitCAStatus', 'CorpAction',
    'Standard', 'String', description='Workflow Status', subTypes=[])
    FBDPCommon.CreateAdditionalInfo('CADefinitionFile', 'CorpAction',
    'Standard', 'String', description='File defines the Corporate Action', subTypes=[])

def CreateMarketPlaces():
    MarketNames = ['ExDate', 'RecordDate']
    for mktName in MarketNames:
        if not acm.FMarketPlace[mktName]:
            mkt = acm.FMarketPlace()
            mkt.Name(mktName)
            mkt.Commit()

def CreatePositionSepcification():
    spec = acm.FPositionSpecification["Corporate Actions"]
    if spec:
        return

    specification= acm.FPositionSpecification()
    specification.Name("Corporate Actions")
    specification.Commit()
    attributes = ['Counterparty.Name', 'Portfolio.Name', 'Instrument.Name', 'Instrument.Underlying.Name']
    for attr in attributes:
        definition = acm.FPositionAttributeDefinition()
        definition.Definition(attr)
        definition.Specification(specification)
        definition.Commit()

def Setup():
    FBDPCurrentContext.CreateLog("FCorpActionSetup", 1, 1, 0, 0,
        False, "", "")
    CreateAdditionalInfo()
    CreatePositionSepcification()
    CreateMarketPlaces()
    FCorpActionElectionStatesSetup.CreateCorporateActionElectionStateChart()

Setup()