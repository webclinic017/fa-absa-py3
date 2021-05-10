'''
Confirmation XML templates.

HISTORY
When            Change                  Who                     What
2015-09-17      Initial deployment      Sanele Macanda
2015-11-05      CHNG0003231673          Willie vd Bank          Added functionality to display the long and short pary names
2016-08-04      ABITFA-4389             Marcelo G. Almiron      Refresh email passed to Adaptiv on non-production environments
2016                                    Manan Gosh              Demat implementation
2017                                    Willie vd Bank          Changed method keyword to function as per 2017 upgrade requirement
'''

Heading = '''<?xml version="1.0" encoding="ISO-8859-1"?>'''
Confirmation = '''
    <CONFIRMATION>
        <ACQUIRERADDRESS><acmCode function='GetAcquirerContactEmail' file='Adaptiv_XML_Functions'/></ACQUIRERADDRESS>
        <AMENDMENT_ADJUSTDEPOSIT><acmCode function='getAmendmentAdjustDeposit' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></AMENDMENT_ADJUSTDEPOSIT>
        <AMENDMENT_FIXED><acmCode function='getAmendmentFixed' file='Adaptiv_XML_Functions'/></AMENDMENT_FIXED>
        <ARRANGED_BY><acmCode method ='Trade.Trader.FullName' ignoreUpdate ='True'/></ARRANGED_BY>
        <CASHPAYMENTID><acmCode function='getCashPaymentId' file='Adaptiv_XML_Functions'/></CASHPAYMENTID>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name' ignoreUpdate ='True'/></CONF_TEMPLATE_CHLNBR>
        <CONF_NUMBER><acmCode method ='Oid' ignoreUpdate ='True'/></CONF_NUMBER>
        <COUNTERPARTYADDRESS><acmCode function='getCounterpartyAddress' file='Adaptiv_XML_Functions'/></COUNTERPARTYADDRESS>
        <CREATEDATE><acmCode function='GetConfCreateData' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CREATEDATE>
        <EVENTCHLITEM><acmCode method='EventChlItem.Name' ignoreUpdate ='True'/></EVENTCHLITEM>
        <FILENAME><acmCode function='GetFileName' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></FILENAME>
        <GETEVENTTYPE><acmCode function='GetEventType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></GETEVENTTYPE>
        <GETTEMPLATETOUSE><acmCode function='GetTemplateToUse' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></GETTEMPLATETOUSE>
        <HEADER><acmCode function='GetEmailSubjectHeader' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></HEADER>
        <ISSHOWSSI><acmCode function='IsShowSSI' file='Adaptiv_XML_Functions'/></ISSHOWSSI>
        <LEGALNOTICE><acmCode function='GetLegalNotice' file='Adaptiv_XML_Functions'/></LEGALNOTICE>
        <NovatedCP><acmCode function='GetNovatedCP' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></NovatedCP>
        <ORIGINATINGCTRY><acmCode method='Trade.Acquirer.Name' ignoreUpdate ='True'/></ORIGINATINGCTRY>
        <SELECTTEMPLATETOUSE><acmCode function='SelectCorrectTemplateFields' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></SELECTTEMPLATETOUSE>
        <SPECIALINSTR><acmCode function='GetSpecialInstruction' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></SPECIALINSTR>
        <TRANSPORT><acmCode method ='Transport' ignoreUpdate ='True'/></TRANSPORT>
        <TRDNUMBER><acmCode method='Trade.Oid' ignoreUpdate ='True'/></TRDNUMBER>
        <TYPE><acmCode function='GetConfType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
    </CONFIRMATION>'''
Acquirer = '''
    <ACQUIRER acmLoop='Trade.Acquirer'>
        <ACQUIRER_SSI acmLoop = "GetAcqrAcc" file = 'Adaptiv_XML_Functions'>
            <CASH_ACCOUNT>
                <ACCNUM><acmCode function='GetAccNumber' file='Adaptiv_XML_Functions'/></ACCNUM>
                <CORRESBANK><acmCode function='GetCorrBank' file='Adaptiv_XML_Functions'/></CORRESBANK>
                <CURRENCY><acmCode function='GetAccCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
            </CASH_ACCOUNT>
        </ACQUIRER_SSI>
        <ACQUIREREMAIL><acmCode function='GetAcquirerEmail' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ACQUIREREMAIL>
        <CITY><acmCode method='City'/></CITY>
        <CONTACT acmLoop='GetAcquirerContact' file = 'Adaptiv_XML_Functions'>
            <ADDRESS1>15 Alice Lane, Sandton, 2196</ADDRESS1>
            <ADDRESS2>Private Bag X10056, Sandton, 2196</ADDRESS2>
            <COUNTRY>South Africa</COUNTRY>
            <TEL>+27 (0)11 895 7708</TEL>
            <FAX><acmCode method='Fax'/></FAX>
            <EMAIL><acmCode method='Email'/></EMAIL>
        </CONTACT>
        <NAME>Absa Corporate and Investment Banking</NAME>
    </ACQUIRER>'''
