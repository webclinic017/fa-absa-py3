""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/CreateDefaultPackages.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    CreateDefaultPackages

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import ConvertiblePackageHooks as hooks
import ConvertiblePackageUtils as utils
from FAssetManagementUtils import logger
from FAscotUtils import SwapFromConvertibleCreator
from FAscotValuationFunctions import SetRecallSwap


def CreateDefaultCASPackage(convertibleBond, dealPackage):
    cb = convertibleBond.Original()
    if cb is None:
        cb = convertibleBond
    irs = _CreateCASRecallSwap(cb, dealPackage)
    ascot = _CreateCASAscot(cb, dealPackage)

    if cb.Quotation().Name() in ['Per Contract', 'Per Contract Clean']:
        price = cb.ContractSize()
    else:
        price = 100

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentAndUpdateTrade(cb, dealPackage, 'cb', price, True)
        _ReplaceInstrumentAndUpdateTrade(irs, dealPackage, 'irs', 0.0)
        _ReplaceInstrumentAndUpdateTrade(ascot, dealPackage, 'ascot', 0.0)
    else:
        _CreateTrade(cb, dealPackage, 'cb', price, True)
        _CreateTrade(irs, dealPackage, 'irs', 0.0)
        _CreateTrade(ascot, dealPackage, 'ascot', 0.0)
    
    irs = dealPackage.InstrumentAt('irs')
    ascot = dealPackage.InstrumentAt('ascot')
    _LinkAscotAndIRSViaExotics(ascot, irs)

def CreateDefaultCBTradePackage(convertibleBond, dealPackage):
    cb = convertibleBond.Original()
    if cb is None:
        cb = convertibleBond

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentAndUpdateTrade(cb, dealPackage, 'cb', utils.GetMarketPrice(cb))
    else:
        _CreateTrade(cb, dealPackage, 'cb', utils.GetMarketPrice(cb))

def CreateDefaultInstrumentOnSwapPackage(instrument, dealPackage):
    ins = instrument.Original()
    if ins is None:
        ins  = instrument
    stock = utils.GetUnderlyingStock(ins)

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentAndUpdateTrade(ins, dealPackage, 'ins', utils.GetMarketPrice(ins))
        _ReplaceInstrumentAndUpdateTrade(stock, dealPackage, 'stock', utils.GetMarketPrice(stock), True)
    else:
        _CreateTrade(ins, dealPackage, 'ins', utils.GetMarketPrice(ins))
        _CreateTrade(stock, dealPackage, 'stock', utils.GetMarketPrice(stock), True)

def CreateDefaultASCOTPackage(convertibleBond, dealPackage):
    cb = convertibleBond.Original()
    if cb is None:
        cb = convertibleBond
    ascot = _CreateAscot(cb, dealPackage)
    irs = _CreateRecallSwap(cb, dealPackage)
    _LinkAscotAndIRSViaExotics(ascot, irs)

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentOnly(dealPackage, 'irs', irs)
        _ReplaceInstrumentAndUpdateTrade(ascot, dealPackage, 'ascot', 0.0)
    else:
        _AddInstrumentToDealPackage(dealPackage, 'irs', irs)
        _CreateTrade(ascot, dealPackage, 'ascot', 0.0)

def CreateDefaultASCOTOnSwapPackage(convertibleBond, dealPackage):
    cb = convertibleBond.Original()
    if cb is None:
        cb = convertibleBond
    ascot = _CreateAscot(cb, dealPackage)
    irs = _CreateRecallSwap(cb, dealPackage)
    _LinkAscotAndIRSViaExotics(ascot, irs)
    stock = cb.Underlying()

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentOnly(dealPackage, 'irs', irs)
        _ReplaceInstrumentAndUpdateTrade(ascot, dealPackage, 'ascot', 0.0)
        _ReplaceInstrumentAndUpdateTrade(stock, dealPackage, 'stock', utils.GetMarketPrice(stock), True)
    else:
        _AddInstrumentToDealPackage(dealPackage, 'irs', irs)
        _CreateTrade(ascot, dealPackage, 'ascot', 0.0)
        _CreateTrade(stock, dealPackage, 'stock', utils.GetMarketPrice(stock), True)

