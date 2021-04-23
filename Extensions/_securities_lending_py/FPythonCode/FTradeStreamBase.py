""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FTradeStreamBase.py"
from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FTradeStreamBase

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    This module is used to build and improve streams from where trades will be parsed
    and imported into the system

------------------------------------------------------------------------------------------------"""
import traceback
import acm
import cStringIO
import contextlib
import csv
import functools

import FPortfolioRouter
import FSecLendRecordLookup
import FSecLendUtils
from FSecLendUtils import logger
import FSecLendDealUtils
import FSecLendReturns
import FSecLendHooks
from FParameterSettings import ParameterSettingsCreator

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')
MAXCHAR = _SETTINGS.MaxCharactersClipboardFile()
# ----------------------------------------------------------------------------------------------
# --------------------------Streams parsing API--------------------------------------
# ----------------------------------------------------------------------------------------------
class FullTextNotProcessedError(Exception):
    pass


class ParsingError(Exception):
    pass


class NoCounterpartyFoundError(Exception):
    pass


def UniqueName(name, cls):
    i = 0
    newName = name
    while cls[newName]:
        newName = name + "#" + str(i)
        i += 1
    return newName


def CreateTradeOriginInfoTextObject(text, reference):
    textObject = None
    if text and reference:
        name = UniqueName("Security Loan %s Import %s" % (reference, acm.Time.TimeNow()), acm.FCustomTextObject)
        textObject = acm.FCustomTextObject()
        textObject.Text(text)
        textObject.Name(name)
        textObject.Commit()
    return textObject


def Required(function):
    """
    Used in the stream buffer for clipboard and file
    this wrapper is used to indicate that this is a
    field lookup function and must be checked if exists or not since it is required.
    It may be added to any required field that will unvalidate the trade creation
    """

    @functools.wraps(function)
    def function_logger(cls, *args, **kwargs):
        result = function(cls, *args, **kwargs)
        if not result:
            cls._is_valid = False
            cls.invalid_string = '----{} not found-----,'.format(function.__name__) + cls.invalid_string
            print('Could not find {} in processed fields:{}'.format(function.__name__, cls._fields))
        return result

    return function_logger


class FStreamReader(object):
    """
    This class is a helper singleton class made of functions to parse files and clipboard
    to build the FStreamReader class, a stream TradeStream class should be used.
    In FParameters, define the FMultipleTradeStream class inheriting from FTradeStreamBase
    """
    #__metaclass__ = Singleton uncomment this if you need to cache  the lookups it in the session

    CLIPBOARD_CF_TEXT = 1
    FIELD_DELIMITERS = ',;\t|'
    FILE_TYPES = ("CSV Files (*.csv)|*.csv|"
                  "Text Files (*.txt)|*.txt|"
                  "All Files (*.*)|*.*")

    def __init__(self, _creator=_SETTINGS.TradeStreamImplementation()):
        self._creator = _creator if _creator else "FTradeStreamBase.FMultipleTradeStream"
        self._invalid_input = None
        inslookupids = list(FSecLendRecordLookup._SETTINGS.InstrumentLookUpIds())
        partylookupids = list(FSecLendRecordLookup._SETTINGS.PartyLookUpIds())
        self.instrumentLookup = FSecLendRecordLookup.FInstrumentLookup(inslookupids)
        self.partyLookup = FSecLendRecordLookup.FPartyLookup(partylookupids)

    def TradeStreamCreator(self, *args, **kwargs):
        moduleName, className = self._creator.split('.', 1)
        module = __import__(moduleName)
        return getattr(module, className)(*args, **kwargs)

    def getInvalidInput(self):
        return self._invalid_input.getvalue() if self._invalid_input.getvalue() != "" else None

    @staticmethod
    def Parser(stream):
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(stream.read(MAXCHAR), FStreamReader.FIELD_DELIMITERS)
            if dialect and stream.tell() >= MAXCHAR:
                raise FullTextNotProcessedError()
        except csv.Error:
            # Likely couldn't find a delimiter, which can happen for a single list.
            # Try to process the file anyway, treating each row as an instrument.
            dialect = 'excel'
        stream.seek(0)
        return list(csv.reader(stream, dialect))

    @staticmethod
    def BrowseToFile(shell):
        selection = acm.FFileSelection()
        selection.FileFilter = FStreamReader.FILE_TYPES
        if acm.UX().Dialogs().BrowseForFile(shell, selection):
            return str(selection.SelectedFile())

    @staticmethod
    def TextFromClipboard():
        with FStreamReader.ClipboardText() as stream:
            string = cStringIO.StringIO(stream).read(MAXCHAR) if stream else ""
            if string and MAXCHAR <= cStringIO.StringIO(stream).tell():
                raise FullTextNotProcessedError()
            return string

    @staticmethod
    def TextFromFile(shell):
        filename = FStreamReader.BrowseToFile(shell)
        if filename:
            with open(filename, 'rb') as stream:
                return filename, stream.read()
        return (None, None)

    @staticmethod
    @contextlib.contextmanager
    def ClipboardText():
        import ctypes
        user32 = ctypes.windll.user32
        user32.OpenClipboard(None)
        try:
            if user32.IsClipboardFormatAvailable(FStreamReader.CLIPBOARD_CF_TEXT):
                user32.GetClipboardData.restype = ctypes.c_char_p
                data = user32.GetClipboardData(FStreamReader.CLIPBOARD_CF_TEXT)
                yield ctypes.c_char_p(data).value
            else:
                yield ''
        finally:
            user32.CloseClipboard()

    def TradesFromString(self, text, **kwargs):
        try:
            parser = FStreamReader.Parser(cStringIO.StringIO(text))
            trades = []
            self._invalid_input = cStringIO.StringIO()
            for line in reversed(parser):
                ts = self.TradeStreamCreator(line, self.instrumentLookup, self.partyLookup, **kwargs)
                tsGet = ts.get()
                if ts.IsValid():
                    if isinstance(tsGet, list):
                        trades.extend(tsGet)
                    else:
                        trades.append(tsGet)
                else:
                    self._invalid_input.write('{}\n'.format(ts.getValidationMessage()))

            if trades:
                parsingErrors = self.getInvalidInput()
                info = FSecLendHooks.CreateTradeOriginInfo(text, parsingErrors, **kwargs)
                toInfo = CreateTradeOriginInfoTextObject(info, kwargs.get('Reference', ''))
                if toInfo:
                    for t in trades:
                        t.AddInfoValue('SBL_TradeOriginId', toInfo.Oid())

            return trades
        except csv.Error as e:
            raise ParsingError(e)
        return []


class FTradeStreamBase(object):
    """
    This class is a helper class for creating trades out of different streams (Clipboard, file, mail)
    THE INSTURMENT is the miniumum required parameter by default.
    """
    def __init__(self, line, inslookup, partylookup, **kwargs):
        self._is_valid = True
        self.invalid_string = ""
        self._enricher = kwargs
        self._line = line
        self._source = self._enricher.get("Source") if self._enricher.get("Source") else "Manual"
        self._fields = [f.strip() for f in self._line if f]
        self._trade = None
        self._counterparty = None
        self._price = None
        self._quantity = None
        self.instrumentLookup = inslookup
        self.partyLookup = partylookup
        self._initalizeTrade()

    def _initalizeTrade(self):
        """
        Only the instrument is required by default
        """
        if self._fields:
            instrument = self.Instrument()
            if instrument and self._is_valid:
                self.Trade = self.CreateTrade(instrument)
        else:
            logger.debug('Unsuccessfully parsed line:{}'.format(self._line))

    def IsValid(self):
        return self._is_valid and self._trade

    def Fields(self):
        return self._fields

    @property
    def Trade(self):
        return self._trade

    @Trade.setter
    def Trade(self, trade):
        self._trade = trade

    def setSource(self, source):
        self._source = source

    def CreateTrade(self, instrument):
        trade = acm.FTrade()
        trade.Instrument(instrument)
        return trade

    def getValidationMessage(self, **kwargs):
        return self.invalid_string + ','.join(self._line)

    @Required
    def Instrument(self):
        """
        Look for the instrument to be used first.
        Delete it from fields if found. This field is mandatory for the deal creation
        """
        for f in self._fields[:]:
            inputParams = [f for x in range(len(self.instrumentLookup.LookupIds()))]
            instruments = self.instrumentLookup(inputParams)
            if instruments:
                self._fields.remove(f)
                return instruments[0]
        return None

    def Quantity(self):
        """first found value as quantity. Mandatory"""
        self._quantity = 0
        for f in self._fields[:]:
            try:
                self._quantity = abs(int(f.replace(" ", "")))
            except ValueError:
                pass
            else:
                self._fields.remove(f)
                return self._quantity
        return self._quantity

    def Price(self):
        """the price or rate or fee..: second scraped value"""
        for f in self._fields[:]:
            try:
                self._price = float(f.replace(" ", "").replace(",", "."))
            except ValueError:
                pass
            else:
                self._fields.remove(f)
                return self._price
        return 0

    def CounterParty(self):
        """
        Look for counterparty either in clipboard input
        or in the enricher (order entry) if wasnt set
        """
        if not self._counterparty:
            for f in self._fields[:]:
                inputParams = [f for x in range(len(self.instrumentLookup.LookupIds()))]
                parties = self.partyLookup(inputParams)
                if parties:
                    self._fields.remove(f)
                    self._counterparty = parties[0]
            if not self._counterparty and self._enricher.get("Counterparty"):
                self._counterparty = self._enricher.get("Counterparty")
        return self._counterparty

    def Portfolio(self):
        """look if portfolio is set already by the API"""
        return self.Trade.Portfolio() is not None

    def SetParameters(self, trade):
        FSecLendUtils.SetSource(trade, self._source)
        FPortfolioRouter.SetPortfolio(trade)
        isvalid, trade_tooltip = FSecLendHooks.IsValidForProcessing(trade)
        FSecLendHooks.SetTradeTooltip(trade, trade_tooltip)

    def get(self):
        """
        This function is a template for parsing the clipboard entry
        It first tries to get the instrument then the quantity and after that the rate. Any found field will be
        deleted from the search
        fields: is the list of values in one line. each attribute will represent a parameter of the trade
        source: is set to Clipbard in case of such.
        fields delimiters allowed but not mixed: ',; \t|'
        This function gives 100% correct result if the line has input into this order:
        Instrument lookup id, Party lookup id, Quantity, rate
        :return: always super class get method.
        """
        self.SetParameters(self.Trade)
        return self.Trade


class FTradeStream(FTradeStreamBase):
    """
    @Ifexists usage: decorate any function that helps getting the requested parameter with this decorator
    in order to get a validation process executed at this point. The validation message will be
    shown in the Order Validation column tooltip. use get + name_of_the_attribute for naming convention
    example: getRate, getPortfolio..
    """

    def getSLAccount(self, party):
        """not mandatory"""
        sl_account = None
        if self._enricher.get("SL_Account"):
            sl_account = FSecLendHooks.FromShortNameToId(party, self._enricher.get("SL_Account"))
        else:
            choices = FSecLendHooks.GetAccountChoices(party)
            if choices:
                sl_account = FSecLendHooks.FromShortNameToId(party, choices[0])
        return sl_account

    def getOrderType(self):
        if self._quantity and self._price:
            return 'Firm'
        else:
            return 'Soft'

    def CreateTrade(self, instrument):
        """
        The logic for creating the deal.
        :return: return the trade deal after creating it
        """
        security = FSecLendDealUtils.SecurityLoanCreator. \
            CreateInstrument(underlying=instrument,
                             isRebate=self._enricher.get("isRebate"))
        self._quantity = self.Quantity()
        self._price = self.Price()
        return FSecLendDealUtils.SecurityLoanCreator.CreateTrade(security,
                                                                 quantity=-1 * self._quantity,
                                                                 source=self._source,
                                                                 orderType=self.getOrderType(),
                                                                 status=FSecLendHooks.OnHoldTradeStatus() if self._enricher.get(
                                                                     "isHold") \
                                                                     else FSecLendHooks.DefaultTradeStatus(),
                                                                 holdTime=True if self._enricher.get(
                                                                     "isHold") else False)

    def get(self):
        """
        This function is a template for parsing the clipboard entry
        It first tries to get the instrument then the quantity and after that the rate. Any found field will be
        deleted from the search
        fields: is the list of values in one line. each attribute will represent a parameter of the trade
        source: is set to Clipbard in case of such.
        fields delimiters allowed but not mixed: ',; \t|'
        This function gives 100% correct result if the line has input into this order:
        Instrument lookup id, Party lookup id, Quantity, rate
        :return: always super class get method.
        """
        try:
            cp = self.CounterParty()
            if cp:
                self.Trade.Counterparty(cp)
            if self.Trade.Counterparty():
                self.Trade.AddInfoValue("SL_Account", self.getSLAccount(self.Trade.Counterparty()))
            # fees
            if self._price is None:
                FSecLendUtils.SetDefaultRate(self.Trade)
            else:
                FSecLendUtils.SetSecurityLoanRate(self.Trade, self._price / 100)
            # CollateralAgreement
            if self._enricher.get("CollateralAgreement"):
                self.Trade.AddInfoValue("CollateralAgreement", self._enricher.get("CollateralAgreement"))
            if self._enricher.get("acquirer"):
                self.Trade.Acquirer(self._enricher.get("acquirer"))
        except Exception as e:
            logger.debug('Unsuccessfully parsed line:{}. Error:{}'.format(self._line, traceback.print_exc()))
            self._is_valid = False
            return None
        return super(FTradeStream, self).get()


class FMultipleTradeStream(FTradeStream):
    """
    Return logic: Can create several trade objects from one parsed line.
    """
    def __init__(self, line, inslookup, partylookup, **kwargs):
        self._trades = []
        super(FMultipleTradeStream, self).__init__(line, inslookup, partylookup, **kwargs)

    def _initalizeTrade(self):
        """
        Only the instrument is required for creating new loans.
        Counterparty and instrument are required for creating return trades.
        """
        if self._fields:
            instrument = self.Instrument()
            if instrument and self._is_valid:
                trades = self.CreateTrades(instrument)
                if not isinstance(trades, list):
                    self.Trade = trades
                else:
                    self.Trades = trades
        else:
            FSecLendUtils.logger.debug('Unsuccessfully parsed line:{}'.format(self._line))

    def CreateTrades(self, instrument):
        """
        The logic for creating the deal.
        """
        if self._enricher.get("isReturn"):
            return self.ReturnTrades(instrument, 'return')
        elif self._enricher.get("isRecall"):
            return self.ReturnTrades(instrument, 'recall')
        else:
            return self.CreateTrade(instrument)

    def ReturnTrades(self, instrument, returntype):
        """
        The logic for creating return trades.
        """
        if self.CounterParty():  # Select counterparty in order to create return trades
            query = FSecLendHooks.ActiveLoansQuery(self.CounterParty(), [instrument])
            query.AddAttrNode('Status', 'NOT_EQUAL', FSecLendHooks.DefaultTradeStatus())
            query.AddAttrNode('Status', 'NOT_EQUAL', FSecLendHooks.OnHoldTradeStatus())
            activeLoans = query.Select()
            if not activeLoans:
                self.invalid_string = '---- No loans found to return for ----'
                return []
            try:
                returnTrades = FSecLendReturns.CreateReturnTrades(activeLoans,
                                                                  quantity=self.Quantity(),
                                                                  clientReturns=True,
                                                                  returnPartial=False,
                                                                  returntype=returntype)
            except FSecLendReturns.NoQuantityFoundError:
                self.invalid_string = '---- Quantity to return must be a number ----'
            except FSecLendReturns.NoReturnLoansFoundError:
                self.invalid_string = '---- No loans found to return for ----'
            else:
                return returnTrades
        else:
            raise NoCounterpartyFoundError()

    def IsValid(self):
        return self._is_valid and (self.Trade or self.Trades)

    @property
    def Trades(self):
        return self._trades

    @Trades.setter
    def Trades(self, trades):
        self._trades = trades

    def get(self):
        if self.Trades:
            for t in self.Trades:
                if self._enricher.get("acquirer"):
                    t.Acquirer(self._enricher.get("acquirer"))
                self.SetParameters(t)
            return self.Trades
        elif self.Trade:
            return super(FMultipleTradeStream, self).get()
