
import acm, SAGEN_IT_Functions, ael, string
from zak_funcs               import formnum
from ISDA_MATRIX import *

################################Variables################################
VALID_INSTYPE_QF = 'Conf_Valid_InsType'

VALID_OPTION_UNDERL_TYPE = ['FRA', 'Swap']

VALID_TRADE_QF = 'Conf_Valid_Trade'

NO_AFFIRMATION_QF = 'SAOps_No_Affirmation'

ALL_LIVE_TRADES_TF = 'SAOps_IRD_Trades'

AFFIRMATION_ALREADY_SENT_STATUS = ['Affirmation not Sent', 'Affirmation Sent', 'Affirmed', 'Disputed', 'Email Missing']

calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
#########################################################################

'''Function to check if there is an Email address on the contact of the CP
and that it has a corresponding rule based on the VALID_ACQUIRER and VALID_INSTYPE.'''
def checkEmailFunc(trade):
    checkEmail = 'no_email'
    if trade.Counterparty():
        for contact in trade.Counterparty().Contacts():
            for contactRule in contact.ContactRules():
                if contactRule.EventChlItem() and contactRule.EventChlItem().Name() == 'New Trade':
                    if contactRule.Acquirer() and acm.FStoredASQLQuery[VALID_TRADE_QF].Query().IsSatisfiedBy(trade) and trade.Acquirer().Name() == contactRule.Acquirer().Name():
                        if contactRule.InsType() and acm.FStoredASQLQuery[VALID_INSTYPE_QF].Query().IsSatisfiedBy(trade) and trade.Instrument().InsType() == contactRule.InsType():
                            if contact.Email():
                                return contact.Email()
    return checkEmail

#Function to check if there is any trade override to the affirmation flag.
def traderOverride(trade, noAffirmation, affirmation_status):
    trade.Text1('Cache Issue')
    trade.Unsimulate()
    acm.PollDbEvents()
    checkEmail = checkEmailFunc(trade)
    affirmationChoiceList = acm.FChoiceList.Select("list = 'Affirmation'")
    if noAffirmation:
        if affirmation_status == 'Yes': #Trader override Affirmation flag.
            if checkEmail != 'no_email':
                #msg = build_message(trade)                
                ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Affirmation Sent')
                SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trade, 'Affirmation', ACMCL)
                sendMail(trade, checkEmail)                                          #Connected to SMTP
            else:
                ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Email Missing')
                SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trade, 'Affirmation', ACMCL)
        else:
            ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Affirmation not Sent')
            SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trade, 'Affirmation', ACMCL)
    else:
        if affirmation_status in ('', 'Yes'):
            if checkEmail != 'no_email':
                #msg = build_message(trade)
                ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Affirmation Sent')
                SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trade, 'Affirmation', ACMCL)
                sendMail(trade, checkEmail)                                          #Connected to SMTP
            else:
                ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Email Missing')
                SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trade, 'Affirmation', ACMCL)
        else:
            ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Affirmation not Sent')
            SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trade, 'Affirmation', ACMCL)

#Function to send the email.
def sendMail(trade, toEmail):
    import smtplib
    from MimeWriter import MimeWriter
    try:
      from cStringIO import StringIO
    except ImportError:
      from StringIO import StringIO
    from email.Utils import COMMASPACE

    send_to = []

    send_to.append('xraAbcapOpsConfirmat@barclayscapital.com') #Uncomment for prod
    send_to.append(toEmail) #Uncomment for prod
    
    #send_to.append('xraxraAbcapOpsConfTe@barclayscapital.com')
    #send_to.append('willie.vanderbank@absacapital.com')
    #send_to.append('tshepo.mabena@absacapital.com')
    #send_to.append('miguel.daSilva@absacapital.com')
    
    send_from = 'xraAbcapOpsConfirmat@barclayscapital.com'
    
    tempfile = StringIO()
    mw = MimeWriter(tempfile)
    mw.addheader('to', COMMASPACE.join(send_to))
    mw.addheader('from', send_from)
    subj = 'Affirmation of deal: ' + str(trade.Oid())
    mw.addheader('subject', subj)
    body = mw.startbody('text/plain')
    body.write(build_message(trade))
    
    message = tempfile.getvalue()

    #smtp = smtplib.SMTP('SMTPMAIL.BARCAPINT.COM') #User connection - Need access to use
    #smtp = smtplib.SMTP('10.14.24.40') #User connection - Need access to use
    smtp = smtplib.SMTP('smtphost.bzwint.com')  #Backend connection
    smtp.sendmail(send_from, send_to, message)
    smtp.quit()
    print 'Email Sent'
    