Counterparty = '''
    <COUNTERPARTY acmLoop='Trade.Counterparty'>
        <CONTACT acmLoop='GetContact' file = 'Adaptiv_XML_Functions'>
            <ADDRESS1><acmCode method='Address'/></ADDRESS1>
            <ADDRESS2><acmCode method='Address2'/></ADDRESS2>
            <ATTENTION><acmCode method='Attention'/></ATTENTION>
            <COUNTRY><acmCode method='Country'/></COUNTRY>
            <EMAIL><acmCode method='Email'/></EMAIL>
            <FAX><acmCode method='Fax'/></FAX>
            <TEL><acmCode method='Telephone'/></TEL>
        </CONTACT>
        <COUNTERPARTY_SSI acmLoop = "GetCptyAcc" file = 'Adaptiv_XML_Functions'>
            <CASH_ACCOUNT>
                <ACCNUM><acmCode function='GetAccNumber' file='Adaptiv_XML_Functions'/></ACCNUM>
                <CASHFLOWTYPE><acmCode function='GetAccCashflowType' file='Adaptiv_XML_Functions'/></CASHFLOWTYPE>
                <CORRESBANK><acmCode function='GetCorrBank' file='Adaptiv_XML_Functions'/></CORRESBANK>
                <CURRENCY><acmCode function='GetAccCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
            </CASH_ACCOUNT>
        </COUNTERPARTY_SSI>
        <FULLNAME><acmCode function='GetCounterpartyFullname' file='Adaptiv_XML_Functions'/></FULLNAME>
        <SHORTNAME><acmCode function='GetCounterpartyShortname' file='Adaptiv_XML_Functions'/></SHORTNAME>
        <ALIAS><acmCode function='GetCounterpartyAlias' file='Adaptiv_XML_Functions'/></ALIAS>
    </COUNTERPARTY>'''

# ----------------------------------------------------------------------------------------------------#
xml_Maturity_Notice_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></EXPDAY>
        <LEGS acmLoop='Legs'>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></PAYOFFSET>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></RATE>
            <SPREAD><acmCode function='GetLegSpread' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></SPREAD>
        </LEGS>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></BUYORSELL>
        <CALLTRADEBALANCE><acmCode function='GetCallTradeBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CALLTRADEBALANCE>
        <CEDEDAMOUNT><acmCode function= 'GetCededAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CEDEDAMOUNT>
        <CURRENCY><acmCode method='Trade.Currency.Name' ignoreUpdate ='True'/></CURRENCY>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <INTEREST><acmCode function='GetTrdInterest' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></INTEREST>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></NOMINAL>
        <PRICE><acmCode method='Trade.Price' ignoreUpdate ='True'/></PRICE>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></VALUEDAY>
        <EXTERNALID><acmCode function= 'GetExternalID' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></EXTERNALID>
    </TRADE>
