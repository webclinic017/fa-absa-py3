""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_MetalLoanDeposit(trade):
    xml_MetalLoanDeposit_template = '''\
        <metalLoanDeposit>
            <effectiveDate>
                <unadjustedDate><acmCode method = "Get_Ins_StartDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention>MODFOLLOWING</businessDayConvention>
                    <businessCenters acmLoop = "Instrument.Legs">
                        <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </effectiveDate>
            <terminationDate>
                <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention>MODFOLLOWING</businessDayConvention>
                    <businessCenters acmLoop = "Instrument.Legs">
                        <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </terminationDate>
            <commodity>
                <commodityType>
                    <id type="abcapFrontarenaIndexGroup"><acmCode method = "Get_Und_Comm_Type" file = 'ABSA_XML_Functions'/></id>
                    <alternateId type="abcapFrontarenaIndexGroup">Gold</alternateId>
                </commodityType>
                <product>
                    <id type="assetControlInstrumentId">XAU</id>
                    <alternateId type="assetControlInstrumentId">XAU</alternateId>
                </product>
                <unit>
                    <id type="bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                </unit>
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Instrument.Currency.Name'/></id>
                </currency>
                <publication>
                    <rateSource>
                        <id type = "bcInformationProvider">Reuters Page ZARL></id>
                    </rateSource>
                </publication>
            </commodity>
            <notionalQuantity>
                <amount><acmCode method = "Start_Cash" file = 'ABSA_XML_Functions'/></amount>
                <unit>
                    <id type = "bcQuantityUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                </unit>
            </notionalQuantity>
            <dayCountFraction acmLoop = "Instrument.Legs">
                <id type = "bcDayCountFraction"><acmCode method = "Get_Day_Count_Method" file = 'ABSA_XML_Functions'/></id>
            </dayCountFraction>
            <price>
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                </currency>
                <amount><acmCode method = "Get_Trd_Price" file = 'ABSA_XML_Functions'/></amount>
                <unit>
                    <id type = "bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                </unit>
            </price>
            <interest>
                <rate acmLoop = "Instrument.Legs"><acmCode method = "Convert_Fixed_Rate" file = 'ABSA_XML_Functions'/></rate>
                <paymentDates>
                    <adjustableDates>
                        <unadjustedDate><acmCode method = "Get_Ins_Expiration" file = 'ABSA_XML_Functions'/></unadjustedDate>
                        <dateAdjustments>
                            <businessDayConvention>FOLLOWING</businessDayConvention>
                            <businessCenters acmLoop = "Instrument.Legs">
                                <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                                    <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                                </businessCenter>
                            </businessCenters>
                        </dateAdjustments>
                    </adjustableDates>
                </paymentDates>
            </interest>
            <totalRepaymentAmountMetal>
                <amount><acmCode method = "End_Cash" file = 'ABSA_XML_Functions'/></amount>
                <unit>
                    <id type = "bcPriceUnit"><acmCode method = "Get_Und_Comm_Unit" file = 'ABSA_XML_Functions'/></id>
                </unit>
            </totalRepaymentAmountMetal>
        </metalLoanDeposit>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_MetalLoanDeposit_template, trade)