def build_message(trade):
    ins = trade.Instrument()
    ins_type = ins.InsType()
    
    #Body
    if ins_type == 'Swap':
        type = 'Swap'
        if Is_PRIME_Linked(trade):
            type = 'Prime Swap'
        msg = 'Good day \n' + '\nPlease affirm the ' + type + ' trade below and forward us with your reference.\n \n'
        msg = SwapMsg(trade, ins, msg)
    elif ins_type == 'IndexLinkedSwap':
        msg = 'Good day \n' + '\nPlease affirm the Index Linked Swap trade below and forward us with your reference.\n \n'
        msg = CPISwapMsg(trade, ins, msg)
    elif ins_type == 'FRA':
        msg = 'Good day \n' + '\nPlease affirm the ' + ins_type + ' trade below and forward us with your reference.\n \n'
        msg = FRAMsg(trade, ins, msg)
    elif ins_type in ('Cap', 'Floor'):
        msg = 'Good day \n' + '\nPlease affirm the ' + ins_type + ' trade below and forward us with your reference.\n \n'
        msg = CapFloorMsg(trade, ins, msg)
    elif ins_type == 'CurrSwap':
        MTM = 'false'
        for l in ins.Legs():
            if l.NominalScaling() != 'None':
                MTM = 'true'
        if MTM == 'true':
            type = 'MTM Currency Swap'
        else:
            type = 'Currency Swap'
        msg = 'Good day \n' + '\nPlease affirm the ' + type + ' trade below and forward us with your reference.\n \n'
        msg = CurrSwapMsg(trade, ins, msg)
    elif ins_type == 'Option':
        if ins.UnderlyingType() == 'Swap':
            msg = 'Good day \n' + '\nPlease affirm the Swaption trade below and forward us with your reference.\n \n'
            msg = SwaptionMsg(trade, ins, msg)
        elif ins.UnderlyingType() == 'FRA':
            if ins.IsCallOption():
                msg = 'Good day \n' + '\nPlease affirm the Caplet trade below and forward us with your reference.\n \n'
            else:
                msg = 'Good day \n' + '\nPlease affirm the Floorlet trade below and forward us with your reference.\n \n'
            msg = CapletFloorletMsg(trade, ins, msg)
    
    #Footer
    msg = msg + '\n'+ 'Our reference              : '+(str)(trade.Oid()) 
    return msg

def lowestCF(leg):
    lowestCF = []
    for c in leg.CashFlows():
        if c.CashFlowType() not in ('Fixed Amount', 'Return'):
            lowestCF.append((c.StartDate(), c))

    lowestCF.sort()
    return lowestCF[0][1]
    
'''Listener function that decides if an Affirmation needs to be send or not.
If needed to be sent it will sent the Affirmation only if there is an Email
address'''
def affirmation(trade):
    #Send an Affirmation email if trade moves from FO to BO Confirmed or if the trade gets inserted as BO Confirmed.
    TODAY = ael.date_today()
    EXPDAY = TODAY.add_banking_day(ael.Instrument['ZAR'], -2)
    if ael.date_from_time(trade.ExecutionTime()) >= EXPDAY:
        if trade.Status() == 'BO Confirmed':
            ins = trade.Instrument()
            if acm.FStoredASQLQuery[VALID_INSTYPE_QF].Query().IsSatisfiedBy(trade):
                if (trade.Instrument().InsType() == 'Option' and VALID_OPTION_UNDERL_TYPE.__contains__(trade.Instrument().UnderlyingType())) or (trade.Instrument().InsType() != 'Option'):
                    noAffirmation = acm.FStoredASQLQuery[NO_AFFIRMATION_QF].Query().IsSatisfiedBy(trade)
                    affirmation_status = trade.add_info('Affirmation')
                    if not AFFIRMATION_ALREADY_SENT_STATUS.__contains__(affirmation_status):
                        traderOverride(trade, noAffirmation, affirmation_status)

#Function for sending Affirmations without the listener
def send_Affirmation(trd,*rest):
    affirmationChoiceList = acm.FChoiceList.Select("list = 'Affirmation'")
    trd = acm.FTrade[trd.trdnbr]
    checkEmail = checkEmailFunc(trd)
    if checkEmail != 'no_email':
        msg = build_message(trd)
        sendMail(trd, checkEmail)
        ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Affirmation Sent')
        SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trd, 'Affirmation', ACMCL)
    else:
        ACMCL = SAGEN_IT_Functions.get_ChoiceList_ACM(affirmationChoiceList, 'Email Missing')
        SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(trd, 'Affirmation', ACMCL)

    return 'Affirmation completed'

