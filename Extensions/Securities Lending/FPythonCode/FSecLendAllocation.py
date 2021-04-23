""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendAllocation.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FSecLendAllocation
    
    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    This class handles the sourcing/hedging of availabilities.

-----------------------------------------------------------------------------"""
import acm
import traceback
from collections import namedtuple

import FPortfolioRouter
import FSecLendUtils
import FSheetUtils
import FUxCore  # @UnresolvedImport pylint: disable=import-error
from ACMPyUtils import Transaction  # @UnresolvedImport pylint: disable=import-error
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FParameterSettings import ParameterSettingsCreator
from FSecLendDealUtils import SecurityLoanCreator
import FSecLendReturns
import FSecLendHooks
import FLogger

def GetLogger(name=''):
    aLogger = FLogger.FLogger.GetLogger(name)
    return aLogger

def SetLoggingLevel(aLogger, level):
    ''' Levels are 1-4 signifying
        1: Info: get warnings, errors and info
        2: Debug: get everything
        3: Warn: get warnings and errors
        4: Error: get only errors
    '''
    aLogger.Reinitialize(level=level)


LOGGER = GetLogger('SecLendAllocation')


AVAILABILITYCOLUMN = 'Fixed Portfolio Inventory Position' #This must be a vector column with time buckets

TradeAndQuantities = namedtuple('TradeAndQuantities', 'trade, quantityProRata, remainingQuantity')
CostAndQuantity = namedtuple('CostAndQuantity', 'item, cost, quantity')
CalculationParameters = namedtuple('CalculationParameters', 'columnId, calculationConf, projectionParts')

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendAllocationSettings')

HIERARCHYTABLE = _SETTINGS.CoverPortfolioMapping()
LIMIT_AVAILABILITY_COLUMN = _SETTINGS.LimitAvailabilityColumn() #Column to limit the amount that can be covered i.e. exposure. Must be a vector column with time buckets.

class CoverReturnMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, eii):
        super(self.__class__, self).__init__(frame=eii, view="SecLendPortfolioView")
        self.calcSpace = None
        self.underlyings = []
        self._warnings = set()

    def EnabledFunction(self):
        try:
            cells = self._frame.ActiveSheet().Selection().SelectedRowCells()
            return str(cells[0].CalculationSpecification().ColumnName()) == AVAILABILITYCOLUMN
        except (AttributeError, IndexError):
            return False

    def _EnsureOneColumnSelected(self):
        return len(set(cell.Column() for cell in self._frame.ActiveSheet().Selection().SelectedCells())) == 1

    def Invoke(self, _eii):
        try:
            assert self._EnsureOneColumnSelected(), 'Only select cells in one column' 
            if not self.calcSpace: 
                self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')
            trades = []
            # Removing simulation in case a previous process failed.
            self.calcSpace.RemoveGlobalSimulation('Simulated Trades Parameter')
            for cell in self._frame.ActiveSheet().Selection().SelectedRowCells():
                if self._UnderlyingFromRow(cell.RowObject()): #Excludes rows for which we cannot tell the underlying
                    trades.extend(self._CoverReturnFromCell(cell))
                    self.calcSpace.SimulateGlobalValue('Simulated Trades Parameter', trades)
            self._DisplayWarnings()
            self._CommitTrades(trades)
                
        except StandardError as e:
            print(traceback.format_exc())
            acm.UX.Dialogs().MessageBoxInformation(self._frame.Shell(), str(e)) 

    def _CommitTrades(self, trades):
        saveTrades = True
        if _SETTINGS.DisplayAllocationSuggestions():
            saveTrades = self.StartDialog(trades) == 1

        if saveTrades:
            with Transaction():
                for trade in trades:
                    trade.Instrument().Commit()
                    trade.Commit()
        else:
            for trade in trades:
                trade.Instrument().Undo()

        #Removing any simulation
        self.calcSpace.RemoveGlobalSimulation('Simulated Trades Parameter')        
    
    def _DateFromCell(self, cell):
        try:
            dateIndex = cell.ProjectionParts()[0].Coordinates()[0]
            timeBuckets = cell.Column().Creator().ConfiguredVector()
            valueday = timeBuckets[dateIndex].BucketDate()
        except (IndexError, AttributeError) as e:
            raise type(e)('Unable to extract a date from cell selection:\n{0}'.format(e.message))
        return valueday

    def _CalcParamsFromCell(self, cell):
        calcConf = cell.CalculationSpecification().Configuration()
        projectionParts = cell.ProjectionParts()
        if LIMIT_AVAILABILITY_COLUMN:
            columnId = LIMIT_AVAILABILITY_COLUMN #Change ColumnId por la columna a usar.
        else:
            columnId = cell.CalculationSpecification().ColumnName()
        return CalculationParameters(columnId, calcConf, projectionParts)
    
    def _CoverReturnFromCell(self, cell):
        row = cell.RowObject()
        ins = self._UnderlyingFromRow(row)
        underlying = ins.Underlying() or ins
        try:
            quantity = int(cell.Value())
        except TypeError as e:
            raise type(e)('Unable to get value from cell selection:\n{0}'.format(e.message))
        availabilityCalculationParams = self._CalcParamsFromCell(cell)
        costCalculationParams = CalculationParameters(_SETTINGS.CoverCostColumn(), None, None)  
        valueday = self._DateFromCell(cell)
         
        if quantity < 0:
            return self._CoverFromCell(underlying, self.calcSpace, quantity, valueday, costCalculationParams, availabilityCalculationParams)
        elif quantity > 0:
            return self._ReturnFromCell(row.Trades(), quantity, valueday)
        else:
            return []
    
    def _CoverFromCell(self, underlying, calcSpace, quantity, valueday, costCalculationParams, availabilityCalculationParams):
        if not underlying in self.underlyings:
                self.underlyings.append(underlying)
                _UpdateCalcSpace(underlying, calcSpace)
        else:
            calcSpace.Refresh() 
        # underlying: current instrument's underlying selected.
        # SuggestCover: will perform the calculation for this underlying only.
        coverAllocation = SuggestCover(underlying, quantity, costCalculationParams,
                                    availabilityCalculationParams, calcSpace)
        if not coverAllocation:
            self.underlyings.remove(underlying)
            self._warnings.add('No availability found for {0}'.format(underlying.Name()))
        return _CreateCoverTrades(coverAllocation, underlying, valueday)

    def _ReturnFromCell(self, trades, quantity, valueday):
        activeTrades = FSecLendReturns.ActiveTrades(trades, clientReturns=False)
        returnCandidates = FSecLendHooks.AllocateReturnByPrice(activeTrades, quantity, highCostFirst=True)
        if not returnCandidates:
            returnCandidates = AllocateReturnByPrice(activeTrades, quantity, highCostFirst=True)
        return FSecLendReturns.ReturningTrades(returnCandidates,
                                                  -quantity,
                                                  valueDay=valueday,
                                                  status=FSecLendHooks.DefaultTradeStatus(),
                                                  source='Manual')

    def _DisplayWarnings(self):
        if self._warnings:
            msg = '\n'.join(self._warnings)
            acm.UX.Dialogs().MessageBox(self._frame.Shell(), 'Warning', msg, 'OK', None, None, 'Button1', 'None')
        self._warnings = set()

    @staticmethod
    def _UnderlyingFromRow(row):
        underlying = row.SingleInstrumentOrSingleTrade()
        if not underlying and row.IsKindOf(acm.FDistributedRow):
            underlyings = set(ins.Underlying() for ins in row.Instruments())
            if len(underlyings) == 1:
                underlying = underlyings.pop()
        return underlying

    def StartDialog(self, trades):
        customDlg = TradeSheetDialog(trades, self.calcSpace)
        builder = customDlg.CreateLayout()
        return acm.UX().Dialogs().ShowCustomDialogModal(self._frame.Shell(), builder, customDlg )


# ---------------------------------- Cover/Return -------------------------------------

def CoverReturn(eii):
    return CoverReturnMenuItem(eii)

def ClipBoardFormat(trades):
    return FSecLendHooks.ClipBoardTextHookFromTrades(trades, event="Allocation")


# -------------------------------------- Cover -----------------------------------------


def SuggestCover(underlying, quantity, costCalc, availabilityCalc, calcSpace=None):
    assert quantity < 0, "Quantity to cover must be negative"
    availabilities = _Availabilities(underlying, costCalc, availabilityCalc, calcSpace)
    quantityToCover = abs(quantity)
    coverCandidates = FSecLendHooks.AllocateCoverByPrice(availabilities, quantityToCover, highCostFirst=False)
    if not coverCandidates:
        coverCandidates = AllocateCoverByPrice(availabilities, quantityToCover, highCostFirst=False)
    return coverCandidates

def _Availabilities(underlying, costCalc, availCalc, calcSpace=None):
    if not calcSpace: 
        calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        _UpdateCalcSpace(underlying, calcSpace)
    iterator = calcSpace.RowTreeIterator()
    iterator = iterator.Find(underlying)
    if not iterator:
        print('No availability found for {0}'.format(underlying.Name()))
        return []
    
    availabilities = []
    for row in _ChildrenTrees(iterator.Tree()): #For each depotName
        if row.Item().Grouping().GroupingValue():
            depotName = row.Item().Grouping().GroupingValue().Name()
            calculatedAvailability = 0
            try:
                calculatedAvailability = calcSpace.CalculateValue(row, availCalc.columnId, availCalc.calculationConf, False, availCalc.projectionParts)
            except: #'Index out of range error': The column might be zero, so the column vector is empty and has no dimension.
                LOGGER.debug('Index out of range error: The column might be zero, so the column vector is empty and has no dimension')           
                pass
            availability = int(calculatedAvailability or 0)
            if availability <= 0: #Availabilities must be positive
                continue
            
            cost = calcSpace.CalculateValue(row, costCalc.columnId)
            availabilities.append(CostAndQuantity(depotName, cost, availability))
    return availabilities
    
def _ChildrenTrees(tree):
    child = tree.Iterator().FirstChild()
    while child:
        yield child.Tree()
        child = child.NextSibling() 
    
def _UpdateCalcSpace(underlying, calcSpace):
    portfolio = _SETTINGS.AvailabilityPortfolio()
    assert portfolio, 'No portfolio for availability found'
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    nodePort = query.AddOpNode('OR')
    nodePort.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio)
    nodeUnd = query.AddOpNode('OR')
    nodeUnd.AddAttrNode('Instrument.Underlying.Oid', 'EQUAL', underlying.Oid())
    topNode = calcSpace.InsertItem(query)
    grouper = acm.FChainedGrouper([
            acm.Risk.GetGrouperFromName('Underlying'),
            acm.Risk.GetGrouperFromName('Counterparty')])
    topNode.ApplyGrouper(grouper)
    calcSpace.Refresh()
    return calcSpace
    
def _CreateCoverTrades(coverAllocation, underlying, valueDay):
    newTrades = []
    for party, quantity in coverAllocation.iteritems():
        instrument = SecurityLoanCreator.CreateInstrument(underlying=underlying, legStartDate=valueDay)
        collateralAgreements = FSecLendHooks.GetCollateralAgreementChoices(acm.FParty[party])
        collAgree = collateralAgreements[0] if collateralAgreements else None
        accounts = FSecLendHooks.GetAccountChoices(acm.FParty[party])
        account = accounts[0] if accounts else None
        trade = SecurityLoanCreator.CreateTrade(instrument,
                                                quantity=quantity,
                                                acquirer=FSecLendHooks.DefaultAcquirer(),
                                                counterparty=party,
                                                collateralAgreement=collAgree,
                                                slAccount=account,
                                                orderType='Firm')
        portfolio = FPortfolioRouter.GetPortfolio(trade, HIERARCHYTABLE)
        if not portfolio:
            print('Portfolio not set for all orders')
        trade.Portfolio(portfolio)
        FSecLendUtils.SetDefaultRate(trade)
        newTrades.append(trade)
    return newTrades


# ---------------------------------- Fair Allocation for Covers -------------------------------------  

# The position is covered from the internal depots with the lowest cost. In the case for which the 
# depots have equal cost the cover is fairly allocated (pro rata) over the internal depots.


def AllocateCoverByPrice(costAndQuantities, sourceAmount, highCostFirst=True):
    if not costAndQuantities:
        print('No loans to allocate.')
        return {}
    cptyPerPrice = FSecLendReturns.SortedByPrice(costAndQuantities)
    amountLeft = abs(sourceAmount)
    allocation = {}
    #Allocate pro rata between all positions at the same price
    for price in sorted(cptyPerPrice, reverse=highCostFirst):
        positionsAtPrice = cptyPerPrice[price]
        totalAvailableAtPrice = sum([pos.quantity for pos in positionsAtPrice])
        totalAvailableToAllocate = min(totalAvailableAtPrice, amountLeft)
        allocatedAmount = 0
        for pos in FSecLendReturns.HighestQuantityFirst(positionsAtPrice):
            ratioOfTotalAvailable = abs(float(pos.quantity) / totalAvailableAtPrice)
            lot = min (round(totalAvailableToAllocate * ratioOfTotalAvailable), amountLeft)
            if lot > 0: #Don't include zero quantities
                #Make sure we don't allocate to much because of rounding
                if allocatedAmount + lot > totalAvailableToAllocate:
                    lot -= (allocatedAmount + lot) - totalAvailableToAllocate
                allocation[pos.item] = lot
                allocatedAmount += lot

        #Distribute residuals
        if totalAvailableToAllocate > allocatedAmount:
            DistributeCoverResiduals(totalAvailableToAllocate, allocatedAmount, positionsAtPrice, allocation)
                
        amountLeft -= allocatedAmount
        if amountLeft == 0:
            break
    return allocation
    
def DistributeCoverResiduals(totalAvailableToAllocate, allocatedAmount, positionsAtPrice, allocation):
    residuals = int(totalAvailableToAllocate-allocatedAmount)
    for pos in FSecLendReturns.HighestQuantityFirst(positionsAtPrice)[:residuals]:
        allocation[pos.item] += 1
        allocatedAmount += 1


# ---------------------------------- Fair Allocation for Returns -------------------------------------  

# The loans with the highest cost are returned first. In the case for which the 
# depots have equal cost the return is fairly allocated (pro rata) over the internal depots. In the 
# case when there exists several loans with one depot, the loans with the highest quantities are 
# returned first, to reduce transactions costs.


def AllocateReturnByPrice(costAndQuantities, sourceAmount, highCostFirst=True):
    if not costAndQuantities:
        print('No loans to allocate.')
    tradesPerPrice = FSecLendReturns.SortedByPrice(costAndQuantities)
    amountLeft = abs(sourceAmount)
    allocation = {}
    #Allocate pro rata between all positions at the same price
    for price in sorted(tradesPerPrice, reverse=highCostFirst):
        positionsAtPrice = tradesPerPrice[price]
        totalAvailableAtPrice = sum([pos.quantity for pos in positionsAtPrice])
        totalAvailableToAllocate = min(totalAvailableAtPrice, amountLeft)
        allocatedAmount = 0
        for pos in sorted(positionsAtPrice, reverse=True, key=lambda x: x.quantity):
            ratioOfTotalAvailable = abs(float(pos.quantity) / totalAvailableAtPrice)
            lot = min (round(totalAvailableToAllocate * ratioOfTotalAvailable), amountLeft)
            if lot > 0: #Don't include zero quantities
                #Make sure we don't allocate to much because of rounding
                if allocatedAmount + lot > totalAvailableToAllocate:
                    lot -= (allocatedAmount + lot) - totalAvailableToAllocate
                #Add TradeAndQuantities in dictionary with counterparties as keys in order to reduce transactions
                if allocation.has_key(pos.item.Counterparty()):
                    allocation[pos.item.Counterparty()].append(TradeAndQuantities(pos.item, lot, pos.quantity))
                else:
                    allocation[pos.item.Counterparty()] = [TradeAndQuantities(pos.item, lot, pos.quantity)]
                allocatedAmount += lot

        if totalAvailableToAllocate > allocatedAmount:
            DistributeReturnResiduals(totalAvailableToAllocate, allocatedAmount, positionsAtPrice, allocation)

        amountLeft -= allocatedAmount
        if amountLeft == 0:
            break
    return ReduceTransactions(allocation)

def DistributeReturnResiduals(totalAvailableToAllocate, allocatedAmount, positionsAtPrice, allocation):
    residuals = int(totalAvailableToAllocate-allocatedAmount)
    for pos in FSecLendReturns.HighestQuantityFirst(positionsAtPrice)[:residuals]:
        for tradeAndQuantities in allocation[pos.item.Counterparty()]:
            if tradeAndQuantities.trade == pos.item:
                qty = tradeAndQuantities.quantityProRata
                allocation[pos.item.Counterparty()].remove(TradeAndQuantities(pos.item, qty, pos.quantity))
                allocation[pos.item.Counterparty()].append(TradeAndQuantities(pos.item, qty+1, pos.quantity))
        allocatedAmount += 1
    
def ReduceTransactions(allocation):
    loansToReturn = {}
    for positionPerCpty in allocation.values(): #Reduce transactions per counterparty
        loansToReturn.update({pos.trade: pos.quantityProRata for pos in positionPerCpty if \
        pos.remainingQuantity == pos.quantityProRata})
        #Reduce transactions for the loans that havn't been completely returned
        reduceTransactionTrades = [pos for pos in positionPerCpty if pos.remainingQuantity != pos.quantityProRata]
        totalQuantity = sum([pos.quantityProRata for pos in reduceTransactionTrades])
        for pos in sorted(reduceTransactionTrades, reverse=True, key=lambda x: x.remainingQuantity):
            #Return the loans with the highest quantities to reduce transactions
            if totalQuantity > pos.remainingQuantity:   
                loansToReturn[pos.trade] = pos.remainingQuantity
                totalQuantity -= pos.remainingQuantity
            else:
                loansToReturn[pos.trade] = totalQuantity
                break
    return loansToReturn


# ----------------------- Trade Sheet Dialog --------------------------  

class TradeSheetDialog (FUxCore.LayoutDialog):
    def __init__(self, trades, calcSpace):
        self.m_closeBtn = None
        self.m_sheet = None
        self.m_sheetCtrl = None
        self.m_fuxDlg = None
        self._trades = trades
        self._calcSpace = calcSpace

    def HandleApply(self):
        return 1
    
    def HandleCancel(self):
        #Removing simulation
        self._calcSpace.RemoveGlobalSimulation('Simulated Trades Parameter')
        return True
    
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Suggested Cover/Return')
        self.m_sheetCtrl = layout.GetControl('sheet')
        
        #In this case GetCustomControl returns a FUxWorkbookSheet
        self.m_sheet = self.m_sheetCtrl.GetCustomControl()
        
        self.m_sheet.ColumnCreators().Clear()
        columns = ['Underlying Instrument', 'Trade Quantity', 'Security Loan Orders Rate', 'Trade Counterparty', 'Trade Portfolio', 'Security Loan Type', 'Trade Value Day', 'Collateral Agreement', 'Security Loan SL Account']
        for columnId in columns:
            FSheetUtils.AddColumn(self.m_sheet, columnId)

        self.m_sheet.InsertObject(self._trades, 'IOAP_LAST')
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddCustom('sheet', 'sheet.FTradeSheet', 780, 200)
        b.  BeginHorzBox('None')
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
