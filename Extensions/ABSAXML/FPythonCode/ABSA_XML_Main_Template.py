""" Compiled: NONE NONE """

IRSOpen = '''\
<?xml version="1.0" encoding="ISO-8859-1"?>
<BCTrade xmlns="http://uri.barcapint.com/BarCapML"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://uri.barcapint.com/BarCapML ../../Schema/barcapml-trade-msg.xsd">
    <header>
        <version edition="3" major="10" minor="0" branchNumber="12" branchMajor="1" branchMinor="0" revision="0" name="absa_dev" build="1">4.11.0_2.0.1_absa_1</version>
    </header>
    <event>
        <eventName><acmCode method = "Get_Event_Name" file = 'ABSA_XML_Functions'/></eventName>
        <eventReason acmLoop = "Get_Event_Reason" file = 'ABSA_XML_Functions'><acmCode method = "Get_Event_Reason_Value" file = 'ABSA_XML_Functions'/></eventReason>
        <eventId>
            <id type = "abcapFrontarenaEventId"><acmCode method = "Get_OperationsDocument" file = 'ABSA_XML_Functions'/></id>
        </eventId>
        <date><acmCode method = "Get_Confirmation_Create_Date" file = 'ABSA_XML_Functions'/></date>
        <time><acmCode method = "Get_Confirmation_Create_Time" file = 'ABSA_XML_Functions'/></time>
        <effectiveDate><acmCode method = "Get_Confirmation_Create_Date" file = 'ABSA_XML_Functions'/></effectiveDate>
        <effectiveTime><acmCode method = "Get_Confirmation_Create_Time" file = 'ABSA_XML_Functions'/></effectiveTime>
        <verificationStatus>Verified</verificationStatus>
        <partialTerminationDetails acmLoop = "Is_PartialTermination" file = 'ABSA_XML_Functions'>
            <decreaseInNotionalAmount acmLoop = "Get_Legs_Conf" file = 'ABSA_XML_Functions'>
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                </currency>
                <amount><acmCode method = "Get_partialTerminationAmount" file = 'ABSA_XML_Functions'/></amount>
            </decreaseInNotionalAmount>
        </partialTerminationDetails>
        <frontOfficeReviewRequired><acmCode method = "Get_Sales_Conf_Approve" file = 'ABSA_XML_Functions'/></frontOfficeReviewRequired>
        <initiatingUserId>
            <id type = "absaUsername"><acmCode method = 'Trade.UpdateUser.Name'/></id>
        </initiatingUserId>
    </event>
    <trade acmLoop = "Trade">
        <tradeHeader>
            <tradeId>
                <id type = "abcapFrontarenaTradeId" version = "#FA#get_TRXnbr"><acmCode method = 'Oid'/></id>
            </tradeId>
            <relatedTrade acmLoop = "Is_Related_Trade" file = 'ABSA_XML_Functions'>
                <role>
                    <id type = "bcRelatedTradeRole">Creator</id>
                </role>
                <tradeId>
                    <id type = "abcapFrontarenaTradeId"><acmCode method = "Get_Related_Trade" file = 'ABSA_XML_Functions'/></id>
                </tradeId>
            </relatedTrade>
            <legalEntity>
                <partyId>
                    <id type = "sdsCounterpartyId"><acmCode eval = 'Acquirer().AdditionalInfo().BarCap_SMS_LE_SDSID()'/></id>
                </partyId>
            </legalEntity>
            <counterParty>
                <partyId>
                    <id type = "sdsCounterpartyId"><acmCode method = "Get_ConfInstr_CP_SDSID" file = 'ABSA_XML_Functions'/></id>
                </partyId>
            </counterParty>
            <tradeDate><acmCode method = "Get_Trade_Create_Date" file = 'ABSA_XML_Functions'/></tradeDate>
            <tradeTime><acmCode method = "Get_Trade_Create_Time" file = 'ABSA_XML_Functions'/></tradeTime>
            <foTradeState><acmCode method = "Get_Trade_Status" file = 'ABSA_XML_Functions'/></foTradeState>
            <closedTradeDetails acmLoop = "Is_Closed_Trade_Details" file = 'ABSA_XML_Functions'>
                <fullTerminationEffectiveDate acmLoop = "Is_Full_Termination" file = 'ABSA_XML_Functions'><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></fullTerminationEffectiveDate>
                <fullNovationOutEffectiveDate acmLoop = "Is_Full_Novation_Out" file = 'ABSA_XML_Functions'><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></fullNovationOutEffectiveDate>
                <allowFinalPeriodPayment>false</allowFinalPeriodPayment>
            </closedTradeDetails>
            <traderId>
                <id type = "absaUsername"><acmCode method = 'Trader.Name'/></id>
            </traderId>
            <tradingDesk>
                <id type = "abcapFrontarenaTradingDesk"><acmCode method = 'Acquirer.Name'/></id>
            </tradingDesk>
            <tradeLocation>
                <id type = "fpmlBusinessCenter">ZAJO</id>
            </tradeLocation>
            <salesPersonId acmLoop = "Is_SalesPersonID" file = 'ABSA_XML_Functions'>
                <id type = "absaUsername"><acmCode method = "Get_Is_SalesPersonID" file = 'ABSA_XML_Functions'/></id>
            </salesPersonId>
            <book>
                <id type = "abcapFrontarenaBook"><acmCode method = 'Portfolio.Name'/></id>
            </book>
        </tradeHeader>
        <productType>
            <mainType>
                <id type = "bcProductMainType"><acmCode method = "Get_Product_Type" file = 'ABSA_XML_Functions'/></id>
            </mainType>
            <subType>
                <id type = "bcProductSubType"><acmCode method = "Get_Product_Subtype" file = 'ABSA_XML_Functions'/></id>
            </subType>
        </productType>
        <customisedProduct>false</customisedProduct>
        <acmCode method = "Get_Product_XML" file = 'ABSA_XML_Functions' dataFormat = 'XML'/>
        <payment acmLoop = "Is_Premium_On_Trade" file = 'ABSA_XML_Functions'>
            <payOrReceive><acmCode method = "Get_Premium_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
            <otherParty>
                <partyId>
                    <id type = "sdsCounterpartyId"><acmCode eval = 'Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID()'/></id>
                </partyId>
            </otherParty>
            <paymentAmount>
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                </currency>
                <amount><acmCode method = "Get_Premium_Amount" file = 'ABSA_XML_Functions'/></amount>
            </paymentAmount>
            <valueDate>
                <unadjustedDate><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention><acmCode method = "Get_Pay_Day_Method_Trade" file = 'ABSA_XML_Functions'/></businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar_Payment" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </valueDate>
            <paymentType>
                <id type = "bcPaymentType"><acmCode method = "Get_Premium_Type" file = 'ABSA_XML_Functions'/></id>
            </paymentType>
        </payment>
        <payment acmLoop = "Get_Premium_Payments" file = 'ABSA_XML_Functions'>
            <payOrReceive><acmCode method = "Get_Payment_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
            <otherParty>
                <partyId>
                    <id type = "sdsCounterpartyId"><acmCode eval = 'Party().AdditionalInfo().BarCap_SMS_LE_SDSID()'/></id>
                </partyId>
            </otherParty>
            <paymentAmount>
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                </currency>
                <amount><acmCode method = "Get_Payment_Amount" file = 'ABSA_XML_Functions'/></amount>
            </paymentAmount>
            <valueDate>
                <unadjustedDate><acmCode method = "Get_Payment_PayDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention><acmCode method = "Get_Pay_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar_Payment" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </valueDate>
            <paymentType>
                <id type = "bcPaymentType"><acmCode method = "Get_Payment_Type" file = 'ABSA_XML_Functions'/></id>
            </paymentType>
        </payment>
    </trade>
</BCTrade>
'''



