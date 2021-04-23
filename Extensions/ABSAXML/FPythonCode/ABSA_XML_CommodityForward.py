""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_CommodityForward(trade):
    xml_CommodityForward_template = '''\
        <commodityForward>
            <buyOrSell><acmCode method = "Get_Premium_BuyOrSell" file = 'ABSA_XML_Functions'/></buyOrSell>
            <valueDate>
                <unadjustedDate><acmCode method = "Get_Value_Date" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention>MODFOLLOWING</businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar_ISDA" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "PassThrough" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </valueDate>
            <commodityType>
                <id type="abcapFrontarenaIndexGroup"><acmCode method = "Get_Und_Comm_Type" file = 'ABSA_XML_Functions'/></id>
                <alternateId type="abcapFrontarenaIndexGroup">Gold</alternateId>
            </commodityType>
            <product>
                <id type = "assetControlInstrumentId"><acmCode method = "Get_CurrPair" file = 'ABSA_XML_Functions'/></id>
            </product>
            <totalQuantity>
                <amount><acmCode method = "Get_Trade_Quantity" file = 'ABSA_XML_Functions'/></amount>
                <unit>
                    <id type="bcPriceUnit">Ounces</id>
                </unit>
            </totalQuantity>
            <price>
                <currency>
                    <id type="grdCurrency"><acmCode method = "Get_Trade_Currency" file = 'ABSA_XML_Functions'/></id>
                </currency>
                <amount><acmCode method = "Get_Trd_Price" file = 'ABSA_XML_Functions'/></amount>
                <unit>
                    <id type="bcPriceUnit">Ounces</id>
                </unit>
            </price>
        </commodityForward>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_CommodityForward_template, trade)
