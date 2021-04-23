""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_CommoditySwaption(trade):
    xml_CommoditySwaption_template = '''\
        <commoditySwaption>
            <buyOrSell><acmCode method = "Get_Trade_Buy_Or_Sell" file = 'ABSA_XML_Functions'/></buyOrSell>
            <fixedPriceLeg acmLoop = "Get_CommOption_Leg_Fixed" file = 'ABSA_XML_Functions'>
                <payOrReceive><acmCode method = "Get_Insrt_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                <effectiveDate>
                    <unadjustedDate><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </effectiveDate>
                <terminationDate>
                    <unadjustedDate><acmCode method = "Get_Leg_EndDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </terminationDate>
                <calculationPeriodsSchedule>
                    <periodMultiplier><acmCode method = "Get_SpotOffSet" file = 'ABSA_XML_Functions'/></periodMultiplier>
                    <period>D</period>
                    <rollConvention>
                        <id type = "bcRollConvention">Business Days</id>
                    </rollConvention>
                </calculationPeriodsSchedule>
                <fixedPrice>
                    <priceSchedule>
                        <initialValue><acmCode method = "Get_Trd_Price" file = 'ABSA_XML_Functions'/></initialValue>
                    </priceSchedule>
                    <currency>
                        <id type = "grdCurrency"><acmCode method = "Get_Trade_Currency" file = 'ABSA_XML_Functions'/></id>
                    </currency>
                    <unit>
                        <id type = "bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                </fixedPrice>
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
                    <amount><acmCode method = "Get_Trd_Nominal" file = 'ABSA_XML_Functions'/></amount>
                    <unit>
                        <id type = "bcPriceUnit"><acmCode method = 'Currency.Name'/></id>
                    </unit>
                </totalNotionalQuantity>
                <paymentDates>
                    <adjustableDates>
                        <unadjustedDate><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                        <dateAdjustments>
                            <businessDayConvention>FOLLOWING</businessDayConvention>
                            <businessCenters>
                                <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                                </businessCenter>
                            </businessCenters>
                        </dateAdjustments>
                    </adjustableDates>
                </paymentDates>
            </fixedPriceLeg>
            <floatingPriceLeg acmLoop = "Get_CommOption_Leg_Float" file = 'ABSA_XML_Functions'>
                <payOrReceive><acmCode method = "Get_Insrt_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                <effectiveDate>
                    <unadjustedDate><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </effectiveDate>
                <terminationDate>
                    <unadjustedDate><acmCode method = "Get_Leg_EndDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>FOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </terminationDate>
                <calculationPeriodsSchedule>
                    <periodMultiplier><acmCode method = "Get_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                    <period><acmCode method = "Get_Reset_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
                    <rollConvention>
                        <id type = "bcRollConvention"><acmCode method = "Get_Day_Count_Method_All" file = 'ABSA_XML_Functions'/></id>
                    </rollConvention>
                </calculationPeriodsSchedule>
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
                        <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                    </currency>
                    <publication>
                        <rateSource>
                            <id type = "bcInformationProvider">Reuters</id>
                        </rateSource>
                    </publication>
                </commodity>
                <notionalQuantity>
                    <quantity>
                        <initialValue><acmCode method = "Get_Trd_Nominal" file = 'ABSA_XML_Functions'/></initialValue>
                    </quantity>
                    <unit>
                        <id type = "bcPriceUnit"><acmCode method = 'Currency.Name'/></id>
                    </unit>
                    <frequency>Monthly</frequency>
                </notionalQuantity>
                <totalNotionalQuantity>
                    <amount><acmCode method = "Get_Trd_Nominal" file = 'ABSA_XML_Functions'/></amount>
                    <unit>
                        <id type = "bcPriceUnit"><acmCode method = 'Currency.Name'/></id>
                    </unit>
                </totalNotionalQuantity>
                <calculation>
                    <pricingDates>
                        <resetPeriod>
                            <periodMultiplier>1</periodMultiplier>
                            <period>D</period>
                        </resetPeriod>
                        <resetRollConvention>
                            <id type = "bcResetRollConvention">Month End</id>
                        </resetRollConvention>
                        <dayType>Business</dayType>
                        <dayDistribution>All</dayDistribution>
                    </pricingDates>
                </calculation>
                <relativePaymentDates>
                    <payRelativeTo>CalculationPeriodEndDate</payRelativeTo>
                    <paymentDaysOffset>
                        <periodMultiplier>2</periodMultiplier>
                        <period>D</period>
                    </paymentDaysOffset>
                    <paymentDatesAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                    </paymentDatesAdjustments>
                </relativePaymentDates>
            </floatingPriceLeg>
            <exercise>
                <exerciseStyle><acmCode method = "Get_Option_Exercise_Style" file = 'ABSA_XML_Functions'/></exerciseStyle>
                <europeanExercise acmLoop = "Is_Option_European_Exercise" file = 'ABSA_XML_Functions'>
                    <expirationDate>
                        <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                        <dateAdjustments>
                            <businessDayConvention>FOLLOWING</businessDayConvention>
                            <businessCenters>
                                <businessCenter acmLoop = "Get_Exercise_Calendar_ISDA" file = 'ABSA_XML_Functions'>
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
            <premium>
                <payOrReceive><acmCode method = "Get_Premium_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                <valueDate>
                    <unadjustedDate><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </valueDate>
                <paymentAmount>
                    <currency>
                        <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                    </currency>
                    <amount><acmCode method = "Get_Premium_Amount" file = 'ABSA_XML_Functions'/></amount>
                </paymentAmount>
            </premium>
        </commoditySwaption>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_CommoditySwaption_template, trade)
