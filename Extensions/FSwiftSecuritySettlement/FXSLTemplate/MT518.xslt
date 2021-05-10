<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SEME)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((CANC|NEWM)(/(CODU|COPY|DUPL))?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRTR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RELA|PREV|MAST|BASK|INDX|LIST|PROG|TRRF|COMM|COLR|ISSU|BMRB|ALMR)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRRF)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,52})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern">
    <xs:attribute fixed="20U" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD|NAVD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD|NAVD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DEAL)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DEAL)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CORA|COWA|BAKL|ENTF|NAVR)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DAAC|GIUP)//(N)?[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_99A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern">
    <xs:attribute fixed="99A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD|SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//(CUST|ICSD|NCSD|SHHE)/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD|SAFE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_94L_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern">
    <xs:attribute fixed="94L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MPLE|PRIC|PROC|RPOR|PRIR|SETG|TTCO|COST|CATB|TRCN)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUSE|PAYM)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FXIB|FXIS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INVE|BUYR|CLBR|SELL|STBR|INBR|BRCR|ETC1|ETC2|AFFM|RQBR)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INVE|BUYR|CLBR|SELL|STBR|INBR|BRCR|ETC1|ETC2|AFFM|RQBR)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INVE|BUYR|CLBR|SELL|STBR|INBR|BRCR|ETC1|ETC2|AFFM|RQBR)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE|CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DECL)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRCA|INCA)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CONF)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PLIS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MICO|FORM|PFRE|PAYS|CFRE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OPST|OPTI)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern">
    <xs:attribute fixed="12B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)//[A-Z0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern">
    <xs:attribute fixed="12C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DENO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|EXPI|FRNR|MATU|ISSU|CALD|CONV|PUTT|DDTE|FCOU|NWFC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRFC|CUFC|NWFC|INTR|NXRT|INDX|YTMR)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|VERN)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|POOL|LOTS|VERN)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CONV|FRNF|COVE|CALL|PUTT|WRTS|ODDC)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|EXER)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|EXER)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MINO|SIZE|ORGV)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FIAN)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CERT)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TPRO|RSTR)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETR|STCO|STAM|RTGS|REGT|BENE|CASY|DBNM|REST|LEOG|SETS|REPT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FXIB|FXIS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PSET)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern">
    <xs:attribute fixed="95C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|REAG|RECU|REI1|REI2|SELL)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REGI)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCW|BENM|DEBT|INTM|PAYE)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCW|BENM|DEBT|INTM|PAYE)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCW|BENM|DEBT|INTM|PAYE)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACRU|STAM|EXEC|RSCH)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH|MEOR|MERE|TRRE|TRAG|VEND|INPA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH|MEOR|MERE|TRRE|TRAG|VEND|INPA)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH|MEOR|MERE|TRRE|TRAG|VEND|INPA)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_95S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_95S_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_95S_Type_Pattern">
    <xs:attribute fixed="95S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE|CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PACO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceD_OtherParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceD_OtherParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceD_OtherParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TERM)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RERT|MICO|REVA|LEGA)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SECO|REPO)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REPO|RSPR|PRIC|SLMG|SHAI)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(VASU|PRIC)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,24})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_92C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern">
    <xs:attribute fixed="92C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CADE|TOCO)//[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_99B_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern">
    <xs:attribute fixed="99B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FORF|TRTE|REPP|ACRU|DEAL|TAPC)//(N)?(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SECO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersMessageReference" type="MT518_SequenceA_GeneralInformation_20C_Type"/>
   <xs:element name="FunctionOfTheMessage" type="MT518_SequenceA_GeneralInformation_23G_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PreparationDateTime_A" type="MT518_SequenceA_GeneralInformation_98A_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_C" type="MT518_SequenceA_GeneralInformation_98C_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_E" type="MT518_SequenceA_GeneralInformation_98E_Type"/>
   </xs:choice>
   <xs:element name="TradeTransactionType" type="MT518_SequenceA_GeneralInformation_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceA1_Linkages" type="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="GENL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LinkedMessage_A" type="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type"/>
    <xs:element minOccurs="0" name="LinkedMessage_B" type="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="Reference_C" type="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type"/>
    <xs:element name="Reference_U" type="MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="LINK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT518_SequenceB_ConfirmationDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT518_SequenceB_ConfirmationDetails_98B_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT518_SequenceB_ConfirmationDetails_98C_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_E" type="MT518_SequenceB_ConfirmationDetails_98E_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="DealPrice_A" type="MT518_SequenceB_ConfirmationDetails_90A_Type"/>
    <xs:element name="DealPrice_B" type="MT518_SequenceB_ConfirmationDetails_90B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate" type="MT518_SequenceB_ConfirmationDetails_92A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberCount" type="MT518_SequenceB_ConfirmationDetails_99A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_B" type="MT518_SequenceB_ConfirmationDetails_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_C" type="MT518_SequenceB_ConfirmationDetails_94C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_F" type="MT518_SequenceB_ConfirmationDetails_94F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_L" type="MT518_SequenceB_ConfirmationDetails_94L_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="SettlementAmount" type="MT518_SequenceB_ConfirmationDetails_19A_Type"/>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Indicator_F" type="MT518_SequenceB_ConfirmationDetails_22F_Type"/>
    <xs:element maxOccurs="unbounded" name="Indicator_H" type="MT518_SequenceB_ConfirmationDetails_22H_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="Currency" type="MT518_SequenceB_ConfirmationDetails_11A_Type"/>
   <xs:element maxOccurs="unbounded" name="SubSequenceB1_ConfirmationParties" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties"/>
   <xs:element name="QuantityOfFinancialInstrument" type="MT518_SequenceB_ConfirmationDetails_36B_Type"/>
   <xs:element name="IdentificationOfTheFinancialInstrument" type="MT518_SequenceB_ConfirmationDetails_35B_Type"/>
   <xs:element minOccurs="0" name="SubSequenceB2_FinancialInstrumentAttribute" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CertificateNumber" type="MT518_SequenceB_ConfirmationDetails_13B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative" type="MT518_SequenceB_ConfirmationDetails_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="CONFDET" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_A" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_B" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_E" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ProcessingDateTime_A" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type"/>
    <xs:element minOccurs="0" name="ProcessingDateTime_C" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_C" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_E" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="CONFPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute">
  <xs:sequence>
   <xs:element minOccurs="0" name="PlaceOfListing" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_A" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_B" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_C" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="CurrencyOfDenomination" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_A" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_B" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="IdentificationOfTheFinancialInstrument" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type"/>
   <xs:element minOccurs="0" name="FinancialInstrumentAttributeNarrative" type="MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="Indicator" type="MT518_SequenceC_SettlementDetails_22F_Type"/>
   <xs:element minOccurs="0" name="Currency" type="MT518_SequenceC_SettlementDetails_11A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceC1_SettlementParties" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceC2_CashParties" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceC3_Amounts" type="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SETDET" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_C" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="SafekeepingAccount_A" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type"/>
    <xs:element minOccurs="0" name="SafekeepingAccount_B" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ProcessingDateTime_A" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type"/>
    <xs:element minOccurs="0" name="ProcessingDateTime_C" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_C" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_D" type="MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SETPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_A" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_E" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ProcessingDateTime_A" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type"/>
    <xs:element minOccurs="0" name="ProcessingDateTime_C" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type"/>
   <xs:element minOccurs="0" name="PartyNarrative" type="MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="CSHPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type"/>
   <xs:element maxOccurs="unbounded" name="Amount" type="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ValueDateTime_A" type="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type"/>
    <xs:element minOccurs="0" name="ValueDateTime_C" type="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ExchangeRate" type="MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="AMT" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceD_OtherParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="PARTY_L" type="MT518_SequenceD_OtherParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_P" type="MT518_SequenceD_OtherParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_Q" type="MT518_SequenceD_OtherParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_R" type="MT518_SequenceD_OtherParties_95R_Type"/>
    <xs:element maxOccurs="unbounded" name="PARTY_S" type="MT518_SequenceD_OtherParties_95S_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_A" type="MT518_SequenceD_OtherParties_97A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_B" type="MT518_SequenceD_OtherParties_97B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_E" type="MT518_SequenceD_OtherParties_97E_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="PartyNarrative" type="MT518_SequenceD_OtherParties_70C_Type"/>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT518_SequenceD_OtherParties_20C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="OTHRPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT518_SequenceE_TwoLegTransactionDetails">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_A" type="MT518_SequenceE_TwoLegTransactionDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_B" type="MT518_SequenceE_TwoLegTransactionDetails_98B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_C" type="MT518_SequenceE_TwoLegTransactionDetails_98C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT518_SequenceE_TwoLegTransactionDetails_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Reference" type="MT518_SequenceE_TwoLegTransactionDetails_20C_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT518_SequenceE_TwoLegTransactionDetails_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_C" type="MT518_SequenceE_TwoLegTransactionDetails_92C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberCount" type="MT518_SequenceE_TwoLegTransactionDetails_99B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT518_SequenceE_TwoLegTransactionDetails_19A_Type"/>
   <xs:element minOccurs="0" name="SecondLegNarrative" type="MT518_SequenceE_TwoLegTransactionDetails_70C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="REPO" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT518">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT518_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_ConfirmationDetails" type="MT518_SequenceB_ConfirmationDetails"/>
    <xs:element minOccurs="0" name="SequenceC_SettlementDetails" type="MT518_SequenceC_SettlementDetails"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="SequenceD_OtherParties" type="MT518_SequenceD_OtherParties"/>
    <xs:element minOccurs="0" name="SequenceE_TwoLegTransactionDetails" type="MT518_SequenceE_TwoLegTransactionDetails"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

