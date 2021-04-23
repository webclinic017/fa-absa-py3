""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_Swaption(trade):
    xml_Swaption_template = '''\
        <swaption>
            <buyOrSell><acmCode method = "Get_Trade_Buy_Or_Sell" file = 'ABSA_XML_Functions'/></buyOrSell>
            <premium >
                <payOrReceive><acmCode method = "Get_Premium_PayOrReceive" file = 'ABSA_XML_Functions'/></payOrReceive>
                <otherParty >
                    <partyId>
                        <id type = "sdsCounterpartyId"><acmCode method = "Get_ConfInstr_CP_SDSID" file = 'ABSA_XML_Functions'/></id>
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
                        <businessDayConvention>FOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">Johannesburg</id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </valueDate>
            </premium>
            <exerciseStyle><acmCode method = "Get_Option_Exercise_Style" file = 'ABSA_XML_Functions'/></exerciseStyle>
            <bermudaExercise acmLoop = "Is_Option_Bermuda_Exercise" file = 'ABSA_XML_Functions'>
                <bermudaExerciseDates>
                    <adjustableDates>
                        <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                        <dateAdjustments>
                            <businessDayConvention>FOLLOWING</businessDayConvention>
                            <businessCenters>
                                <businessCenter acmLoop = "Get_Exercise_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </businessCenters>
                        </dateAdjustments>
                    </adjustableDates>
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
                    <hourMinuteTime><acmCode method = "Get_Expiration_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                    <businessCenter>
                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                    </businessCenter>
                </expirationTime>
            </bermudaExercise>
            <europeanExercise acmLoop = "Is_Option_European_Exercise" file = 'ABSA_XML_Functions'>
                <expirationDate>
                    <adjustableDate>
                        <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                        <dateAdjustments>
                            <businessDayConvention>FOLLOWING</businessDayConvention>
                            <businessCenters>
                                <businessCenter acmLoop = "Get_Exercise_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </businessCenters>
                        </dateAdjustments>
                    </adjustableDate>
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
            <exerciseProcedure>
                <manualExercise acmLoop = "Get_FallBackExerc" file = 'ABSA_XML_Functions'>
                    <fallbackExercise><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></fallbackExercise>
                </manualExercise>
                <automaticExercise acmLoop = "Get_AutomaticExerc" file = 'ABSA_XML_Functions'>
                    <thresholdRate>0</thresholdRate>
                </automaticExercise>
                <followUpConfirmation>false</followUpConfirmation>
            </exerciseProcedure>
            <settlementType><acmCode method = "Get_SettlementType" file = 'ABSA_XML_Functions'/></settlementType>
            <cashSettlement acmLoop = "Get_IsCash" file = 'ABSA_XML_Functions'>
                <cashSettlementValuationTime>
                    <hourMinuteTime><acmCode method = "Get_Latest_ExerciseTime" file = 'ABSA_XML_Functions'/></hourMinuteTime>
                    <businessCenter>
                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Instr_ExerciseTime" file = 'ABSA_XML_Functions'/></id>
                    </businessCenter>
                </cashSettlementValuationTime>
                <cashSettlementValuationDate>
                    <periodMultiplier>0</periodMultiplier>
                    <period>D</period>
                    <businessDayConvention>FOLLOWING</businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Valuation_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                    <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                </cashSettlementValuationDate>
                <cashSettlementValueDate>
                    <relativeDate>
                        <periodMultiplier><acmCode method = "Get_Swaption_CSPD" file = 'ABSA_XML_Functions'/></periodMultiplier>
                        <period>D</period>
                        <businessDayConvention>FOLLOWING</businessDayConvention>
			<businessCenters>
                            <businessCenter acmLoop = "Get_Valuation_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                                <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                            </businessCenter>
                        </businessCenters>
                        <dateRelativeTo>CashSettlementPaymentDate</dateRelativeTo>
                    </relativeDate>
                </cashSettlementValueDate>
                <cashPriceMethod acmLoop = "Get_CashSettle" file = 'ABSA_XML_Functions'>
                    <cashSettlementCurrency>
                        <id type = "grdCurrency"><acmCode method = "Get_Settlement_Currency" file = 'ABSA_XML_Functions'/></id>
                    </cashSettlementCurrency>
                    <quotationRateType>Mid</quotationRateType>
                </cashPriceMethod>
                <zeroCouponYieldAdjustedMethod acmLoop = "Get_ZeroCouponYieldSettle" file = 'ABSA_XML_Functions'>
                    <settlementRateSource>
                        <informationSource acmLoop = "Get_ISDA_Source" file = 'ABSA_XML_Functions'>
                            <rateSource>
                                <id type = "bcInformationProvider">Reuters</id>
                            </rateSource>
                        </informationSource>
                        <cashSettlementReferenceBanks acmLoop = "Get_Ref_Banks" file = 'ABSA_XML_Functions'>
                            <referenceBank>
                                <referenceBankId>
                                    <id type = "sdsCounterpartyId">1</id>
                                </referenceBankId>
                            </referenceBank>
                        </cashSettlementReferenceBanks>
                    </settlementRateSource>
                    <quotationRateType>Mid</quotationRateType>
                </zeroCouponYieldAdjustedMethod>
       	        <parYieldCurveUnadjustedMethod acmLoop = "Get_ParYieldCurveUnadjustedSettle" file = 'ABSA_XML_Functions'>
                    <settlementRateSource>
                        <informationSource acmLoop = "Get_ISDA_Source" file = 'ABSA_XML_Functions'>
                            <rateSource>
                                <id type = "bcInformationProvider">Reuters</id>
                            </rateSource>
                        </informationSource>
                        <cashSettlementReferenceBanks acmLoop = "Get_Ref_Banks" file = 'ABSA_XML_Functions'>
                            <referenceBank>
                                <referenceBankId>
                                    <id type = "sdsCounterpartyId">1</id>
                                </referenceBankId>
                            </referenceBank>
                        </cashSettlementReferenceBanks>
                    </settlementRateSource>
                    <quotationRateType>Mid</quotationRateType>
		</parYieldCurveUnadjustedMethod>
            </cashSettlement>
            <acmCode method = "Get_Product_XML_IRSwap" file = 'ABSA_XML_Functions' dataFormat = 'XML'/>
        </swaption>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_Swaption_template, trade)