</MESSAGE>
'''

xml_Deposit_Close_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <LEGS acmLoop='Legs'>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></PAYOFFSET>
        </LEGS>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <CASHFLOWS acmLoop='GetClosingPayments' file='Adaptiv_XML_Functions'>
            <AMOUNT><acmCode function='GetAbsoluteRoundPayment' file='Adaptiv_XML_Functions'/></AMOUNT>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <INSTRUCTION><acmCode function='GetPaymentPayOrReceive' file='Adaptiv_XML_Functions'/></INSTRUCTION>
            <PAYDAY><acmCode method='PayDay'/></PAYDAY>
            <TYPE><acmCode method='Type'/></TYPE>
        </CASHFLOWS>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></BUYORSELL>
        <CEDEDAMOUNT><acmCode function= 'GetCededAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CEDEDAMOUNT>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <FEES><acmCode function='GetPaymentSum' file='Adaptiv_XML_Functions'/></FEES>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <NETTERMINATEDAMOUNT><acmCode function= 'GetTerminatedAmount' file='Adaptiv_XML_Functions'/></NETTERMINATEDAMOUNT>
        <TERMINATIONREMAININGAMOUNT><acmCode function= 'GetTerminationRemainingAmount' file='Adaptiv_XML_Functions'/></TERMINATIONREMAININGAMOUNT>
        <NOMINAL><acmCode function='GetPaymentSum' file='Adaptiv_XML_Functions'/></NOMINAL>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_Deposit_Novation_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <LEGS acmLoop='Legs'>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></PAYOFFSET>
        </LEGS>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <CASHFLOWS acmLoop='GetClosingPayments' file='Adaptiv_XML_Functions'>
            <AMOUNT><acmCode function='GetAbsoluteRoundPayment' file='Adaptiv_XML_Functions'/></AMOUNT>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <INSTRUCTION><acmCode function='GetPaymentPayOrReceive' file='Adaptiv_XML_Functions'/></INSTRUCTION>
            <PAYDAY><acmCode method='PayDay'/></PAYDAY>
            <TYPE><acmCode method='Type'/></TYPE>
        </CASHFLOWS>
        <CEDEDAMOUNT><acmCode function= 'GetCededAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CEDEDAMOUNT>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <NETTERMINATEDAMOUNT><acmCode function= 'GetTerminatedAmount' file='Adaptiv_XML_Functions'/></NETTERMINATEDAMOUNT>
        <NOMINAL><acmCode function='GetPaymentSum' file='Adaptiv_XML_Functions'/></NOMINAL>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''
xml_Deposit_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <CALLMOVEMENT>
            <AMOUNT><acmCode function='GetCallMovementAmt' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></AMOUNT>
            <INOUT><acmCode function='GetCallMovementSgn' file='Adaptiv_XML_Functions'/></INOUT>
        </CALLMOVEMENT>
        <DAYSBETWEEN><acmCode function='GetDaysBetween' file='Adaptiv_XML_Functions'/></DAYSBETWEEN>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
        <ISCALLACCOUNT><acmCode method='IsCallAccount'/></ISCALLACCOUNT>
        <LEGS acmLoop='Legs'>
            <AMORTISATION>
                <ROLLING><acmCode function='GetAmortRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
                <TYPE><acmCode method='AmortType'/></TYPE>
            </AMORTISATION>
            <CASHFLOWS acmLoop='GetCashFlows' file='Adaptiv_XML_Functions'>
                <AMOUNT><acmCode function='GetCFProjConverted' file='Adaptiv_XML_Functions'/></AMOUNT>
                <CURRENCY><acmCode function='GetCFCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
                <INSTRUCTION><acmCode function='GetCFPayOrReceive' file='Adaptiv_XML_Functions'/></INSTRUCTION>
                <PAYDAY><acmCode function='GetCFPayDay' file='Adaptiv_XML_Functions'/></PAYDAY>
                <TYPE><acmCode function='GetCFTypeConverted' file='Adaptiv_XML_Functions'/></TYPE>
            </CASHFLOWS>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions'/></DAYCOUNT>
            <FLOATREF><acmCode method='FloatRateReference.Name'/></FLOATREF>
            <INITIALRATE acmLoop = "Is_Initial_Rate" file = 'Adaptiv_XML_Functions'><acmCode function = "Convert_Reset_Rate" file = 'Adaptiv_XML_Functions'/></INITIALRATE>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions'/></PAYOFFSET>
            <PAYOFFSETCALS>
                <PAYOFFSETCAL1 acmLoop='PayCalendar'><acmCode method='Name'/></PAYOFFSETCAL1>
                <PAYOFFSETCAL2 acmLoop='Pay2Calendar'><acmCode method='Name'/></PAYOFFSETCAL2>
                <PAYOFFSETCAL3 acmLoop='Pay3Calendar'><acmCode method='Name'/></PAYOFFSETCAL3>
                <PAYOFFSETCAL4 acmLoop='Pay4Calendar'><acmCode method='Name'/></PAYOFFSETCAL4>
                <PAYOFFSETCAL5 acmLoop='Pay5Calendar'><acmCode method='Name'/></PAYOFFSETCAL5>
            </PAYOFFSETCALS>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions'/></RATE>
            <REDEMPTIONAMOUNT>TBD</REDEMPTIONAMOUNT>
            <RESETPERIOD><acmCode function='GetResetPeriod' file='Adaptiv_XML_Functions'/></RESETPERIOD>
            <ROLLING><acmCode function='GetLegRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
            <SPREAD><acmCode function='GetLegSpread' file='Adaptiv_XML_Functions'/></SPREAD>
            <TYPE><acmCode function='GetLegTypeFixOrFloat' file='Adaptiv_XML_Functions'/></TYPE>
        </LEGS>
        <NAME><acmCode method='Name'/></NAME>
        <RESETS acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
            <DATE><acmCode function='GetResetDay' file='Adaptiv_XML_Functions'/></DATE>
        </RESETS>      
        <RATE_RESETS>
            <RESET acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
                <DATE><acmCode function='GetResetDay' file='Adaptiv_XML_Functions'/></DATE>
            </RESET>
        </RATE_RESETS>    
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <BARXTRADENUMBER><acmCode function='GetBARXTradeNumber' file='Adaptiv_XML_Functions'/></BARXTRADENUMBER>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <CALLTRADEBALANCE><acmCode function='GetCallTradeBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CALLTRADEBALANCE>
        <CEDEDAMOUNT><acmCode function= 'GetCededAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CEDEDAMOUNT>
        <CONTRACTTRADE><acmCode function= 'CloseTrade' file='Adaptiv_XML_Functions'/></CONTRACTTRADE>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <DEPOSITBALANCE><acmCode function= 'GetDepositBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DEPOSITBALANCE>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <INTEREST><acmCode function='GetTrdInterest' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></INTEREST>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions'/></NOMINAL>
        <PRICE><acmCode method='Trade.Price'/></PRICE>
        <FEES><acmCode function='GetPaymentSum' file='Adaptiv_XML_Functions'/></FEES>
        <FUNDINGINSTYPE><acmCode function='funding_instype' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></FUNDINGINSTYPE>
        <TERMAVAILABLEBALANCE><acmCode function='GetTermAvailableBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TERMAVAILABLEBALANCE>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
        <EXTERNALID><acmCode function= 'GetExternalID' file='Adaptiv_XML_Functions'/></EXTERNALID>
    </TRADE>
</MESSAGE>
'''