#Function to resend Affirmations
def resend_Affirmation():
    TODAY = ael.date_today()
    EXPDAY = TODAY.add_banking_day(ael.Instrument['ZAR'], -2)
    IRD_TRADES = acm.FTradeSelection[ALL_LIVE_TRADES_TF]
    i = 1
    for t in IRD_TRADES.Trades():
        if ael.date_from_time(t.ExecutionTime()) >= EXPDAY:
            if t.Status() in ('BO Confirmed'):
                if t.add_info('Affirmation'):
                    if t.add_info('Affirmation') in ('Affirmation Sent', 'Email Missing'):
                        confs = acm.FConfirmation.Select('trade=%i' %t.Oid())
                        if confs:
                            for c in confs:
                                if c.EventChlItem().Name() == 'New Trade':
                                    if c.Status() not in ('Matched', 'Matching Failed'):
                                        send_Affirmation(ael.Trade[t.Oid()])
                                        print 'Affirmation for trade :' + str(t.Oid()) + ' was re-send.'
                                        break
  
def __Get_Calendar(leg):
    calendars = acm.FArray()
    if leg.PayCalendar():
        calendars.Add(leg.PayCalendar())
    if leg.Pay2Calendar():
        calendars.Add(leg.Pay2Calendar())
    if leg.Pay3Calendar():
        calendars.Add(leg.Pay3Calendar())
    if leg.Pay4Calendar():
        calendars.Add(leg.Pay4Calendar())
    if leg.Pay5Calendar():
        calendars.Add(leg.Pay5Calendar())
    
    return calendars
    
def Get_Calendar(leg):
    calendars = __Get_Calendar(leg)
    #if Is_LIBOR_Linked(leg):
    #    calendars = Add_GBP_London(calendars)
    return calendars
    
def Get_Reset_Calendar(leg):
    if leg.Instrument().InsType() == 'IndexLinkedSwap' and leg.IndexRef() and leg.IndexRef().Name() == 'SACPI':
        return Get_Calendar(leg)
        
    calendars = acm.FArray()
    if leg.ResetCalendar():
        calendars.Add(leg.ResetCalendar())
    if leg.Reset2Calendar():
        calendars.Add(leg.Reset2Calendar())
    if leg.Reset3Calendar():
        calendars.Add(leg.Reset3Calendar())
    if leg.Reset4Calendar():
        calendars.Add(leg.Reset4Calendar())
    if leg.Reset5Calendar():
        calendars.Add(leg.Reset5Calendar())
    
    #if Is_LIBOR_Linked(leg):
    #    calendars = Add_GBP_London(calendars)
    return calendars
    
def Get_Frequency_Period(leg):
    if leg.RollingPeriodCount() == 0:
        return 'T'
    return leg.RollingPeriodUnit()[0]

def Get_Frequency_Period_Multiplier(leg):
    multiplier = leg.RollingPeriodCount()
    if multiplier == 0:
        return 1
    return multiplier
   
def earliestCF(ins):
    lowestCF = []
    for leg in ins.Legs():
        for c in leg.CashFlows():
            if c.CashFlowType() not in ('Fixed Amount', 'Return'):
                lowestCF.append(c.PayDate())

    lowestCF.sort()
    return lowestCF[0]    
    
def NotBlank(text, field):
    if field:
        return text + str(field) + '\n'
    else:
        return ''
        
def Is_PRIME_Linked(trade):
    for l in trade.Instrument().Legs():
        if l.FloatRateReference():
            if 'PRIME' in l.FloatRateReference().Name():
                return True
    return False
    
