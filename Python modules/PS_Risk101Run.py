'''-----------------------------------------------------------------------
MODULE
    PS_Risk101Run

DESCRIPTION
    Date                : 2011-07-05
    Purpose             : Risk101 Run File
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Paul Jacot-Guillarmod, Francois Truter, Herman Hoon
    CR Number           : 703542
    
HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-07-05 703542       Herman Hoon    Initial Implementation
2011-07-08 707977       Herman Hoon    Updated to send an email if the mappings does not exist
2011-07-12 710203       Herman Hoon    Updated the Instrument codes to map to YieldX and SAFEX codes
2011-07-15 713436       Herman Hoon    Updated mappings for Swaps and FRAs
2011-07-18 715943       Herman Hoon    Updated the logic for Cap, Floors, FRNs and absolute Considerations
2011-08-25 750738       Herman Hoon    Updated logic for Cap, Floors and CFDs
ENDDESCRIPTION
-----------------------------------------------------------------------'''
import acm
import os
import string
import PS_Risk101Interface
reload(PS_Risk101Interface)
import FRunScriptGUI

calendar = acm.FCalendar['ZAR Johannesburg']
INCEPTION = acm.Time().DateFromYMD(1970, 1, 1)
TODAY = acm.Time().DateToday()
FIRSTOFYEAR = acm.Time().FirstDayOfYear(TODAY)
FIRSTOFMONTH = acm.Time().FirstDayOfMonth(TODAY)
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
TWODAYSAGO = acm.Time().DateAddDelta(TODAY, 0, 0, -2)
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)
TWOBUSDAYSAGO = calendar.AdjustBankingDays(TODAY, -2)

# Generate date lists to be used as drop downs in the GUI.
startDateList   = {'Inception':INCEPTION,
                   'First Of Year':FIRSTOFYEAR,
                   'First Of Month':FIRSTOFMONTH,
                   'PrevBusDay':PREVBUSDAY,
                   'TwoBusinessDaysAgo':TWOBUSDAYSAGO,
                   'TwoDaysAgo':TWODAYSAGO,
                   'Yesterday':YESTERDAY,
                   'Custom Date':TODAY,
                   'Now':TODAY} 
startDateKeys = startDateList.keys()
startDateKeys.sort()

def enableCustomStartDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == 'Custom Date')
    return fieldValues


FILE_NAME = 'PS_Risk101_'
defaultTradeFilter = acm.FTradeSelection['PS_Risk101']
directorySelection = FRunScriptGUI.DirectorySelection()
directorySelection.SelectedDirectory('F:\Test')

ttMailList = 'Specify mail recipients that will recieve the email notification of instrument types that are not mapped.\n\
              Specify them in the form: user1@address.com, user2@address.com.'

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['date', 'Date', 'string', startDateKeys, 'Now', 1, 0, 'Date for witch the file should be selected.', enableCustomStartDate, 1],
                 ['dateCustom', 'Date Custom', 'string', None, TODAY, 0, 0, 'Custom date', None, 0],
                 ['tradefilter',  'Trade Filter', 'FTradeSelection', None, defaultTradeFilter, 1, 1, 'Trades that will be included in the risk101 report.', None, 1],
                 ['fileName', 'File name', 'string', None, FILE_NAME, 1, 0, 'File name prefix. Will be followed by the date specifieds', None, 1],
                 ['filePath', 'Directory', directorySelection, None, directorySelection, 1, 1, 'Folder where files will be placed.', None, 1],
                 ['mailList', 'MailList', 'string', None, None, 0, 0, ttMailList]
                ]

def ael_main(dictionary):
    if dictionary['date'] == 'Custom Date':
        date = dictionary['dateCustom']
    else:
        date = startDateList[dictionary['date']]
    
    if dictionary['date'] == 'Custom Date':
        date = dictionary['dateCustom']
    else:
        date = startDateList[dictionary['date']]

    filepath  = dictionary['filePath'].SelectedDirectory().Text()
    filename  = dictionary['fileName']
    filename  = ''.join([filename, date, '.csv'])
    directory = os.path.join(filepath, filename)
    mailList  = dictionary['mailList']
    
    trades = dictionary['tradefilter'][0]
    if trades:
        try:
            WriteTrades(trades.Trades(), directory, mailList)
            print 'Wrote secondary output to: %s' %(directory)
            print 'completed successfully' 
        except Exception, err:
            print 'ERROR: While writing file: %s' %(err)
    else:
        print 'No trades to export.'
    
    
def _lookupFXInstrumentCode(name):
    prefix = 'ZA'
    fx = {'AUD':'AD','CAD':'CA','CNY':'CY','EUR':'EU','GBP':'GB','JPY':'JY','USD':'US','UM':'UM','FR':'FR','RAIN':'RAIN'}
    value = ''
    if fx.has_key(name):
        value = prefix + fx[name]
    else:
        value = ''
    return value