xml_Deposit_Adjust_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <CALLMOVEMENT>
            <AMOUNT><acmCode function='GetCallMovementAmt' file='Adaptiv_XML_Functions'/></AMOUNT>
            <INOUT><acmCode function='GetCallMovementSgn' file='Adaptiv_XML_Functions'/></INOUT>
        </CALLMOVEMENT>
        <ISCALLACCOUNT><acmCode method='IsCallAccount'/></ISCALLACCOUNT>
        <LEGS acmLoop='Legs'>
            <AMORTISATION>
                <ROLLING><acmCode function='GetAmortRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
                <TYPE><acmCode method='AmortType'/></TYPE>
            </AMORTISATION>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions'/></DAYCOUNT>
            <FLOATREF><acmCode method='FloatRateReference.Name'/></FLOATREF>
            <INITIALRATE acmLoop = "Is_Initial_Rate" file = 'Adaptiv_XML_Functions'><acmCode function = "Convert_Reset_Rate" file = 'Adaptiv_XML_Functions'/></INITIALRATE>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions'/></PAYOFFSET>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions'/></RATE>
            <REDEMPTIONAMOUNT>TBD</REDEMPTIONAMOUNT>
            <RESETPERIOD><acmCode function='GetResetPeriod' file='Adaptiv_XML_Functions'/></RESETPERIOD>
            <ROLLING><acmCode function='GetLegRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
            <SPREAD><acmCode function='GetLegSpread' file='Adaptiv_XML_Functions'/></SPREAD>
            <TYPE><acmCode function='GetLegTypeFixOrFloat' file='Adaptiv_XML_Functions'/></TYPE>
        </LEGS>
        <NAME><acmCode method='Name'/></NAME>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <BARXTRADENUMBER><acmCode function='GetBARXTradeNumber' file='Adaptiv_XML_Functions'/></BARXTRADENUMBER>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <CALLTRADEBALANCE><acmCode function='GetCallTradeBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CALLTRADEBALANCE>
        <CEDEDAMOUNT><acmCode function= 'GetCededAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CEDEDAMOUNT>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <DEPOSITBALANCE><acmCode function= 'GetDepositBalance' file='Adaptiv_XML_Functions'/></DEPOSITBALANCE>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <EXTERNALID><acmCode function= 'GetExternalID' file='Adaptiv_XML_Functions'/></EXTERNALID>
        <INTEREST><acmCode function='GetTrdInterest' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></INTEREST>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_Call_Deposit_Opening_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
        <LEGS acmLoop='Legs'>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions' ignoreUpdate='True'/></RATE>
        </LEGS>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <BARXTRADENUMBER><acmCode function='GetBARXTradeNumber' file='Adaptiv_XML_Functions'/></BARXTRADENUMBER>
        <CALLTRADEBALANCE><acmCode function='GetCallTradeBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CALLTRADEBALANCE>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <DEPOSITBALANCE><acmCode function= 'GetDepositBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DEPOSITBALANCE>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <EXTERNALID><acmCode function= 'GetExternalID' file='Adaptiv_XML_Functions'/></EXTERNALID>
    </TRADE>
</MESSAGE>
'''

xml_Deposit_Cede_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <BARXTRADENUMBER><acmCode function='GetBARXTradeNumber' file='Adaptiv_XML_Functions'/></BARXTRADENUMBER>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <CALLTRADEBALANCE><acmCode function='GetCallTradeBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CALLTRADEBALANCE>
        <CEDEDAMOUNT><acmCode function= 'GetCededAmount' file='Adaptiv_XML_Functions'/></CEDEDAMOUNT>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <DEPOSITBALANCE><acmCode function= 'GetDepositBalance' file='Adaptiv_XML_Functions'/></DEPOSITBALANCE>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ENDCASH>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></NOMINAL>
        <TERMAVAILABLEBALANCE><acmCode function= 'GetTermAvailableBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TERMAVAILABLEBALANCE>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <EXTERNALID><acmCode function= 'GetExternalID' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></EXTERNALID>
    </TRADE>
</MESSAGE>
'''

xml_Rate_Fixing_Main_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <EXP_DAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></EXP_DAY>
        <LEGS acmLoop='Legs'>
            <INITIALRATE acmLoop = "Is_Initial_Rate" file = 'Adaptiv_XML_Functions'><acmCode function = "Convert_Reset_Rate" file = 'Adaptiv_XML_Functions' ignoreUpdate ='True'/></INITIALRATE>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions' ignoreUpdate='True'/></RATE>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions'/></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions'/></PAYOFFSET>
            <FLOATREF><acmCode method='FloatRateReference.Name' ignoreUpdate ='True'/></FLOATREF>
            <ROLLING><acmCode function='GetLegRollingFormatted' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ROLLING>
            <SPREAD><acmCode function='GetLegSpread' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></SPREAD>
        </LEGS>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
    </INSTRUMENT>
    <RATE_FIXING acmLoop='Reset'>
        <DAY><acmCode function='GetResetDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DAY>
        <FORWARDRATE><acmCode function='GetForwardRate' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></FORWARDRATE>
        <NEXTPAYAMOUNT><acmCode function='GetCashFlowAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></NEXTPAYAMOUNT>
        <NEXTPAYDATE><acmCode function='GetCashFlowDate' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></NEXTPAYDATE>
        <VALUE><acmCode method ='FixingValue' ignoreUpdate ='True'/></VALUE>
    </RATE_FIXING>
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></BUYORSELL>
        <CALLTRADEBALANCE><acmCode function='GetCallTradeBalance' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></CALLTRADEBALANCE>
        <DEPOSITBALANCE><acmCode function= 'GetDepositBalance' file='Adaptiv_XML_Functions'/></DEPOSITBALANCE>
        <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></NOMINAL>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></VALUEDAY>
        <INTEREST><acmCode function='GetTrdInterest' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></INTEREST>
    </TRADE>
