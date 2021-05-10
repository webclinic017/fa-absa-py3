<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(/(CLSTIME|RNCTIME|SNDTIME)/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([+]|[-])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_13C_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern">
    <xs:attribute fixed="13C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_32A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern">
    <xs:attribute fixed="32A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_52A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern">
    <xs:attribute fixed="52A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_52D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern">
    <xs:attribute fixed="52D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_53B_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern">
    <xs:attribute fixed="53B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_54A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern">
    <xs:attribute fixed="54A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_54B_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern">
    <xs:attribute fixed="54B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_54D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern">
    <xs:attribute fixed="54D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_57B_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern">
    <xs:attribute fixed="57B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceA_GeneralInformation_72_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation_72_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceA_GeneralInformation_72_Type_Pattern">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern">
    <xs:attribute fixed="50A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern">
    <xs:attribute fixed="50F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern">
    <xs:attribute fixed="50K" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern">
    <xs:attribute fixed="52A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern">
    <xs:attribute fixed="52D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern">
    <xs:attribute fixed="56C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern">
    <xs:attribute fixed="57B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern">
    <xs:attribute fixed="57C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern">
    <xs:attribute fixed="59" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern">
    <xs:attribute fixed="59A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?((1|2|3)/(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,33}\n?){1,4}))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern">
    <xs:attribute fixed="59F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern">
    <xs:attribute fixed="70" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type">
  <xs:simpleContent>
   <xs:extension base="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern">
    <xs:attribute fixed="33B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT202COV_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="TransactionReferenceNumber" type="MT202COV_SequenceA_GeneralInformation_20_Type"/>
   <xs:element name="RelatedReference" type="MT202COV_SequenceA_GeneralInformation_21_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="TimeIndication" type="MT202COV_SequenceA_GeneralInformation_13C_Type"/>
   <xs:element name="DateCurrencyAmount" type="MT202COV_SequenceA_GeneralInformation_32A_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="OrderingInstitution_A" type="MT202COV_SequenceA_GeneralInformation_52A_Type"/>
    <xs:element minOccurs="0" name="OrderingInstitution_D" type="MT202COV_SequenceA_GeneralInformation_52D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="SendersCorrespondent_A" type="MT202COV_SequenceA_GeneralInformation_53A_Type"/>
    <xs:element minOccurs="0" name="SendersCorrespondent_B" type="MT202COV_SequenceA_GeneralInformation_53B_Type"/>
    <xs:element minOccurs="0" name="SendersCorrespondent_D" type="MT202COV_SequenceA_GeneralInformation_53D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ReceiversCorrespondent_A" type="MT202COV_SequenceA_GeneralInformation_54A_Type"/>
    <xs:element minOccurs="0" name="ReceiversCorrespondent_B" type="MT202COV_SequenceA_GeneralInformation_54B_Type"/>
    <xs:element minOccurs="0" name="ReceiversCorrespondent_D" type="MT202COV_SequenceA_GeneralInformation_54D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermedairy_A" type="MT202COV_SequenceA_GeneralInformation_56A_Type"/>
    <xs:element minOccurs="0" name="Intermedairy_D" type="MT202COV_SequenceA_GeneralInformation_56D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="AccountWithInstitution_A" type="MT202COV_SequenceA_GeneralInformation_57A_Type"/>
    <xs:element minOccurs="0" name="AccountWithInstitution_B" type="MT202COV_SequenceA_GeneralInformation_57B_Type"/>
    <xs:element minOccurs="0" name="AccountWithInstitution_D" type="MT202COV_SequenceA_GeneralInformation_57D_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="BeneficiaryInstitution_A" type="MT202COV_SequenceA_GeneralInformation_58A_Type"/>
    <xs:element name="BeneficiaryInstitution_D" type="MT202COV_SequenceA_GeneralInformation_58D_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT202COV_SequenceA_GeneralInformation_72_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails">
  <xs:sequence>
   <xs:choice>
    <xs:element name="OrderingCustomer_A" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type"/>
    <xs:element name="OrderingCustomer_F" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type"/>
    <xs:element name="OrderingCustomer_K" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="OrderingInstitution_A" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type"/>
    <xs:element minOccurs="0" name="OrderingInstitution_D" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="IntermediaryInstitution_A" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type"/>
    <xs:element minOccurs="0" name="IntermediaryInstitution_C" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type"/>
    <xs:element minOccurs="0" name="IntermediaryInstitution_D" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="AccountWithInstitution_A" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type"/>
    <xs:element minOccurs="0" name="AccountWithInstitution_B" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type"/>
    <xs:element minOccurs="0" name="AccountWithInstitution_C" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type"/>
    <xs:element minOccurs="0" name="AccountWithInstitution_D" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="BeneficiaryCustomer" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type"/>
    <xs:element name="BeneficiaryCustomer_A" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type"/>
    <xs:element name="BeneficiaryCustomer_F" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="RemittanceInformation" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type"/>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type"/>
   <xs:element minOccurs="0" name="CurrencyInstructedAmount" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:element name="MT202COV">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT202COV_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_UnderlyingCustomerCreditTransferDetails" type="MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

