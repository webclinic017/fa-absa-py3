"""-----------------------------------------------------------------------------
MODULE
    PS_RepoBonds_InternalRepo

DESCRIPTION
    Date                : 17 May 2013
    Purpose             : Book internal repo according to instructions from input csv file
    Department and Desk : Prime Services Desk
    Requester           : Francois Henrion & Kelly Hattingh
    Developer           : Peter Fabian
    CR Number           : CHNG0001033361
    
NOTES
    
    
HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2013-05-21 C1056001     Peter Fabian       Adjustable price for BSB booking (YMtM column)
2013-07-26 C1197225     Peter Fabian       Adjustments to support new BSBbooker
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
from PS_RepoBonds_RepoRates import InsRepoRatesReader
from PS_RepoBonds_BSBBooker import bookBsb
from collections import defaultdict

import os
import acm
import FBDPGui

def instrumentActiveOnDate(ins, date):
    # ExpiryDate is actually + 00:00:00 which misbehaves
    # if we don't get rid of it
    return ins.StartDate() <= date < acm.Time.AsDate(ins.ExpiryDate())


def getPositionsForInternalRepo(settleDate, verbose=False):
    """ Get sum of quantities on active BSBacks in PB_RISK_FV_CLIENTBONDS
    """
    bsbTrades = defaultdict(lambda: defaultdict(list))
    risk_fv_prf = acm.FPhysicalPortfolio['PB_RISK_FV_CLIENTBONDS']
    for trade in risk_fv_prf.Trades():
        if trade.Status() in ('Simulated', 'Void', 'Terminated', 'Confirmed Void'):
            continue
        ins = trade.Instrument()
        ctptyName = trade.Counterparty().Name()
        if (ins.InsType() == 'BuySellback'
                and instrumentActiveOnDate(ins, settleDate)):
            undName = ins.Underlying().Name()
            bsbTrades[undName][ctptyName].append(trade)

    # this is slightly suboptimal as this sum can be calculated
    # in the loop above, but it's useful for debug reasons
    # to know which trades were summed up, so I'm leaving it here
    bsbQties = defaultdict(lambda: defaultdict(int))
    for insName, tradesForInstr in bsbTrades.items():
        for clientName, trades in tradesForInstr.items():
            bsbQties[insName][clientName] = sum(
                                                trade.Quantity() for trade in trades
                                                )

    if verbose:
        acm.LogAll("="*20, "BSBacks", "="*20)
        insNames = list(bsbQties.keys())
        insNames.sort()
        for insName in insNames:
            acm.LogAll(insName)
            clientNames = list(bsbQties[insName].keys())
            clientNames.sort()
            for clientName in clientNames:
                acm.LogAll("\t %s %s" % (clientName, bsbQties[insName][clientName]))
                acm.LogAll([[trade.Oid(), trade.Quantity()] 
                         for trade in bsbTrades[insName][clientName]])

    return bsbQties

def bookInternalBsb(positions, dateStart, dateEnd, repoRates):
    """ 
        we take sum of qties for the instrument for all clients
        and book a repo
        with resulting quantity to repo prf for each instrument 
        (with mirror in PB_RISK_FV_CLIENTBONDS)
    """
    acquirer = acm.FParty['CM FUNDING']
    ctpty = acm.FParty['PRIME SERVICES DESK']
    cp_prf = acm.FPhysicalPortfolio['PB_RISK_FV_CLIENTBONDS']


    for insId, qtyForClient in positions.items():
        acm.LogAll("="*30)
        acm.LogAll(insId)
        ins = acm.FInstrument[insId]
        qtyToRepo = 0
        if qtyForClient:
            qtyToRepo = sum(qtyForClient.values())


        repoRate = repoRates.repoRateForIns(insId)
        direction = "offer" if qtyToRepo < 0 else "bid"
        usedRate = 0
        if repoRate:
            usedRate = getattr(repoRate, direction)
            prf = acm.FPhysicalPortfolio[repoRate.repo_to]
            if not prf:
                acm.LogAll("No portfolio '%s' found" % repoRate.repo_to)
                continue
            else:
                acquirer = prf.PortfolioOwner()


        else:
            acm.LogAll(" no rate for %s, not booking" % insId)
            continue

        if qtyToRepo:
            for clientName, qty in qtyForClient.items():
                acm.LogAll("\t %s -> %s" % (clientName, qty))
            acm.LogAll(" => Booking bsb with qty %s to %s from %s to %s at %s rate = %s"
            % (qtyToRepo, repoRate.repo_to, dateStart, dateEnd, direction, usedRate))
            try:
                bookBsb(dateStart, dateEnd, usedRate, ins, qtyToRepo, prf, acquirer,
                    ctpty, cp_prf, tradeDate=min(acm.Time.DateToday(), dateStart),
                    acquireDate=dateStart, startPrice=repoRate.YMtM, transaction=None)
            except Exception as ex:
                acm.LogAll('    Could not book BSB to portfolio %(portfolio)s,'
                        ' for und instrument %(instrument)s, amount %(amount)f:'
                        ' %(ex)s' % 
                            {'portfolio': prf.Name(), 
                             'instrument': ins.Name(), 'amount': qtyToRepo, 
                             'ex': str(ex)}
                        )
                # eating exception here as I want to book for other clients
        else:
            for clientName, qty in qtyForClient.items():
                acm.LogAll("\t %s -> %s" % (clientName, qty))
            acm.LogAll(" => Qty = 0, nothing to book")




calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()

def enableCustomDate(index, fieldValues):
    ael_variables[2][9] = (fieldValues[1] == 'Yes')
    return fieldValues

directorySelection = acm.FFileSelection()

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(
                 ['verboseLog', 'Verbose log', 'string', ['No', 'Yes'], 'No', 1, 0, 'Output more detailed information?', None, 1],
                 ['overrideDate', 'Override date?', 'string', ['No', 'Yes'], 'No', 1, 0, 'Override date from the upload file?', enableCustomDate, 1],
                 ['dateCustom', 'Date Custom', 'string', None, TODAY, 0, 0, 'Custom date', None, 0],
                 ['filePath', 'Directory', directorySelection, None, directorySelection, 1, 1, 'Directory where files will be uploaded from.', None, 1],
                )


def ael_main(dictionary):
    calendar = acm.FCalendar['ZAR Johannesburg']
    # get the date
    inputDate = dictionary['dateCustom'] \
        if dictionary['overrideDate'] == 'Yes'\
        else TODAY
    acm.LogAll("Input date %s" % inputDate)
    settleDate = calendar.AdjustBankingDays(inputDate, 2)
    acm.LogAll("Settle date %s" % settleDate)

    # get file name
    filepath = str(dictionary['filePath'])  # .SelectedDirectory().Text()
    if os.path.exists(filepath):
        acm.LogAll("Using repo rates file %s" % filepath)
    else:
        raise RuntimeError("File %s does not exist" % filepath)
    try:
        # prepare repo rates
        repoRates = InsRepoRatesReader(filepath)

        # prepare positions for bsbacks from PB_RISK_FV_CLIENTBONDS portfolio
        verbose = dictionary['verboseLog'] == 'Yes'
        bsbQties = getPositionsForInternalRepo(settleDate, verbose)

        # book repos
        bsbStartDate = settleDate
        bsbEndDate = calendar.AdjustBankingDays(bsbStartDate, 1)
        bookInternalBsb(bsbQties, bsbStartDate, bsbEndDate, repoRates)
    except Exception as e:
        acm.LogAll("Error booking BuySellbacks: %s" % e)
        raise
    else:
        acm.LogAll("Completed successfully")