</MESSAGE>
'''

xml_CD_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <CALLMOVEMENT>
            <AMOUNT><acmCode function='GetCallMovementAmt' file='Adaptiv_XML_Functions'/></AMOUNT>
            <INOUT><acmCode function='GetCallMovementSgn' file='Adaptiv_XML_Functions'/></INOUT>
        </CALLMOVEMENT>
        <DAYSBETWEEN><acmCode function='GetDaysBetween' file='Adaptiv_XML_Functions'/></DAYSBETWEEN>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
        <ISCALLACCOUNT><acmCode method='IsCallAccount'/></ISCALLACCOUNT>
        <LEGS acmLoop='Legs'>
            <AMORTISATION>
                <ROLLING><acmCode function='GetAmortRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
                <TYPE><acmCode method='AmortType'/></TYPE>
            </AMORTISATION>
            <CASHFLOWS acmLoop='GetCashFlows' file='Adaptiv_XML_Functions'>
                <AMOUNT><acmCode function='GetCFProjConverted' file='Adaptiv_XML_Functions'/></AMOUNT>
                <CURRENCY><acmCode function='GetCFCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
                <INSTRUCTION><acmCode function='GetCFPayOrReceive' file='Adaptiv_XML_Functions'/></INSTRUCTION>
                <PAYDAY><acmCode function='GetCFPayDay' file='Adaptiv_XML_Functions'/></PAYDAY>
                <TYPE><acmCode function='GetCFTypeConverted' file='Adaptiv_XML_Functions'/></TYPE>
            </CASHFLOWS>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions'/></DAYCOUNT>
            <FLOATREF><acmCode method='FloatRateReference.Name'/></FLOATREF>
            <INITIALRATE acmLoop = "Is_Initial_Rate" file = 'Adaptiv_XML_Functions'><acmCode function = "Convert_Reset_Rate" file = 'Adaptiv_XML_Functions'/></INITIALRATE>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions'/></PAYOFFSET>
            <PAYOFFSETCALS>
                <PAYOFFSETCAL1 acmLoop='PayCalendar'><acmCode method='Name'/></PAYOFFSETCAL1>
                <PAYOFFSETCAL2 acmLoop='Pay2Calendar'><acmCode method='Name'/></PAYOFFSETCAL2>
                <PAYOFFSETCAL3 acmLoop='Pay3Calendar'><acmCode method='Name'/></PAYOFFSETCAL3>
                <PAYOFFSETCAL4 acmLoop='Pay4Calendar'><acmCode method='Name'/></PAYOFFSETCAL4>
                <PAYOFFSETCAL5 acmLoop='Pay5Calendar'><acmCode method='Name'/></PAYOFFSETCAL5>
            </PAYOFFSETCALS>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions'/></RATE>
            <REDEMPTIONAMOUNT>TBD</REDEMPTIONAMOUNT>
            <RESETPERIOD><acmCode function='GetResetPeriod' file='Adaptiv_XML_Functions'/></RESETPERIOD>
            <ROLLING><acmCode function='GetLegRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
            <SPREAD><acmCode function='GetLegSpread' file='Adaptiv_XML_Functions'/></SPREAD>
            <TYPE><acmCode function='GetLegTypeFixOrFloat' file='Adaptiv_XML_Functions'/></TYPE>
        </LEGS>
        <NAME><acmCode method='Name'/></NAME>
        <RESETS acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
            <DATE><acmCode function='GetResetDay' file='Adaptiv_XML_Functions'/></DATE>
        </RESETS>      
        <RATE_RESETS>
            <RESET acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
                <DATE><acmCode function='GetResetDay' file='Adaptiv_XML_Functions'/></DATE>
            </RESET>
        </RATE_RESETS>    
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <ENDCASH><acmCode function='GetTrdEndCash' file='Adaptiv_XML_Functions'/></ENDCASH>
        <INTEREST><acmCode function='GetTrdInterest' file='Adaptiv_XML_Functions'/></INTEREST>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions'/></NOMINAL>
        <PRICE><acmCode method='Trade.Price'/></PRICE>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_Deposit_Expiry_Notice_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
    </INSTRUMENT>    
    <TRADE acmLoop='Trade'>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
    </TRADE>
</MESSAGE>
'''