########## Message Tamplates ########## 
def SwapMsg(trade, ins, msg):
    msg = msg + 'Start Date                 : ' + str(ins.StartDate()) + '\n'
    msg = msg + 'Trade Date                 : ' + trade.TradeTime()[:10] + '\n'
    msg = msg + 'End/Expiry Date            : ' + str(ins.ExpiryDate())[:10] + '\n'
    msg = msg + 'Commencement Payment Date  : ' + earliestCF(ins) + '\n'
    msg = msg + 'Currency                   : ' + ins.Currency().Name() + '\n' + '\n'
    
    pay_type = ''
    receive_type = ''
    LegsType = []
    legslist = []       #This is for sorting purposes i.e. to first read the pay leg.
    legslist.append('')
    legslist.append('')
    
    for l in ins.Legs():
        LegsType.append(l.LegType())
        if l.PayLeg():
            legslist[0] = l
        else:
            legslist[1] = l
        
    for l in legslist:
        legType = l.LegType()
        swap = 0
        if l.AmortType() != 'None':
            swap = 1
            
        if swap:
            lowCF = lowestCF(l)
            startNominal = trade.Quantity() * lowCF.Calculation().Nominal(calcSpace, trade).Value().Number()
            msg = msg + 'Start Notional Amount      : ' + formnum(abs(startNominal)) + '\n'
        else:
            msg = msg + 'Notional Amount            : ' + formnum(abs(trade.Nominal())) + '\n'

        if 'Fixed' in LegsType:
            legnbr = ' '
        else:
            if l.PayLeg():
                legnbr = '1'
            else:
                legnbr = '2'
                
        if legType == 'Fixed':
            rate = 'Fixed Rate                 : ' + str(l.FixedRate()) + '\n'
        elif legType == 'Float':
            rate = 'Floating Index ' + legnbr + '           : ' + str(l.FloatRateReference().FreeText()) + '\n'
            rate = rate + 'Reset Frequency            : ' + str(l.RollingPeriod()) + '\n'
        if l.Spread() <> 0:
            rate = rate + 'Spread                     : ' + str(l.Spread()) + '\n'
        msg = msg + rate
              
        calendars = Get_Calendar(l)
        uniquecalenders = ''
        for c in calendars:
            if str(c.Name()) not in uniquecalenders:
                uniquecalenders = uniquecalenders + 'Payment Calendar           : ' + str(c.Name()) + '\n' 
        msg = msg + uniquecalenders + '\n'
        
        if l.PayLeg():
            pay_type = l.LegType()
            pay_freq = str(Get_Frequency_Period_Multiplier(l)) + Get_Frequency_Period(l)
        else:
            receive_type = l.LegType()
            receive_freq = str(Get_Frequency_Period_Multiplier(l)) + Get_Frequency_Period(l)
    
    msg = msg + 'Period End                 : ' + str(l.EndDate()) + '\n'

    if 'Fixed' in LegsType:
        if (trade.Nominal()) < 0:
            msg = msg + pay_type + ' Rate Payer           : ' + str(trade.Counterparty().Name()) + '\n'
            msg = msg + receive_type + ' Rate Payer           : ABSA Capital \n'
        else:
            msg = msg + pay_type + ' Rate Payer           : ABSA Capital \n'
            msg = msg + receive_type + ' Rate Payer           : ' + str(trade.Counterparty().Name()) + '\n'
            
        msg = msg + pay_type + ' Payment Frequency    : ' + pay_freq + '\n'
        msg = msg + receive_type + ' Payment Frequency    : ' +  receive_freq + '\n'
        
    else:
        if (trade.Nominal()) < 0:
            msg = msg + pay_type + ' Rate Payer 1         : ' + str(trade.Counterparty().Name()) + '\n'
            msg = msg + receive_type + ' Rate Payer 2         : ABSA Capital \n'
        else:
            msg = msg + pay_type + ' Rate Payer 1         : ABSA Capital \n'
            msg = msg + receive_type + ' Rate Payer 2         : ' + str(trade.Counterparty().Name()) + '\n'
            
        msg = msg + pay_type + ' Pay Frequency 1      : ' + pay_freq + '\n'
        msg = msg + receive_type + ' Pay Frequency 2      : ' +  receive_freq + '\n'

    return msg
  