def CreateDefaultASCOTTradePackage(ASCOT, dealPackage):
    ascot = ASCOT.Original()
    if ascot is None:
        ascot = ASCOT
    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentAndUpdateTrade(ascot, dealPackage, 'ascot', 0.0)
    else:
        _CreateTrade(ascot, dealPackage, 'ascot', 0.0)

def CreateDefaultCBOptionPackage(convertibleBond, dealPackage):
    cb = convertibleBond.Original()
    if cb is None:
        cb = convertibleBond
    irs = _CreateRecallSwap(cb, dealPackage)
    ascot = _CreateAscot(cb, dealPackage)
    _LinkAscotAndIRSViaExotics(ascot, irs)

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentOnly(dealPackage, 'irs', irs)
        _ReplaceInstrumentAndUpdateTrade(cb, dealPackage, 'cb')
        _ReplaceInstrumentAndUpdateTrade(ascot, dealPackage, 'ascot')
    else:
        _AddInstrumentToDealPackage(dealPackage, 'irs', irs)
        _CreateTrade(cb, dealPackage, 'cb')
        _CreateTrade(ascot, dealPackage, 'ascot')

def CreateDefaultCBOriginalOptionPackage(ASCOT, dealPackage):
    ascot = ASCOT.Original()
    if ascot is None:
        ascot = ASCOT
    exotics = ascot.Exotics()
    if exotics.IsEmpty():
        logger.warn('Ascot %s has no IRS linked to it through the exotic table. Make sure that outdated Ascots have been successfully upgraded.' % ascot.Name())
    cb = ascot.Underlying()

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentAndUpdateTrade(cb, dealPackage, 'cb')
        _ReplaceInstrumentAndUpdateTrade(ascot, dealPackage, 'ascot')
    else:
        _CreateTrade(cb, dealPackage, 'cb')
        _CreateTrade(ascot, dealPackage, 'ascot')

def CreateDefaultEquityDerivativeOnSwapPackage(ins, dealPackage):
    stock = ins.Original()
    if stock is None:
        stock = ins
    option = _CreateOption(stock, dealPackage)

    if dealPackage.Trades().Size() > 0:
        _ReplaceInstrumentAndUpdateTrade(stock, dealPackage, 'stock')
        _ReplaceInstrumentAndUpdateTrade(option, dealPackage, 'option')
    else:
        _CreateTrade(stock, dealPackage, 'stock')
        _CreateTrade(option, dealPackage, 'option')

def _CreateCASAscot(underlying, dealPackage):
    maturityDate = utils.GetCBNextPutDate2BD(underlying)
    if maturityDate < acm.Time.DateNow():
        maturityDate = utils.GetCBMaturityDate2BD(underlying)
    return _CreateOption(underlying, dealPackage, maturityDate, 6)

def _CreateAscot(underlying, dealPackage):
    maturityDate = utils.GetCBNextPutDate(underlying)
    if maturityDate < acm.Time.DateNow():
        maturityDate = underlying.EndDate()
    return _CreateOption(underlying, dealPackage, maturityDate, 7)

def _CreateCASRecallSwap(convertibleBond, dealPackage):
    maturityDate = utils.GetCBNextPutDate2BD(convertibleBond)
    if maturityDate < acm.Time.DateNow():
        maturityDate = utils.GetCBMaturityDate2BD(convertibleBond)
    return _CreateIRS(convertibleBond, dealPackage, maturityDate, 6)

def _CreateRecallSwap(convertibleBond, dealPackage):
    maturityDate = utils.GetCBNextPutDate(convertibleBond)
    if maturityDate < acm.Time.DateNow():
        maturityDate = convertibleBond.EndDate()
    return _CreateIRS(convertibleBond, dealPackage, maturityDate, 7)