def _lookupInstrumentCode(instrument):
    name = instrument.Name()
    instrumentType = instrument.InsType()
    underlying = instrument.Underlying()
    insCode = ''
    insType = None
    
    if underlying:
        namelist = underlying.Name().split('/')
        if len(namelist) > 1:
            if len(namelist[1].split('_')) > 1 and namelist[1].split('_')[1] == 'DivFut':
                #Dividend Futures' type should be overriden with Equity Future (E3)
                insType = 'E3'
                insCode = name.split('/')[1]
            else:
                insCode = namelist[1]
        else:
            if instrumentType == 'Future/Forward' and underlying.InsType() == 'Curr' and instrument.Currency().Name() == 'ZAR':
                namelist = name.split('/')
                if len(namelist) > 2:
                    if namelist[2] == 'YIELDX':
                        insCode = _lookupFXInstrumentCode(underlying.Name())
            else:
                insCode = namelist[0]
    else:
        namelist = name.split('/')
        if len(namelist) > 1:
            if instrumentType in ('FRN', 'Cap', 'Floor', 'CLN'):
                insCode = name
            elif instrumentType == 'Deposit':
                insCode = 'CASH'
            else:
                insCode = namelist[1]
        else:
            insCode = namelist[0]
        
    return insCode[:14], insType
    