def CapFloorMsg(trd, ins, msg):
    msg = msg + 'Start Date                 : ' + str(ins.StartDate()) + '\n'
    msg = msg + 'Trade Date                 : ' + trd.TradeTime()[:10] + '\n'
    msg = msg + 'End/Expiry Date            : ' + str(ins.ExpiryDate())[:10] + '\n'
    msg = msg + 'Commencement Payment Date  : ' + earliestCF(ins) + '\n'
    msg = msg + 'Currency                   : ' + ins.Currency().Name() + '\n' + '\n'

    msg = msg + 'Notional Amount            : ' + formnum(abs(trd.Nominal())) + '\n'
    pay_type = ''
    receive_type = ''
    
    if (trd.Nominal()) > 0:
        msg = msg + 'Buy/Sell                   : Buy' + '\n'
    else:
        msg = msg + 'Buy/Sell                   : Sell' + '\n'

    for l in ins.Legs():
        if l.Spread() <> 0:
            msg = msg + 'Spread                     : ' + str(l.Spread()) + '\n'
        msg = msg + 'Strike Price               : ' + str(l.Strike()) + '\n'
        msg = msg + 'Underlying Index           : ' + str(l.FloatRateReference().FreeText()) + '\n'
        msg = msg + 'Underlying Index Frequency : ' + str(l.RollingPeriod()) + '\n'

        calendars = Get_Calendar(l)
        uniquecalenders = ''
        for c in calendars:
            if str(c.Name()) not in uniquecalenders:
                uniquecalenders = uniquecalenders + 'Payment Calendar           : ' + str(c.Name()) + '\n'
        msg = msg + uniquecalenders

        if l.PayLeg():
            pay_type = l.LegType()
        else:
            receive_type = l.LegType()
            
    if trd.Premium() < 0:
        msg = msg + 'Premium Payer              : ABSA Capital \n'
    else:
        msg = msg + 'Premium Payer              : ' + str(trd.Counterparty().Name()) + '\n'
        
    msg = msg + 'Premium Amount             : ' + formnum(abs(round(trd.Premium(), 2))) + '\n'
    msg = msg + 'Premium Currency           : ' + str(trd.Currency().Name()) + '\n'
    msg = msg + 'Settlement Date            : ' + str(trd.ValueDay()) +'\n'

    if (trd.Nominal()) > 0:
        msg = msg + string.ljust(receive_type + ' Rate Payer', 27) + ': ABSA Capital \n'
        msg = msg + string.ljust(receive_type + ' Rate Receiver', 27) +  ': ' + str(trd.Counterparty().Name()) + '\n'
    else:
        msg = msg + string.ljust(receive_type + ' Rate Payer', 27) + ': ' + str(trd.Counterparty().Name()) + '\n'
        msg = msg + string.ljust(receive_type + ' Rate Receiver', 27) + ': ABSA Capital \n'

    return msg

    
def CurrSwapMsg(trd, ins, msg):
    LegCurrency1 = ''
    LegCurrency2 = ''
    pay_type = ''
    receive_type = ''
    LegsType = []
    legslist = []       #This is for sorting purposes i.e. to first read the pay leg.
    legslist.append('')
    legslist.append('')

    msg = msg + 'Trade Date                 : ' + trd.TradeTime()[:10] + '\n'
    msg = msg + 'Start Date                 : ' + str(ins.StartDate()) + '\n'
    msg = msg + 'End/Expiry Date            : ' + str(ins.ExpiryDate())[:10] + '\n'
    msg = msg + 'Commencement Payment Date  : ' + earliestCF(ins) + '\n'
    msg = msg + '\n'

    for l in ins.Legs():
        LegsType.append(l.LegType())
        if l.PayLeg():
            legslist[0] = l
        else:
            legslist[1] = l
        
    for l in legslist:
        legType = l.LegType()
        lowCF = lowestCF(l)
        
        if 'Fixed' in LegsType:
            legnbr = ' '
        else:
            if l.PayLeg():
                legnbr = '1'
            else:
                legnbr = '2'
                
        if l.IsFixedLeg():
            rate = 'Fixed Rate                 : ' + str(l.FixedRate()) + '\n'
            nominal = 'Notional Amount            : ' + formnum(abs(round(lowCF.Calculation().Nominal(calcSpace, trd).Value().Number(), 2))) + '\n'
            currency = 'Currency                   : ' + str(l.Currency().Name()) + '\n'
        
        elif l.IsFloatLeg():
            rate = 'Floating Index ' + legnbr + '           : ' + str(l.FloatRateReference().FreeText()) + '\n'
            rate = rate + 'Reset Frequency            : ' + str(l.RollingPeriod()) + '\n'
            nominal = 'Notional Amount            : ' + formnum(abs(round(lowCF.Calculation().Nominal(calcSpace, trd).Value().Number(), 2))) + '\n'
            currency = 'Currency                   : ' + str(l.Currency().Name()) + '\n'

        if l.PayLeg():
            LegCurrency2 = l.Currency().Name()
        if not l.PayLeg():
            LegCurrency1 = l.Currency().Name()
            FXrate1 = 1/l.NominalFactor()
            FXrate2 = l.NominalFactor()
        
        msg = msg + rate + nominal + currency

        if l.Spread() <> 0:
            msg = msg + 'Currency Spread            : ' + str(l.Spread()) + '\n'
        msg = msg + 'Initial Floating Rate      : ' + str(round(l.InitialIndexValue(), 4)) + '\n'

        calendars = Get_Calendar(l)
        uniquecalenders = ''
        for c in calendars:
            if str(c.Name()) not in uniquecalenders:
                uniquecalenders = uniquecalenders + 'Payment Calendar           : ' + str(c.Name()) + '\n'
        msg = msg + uniquecalenders
        
        calendars = Get_Reset_Calendar(l)
        uniquecalenders = ''
        for c in calendars:
            if str(c.Name()) not in uniquecalenders:
                uniquecalenders = uniquecalenders + 'Reset Calendar             : ' + str(c.Name()) + '\n'
        msg = msg + uniquecalenders + '\n'
        
        if l.PayLeg():
            pay_type = l.LegType()
        else:
            receive_type = l.LegType()

    msg = msg + 'Current Rate             \n'
    msg = msg + str(LegCurrency2) + '/' + str(LegCurrency1) +'                    : ' + str(FXrate2) + '\n'
    msg = msg + str(LegCurrency1) + '/' + str(LegCurrency2) +'                    : ' + str(FXrate1) + '\n'

    msg = msg + 'Period End                 : ' + str(l.RollingPeriodBase()) + '\n'

    if 'Fixed' in LegsType:
        if (trd.Nominal()) < 0:
            msg = msg + pay_type + ' Rate Payer           : ' + str(trd.Counterparty().Name()) + '\n'
            msg = msg + receive_type + ' Rate Payer           : ABSA Capital \n'
        else:
            msg = msg + pay_type + ' Rate Payer           : ABSA Capital \n'
            msg = msg + receive_type + ' Rate Payer           : ' + str(trd.Counterparty().Name()) + '\n'
    else:    
        if trd.Nominal() < 1:
            msg = msg + 'Float Rate Payer 1         : ' + str(trd.Counterparty().Name()) + '\n'
            msg = msg + 'Float Rate Payer 2         : ABSA Capital \n'
        else:
            msg = msg + 'Float Rate Payer 1         : ABSA Capital \n'
            msg = msg + 'Float Rate Payer 2         : ' + str(trd.Counterparty().Name()) + '\n'
        
    return msg


