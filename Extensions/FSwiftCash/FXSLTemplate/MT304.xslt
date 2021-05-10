<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_22A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMND|CAMN|CCAN|CANC|DUPL|NEWT|CNEW))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_22A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_22A_Type_Pattern">
    <xs:attribute fixed="22A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_94A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AFWD|ANDF|ASET))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_94A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_94A_Type_Pattern">
    <xs:attribute fixed="94A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_17O_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_17O_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_17O_Type_Pattern">
    <xs:attribute fixed="17O" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_17F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_17F_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_17F_Type_Pattern">
    <xs:attribute fixed="17F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_17N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_17N_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_17N_Type_Pattern">
    <xs:attribute fixed="17N" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_83A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_83A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_83A_Type_Pattern">
    <xs:attribute fixed="83A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_83J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_83J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_83J_Type_Pattern">
    <xs:attribute fixed="83J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_82A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_82A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_82A_Type_Pattern">
    <xs:attribute fixed="82A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_82J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_82J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_82J_Type_Pattern">
    <xs:attribute fixed="82J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_87A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_87A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_87A_Type_Pattern">
    <xs:attribute fixed="87A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_87J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_87J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_87J_Type_Pattern">
    <xs:attribute fixed="87J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_81A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_81A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_81A_Type_Pattern">
    <xs:attribute fixed="81A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_81D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_81D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_81D_Type_Pattern">
    <xs:attribute fixed="81D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_81J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_81J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_81J_Type_Pattern">
    <xs:attribute fixed="81J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_89A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_89A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_89A_Type_Pattern">
    <xs:attribute fixed="89A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_89D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_89D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_89D_Type_Pattern">
    <xs:attribute fixed="89D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_89J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_89J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_89J_Type_Pattern">
    <xs:attribute fixed="89J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_17I_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(N|[0-9])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_17I_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_17I_Type_Pattern">
    <xs:attribute fixed="17I" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_77H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))?(//[0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_77H_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_77H_Type_Pattern">
    <xs:attribute fixed="77H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_14C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_14C_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_14C_Type_Pattern">
    <xs:attribute fixed="14C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_32E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_32E_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_32E_Type_Pattern">
    <xs:attribute fixed="32E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_30U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_30U_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_30U_Type_Pattern">
    <xs:attribute fixed="30U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_21A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_21A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_21A_Type_Pattern">
    <xs:attribute fixed="21A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceA_GeneralInformation_14E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation_14E_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceA_GeneralInformation_14E_Type_Pattern">
    <xs:attribute fixed="14E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_30T_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern">
    <xs:attribute fixed="30T" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_30V_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern">
    <xs:attribute fixed="30V" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_36_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern">
    <xs:attribute fixed="36" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_39M_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern">
    <xs:attribute fixed="39M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern">
    <xs:attribute fixed="33B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_21A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern">
    <xs:attribute fixed="21A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_21G_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern">
    <xs:attribute fixed="21G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern">
    <xs:attribute fixed="22L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern">
    <xs:attribute fixed="22M" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern">
    <xs:attribute fixed="22N" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
    <xs:attribute fixed="22P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
    <xs:attribute fixed="22R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_22U_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern">
    <xs:attribute fixed="22U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_22V_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern">
    <xs:attribute fixed="22V" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_98D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern">
    <xs:attribute fixed="98D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_98G_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern">
    <xs:attribute fixed="98G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_29A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern">
    <xs:attribute fixed="29A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_34C_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern">
    <xs:attribute fixed="34C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_72_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceD_AccountingInformation_21P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceD_AccountingInformation_21P_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceD_AccountingInformation_21P_Type_Pattern">
    <xs:attribute fixed="21P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceD_AccountingInformation_17G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceD_AccountingInformation_17G_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceD_AccountingInformation_17G_Type_Pattern">
    <xs:attribute fixed="17G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceD_AccountingInformation_32G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceD_AccountingInformation_32G_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceD_AccountingInformation_32G_Type_Pattern">
    <xs:attribute fixed="32G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceD_AccountingInformation_34B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceD_AccountingInformation_34B_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceD_AccountingInformation_34B_Type_Pattern">
    <xs:attribute fixed="34B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceD_AccountingInformation_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceD_AccountingInformation_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceD_AccountingInformation_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_17G_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern">
    <xs:attribute fixed="17G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_32G_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern">
    <xs:attribute fixed="32G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersReference" type="MT304_SequenceA_GeneralInformation_20_Type"/>
   <xs:element minOccurs="0" name="RelatedReference" type="MT304_SequenceA_GeneralInformation_21_Type"/>
   <xs:element name="TypeOfOperation" type="MT304_SequenceA_GeneralInformation_22A_Type"/>
   <xs:element name="ScopeOfOperation" type="MT304_SequenceA_GeneralInformation_94A_Type"/>
   <xs:element minOccurs="0" name="OpenIndicator" type="MT304_SequenceA_GeneralInformation_17O_Type"/>
   <xs:element minOccurs="0" name="FinalCloseIndicator" type="MT304_SequenceA_GeneralInformation_17F_Type"/>
   <xs:element minOccurs="0" name="NetSettlementIndicator" type="MT304_SequenceA_GeneralInformation_17N_Type"/>
   <xs:choice>
    <xs:element name="Fund_A" type="MT304_SequenceA_GeneralInformation_83A_Type"/>
    <xs:element name="Fund_J" type="MT304_SequenceA_GeneralInformation_83J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="FundManager_A" type="MT304_SequenceA_GeneralInformation_82A_Type"/>
    <xs:element name="FundManager_J" type="MT304_SequenceA_GeneralInformation_82J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ExecutingBroker_A" type="MT304_SequenceA_GeneralInformation_87A_Type"/>
    <xs:element name="ExecutingBroker_J" type="MT304_SequenceA_GeneralInformation_87J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_A" type="MT304_SequenceA_GeneralInformation_81A_Type"/>
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_D" type="MT304_SequenceA_GeneralInformation_81D_Type"/>
    <xs:element minOccurs="0" name="CentralCounterpartyClearingHouse_J" type="MT304_SequenceA_GeneralInformation_81J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ClearingBroker_A" type="MT304_SequenceA_GeneralInformation_89A_Type"/>
    <xs:element minOccurs="0" name="ClearingBroker_D" type="MT304_SequenceA_GeneralInformation_89D_Type"/>
    <xs:element minOccurs="0" name="ClearingBroker_J" type="MT304_SequenceA_GeneralInformation_89J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="PaymentVersusPaymentSettlementIndicator" type="MT304_SequenceA_GeneralInformation_17I_Type"/>
   <xs:element minOccurs="0" name="TypeDateVersionOfTheAgreement" type="MT304_SequenceA_GeneralInformation_77H_Type"/>
   <xs:element minOccurs="0" name="YearOfDefinitions" type="MT304_SequenceA_GeneralInformation_14C_Type"/>
   <xs:element minOccurs="0" name="SettlementCurrency" type="MT304_SequenceA_GeneralInformation_32E_Type"/>
   <xs:element minOccurs="0" name="ValuationDate" type="MT304_SequenceA_GeneralInformation_30U_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SettlementRateSource" type="MT304_SequenceA_GeneralInformation_14S_Type"/>
   <xs:element minOccurs="0" name="ReferenceToOpeningInstruction" type="MT304_SequenceA_GeneralInformation_21A_Type"/>
   <xs:element minOccurs="0" name="ClearingOrSettlementSession" type="MT304_SequenceA_GeneralInformation_14E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15A" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails">
  <xs:sequence>
   <xs:element name="TradeDate" type="MT304_SequenceB_ForexTransactionDetails_30T_Type"/>
   <xs:element name="ValueDate" type="MT304_SequenceB_ForexTransactionDetails_30V_Type"/>
   <xs:element name="ExchangeRate" type="MT304_SequenceB_ForexTransactionDetails_36_Type"/>
   <xs:element minOccurs="0" name="PaymentClearingCentre" type="MT304_SequenceB_ForexTransactionDetails_39M_Type"/>
   <xs:element name="SubsequenceB1_AmountBought" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought"/>
   <xs:element name="SubsequenceB2_AmountSold" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold"/>
  </xs:sequence>
  <xs:attribute fixed="15B" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought">
  <xs:sequence>
   <xs:element name="CurrencyAmountBought" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type"/>
   <xs:choice>
    <xs:element name="DeliveryAgent_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type"/>
    <xs:element name="DeliveryAgent_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ReceivingAgent_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type"/>
    <xs:element minOccurs="0" name="ReceivingAgent_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold">
  <xs:sequence>
   <xs:element name="CurrencyAmountSold" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation">
  <xs:sequence>
   <xs:element minOccurs="0" name="ReferenceToTheAssociatedTrade" type="MT304_SequenceC_OptionalGeneralInformation_21A_Type"/>
   <xs:element minOccurs="0" name="ExecutingBrokersReference" type="MT304_SequenceC_OptionalGeneralInformation_21G_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceC1_UniqueTransactionIdentifier" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier"/>
   <xs:element minOccurs="0" name="UnderlyingProductIdentifier" type="MT304_SequenceC_OptionalGeneralInformation_22U_Type"/>
   <xs:element minOccurs="0" name="IdentificationOfFinancialInstrument" type="MT304_SequenceC_OptionalGeneralInformation_35B_Type"/>
   <xs:element minOccurs="0" name="ExecutionVenue" type="MT304_SequenceC_OptionalGeneralInformation_22V_Type"/>
   <xs:element minOccurs="0" name="ExecutionTimestamp" type="MT304_SequenceC_OptionalGeneralInformation_98D_Type"/>
   <xs:element minOccurs="0" name="ClearingTimestamp" type="MT304_SequenceC_OptionalGeneralInformation_98G_Type"/>
   <xs:element minOccurs="0" name="ContactInformation" type="MT304_SequenceC_OptionalGeneralInformation_29A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CommissionAndFees" type="MT304_SequenceC_OptionalGeneralInformation_34C_Type"/>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT304_SequenceC_OptionalGeneralInformation_72_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15C" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="ReportingJurisdiction" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type"/>
   <xs:element name="UTINamespaceIssuerCode" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type"/>
   <xs:element name="TransactionIdentifier" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceC1a_PriorUniqueTransactionIdentifier" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="PUTINamespaceIssuerCode" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type"/>
   <xs:element name="PriorTransactionIdentifier" type="MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceD_AccountingInformation">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="ReferenceToPreviousDeals" type="MT304_SequenceD_AccountingInformation_21P_Type"/>
   <xs:element minOccurs="0" name="GainIndicator" type="MT304_SequenceD_AccountingInformation_17G_Type"/>
   <xs:element minOccurs="0" name="CurrencyAmount" type="MT304_SequenceD_AccountingInformation_32G_Type"/>
   <xs:element minOccurs="0" name="CommissionAndFeesCurrencyAndAmount" type="MT304_SequenceD_AccountingInformation_34B_Type"/>
   <xs:element minOccurs="0" name="CommissionAndFeesSettlementDate" type="MT304_SequenceD_AccountingInformation_30F_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15D" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT304_SequenceE_NetAmountToBeSettled">
  <xs:sequence>
   <xs:element name="GainIndicator" type="MT304_SequenceE_NetAmountToBeSettled_17G_Type"/>
   <xs:element name="CurrencyAmount" type="MT304_SequenceE_NetAmountToBeSettled_32G_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT304_SequenceE_NetAmountToBeSettled_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT304_SequenceE_NetAmountToBeSettled_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT304_SequenceE_NetAmountToBeSettled_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT304_SequenceE_NetAmountToBeSettled_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT304_SequenceE_NetAmountToBeSettled_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT304_SequenceE_NetAmountToBeSettled_56J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ReceivingAgent_A" type="MT304_SequenceE_NetAmountToBeSettled_57A_Type"/>
    <xs:element minOccurs="0" name="ReceivingAgent_D" type="MT304_SequenceE_NetAmountToBeSettled_57D_Type"/>
    <xs:element minOccurs="0" name="ReceivingAgent_J" type="MT304_SequenceE_NetAmountToBeSettled_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT304_SequenceE_NetAmountToBeSettled_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT304_SequenceE_NetAmountToBeSettled_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT304_SequenceE_NetAmountToBeSettled_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15E" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT304">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT304_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_ForexTransactionDetails" type="MT304_SequenceB_ForexTransactionDetails"/>
    <xs:element minOccurs="0" name="SequenceC_OptionalGeneralInformation" type="MT304_SequenceC_OptionalGeneralInformation"/>
    <xs:element minOccurs="0" name="SequenceD_AccountingInformation" type="MT304_SequenceD_AccountingInformation"/>
    <xs:element minOccurs="0" name="SequenceE_NetAmountToBeSettled" type="MT304_SequenceE_NetAmountToBeSettled"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

