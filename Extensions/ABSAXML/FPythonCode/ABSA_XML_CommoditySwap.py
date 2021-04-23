""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_CommoditySwap(trade):
    xml_CommoditySwap_template = '''\
        <commoditySwap>
            <fixedPriceLeg>
                <payOrReceive>Pay</payOrReceive>
                <effectiveDate>
                    <unadjustedDate><acmCode method = "Get_Trade_Create_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </effectiveDate>
                <terminationDate>
                    <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </terminationDate>
                <calculationPeriodsSchedule>
                    <periodMultiplier><acmCode method = "Get_SpotOffSet" file = 'ABSA_XML_Functions'/></periodMultiplier>
                    <period>D</period>
                    <rollConvention>
                        <id type="bcRollConvention">Business Days</id>
                    </rollConvention>
                </calculationPeriodsSchedule>
                <fixedPrice>
                    <priceSchedule>
                        <initialValue><acmCode method = "Get_Trd_Price" file = 'ABSA_XML_Functions'/></initialValue>
                    </priceSchedule>
                    <currency>
                        <id type="grdCurrency"><acmCode method = "Get_Trade_Currency" file = 'ABSA_XML_Functions'/></id>
                    </currency>
                    <unit>
                        <id type="bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                </fixedPrice>
                <notionalQuantity>
                    <quantity>
                        <initialValue><acmCode method = "Get_Trade_Quantity" file = 'ABSA_XML_Functions'/></initialValue>
                    </quantity>
                    <unit>
                        <id type="bcQuantityUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                    <frequency>Monthly</frequency>
                </notionalQuantity>
                <totalNotionalQuantity>
                    <amount><acmCode method = "Get_Trd_Nominal" file = 'ABSA_XML_Functions'/></amount>
                    <unit>
                        <id type="bcQuantityUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                </totalNotionalQuantity>
                <relativePaymentDates>
                    <payRelativeTo>CalculationPeriodEndDate</payRelativeTo>
                    <paymentDaysOffset>
                        <periodMultiplier><acmCode method = "Get_SpotOffSet" file = 'ABSA_XML_Functions'/></periodMultiplier>
                        <period>D</period>
                    </paymentDaysOffset>
                    <paymentDatesAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </paymentDatesAdjustments>
                </relativePaymentDates>
            </fixedPriceLeg>
            <floatingPriceLeg>
                <payOrReceive>Receive</payOrReceive>
                <effectiveDate>
                    <unadjustedDate><acmCode method = "Get_Trade_Create_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>MODFOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </effectiveDate>
                <terminationDate>
                    <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                    <dateAdjustments>
                        <businessDayConvention>FOLLOWING</businessDayConvention>
                        <businessCenters>
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </dateAdjustments>
                </terminationDate>
                <calculationPeriodsSchedule>
                    <periodMultiplier><acmCode method = "Get_SpotOffSet" file = 'ABSA_XML_Functions'/></periodMultiplier>
                    <period>D</period>
                    <rollConvention>
                        <id type="bcRollConvention">Business Days</id>
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
                        <initialValue><acmCode method = "Get_Trade_Quantity" file = 'ABSA_XML_Functions'/></initialValue>
                    </quantity>
                    <unit>
                        <id type = "bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                    </unit>
                    <frequency>Monthly</frequency>
                </notionalQuantity>
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
                            <businessCenter>
                                <id type = "fpmlBusinessCenter">ZAJO</id>
                            </businessCenter>
                        </businessCenters>
                    </paymentDatesAdjustments>
                </relativePaymentDates>
            </floatingPriceLeg>
        </commoditySwap>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_CommoditySwap_template, trade)
