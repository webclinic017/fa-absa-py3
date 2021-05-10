<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_22_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMEND|CANCEL|CLOSEOUT|NEW)/[A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_22_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_22_Type_Pattern">
    <xs:attribute fixed="22" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_23_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((BUY|SELL)/(CALL|PUT)/(A|E)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_23_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_23_Type_Pattern">
    <xs:attribute fixed="23" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_94A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(AGN([0-5][0-9])|BILA|BROK)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_94A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_94A_Type_Pattern">
    <xs:attribute fixed="94A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_82A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_82A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_82A_Type_Pattern">
    <xs:attribute fixed="82A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_82D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_82D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_82D_Type_Pattern">
    <xs:attribute fixed="82D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_82J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_82J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_82J_Type_Pattern">
    <xs:attribute fixed="82J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_87A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_87A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_87A_Type_Pattern">
    <xs:attribute fixed="87A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_87D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_87D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_87D_Type_Pattern">
    <xs:attribute fixed="87D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_87J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_87J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_87J_Type_Pattern">
    <xs:attribute fixed="87J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_83A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_83A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_83A_Type_Pattern">
    <xs:attribute fixed="83A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_83D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_83D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_83D_Type_Pattern">
    <xs:attribute fixed="83D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_83J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_83J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_83J_Type_Pattern">
    <xs:attribute fixed="83J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_30_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_30_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_30_Type_Pattern">
    <xs:attribute fixed="30" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_31C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_31C_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_31C_Type_Pattern">
    <xs:attribute fixed="31C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_31G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_31G_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_31G_Type_Pattern">
    <xs:attribute fixed="31G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_31E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_31E_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_31E_Type_Pattern">
    <xs:attribute fixed="31E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_26F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(NE([0-5][0-9])CAS(0[0-9]|[1][0-9]|2[1-3])|PRINCIPAL)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_26F_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_26F_Type_Pattern">
    <xs:attribute fixed="26F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_39M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_39M_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_39M_Type_Pattern">
    <xs:attribute fixed="39M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_17F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_17F_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_17F_Type_Pattern">
    <xs:attribute fixed="17F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_32E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_32E_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_32E_Type_Pattern">
    <xs:attribute fixed="32E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_36_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_36_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_36_Type_Pattern">
    <xs:attribute fixed="36" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_33B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_33B_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_33B_Type_Pattern">
    <xs:attribute fixed="33B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_37K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD|PCT)[0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_37K_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_37K_Type_Pattern">
    <xs:attribute fixed="37K" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_34P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_34P_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_34P_Type_Pattern">
    <xs:attribute fixed="34P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_34R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_34R_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_34R_Type_Pattern">
    <xs:attribute fixed="34R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_77H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))?(//[0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_77H_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_77H_Type_Pattern">
    <xs:attribute fixed="77H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_14C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_14C_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_14C_Type_Pattern">
    <xs:attribute fixed="14C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceA_GeneralInformation_72_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation_72_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceA_GeneralInformation_72_Type_Pattern">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern">
    <xs:attribute fixed="22L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern">
    <xs:attribute fixed="91A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern">
    <xs:attribute fixed="91D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern">
    <xs:attribute fixed="91J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern">
    <xs:attribute fixed="22M" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern">
    <xs:attribute fixed="22N" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
    <xs:attribute fixed="22P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
    <xs:attribute fixed="22R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_81A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_81A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_81A_Type_Pattern">
    <xs:attribute fixed="81A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_81D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_81D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_81D_Type_Pattern">
    <xs:attribute fixed="81D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_81J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_81J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_81J_Type_Pattern">
    <xs:attribute fixed="81J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_89A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_89A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_89A_Type_Pattern">
    <xs:attribute fixed="89A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_89D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_89D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_89D_Type_Pattern">
    <xs:attribute fixed="89D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_89J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_89J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_89J_Type_Pattern">
    <xs:attribute fixed="89J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_96A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_96A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_96A_Type_Pattern">
    <xs:attribute fixed="96A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_96D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_96D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_96D_Type_Pattern">
    <xs:attribute fixed="96D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_96J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_96J_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_96J_Type_Pattern">
    <xs:attribute fixed="96J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_22S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((C|P)/(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_22S_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_22S_Type_Pattern">
    <xs:attribute fixed="22S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_22T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_22T_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_22T_Type_Pattern">
    <xs:attribute fixed="22T" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17E_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17E_Type_Pattern">
    <xs:attribute fixed="17E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_22U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((FXNDOP|FXVAOP))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_22U_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_22U_Type_Pattern">
    <xs:attribute fixed="22U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((A|P|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17H_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17H_Type_Pattern">
    <xs:attribute fixed="17H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((F|O|P|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17P_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17P_Type_Pattern">
    <xs:attribute fixed="17P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_22V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_22V_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_22V_Type_Pattern">
    <xs:attribute fixed="22V" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_98D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_98D_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_98D_Type_Pattern">
    <xs:attribute fixed="98D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17W_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17W_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17W_Type_Pattern">
    <xs:attribute fixed="17W" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17Y_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((F|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17Y_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17Y_Type_Pattern">
    <xs:attribute fixed="17Y" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17Z_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17Z_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17Z_Type_Pattern">
    <xs:attribute fixed="17Z" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_22Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_22Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_22Q_Type_Pattern">
    <xs:attribute fixed="22Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17L_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17L_Type_Pattern">
    <xs:attribute fixed="17L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((A|C|F|I|L|O|R|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17M_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17M_Type_Pattern">
    <xs:attribute fixed="17M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(N|[0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17Q_Type_Pattern">
    <xs:attribute fixed="17Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(N|[0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17S_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17S_Type_Pattern">
    <xs:attribute fixed="17S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_17X_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(N|[0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_17X_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_17X_Type_Pattern">
    <xs:attribute fixed="17X" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_34C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_34C_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_34C_Type_Pattern">
    <xs:attribute fixed="34C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_SequenceB_ReportingInformation_77A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,20})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_77A_Type">
  <xs:simpleContent>
   <xs:extension base="MT305_SequenceB_ReportingInformation_77A_Type_Pattern">
    <xs:attribute fixed="77A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT305_15A_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:simpleType name="MT305_15B_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT305_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="TransactionReferenceNumber" type="MT305_SequenceA_GeneralInformation_20_Type"/>
   <xs:element name="RelatedReference" type="MT305_SequenceA_GeneralInformation_21_Type"/>
   <xs:element name="CodeCommonReference" type="MT305_SequenceA_GeneralInformation_22_Type"/>
   <xs:element name="FurtherIdentification" type="MT305_SequenceA_GeneralInformation_23_Type"/>
   <xs:element minOccurs="0" name="ScopeOfOperation" type="MT305_SequenceA_GeneralInformation_94A_Type"/>
   <xs:choice>
    <xs:element name="PartyA_A" type="MT305_SequenceA_GeneralInformation_82A_Type"/>
    <xs:element name="PartyA_D" type="MT305_SequenceA_GeneralInformation_82D_Type"/>
    <xs:element name="PartyA_J" type="MT305_SequenceA_GeneralInformation_82J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="PartyB_A" type="MT305_SequenceA_GeneralInformation_87A_Type"/>
    <xs:element name="PartyB_D" type="MT305_SequenceA_GeneralInformation_87D_Type"/>
    <xs:element name="PartyB_J" type="MT305_SequenceA_GeneralInformation_87J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_A" type="MT305_SequenceA_GeneralInformation_83A_Type"/>
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_D" type="MT305_SequenceA_GeneralInformation_83D_Type"/>
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_J" type="MT305_SequenceA_GeneralInformation_83J_Type"/>
   </xs:choice>
   <xs:element name="DateContractAgreedAmended" type="MT305_SequenceA_GeneralInformation_30_Type"/>
   <xs:element minOccurs="0" name="EarliestExerciseDate" type="MT305_SequenceA_GeneralInformation_31C_Type"/>
   <xs:element name="ExpiryDetails" type="MT305_SequenceA_GeneralInformation_31G_Type"/>
   <xs:element name="FinalSettlementDate" type="MT305_SequenceA_GeneralInformation_31E_Type"/>
   <xs:element name="SettlementType" type="MT305_SequenceA_GeneralInformation_26F_Type"/>
   <xs:element minOccurs="0" name="PaymentClearingCentre" type="MT305_SequenceA_GeneralInformation_39M_Type"/>
   <xs:element minOccurs="0" name="NonDeliverableIndicator" type="MT305_SequenceA_GeneralInformation_17F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SettlementRateSource" type="MT305_SequenceA_GeneralInformation_14S_Type"/>
   <xs:element minOccurs="0" name="SettlementCurrency" type="MT305_SequenceA_GeneralInformation_32E_Type"/>
   <xs:element name="UnderlyingCurrencyNAmount" type="MT305_SequenceA_GeneralInformation_32B_Type"/>
   <xs:element name="StrikePrice" type="MT305_SequenceA_GeneralInformation_36_Type"/>
   <xs:element name="CounterCurrencyNAmount" type="MT305_SequenceA_GeneralInformation_33B_Type"/>
   <xs:element name="PremiumPrice" type="MT305_SequenceA_GeneralInformation_37K_Type"/>
   <xs:choice>
    <xs:element name="PremiumPayment_P" type="MT305_SequenceA_GeneralInformation_34P_Type"/>
    <xs:element name="PremiumPayment_R" type="MT305_SequenceA_GeneralInformation_34R_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="SendersCorrespondent_A" type="MT305_SequenceA_GeneralInformation_53A_Type"/>
    <xs:element minOccurs="0" name="SendersCorrespondent_B" type="MT305_SequenceA_GeneralInformation_53D_Type"/>
    <xs:element minOccurs="0" name="SendersCorrespondent_D" type="MT305_SequenceA_GeneralInformation_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT305_SequenceA_GeneralInformation_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT305_SequenceA_GeneralInformation_56D_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="AccountWithInstitution_A" type="MT305_SequenceA_GeneralInformation_57A_Type"/>
    <xs:element name="AccountWithInstitution_D" type="MT305_SequenceA_GeneralInformation_57D_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="TypeDateVersionOfAgreement" type="MT305_SequenceA_GeneralInformation_77H_Type"/>
   <xs:element minOccurs="0" name="YearOfDefinitions" type="MT305_SequenceA_GeneralInformation_14C_Type"/>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT305_SequenceA_GeneralInformation_72_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15A" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1_ReportingParties" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_A" type="MT305_SequenceB_ReportingInformation_81A_Type"/>
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_D" type="MT305_SequenceB_ReportingInformation_81D_Type"/>
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_J" type="MT305_SequenceB_ReportingInformation_81J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ClearingBroker_A" type="MT305_SequenceB_ReportingInformation_89A_Type"/>
    <xs:element minOccurs="0" name="ClearingBroker_D" type="MT305_SequenceB_ReportingInformation_89D_Type"/>
    <xs:element minOccurs="0" name="ClearingBroker_J" type="MT305_SequenceB_ReportingInformation_89J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ClearingExceptionParty_A" type="MT305_SequenceB_ReportingInformation_96A_Type"/>
    <xs:element minOccurs="0" name="ClearingExceptionParty_D" type="MT305_SequenceB_ReportingInformation_96D_Type"/>
    <xs:element minOccurs="0" name="ClearingExceptionParty_J" type="MT305_SequenceB_ReportingInformation_96J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="ClearingBrokerIdentification" type="MT305_SequenceB_ReportingInformation_22S_Type"/>
   <xs:element minOccurs="0" name="ClearedProductIdentification" type="MT305_SequenceB_ReportingInformation_22T_Type"/>
   <xs:element minOccurs="0" name="ClearingThresholdIndicator" type="MT305_SequenceB_ReportingInformation_17E_Type"/>
   <xs:element minOccurs="0" name="UnderlyingProductIdentifier" type="MT305_SequenceB_ReportingInformation_22U_Type"/>
   <xs:element minOccurs="0" name="IdentificationOfFinancialInstrument" type="MT305_SequenceB_ReportingInformation_35B_Type"/>
   <xs:element minOccurs="0" name="AllocationIndicator" type="MT305_SequenceB_ReportingInformation_17H_Type"/>
   <xs:element minOccurs="0" name="CollateralisationIndicator" type="MT305_SequenceB_ReportingInformation_17P_Type"/>
   <xs:element minOccurs="0" name="ExecutionVenue" type="MT305_SequenceB_ReportingInformation_22V_Type"/>
   <xs:element minOccurs="0" name="ExecutionTimestamp" type="MT305_SequenceB_ReportingInformation_98D_Type"/>
   <xs:element minOccurs="0" name="NonStandardFlag" type="MT305_SequenceB_ReportingInformation_17W_Type"/>
   <xs:element minOccurs="0" name="FinancialNatureOfCounterpartyIndicator" type="MT305_SequenceB_ReportingInformation_17Y_Type"/>
   <xs:element minOccurs="0" name="CollateralPortfolioIndicator" type="MT305_SequenceB_ReportingInformation_17Z_Type"/>
   <xs:element minOccurs="0" name="CollateralPortfolioCode" type="MT305_SequenceB_ReportingInformation_22Q_Type"/>
   <xs:element minOccurs="0" name="PortfolioCompressionIndicator" type="MT305_SequenceB_ReportingInformation_17L_Type"/>
   <xs:element minOccurs="0" name="CorporateSectorIndicator" type="MT305_SequenceB_ReportingInformation_17M_Type"/>
   <xs:element minOccurs="0" name="TradeWithNonEEACounterpartyIndicator" type="MT305_SequenceB_ReportingInformation_17Q_Type"/>
   <xs:element minOccurs="0" name="IntragroupTradeIndicator" type="MT305_SequenceB_ReportingInformation_17S_Type"/>
   <xs:element minOccurs="0" name="CommercialOrTreasuryFinancingIndicator" type="MT305_SequenceB_ReportingInformation_17X_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CommissionAndFees" type="MT305_SequenceB_ReportingInformation_34C_Type"/>
   <xs:element minOccurs="0" name="AdditionalReportingInformation" type="MT305_SequenceB_ReportingInformation_77A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15B" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties">
  <xs:sequence>
   <xs:element name="ReportingJurisdiction" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ReportingParty_A" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type"/>
    <xs:element minOccurs="0" name="ReportingParty_D" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type"/>
    <xs:element minOccurs="0" name="ReportingParty_J" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1a_UniqueTransactionIdentifier" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="UTINamespaceIssuerCode" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type"/>
   <xs:element name="TransactionIdentifier" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1a1_PriorUniqueTransactionIdentifier" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="PUTINamespaceIssuerCode" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type"/>
   <xs:element name="PriorTransactionIdentifier" type="MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:element name="MT305">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT305_SequenceA_GeneralInformation"/>
    <xs:element minOccurs="0" name="SequenceB_ReportingInformation" type="MT305_SequenceB_ReportingInformation"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