def _CreateIRS(convertibleBond, dealPackage, maturityDate=None, spotBankingDays=None):
    irs = SwapFromConvertibleCreator(convertibleBond).CreateSwap(maturityDate, spotBankingDays)
    try:
        hooks.CustomDefaultInstrumentProperties(irs, dealPackage.DefinitionName())
    except StandardError as err:
        logger.error('Failed to invoke "ConvertiblePackageHooks.CustomDefaultInstrumentProperties" hook: %s', err)
    return irs

def _CreateOption(underlying, dealPackage, maturityDate=None, payDayOffset=None):

    def SuggestId(underlyingName):
        try:
            from FMonisUploadUtils import InstrumentNameTools
        except ImportError:
            return ''
        return InstrumentNameTools.CreateUniqueNameForAssetSwap(underlyingName)

    option = acm.DealCapturing().CreateNewInstrument('Option')
    isAscot = False
    if underlying.InsType() == 'Convertible':
        isAscot = True
    option.Underlying = underlying
    option.Currency = underlying.Currency()
    option.StrikeCurrency = underlying.Currency()
    option.IsCallOption = True
    option.ExerciseType = 'American'
    option.SettlementType = 'Physical Delivery'
    if not payDayOffset is None:
        option.PayDayOffset = payDayOffset
    if maturityDate:
        option.ExpiryDate = maturityDate
    if isAscot:
        if underlying.Quotation().Name() in ['Per Contract', 'Per Contract Clean']:
            option.Quotation = acm.FQuotation['Per Contract']
            option.ContractSize = 1.0
        else:
            option.Quotation = acm.FQuotation['Per 100 Units']
            option.ContractSize = underlying.ContractSize()
        optionName = SuggestId(underlying.Name())
    else:
        option.Quotation = underlying.Quotation()
        option.ContractSize = underlying.ContractSize()
        optionName = option.SuggestName()
    option.Name = optionName
    try:
        hooks.CustomDefaultInstrumentProperties(option, dealPackage.DefinitionName())
    except StandardError as err:
        logger.error('Failed to invoke "ConvertiblePackageHooks.CustomDefaultInstrumentProperties" hook: %s', err)
    return option

def _AddInstrumentToDealPackage(dealPackage, key, instrument):
    if not key in dealPackage.InstrumentKeys():
        dealPackage.AddInstrument(instrument, key)

def _ReplaceInstrumentOnly(dealPackage, key, newInstrument):
    dealPackageInstrumentLink = dealPackage.InstrumentLinkAt(key)
    dealPackageInstrumentLink.Instrument(newInstrument)

def _ReplaceInstrumentAndUpdateTrade(instrument, dealPackage, key, price = 0, isSell=False):
    dealPackage.ReplaceInstrumentAt(key, instrument)
    trade = dealPackage.TradeAt(key)
    _UpdateTrade(dealPackage, trade, price, isSell)

def _CreateTrade(instrument, dealPackage, key, price = 0, isSell=False):
    trade = acm.DealCapturing().CreateNewTrade(instrument)
    _UpdateTrade(dealPackage, trade, price, isSell)
    dealPackage.AddTrade(trade, key)

def _UpdateTrade(dealPackage, trade, price = 0, isSell=False):
    trade.TradeTime = acm.Time().TimeNow()
    trade.Price = price
    trade.Currency = trade.Instrument().Currency()
    # Set trade quantity to MinimumIncremental to avoid warning at startup
    minimumIncremental = trade.Instrument().MinimumIncremental()
    if minimumIncremental:
        trade.Nominal = minimumIncremental
    else:
        trade.Quantity = 1.0
    if isSell:
        trade.Quantity = -trade.Quantity()
    try:
        hooks.CustomDefaultTradeProperties(trade, dealPackage.DefinitionName())
    except StandardError as err:
        logger.error('Failed to invoke "ConvertiblePackageHooks.CustomDefaultTradeProperties" hook: %s', err)

def _LinkAscotAndIRSViaExotics(ascot, irs):
    SetRecallSwap(ascot, irs)