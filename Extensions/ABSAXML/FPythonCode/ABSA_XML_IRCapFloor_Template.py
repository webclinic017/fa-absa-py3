""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_IRCapFloor(trade):
    xml_irCapFloor_template = '''\
        <irCapFloor>
                <capFloorStream acmLoop = "GetLegs" file = 'ABSA_XML_Functions'>
                    <payOrReceive><acmCode method = "Get_Insrt_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                    <calculationPeriodDates>
                        <effectiveDate>
                            <unadjustedDate><acmCode method = "Get_CapFloor_EffectiveDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                            <dateAdjustments>
                                <businessDayConvention><acmCode method = "Get_Leg_PayDayMethod" file = 'ABSA_XML_Functions'/></businessDayConvention>
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
                                <businessDayConvention><acmCode method = "Get_Leg_PayDayMethod" file = 'ABSA_XML_Functions'/></businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                    </businessCenter>
                                </businessCenters>
                            </dateAdjustments>
                        </terminationDate>
                        <calculationPeriodDatesAdjustments>
                            <businessDayConvention><acmCode method = "Get_Leg_PayDayMethod" file = 'ABSA_XML_Functions'/></businessDayConvention>
                            <businessCenters>
                                <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </businessCenters>
                        </calculationPeriodDatesAdjustments>
                        <stubPeriodDetails acmLoop = "Get_Stub_Period_Object" file = 'ABSA_XML_Functions'>
                            <stubPeriodType><acmCode method = "Get_Stub_Period_Type" file = 'ABSA_XML_Functions'/></stubPeriodType>
                        </stubPeriodDetails>
                        <calculationPeriodFrequency>
                            <periodMultiplier><acmCode method = "Get_Reset_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                            <period><acmCode method = "Get_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
                            <rollConvention><acmCode method = "Get_Rolling_Day" file = 'ABSA_XML_Functions'/></rollConvention>
                        </calculationPeriodFrequency>
                    </calculationPeriodDates>
                    <paymentDates>
                        <paymentFrequency>
                            <periodMultiplier><acmCode method = "Get_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                            <period><acmCode method = "Get_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
                        </paymentFrequency>
                        <payRelativeTo><acmCode method = "Get_Pay_Relative_To" file = 'ABSA_XML_Functions'/></payRelativeTo>
                        <paymentDaysOffset>
                            <periodMultiplier><acmCode method = "Get_Pay_Offset_Count" file = 'ABSA_XML_Functions'/></periodMultiplier>
                            <period><acmCode method = "Get_Pay_Offset_Unit" file = 'ABSA_XML_Functions'/></period>
                            <dayType>Business</dayType>
                        </paymentDaysOffset>
                        <paymentDatesAdjustments>
                            <businessDayConvention><acmCode method = "Get_Leg_PayDayMethod" file = 'ABSA_XML_Functions'/></businessDayConvention>
                            <businessCenters>
                                <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </businessCenters>
                        </paymentDatesAdjustments>
                    </paymentDates>
                    <resetDetails>
                        <resetDates>
                            <resetRelativeTo>CalculationPeriodStartDate</resetRelativeTo>
                            <initialFixingDate>
                                <periodMultiplier><acmCode method = "Get_Reset_Day_Offset" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                <period>D</period>
                                <businessDayConvention><acmCode method = "Get_Reset_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Reset_Calendar" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                    </businessCenter>
                                </businessCenters>
                                <dateRelativeTo>ResetDates</dateRelativeTo>
                            </initialFixingDate>
                            <fixingDates>
                                <periodMultiplier><acmCode method = "Get_Reset_Day_Offset" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                <period>D</period>
                                <businessDayConvention><acmCode method = "Get_Reset_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Reset_Calendar" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                    </businessCenter>
                                </businessCenters>
                                <dateRelativeTo>ResetDates</dateRelativeTo>
                            </fixingDates>
                            <resetFrequency>
                                <periodMultiplier><acmCode method = "Get_Reset_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                <period><acmCode method = "Get_Reset_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
                                <rollConvention><acmCode method = "Get_Rolling_Day" file = 'ABSA_XML_Functions'/></rollConvention>
                            </resetFrequency>
                            <resetDatesAdjustments>
                                <businessDayConvention><acmCode method = "Get_Reset_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Reset_Calendar" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                    </businessCenter>
                                </businessCenters>
                            </resetDatesAdjustments>
                        </resetDates>
                        <resetSourceSystem>AbcapFrontArena</resetSourceSystem>
                        <resetMethod>Automatic</resetMethod>
                        <resetInStub><acmCode method = "Is_Reset_In_Stub" file = 'ABSA_XML_Functions'/></resetInStub>
                    </resetDetails>
                    <calculationPeriodAmount>
                        <calculation>
                            <notional acmLoop = "Is_Non_Amortising" file = 'ABSA_XML_Functions'>
                                <currency>
                                    <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                                </currency>
                                <amount><acmCode method = "Get_First_CF_Nominal" file = 'ABSA_XML_Functions'/></amount>
                            </notional>
                            <notionalSchedule acmLoop = "Is_Amortising" file = 'ABSA_XML_Functions'>
                                <notionalStepSchedule>
                                    <initialValue><acmCode method = "Get_First_CF_Nominal" file = 'ABSA_XML_Functions'/></initialValue>
                                    <step acmLoop = "Get_All_Fixed_Amount" file = 'ABSA_XML_Functions'>
                                        <stepDate><acmCode method = "Get_CF_PayDate" file = 'ABSA_XML_Functions'/></stepDate>
                                        <stepValue><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></stepValue>
                                    </step>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                                    </currency>
                                </notionalStepSchedule>
                            </notionalSchedule>
                            <floatingRateCalculation>
                                <floatingRateIndex>
                                    <id type = "bcFloatingRateIndex"><acmCode method = 'FloatRateReference.FreeText'/></id>
                                </floatingRateIndex>
                                <indexTenor>
                                    <periodMultiplier><acmCode method = "Get_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                    <period><acmCode method = "Get_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
                                </indexTenor>
                                <spreadSchedule>
                                    <initialValue><acmCode method = 'Spread'/></initialValue>
                                </spreadSchedule>
                                <capRateSchedule acmLoop = "Is_Cap" file = 'ABSA_XML_Functions'>
                                    <initialValue><acmCode method = "Convert_Strike" file = 'ABSA_XML_Functions'/></initialValue>
                                    <buyOrSell><acmCode method = "Get_Buy_Or_Sell" file = 'ABSA_XML_Functions'/></buyOrSell>
                                </capRateSchedule>
                                <floorRateSchedule acmLoop = "Is_Floor" file = 'ABSA_XML_Functions'>
                                    <initialValue><acmCode method = "Convert_Strike" file = 'ABSA_XML_Functions'/></initialValue>
                                    <buyOrSell><acmCode method = "Get_Buy_Or_Sell" file = 'ABSA_XML_Functions'/></buyOrSell>
                                </floorRateSchedule>
                                <initialRate acmLoop = "Is_Initial_Rate" file = 'ABSA_XML_Functions'><acmCode method = "Convert_Reset_Rate" file = 'ABSA_XML_Functions'/></initialRate>
                                <finalRateRounding>
                                    <roundingDirection>Nearest</roundingDirection>
                                    <precision><acmCode method = 'Decimals'/></precision>
                                </finalRateRounding>
                                <averaging acmLoop = "Is_Averaging" file = 'ABSA_XML_Functions'>
                                    <averagingMethodology>
                                        <id type= "bcAveragingMethodology"><acmCode method = "Get_AveragingMethodology" file = 'ABSA_XML_Functions'/></id>
                                    </averagingMethodology>
                                    <averagingFrequency>D</averagingFrequency>
                                    <averagingCutOff>
                                        <averagingCutOffPeriod>
                                            <periodMultiplier>1</periodMultiplier>
                                            <period>D</period>
                                            <dayType>Business</dayType>
                                        </averagingCutOffPeriod>
                                        <daysGap>
                                            <periodMultiplier>0</periodMultiplier>
                                            <period>D</period>
                                        </daysGap>
                                    </averagingCutOff>
                                    <averagingDatesAdjustments>
                                        <businessDayConvention><acmCode method = "Get_Reset_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                                        <businessCenters>
                                            <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                            </businessCenter>
                                        </businessCenters>
                                    </averagingDatesAdjustments>
                                    <averagingRollConvention>1</averagingRollConvention>
                                    <averagingCompoundingApplicable>false</averagingCompoundingApplicable>
                                </averaging>
                            </floatingRateCalculation>
                            <dayCountFraction>
                                <id type = "bcDayCountFraction"><acmCode method = "Get_Day_Count_Method" file = 'ABSA_XML_Functions'/></id>
                            </dayCountFraction>
                            <compoundingMethod>
                                <id type = "bcCompoundingMethod"><acmCode method = "Get_CompoundingMethod" file = 'ABSA_XML_Functions'/></id>
                            </compoundingMethod>
                            <discounting acmLoop = "Get_FRA_Discounting"  file = 'ABSA_XML_Functions'>
                                <discountingType>FRA</discountingType>
                            </discounting>
                        </calculation>
                    </calculationPeriodAmount>
                    <cashflows>
                        <cashflowsMatchParameters>false</cashflowsMatchParameters>
                        <paymentCalculationPeriod acmLoop = "Get_PaymentCalculationPeriod" file = 'ABSA_XML_Functions'>
                            <adjustedValueDate acmLoop = "Is_AdjustedValueDate" file = 'ABSA_XML_Functions'><acmCode method = "Get_AdjustedValueDate" file = 'ABSA_XML_Functions'/></adjustedValueDate>
                            <calculationPeriod>
                                <status><acmCode method = "Get_CashFlow_Status_Object" file = 'ABSA_XML_Functions'/></status>
                                <adjustedAccrualStartDate><acmCode method = "Get_CF_Reset_StartDate" file = 'ABSA_XML_Functions'/></adjustedAccrualStartDate>
                                <adjustedAccrualEndDate><acmCode method = "Get_CF_Reset_EndDate" file = 'ABSA_XML_Functions'/></adjustedAccrualEndDate>
                                <notionalAmount>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'Leg.Currency.Name'/></id>
                                    </currency>
                                    <amount><acmCode method = "Get_CF_Nominal" file = 'ABSA_XML_Functions'/></amount>
                                </notionalAmount>
                                <fixedRate><acmCode method = "Convert_Strike_CF_Object" file = 'ABSA_XML_Functions'/></fixedRate>
                                <calculationPeriodAmount>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'Leg.Currency.Name'/></id>
                                    </currency>
                                    <amount><acmCode method = "Get_CF_Nominal" file = 'ABSA_XML_Functions'/></amount>
                                </calculationPeriodAmount>
                                <compoundingCashflow><acmCode method = "Is_Compounding_CF_Object_Value" file = 'ABSA_XML_Functions'/></compoundingCashflow>
                            </calculationPeriod>
                        </paymentCalculationPeriod>
                    </cashflows>
                </capFloorStream>
                <earlyTerminationProvision acmLoop = "Is_Early_Termination" file = 'ABSA_XML_Functions'>
                    <optionalEarlyTermination>
                        <exerciseRightHolder>Both</exerciseRightHolder>
                        <exerciseStyle><acmCode method = "Get_Exercise_Style" file = 'ABSA_XML_Functions'/></exerciseStyle>
                        <bermudaExercise acmLoop = "Is_Bermuda_Exercise" file = 'ABSA_XML_Functions'>
                            <bermudaExerciseDates>
                                <adjustableDates>
                                    <unadjustedDate acmLoop = "Get_Bermuda_Unadjusted_Dates" file = 'ABSA_XML_Functions'><acmCode method = 'First'/></unadjustedDate>
                                    <dateAdjustments>
                                        <businessDayConvention>FOLLOWING</businessDayConvention>
                                        <businessCenters>
                                            <businessCenter acmLoop = "Get_Calendar_Trade_London" file = 'ABSA_XML_Functions'>
                                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                            </businessCenter>
                                        </businessCenters>
                                    </dateAdjustments>
                                </adjustableDates>
                                <relativeDate>
                                    <periodMultiplier>5</periodMultiplier>
                                    <period>D</period>
                                    <businessDayConvention>FOLLOWING</businessDayConvention>
                                    <businessCenters>
                                        <businessCenter acmLoop = "Get_Calendar_Trade_London" file = 'ABSA_XML_Functions'>
                                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                        </businessCenter>
                                    </businessCenters>
                                    <dateRelativeTo>BermudaOptionExerciseDate</dateRelativeTo>
                                </relativeDate>
                                <exerciseFrequency>
                                    <periodMultiplier>1</periodMultiplier>
                                    <period>Y</period>
                                </exerciseFrequency>
                            </bermudaExerciseDates>
                            <earliestExerciseTime>
                                <hourMinuteTime><acmCode eval = 'Instrument().Currency().AdditionalInfo().EarliestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </earliestExerciseTime>
                            <latestExerciseTime>
                                <hourMinuteTime><acmCode eval = 'Instrument().Currency().AdditionalInfo().LatestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </latestExerciseTime>
                            <expirationTime>
                                <hourMinuteTime><acmCode eval = 'Instrument().Currency().AdditionalInfo().LatestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </expirationTime>
                        </bermudaExercise>
                        <europeanExercise acmLoop = "Is_European_Exercise" file = 'ABSA_XML_Functions'>
                            <expirationDate>
                                <relativeDate>
                                    <periodMultiplier>5</periodMultiplier>
                                    <period>D</period>
                                    <businessDayConvention>FOLLOWING</businessDayConvention>
                                    <businessCenters>
                                        <businessCenter acmLoop = "Get_Calendar_Trade_London" file = 'ABSA_XML_Functions'>
                                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                        </businessCenter>
                                    </businessCenters>
                                    <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                                </relativeDate>
                            </expirationDate>
                            <expirationTime>
                                <hourMinuteTime><acmCode eval = 'Instrument().Currency().AdditionalInfo().LatestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </expirationTime>
                            <earliestExerciseTime>
                                <hourMinuteTime><acmCode eval = 'Instrument().Currency().AdditionalInfo().EarliestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </earliestExerciseTime>
                        </europeanExercise>
                        <settlementType>Cash</settlementType>
                        <cashSettlement>
                            <cashSettlementValuationTime>
                                <hourMinuteTime><acmCode eval = 'Instrument().Currency().AdditionalInfo().LatestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </cashSettlementValuationTime>
                            <cashSettlementValuationDate>
                                <periodMultiplier><acmCode method = "Get_Cashsettlement_Period" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                <period>D</period>
                                <businessDayConvention>FOLLOWING</businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Calendar_Trade_London" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                    </businessCenter>
                                </businessCenters>
                                <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                            </cashSettlementValuationDate>
                            <cashSettlementValueDate>
                                <adjustableDate acmLoop = "Is_European_Exercise" file = 'ABSA_XML_Functions'>
                                    <unadjustedDate><acmCode method = "Get_European_Unadjusted_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                                    <dateAdjustments>
                                        <businessDayConvention>FOLLOWING</businessDayConvention>
                                        <businessCenters>
                                            <businessCenter acmLoop = "Get_Calendar_Trade" file = 'ABSA_XML_Functions'>
                                                <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                            </businessCenter>
                                        </businessCenters>
                                    </dateAdjustments>
                                </adjustableDate>
                                <relativeDate acmLoop = "Is_Bermuda_Exercise" file = 'ABSA_XML_Functions'>
                                    <periodMultiplier>0</periodMultiplier>
                                    <period>D</period>
                                    <businessDayConvention>FOLLOWING</businessDayConvention>
                                    <businessCenters>
                                        <businessCenter acmLoop = "Get_Calendar_Trade" file = 'ABSA_XML_Functions'>
                                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                        </businessCenter>
                                    </businessCenters>
                                    <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                                </relativeDate>
                            </cashSettlementValueDate>
                            <cashPriceMethod acmLoop = "Get_CashPriceMethod" file = 'ABSA_XML_Functions'>
                                <cashSettlementCurrency>
                                    <id type = "grdCurrency"><acmCode method = 'Trade.Currency.Name'/></id>
                                </cashSettlementCurrency>
                                <quotationRateType>Mid</quotationRateType>
                            </cashPriceMethod>
                            <zeroCouponYieldAdjustedMethod acmLoop = "Get_zeroCouponYieldAdjustedMethod" file = 'ABSA_XML_Functions'>
                                <settlementRateSource>
                                    <informationSource>
                                        <rateSource>
                                            <id type = "bcInformationProvider">Reuters</id>
                                        </rateSource>
                                        <rateSourcePage>
                                            <id type = "abcapFrontarenaRateSourcePage">17143</id>
                                        </rateSourcePage>
                                    </informationSource>
                                </settlementRateSource>
                                <quotationRateType>Mid</quotationRateType>
                            </zeroCouponYieldAdjustedMethod>
                        </cashSettlement>
                    </optionalEarlyTermination>
                </earlyTerminationProvision>
            </irCapFloor>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_irCapFloor_template, trade)

