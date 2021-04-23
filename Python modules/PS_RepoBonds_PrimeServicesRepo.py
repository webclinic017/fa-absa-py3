"""-----------------------------------------------------------------------------
MODULE
    PS_RepoBonds_InternalRepo

DESCRIPTION
    Date                : 26 July 2013
    Purpose             : Book Prime Services repo according to instructions from input csv file
    Department and Desk : Prime Services Desk
    Requester           : Francois Henrion
    Developer           : Peter Fabian
    CR Number           : CHNG000C1197225
    
NOTES
    
    
HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2014-08-29 2199087      Ondrej Bahounek    Correct term of booked BSBacks.
2017-11-02 5105273      Marcelo Almiron    Change precision in booking from 4 to
                                           up to 5 digits.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
from PS_RepoBonds_RepoRates import ClientRepoRate, ClientRepoRatesReader
from PS_RepoBonds_BSBBooker import bookBsb
from collections import defaultdict

import re
import os
import ael
import acm
import FBDPGui

class BSBBookingStep(object):
    def __init__(self, positions, settleDate, repoRates):
        self.acquirer = None
        self.ctpty = None
        self.cp_prf = None
        self.positions = positions
        self.settleDate = settleDate
        self.repoRates = repoRates
        self.calendar = acm.FCalendar['ZAR Johannesburg']
    
    @staticmethod
    def _nextThursday(date):
        """ Returns the next Thursday after the specified date
        """
        date = acm.Time.DateAddDelta(date, 0, 0, 1)
        while acm.Time.DayOfWeek(date) != 'Thursday':
            date = acm.Time.DateAddDelta(date, 0, 0, 1)
        return date

    def _nextThursdayOrFollowingBusDay(self, date):
        """ Returns the next Thursday or the following business day
            if Thursday is a public holiday in Jhb
        """
        resultDate = BSBBookingStep._nextThursday(date)
        if self.calendar.IsNonBankingDay(None, None, resultDate):
            resultDate = self.calendar.AdjustBankingDays(resultDate, 1)
        return resultDate
    
    def _plusNWeeksThursday(self, date, n):
        """ Returns the first Thursday or following business days after n weeks.
        """
        daysInAWeek = 7 # should this change, we can easily adjust
        if n > 1:
            date = acm.Time.DateAddDelta(date, 0, 0, (n-1) * daysInAWeek)
        nextThursday = self._nextThursdayOrFollowingBusDay(date)
        return nextThursday
    
    def bsbStartDate(self):
        """ Returns the start date for the BSBack
        """
        return self.settleDate
    
    def bsbEndDate(self, clientName, instrument):
        """ Returns the end date for the BSBack
        """
        repoFrequency = self.repoRates.getFrequency(instrument.Name(), clientName)
        
        regexp = '(\d{1,2})(day|week|month)'
        m = re.match(regexp, repoFrequency)
        if m:
            period, period_type = m.groups()
        else:
            period, period_type = 1, 'day'
        period = int(period)

        if period_type == 'week':
            return self._plusNWeeksThursday(self.bsbStartDate(), period) # period is week's #
        elif period_type == 'month':
            return self._plusNWeeksThursday(self.bsbStartDate(), period * 4) # period is month's #
        elif period_type == 'day':
            nextNdaysDate = acm.Time.DateAddDelta(self.bsbStartDate(), 0, 0, period-1) # period is day's #
            return self.calendar.AdjustBankingDays(nextNdaysDate, 1)  
        
    def check_end_date(self, start_date, end_date, ins, portf, acquirer, ctpty):
        """ Check if end date of existing BSBacks lies within interval for new BSBack.
            In that case select existing intrument's end date instead of the new one.
        """
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portf.Name())
        query.AddAttrNode('Acquirer.Name', 'EQUAL', acquirer.Name())
        query.AddAttrNode('Counterparty.Name', 'EQUAL', ctpty.Name())
        query.AddAttrNode('Instrument.Underlying.Name', 'EQUAL', ins.Name())
        query.AddAttrNode('Instrument.StartDate', 'LESS_EQUAL', start_date)
        query.AddAttrNode('Instrument.ExpiryDate', 'GREATER', start_date)
        query.AddAttrNode('Instrument.ExpiryDate', 'LESS', end_date)
        trades = query.Select()
        end_dates = [t.Instrument().ExpiryDate() for t in trades] + [end_date]
        return min(end_dates)
    
    def book(self, ins, clientName, qtyToRepo, transaction):
        """ Book the BSBack according to the parameters and 
            client configuration
        """
        if not qtyToRepo:
            acm.LogAll(" => qty = 0, nothing to book")
            return

        ctpty = self.bsbCounterparty(clientName)
        
        # this is from the input csv file
        repoRate = self.repoRates.getRate(ins.Name(), clientName)
        if qtyToRepo < 0:
            direction = "offer"
        else:
            direction = "bid"
            
        usedRate = 0
        if repoRate:
            usedRate = float(getattr(repoRate, direction))
            prf = self.bsbPortfolio(clientName, repoRate)
            acquirer = self.acquirer

        else:
            acm.LogAll(" no rate for %s, not booking" % ins.Name())
            return

        dateStart = self.bsbStartDate()
        dateEnd = self.bsbEndDate(clientName, ins)
        dateEnd = self.check_end_date(dateStart, dateEnd, ins, prf, acquirer, ctpty)
        
        cp_prf = self.cp_prf
        qtyToRepo = self.qtyFactor * qtyToRepo 
        
        acm.LogAll(" => Booking bsb with qty %s to %s from %s to %s at %s rate = %s"
        % (qtyToRepo, prf.Name(), dateStart, dateEnd, direction, usedRate))
        try:
            return bookBsb(dateStart, dateEnd, usedRate, ins, qtyToRepo, prf, acquirer,
                    ctpty, cp_prf=cp_prf, tradeDate=min(acm.Time.DateToday(), dateStart), 
                    acquireDate=dateStart, startPrice=repoRate.YMtM, transaction=transaction)
        except Exception as ex:
            acm.LogAll('    Could not book BSB to portfolio %(portfolio)s, '
                    'for und instrument %(instrument)s, amount %(amount)f:'
                    ' %(ex)s' % 
                    {'portfolio': prf.Name(), 
                     'instrument': ins.Name(), 'amount': qtyToRepo, 
                     'ex': str(ex)}
                    )
            raise
            


    
class Step1(BSBBookingStep):
    def __init__(self, positions, settleDate, repoRates):
        super(Step1, self).__init__(positions, settleDate, repoRates)
        self.acquirer = acm.FParty['PRIME SERVICES DESK']
        self.ctpty = acm.FParty['ABSA BANK LTD']
        # prf for client map
        self.prfForClient = defaultdict(lambda: defaultdict(acm.FPhysicalPortfolio))
        self.qtyFactor = -1
        # no mirror trade, no counterparty prf
        self.cp_prf = None
        
    def _buildPrfMap(self):
        """ Creates a mapping between each client, instrument and portfolio.
            Beacuse we need to book the BSB to the same prf 
            where the underlying bond is booked
        """
        clientReportingPrfs = acm.FCompoundPortfolio['CLIENT REPORTING'].AllPhysicalPortfolios()
        repoedBondPrfs = [ prf for prf in clientReportingPrfs
                            if PrimeServicesBsb._prfRelevantForRepoing(prf)
                         ]

        for prf in repoedBondPrfs:            
            clientName = prf.AdditionalInfo().PSClientCallAcc().Trades()[0].Counterparty().Name()
            for trd in prf.Trades():
                if trd.Status() in ('Simulated', 'Void', 'Confirmed Void'):
                    continue
                ins = trd.Instrument()
                if ins.InsType() in ('Bond', 'FRN', 'IndexLinkedBond'):
                    insName = PrimeServicesBsb.removeMTMfromInsName(trd.Instrument().Name())
                    self.prfForClient[clientName][insName] = prf        
        
    def bsbPortfolio(self, clientName, repoRate):
        """ Returns the portfolio where to book the BSBack
            according to prf of the underlying instrument 
            and the client
        """
        if not self.prfForClient:
            self._buildPrfMap()
        if (clientName in self.prfForClient
                and repoRate.insid in self.prfForClient[clientName]):
            return self.prfForClient[clientName][repoRate.insid]
        else:
            acm.LogAll("No prf for client name %s found" % clientName)
            
    def bsbCounterparty(self, clientName):
        """ Returns counterparty for the BSBack
            
            In this booking step it's the one specified in the constructor.
        """
        return self.ctpty
    

class Step2(BSBBookingStep):
    def __init__(self, positions, settleDate, repoRates):
        super(Step2, self).__init__(positions, settleDate, repoRates)
        self.acquirer = acm.FParty['PRIME SERVICES DESK']
        self.qtyFactor = 1
        # no mirror trade, no counterparty prf
        self.cp_prf = None
    
    @staticmethod
    def bsbPortfolio(clientName, repoRate):
        """ Returns the portfolio where to book the BSBack
            
            In this booking step it's just the one specified in the 
            input csv file
        """
        prf = acm.FPhysicalPortfolio[repoRate.repo_to]
        if prf:
            return prf
        else:
            raise RuntimeError("No such portfolio found: %s" % repoRate.repo_to)
    
    @staticmethod
    def bsbCounterparty(clientName):
        """ Returns counterparty for the BSBack
            
            In this booking step it's the client itself.
        """
        # ctpty == client
        return acm.FParty[clientName]


class PS_RepoBonds_Transaction(list):
    """ Void trades if transaction is not successful, 
        do nothing for other object types
    """
    @staticmethod
    def _isAcmTrade(object):
        try:
            return object.IsKindOf(acm.FTrade)
        except:
            return False
    
    def begin(self):
        if self:
            raise RuntimeError("Another transaction has not yet finished")
        
    def commit(self):
        self[:] = []
        
    def abort(self):
        if not self:
            return
        
        acm.LogAll("Aborting the booking...")
        acm.BeginTransaction()
        try:
            while self:
                object_ = self.pop()
                if self._isAcmTrade(object_):
                    acm.LogAll("Voiding trade %s" % object_.Oid())
                    object_.Status('Void')
                    object_.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise
            
            

class PrimeServicesBsb(object):
    def __init__(self, settleDate, repoRates):
        self.clientReportingTrades = defaultdict(lambda: defaultdict(list))
        self.secondLegTrades = {}
        self.ctptyNameFor = {}
        self.settleDate = settleDate
        self.repoRates = repoRates
        self.transaction = PS_RepoBonds_Transaction()
    
    @staticmethod
    def removeMTMfromInsName(insName):
        if insName.endswith('/MTM'):
            if not acm.FInstrument[insName[:-4]]:
                raise RuntimeError("Can't find non-/MTM equivalent for %s" % insName)
            
            insName = insName[:-4]
        return insName
    
    @staticmethod
    def instrumentActiveOnDate(ins, date):
        # ExpiryDate is actually + 00:00:00 which misbehaves
        # if we don't get rid of it
        return ins.StartDate() <= date < acm.Time.AsDate(ins.ExpiryDate())

    @staticmethod
    def _prfRelevantForRepoing(prf):
        """ Test/filter for CR portfolios relevant for creating BSBacks
            
            This is based on the naming conventions right now 
            but hopefully will one day be based on some prf metadata
        """
        prfName = prf.Name()
        #print prf.Name()
        return (# credit and repo bonds
                'BOND' in prfName
                # but not naked bonds
                and 'NAKEDBOND' not in prfName
                # and also not test client's bond collaterals
                and 'CLIENT1_BOND_COLL' not in prfName
                # exclude old Oakhaven positions as well
                and 'OAKHAVEN_OLD' not in prfName
                and
                # only financed are repo-ed
                    (
                     not prf.AdditionalInfo().PS_FullyFunded()
                     or prf.AdditionalInfo().PS_FullyFunded() == 'No'
                    )
                and prf.AdditionalInfo().PSClientCallAcc().Trades()[0].Counterparty().Name() != "TEST"
                )

    def _getClientName(self, trade):
        """ Returns client's name for a trade -- determined by portfolio where the 
            trade is booked
            
            Uses dict to cache prf name - client name relationship
        """
        prfName = trade.Portfolio().Name()
        if prfName not in self.ctptyNameFor:
            self.ctptyNameFor[prfName] = trade.Portfolio().AdditionalInfo().PSClientCallAcc()\
                                    .Trades()[0].Counterparty().Name()
        return self.ctptyNameFor[prfName]

    def _addTradeIfRelevant(self, trade):
        """ Adds trade to internal dict if it is relevant for creating BSBacks -- 
            That means settled bonds and active BSBacks.
        """
        if trade.Status() in ('Simulated', 'Void', 'Confirmed Void'):
            return
        
        ins = trade.Instrument()
        
        if ins.InsType() in ('Bond', 'IndexLinkedBond', 'FRN'):
            if trade.AcquireDay() > self.settleDate:
                return
            
            # remove /MTM if applicable
            insName = PrimeServicesBsb.removeMTMfromInsName(ins.Name())
                
        elif ins.InsType() == 'BuySellback':
            if not PrimeServicesBsb.instrumentActiveOnDate(ins, self.settleDate):
                return
            
            insName = ins.Underlying().Name()
        else:
            return
                
        clientName = self._getClientName(trade)
        self.clientReportingTrades[insName][clientName].append(trade)

    def getPositionsForClientsRepo(self, verbose=False):
        """ Calculate quantities for repo operations -- sums settled bonds 
            and active BSBacks and store resulting qty in a dict
        """
        clientReportingPrfs = acm.FCompoundPortfolio['CLIENT REPORTING'].AllPhysicalPortfolios()
        repoedBondPrfs = [ prf for prf in clientReportingPrfs
                                if PrimeServicesBsb._prfRelevantForRepoing(prf)
                          ]
    
        # does this scale? not sure...
        for prf in repoedBondPrfs:
            for trade in prf.Trades():
                self._addTradeIfRelevant(trade)
                
    
        # this is just for debug reasons, 
        # could be merged into the loop above 
        settledQties = defaultdict(lambda: defaultdict(int))
        for insName, tradesForInstr in self.clientReportingTrades.iteritems():
            for clientName, trades in tradesForInstr.iteritems():
                settledQties[insName][clientName] = sum(
                                                    trade.Quantity() for trade in trades
                                                    )
                              
                # round quantity to 5 decimal places
                # also required to eliminate too small values which are not zeros
                settledQties[insName][clientName] = round(settledQties[insName][clientName], 5)
    
        if verbose:
            insNames = settledQties.keys()
            insNames.sort()
            for insName in insNames:
                acm.LogAll(insName)
                clientNames = settledQties[insName].keys()
                clientNames.sort()
                for clientName in clientNames:
                    acm.LogAll("\t %s %s" % (clientName, settledQties[insName][clientName]))
    
        return settledQties

    def bookPrimeServicesBsb(self):
        """ Books the BSBacks for the clients
        """
        # prepare positions for bsbacks from client bond portfolios
        verbose = True
        positions = self.getPositionsForClientsRepo(verbose)
        
        bookingStep1 = Step1(positions, self.settleDate, self.repoRates)
        bookingStep2 = Step2(positions, self.settleDate, self.repoRates)
        
        for insId, qtyForClient in positions.iteritems():
            acm.LogAll("="*30)
            acm.LogAll(insId)
            ins = acm.FInstrument[insId]
            
            for clientName, qtyToRepo in qtyForClient.iteritems():
                acm.LogAll(clientName)
                repoRate = self.repoRates.getRate(ins.Name(), clientName)
                if not repoRate:
                    acm.LogAll("Could not get rate for instrument %s and client %s" 
                            % (ins.Name(), clientName)
                            )
                    continue
                
                self.transaction.begin()
                try:
                    bookingStep1.book(ins, clientName, qtyToRepo, self.transaction)
                    bookingStep2.book(ins, clientName, qtyToRepo, self.transaction)
                    self.transaction.commit()
                except Exception as e:
                    self.transaction.abort()
                    # eating exception here as I want to book for other clients
                    acm.LogAll("Failed to book BSB for underlying %s and client %s: %s" 
                            % (insId, clientName, e))
                    
    
    

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()

def enableCustomDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == 'Yes')
    return fieldValues

directorySelection = acm.FFileSelection()

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(
                 ['overrideDate', 'Override date?', 'string', ['No', 'Yes'], 'No', 1, 0, 'Override date from the upload file?', enableCustomDate, 1],
                 ['dateCustom', 'Date Custom', 'string', None, TODAY, 0, 0, 'Custom date', None, 0],
                 ['filePath', 'Csv rate file', directorySelection, None, directorySelection, 1, 1, 'Directory where files will be uploaded from.', None, 1],
                )


def ael_main(dictionary):
    # get the date
    inputDate = dictionary['dateCustom'] \
        if dictionary['overrideDate'] == 'Yes'\
        else TODAY
    acm.LogAll("Input date %s" % inputDate)
    settleDate = calendar.AdjustBankingDays(inputDate, 2)
    acm.LogAll("Settle date %s" % settleDate)

    # get file name
    filepath = str(dictionary['filePath'])
    if os.path.exists(filepath):
        acm.LogAll("Using repo rates file %s" % filepath)
    else:
        acm.LogAll("File %s does not exist" % filepath)
        raise RuntimeError("File %s does not exist" % filepath)

    # prepare repo rates and client config
    repoRates = ClientRepoRatesReader(filepath)

    # book repos
    bsbBooker = PrimeServicesBsb(settleDate, repoRates)
    bsbBooker.bookPrimeServicesBsb()