xml_Cash_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>
    <TRADE acmLoop='Trade'>
        <CURRENCY_PAIR acmLoop = 'GetFxSwapTrades' file='Adaptiv_XML_Functions'>
            <PAIR>
                <AMOUNT><acmCode function='GetTrdQuantity' file='Adaptiv_XML_Functions'/></AMOUNT>
                <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
                <CURRENCY><acmCode method='Instrument.Currency.Name'/></CURRENCY>
            </PAIR>
            <PAIR>
                <AMOUNT><acmCode function='GetTrdPremium' file='Adaptiv_XML_Functions'/></AMOUNT>
                <BUYORSELL><acmCode function='GetPremiumBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
                <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            </PAIR>
            <PAYDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></PAYDAY>
            <RATE><acmCode method='Price'/></RATE>
        </CURRENCY_PAIR>
        <CURRENCYQUOTE><acmCode function='GetCurrencyQuote' file='Adaptiv_XML_Functions'/></CURRENCYQUOTE>
        <PRICE><acmCode method='Price'/></PRICE>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_Frn_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <DAYSBETWEEN><acmCode function='GetDaysBetween' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></DAYSBETWEEN>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></EXPDAY>
        <ISSUER><acmCode method='Issuer.Name' ignoreUpdate ='True' /></ISSUER>
        <LEGS acmLoop='Legs'>
            <CASHFLOWS acmLoop='CashFlows'>
                <AMOUNT><acmCode function='GetCFProjConverted' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></AMOUNT>
                <CURRENCY><acmCode function='GetCFCurr' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></CURRENCY>
                <PAYDAY><acmCode function='GetCFPayDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></PAYDAY>
                <TYPE><acmCode function='GetCFTypeConverted' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></TYPE>
            </CASHFLOWS>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></PAYOFFSET>
            <REDEMPTIONAMOUNT>100% of Principal Amount</REDEMPTIONAMOUNT>
            <FLOATREF><acmCode method='FloatRateReference.Name' ignoreUpdate ='True' /></FLOATREF>
            <ROLLING><acmCode function='GetLegRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
            <SPREAD><acmCode function='GetLegSpread' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></SPREAD>
            <TYPE><acmCode function='GetLegTypeFixOrFloat' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
        </LEGS>
        <NAME><acmCode method='Name'/></NAME>
        <PAYDAYS><acmCode function='GetAllCFPayDays' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></PAYDAYS>
        <RESETS acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
            <DAY><acmCode function='GetResetDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DAY>
        </RESETS>
        <RATE_RESETS>
            <RESET acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
                <DATE><acmCode function='GetResetDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DATE>
            </RESET>
        </RATE_RESETS> 
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
    </INSTRUMENT>
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></BUYORSELL>
        <CURRENCY><acmCode method='Trade.Currency.Name' ignoreUpdate ='True' /></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></NOMINAL>
        <POSITION><acmCode function='GetTrdPos' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></POSITION>
        <PREMIUM>
            <AMOUNT><acmCode function='GetTrdPremium' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></AMOUNT>
            <PAYDATE><acmCode function='GetTrdPremiumPayDate' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></PAYDATE>
        </PREMIUM>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid' /></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_FXOption_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <CALL>
            <AMOUNT><acmCode function='GetOptCallAmnt' file='Adaptiv_XML_Functions'/></AMOUNT>
            <CURRENCY><acmCode function='GetOptCallCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
        </CALL>
        <CALLORPUT><acmCode function='GetOptCallOrPut' file='Adaptiv_XML_Functions'/></CALLORPUT>
        <DELIVERYDAY><acmCode function='GetInsDeliveryDate' file='Adaptiv_XML_Functions'/></DELIVERYDAY>
        <EXERCISESTYLE><acmCode method='ExerciseType'/></EXERCISESTYLE>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
        <OPTIONTYPE><acmCode function='GetOptType' file='Adaptiv_XML_Functions'/></OPTIONTYPE>
        <PUT>
            <AMOUNT><acmCode function='GetOptPutAmnt' file='Adaptiv_XML_Functions'/></AMOUNT>
            <CURRENCY><acmCode function='GetOptPutCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
        </PUT>
        <NAME><acmCode method='Name'/></NAME>
        <STRIKEPRICE><acmCode method='StrikePrice'/></STRIKEPRICE>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>            
    <TRADE acmLoop='Trade'>
        <BUYER><acmCode function='GetOptBuyer' file='Adaptiv_XML_Functions'/></BUYER>
        <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions'/></NOMINAL>
        <PREMIUM>
            <AMOUNT><acmCode function='GetTrdPremium' file='Adaptiv_XML_Functions'/></AMOUNT>
            <PAYDATE><acmCode function='GetTrdPremiumPayDate' file='Adaptiv_XML_Functions'/></PAYDATE>
        </PREMIUM>
        <SELLER><acmCode function='GetOptSeller' file='Adaptiv_XML_Functions'/></SELLER>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_MMDemat_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <EXP_DAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXP_DAY>
        <LEGS acmLoop='Legs'>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions'/></RATE>
        </LEGS>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>
    <TRADE acmLoop='Trade'>
        <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions'/></NOMINAL>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

'''
*******************************************************************************
Unused
*******************************************************************************
'''

