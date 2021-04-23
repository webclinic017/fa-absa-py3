import acm, ael, csv, datetime
#import xml.dom.minidom as xml

#This is used to map brokers from FA back to the MarkitWire values
#configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'AMWI_Mappings')
#config = xml.parseString(configuration)
#mappings = config.getElementsByTagName("Mappings")

fieldnames = {
                'Swap': ['tradeid', 'internal trade id', 'error', 'directionfrompartya', 'fixedrate', 'rolls convention', 'tradedate', 'start date', 'end date', 'currency', 'notional', 'my entity', 'counterparty', 'floating rate index', 'Spread Over Floating', 'Initial Rate', 'Adjust Fixed Period End Dates', 'Payer Day Basis', 'Payer Business Day Convention', 'Roll Dates Holiday Centres', 'payment holiday centres', 'Payer Payment Frequency', 'Compounding Method', 'Float Roll Frequency', 'Floating Rate Index 2', 'Spread Over Floating 2', 'Fixed Rate 2', 'Adjust Fixed Period End Dates 2', 'Receiver Day Basis', 'Receiver Business Day Convention', 'Roll Dates Holiday Centres 2', 'Receiver Payment Frequency', 'Compounding Method 2', 'Float Roll Frequency 2', 'Roll Day', 'swNormalisationDate', 'batch id', 'book', 'brokerid', 'sales credit', 'swadditionalfield1', 'swadditionalfield2', 'swadditionalfield3', 'swadditionalfield4', 'swadditionalfield5', 'messagetext', 'Break Date', 'Break Frequency', 'Break Date Override', 'Break Date Calculation Method', 'stub at', 'Fixed Stub', 'Float Stub', 'Linear Interpolation', 'Stub Interpolation Floating Rate Index Tenor (1)', 'Stub Interpolation Floating Rate Index Tenor (2)', 'Contractual Definitions', 'Master Agreement', 'Fixing Days Holidays Centres', 'Fixing Days Holidays Centres 2', 'product', 'Initial Rate 2', 'initial rate', 'clientclearing', 'autosendforclearing', 'backloadingflag', 'swClearingBrokerId', 'bilateralclearinghousebic'],
                'FRA': ['tradeid', 'internal trade id', 'error', 'product', 'tradedate', 'start_date', 'amount', 'swbrokertradeid', 'currency', 'fixedrate', 'partya', 'partyb', 'directionfrompartya', 'effectiveDateTenor', 'terminationDateTenor', 'rollConvention', 'swtradingbookid', 'swsalescredit', 'swbatchid', 'swreaffirmnotrequired', 'swadditionalfield1', 'swadditionalfield2', 'swadditionalfield3', 'swadditionalfield4', 'swswaptionexerciseswtradingbookid', 'backloadingflag', 'clientclearing', 'autosendforclearing', 'swClearingBrokerId', 'bilateralclearinghousebic'],
                'AdditionalPayments': ['swbrokerageamountcurrency', 'Swbrokerageamount', 'additional payment 1 amount', 'additional payment 1 date', 'additional payment 1 reason', 'additional payment 1 currency', 'additional payment 1 direction', 'additional payment 1 convention', 'additional payment 1 holiday calendar', 'additional payment 2 amount', 'additional payment 2 date', 'additional payment 2 reason', 'additional payment 2 currency', 'additional payment 2 direction', 'additional payment 2 convention', 'additional payment 2 holiday calendar', 'additional payment 3 amount', 'additional payment 3 date', 'additional payment 3 reason', 'additional payment 3 currency', 'additional payment 3 direction', 'additional payment 3 convention', 'additional payment 3 holiday calendar', 'additional payment 4 amount', 'additional payment 4 date', 'additional payment 4 reason', 'additional payment 4 currency', 'additional payment 4 direction', 'additional payment 4 convention', 'additional payment 4 holiday calendar', 'additional payment 5 amount', 'additional payment 5 date', 'additional payment 5 reason', 'additional payment 5 currency', 'additional payment 5 direction', 'additional payment 5 convention', 'additional payment 5 holiday calendar', 'additional payment 6 amount', 'additional payment 6 date', 'additional payment 6 reason', 'additional payment 6 currency', 'additional payment 6 direction', 'additional payment 6 convention', 'additional payment 6 holiday calendar']
             }

#def GetBrokerMapping(entry):
#    for mapping in mappings:
#        if mapping.getAttribute("MappingName") == 'Brokers':
#            map = mapping.getElementsByTagName("Mapping")
#            for mappedentries in map:
#                if mappedentries.childNodes[0].nodeValue == entry:
#                    return mappedentries.getAttribute("key")

def GetDirectionFromPartyA(fTrade):
    if fTrade.Instrument().InsType() == 'Swap':
        direction = fTrade.Direction()
        if direction == 'Pay Fixed':
            return 'pay'
        elif direction == 'Receive Fixed':
            return 'receive'
    elif fTrade.Instrument().InsType() == 'FRA':
        direction = fTrade.Direction()
        if direction == 'Buy':
            return 'pay'
        elif direction == 'Sell':
            return 'receive'

