<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_22A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMND|CANC|DUPL|EXOP|NEWT))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_22A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_22A_Type_Pattern">
    <xs:attribute fixed="22A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_94A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AGNT|BILA|BROK))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_94A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_94A_Type_Pattern">
    <xs:attribute fixed="94A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_22C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_22C_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_22C_Type_Pattern">
    <xs:attribute fixed="22C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_17T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_17T_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_17T_Type_Pattern">
    <xs:attribute fixed="17T" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_17U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_17U_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_17U_Type_Pattern">
    <xs:attribute fixed="17U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_17I_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_17I_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_17I_Type_Pattern">
    <xs:attribute fixed="17I" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_82A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_82A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_82A_Type_Pattern">
    <xs:attribute fixed="82A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_82J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_82J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_82J_Type_Pattern">
    <xs:attribute fixed="82J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_87A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_87A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_87A_Type_Pattern">
    <xs:attribute fixed="87A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_87J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_87J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_87J_Type_Pattern">
    <xs:attribute fixed="87J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_83A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_83A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_83A_Type_Pattern">
    <xs:attribute fixed="83A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_83J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_83J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_83J_Type_Pattern">
    <xs:attribute fixed="83J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_77H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{8})?(//[0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_77H_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_77H_Type_Pattern">
    <xs:attribute fixed="77H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_77D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_77D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_77D_Type_Pattern">
    <xs:attribute fixed="77D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_14C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_14C_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_14C_Type_Pattern">
    <xs:attribute fixed="14C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_17F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_17F_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_17F_Type_Pattern">
    <xs:attribute fixed="17F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_17O_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_17O_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_17O_Type_Pattern">
    <xs:attribute fixed="17O" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_32E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_32E_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_32E_Type_Pattern">
    <xs:attribute fixed="32E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_30U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_30U_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_30U_Type_Pattern">
    <xs:attribute fixed="30U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/[0-9]{4}/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_21A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_21A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_21A_Type_Pattern">
    <xs:attribute fixed="21A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceA_GeneralInformation_14E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation_14E_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceA_GeneralInformation_14E_Type_Pattern">
    <xs:attribute fixed="14E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_30T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_30T_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_30T_Type_Pattern">
    <xs:attribute fixed="30T" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_30V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_30V_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_30V_Type_Pattern">
    <xs:attribute fixed="30V" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_36_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_36_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_36_Type_Pattern">
    <xs:attribute fixed="36" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_39M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_39M_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_39M_Type_Pattern">
    <xs:attribute fixed="39M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SubSequenceB1_AmountBought_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SubSequenceB1_AmountBought_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SubSequenceB1_AmountBought_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SubSequenceB2_AmountSold_33B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SubSequenceB2_AmountSold_33B_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SubSequenceB2_AmountSold_33B_Type_Pattern">
    <xs:attribute fixed="33B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_29A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern">
    <xs:attribute fixed="29A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((BROK|ELEC|FAXT|PHON|TELX)(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_24D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern">
    <xs:attribute fixed="24D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_84A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern">
    <xs:attribute fixed="84A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_84B_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern">
    <xs:attribute fixed="84B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_84D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern">
    <xs:attribute fixed="84D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_84J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern">
    <xs:attribute fixed="84J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_85A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern">
    <xs:attribute fixed="85A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_85B_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern">
    <xs:attribute fixed="85B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_85D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern">
    <xs:attribute fixed="85D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_85J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern">
    <xs:attribute fixed="85J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_88A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern">
    <xs:attribute fixed="88A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_88D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern">
    <xs:attribute fixed="88D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_88J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern">
    <xs:attribute fixed="88J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_71F_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern">
    <xs:attribute fixed="71F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_26H_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern">
    <xs:attribute fixed="26H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_21G_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern">
    <xs:attribute fixed="21G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation_72_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(N|[0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern">
    <xs:attribute fixed="17A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_16A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern">
    <xs:attribute fixed="16A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern">
    <xs:attribute fixed="22L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern">
    <xs:attribute fixed="91A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern">
    <xs:attribute fixed="91D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern">
    <xs:attribute fixed="91J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern">
    <xs:attribute fixed="22M" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern">
    <xs:attribute fixed="22N" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
    <xs:attribute fixed="22P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
    <xs:attribute fixed="22R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_81A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_81A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_81A_Type_Pattern">
    <xs:attribute fixed="81A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_81D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_81D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_81D_Type_Pattern">
    <xs:attribute fixed="81D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_81J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_81J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_81J_Type_Pattern">
    <xs:attribute fixed="81J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_89A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_89A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_89A_Type_Pattern">
    <xs:attribute fixed="89A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_89D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_89D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_89D_Type_Pattern">
    <xs:attribute fixed="89D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_89J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_89J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_89J_Type_Pattern">
    <xs:attribute fixed="89J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_96A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_96A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_96A_Type_Pattern">
    <xs:attribute fixed="96A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_96D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_96D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_96D_Type_Pattern">
    <xs:attribute fixed="96D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_96J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_96J_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_96J_Type_Pattern">
    <xs:attribute fixed="96J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_22S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((C|P)/(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_22S_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_22S_Type_Pattern">
    <xs:attribute fixed="22S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_22T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_22T_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_22T_Type_Pattern">
    <xs:attribute fixed="22T" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17E_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17E_Type_Pattern">
    <xs:attribute fixed="17E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_22U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((FXFORW|FXNDFO|FXSPOT|FXSWAP))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_22U_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_22U_Type_Pattern">
    <xs:attribute fixed="22U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((A|P|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17H_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17H_Type_Pattern">
    <xs:attribute fixed="17H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((F|O|P|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17P_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17P_Type_Pattern">
    <xs:attribute fixed="17P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_22V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_22V_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_22V_Type_Pattern">
    <xs:attribute fixed="22V" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_98D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_98D_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_98D_Type_Pattern">
    <xs:attribute fixed="98D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17W_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17W_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17W_Type_Pattern">
    <xs:attribute fixed="17W" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_22W_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,42})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_22W_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_22W_Type_Pattern">
    <xs:attribute fixed="22W" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17Y_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((F|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17Y_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17Y_Type_Pattern">
    <xs:attribute fixed="17Y" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17Z_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17Z_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17Z_Type_Pattern">
    <xs:attribute fixed="17Z" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_22Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_22Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_22Q_Type_Pattern">
    <xs:attribute fixed="22Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17L_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17L_Type_Pattern">
    <xs:attribute fixed="17L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((A|C|F|I|L|O|R|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17M_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17M_Type_Pattern">
    <xs:attribute fixed="17M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17Q_Type_Pattern">
    <xs:attribute fixed="17Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17S_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17S_Type_Pattern">
    <xs:attribute fixed="17S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_17X_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_17X_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_17X_Type_Pattern">
    <xs:attribute fixed="17X" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_98G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_98G_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_98G_Type_Pattern">
    <xs:attribute fixed="98G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_98H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_98H_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_98H_Type_Pattern">
    <xs:attribute fixed="98H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_34C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_34C_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_34C_Type_Pattern">
    <xs:attribute fixed="34C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceE_ReportingInformation_77A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,20})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_77A_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceE_ReportingInformation_77A_Type_Pattern">
    <xs:attribute fixed="77A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceF_PostTradeEvents_21H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((EAMT|PEAM|PRUR|PRUW|ROLL|UNWD|UNWR)[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceF_PostTradeEvents_21H_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceF_PostTradeEvents_21H_Type_Pattern">
    <xs:attribute fixed="21H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceF_PostTradeEvents_21F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceF_PostTradeEvents_21F_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceF_PostTradeEvents_21F_Type_Pattern">
    <xs:attribute fixed="21F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceF_PostTradeEvents_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceF_PostTradeEvents_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceF_PostTradeEvents_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceF_PostTradeEvents_32H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceF_PostTradeEvents_32H_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceF_PostTradeEvents_32H_Type_Pattern">
    <xs:attribute fixed="32H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_SequenceF_PostTradeEvents_33E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceF_PostTradeEvents_33E_Type">
  <xs:simpleContent>
   <xs:extension base="MT300_SequenceF_PostTradeEvents_33E_Type_Pattern">
    <xs:attribute fixed="33E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT300_15A_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:simpleType name="MT300_15B_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:simpleType name="MT300_15C_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:simpleType name="MT300_15D_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:simpleType name="MT300_15E_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT300_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersReference" type="MT300_SequenceA_GeneralInformation_20_Type"/>
   <xs:element minOccurs="0" name="RelatedReference" type="MT300_SequenceA_GeneralInformation_21_Type"/>
   <xs:element name="TypeOfOperation" type="MT300_SequenceA_GeneralInformation_22A_Type"/>
   <xs:element minOccurs="0" name="ScopeOfOperation" type="MT300_SequenceA_GeneralInformation_94A_Type"/>
   <xs:element name="CommonReference" type="MT300_SequenceA_GeneralInformation_22C_Type"/>
   <xs:element minOccurs="0" name="BlockTradeIndicator" type="MT300_SequenceA_GeneralInformation_17T_Type"/>
   <xs:element minOccurs="0" name="SplitSettlementIndicator" type="MT300_SequenceA_GeneralInformation_17U_Type"/>
   <xs:element minOccurs="0" name="PaymentVersusPaymentSettlementIndicator" type="MT300_SequenceA_GeneralInformation_17I_Type"/>
   <xs:choice>
    <xs:element name="PartyA_A" type="MT300_SequenceA_GeneralInformation_82A_Type"/>
    <xs:element name="PartyA_J" type="MT300_SequenceA_GeneralInformation_82J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="PartyB_A" type="MT300_SequenceA_GeneralInformation_87A_Type"/>
    <xs:element name="PartyB_J" type="MT300_SequenceA_GeneralInformation_87J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_A" type="MT300_SequenceA_GeneralInformation_83A_Type"/>
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_J" type="MT300_SequenceA_GeneralInformation_83J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="TypeDateVersionOfAgreement" type="MT300_SequenceA_GeneralInformation_77H_Type"/>
   <xs:element minOccurs="0" name="TermsAndConditions" type="MT300_SequenceA_GeneralInformation_77D_Type"/>
   <xs:element minOccurs="0" name="YearOfDefinitions" type="MT300_SequenceA_GeneralInformation_14C_Type"/>
   <xs:element minOccurs="0" name="Non-DeliverableIndicator" type="MT300_SequenceA_GeneralInformation_17F_Type"/>
   <xs:element minOccurs="0" name="NDFOpenIndicator" type="MT300_SequenceA_GeneralInformation_17O_Type"/>
   <xs:element minOccurs="0" name="SettlementCurrency" type="MT300_SequenceA_GeneralInformation_32E_Type"/>
   <xs:element minOccurs="0" name="ValuationDate" type="MT300_SequenceA_GeneralInformation_30U_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SettlementRateSource" type="MT300_SequenceA_GeneralInformation_14S_Type"/>
   <xs:element minOccurs="0" name="ReferenceToOpeningConfirmation" type="MT300_SequenceA_GeneralInformation_21A_Type"/>
   <xs:element minOccurs="0" name="ClearingOrSettlementSession" type="MT300_SequenceA_GeneralInformation_14E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15A" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails">
  <xs:sequence>
   <xs:element name="TradeDate" type="MT300_SequenceB_TransactionDetails_30T_Type"/>
   <xs:element name="ValueDate" type="MT300_SequenceB_TransactionDetails_30V_Type"/>
   <xs:element name="ExchangeRate" type="MT300_SequenceB_TransactionDetails_36_Type"/>
   <xs:element minOccurs="0" name="PaymentClearingCentre" type="MT300_SequenceB_TransactionDetails_39M_Type"/>
   <xs:element name="SubSequenceB1_AmountBought" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought"/>
   <xs:element name="SubSequenceB2_AmountSold" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold"/>
  </xs:sequence>
  <xs:attribute fixed="15B" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought">
  <xs:sequence>
   <xs:element name="CurrencyAmount" type="MT300_SubSequenceB1_AmountBought_32B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold">
  <xs:sequence>
   <xs:element name="CurrencyAmount" type="MT300_SubSequenceB2_AmountSold_33B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceC_OptionalGeneralInformation">
  <xs:sequence>
   <xs:element minOccurs="0" name="ContactInformation" type="MT300_SequenceC_OptionalGeneralInformation_29A_Type"/>
   <xs:element minOccurs="0" name="DealingMethod" type="MT300_SequenceC_OptionalGeneralInformation_24D_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DealingBranchPartyA_A" type="MT300_SequenceC_OptionalGeneralInformation_84A_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyA_B" type="MT300_SequenceC_OptionalGeneralInformation_84B_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyA_D" type="MT300_SequenceC_OptionalGeneralInformation_84D_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyA_J" type="MT300_SequenceC_OptionalGeneralInformation_84J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DealingBranchPartyB_A" type="MT300_SequenceC_OptionalGeneralInformation_85A_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyB_B" type="MT300_SequenceC_OptionalGeneralInformation_85B_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyB_D" type="MT300_SequenceC_OptionalGeneralInformation_85D_Type"/>
    <xs:element minOccurs="0" name="DealingBranchPartyB_J" type="MT300_SequenceC_OptionalGeneralInformation_85J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BrokerIdentification_A" type="MT300_SequenceC_OptionalGeneralInformation_88A_Type"/>
    <xs:element minOccurs="0" name="BrokerIdentification_D" type="MT300_SequenceC_OptionalGeneralInformation_88D_Type"/>
    <xs:element minOccurs="0" name="BrokerIdentification_J" type="MT300_SequenceC_OptionalGeneralInformation_88J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="BrokersCommission" type="MT300_SequenceC_OptionalGeneralInformation_71F_Type"/>
   <xs:element minOccurs="0" name="CounterpartysReference" type="MT300_SequenceC_OptionalGeneralInformation_26H_Type"/>
   <xs:element minOccurs="0" name="BrokersReference" type="MT300_SequenceC_OptionalGeneralInformation_21G_Type"/>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT300_SequenceC_OptionalGeneralInformation_72_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15C" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="SettlementDetails" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails"/>
   <xs:element name="NumberOfSettlements" type="MT300_SequenceD_SplitSettlementDetails_16A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15D" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceD_SplitSettlementDetails_SettlementDetails">
  <xs:sequence>
   <xs:element name="BuySellIndicator" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type"/>
   <xs:element name="CurrencyAmount" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceE1_ReportingParties" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_A" type="MT300_SequenceE_ReportingInformation_81A_Type"/>
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_D" type="MT300_SequenceE_ReportingInformation_81D_Type"/>
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_J" type="MT300_SequenceE_ReportingInformation_81J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ClearingBroker_A" type="MT300_SequenceE_ReportingInformation_89A_Type"/>
    <xs:element minOccurs="0" name="ClearingBroker_D" type="MT300_SequenceE_ReportingInformation_89D_Type"/>
    <xs:element minOccurs="0" name="ClearingBroker_J" type="MT300_SequenceE_ReportingInformation_89J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ClearingExceptionParty_A" type="MT300_SequenceE_ReportingInformation_96A_Type"/>
    <xs:element minOccurs="0" name="ClearingExceptionParty_D" type="MT300_SequenceE_ReportingInformation_96D_Type"/>
    <xs:element minOccurs="0" name="ClearingExceptionParty_J" type="MT300_SequenceE_ReportingInformation_96J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="ClearingBrokerIdentification" type="MT300_SequenceE_ReportingInformation_22S_Type"/>
   <xs:element minOccurs="0" name="ClearedProductIdentification" type="MT300_SequenceE_ReportingInformation_22T_Type"/>
   <xs:element minOccurs="0" name="ClearingThresholdIndicator" type="MT300_SequenceE_ReportingInformation_17E_Type"/>
   <xs:element minOccurs="0" name="UnderlyingProductIdentifier" type="MT300_SequenceE_ReportingInformation_22U_Type"/>
   <xs:element minOccurs="0" name="IdentificationOfFinancialInstrument" type="MT300_SequenceE_ReportingInformation_35B_Type"/>
   <xs:element minOccurs="0" name="AllocationIndicator" type="MT300_SequenceE_ReportingInformation_17H_Type"/>
   <xs:element minOccurs="0" name="CollateralisationIndicator" type="MT300_SequenceE_ReportingInformation_17P_Type"/>
   <xs:element minOccurs="0" name="ExecutionVenue" type="MT300_SequenceE_ReportingInformation_22V_Type"/>
   <xs:element minOccurs="0" name="ExecutionTimestamp" type="MT300_SequenceE_ReportingInformation_98D_Type"/>
   <xs:element minOccurs="0" name="NonStandardFlag" type="MT300_SequenceE_ReportingInformation_17W_Type"/>
   <xs:element minOccurs="0" name="LinkSwapIdentification" type="MT300_SequenceE_ReportingInformation_22W_Type"/>
   <xs:element minOccurs="0" name="FinancialNatureOfCounterpartyIndicator" type="MT300_SequenceE_ReportingInformation_17Y_Type"/>
   <xs:element minOccurs="0" name="CollateralPortfolioIndicator" type="MT300_SequenceE_ReportingInformation_17Z_Type"/>
   <xs:element minOccurs="0" name="CollateralPortfolioCode" type="MT300_SequenceE_ReportingInformation_22Q_Type"/>
   <xs:element minOccurs="0" name="PortfolioCompressionIndicator" type="MT300_SequenceE_ReportingInformation_17L_Type"/>
   <xs:element minOccurs="0" name="CorporateSectorIndicator" type="MT300_SequenceE_ReportingInformation_17M_Type"/>
   <xs:element minOccurs="0" name="TradeWithNonEEACounterpartyIndicator" type="MT300_SequenceE_ReportingInformation_17Q_Type"/>
   <xs:element minOccurs="0" name="IntragroupTradeIndicator" type="MT300_SequenceE_ReportingInformation_17S_Type"/>
   <xs:element minOccurs="0" name="CommercialOrTreasuryFinancingIndicator" type="MT300_SequenceE_ReportingInformation_17X_Type"/>
   <xs:element minOccurs="0" name="ConfirmationTimestamp" type="MT300_SequenceE_ReportingInformation_98G_Type"/>
   <xs:element minOccurs="0" name="ClearingTimestamp" type="MT300_SequenceE_ReportingInformation_98H_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CommissionAndFees" type="MT300_SequenceE_ReportingInformation_34C_Type"/>
   <xs:element minOccurs="0" name="AdditionalReportingInformation" type="MT300_SequenceE_ReportingInformation_77A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15E" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties">
  <xs:sequence>
   <xs:element name="ReportingJurisdiction" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ReportingParty_A" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type"/>
    <xs:element minOccurs="0" name="ReportingParty_D" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type"/>
    <xs:element minOccurs="0" name="ReportingParty_J" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceE1a_UniqueTransactionIdentifier" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="UTINamespaceIssuerCode" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type"/>
   <xs:element name="TransactionIdentifier" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceE1a1_PriorUniqueTransactionIdentifier" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="PUTINamespaceIssuerCode" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type"/>
   <xs:element name="PriorTransactionIdentifier" type="MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT300_SequenceF_PostTradeEvents">
  <xs:sequence>
   <xs:element name="EventTypeAndReference" type="MT300_SequenceF_PostTradeEvents_21H_Type"/>
   <xs:element minOccurs="0" name="UnderlyingLiabilityReference" type="MT300_SequenceF_PostTradeEvents_21F_Type"/>
   <xs:element minOccurs="0" name="ProfitAndLossSettlementDate" type="MT300_SequenceF_PostTradeEvents_30F_Type"/>
   <xs:element minOccurs="0" name="ProfitAndLossSettlementAmount" type="MT300_SequenceF_PostTradeEvents_32H_Type"/>
   <xs:element minOccurs="0" name="OutstandingSettlementAmount" type="MT300_SequenceF_PostTradeEvents_33E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15F" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT300">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT300_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_TransactionDetails" type="MT300_SequenceB_TransactionDetails"/>
    <xs:element minOccurs="0" name="SequenceC_OptionalGeneralInformation" type="MT300_SequenceC_OptionalGeneralInformation"/>
    <xs:element minOccurs="0" name="SequenceD_SplitSettlementDetails" type="MT300_SequenceD_SplitSettlementDetails"/>
    <xs:element minOccurs="0" name="SequenceE_ReportingInformation" type="MT300_SequenceE_ReportingInformation"/>
    <xs:element minOccurs="0" name="SequenceF_PostTradeEvents" type="MT300_SequenceF_PostTradeEvents"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

