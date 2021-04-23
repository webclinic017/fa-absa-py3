""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
import acm

def Get_FRA(trade):
    xml_FRA_template = '''\
        <fra>
            <buyOrSell acmLoop = "Instrument.Legs"><acmCode method = "Get_Buy_Or_Sell" file = 'ABSA_XML_Functions'/></buyOrSell>
            <effectiveDate acmLoop = "Instrument.Legs">
                <unadjustedDate><acmCode method = "Get_Leg_StartDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention><acmCode method = "Get_Leg_PayDayMethod" file = 'ABSA_XML_Functions'/></businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </effectiveDate>
            <terminationDate acmLoop = "Instrument.Legs">
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
            <paymentDate acmLoop = "Instrument.Legs">
                <unadjustedDate><acmCode method = "Get_First_CF_PayDate" file = 'ABSA_XML_Functions'/></unadjustedDate>
                <dateAdjustments>
                    <businessDayConvention><acmCode method = "Get_Leg_PayDayMethod" file = 'ABSA_XML_Functions'/></businessDayConvention>
                    <businessCenters>
                        <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                            <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                        </businessCenter>
                    </businessCenters>
                </dateAdjustments>
            </paymentDate>
            <fixingDateOffset acmLoop = "Instrument.Legs">
                <periodMultiplier><acmCode method = "Get_Reset_Day_Offset" file = 'ABSA_XML_Functions'/></periodMultiplier>
                <period>D</period>
                <businessDayConvention><acmCode method = "Get_Reset_Day_Method" file = 'ABSA_XML_Functions'/></businessDayConvention>
                <businessCenters>
                    <businessCenter acmLoop = "Get_Calendar" file = 'ABSA_XML_Functions'>
                        <id type = "fpmlBusinessCenter"><acmCode method = "Get_Calendar_Map" file = 'ABSA_XML_Functions'/></id>
                    </businessCenter>
                </businessCenters>
                <fixingRelativeTo>EffectiveDate</fixingRelativeTo>
            </fixingDateOffset>
            <dayCountFraction acmLoop = "Instrument.Legs">
                <id type = "bcDayCountFraction"><acmCode method = "Get_Day_Count_Method" file = 'ABSA_XML_Functions'/></id>
            </dayCountFraction>
            <resetSourceSystem>AbcapFrontArena</resetSourceSystem>
            <resetMethod>Automatic</resetMethod>
            <notional acmLoop = "Instrument.Legs">
                <currency>
                    <id type = "grdCurrency"><acmCode method = 'Currency.Name'/></id>
                </currency>
                <amount><acmCode method = "Get_First_CF_Nominal" file = 'ABSA_XML_Functions'/></amount>
            </notional>
            <fixedRate acmLoop = "Instrument.Legs"><acmCode method = "Convert_Fixed_Rate" file = 'ABSA_XML_Functions'/></fixedRate>
            <floatingRateIndex acmLoop = "Instrument.Legs">
                <id type = "bcFloatingRateIndex"><acmCode method = 'FloatRateReference.FreeText'/></id>
            </floatingRateIndex>
            <indexTenor acmLoop = "Instrument.Legs">
                <periodMultiplier><acmCode method = "Get_Frequency_Period_Multiplier" file = 'ABSA_XML_Functions'/></periodMultiplier>
                <period><acmCode method = "Get_Frequency_Period" file = 'ABSA_XML_Functions'/></period>
            </indexTenor>
            <fraDiscounting>
                <id type = "bcFraDiscounting">Forward</id>
            </fraDiscounting>
            <paymentRule>Advance</paymentRule>
        </fra>
    '''
    return ABSAFOperationsXML.GenerateXmlFromTemplateAsString(xml_FRA_template, trade)