def GetDayConvention(s):
    if s == 'Mod. Following':
        return 'MODFOLLOWING'
    elif s in ('Preceding', 'Following'):
        return s.upper()
    else:
        return ''

def GetPeriodShort(count, unit):
    return '%s%s' %(count, unit[0])

def OpenFile(n,FileDir,Filename,instrument,*rest):
    filename = FileDir + Filename
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames[instrument] + fieldnames['AdditionalPayments'])

    return filename

def GetRollDatesHolidayCentres(calenders):
    tempstring = ''
    i = 1
    for c in calenders:
        if c is None:
            break

        if i > 1:
            tempstring+=';'

        tempstring += c.BusinessCenter()
        i+=1

    return tempstring

def MapProduct(t):
    insType = t.Instrument().InsType()
    if insType == 'Swap':
        return 'IRS'
    else:
        return insType

def GetBackloadingFlag(t):
    diff = datetime.datetime.today() - datetime.datetime.strptime(t.TradeTime(), '%Y-%m-%d %H:%M:%S')
    if diff.days > 10:
        return True
    else:
        return ''

def GetSwiftCode(party):
    matches = [x for x in party.Aliases() if x.Type().AliasTypeName() == 'MarkitWireID']
    if len(matches) == 0:
        if party.Swift():
            return party.Swift()
        else:
            raise Exception('No MarkitWireID alias found for FParty %s' %(party.Name()))
    else:
        return matches[0].Alias()

def GetTerminationDateTenor(leg):
    if not leg:
        return ''

    months = leg.EndPeriodCount()

    if (leg.EndPeriodUnit() == 'Days'):
        months/= 30
    elif (leg.EndPeriodUnit() == 'Years'):
        months*= 12

    temp = leg.RollingPeriodCount()

    if (leg.RollingPeriodUnit() == 'Days'):
        temp/= 30
    elif (leg.RollingPeriodUnit() == 'Years'):
        temp*= 12

    months+=temp
    return '%s%s' %(months, 'M')

def GetEffectiveDateTenor(leg):
    if not leg:
        return ''

    months = leg.EndPeriodCount()

    if (leg.EndPeriodUnit() == 'Days'):
        months/= 30
    elif (leg.EndPeriodUnit() == 'Years'):
        months*= 12

    return '%s%s' %(months, 'M')

def MapPaymentType(pType):
    if pType == 'Premium':
        return 'UpfrontFee'
    elif pType == 'Termination Fee':
        return 'PartialTermination'
    else:
        return 'UnclassifiedFee'

def GenerateAdditionalPayments(payments, holidays):
    paymentsList = {}
    count = 1

    for p in payments:
        if p.Type() == 'Broker Fee':
            paymentsList['swbrokerageamountcurrency'] = p.Currency().Name()
            paymentsList['Swbrokerageamount'] = abs(p.Amount())
        else:
            paymentsList['additional payment %s amount' %(count)] = abs(p.Amount())
            paymentsList['additional payment %s date' %(count)] = p.PayDay()

            paymentsList['additional payment %s reason' %(count)] = MapPaymentType(p.Type())
            paymentsList['additional payment %s currency' %(count)] = p.Currency().Name()
            paymentsList['additional payment %s direction' %(count)] = 'Pay' if p.Amount() < 0 else 'Rec'
            paymentsList['additional payment %s convention' %(count)] = 'MODFOLLOWING'
            paymentsList['additional payment %s holiday calendar' %(count)] = holidays
            count += 1

    return paymentsList


def MapDayCountMethod(leg):
    daycountmethod = leg.DayCountMethod()
    if leg.LegType() == 'Fixed':
        type = '.FIXED'
    else:
        type = ''

    if daycountmethod.upper() == 'ACT/365':
        return daycountmethod.upper() + '.FIXED'
    else:
        return daycountmethod.upper()

def WriteFRA(t, writer, autoclear):
    us = GetSwiftCode(t.Acquirer())

    if us != 'ABSAZAJJ':
        return None

    fields = {
             'amount': '%d' %(abs(t.Nominal())),
             'backloadingflag': GetBackloadingFlag(t),
             'currency': t.Instrument().Currency().Name(),
             'directionfrompartya': GetDirectionFromPartyA(t),
             'effectiveDateTenor': GetEffectiveDateTenor(t.Instrument().FirstFloatLeg()),
             'fixedrate': str("%.8f" % round(t.Instrument().FirstFloatLeg().FixedRate() / 100, 8)) if t.Instrument().FirstFloatLeg() else '',
             'internal trade id': t.Oid(),
             'partya': us,
             'partyb': GetSwiftCode(t.Counterparty()),
             'product': MapProduct(t),
             'rollConvention': 'IMM',
             'start_date': acm.Time.AsDate(t.Instrument().FirstFloatLeg().StartDate()),
             'swadditionalfield1': t.Acquirer().Name(),
             'swadditionalfield2': '',
             'swadditionalfield3': '',
             'swadditionalfield4': '',
             'swbatchid': '',
             'swreaffirmnotrequired': '',
             'swsalescredit': '',
             'swswaptionexerciseswtradingbookid': '',
             'swtradingbookid': t.Portfolio().Name(),
             'terminationDateTenor': GetTerminationDateTenor(t.Instrument().FirstFloatLeg()),
             'tradedate': acm.Time.AsDate(t.TradeTime()),
    }

    if autoclear == 'true':
        clearingfields = {
            'swClearingBrokerId'                : 'MEGA1234',
            'bilateralclearinghousebic'         : 'LCHLGB22XXX',
            'autosendforclearing'               : '1',
            'clientclearing'                    : '1'
        }

        fields.update(clearingfields)

    payments = GenerateAdditionalPayments(t.Payments(), 'USNY')
    fields.update(payments)
    writer.writerow(fields)

