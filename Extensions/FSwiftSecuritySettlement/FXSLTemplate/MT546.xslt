<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SEME)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((CANC|NEWM|RVSL)(/(CODU|COPY|DUPL))?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PARS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREC)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(POOL|PREV|RELA|TRRF|COMM|COLR|CORP|TCTR|CLTR|CLCI|TRCI|MITI|PCTI)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRRF)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,52})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern">
    <xs:attribute fixed="20U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_94H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLEA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_94H_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_94H_Type_Pattern">
    <xs:attribute fixed="94H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_94L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD|CLEA)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_94L_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_94L_Type_Pattern">
    <xs:attribute fixed="94L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD|ESET|CERT)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD|ESET)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD|ESET|CERT)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DEAL)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DEAL)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_99A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DAAC)//(N)?[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_99A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_99A_Type_Pattern">
    <xs:attribute fixed="99A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PLIS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MICO|FORM|PFRE|PAYS|CFRE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OPST|OPTI)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern">
    <xs:attribute fixed="12B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)//[A-Z0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern">
    <xs:attribute fixed="12C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DENO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|EXPI|FRNR|MATU|ISSU|CALD|PUTT|DDTE|FCOU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRFC|CUFC|NWFC|INTR|NXRT|INDX|YTMR)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|POOL)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FRNF|CALL|PUTT)//[A-Z]{1})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|EXER)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|EXER)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MINO|SIZE)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FIAN)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC|RPOR|PRIR|BORR|TTCO|INCA|TRCA|PRIC)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceB_TradeDetails_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FXIN|SPRO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceB_TradeDetails_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ESTT|PSTT|RSTT)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PSTT|RSTT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DENC)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CERT)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE|CASH|REGI)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE|REGI)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//(CUST|ICSD|NCSD|SHHE)/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_94L_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern">
    <xs:attribute fixed="94L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LOTS)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|SSBT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TREM)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RERT|MICO|REVA|LEGA|INTR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SECO|REPO)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REPO|RSPR|PRIC|SLMG|SHAI)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(VASU|PRIC)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,24})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_92C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern">
    <xs:attribute fixed="92C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CADE|TOCO)//[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_99B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern">
    <xs:attribute fixed="99B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FORF|TRTE|REPP|ACRU|DEAL|TAPC)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SECO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(STCO|SETR|TRCA|STAM|RTGS|REGT|BENE|CASY|DBNM|TCPI|MACL|BLOC|REST|SETS|NETT|CCPT|LEOG|COLA|REPT|COLE|SSBT|CSBT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PSET)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern">
    <xs:attribute fixed="95C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REGI)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DECL)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCW|BENM|DEBT|INTM|PAYE)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCW|BENM|DEBT|INTM|PAYE)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCW|BENM|DEBT|INTM|PAYE)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DECL)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACRU|STAM|EXEC|RSCH)//(N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACRU|ANTO|BOOK|CHAR|COMT|COUN|DEAL|ESTT|EXEC|ISDI|LADT|LEVY|LOCL|LOCO|MARG|OTHR|REGF|SHIP|SPCN|STAM|STEX|TRAN|TRAX|VATA|WITH|COAX|ACCA|RSCH|RESU|OCMT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_95C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INVE)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_95C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_95C_Type_Pattern">
    <xs:attribute fixed="95C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH|MEOR|MERE|TRRE|INVE|VEND|QFIN|TRAG|BRKR)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH|MEOR|MERE|TRRE|INVE|VEND|QFIN|TRAG|BRKR)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH|MEOR|MERE|TRRE|INVE|VEND|QFIN|TRAG|BRKR)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REGI)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DECL)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_SequenceF_OtherParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceF_OtherParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT546_SequenceF_OtherParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT546_16R_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersMessageReference" type="MT546_SequenceA_GeneralInformation_20C_Type"/>
   <xs:element name="FunctionOfMessage" type="MT546_SequenceA_GeneralInformation_23G_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PreparationDateTime_A" type="MT546_SequenceA_GeneralInformation_98A_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_C" type="MT546_SequenceA_GeneralInformation_98C_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_E" type="MT546_SequenceA_GeneralInformation_98E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator_F" type="MT546_SequenceA_GeneralInformation_22F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator_H" type="MT546_SequenceA_GeneralInformation_22H_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" name="SubSequenceA1_Linkages" type="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="GENL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages">
  <xs:sequence>
   <xs:element minOccurs="0" name="LinkageTypeIndicator" type="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LinkedMessage_A" type="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type"/>
    <xs:element minOccurs="0" name="LinkedMessage_B" type="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Reference_C" type="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type"/>
    <xs:element minOccurs="0" name="Reference_U" type="MT546_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="LINK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceB_TradeDetails">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_B" type="MT546_SequenceB_TradeDetails_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_H" type="MT546_SequenceB_TradeDetails_94H_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_L" type="MT546_SequenceB_TradeDetails_94L_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT546_SequenceB_TradeDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT546_SequenceB_TradeDetails_98B_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT546_SequenceB_TradeDetails_98C_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_E" type="MT546_SequenceB_TradeDetails_98E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DealPrice_A" type="MT546_SequenceB_TradeDetails_90A_Type"/>
    <xs:element minOccurs="0" name="DealPrice_B" type="MT546_SequenceB_TradeDetails_90B_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="NumberOfDaysAccrued" type="MT546_SequenceB_TradeDetails_99A_Type"/>
   <xs:element name="IdentificationOfFinancialInstrument" type="MT546_SequenceB_TradeDetails_35B_Type"/>
   <xs:element minOccurs="0" name="SubSequenceB1_FinancialInstrumentAttributes" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT546_SequenceB_TradeDetails_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative" type="MT546_SequenceB_TradeDetails_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="TRADDET" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes">
  <xs:sequence>
   <xs:element minOccurs="0" name="PlaceOfListing" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_A" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_B" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_C" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="CurrencyOfDenomination" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Date" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_A" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_B" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="IdentificationOfFinancialInstrument" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type"/>
   <xs:element minOccurs="0" name="FinancialInstrumentAttributeNarrative" type="MT546_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="QuantityOfFinancialInstrument" type="MT546_SequenceC_FinancialInstrumentAccount_36B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT546_SequenceC_FinancialInstrumentAccount_19A_Type"/>
   <xs:element minOccurs="0" name="DenominationChoice" type="MT546_SequenceC_FinancialInstrumentAccount_70D_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CertificateNumber" type="MT546_SequenceC_FinancialInstrumentAccount_13B_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT546_SequenceC_FinancialInstrumentAccount_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT546_SequenceC_FinancialInstrumentAccount_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT546_SequenceC_FinancialInstrumentAccount_95R_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Account_A" type="MT546_SequenceC_FinancialInstrumentAccount_97A_Type"/>
    <xs:element maxOccurs="unbounded" name="Account_B" type="MT546_SequenceC_FinancialInstrumentAccount_97B_Type"/>
    <xs:element maxOccurs="unbounded" name="Account_E" type="MT546_SequenceC_FinancialInstrumentAccount_97E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_B" type="MT546_SequenceC_FinancialInstrumentAccount_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_C" type="MT546_SequenceC_FinancialInstrumentAccount_94C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_F" type="MT546_SequenceC_FinancialInstrumentAccount_94F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_L" type="MT546_SequenceC_FinancialInstrumentAccount_94L_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceC1_QuantityBreakdown" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="FIAC" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown">
  <xs:sequence>
   <xs:element minOccurs="0" name="LotNumber" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type"/>
   <xs:element minOccurs="0" name="QuantityOfFinancialInstrumentInTheLot" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LotDateTime_A" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type"/>
    <xs:element minOccurs="0" name="LotDateTime_C" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type"/>
    <xs:element minOccurs="0" name="LotDateTime_E" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BookLotPrice_A" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type"/>
    <xs:element minOccurs="0" name="BookLotPrice_B" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT546_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="BREAK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceD_TwoLegTransactionDetails">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_A" type="MT546_SequenceD_TwoLegTransactionDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_B" type="MT546_SequenceD_TwoLegTransactionDetails_98B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_C" type="MT546_SequenceD_TwoLegTransactionDetails_98C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT546_SequenceD_TwoLegTransactionDetails_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Reference" type="MT546_SequenceD_TwoLegTransactionDetails_20C_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT546_SequenceD_TwoLegTransactionDetails_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_C" type="MT546_SequenceD_TwoLegTransactionDetails_92C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberCount" type="MT546_SequenceD_TwoLegTransactionDetails_99B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT546_SequenceD_TwoLegTransactionDetails_19A_Type"/>
   <xs:element minOccurs="0" name="SecondLegNarrative" type="MT546_SequenceD_TwoLegTransactionDetails_70C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="REPO" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="Indicator" type="MT546_SequenceE_SettlementDetails_22F_Type"/>
   <xs:element maxOccurs="unbounded" name="SubSequenceE1_SettlementParties" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceE2_CashParties" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceE3_Amounts" type="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="SETDET" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_C" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="SafekeepingAccount_A" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type"/>
    <xs:element minOccurs="0" name="SafekeepingAccount_B" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ProcessingDateTime_A" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type"/>
    <xs:element minOccurs="0" name="ProcessingDateTime_C" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_C" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_D" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_E" type="MT546_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="SETPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_A" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_E" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_20C_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_C" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_E" type="MT546_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="CSHPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type"/>
   <xs:element maxOccurs="unbounded" name="Amount" type="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ValueDateTime_A" type="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type"/>
    <xs:element minOccurs="0" name="ValueDateTime_C" type="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ExchangeRate" type="MT546_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SubSequenceE3_Amounts" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT546_SequenceF_OtherParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_C" type="MT546_SequenceF_OtherParties_95C_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT546_SequenceF_OtherParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT546_SequenceF_OtherParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT546_SequenceF_OtherParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT546_SequenceF_OtherParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT546_SequenceF_OtherParties_95S_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="SafekeepingAccount" type="MT546_SequenceF_OtherParties_97A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_C" type="MT546_SequenceF_OtherParties_70C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_D" type="MT546_SequenceF_OtherParties_70D_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_E" type="MT546_SequenceF_OtherParties_70E_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT546_SequenceF_OtherParties_20C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="OTHRPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT546">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT546_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_TradeDetails" type="MT546_SequenceB_TradeDetails"/>
    <xs:element name="SequenceC_FinancialInstrumentAccount" type="MT546_SequenceC_FinancialInstrumentAccount"/>
    <xs:element minOccurs="0" name="SequenceD_TwoLegTransactionDetails" type="MT546_SequenceD_TwoLegTransactionDetails"/>
    <xs:element name="SequenceE_SettlementDetails" type="MT546_SequenceE_SettlementDetails"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="SequenceF_OtherParties" type="MT546_SequenceF_OtherParties"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