def FRAMsg(trd, ins, msg):
    pay_type = ''
    receive_type = ''

    msg = msg + 'Trade Date                 : ' + trd.TradeTime()[:10] + '\n'
    msg = msg + 'Start Date                 : ' + str(ins.StartDate()) + '\n'
    msg = msg + 'End/Expiry Date            : ' + str(ins.ExpiryDate())[:10] + '\n'
    msg = msg + 'Currency                   : ' + ins.Currency().Name() + '\n' + '\n'
    
    msg = msg + 'Notional Amount            : ' + formnum(abs(trd.Nominal())) + '\n'

    if (trd.Nominal()) > 0:
        msg = msg + 'Buy/Sell                   : Buy' + '\n'
    else:
        msg = msg + 'Buy/Sell                   : Sell' + '\n'
    for l in ins.Legs():

        msg = msg + 'Fixed Rate                 : ' + str(l.FixedRate()) + '\n'
        msg = msg + 'Floating Index             : ' + str(l.FloatRateReference().FreeText()) + '\n'
        msg = msg + 'Floating Index Frequency   : ' + str(l.RollingPeriod()) + '\n'
        if l.Spread() <> 0:
            msg = msg + 'Spread                     : ' + str(l.Spread()) + '\n'

        calendars = Get_Calendar(l)
        uniquecalenders = ''
        for c in calendars:
            if str(c.Name()) not in uniquecalenders:
                uniquecalenders = uniquecalenders + 'Payment Calendar           : ' + str(c.Name()) + '\n'
        msg = msg + uniquecalenders
                
        if l.PayLeg():
            pay_type = l.LegType()
        else:
            receive_type = l.LegType()

    if (trd.Nominal()) > 0:
        msg = msg + 'Fixed Rate Payer           : ABSA Capital \n'
        msg = msg + 'Float Rate Payer           : ' + str(trd.Counterparty().Name()) + '\n'
    else:
        msg = msg + 'Fixed Rate Payer           : ' + str(trd.Counterparty().Name()) + '\n'
        msg = msg + 'Float Rate Payer           : ABSA Capital \n'

    return msg
    
    
