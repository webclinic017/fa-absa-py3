""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_CommodityOption(trade):
    xml_CommodityOption_template = '''\
        <commodityOption>
            <buyOrSell><acmCode method = "Get_Premium_BuyOrSell" file = 'ABSA_XML_Functions'/></buyOrSell>
            <effectiveDate>
                <unadjustedDate><acmCode method = "Get_Trade_Create_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention>MODFOLLOWING</businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </effectiveDate>
            <terminationDate>
                <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention>MODFOLLOWING</businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </terminationDate>
            <calculationPeriodsSchedule>
                <periodMultiplier>1</periodMultiplier>
                <period>Y</period>
                <rollConvention>
                    <id type = "bcRollConvention">Term</id>
                </rollConvention>
            </calculationPeriodsSchedule>
            <underlying>
                <payOrReceive><acmCode method = "Get_Premium_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                <commodity>
                    <commodityType>
                        <id type="abcapFrontarenaIndexGroup"><acmCode method = "Get_Und_Comm_Type" file = 'ABSA_XML_Functions'/></id>
                        <alternateId type="abcapFrontarenaIndexGroup"><acmCode method = "Get_Und_Comm_Name" file = 'ABSA_XML_Functions'/></alternateId>
                    </commodityType>
                    <product>
                        <id type="assetControlInstrumentId">CommodityOption</id>
                    </product>
                    <unit>
                        <id type="bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                    <currency>
                        <id type = "grdCurrency"><acmCode method = 'Instrument.Currency.Name'/></id>
                    </currency>
                    <publication>
                        <rateSource>
                            <id type="bcInformationProvider">Reuters</id>
                        </rateSource>
                    </publication>
                </commodity>
                <notionalQuantity>
                    <quantity>
                        <initialValue><acmCode method = "Get_Trade_Quantity" file = 'ABSA_XML_Functions'/></initialValue>
                    </quantity>
                    <unit>
                        <id type="bcQuantityUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                    <frequency>Contract</frequency>
                </notionalQuantity>
                <totalNotionalQuantity>
                    <amount><acmCode method = "Get_Barcap_BTB" file = 'ABSA_XML_Functions'/></amount>
                    <unit>
                        <id type="bcQuantityUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                </totalNotionalQuantity>
                <calculation>
                    <pricingDates>
                        <resetPeriod>
                            <periodMultiplier>1</periodMultiplier>
                            <period>T</period>
                        </resetPeriod>
                        <dayType>Business</dayType>
                        <dayOfWeek><acmCode method = "Get_Ins_Expiration_DayOfWeek" file = 'ABSA_XML_Functions'/></dayOfWeek>
                    </pricingDates>
                </calculation>
            </underlying>
            <putOrCall><acmCode method = "CallOrPut" file = 'ABSA_XML_Functions'/></putOrCall>
            <exercise>
                <exerciseStyle><acmCode method = "Get_Option_Exercise_Style" file = 'ABSA_XML_Functions'/></exerciseStyle>
                <europeanExercise acmLoop = "Is_Option_European_Exercise" file = 'ABSA_XML_Functions'>
                    <expirationDate>
                        <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                        <dateAdjustments>
                            <businessDayConvention>MODFOLLOWING</businessDayConvention>
                            <businessCenters>
                                <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </businessCenters>
                        </dateAdjustments>
                    </expirationDate>
                    <expirationTime>
                        <hourMinuteTime><acmCode method = "Get_Expiration_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                        <businessCenter>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </expirationTime>
                    <earliestExerciseTime>
                        <hourMinuteTime><acmCode method = "Get_Earliest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                        <businessCenter>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </earliestExerciseTime>
                </europeanExercise>
            </exercise>
            <strikePrice>
                <priceSchedule>
                    <initialValue><acmCode method = "Get_Ins_StrikePrice" file = 'ABSA_XML_Functions'/></initialValue>
                </priceSchedule>
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Instrument.Currency.Name'/></id>
                </currency>
                <unit>
                    <id type="bcPriceUnit">Currency</id>
                </unit>
            </strikePrice>
            <cashSettlement>
                <settlementCurrency>
                    <id type = "grdCurrency"><acmCode method = 'Instrument.Currency.Name'/></id>
                </settlementCurrency>
            </cashSettlement>
            <relativePaymentDates>
                <payRelativeTo>CalculationPeriodEndDate</payRelativeTo>
                <paymentDaysOffset>
                    <periodMultiplier><acmCode method = "Get_Ins_SettleDays" file = 'ABSA_XML_Functions'/></periodMultiplier>
                    <period>D</period>
                </paymentDaysOffset>
                <paymentDatesAdjustments>
                    <businessDayConvention>MODFOLLOWING</businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </paymentDatesAdjustments>
            </relativePaymentDates>
            <premium>
                <payOrReceive><acmCode method = "Get_Premium_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                <relativeValueDate>
                    <payRelativeTo>CalculationPeriodEndDate</payRelativeTo>
                    <paymentDaysOffset>
                        <periodMultiplier><acmCode method = "Get_Ins_SettleDays" file = 'ABSA_XML_Functions'/></periodMultiplier>
                        <period>D</period>
                    </paymentDaysOffset>
                    <paymentDatesAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                    </paymentDatesAdjustments>
                </relativeValueDate>                
                <paymentAmount>
                    <currency>
                        <id type = "grdCurrency"><acmCode method = 'Trade.Currency.Name'/></id>
                    </currency>
                    <amount><acmCode method = "Get_Premium_Amount" file = 'ABSA_XML_Functions'/></amount>
                </paymentAmount>
            </premium>
        </commodityOption>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_CommodityOption_template, trade)
