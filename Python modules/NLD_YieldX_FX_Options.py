'''----------------------------------------------------------------------------------------------------------------
MODULE
    NLD_YieldX_FX_Options
DESCRIPTION
    Developer           : Nidheesh Sharma
    Date                : 2012-08-21
    Purpose             : Sets mtm from feed on for trades on given portfolios
                          This is for yieldx fx options in NLD desk that feed from CRE
    Requestor           : Pedro de Moura
    CR Number           : C415508
ENDDESCRIPTION

HISTORY
    Date:       CR Number:      Developer:              Description:
----------------------------------------------------------------------------------------------------------------'''

import sys

import acm

import FBDPGui
import FBDPString

INSTRUMENTS = {}
SCRIPT_NAME = 'NLD_YieldX_FX_Options'
logme = FBDPString.logme

#Generate instrument pay type list to be used as drop downs in the GUI
startPayTypeList = {'Spot':'Spot',
                   'Future':'Future',
                   'Forward':'Forward',
                   'Contingent':'Contingent'}
startPayTypeKeys = startPayTypeList.keys()

#------------------------------------------------------------------------------------------------------------------
#Function to get instruments, from the trades of specified portfolios, that need mtm from feed turned on
#------------------------------------------------------------------------------------------------------------------
def Get_Instruments_Of_Trades(date, portfolio, acquirer, counterparty, payType):
    trades = portfolio.Trades()
    for trade in trades:
        instrument = trade.Instrument()
        if instrument.Name() not in INSTRUMENTS:
            if instrument.InsType() in ('Option') and instrument.PayType() == payType and instrument.ExpiryDate() >= date:
                if trade.Counterparty() in counterparty and trade.Acquirer() in acquirer and trade.Status() not in ('Void', 'Simulated', 'Terminated'):
                    INSTRUMENTS[instrument.Name()] = instrument

#------------------------------------------------------------------------------------------------------------------
#Function to turn on mtm from feed and to ensure that the price finding group is defined
#------------------------------------------------------------------------------------------------------------------
def Turn_MTM_On(priceFindingGroup):
    for i in INSTRUMENTS:
        instrument = INSTRUMENTS[i]
        if not instrument.MtmFromFeed():
            try:
                if instrument.PriceFindingChlItem() == None:
                    instrument.PriceFindingChlItem(priceFindingGroup)
                instrument.MtmFromFeed(1)
                instrument.Commit()
                logme ( 'MTM From Feed turned on: %s' % instrument.Name() )
            except Exception as e:
                logme ( 'Could not turn on MTM From Feed for %s: %s' % (instrument.Name(), e) )


# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(['portfolio', 'Portfolio', 'FPhysicalPortfolio', None, None, 1, 1, 'The portfolio of the trades that require MTM From Feed turned on. Separate multiple portfolio names by a comma.', None, 1],
                ['acquirer', 'Acquirer', 'FParty', None, None, 1, 1, 'The acquirer of the trades that require MTM From Feed turned on. Separate multiple acquirer names by a comma.', None, 1],
                ['counterparty', 'Counterparty', 'FCounterParty', None, None, 1, 1, 'The counterparty of the trades that require MTM From Feed turned on. Separate multiple counterparty names by a comma.', None, 1],
                ['payType', 'Pay Type', 'string', startPayTypeKeys, 'Future', 1, 0, 'The pay type of the trades that require MTM From Feed turned on.', None, 1],
                )

def ael_main(ael_dict):
    logme.setLogmeVar(SCRIPT_NAME,
                      ael_dict['Logmode'],
                      ael_dict['LogToConsole'],
                      ael_dict['LogToFile'],
                      ael_dict['Logfile'],
                      ael_dict['SendReportByMail'],
                      ael_dict['MailList'],
                      ael_dict['ReportMessageType'])

    date = acm.Time().DateNow()
    portfolios = ael_dict['portfolio']
    acquirer = ael_dict['acquirer']
    counterparty = ael_dict['counterparty']
    payType = ael_dict['payType']

    #to ensure the price finding group is not none when setting mtm from feed on - if none then set it to close
    priceFindingGroup = None
    # FIXME: It would be great if we could just use a combined condition
    # (i.e. name = something and list = something else),
    # but unfortunately that does not work.
    allChoiceLists = acm.FChoiceList.Select("name = PriceFindingGroup")
    choiceLists = [cl for cl in allChoiceLists if cl.List() == "MASTER"]
    if not choiceLists:
        error_message = ("Error: There is no "
            "candidate choice list with name == PriceFindingGroup.")
        print >> sys.stderr, error_message
        raise RuntimeError(error_message)
    if len(choiceLists) > 1:
        print >> sys.stderr, ("Warning: There is more than one "
            "candidate choice list with name == PriceFindingGroup. "
            "Selecting the first one.")
    choiceList = choiceLists[0]
    for priceFindingChoice in choiceList.Choices():
        if priceFindingChoice.Name() == 'Close':
            priceFindingGroup = priceFindingChoice

    for portfolio in portfolios:
        Get_Instruments_Of_Trades(date, portfolio, acquirer, counterparty, payType)
        Turn_MTM_On(priceFindingGroup)