xml_FXSwap_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
        <PAYLEG acmLoop = 'GetPayLeg' file='Adaptiv_XML_Functions'>
            <CASHFLOWS acmLoop='CashFlows'>
                <AMOUNT><acmCode function='GetCFProjConverted' file='Adaptiv_XML_Functions'/></AMOUNT>
                <BUYORSELL><acmCode function='GetCFBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
                <CURRENCY><acmCode function='GetCFCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
                <PAYDAY><acmCode function='GetCFPayDay' file='Adaptiv_XML_Functions'/></PAYDAY>
            </CASHFLOWS>
        </PAYLEG>
        <RECEIVELEG acmLoop = 'GetReceiveLeg' file='Adaptiv_XML_Functions'>
            <CASHFLOWS acmLoop='CashFlows'>
                <AMOUNT><acmCode function='GetCFProjConverted' file='Adaptiv_XML_Functions'/></AMOUNT>
                <BUYORSELL><acmCode function='GetCFBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
                <CURRENCY><acmCode function='GetCFCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
                <PAYDAY><acmCode function='GetCFPayDay' file='Adaptiv_XML_Functions'/></PAYDAY>
            </CASHFLOWS>
        </RECEIVELEG>
        <NAME><acmCode method='Name'/></NAME>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>            
    <TRADE acmLoop='Trade'>
        <COST><acmCode function='GetFXSwapCost' file='Adaptiv_XML_Functions'/></COST>
        <CURRENCY><acmCode function='GetFXSwapCostCurr' file='Adaptiv_XML_Functions'/></CURRENCY>
        <MARGIN><acmCode function='GetFXSwapMargin' file='Adaptiv_XML_Functions'/></MARGIN>
        <SWAPRATES acmLoop = 'GetFXSwapCFs' file='Adaptiv_XML_Functions'>
            <DATE><acmCode function='GetFXSwapCFsRateDate' file='Adaptiv_XML_Functions'/></DATE>
            <RATE><acmCode function='GetFXSwapCFsRate' file='Adaptiv_XML_Functions'/></RATE>
        </SWAPRATES>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
    </TRADE>
</MESSAGE>
'''

xml_Bond_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <DAYSBETWEEN><acmCode function='GetDaysBetween' file='Adaptiv_XML_Functions'/></DAYSBETWEEN>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
        <ISSUER><acmCode method='Issuer.Name'/></ISSUER>
        <LEGS acmLoop='Legs'>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions'/></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions'/></PAYOFFSET>
                <PAYOFFSETCALS>
                <PAYOFFSETCAL1 acmLoop='PayCalendar'><acmCode method='Name'/></PAYOFFSETCAL1>
                <PAYOFFSETCAL2 acmLoop='Pay2Calendar'><acmCode method='Name'/></PAYOFFSETCAL2>
                <PAYOFFSETCAL3 acmLoop='Pay3Calendar'><acmCode method='Name'/></PAYOFFSETCAL3>
                <PAYOFFSETCAL4 acmLoop='Pay4Calendar'><acmCode method='Name'/></PAYOFFSETCAL4>
                <PAYOFFSETCAL5 acmLoop='Pay5Calendar'><acmCode method='Name'/></PAYOFFSETCAL5>
            </PAYOFFSETCALS>
            <RATE><acmCode function='GetRate' file='Adaptiv_XML_Functions'/></RATE>
            <ROLLING><acmCode function='GetLegRollingFormatted' file='Adaptiv_XML_Functions'/></ROLLING>
        </LEGS>
        <NAME><acmCode method='Name'/></NAME>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function= 'GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions'/></NOMINAL>
        <PREMIUM>
            <AMOUNT><acmCode function='GetTrdPremium' file='Adaptiv_XML_Functions'/></AMOUNT>
            <PAYDATE><acmCode function='GetTrdPremiumPayDate' file='Adaptiv_XML_Functions'/></PAYDATE>
        </PREMIUM>
        <PRICE><acmCode method='Price'/></PRICE>
        <PRICECLEAN><acmCode function='GetBondCleanPrice' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></PRICECLEAN>
        <PRICEDIRTY><acmCode function='GetBondDirtyPrice' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></PRICEDIRTY>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
        <HANDLING_FEE><acmCode function='GetHandlingFee' file='Adaptiv_XML_Functions'/></HANDLING_FEE>
        <COMMISSION><acmCode function='GetCommission' file='Adaptiv_XML_Functions'/></COMMISSION>
    </TRADE>
</MESSAGE>
'''

