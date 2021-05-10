<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_22A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMND|CANC|DUPL|NEWT))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_22A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_22A_Type_Pattern">
    <xs:attribute fixed="22A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_94A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AGNT|BILA|BROK))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_94A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_94A_Type_Pattern">
    <xs:attribute fixed="94A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_22B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((CONF|MATU|ROLL))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_22B_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_22B_Type_Pattern">
    <xs:attribute fixed="22B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_22C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_22C_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_22C_Type_Pattern">
    <xs:attribute fixed="22C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_21N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_21N_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_21N_Type_Pattern">
    <xs:attribute fixed="21N" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_82A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_82A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_82A_Type_Pattern">
    <xs:attribute fixed="82A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_82D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_82D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_82D_Type_Pattern">
    <xs:attribute fixed="82D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_82J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_82J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_82J_Type_Pattern">
    <xs:attribute fixed="82J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_87A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_87A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_87A_Type_Pattern">
    <xs:attribute fixed="87A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_87D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_87D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_87D_Type_Pattern">
    <xs:attribute fixed="87D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_87J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_87J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_87J_Type_Pattern">
    <xs:attribute fixed="87J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_83A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_83A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_83A_Type_Pattern">
    <xs:attribute fixed="83A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_83D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_83D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_83D_Type_Pattern">
    <xs:attribute fixed="83D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_83J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_83J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_83J_Type_Pattern">
    <xs:attribute fixed="83J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceA_GeneralInformation_77D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation_77D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceA_GeneralInformation_77D_Type_Pattern">
    <xs:attribute fixed="77D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_17R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((B|L))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_17R_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_17R_Type_Pattern">
    <xs:attribute fixed="17R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_30T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_30T_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_30T_Type_Pattern">
    <xs:attribute fixed="30T" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_30V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_30V_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_30V_Type_Pattern">
    <xs:attribute fixed="30V" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_30P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_30P_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_30P_Type_Pattern">
    <xs:attribute fixed="30P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_32H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_32H_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_32H_Type_Pattern">
    <xs:attribute fixed="32H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_30X_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_30X_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_30X_Type_Pattern">
    <xs:attribute fixed="30X" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_34E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_34E_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_34E_Type_Pattern">
    <xs:attribute fixed="34E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_37G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?[0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_37G_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_37G_Type_Pattern">
    <xs:attribute fixed="37G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_14D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,7})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_14D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_14D_Type_Pattern">
    <xs:attribute fixed="14D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_38J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{1}[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_38J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_38J_Type_Pattern">
    <xs:attribute fixed="38J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceB_TransactionDetails_39M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails_39M_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceB_TransactionDetails_39M_Type_Pattern">
    <xs:attribute fixed="39M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceG_TaxInformation_37L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceG_TaxInformation_37L_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceG_TaxInformation_37L_Type_Pattern">
    <xs:attribute fixed="37L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceG_TaxInformation_33B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceG_TaxInformation_33B_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceG_TaxInformation_33B_Type_Pattern">
    <xs:attribute fixed="33B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceG_TaxInformation_36_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceG_TaxInformation_36_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceG_TaxInformation_36_Type_Pattern">
    <xs:attribute fixed="36" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceG_TaxInformation_33E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceG_TaxInformation_33E_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceG_TaxInformation_33E_Type_Pattern">
    <xs:attribute fixed="33E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_29A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_29A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_29A_Type_Pattern">
    <xs:attribute fixed="29A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_24D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((BROK|ELEC|PHON)(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_24D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_24D_Type_Pattern">
    <xs:attribute fixed="24D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_84A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_84A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_84A_Type_Pattern">
    <xs:attribute fixed="84A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_84B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_84B_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_84B_Type_Pattern">
    <xs:attribute fixed="84B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_84D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_84D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_84D_Type_Pattern">
    <xs:attribute fixed="84D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_84J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_84J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_84J_Type_Pattern">
    <xs:attribute fixed="84J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_85A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_85A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_85A_Type_Pattern">
    <xs:attribute fixed="85A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_85B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_85B_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_85B_Type_Pattern">
    <xs:attribute fixed="85B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_85D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_85D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_85D_Type_Pattern">
    <xs:attribute fixed="85D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_85J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_85J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_85J_Type_Pattern">
    <xs:attribute fixed="85J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_88A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_88A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_88A_Type_Pattern">
    <xs:attribute fixed="88A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_88D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_88D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_88D_Type_Pattern">
    <xs:attribute fixed="88D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_88J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_88J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_88J_Type_Pattern">
    <xs:attribute fixed="88J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_71F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_71F_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_71F_Type_Pattern">
    <xs:attribute fixed="71F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_26H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_26H_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_26H_Type_Pattern">
    <xs:attribute fixed="26H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_21G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_21G_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_21G_Type_Pattern">
    <xs:attribute fixed="21G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_34C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_34C_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_34C_Type_Pattern">
    <xs:attribute fixed="34C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceH_AdditionalInformation_72_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation_72_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceH_AdditionalInformation_72_Type_Pattern">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_18A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern">
    <xs:attribute fixed="18A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern">
    <xs:attribute fixed="32H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersReference" type="MT320_SequenceA_GeneralInformation_20_Type"/>
   <xs:element minOccurs="0" name="RelatedReference" type="MT320_SequenceA_GeneralInformation_21_Type"/>
   <xs:element name="TypeOfOperation" type="MT320_SequenceA_GeneralInformation_22A_Type"/>
   <xs:element minOccurs="0" name="ScopeOfOperation" type="MT320_SequenceA_GeneralInformation_94A_Type"/>
   <xs:element name="TypeOfEvent" type="MT320_SequenceA_GeneralInformation_22B_Type"/>
   <xs:element name="CommonReference" type="MT320_SequenceA_GeneralInformation_22C_Type"/>
   <xs:element minOccurs="0" name="ContractNumberPartyA" type="MT320_SequenceA_GeneralInformation_21N_Type"/>
   <xs:choice>
    <xs:element name="PartyA_A" type="MT320_SequenceA_GeneralInformation_82A_Type"/>
    <xs:element name="PartyA_D" type="MT320_SequenceA_GeneralInformation_82D_Type"/>
    <xs:element name="PartyA_J" type="MT320_SequenceA_GeneralInformation_82J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="PartyB_A" type="MT320_SequenceA_GeneralInformation_87A_Type"/>
    <xs:element name="PartyB_D" type="MT320_SequenceA_GeneralInformation_87D_Type"/>
    <xs:element name="PartyB_J" type="MT320_SequenceA_GeneralInformation_87J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="FundOrInstructingParty_A" type="MT320_SequenceA_GeneralInformation_83A_Type"/>
    <xs:element minOccurs="0" name="FundOrInstructingParty_D" type="MT320_SequenceA_GeneralInformation_83D_Type"/>
    <xs:element minOccurs="0" name="FundOrInstructingParty_J" type="MT320_SequenceA_GeneralInformation_83J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="TermsAndConditions" type="MT320_SequenceA_GeneralInformation_77D_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15A" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceB_TransactionDetails">
  <xs:sequence>
   <xs:element name="PartyAsRole" type="MT320_SequenceB_TransactionDetails_17R_Type"/>
   <xs:element name="TradeDate" type="MT320_SequenceB_TransactionDetails_30T_Type"/>
   <xs:element name="ValueDate" type="MT320_SequenceB_TransactionDetails_30V_Type"/>
   <xs:element name="MaturityDate" type="MT320_SequenceB_TransactionDetails_30P_Type"/>
   <xs:element name="CurrencyAndPrincipalAmount" type="MT320_SequenceB_TransactionDetails_32B_Type"/>
   <xs:element minOccurs="0" name="AmountToBeSettled" type="MT320_SequenceB_TransactionDetails_32H_Type"/>
   <xs:element minOccurs="0" name="NextInterestDueDate" type="MT320_SequenceB_TransactionDetails_30X_Type"/>
   <xs:element name="CurrencyAndInterestAmount" type="MT320_SequenceB_TransactionDetails_34E_Type"/>
   <xs:element name="InterestRate" type="MT320_SequenceB_TransactionDetails_37G_Type"/>
   <xs:element name="DayCountFraction" type="MT320_SequenceB_TransactionDetails_14D_Type"/>
   <xs:element minOccurs="0" name="LastDayOfTheFirstInterestPeriod" type="MT320_SequenceB_TransactionDetails_30F_Type"/>
   <xs:element minOccurs="0" name="NumberOfDays" type="MT320_SequenceB_TransactionDetails_38J_Type"/>
   <xs:element minOccurs="0" name="PaymentClearingCentre" type="MT320_SequenceB_TransactionDetails_39M_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15B" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15C" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15D" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15E" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15F" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceG_TaxInformation">
  <xs:sequence>
   <xs:element name="TaxRate" type="MT320_SequenceG_TaxInformation_37L_Type"/>
   <xs:element name="TransactionCurrencyAndNetInterestAmount" type="MT320_SequenceG_TaxInformation_33B_Type"/>
   <xs:element minOccurs="0" name="ExchangeRate" type="MT320_SequenceG_TaxInformation_36_Type"/>
   <xs:element minOccurs="0" name="ReportingCurrencyAndTaxAmount" type="MT320_SequenceG_TaxInformation_33E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15G" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceH_AdditionalInformation">
  <xs:sequence>
   <xs:element minOccurs="0" name="ContactInformation" type="MT320_SequenceH_AdditionalInformation_29A_Type"/>
   <xs:element minOccurs="0" name="DealingMethod" type="MT320_SequenceH_AdditionalInformation_24D_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DealingBranchPartyA_A" type="MT320_SequenceH_AdditionalInformation_84A_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyA_B" type="MT320_SequenceH_AdditionalInformation_84B_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyA_D" type="MT320_SequenceH_AdditionalInformation_84D_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyA_J" type="MT320_SequenceH_AdditionalInformation_84J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DealingBranchPartyB_A" type="MT320_SequenceH_AdditionalInformation_85A_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyB_B" type="MT320_SequenceH_AdditionalInformation_85B_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyB_D" type="MT320_SequenceH_AdditionalInformation_85D_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyB_J" type="MT320_SequenceH_AdditionalInformation_85J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BrokerIdentification_A" type="MT320_SequenceH_AdditionalInformation_88A_Type"/>
    <xs:element minOccurs="0" name="BrokerIdentification_D" type="MT320_SequenceH_AdditionalInformation_88D_Type"/>
    <xs:element minOccurs="0" name="BrokerIdentification_J" type="MT320_SequenceH_AdditionalInformation_88J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="BrokersCommission" type="MT320_SequenceH_AdditionalInformation_71F_Type"/>
   <xs:element minOccurs="0" name="CounterpartysReference" type="MT320_SequenceH_AdditionalInformation_26H_Type"/>
   <xs:element minOccurs="0" name="BrokersReference" type="MT320_SequenceH_AdditionalInformation_21G_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CommissionAndFees" type="MT320_SequenceH_AdditionalInformation_34C_Type"/>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT320_SequenceH_AdditionalInformation_72_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15H" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts">
  <xs:sequence>
   <xs:element name="NumberOfRepetitions" type="MT320_SequenceI_AdditionalAmounts_18A_Type"/>
   <xs:element maxOccurs="unbounded" name="AMOUNT" type="MT320_SequenceI_AdditionalAmounts_AMOUNT"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT320_SequenceI_AdditionalAmounts_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT320_SequenceI_AdditionalAmounts_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT320_SequenceI_AdditionalAmounts_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT320_SequenceI_AdditionalAmounts_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT320_SequenceI_AdditionalAmounts_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT320_SequenceI_AdditionalAmounts_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT320_SequenceI_AdditionalAmounts_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT320_SequenceI_AdditionalAmounts_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT320_SequenceI_AdditionalAmounts_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT320_SequenceI_AdditionalAmounts_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT320_SequenceI_AdditionalAmounts_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT320_SequenceI_AdditionalAmounts_57J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15I" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT320_SequenceI_AdditionalAmounts_AMOUNT">
  <xs:sequence>
   <xs:element name="PaymentDate" type="MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type"/>
   <xs:element name="CurrencyPaymentAmount" type="MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:element name="MT320">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT320_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_TransactionDetails" type="MT320_SequenceB_TransactionDetails"/>
    <xs:element name="SequenceC_SettlementInstructionsforAmountsPayablebyPartyA" type="MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA"/>
    <xs:element name="SequenceD_SettlementInstructionsforAmountsPayablebyPartyB" type="MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB"/>
    <xs:element minOccurs="0" name="SequenceE_SettlementInstructionsforInterestsPayablebyPartyA" type="MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA"/>
    <xs:element minOccurs="0" name="SequenceF_SettlementInstructionsforInterestsPayablebyPartyB" type="MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB"/>
    <xs:element minOccurs="0" name="SequenceG_TaxInformation" type="MT320_SequenceG_TaxInformation"/>
    <xs:element minOccurs="0" name="SequenceH_AdditionalInformation" type="MT320_SequenceH_AdditionalInformation"/>
    <xs:element minOccurs="0" name="SequenceI_AdditionalAmounts" type="MT320_SequenceI_AdditionalAmounts"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

