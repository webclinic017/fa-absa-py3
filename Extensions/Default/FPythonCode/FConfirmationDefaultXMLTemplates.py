""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationDefaultXMLTemplates.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationDefaultXMLTemplates

DESCRIPTION
    This module is by default called from FConfirmationParametersTemplate.
    Changes to this module require a restart of both the
    Confirmation ATS and the Documentation ATS.
----------------------------------------------------------------------------"""


from FOperationsDocumentXML import FOperationsDocumentXML
import FConfirmationDefaultXMLHooks

document = '''\
<?xml version="1.0" encoding="ISO-8859-1"?>
<MESSAGE>
  <CONFIRMATION>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid'/></TRDNBR>
    <RedCode><acmCode method ='Trade.Counterparty.RedCode'/></RedCode>
  </CONFIRMATION>
  <TRADE>
    <TRDNBR><acmCode method ='Trade.Oid'/></TRDNBR>
    <BUYER><acmCode function ='GetBuyer' file ='FConfirmationDefaultXMLHooks'/></BUYER>
    <SELLER><acmCode function ='GetSeller' file ='FConfirmationDefaultXMLHooks'/></SELLER>
    <PREMIUM><acmCode method ='Trade.Premium'/></PREMIUM>
    <ACQUIRER_PTYNBR><acmCode method ='Trade.Acquirer.Oid'/></ACQUIRER_PTYNBR>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <BROKER><acmCode method = 'Trade.Broker.Name'/></BROKER>
  </TRADE>
  <INSTRUMENT>
    <INSTYPE><acmCode method ='Trade.Instrument.InsType'/></INSTYPE>
    <EXP_DAY><acmCode method ='Trade.Instrument.ExpiryDate'/></EXP_DAY>
  </INSTRUMENT>
  <acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
  </MESSAGE>
'''

documentConfirmationSWIFT = ''

documentConfirmationCancellationSWIFT = ''

capFloorOpen = '''\
<?xml version="1.0" ?><MESSAGE>
<CONFIRMATION>
    <capFloorOpen>capFloorOpen</capFloorOpen>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid' ignoreUpdate ='True'/></TRDNBR>
    <EVENT_CHLNBR><acmCode method = 'EventChlItem.Name'/></EVENT_CHLNBR>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TYPE><acmCode method ='Type' ignoreUpdate ='True'/></TYPE>
</CONFIRMATION>
<acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
<INSTRUMENT  acmLoop = "Trade.Instrument">
    <INSTYPE><acmCode method ='InsType'/></INSTYPE>
    <EXP_DAY><acmCode method ='ExpiryDate'/></EXP_DAY>
    <LEG acmLoop = "Legs">
        <STRIKE><acmCode method ='Strike'/></STRIKE>
        <SPREAD><acmCode method ='Spread'/></SPREAD>
    </LEG>
</INSTRUMENT>
<TRADE>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <NOMINAL_AMOUNT><acmCode function ='GetNominal' file ='FConfirmationDefaultXMLHooks'/></NOMINAL_AMOUNT>
    <ACQUIRE_DAY><acmCode method ='Trade.AcquireDay'/></ACQUIRE_DAY>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <PREMIUM><acmCode method ='Trade.Premium'/></PREMIUM>
    <QUANTITY><acmCode method ='Trade.Quantity'/></QUANTITY>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <COUNTERPARTY_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetCounterpartyBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetCounterpartyCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetCounterpartyAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </COUNTERPARTY_SSI>
    <ACQUIRER_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetAcquirerBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetAcquirerCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetAcquirerAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </ACQUIRER_SSI>
</TRADE>
</MESSAGE>
'''

cashOpen = '''\
<?xml version="1.0" ?><MESSAGE>
<CONFIRMATION>
    <cashOpen>cashOpen</cashOpen>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid' ignoreUpdate ='True'/></TRDNBR>
    <EVENT_CHLNBR><acmCode method = 'EventChlItem.Name'/></EVENT_CHLNBR>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TYPE><acmCode method ='Type' ignoreUpdate ='True'/></TYPE>
</CONFIRMATION>
<acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
<INSTRUMENT  acmLoop = "Trade.Instrument">
    <INSTYPE><acmCode method ='InsType'/></INSTYPE>
    <EXP_DAY><acmCode method ='ExpiryDate'/></EXP_DAY>
    <LEG acmLoop = "Legs">
        <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
    </LEG>
</INSTRUMENT>
<TRADE>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <NOMINAL_AMOUNT><acmCode function ='GetProjectedFixedAmount' file ='FConfirmationDefaultXMLHooks'/></NOMINAL_AMOUNT>
    <ACQUIRE_DAY><acmCode method ='Trade.AcquireDay'/></ACQUIRE_DAY>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <PREMIUM><acmCode method ='Trade.Premium'/></PREMIUM>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <PRICE><acmCode method ='Trade.Price'/></PRICE>
    <INTEREST_AT_MATURITY><acmCode function ='ProjectedForAllFlows' file ='FConfirmationDefaultXMLHooks'/></INTEREST_AT_MATURITY>
    <COUNTERPARTY_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetCounterpartyBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetCounterpartyCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetCounterpartyAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </COUNTERPARTY_SSI>
    <ACQUIRER_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetAcquirerBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetAcquirerCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetAcquirerAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </ACQUIRER_SSI>
</TRADE>
</MESSAGE>
'''


fxOpen = '''\
<?xml version="1.0" ?><MESSAGE>
<CONFIRMATION>
    <fxOpen>fxOpen</fxOpen>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid' ignoreUpdate ='True'/></TRDNBR>
    <EVENT_CHLNBR><acmCode method = 'EventChlItem.Name'/></EVENT_CHLNBR>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TYPE><acmCode method ='Type' ignoreUpdate ='True'/></TYPE>
</CONFIRMATION>
<acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
<INSTRUMENT>
    <INSTYPE><acmCode method ='Trade.Instrument.InsType'/></INSTYPE>
    <INSADDR><acmCode method ='Trade.Instrument.Name'/></INSADDR>
</INSTRUMENT>
<TRADE>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <NOMINAL_AMOUNT><acmCode function ='GetNominal' file ='FConfirmationDefaultXMLHooks'/></NOMINAL_AMOUNT>
    <ACQUIRE_DAY><acmCode method ='Trade.AcquireDay'/></ACQUIRE_DAY>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <PREMIUM><acmCode method ='Trade.Premium'/></PREMIUM>
    <QUANTITY><acmCode method ='Trade.Quantity'/></QUANTITY>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <ABS_PREMIUM><acmCode function ='ABSPremium' file ='FConfirmationDefaultXMLHooks'/></ABS_PREMIUM>
    <ABS_QUANTITY><acmCode function ='ABSQuantity' file ='FConfirmationDefaultXMLHooks'/></ABS_QUANTITY>
    <PRICE><acmCode method ='Trade.Price'/></PRICE>
    <INSADDR><acmCode method ='Trade.Instrument.Name'/></INSADDR>
    <COUNTERPARTY_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetCounterpartyBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetCounterpartyCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetCounterpartyAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </COUNTERPARTY_SSI>
    <ACQUIRER_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetAcquirerBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetAcquirerCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetAcquirerAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </ACQUIRER_SSI>
</TRADE>
</MESSAGE>
'''

rateFixing = '''\
<?xml version="1.0" ?><MESSAGE>
<CONFIRMATION>
    <rateFixing>rateFixing</rateFixing>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid' ignoreUpdate ='True'/></TRDNBR>
    <EVENT_CHLNBR><acmCode method = 'EventChlItem.Name'/></EVENT_CHLNBR>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TYPE><acmCode method ='Type' ignoreUpdate ='True'/></TYPE>
</CONFIRMATION>
<acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
<TRADE>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <NOMINAL_AMOUNT><acmCode function ='GetNominal' file ='FConfirmationDefaultXMLHooks'/></NOMINAL_AMOUNT>
    <ACQUIRE_DAY><acmCode method ='Trade.AcquireDay'/></ACQUIRE_DAY>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <INSADDR><acmCode method ='Trade.Instrument.Name'/></INSADDR>
</TRADE>
<INSTRUMENT>
    <EXP_DAY><acmCode method ='Trade.Instrument.ExpiryDate'/></EXP_DAY>
</INSTRUMENT>
<RATE_FIXING>
    <DAY><acmCode method ='Reset.Day'/></DAY>
    <VALUE><acmCode method ='Reset.FixingValue'/></VALUE>
    <SETTLEMENT_AMOUNT><acmCode function ='GetFloatRateSettlementAmount' file ='FConfirmationDefaultXMLHooks'/></SETTLEMENT_AMOUNT>
    <PAYDAY><acmCode function ='GetFloatRateSettlementPayDay' file ='FConfirmationDefaultXMLHooks'/></PAYDAY>
</RATE_FIXING>
</MESSAGE>
'''

IRSOpen = '''\
<?xml version="1.0" ?><MESSAGE>
<CONFIRMATION>
    <Swap>Swap</Swap>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid' ignoreUpdate ='True'/></TRDNBR>
    <EVENT_CHLNBR><acmCode method = 'EventChlItem.Name'/></EVENT_CHLNBR>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TYPE><acmCode method ='Type' ignoreUpdate ='True'/></TYPE>
</CONFIRMATION>
<acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
<INSTRUMENT  acmLoop = "Trade.Instrument">
    <INSTYPE><acmCode method ='InsType'/></INSTYPE>
    <EXP_DAY><acmCode method ='ExpiryDate'/></EXP_DAY>
    <FIXED_LEG acmLoop = "FixedLeg"  file ='FConfirmationDefaultXMLHooks'>
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <STRIKE><acmCode method ='Strike'/></STRIKE>
        <SPREAD><acmCode method ='Spread'/></SPREAD>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method = 'CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function = 'CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </FIXED_LEG>
    <FLOAT_LEG acmLoop = "FloatLeg"  file ='FConfirmationDefaultXMLHooks'>
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <STRIKE><acmCode method ='Strike'/></STRIKE>
        <SPREAD><acmCode method ='Spread'/></SPREAD>
        <FLOAT_RATE><acmCode method ='FloatRateReference.Name'/></FLOAT_RATE>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </FLOAT_LEG>
    <PAY_LEG acmLoop = "PayLeg">
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <CASHFLOW acmLoop = "CashFlows">
            <RESET>
                <DAY><acmCode function ='GetFirstResetDate' file ='FConfirmationDefaultXMLHooks'/></DAY>
            </RESET>
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </PAY_LEG>
    <RECEIVE_LEG acmLoop = "RecLeg">
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <AMORT_TYPE><acmCode method ='AmortType'/></AMORT_TYPE>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </RECEIVE_LEG>
</INSTRUMENT>
<TRADE>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <NOMINAL_AMOUNT><acmCode function ='GetNominal' file ='FConfirmationDefaultXMLHooks'/></NOMINAL_AMOUNT>
    <ACQUIRE_DAY><acmCode method ='Trade.AcquireDay'/></ACQUIRE_DAY>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <PREMIUM><acmCode method ='Trade.Premium'/></PREMIUM>
    <QUANTITY><acmCode method ='Trade.Quantity'/></QUANTITY>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <SELLER><acmCode function ='GetSeller' file ='FConfirmationDefaultXMLHooks'/></SELLER>
    <BUYER><acmCode function ='GetBuyer' file ='FConfirmationDefaultXMLHooks'/></BUYER>
    <COUNTERPARTY_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetCounterpartyBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetCounterpartyCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetCounterpartyAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </COUNTERPARTY_SSI>
    <ACQUIRER_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetAcquirerBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetAcquirerCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetAcquirerAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </ACQUIRER_SSI>
</TRADE>
</MESSAGE>
'''

TRSOpen = '''\
<?xml version="1.0" ?><MESSAGE>
<CONFIRMATION>
    <Swap>Swap</Swap>
    <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
    <TRDNBR><acmCode method ='Trade.Oid' ignoreUpdate ='True'/></TRDNBR>
    <EVENT_CHLNBR><acmCode method = 'EventChlItem.Name'/></EVENT_CHLNBR>
    <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
    <TYPE><acmCode method ='Type' ignoreUpdate ='True'/></TYPE>
</CONFIRMATION>
<acmTemplate function ='GetContact' file ='FConfirmationDefaultXMLTemplates'/>
<INSTRUMENT  acmLoop = "Trade.Instrument">
    <INSTYPE><acmCode method ='InsType'/></INSTYPE>
    <EXP_DAY><acmCode method ='ExpiryDate'/></EXP_DAY>
    <FIXED_LEG acmLoop = "FixedLegs"  file ='FConfirmationDefaultXMLHooks'>
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <STRIKE><acmCode method ='Strike'/></STRIKE>
        <SPREAD><acmCode method ='Spread'/></SPREAD>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </FIXED_LEG>
    <FLOAT_LEG acmLoop = "FloatLegs"  file ='FConfirmationDefaultXMLHooks'>
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <STRIKE><acmCode method ='Strike'/></STRIKE>
        <SPREAD><acmCode method ='Spread'/></SPREAD>
        <FLOAT_RATE><acmCode method ='FloatRateReference.Name'/></FLOAT_RATE>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </FLOAT_LEG>
    <PAY_LEG acmLoop = "PayLegs" file ='FConfirmationDefaultXMLHooks'>
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <CASHFLOW acmLoop = "CashFlows">
            <RESET>
                <DAY><acmCode function ='GetFirstResetDate' file ='FConfirmationDefaultXMLHooks'/></DAY>
            </RESET>
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </PAY_LEG>
    <RECEIVE_LEG acmLoop = "RecLegs" file ='FConfirmationDefaultXMLHooks'>
        <TYPE><acmCode method ='LegType'/></TYPE>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
        <DAYCOUNT_METHOD><acmCode method ='DayCountMethod'/></DAYCOUNT_METHOD>
        <AMORT_TYPE><acmCode method ='AmortType'/></AMORT_TYPE>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DAY><acmCode function ='EndDateCashflow' file ='FConfirmationDefaultXMLHooks'/></END_DAY>
            <PAY_DAY><acmCode function ='PayDateCashflow' file ='FConfirmationDefaultXMLHooks'/></PAY_DAY>
            <START_DAY><acmCode function ='StartDateCashflow' file ='FConfirmationDefaultXMLHooks'/></START_DAY>
            <CF_AMOUNT><acmCode function ='CfAmount' file ='FConfirmationDefaultXMLHooks'/></CF_AMOUNT>
            <CF_PERIOD><acmCode function ='CfPeriod' file ='FConfirmationDefaultXMLHooks'/></CF_PERIOD>
            <CF_TYPE><acmCode method ='CashFlowType'/></CF_TYPE>
            <CF_CURR><acmCode function ='CfCurr' file ='FConfirmationDefaultXMLHooks'/></CF_CURR>
            <CF_NOMINAL><acmCode function ='CfNominal' file ='FConfirmationDefaultXMLHooks'/></CF_NOMINAL>
        </CASHFLOW>
    </RECEIVE_LEG>
</INSTRUMENT>
<TRADE>
    <CURR><acmCode method ='Trade.Currency.Name'/></CURR>
    <NOMINAL_AMOUNT><acmCode function ='GetNominal' file ='FConfirmationDefaultXMLHooks'/></NOMINAL_AMOUNT>
    <ACQUIRE_DAY><acmCode method ='Trade.AcquireDay'/></ACQUIRE_DAY>
    <VALUE_DAY><acmCode method ='Trade.ValueDay'/></VALUE_DAY>
    <PREMIUM><acmCode method ='Trade.Premium'/></PREMIUM>
    <QUANTITY><acmCode method ='Trade.Quantity'/></QUANTITY>
    <TIME><acmCode method ='Trade.TradeTime'/></TIME>
    <SELLER><acmCode function ='GetSeller' file ='FConfirmationDefaultXMLHooks'/></SELLER>
    <BUYER><acmCode function ='GetBuyer' file ='FConfirmationDefaultXMLHooks'/></BUYER>
    <COUNTERPARTY_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetCounterpartyBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetCounterpartyCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetCounterpartyAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </COUNTERPARTY_SSI>
    <ACQUIRER_SSI>
        <CASH_ACCOUNT>
            <BIC_SEQNBR><acmCode function ='GetAcquirerBICForValueDay' file ='FConfirmationDefaultXMLHooks'/></BIC_SEQNBR>
            <CORRESPONDENT_BANK_PTYNBR><acmCode function ='GetAcquirerCorrespondentBankForValueDay' file ='FConfirmationDefaultXMLHooks'/></CORRESPONDENT_BANK_PTYNBR>
            <ACCOUNT><acmCode function ='GetAcquirerAccountForValueDay' file ='FConfirmationDefaultXMLHooks'/></ACCOUNT>
        </CASH_ACCOUNT>
    </ACQUIRER_SSI>
</TRADE>
</MESSAGE>
'''



def GetContact():
    contact_template = '''
<CONTACT acmLoop = "GetContactCounterparty"  file ='FConfirmationDefaultXMLHooks'>
    <PTYID><acmCode method ='Name'/></PTYID>
    <PTYNBR><acmCode method ='Oid'/></PTYNBR>
    <CITY><acmCode method ='City' /></CITY>
    <ADDRESS><acmCode method ='Address' /></ADDRESS>
    <ADDRESS2><acmCode method ='Address2'/></ADDRESS2>
    <ZIPCODE><acmCode method ='Zipcode'/></ZIPCODE>
    <COUNTRY><acmCode method ='Country'/></COUNTRY>
    <TELEPHONE><acmCode method ='Telephone'/></TELEPHONE>
    <FAX><acmCode method ='Fax'/></FAX>
    <EMAIL><acmCode method ='Email'/></EMAIL>
    </CONTACT>
    '''
    return contact_template