def WriteTrades(trades, filepath, mailList):
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    
    msgBuffer = ''
    
    file = PS_Risk101Interface.InstrumentFile()
    for trade in trades:
        instrument = trade.Instrument()
        instrumentType = instrument.InsType()
        if trade.Status() not in ('Void', 'Simulated'):
            try:
                risk101InstrumentType, msg = PS_Risk101Interface.Risk101InstrumentTypes.TranslateFrontInstrument(instrument)
                if msg != None:
                    msgBuffer += ''.join(['For trade: ', str(trade.Oid()), ' ', msg, '\n'])
                    
                underlying = instrument.Underlying()
                record = file.CreateRecord(trade)
                record.START_TradeNumber.Value(trade.Oid())
                insCode, insType = _lookupInstrumentCode(instrument)
                
                if insType == None:
                    record.InstrumentType.Value(risk101InstrumentType) 
                else:
                    record.InstrumentType.Value(insType)
                record.InstrumentCode.Value(insCode)    
                
                if trade.Counterparty().Id2() in ('JSE', 'SAFEX', 'JSE SECURITIES EXCHANGE SOUTH AFRICA'):
                    record.CapacityType.Value('A')
                else:
                    record.CapacityType.Value('P')

                tradeTime = trade.TradeTime()
                record.DealTimeHour.Value(tradeTime, TIME_FORMAT)
                record.DealTimeMinute.Value(tradeTime, TIME_FORMAT)
                record.DealDateDay.Value(tradeTime, TIME_FORMAT)
                record.DealDateMonth.Value(tradeTime, TIME_FORMAT)
                record.DealDateYear.Value(tradeTime, TIME_FORMAT)
                
                acquireDay = trade.AcquireDay()
                record.SettlementDateDay.Value(acquireDay, DATE_FORMAT)
                record.SettlementDateMonth.Value(acquireDay, DATE_FORMAT)
                record.SettlementDateYear.Value(acquireDay, DATE_FORMAT)
                
                record.Nominal.Value(trade.QuantityOrNominalAmount())
                if underlying:
                    price = trade.Price() if (underlying.Quotation().Name() != 'Per 100 Units') else trade.Price() * 0.01
                else:
                    price = trade.Price() if (instrument.Quotation().Name() != 'Per 100 Units') else trade.Price() * 0.01
                
                record.Price.Value(abs(price))
                
                if instrument.Quotation().Name() == 'Yield':
                    record.Yield.Value(abs(price))
                
                if instrumentType == 'Swap':
                    fixedLeg = instrument.FirstFixedLeg()
                    if fixedLeg:
                        price = fixedLeg.FixedRate()
                        record.Price.Value(abs(price))
                        record.Yield.Value(abs(price))
                elif instrumentType == 'FRA':
                    leg = instrument.Legs()[0]
                    if leg:
                        price = leg.FixedRate()
                        if price:
                            record.Price.Value(abs(price))
                            record.Yield.Value(abs(price))  
                elif instrumentType == 'Option':
                    price = trade.Premium()
                    record.Price.Value(abs(price))
                    
                portfolio = trade.Portfolio()
                paymentCurrency = instrument.Currency()
                baseCurrency = portfolio.Currency()
                
                record.BuyOrSell.Value('S' if (trade.Quantity()) < 0 else 'B')
                #REMOVE SUBSTR
                record.Portfolio.Value(portfolio.Name()[:8])
                #REMOVE SUBSTR
                record.Counterparty.Value('TESTXXX' if trade.Counterparty().Name()[:8] == 'TEST' else trade.Counterparty().Name()[:8])
                record.PaymentCurrency.Value(paymentCurrency.Name())
                record.BaseCurrency.Value(baseCurrency.Name())
                
                if paymentCurrency != baseCurrency:
                    record.CrossRate.Value(paymentCurrency.Calculation().FXRate(CALC_SPACE, baseCurrency, tradeTime).Number())
                record.BookingCosts.Value(0)
                record.MarginTraded.Value(instrument.PayType() == 'Future')                
                
                if instrumentType == 'Future/Forward' or (instrumentType == 'Option' and instrument.PayType() == 'Future'):
                    expiryDate = instrument.ExpiryDate()
                    record.FuturesCloseOutDateDay.Value(expiryDate, TIME_FORMAT)
                    record.FuturesCloseOutDateMonth.Value(expiryDate, TIME_FORMAT)
                    record.FuturesCloseOutDateYear.Value(expiryDate, TIME_FORMAT)
                    
                    consideration = abs(price * trade.Nominal())
                    record.CleanConsideration.Value(consideration)
                    record.TotalConsideration.Value(consideration)
                    
                elif instrumentType == 'CFD':
                    consideration = abs(price * trade.Nominal())
                    record.CleanConsideration.Value(consideration)
                    record.TotalConsideration.Value(consideration)
                else:
                    consideration = abs(trade.Premium())
                    record.CleanConsideration.Value(consideration)
                    record.TotalConsideration.Value(consideration)
                
                if instrumentType == 'Option':
                    expiryDate = instrument.ExpiryDate()
                    record.StrikePrice.Value(instrument.StrikePrice() if (underlying.Quotation().Name() != 'Per 100 Units') else instrument.StrikePrice() * 0.01)
                    record.AmericanOrEuropean.Value(instrument.ExerciseType()[0])
                    record.PutOrCall.Value('C' if (instrument.OptionType()[0]) in ('R', 'C', 'L') else 'P')
                    record.OptionExpiryDateDay.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryDateMonth.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryDateYear.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryTimeHour.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryTimeMinute.Value(expiryDate, TIME_FORMAT)
                    record.SettlementTerms.Value(PS_Risk101Interface.Risk101SettlementTerms.TranslateFromSpotDays(instrument.SpotBankingDaysOffset()))
                    
                    consideration = abs(trade.Premium())
                    record.CleanConsideration.Value(consideration)
                    record.TotalConsideration.Value(consideration)
                    
                    if underlying.InsType() in ('Swap', 'FRA'):
                        record.Yield.Value(instrument.StrikePrice())
                        record.Nominal.Value(trade.Nominal())
                
                if instrumentType in ('Cap', 'Floor'):
                    record.StrikePrice.Value(instrument.StrikePrice())
                    record.AmericanOrEuropean.Value('E')
                    record.PutOrCall.Value('C' if (instrument.ExerciseEventType()[0]) in ('R', 'C', 'L') else 'P')
                    expiryDate = instrument.StartDate() + ' 00:00:00'
                    record.OptionExpiryDateDay.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryDateMonth.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryDateYear.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryTimeHour.Value(expiryDate, TIME_FORMAT)
                    record.OptionExpiryTimeMinute.Value(expiryDate, TIME_FORMAT)
                    
                if instrumentType in ('Swap', 'FRA', 'Cap', 'Floor', 'FRN') :
                    expiryDate = instrument.ExpiryDateOnly()
                    record.MaturityDateDay.Value(expiryDate, DATE_FORMAT)
                    record.MaturityDateMonth.Value(expiryDate, DATE_FORMAT)
                    record.MaturityDateYear.Value(expiryDate, DATE_FORMAT)
                
                if underlying and underlying.InsType() in ('Swap', 'FRA'):
                    expiryDate = underlying.ExpiryDateOnly()
                    record.MaturityDateDay.Value(expiryDate, DATE_FORMAT)
                    record.MaturityDateMonth.Value(expiryDate, DATE_FORMAT)
                    record.MaturityDateYear.Value(expiryDate, DATE_FORMAT)
                
            except Exception, ex:
                print 'ERROR: Error while loading trade %s: %s' %(trade.Oid(), ex)
    

    if msgBuffer != '' and mailList != '':
        subject = 'PS_Risk101 unmapped instrument types'
        header = 'No instrument type mapping exists from Front instument types to to Risk101 instrument types for the following trades: \
                 \nThese trades will be set to the default instrument type: EQUITY_SPOT (Code E1 in Risk101).\
                 \n\nNotify Risk101 that the instrument mapping for the following trades was set to instrument type E1 and not the actual instrument type.\
                 \n\nNotify Front Arena IT that the mappings needs to be updated in the PS_Risk101Interface script.\n\n'
        msg = header + msgBuffer
        sendMail(mailList, subject, msg)
                
    file.WriteFile(filepath)

def sendMail(TO, SUBJECT, MSG):
    import smtplib
    
    HOST = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(), 'mailServerAddress').Value()
    FROM = "PRIME client"
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "", MSG), "\r\n")
    if not HOST:
        print ('No mail server address specified!\n Please specify your mail server name or IP address '
                'in the extension attribute mailServerAddress!')
    try:
        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, TO.split(','), BODY)
        server.quit()
        print 'Mail sent to: %s' % TO
    except:
        print 'Failed sending mail.'