def CPISwapMsg(trade, ins, msg):
    msg = msg + 'Trade Date                 : ' + trade.TradeTime()[:10] + '\n'
    msg = msg + 'Start Date                 : ' + str(ins.StartDate()) + '\n'
    msg = msg + 'End/Expiry Date            : ' + str(ins.ExpiryDate())[:10] + '\n'
    msg = msg + 'Commencement Payment Date  : ' + earliestCF(ins) + '\n'
    msg = msg + 'Currency                   : ' + ins.Currency().Name() + '\n' + '\n'
    
    pay_type = ''
    receive_type = ''
    for l in ins.Legs():
        swap = 0
        if l.AmortType() != 'None':
            swap = 1

        if swap:
            lowCF = lowestCF(l)
            startNominal = trade.Quantity() * lowCF.Calculation().Nominal(calcSpace, trade).Value().Number()
            msg = msg + 'Start Notional Amount      : ' + formnum(abs(startNominal)) + '\n'
        else:
            msg = msg + 'Notional Amount            : ' + formnum(abs(trade.Nominal())) + '\n'
        
        legType = l.LegType()
        try:
            if l.IndexRef().Name() == 'SACPI':
                LLegType = '  CPI'
            else:
                LLegType = legType
        except:
            LLegType = legType
        if legType == 'Fixed':
            rate = 'Fixed Rate                 : ' + str(round(l.FixedRate(), 7)) + '\n'
        elif legType == 'Float':
            rate = 'Floating Index             : ' + str(l.FloatRateReference().FreeText()) + '\n'
            rate = rate + 'Reset Frequency            : ' + str(l.RollingPeriod()) + '\n'
        
        if l.PayLeg():
            msg = msg + rate
            msg = msg + 'Reset Type                 : ' + l.ResetType() + '\n'
            msg = msg + NotBlank('Reset Day Offset           : ', l.ResetDayOffset())
            msg = msg + 'Spread                     : ' + str(l.Spread()) + '\n'
        else:
            msg = msg + rate
            msg = msg + 'Initial Price              : ' + str(l.InitialIndexValue()) + '\n'
            msg = msg + 'NACS Rate                  : ' + ins.add_info('NACSRate') + '\n'
            msg = msg + 'Compounding                : ' + 'Applicable' + '\n'

        calendars = Get_Calendar(l)
        uniquecalenders = ''
        for c in calendars:
            if str(c.Name()) not in uniquecalenders:
                uniquecalenders = uniquecalenders + 'Payment Calendar           : ' + str(c.Name()) + '\n' 
        msg = msg + uniquecalenders + '\n'
              
        if l.PayLeg():
            pay_type = LLegType
        else:
            receive_type = LLegType
    
    msg = msg + 'Period End                 : ' + str(l.EndDate()) + '\n'

    if (trade.Nominal()) < 0:
        msg = msg + pay_type + ' Rate Payer           : ' + str(trade.Counterparty().Name()) + '\n'
        msg = msg + receive_type + ' Rate Payer           : ABSA Capital \n'
    else:
        msg = msg + pay_type + ' Rate Payer           : ABSA Capital \n'
        msg = msg + receive_type + ' Rate Payer           : ' + str(trade.Counterparty().Name()) + '\n'

    return msg

def SwaptionMsg(trd, ins, msg):
    curr = ins.Currency().Name()
    matrix = ISDA_SWAPTION_MATRIX[curr]
    Resets = ''
    fixmsg = ''
    floatmsg = ''
    LIBOR = 'No'

    msg = msg + 'Option:' + '\n'
    msg = msg + 'Trade Date                 : ' + str(trd.TradeTime()[:10]) + '\n'
    msg = msg + 'Option Style               : ' + ins.ExerciseType() + '\n'
    msg = msg + 'Premium Amount             : ' + formnum(abs(round(trd.Premium(), 2))) + '\n'
    msg = msg + 'Premium Currency           : ' + trd.Currency().Name() + '\n'
    msg = msg + 'Premium Payment Date       : ' + str(trd.ValueDay()) + '\n'
    msg = msg + 'Expiration Date            : ' + ins.ExpiryDate()[:10] + '\n'
    msg = msg + 'Settlement Type            : ' + str(ins.SettlementType()) + '\n'
    msg = msg + '\n'
    
    msg = msg + 'Swap:\n'
    msg = msg + 'Notional                   : ' + formnum(abs(trd.Nominal())) + '\n'
    msg = msg + 'Currency                   : ' + curr + '\n'
    msg = msg + 'Effective Date             : ' + str(ins.Underlying().StartDate()) + '\n'
    msg = msg + 'Termination Date           : ' + str(ins.Underlying().ExpiryDate()[:10]) + '\n'
    calendars = Get_Calendar(ins.Underlying().Legs()[0])
    for c in calendars:
        msg = msg + 'Business Days              : ' + str(c.Name()) + '\n'
    msg = msg + 'Commencement Payment Date  : ' + earliestCF(ins.Underlying()) + '\n'

    fixmsg = fixmsg + '\n' + 'Fixed Leg:' + '\n'
    floatmsg = floatmsg + '\n' + 'Float Leg:' + '\n'
    fixmsg = fixmsg + 'Fixed Rate                 : ' + str(ins.StrikePrice()) + '\n'
    for p in ins.Underlying().Legs():
        if p.LegType() == 'Fixed':
            a = 1
        elif p.LegType() == 'Float':
            floatmsg = floatmsg + 'Designated Maturity        : ' + str(p.RollingPeriodCount()) + ' ' + p.RollingPeriodUnit() + '\n'
            floatmsg = floatmsg+ 'Spread                     : ' + str(p.Spread()) + '\n'
            floatmsg = floatmsg + 'Compounding                : ' + 'Inapplicable' + '\n'
            floatmsg = floatmsg + 'Floating Rate Option       : ' + p.FloatRateReference().FreeText() + '\n'
    floatmsg = floatmsg + Resets + '\n'
    msg = msg + fixmsg + floatmsg

    if trd.Nominal() < 0:
        msg = msg + 'Buyer                     : ' + trd.Counterparty().Name() + '\n'
        msg = msg + 'Seller                     : ABSA Capital' + '\n'
        if ins.IsCallOption():          #true = Payer
            fixer = trd.Counterparty().Name()
            floater = 'ABSA Capital'
        else:                           #false = Reciever
            fixer = 'ABSA Capital'
            floater = trd.Counterparty().Name()
    else:
        msg = msg + 'Buyer                      : ABSA Capital' + '\n'
        msg = msg + 'Seller                     : ' + trd.Counterparty().Name() + '\n'
        if ins.IsCallOption():          #True = Payer
            fixer = 'ABSA Capital'
            floater = trd.Counterparty().Name()
        else:                           #False = Reciever
            fixer = trd.Counterparty().Name()
            floater = 'ABSA Capital'

    msg = msg + '\n'    
    msg = msg + 'Fixed Rate Payer           : ' + fixer + '\n'
    msg = msg + 'Float Rate Payer           : ' + floater + '\n'
    return msg