def WriteSwap(t, writer, autoclear):
    us = GetSwiftCode(t.Acquirer())

    if us != 'ABSAZAJJ':
        return None

    direction = GetDirectionFromPartyA(t)
    payLeg = t.Instrument().PayLeg() if direction == 'pay' else t.Instrument().RecLeg()
    recLeg = t.Instrument().RecLeg() if direction == 'pay' else t.Instrument().PayLeg()

    fields = {
             'backloadingflag': GetBackloadingFlag(t),
             'book': t.Portfolio().Name(),
             'counterparty': GetSwiftCode(t.Counterparty()),
             'currency': t.Instrument().Currency().Name(),
             'directionfrompartya': GetDirectionFromPartyA(t),
             'end date': t.Instrument().EndDate(),
             'fixedrate': str("%.8f" % round(t.Instrument().PayLeg().FixedRate() / 100, 8)) if t.Instrument().PayLeg() else '',
             'Float Roll Frequency': GetPeriodShort(t.Instrument().FirstFloatLeg().RollingPeriodCount(), t.Instrument().FirstFloatLeg().RollingPeriodUnit()),
             'floating rate index': t.Instrument().PayLeg().FloatRateReference().FreeText() if t.Instrument().PayLeg().FloatRateReference() else '',
             'Floating Rate Index 2': t.Instrument().RecLeg().FloatRateReference().FreeText() if t.Instrument().RecLeg().FloatRateReference() else '',
             'internal trade id': t.Oid(),
             'my entity': us,
             'notional': '%d' %(abs(t.Nominal())),
             'Payer Business Day Convention': GetDayConvention(payLeg.PayDayMethod()),
             'Payer Day Basis': MapDayCountMethod(payLeg),
             'Payer Payment Frequency': GetPeriodShort(payLeg.RollingPeriodCount(), payLeg.RollingPeriodUnit()),
             'payment holiday centres': GetRollDatesHolidayCentres( [t.Instrument().PayLeg().PayCalendar(), t.Instrument().PayLeg().Pay2Calendar(), t.Instrument().PayLeg().Pay3Calendar()] ),
             'product': MapProduct(t),
             'Receiver Business Day Convention': GetDayConvention(recLeg.PayDayMethod()),
             'Receiver Day Basis': MapDayCountMethod(recLeg),
             'Receiver Payment Frequency': GetPeriodShort(recLeg.RollingPeriodCount(), recLeg.RollingPeriodUnit()),
             'Roll Dates Holiday Centres': GetRollDatesHolidayCentres( [payLeg.PayCalendar(), payLeg.Pay2Calendar(), payLeg.Pay3Calendar()] ),
             'Roll Day': datetime.datetime.strptime(t.Instrument().PayLeg().RollingPeriodBase(), '%Y-%m-%d').strftime('%d'),
             'Spread Over Floating 2': t.Instrument().RecLeg().Spread(),
             'Spread Over Floating': t.Instrument().PayLeg().Spread(),
             'start date': t.Instrument().StartDate(),
             'swadditionalfield1': t.Acquirer().Name(),
             'tradedate': acm.Time.AsDate(t.TradeTime()),
    }

    if autoclear == 'true':
       clearingfields = {
           'swClearingBrokerId'                : 'MEGA1234',
           'bilateralclearinghousebic'         : 'LCHLGB22XXX',
           'autosendforclearing'               : 'true',
           'clientclearing'                    : 'true'
       }

       fields.update(clearingfields)

    payments = GenerateAdditionalPayments(t.Payments(), fields['Roll Dates Holiday Centres'])
    fields.update(payments)
    writer.writerow(fields)

def Write(n,trade,FileDir,Filename,autoclear, *rest):
    try:
        t = acm.FTrade[trade]

        filename = FileDir + Filename
        with open(filename, 'ab') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames[t.Instrument().InsType()] + fieldnames['AdditionalPayments'])
            if t.Instrument().InsType() in ('FRA'):
                WriteFRA(t, writer, autoclear);
            elif t.Instrument().InsType() in ('Swap'):
                WriteSwap(t, writer, autoclear);
            else:
                raise Exception('Trade %s doesn''t fall within the instrument scope of the BAT tool' %(trade))

        return '3. Successful write'

    except Exception as inst:
        print 'Failed writing %s due to %s on field %s' %(trade, type(inst), inst)
        return '4. Failed write'