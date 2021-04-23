""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_IRSwap(trade):
    xml_irSwap_template = '''\
        <irSwap>
                <swapStream acmLoop = "GetLegs" file = 'ABSA_XML_Functions'>
                    <payOrReceive><acmCode method = "Get_Insrt_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                    <calculationPeriodDates>
                        <effectiveDate>
                            <unadjustedDate><acmCode method = "Get_UnadjustedDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
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
                        <firstRegularPeriodStartDate acmLoop = "Is_FirstRegularPeriodStartDate" file = 'ABSA_XML_Functions'><acmCode method = "Get_CF_StartDate" file = 'ABSA_XML_Functions'/></firstRegularPeriodStartDate>
                        <lastRegularPeriodEndDate acmLoop = "Is_FinalRegularPeriodEndDate" file = 'ABSA_XML_Functions'><acmCode method = "Get_CF_EndDate" file = 'ABSA_XML_Functions'/></lastRegularPeriodEndDate>
                        <stubPeriodDetails acmLoop = "Get_Stub_Period_Object" file = 'ABSA_XML_Functions'>
                            <stubPeriodType><acmCode method = "Get_Stub_Period_Type" file = 'ABSA_XML_Functions'/></stubPeriodType>
                        </stubPeriodDetails>
                        <calculationPeriodFrequency>
                            <periodMultiplier><acmCode method = "Get_Reset_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                            <period><acmCode method = "Get_Reset_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
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
                    <resetDetails acmLoop = "Is_Float_Leg" file = 'ABSA_XML_Functions'>
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
                                    <step acmLoop = "Get_All_Interest" file = 'ABSA_XML_Functions'>
                                        <stepDate><acmCode method = "Get_CF_PayDate" file = 'ABSA_XML_Functions'/></stepDate>
                                        <stepValue><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></stepValue>
                                    </step>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                                    </currency>
                                </notionalStepSchedule>
                            </notionalSchedule>
                            <fixedRate acmLoop = "Is_Fixed_Leg" file = 'ABSA_XML_Functions'><acmCode method = "Convert_Fixed_Rate" file = 'ABSA_XML_Functions'/></fixedRate>
                            <floatingRateCalculation acmLoop = "Is_Float_Leg_Swap" file = 'ABSA_XML_Functions'>
                                <floatingRateIndex>
                                    <id type = "bcFloatingRateIndex"><acmCode method = 'FloatRateReference.FreeText'/></id>
                                </floatingRateIndex>
                                <indexTenor>
                                    <periodMultiplier><acmCode method = "Get_IndexTenor_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                    <period><acmCode method = "Get_IndexTenor_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
                                </indexTenor>
                                <spreadSchedule>
                                    <initialValue><acmCode method = "Convert_Leg_Spread_Leg" file = 'ABSA_XML_Functions'/></initialValue>
                                </spreadSchedule>
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
                            <inflationFloatingRateCalculation acmLoop = "Is_Inflation_Swap" file = 'ABSA_XML_Functions'>
                                <floatingRateIndex>
                                    <id type = "bcInflationFloatingRateIndex"><acmCode method = 'IndexRef.FreeText'/></id>
                                </floatingRateIndex>
                                <publicationLag>
                                    <periodMultiplier>2</periodMultiplier>
                                    <period>D</period>
                                </publicationLag>
                                <initialIndexLevel acmLoop = "Is_Initial_Index_Level" file = 'ABSA_XML_Functions'><acmCode method = 'InitialIndexValue'/></initialIndexLevel>
                                <initialIndexDate><acmCode method = "Get_Leg_StartDate" file = 'ABSA_XML_Functions'/></initialIndexDate>
                                <endIndexDate><acmCode method = "Get_Leg_EndDate" file = 'ABSA_XML_Functions'/></endIndexDate>
                                <interpolationMethod>
                                    <id type = "bcInterpolationMethod"><acmCode method = "Get_InterpolationMethod" file = 'ABSA_XML_Functions'/></id>
                                </interpolationMethod>
                                <interpolationOffset>
                                    <periodMultiplier>2</periodMultiplier>
                                    <period>D</period>
                                </interpolationOffset>
                                <startDays>1</startDays>
                                <endDays>1</endDays>
                            </inflationFloatingRateCalculation>
                            <dayCountFraction>
                                <id type = "bcDayCountFraction"><acmCode method = "Get_Day_Count_Method" file = 'ABSA_XML_Functions'/></id>
                            </dayCountFraction>
                            <compoundingMethod>
                                <id type = "bcCompoundingMethod"><acmCode method = "Get_CompoundingMethod" file = 'ABSA_XML_Functions'/></id>
                            </compoundingMethod>
                        </calculation>
                    </calculationPeriodAmount>
                    <cashflows>
                        <principalAdjustment acmLoop = "Get_All_Interest_CF_CurrSwap" file = 'ABSA_XML_Functions'>
                            <payOrReceive><acmCode method = "Get_CF_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                            <unadjustedPrincipalAdjustmentValueDate><acmCode method = "Get_CF_PayDate" file = 'ABSA_XML_Functions'/></unadjustedPrincipalAdjustmentValueDate>
                            <principalAdjustmentAmount>
                                <currency>
                                    <id type = "grdCurrency"><acmCode method = 'Leg.Currency.Name'/></id>
                                </currency>
                                <amount><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></amount>
                            </principalAdjustmentAmount>
                        </principalAdjustment>
                        <principalExchange acmLoop = "Get_All_Fixed_Amount_CurrSwap" file = 'ABSA_XML_Functions'>
                            <payOrReceive><acmCode method = "Get_CF_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                            <unadjustedPrincipalExchangeValueDate><acmCode method = "Get_CF_PayDate" file = 'ABSA_XML_Functions'/></unadjustedPrincipalExchangeValueDate>
                            <principalExchangeAmount>
                                <currency>
                                    <id type = "grdCurrency"><acmCode method = 'Leg.Currency.Name'/></id>
                                </currency>
                                <amount><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></amount>
                            </principalExchangeAmount>
                            <principalExchangeType><acmCode method = "Get_PrincipalExchangeType" file = 'ABSA_XML_Functions'/></principalExchangeType>
                        </principalExchange>
                        <cashflowsMatchParameters>false</cashflowsMatchParameters>
                        <paymentCalculationPeriod acmLoop = "Get_PaymentCalculationPeriod" file = 'ABSA_XML_Functions'>
                            <adjustedValueDate acmLoop = "Is_AdjustedValueDate" file = 'ABSA_XML_Functions'><acmCode method = "Get_AdjustedValueDate" file = 'ABSA_XML_Functions'/></adjustedValueDate>
                            <calculationPeriod acmLoop = "Is_Not_Compounding_CF_Object" file = 'ABSA_XML_Functions'>
                                <status><acmCode method = "Get_Cashflow_Status" file = 'ABSA_XML_Functions'/></status>
                                <adjustedAccrualStartDate><acmCode method = "Get_CF_StartDate" file = 'ABSA_XML_Functions'/></adjustedAccrualStartDate>
                                <adjustedAccrualEndDate><acmCode method = "Get_CF_EndDate" file = 'ABSA_XML_Functions'/></adjustedAccrualEndDate>
                                <notionalAmount>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'Leg.Currency.Name'/></id>
                                    </currency>
                                    <amount><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></amount>
                                </notionalAmount>
                                <floatingRateDefinition acmLoop = "Is_CF_Type_Float" file = 'ABSA_XML_Functions'>
                                    <rateObservation>
                                        <adjustedFixingDate><acmCode method = "Get_Rate_Observation" file = 'ABSA_XML_Functions'/></adjustedFixingDate>
                                    </rateObservation>
                                    <floatingRateMultiplier acmLoop = "Get_CF_Nominal_Factor" file = 'ABSA_XML_Functions'><acmCode method = "Get_CF_Nominal_Factor_Value" file = 'ABSA_XML_Functions'/></floatingRateMultiplier>
                                    <spread><acmCode method = "Convert_Leg_Spread" file = 'ABSA_XML_Functions'/></spread>
                                </floatingRateDefinition>
                                <fixedRate acmLoop = "Is_CF_Type_Fixed" file = 'ABSA_XML_Functions'><acmCode method = "Convert_CF_Fixed_Rate" file = 'ABSA_XML_Functions'/></fixedRate>
                                <calculationPeriodAmount>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'Leg.Currency.Name'/></id>
                                    </currency>
                                    <amount><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></amount>
                                </calculationPeriodAmount>
                                <compoundingCashflow><acmCode method = "Is_Compounding_CF" file = 'ABSA_XML_Functions'/></compoundingCashflow>
                            </calculationPeriod>
                            <calculationPeriod acmLoop = "Is_Compounding_CF_Object" file = 'ABSA_XML_Functions'>
                                <status><acmCode method = "Get_Cashflow_Status_Reset" file = 'ABSA_XML_Functions'/></status>
                                <adjustedAccrualStartDate><acmCode method = "Get_Reset_StartDate" file = 'ABSA_XML_Functions'/></adjustedAccrualStartDate>
                                <adjustedAccrualEndDate><acmCode method = "Get_Reset_EndDate" file = 'ABSA_XML_Functions'/></adjustedAccrualEndDate>
                                <notionalAmount>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'CashFlow.Leg.Currency.Name'/></id>
                                    </currency>
                                    <amount><acmCode method = "Get_CashFlow_Nominal_Amount_Reset" file = 'ABSA_XML_Functions'/></amount>
                                </notionalAmount>
                                <floatingRateDefinition acmLoop = "Is_CF_Type_Float_Reset" file = 'ABSA_XML_Functions'>
                                    <rateObservation>
                                        <adjustedFixingDate><acmCode method = "Get_Rate_Observation_Reset" file = 'ABSA_XML_Functions'/></adjustedFixingDate>
                                    </rateObservation>
                                    <floatingRateMultiplier acmLoop = "Get_CF_Nominal_Factor_Reset" file = 'ABSA_XML_Functions'><acmCode method = "Get_CF_Nominal_Factor_Value" file = 'ABSA_XML_Functions'/></floatingRateMultiplier>
                                    <spread><acmCode method = "Convert_Leg_Spread_Reset" file = 'ABSA_XML_Functions'/></spread>
                                </floatingRateDefinition>
                                <fixedRate acmLoop = "Is_CF_Type_Fixed_Reset" file = 'ABSA_XML_Functions'><acmCode method = "Convert_CF_Fixed_Rate_Reset" file = 'ABSA_XML_Functions'/></fixedRate>
                                <calculationPeriodAmount>
                                    <currency>
                                        <id type = "grdCurrency"><acmCode method = 'CashFlow.Leg.Currency.Name'/></id>
                                    </currency>
                                    <amount><acmCode method = "Get_CashFlow_Nominal_Amount_Reset" file = 'ABSA_XML_Functions'/></amount>
                                </calculationPeriodAmount>
                                <compoundingCashflow><acmCode method = "Is_Compounding_CF_Reset" file = 'ABSA_XML_Functions'/></compoundingCashflow>
                            </calculationPeriod>
                        </paymentCalculationPeriod>
                    </cashflows>
                    <crossCurrencySwapDetails acmLoop = "Is_CurrSwap" file = 'ABSA_XML_Functions'>
                        <markToMarket>
                            <mtmFrequency>
                                <id type = "bcMtmFrequency">FirstResetDateOnwards</id>
                            </mtmFrequency>
                            <principalInterimExchangeCalendar>
                                <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </principalInterimExchangeCalendar>
                            <fixingDateOffset>
                                <periodMultiplier><acmCode method = 'ResetDayOffset'/></periodMultiplier>
                                <period>D</period>
                                <businessDayConvention><acmCode method = "Get_Reset_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Reset_Calendar" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                    </businessCenter>
                                </businessCenters>
                            </fixingDateOffset>
                            <fixingTime>
                                <hourMinuteTime><acmCode eval = 'Currency().AdditionalInfo().LatestExTime()'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_From_Leg" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </fixingTime>
                            <mtmRoundingPrecision>
                                <roundingDirection>Nearest</roundingDirection>
                                <precision><acmCode method = 'Decimals'/></precision>
                            </mtmRoundingPrecision>
                            <informationSource>
                                <rateSource>
                                    <id type = "bcInformationProvider">Reuters</id>
                                </rateSource>
                                <rateSourcePage>
                                    <id type = "abcapFrontarenaRateSourcePage">UKRPI</id>
                                </rateSourcePage>
                            </informationSource>
                        </markToMarket>
                    </crossCurrencySwapDetails>
                    <zeroCouponSwapDetails acmLoop = "Is_Zero_Coupon_Swap" file = 'ABSA_XML_Functions'>
                        <zeroCouponPaymentAmount>
                            <currency>
                                <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                            </currency>
                            <amount acmLoop = "CashFlows"><acmCode method = "Get_CashFlow_Nominal_Amount" file = 'ABSA_XML_Functions'/></amount>
                        </zeroCouponPaymentAmount>
                        <zeroCouponAdjustedPaymentDate acmLoop = "CashFlows"><acmCode method = "Get_CF_PayDate" file = 'ABSA_XML_Functions'/></zeroCouponAdjustedPaymentDate>
                    </zeroCouponSwapDetails>
                </swapStream>
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
                                            <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                                <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                            </businessCenter>
                                        </businessCenters>
                                    </dateAdjustments>
                                </adjustableDates>
                                <relativeDate>
                                    <periodMultiplier>5</periodMultiplier>
                                    <period>D</period>
                                    <businessDayConvention>FOLLOWING</businessDayConvention>
                                    <businessCenters>
                                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
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
                                <hourMinuteTime><acmCode method = "Get_Earliest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </earliestExerciseTime>
                            <latestExerciseTime>
                                <hourMinuteTime><acmCode method = "Get_Latest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </latestExerciseTime>
                            <expirationTime>
                                <hourMinuteTime><acmCode method = "Get_Latest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
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
                                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                        </businessCenter>
                                    </businessCenters>
                                    <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                                </relativeDate>
                            </expirationDate>
                            <expirationTime>
                                <hourMinuteTime><acmCode method = "Get_Latest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
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
                        <settlementType>Cash</settlementType>
                        <cashSettlement>
                            <cashSettlementValuationTime>
                                <hourMinuteTime><acmCode method = "Get_Latest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                                <businessCenter>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </cashSettlementValuationTime>
                            <cashSettlementValuationDate>
                                <periodMultiplier><acmCode method = "Get_Cashsettlement_Period" file = 'ABSA_XML_Functions'/></periodMultiplier>
                                <period>D</period>
                                <businessDayConvention>FOLLOWING</businessDayConvention>
                                <businessCenters>
                                    <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                        <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
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
                                            <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                                <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                            </businessCenter>
                                        </businessCenters>
                                    </dateAdjustments>
                                </adjustableDate>
                                <relativeDate acmLoop = "Is_Bermuda_Exercise" file = 'ABSA_XML_Functions'>
                                    <periodMultiplier>0</periodMultiplier>
                                    <period>D</period>
                                    <businessDayConvention>FOLLOWING</businessDayConvention>
                                    <businessCenters>
                                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                        </businessCenter>
                                    </businessCenters>
                                    <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                                </relativeDate>
                            </cashSettlementValueDate>
                            <cashPriceMethod acmLoop = "Get_CashPriceMethod" file = 'ABSA_XML_Functions'>
                                <cashSettlementCurrency>
                                    <id type = "grdCurrency"><acmCode method = "Get_Settlement_Currency" file = 'ABSA_XML_Functions'/></id>
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
                <oisSwap>false</oisSwap>
                <principalExchangesApplicable><acmCode method = "Get_Principal_Exchange" file = 'ABSA_XML_Functions'/></principalExchangesApplicable>
            </irSwap>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_irSwap_template, trade)