def CapletFloorletMsg(trd, ins, msg):
    Resets = ''
    msg = msg + 'Trade Date                 : ' + str(trd.TradeTime()[:10]) + '\n'
    msg = msg + 'Effective Date             : ' + str(ins.Underlying().StartDate()) + '\n'
    msg = msg + 'Termination Date           : ' + str(ins.Underlying().ExpiryDate()[:10]) + '\n'
    msg = msg + 'Notional                   : ' + formnum(abs(trd.Nominal())) + '\n'
    msg = msg + 'Currency                   : ' + str(ins.Currency().Name()) + '\n'
    msg = msg + 'Fixed Rate Payment Date    : ' + trd.ValueDay() + '\n'
    msg = msg + 'Fixed Amount               : ' + formnum(abs(trd.Premium())) + '\n'
    msg = msg + 'Float Payment Dates        : ' + str(ins.Underlying().StartDate()) + '\n'
    
    if ins.IsCallOption():    #Caplet
        msg = msg + 'Caplet Rate                : ' + str(ins.StrikePrice()) + '\n'
    else:                               #Floorlet
        msg = msg + 'Floorlet Rate              : ' + str(ins.StrikePrice()) + '\n'
    
    for p in ins.Underlying().Legs():
        msg = msg + 'Spread                     : ' + str(p.Spread()) + '\n'
        if p.LegType() == 'Float':
            msg = msg + 'Floating Rate Option       : ' + p.FloatRateReference().FreeText() + '\n'
    
    
    calendars = Get_Calendar(ins.Underlying().Legs()[0])
    for c in calendars:
        msg = msg + 'Business Days              : ' + str(c.Name()) + '\n'
    msg = msg + 'FRA Discounting            : ' + 'Applicable' + '\n'
    
    msg = msg + '\n'
    if trd.Nominal() < 0:
        msg = msg + 'Buyer                      : ' + trd.Counterparty().Name() + '\n'
        msg = msg + 'Seller                     : ABSA Capital' + '\n'
        if ins.IsCallOption():          #True = Borrower  
            fixer = trd.Counterparty().Name()
            floater = 'ABSA Capital'
        else:                           #False = Lender
            fixer = trd.Counterparty().Name()
            floater = 'ABSA Capital'
    else:
        msg = msg + 'Buyer                      : ABSA Capital' + '\n'
        msg = msg + 'Seller                     : ' + trd.Counterparty().Name() + '\n'
        if ins.IsCallOption():          #True = Borrower  
            fixer = 'ABSA Capital'
            floater = trd.Counterparty().Name()
        else:                           #False = Lender
            fixer = 'ABSA Capital'
            floater = trd.Counterparty().Name()
            
    msg = msg + '\n'    
    msg = msg + 'Fixed Rate Payer           : ' + fixer + '\n'
    msg = msg + 'Float Rate Payer           : ' + floater + '\n'
    
    return msg