xml_Bill_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <DAYSBETWEEN><acmCode function='GetDaysBetween' file='Adaptiv_XML_Functions'/></DAYSBETWEEN>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions'/></EXPDAY>
        <ISSUER><acmCode method='Issuer.Name'/></ISSUER>
        <LEGS acmLoop='Legs'>
            <CURRENCY><acmCode method='Currency.Name'/></CURRENCY>
            <DAYCOUNT><acmCode function='DayCountMethod' file='Adaptiv_XML_Functions'/></DAYCOUNT>
            <PAYOFFSET><acmCode function='PayDayMethod' file='Adaptiv_XML_Functions'/></PAYOFFSET>
                <PAYOFFSETCALS>
                <PAYOFFSETCAL1 acmLoop='PayCalendar'><acmCode method='Name'/></PAYOFFSETCAL1>
                <PAYOFFSETCAL2 acmLoop='Pay2Calendar'><acmCode method='Name'/></PAYOFFSETCAL2>
                <PAYOFFSETCAL3 acmLoop='Pay3Calendar'><acmCode method='Name'/></PAYOFFSETCAL3>
                <PAYOFFSETCAL4 acmLoop='Pay4Calendar'><acmCode method='Name'/></PAYOFFSETCAL4>
                <PAYOFFSETCAL5 acmLoop='Pay5Calendar'><acmCode method='Name'/></PAYOFFSETCAL5>
            </PAYOFFSETCALS>
        </LEGS>
        <NAME><acmCode method='Name'/></NAME>
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions'/></TYPE>
    </INSTRUMENT>           
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdBuyOrSell' file='Adaptiv_XML_Functions'/></BUYORSELL>
        <CURRENCY><acmCode method='Trade.Currency.Name'/></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominal' file='Adaptiv_XML_Functions'/></NOMINAL>
        <PREMIUM>
            <AMOUNT><acmCode function='GetTrdPremium' file='Adaptiv_XML_Functions'/></AMOUNT>
            <PAYDATE><acmCode function='GetTrdPremiumPayDate' file='Adaptiv_XML_Functions'/></PAYDATE>
        </PREMIUM>
        <PRICE><acmCode method='Trade.Price'/></PRICE>
        <PRICECLEAN><acmCode function='GetBondCleanPrice' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></PRICECLEAN>
        <TIME><acmCode method='TradeTime'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions'/></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid'/></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions'/></VALUEDAY>
        <HANDLING_FEE><acmCode function='GetHandlingFee' file='Adaptiv_XML_Functions'/></HANDLING_FEE>
        <COMMISSION><acmCode function='GetCommission' file='Adaptiv_XML_Functions'/></COMMISSION>
    </TRADE>
</MESSAGE>
'''

xml_FI_Generic_template = \
    Heading + '''<MESSAGE>''' + Confirmation + Acquirer + Counterparty + '''
    <INSTRUMENT acmLoop='Trade.Instrument'>
        <DAYSBETWEEN><acmCode function='GetDaysBetween' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></DAYSBETWEEN>
        <EXPDAY><acmCode function='GetInsExpiration' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></EXPDAY>
        <ISSUER><acmCode method='Issuer.Name' ignoreUpdate ='True' /></ISSUER>
        <NAME><acmCode method='Name'/></NAME>
        <PAYDAYS><acmCode function='GetAllCFPayDays' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></PAYDAYS>
        <RESETS acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
            <DAY><acmCode function='GetResetDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></DAY>
        </RESETS>
        <RATE_RESETS>
            <RESET acmLoop='GetResets' file = 'Adaptiv_XML_Functions'>
                <DATE><acmCode function='GetResetDay' file='Adaptiv_XML_Functions'/></DATE>
            </RESET>
        </RATE_RESETS>        
        <COUPONS>
            <COUPON acmLoop='GetCoupons' file = 'Adaptiv_XML_Functions'>
                <DATE><acmCode function='GetCashFlowPayDate' file='Adaptiv_XML_Functions'/></DATE>
            </COUPON>
        </COUPONS>              
        <TYPE><acmCode function='GetInsType' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></TYPE>
        <ISIN><acmCode function='GetIsin' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></ISIN>
    </INSTRUMENT>
    <TRADE acmLoop='Trade'>
        <BUYORSELL><acmCode function='GetTrdSalePurchaseIndicator' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></BUYORSELL>
        <CURRENCY><acmCode method='Trade.Currency.Name' ignoreUpdate ='True' /></CURRENCY>
        <NOMINAL><acmCode function='GetTrdNominalFormat' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></NOMINAL>
        <POSITION><acmCode function='GetTrdPos' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></POSITION>
        <PREMIUM>
            <AMOUNT><acmCode function='GetTrdPremiumFormat' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></AMOUNT>
            <PAYDATE><acmCode function='GetTrdPremiumPayDate' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></PAYDATE>
        </PREMIUM>
        <BUYER><acmCode function='GetOptBuyer' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></BUYER>
        <SELLER><acmCode function='GetOptSeller' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></SELLER>
        <TIME><acmCode method='TradeTime' ignoreUpdate ='True'/></TIME>
        <TRADECORRECTION><acmCode function= 'GetTradeCorrection' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></TRADECORRECTION>
        <TRDNUMBER><acmCode method='Oid' /></TRDNUMBER>
        <TRADEREFERENCENUMBER><acmCode function='GetTradeReferenceNumber' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBER>
        <TRADEREFERENCENUMBERLABEL><acmCode function='GetTradeReferenceNumberLabel' file='Adaptiv_XML_Functions'/></TRADEREFERENCENUMBERLABEL>
        <VALUEDAY><acmCode function='GetTrdValueDay' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></VALUEDAY>
        <TRADERBPID><acmCode function='GetTraderBPID' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></TRADERBPID>
        <INTEREST_RATE><acmCode function='GetInterestRate' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></INTEREST_RATE>
        <INTEREST_AMOUNT><acmCode function='GetInterestAmount' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></INTEREST_AMOUNT>
        <DEMAT_PAYMENT_FLAG><acmCode function='GetDematPaymentFlag' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></DEMAT_PAYMENT_FLAG>
        <DEMAT_RESET_FLAG><acmCode function='GetDematResetFlag' file='Adaptiv_XML_Functions' ignoreUpdate ='True' /></DEMAT_RESET_FLAG>
    </TRADE>
</MESSAGE>
'''
