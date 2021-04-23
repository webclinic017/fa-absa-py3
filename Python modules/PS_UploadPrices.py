"""----------------------------------------------------------------------------
MODULE
    PS_UploadPrices

DESCRIPTION
    Date                : 2011-07-01
    Purpose             : Uploads the SAFEX prices from a CSV file
                          for a specific portfolio.
                          This script is dependand on the SAPS_MoveTrades
                          script that creates the instruments
                          with the /MTM postfix.
    Department and Desk : Prime Services
    Requester           : Stephen Linell
    Developer           : Herman Hoon
    CR Number           : 699989

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------
2011-07-01  699989  Herman Hoon         Initial Implementation
2011-07-05  703542  Herman Hoon         Updated to set the values
                                        to the Theoretical price
                                        if no prices is availible
                                        from the file.
2011-07-07  706358  Herman Hoon         Add mapping for FX Futures
                                        and Options
2011-09-19  772824  Herman Hoon         Updated to exclude expired
                                        instruments and to ensure
                                        that the theoretical price
                                        will be uploaded correctly.
2012-01-12  869163  Herman Hoon         Updated to remove ambiguity
                                        with FX Options names
2012-01-19  869163  Herman Hoon         Updated to correct scaling
                                        for FX Futures
2012-02-24  62717   Herman Hoon         Updated to add AnyDay Futures
2012-04-05          Herman Hoon         Fixed mapping bug for AnyDay Futures
2012-04-24  154014  Peter Kutnik        Hotfix for AnyDay Options
2012-07-08  318884  Anwar Banoo         Removed dependancy on query folder
                                        to figure out where the /MTM
                                        instruments are - use
                                        an inline query instead
2012-07-26  353807  Nidheesh Sharma     Removed the mtm price from
                                        being multiplied by 10,000
                                        for FX candos
2012-08-07  381413  Nidheesh Sharma     Made the _getMTMInstruments query
                                        more efficient by ensuring
                                        that instruments are not expired
                                        and have MtmFromFeed set to true
2013-02-15  804059  Nidheesh Sharma     Changed the naming convention
                                        for AnyDay and Forex instruments
                                        and removed the 10,000 factor
                                        from fxOptions.AddRecord
2013-03-04  842516  Peter Basista       The function TranslateToFrontName
                                        now returns more names for AnyDay
                                        instruments, namely it also returns
                                        a name containing the zero-padded
                                        day number.
2013-03-07  none    Peter Basista       Added additional instrument name
                                        mapping for FX Futures.
2013-11-22  N/A     Peter Fabian        Added support for FX vs FX Futures
2014-08-26  2240390 Anwar Banoo         Added support for can do options on alsi
2014-11-20  2450799 Libor Svoboda       Updated logging and error reporting
2014-11-27  2475014 Libor Svoboda       Added support for can-do futures
2015-09-15  3105564 Ondrej Bahounek     Add Interest Rate Swap Future
2019-05-02          Tibor Reiss         Check isin first due to ITAC
ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import ael
import os
import csv
import FRunScriptGUI
import FBDPGui
import FBDPString
from SAGEN_Set_Additional_Info import set_AdditionalInfoValue_ACM
from at_ael_variables import AelVariableHandler
from at_logging import  getLogger, bp_start

LOGGER = getLogger()

logme = FBDPString.logme

CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
FILE_NAME = 'ClosingPrices_'
VALID_INSTYPES = (
    'Future/Forward',
    'Option',
)


def get_start_day_config():
    """Generate date options to be used as drop downs in the GUI."""
    return {
        'Inception': acm.Time.DateFromYMD(1970, 1, 1),
        'First Of Year': acm.Time.FirstDayOfYear(TODAY),
        'First Of Month': acm.Time.FirstDayOfMonth(TODAY),
        'PrevBusDay': CALENDAR.AdjustBankingDays(TODAY, -1),
        'TwoBusinessDaysAgo': CALENDAR.AdjustBankingDays(TODAY, -2),
        'TwoDaysAgo': acm.Time.DateAddDelta(TODAY, 0, 0, -2),
        'Yesterday': acm.Time.DateAddDelta(TODAY, 0, 0, -1),
        'Custom Date': TODAY,
        'Now': TODAY,
    }


def get_spot_sob_day_config():
    """Generate date options to be used as drop downs in the GUI."""
    return {
        'NextBusinessDay': CALENDAR.AdjustBankingDays(TODAY, 1),
        'Tomorrow': acm.Time.DateAddDelta(TODAY, 0, 0, 1),
        'Custom Date': CALENDAR.AdjustBankingDays(TODAY, 1),
        'Now': TODAY,
    }


def enable_custom_start_date(ael_var):
    for var in ael_variables:
        if var[0] == 'dateCustom':
            var.enabled = ael_var.value == 'Custom Date'


def enable_custom_spot_sob_date(ael_var):
    for var in ael_variables:
        if var[0] == 'spotSobDateCustom':
            var.enabled = (ael_var.value == 'Custom Date' and
                           ael_var.enabled)


def enable_spot_sob(ael_var):
    for var in ael_variables:
        if var[0] == 'spotSobDate':
            var.enabled = ael_var.value
            enable_custom_spot_sob_date(var)


def get_ael_variables():
    directory_selection = FRunScriptGUI.DirectorySelection()
    directory_selection.SelectedDirectory(
            'F:\\Book of Work\\2 Analysis\Futures Upload\\Test')
    variables = AelVariableHandler()
    variables.add('date',
        label='Date',
        collection=sorted(get_start_day_config().keys()),
        default='Now',
        alt='Date for witch the file should be selected.',
        hook=enable_custom_start_date
    )
    variables.add('dateCustom',
        label='Date Custom',
        default=TODAY, 
        mandatory=False,
        alt='Custom date',
        enabled=False
    )
    variables.add('fileName',
        label='File name',
        default=FILE_NAME,
        alt='File name prefix. Will be followed by the date specifieds')
    variables.add('filePath',
        label='Directory',
        cls=directory_selection,
        default=directory_selection,
        multiple=True,
        alt='Directory where files will be uploaded from. \n'
            'A date subfolder in the form yyyy-mm-dd will '
            'be automatically added.'
    )
    variables.add('skipInstruments',
        label='Skip Instruments',
        alt='Instruments that will not be considered for price upload',
        cls='FInstrument',
        multiple=True,
        mandatory=False
    )
    variables.add_bool('updateSpotSob',
        label='Update SPOT-SOB',
        default=False,
        hook=enable_spot_sob
    )
    variables.add('spotSobDate',
        label='SPOT-SOB Date',
        collection=sorted(get_spot_sob_day_config().keys()),
        default='Tomorrow',
        hook=enable_custom_spot_sob_date
    )
    variables.add('spotSobDateCustom',
        label='SPOT-SOB Date Custom',
        default=CALENDAR.AdjustBankingDays(TODAY, 1), 
        mandatory=False,
        enabled=False
    )
    variables.extend(FBDPGui.LogVariables())
    return variables

ael_variables = get_ael_variables()


def ael_main(dictionary):
    
    process_name = "ps_upload_prices"
    with bp_start(process_name):
        logme.setLogmeVar('PS_UploadPrices',
                          dictionary['Logmode'],
                          dictionary['LogToConsole'],
                          dictionary['LogToFile'],
                          dictionary['Logfile'],
                          dictionary['SendReportByMail'],
                          dictionary['MailList'],
                          dictionary['ReportMessageType'])
        
        if dictionary['date'] == 'Custom Date':
            date = dictionary['dateCustom']
        else:
            date = get_start_day_config()[dictionary['date']]
    
        filepath = dictionary['filePath'].SelectedDirectory().Text()
        filename = dictionary['fileName']
        nameDate = ael.date(date).to_string('%Y%m%d')
        filename = ''.join([filename, nameDate, '.csv'])
        
        directory = os.path.join(filepath, date, filename)
        
        spot_sob = dictionary['updateSpotSob']
        if dictionary['spotSobDate'] == 'Custom Date':
            spot_sob_date = dictionary['spotSobDateCustom']
        else:
            spot_sob_date = get_spot_sob_day_config()[dictionary['spotSobDate']]
        
        try:
            prices = _readPrices(directory, date)
        except Exception as e:
            LOGGER.exception('Failed to read prices from file: %s, no prices will be uploaded.', directory)
            logme('Failed to read prices from file: %s, '
                  'no prices will be uploaded. Error:  %s' 
                  % (directory, e), 'ERROR')
            
            LOGGER.info('FINISH')
            logme(None, 'FINISH')
            raise       
        
        for insname, price in prices.iteritems():
            LOGGER.info("%s %s", insname, price)
        
        instruments = _getMTMInstruments(VALID_INSTYPES, date)
        skip_instruments = dictionary['skipInstruments']
        for ins in skip_instruments:
            if ins in instruments:
                LOGGER.warning('Skipping price upload for %s', ins.Name())
                logme('Skipping price upload for %s' % ins.Name(), 'WARNING')
        
        instruments = list(set(instruments) - set(skip_instruments))
        _setMTMPrices(instruments, prices, date, directory, spot_sob, spot_sob_date)
        
        errorMsg = ''.join([msg[1] for msg in logme.LogBuffert if 'ERROR' in msg])
        if errorMsg:
            LOGGER.info('FINISH')
            logme(None, 'FINISH')
            raise UploadPricesError(errorMsg)
        
        LOGGER.info('Completed successfully')
        LOGGER.info('FINISH')
        logme(None, 'FINISH')

# This resolves ambiguity between Can-do options
# and options on can-do futures in front,
# and the ambiguity between can-do options and futures in the SAFEX feed.
# Declares a record without option strike and call/put a candidate record
# for all matching instruments, with option-on-future records
# overriding the candidates with a match
class CandoLookup():
    def __init__(self):
        self.candoCandidates = {}
        self.candoMatches = {}

    def AddRecord(self, shortName, expiryDate, callPut, strike,
            mtmPrice, delta):

        if callPut in (JSEInstrumentTypes.CALL, JSEInstrumentTypes.PUT):
        # options on futures - unambiguous, override potential can-do options
            if shortName[0] == 'C':  # FX candos
                name = (JSEInstrumentTypes.YIELDX_PREFIX + shortName + 
                    '/' + JSEInstrumentTypes._getExpiryString(expiryDate) + 
                    '/' + callPut + '/' + 
                    JSEInstrumentTypes._formatStrike(strike))
            else:
                name = (JSEInstrumentTypes.FUTURE_PREFIX + 
                    JSEInstrumentTypes._getEquityName(shortName) + 
                    JSEInstrumentTypes._getSSFTypeMarker(shortName) + 
                    JSEInstrumentTypes._getExpiryString(expiryDate) + '/' + 
                    callPut + '/' + JSEInstrumentTypes._formatStrike(strike))

            name = (JSEInstrumentTypes.NAME_PREFIX + name + 
                JSEInstrumentTypes.MTM_POSTFIX)

            if name in self.candoMatches:
                msg = ('Cando: Duplicate price entries for instrument %s '
                    'in file, selected the first price.' % name)
                LOGGER.info(msg)
                logme(msg)
            else:
                if name in self.candoCandidates:
                    LOGGER.info("Removed candidate: %s", name)
                    del self.candoCandidates[name]
                self.candoMatches[name] = [mtmPrice, delta]

        else:
        # can-do options and futures, the record may map to an instrument
        # that will turn out to be option on can-do future at this point
            
            if shortName[0] == 'C':
                nameBase = (JSEInstrumentTypes.NAME_PREFIX + 
                    JSEInstrumentTypes.YIELDX_PREFIX + shortName + 
                    JSEInstrumentTypes._getExpiryString(expiryDate))
            else:
                nameBase = (JSEInstrumentTypes.NAME_PREFIX + 
                    JSEInstrumentTypes.FUTURE_PREFIX + 
                    JSEInstrumentTypes._getEquityName(shortName) + 
                    JSEInstrumentTypes._getSSFTypeMarker(shortName) + 
                    JSEInstrumentTypes._getExpiryString(expiryDate))

            # can-do futures
            name = nameBase + JSEInstrumentTypes.MTM_POSTFIX
            if name in self.candoMatches:
                msg = ('Cando: Duplicate price entries for instrument %s '
                      'in file, selected the first price.' % name)
                LOGGER.info(msg)
                logme(msg)
            else:
                self.candoMatches[name] = [mtmPrice, delta]

            # options based on can-do futures
            matchingInsids = ael.asql(
                "select insid from Instrument where insid like '%s%%%s'" % 
                (nameBase, JSEInstrumentTypes.MTM_POSTFIX))[1][0]

            if matchingInsids is not None and len(matchingInsids) > 0:
            # we got matches, time to log candidates
            # for instruments that are options on futures,
            # these will be reset by the matching mechanism
            # for instruments that are can-do options and futures,
            # these will not be overwritten by the matching mechanism
                for insid in matchingInsids:
                    fullName = insid[0]
                    acmIns = acm.FInstrument[fullName]
                    if acmIns is not None and _IsCandoOption(acmIns):
                        LOGGER.info("Logging candidate: %s", fullName)
                        if fullName in self.candoMatches:
                            LOGGER.info("Can-do candidate previously matched, skipping: %s", fullName)
                        else:
                            if fullName in self.candoCandidates:
                                LOGGER.info("Can-do candidate conflict, loss of data likely: %s", fullName)
                            else:
                                LOGGER.info("Logged candidate: %s", fullName)
                                self.candoCandidates[fullName] = [mtmPrice,
                                    delta]
            else:
                LOGGER.info("No matching instruments for cando option like: %s", nameBase)

    def MatchRecords(self):
        self.candoCandidates.update(self.candoMatches)
        return self.candoCandidates

class FXOptionLookup():
    """
    FX Option's naming convention is different to the other Instrument types.
    The same option can have multiple Quantities associated with it.
    For example:
        ZAR-USD/C/7.50/111219/1000/MTM
        ZAR-USD/C/7.50/111219/3780/MTM
        ZAR-USD/C/7.50/111219/500/MTM
    """
    def __init__(self):
        self.fxCandidates = {}

    def AddRecord(self, shortName, expiryDate, callPut, strike, mtmPrice, delta):
        """Add a record to the Candidates list of FX Options
        """
        # Catering for old and new naming convention
        nameBaseOld = ('ZAR-' + 
            JSEInstrumentTypes._lookupFXInstrument(shortName) + 
            '/' + callPut + '/' + JSEInstrumentTypes._formatStrike(strike) + 
            JSEInstrumentTypes._getFXOExpiryDate(expiryDate))
        nameBaseNew = ('ZAR' + '/' + shortName + '/' + callPut + '/' + 
            JSEInstrumentTypes._formatStrike(strike) + 
            JSEInstrumentTypes._getFXOExpiryDate(expiryDate))
        matchingInsids = ael.asql(
            "select insid from Instrument where insid like '%s%%%s'" % 
            (nameBaseOld, JSEInstrumentTypes.MTM_POSTFIX))[1][0]
        matchingInsidsNew = (ael.asql(
            "select insid from Instrument where insid like '%s%%%s'" % 
            (nameBaseNew, JSEInstrumentTypes.MTM_POSTFIX))[1][0])
        if matchingInsidsNew:
            matchingInsids.append(matchingInsidsNew[0])

        # mtmPrice *=  10000

        if matchingInsids is not None and len(matchingInsids) > 0:
            for insid in matchingInsids:
                fullName = insid[0]
                acmIns = acm.FInstrument[fullName]
                if acmIns is not None:
                    if fullName in self.fxCandidates:
                        LOGGER.info("FX Option candidate already logged: %s", fullName)
                    else:
                        LOGGER.info("Logged FX Option candidate: %s", fullName)
                        self.fxCandidates[fullName] = [mtmPrice, delta]

    def MatchRecords(self):
        return self.fxCandidates


class JSEInstrumentTypes():
    NAME_PREFIX = 'ZAR/'
    FUTURE_PREFIX = 'FUT/'
    BOND_PREFIX = 'JFUTURE'
    BOND_OPTION_PREFIX = 'BD/'
    YIELDX_PREFIX = 'YIELDX/'
    SWAP_PREFIX = 'SFUT'

    SAFEX_POSTFIX = '/SAFEX'
    YIELDX_POSTFIX = '/YIELDX'
    MTM_POSTFIX = '/MTM'
    ANY_EXP_POSTFIX = '/AnyExp'
    ANY_EXP_OPT_POSTFIX = '/AE'

    SINGLE_STOCK_FUTURE = 'SSF'
    DIVIDEND_FUTURE = 'DIVF'
    BOND_FUTURE = 'FUT'
    INDEX_FUTURE = 'INDEX'
    INT_FUT = 'IDXFUT'
    INT_DIV = 'IDXDIV'
    FX_FUTURE = 'FOREX'
    GOVI_FUTURE = 'GOVI'
    COMMODITY_FUTURE = 'COMM'
    AGRI_FUTURE = 'AGRIF'
    CANDO_FUTURE = 'CANDO'
    ANYDAY = 'ANYDAY'
    
    FUT_SWAP = 'SWAP'
    INTEREST_RATE_SWAP = 'IRS/F-JI'

    CALL = 'C'
    PUT = 'P'

    @classmethod
    def TranslateToFrontName(cls, insTypeCode, shortName,
            expiryDate, callPut, strike):
        name = ''
        names = []

        # Options on Futures
        if callPut in (cls.CALL, cls.PUT):
            if insTypeCode == cls.SINGLE_STOCK_FUTURE:
                name = (cls.FUTURE_PREFIX + cls._getEquityName(shortName) + 
                    cls._getSSFTypeMarker(shortName) + cls._getExpiryString(
                        expiryDate) + '/' + callPut + '/' + cls._formatStrike(
                            strike))

            elif insTypeCode in (cls.INDEX_FUTURE, cls.INT_FUT, cls.INT_DIV):
                name = (cls.FUTURE_PREFIX + shortName + 
                    cls._getExpiryString(expiryDate) + '/' + callPut + '/' + 
                    cls._formatStrike(strike))

            elif insTypeCode == cls.BOND_FUTURE:
                name = (cls.BOND_OPTION_PREFIX + shortName + 
                    JSEInstrumentTypes._getFXOExpiryDate(expiryDate) + '/' +
                    callPut + '/' + cls._formatStrike(strike))

            elif insTypeCode == cls.GOVI_FUTURE:
                name = (cls.FUTURE_PREFIX + shortName + cls.YIELDX_POSTFIX + 
                    cls._getExpiryString(expiryDate) + '/' + callPut + '/' + 
                    cls._formatStrike(strike))

            elif insTypeCode in [cls.COMMODITY_FUTURE, cls.AGRI_FUTURE]:
                name = (cls.FUTURE_PREFIX + shortName + cls.SAFEX_POSTFIX + 
                    cls._getExpiryString(expiryDate) + '/' + callPut + '/' + 
                    cls._formatStrike(strike))
            
            elif insTypeCode == cls.ANYDAY:
                any_expiry_string = cls._getAnyExpiryString(expiryDate)
                zero_padded_any_expiry_string = \
                    cls._getZeroPaddedAnyExpiryString(expiryDate)
                name = (shortName + cls.YIELDX_POSTFIX + 
                    cls.ANY_EXP_OPT_POSTFIX + 
                    any_expiry_string + 
                    '/' + callPut + '/' + cls._formatStrike(strike))
                if any_expiry_string != zero_padded_any_expiry_string:
                    # Adding also zero-padded variation of the instrument name
                    names.append(cls.NAME_PREFIX + name + cls.MTM_POSTFIX)
                    name = (shortName + cls.YIELDX_POSTFIX + 
                        cls.ANY_EXP_OPT_POSTFIX + 
                        zero_padded_any_expiry_string + 
                        '/' + callPut + '/' + cls._formatStrike(strike))

                # Catering for old and new naming convention,
                # and storing old naming convention
                names.append(cls.NAME_PREFIX + name + cls.MTM_POSTFIX)
                name = (shortName + '/' + callPut + '/' + 
                    cls._formatStrike(strike) + 
                    JSEInstrumentTypes._getFXOExpiryDate(expiryDate))

        # Futures
        else:
            if insTypeCode == cls.SINGLE_STOCK_FUTURE:
                name = (cls._getEquityName(shortName) + cls._getSSFTypeMarker(
                    shortName) + cls._getExpiryString(expiryDate))

            elif insTypeCode in (cls.DIVIDEND_FUTURE, cls.INDEX_FUTURE, cls.INT_FUT, cls.INT_DIV):
                name = shortName + cls._getExpiryString(expiryDate)

            elif insTypeCode == cls.BOND_FUTURE:
                name = (cls.BOND_PREFIX + shortName + 
                    cls._getExpiryString(expiryDate))

            elif insTypeCode == cls.GOVI_FUTURE:
                name = (shortName + cls.YIELDX_POSTFIX + 
                    cls._getExpiryString(expiryDate))

            elif insTypeCode == cls.FX_FUTURE:
                cur1 = cls._lookupFXInstrument(shortName, 0, 2)
                alternate_shortName = cls._lookupFXInstrument(shortName)
                if shortName != alternate_shortName:
                    # Adding alternative FX future name
                    names.append(cur1 + "/" + alternate_shortName + 
                        cls.YIELDX_POSTFIX + cls._getExpiryString(expiryDate) + 
                        cls.MTM_POSTFIX)

                name = (shortName + cls.YIELDX_POSTFIX + 
                    cls._getExpiryString(expiryDate))

            elif insTypeCode in [cls.COMMODITY_FUTURE, cls.AGRI_FUTURE]:
                name = (shortName + cls.SAFEX_POSTFIX + 
                    cls._getExpiryString(expiryDate))
            
            elif insTypeCode == cls.ANYDAY:
                any_expiry_string = cls._getAnyExpiryString(expiryDate)
                zero_padded_any_expiry_string = \
                    cls._getZeroPaddedAnyExpiryString(expiryDate)
                name = (shortName + cls.YIELDX_POSTFIX + cls.ANY_EXP_POSTFIX + 
                    any_expiry_string)
                if any_expiry_string != zero_padded_any_expiry_string:
                    # Adding also zero-padded variation of the instrument name
                    names.append(cls.NAME_PREFIX + name + cls.MTM_POSTFIX)
                    name = (shortName + cls.YIELDX_POSTFIX + 
                        cls.ANY_EXP_POSTFIX + zero_padded_any_expiry_string)

            elif insTypeCode == cls.FUT_SWAP and shortName.startswith("IS"):
                # SFUT_IS10_ZAR/IRS/F-JI/YYMMDD/MTM
                name = cls.SWAP_PREFIX + "_" + shortName + "_" + cls.NAME_PREFIX
                name += cls.INTEREST_RATE_SWAP
                exp_date = cls._getFXOExpiryDate(expiryDate)
                name += exp_date + cls.MTM_POSTFIX
                names.append(name)
                name = None
                
        if name:
            name = cls.NAME_PREFIX + name + cls.MTM_POSTFIX
            names.append(name)
        return names

    @classmethod
    def _getEquityName(cls, name):
        return name[0:3]

    @classmethod
    def _getSSFTypeMarker(cls, name):
        """
        Get Single Stock Future type to be reflected in instrument name.

        'Q' denotes the most common type by far, therefore is not mentioned
        in instrument name (also for historical reasons).
        'S' is the cash settled version
        'N' is the nill-paid letter

        Example: BVTQ -  "BVT" is the stock identifier, "Q" is the type marker.

        """
        return '' if len(name) < 4 or name[3] == 'Q' else name[3]

    @classmethod
    def _getAnyExpiryString(cls, expiryDate):
        """get expiry string for AnyExp options
        """
        month = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
            7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
        y, m, d = acm.Time.DateToYMD(expiryDate)
        value = '/' + str(d) + month[m] + str(y)[2:4]
        return value

    @classmethod
    def _getZeroPaddedAnyExpiryString(cls, expiryDate):
        """
        Get expiry string for AnyExp options
        with the day number padded with zeros.

        """
        month = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
            7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
        y, m, d = acm.Time.DateToYMD(expiryDate)
        value = '/' + ('%02d' % d) + month[m] + str(y)[2:4]
        return value

    @classmethod
    def _getExpiryString(cls, expiryDate):
        month = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
            7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
        y, m, d = acm.Time.DateToYMD(expiryDate)
        value = '/' + month[m] + str(y)[2:4]
        return value

    @classmethod
    def _getFXOExpiryDate(cls, expiryDate):
        y, m, d = acm.Time.DateToYMD(expiryDate)
        value = '/' + str(y)[2:4] + str(m).zfill(2) + str(d).zfill(2)
        return value

    @classmethod
    def _formatStrike(cls, strike):
        return '%.2f' % (float(strike))

    @classmethod
    def _lookupFXInstrument(cls, name, start=2, end=4):
        lookup = name[start:end]
        fx = {'AD': 'AUD', 'CA': 'CAD', 'CY': 'CNY', 'EU': 'EUR', 'GB': 'GBP',
            'JY': 'JPY', 'US': 'USD', 'UM': 'UM', 'NZ': 'NZD', 'FR': 'FR',
            'RAIN': 'RAIN', 'ZA': 'ZAR', 'CR': 'CNY'}
        try:
            value = fx[lookup]
        except Exception, error:
            value = ''
        return value

def _readPrices(filepath, date):

    SOURCE = 0
    SHORT_NAME = 1
    INSTRUMENT_TYPE_CODE = 2
    INSTRUMENT_TYPE_NAME = 3
    ISIN = 4
    EXPIRY_DATE = 5
    CALL_PUT = 6
    STRIKE = 7
    DELTA = 8
    CLOSE_PRICE = 9
    MTM_PRICE = 10
    QOUTED = 11
    PRICING_TYPE = 12

    prices = {}
    candos = CandoLookup()
    fxOptions = FXOptionLookup()
    
    with open(filepath, 'r') as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            try:
                source = row[SOURCE]
                shortName = row[SHORT_NAME]
                insTypeCode = row[INSTRUMENT_TYPE_CODE]
                mtmPrice = row[MTM_PRICE]
                delta = row[DELTA]
                expiryDate = row[EXPIRY_DATE]
                callPut = row[CALL_PUT]
                strike = row[STRIKE]
                qoute = row[QOUTED]
                isin = row[ISIN]
    
                mtmPrice = float(mtmPrice)
                if isin:
                    prices[isin + "_MTM"] = [mtmPrice, delta]
                elif insTypeCode == JSEInstrumentTypes.CANDO_FUTURE:
                    candos.AddRecord(shortName, expiryDate, callPut,
                        strike, mtmPrice, delta)
                elif ((insTypeCode == JSEInstrumentTypes.FX_FUTURE) and
                        (callPut in (JSEInstrumentTypes.CALL,
                        JSEInstrumentTypes.PUT))):
                    fxOptions.AddRecord(shortName, expiryDate, callPut,
                        strike, mtmPrice, delta)
                else:
                    names = JSEInstrumentTypes.TranslateToFrontName(insTypeCode,
                        shortName, expiryDate, callPut, strike)
                    for name in names:
                        if name:
                            if not prices.has_key(name):
                                prices[name] = [mtmPrice, delta]
                            else:
                                LOGGER.info(('Duplicate price entries for instrument %s '
                                      'in file, selected the first price.'), name)
                                logme('Duplicate price entries for instrument %s '
                                      'in file, selected the first price.' % name)
            except Exception as e:
                LOGGER.exception('Failed to read prices for row %s', row)
                logme('Failed to read prices for row %s : %s' % (row, e), 'WARNING')

    candoPrices = candos.MatchRecords()
    prices.update(candoPrices)
    fxOptionsPrices = fxOptions.MatchRecords()
    prices.update(fxOptionsPrices)
    
    return prices

def _getMTMInstruments(instypes, date):
    query = acm.CreateFASQLQuery('FInstrument', 'AND')
    query.AddAttrNode('Name', 'RE_LIKE_NOCASE', '*/MTM')
    query.AddAttrNode('MtmFromFeed', 'EQUAL', 1)
    query.AddAttrNode('ExpiryDate', 'GREATER_EQUAL', date)
    if instypes:
        op = query.AddOpNode('OR')
        for type in instypes:
            op.AddAttrNode('InsType', 'EQUAL',
                acm.EnumFromString('InsType', type))
    ins = query.Select()
    return ins

def _IsCandoOption(instrument):
    if instrument.InsType() == 'Option':
        return instrument.add_info('Cando Option')
    else:
        return False

def _GetSpotPrice(instrument, date):
    """
    Return the Spot price for a given date.
    First check the latest prices and then historical prices.
    """
    marketName = 'SPOT'
    for price in instrument.Prices():
        if price.Market().Name() == marketName and price.Day() == date:
            return price

    for price in instrument.HistoricalPrices():
        if price.Market().Name() == marketName and price.Day() == date:
            return price

    return None

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber

def _setMTMPrices(instruments, prices, date, filename, 
                  spot_sob=False, spot_sob_date=''):
    """Set the MTM price of all instruments that have not expired yet.
    """

    for ins in instruments:
        if acm.Time.DateDifference(ins.ExpiryDateOnly(), date) >= 0:
            name = ins.Name()
            isin = ins.Isin()
            price = None
            delta = None
            if isin in prices:
                price, delta = prices[isin]
                price = _changePriceQuotation(ins, price, date)
            elif name in prices:
                price, delta = prices[name]
                price = _changePriceQuotation(ins, price, date)
            else:
                LOGGER.warning(('Failed to map to price from SAFEX upload file '
                                'for instrument %s on %s, setting to Theoretical price.' %
                                (name, date)))
                logme('Failed to map to price from SAFEX upload file '
                      'for instrument %s on %s, setting to Theoretical price.' %
                      (name, date), 'WARNING')
                try:
                    price = _getTheorPrice(ins)
                except RuntimeError:
                    LOGGER.warning('Failed to get Theoretical price for %s.',
                                   name)
                    logme('Failed to get Theoretical price for %s.' % name,
                          'WARNING')
                    price = None
            
            if price != None:
                _setInstrumentPrice(ins, price, date, 'SPOT')
                _setInstrumentPrice(ins, price, date, 'internal')
                if spot_sob and spot_sob_date:
                    _setInstrumentPrice(ins, price, spot_sob_date, 'SPOT_SOB')

            if delta != None and ins.InsType() == 'Option':
                _setInstrumentDelta(ins, delta, date)

class SheetCalcSpace(object):
    CALC_SPACE = acm.Calculations().CreateCalculationSpace(
        acm.GetDefaultContext(), 'FDealSheet')

    @classmethod
    def getValue(cls, obj, column_id):
        return  cls.CALC_SPACE.CreateCalculation(obj, column_id)

def _getTheorPrice(ins):
    theorPrice = SheetCalcSpace.getValue(ins, 'Price Theor')
    if theorPrice:
        if theorPrice.Value() == 0.0:
            return 0
        else:
            return theorPrice.Value().Number()
    else:
        return None

def _changePriceQuotation(ins, price, date):
    quotation = ins.Quotation().Name()
    if quotation == 'Per Contract' and ins.InsType() != 'Option':
        price = price * ins.ContractSize()
    elif ins.InsType() == 'Option' and '/YIELDX/AE/' in ins.Name():
        price /= ins.ContractSize()

    return price

def _setInstrumentDelta(ins, delta, date):
    try:
        set_AdditionalInfoValue_ACM(ins, 'PS_SAFEX_Delta', delta)
        LOGGER.info('Stored delta for instrument %s on %s', ins.Name(), date)
        logme('Stored delta for instrument %s on %s' % (ins.Name(), date))
    except Exception, err:
        LOGGER.exception('Failed to set delta from file for instrument %s on %s', ins.Name(), date)
        logme('Failed to set delta from file for instrument %s on %s: %s' % 
            (ins.Name(), date, err), 'ERROR')


def _setInstrumentPrice(ins, price, date, market):
    found = False
    if market in ['SPOT', 'SPOT_SOB']:
        for p in ins.Prices():
            update_spot = (market == 'SPOT' and p.Market().Name() == market and
                           date == TODAY and p.Day() <= date)
            update_spot_sob = (market == 'SPOT_SOB' and 
                               p.Market().Name() == market and p.Day() <= date)
            if update_spot or update_spot_sob:
                found = True
                clone = p.Clone()
                _setPriceFields(ins, clone, p, price, date, market)

    for p in ins.HistoricalPrices():
        if p.Market().Name() == market and p.Day() == date:
            found = True
            clone = p.Clone()
            _setPriceFields(ins, clone, p, price, date, market)

    if not found:
        p = acm.FPrice()
        clone = p.Clone()
        clone.Day(date)
        clone.Instrument(ins)
        clone.Market(acm.FParty[market])
        clone.Currency(ins.Currency())
        _setPriceFields(ins, clone, p, price, date, market)


def _setPriceFields(ins, p, orig, price, date, market):
    p.Day(date)
    p.Settle(price)
    if market in ('SPOT', 'SPOT_SOB'):
        p.Bid(price)
        p.Ask(price)
        p.Last(price)
    try:
        orig.Apply(p)
        orig.Touch()
        orig.Commit()
        LOGGER.info('%s %s price on %s was updated to %s', ins.Name(), market, date, price)
        logme('%s %s price on %s was updated to %s' % 
            (ins.Name(), market, date, price))
    except Exception, err:
        LOGGER.exception('%s %s price on %s not committed.', ins.Name(), market, date)
        logme('%s %s price on %s not committed: %s' % 
            (ins.Name(), market, date, err), 'ERROR')


class UploadPricesError(Exception):
    """Custom UploadPrices Exception."""
    pass

