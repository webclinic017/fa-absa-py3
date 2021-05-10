<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT210_SEQUENCE1_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE1_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE1_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE1_25_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE1_25_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE1_25_Type_Pattern">
    <xs:attribute fixed="25" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE1_30_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE1_30_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE1_30_Type_Pattern">
    <xs:attribute fixed="30" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_50_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_50_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_50_Type_Pattern">
    <xs:attribute fixed="50" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_50C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_50C_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_50C_Type_Pattern">
    <xs:attribute fixed="50C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_50F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_50F_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_50F_Type_Pattern">
    <xs:attribute fixed="50F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_52A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_52A_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_52A_Type_Pattern">
    <xs:attribute fixed="52A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_52D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_52D_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_52D_Type_Pattern">
    <xs:attribute fixed="52D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT210_SEQUENCE2_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT210_SEQUENCE2_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT210_SEQUENCE2_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT210_SEQUENCE1">
  <xs:sequence>
   <xs:element name="TransactionReferenceNumber" type="MT210_SEQUENCE1_20_Type"/>
   <xs:element minOccurs="0" name="AccountIdentification" type="MT210_SEQUENCE1_25_Type"/>
   <xs:element name="ValueDate" type="MT210_SEQUENCE1_30_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT210_SEQUENCE2">
  <xs:sequence>
   <xs:element name="RelatedReference" type="MT210_SEQUENCE2_21_Type"/>
   <xs:element name="CurrencyCodeAmount" type="MT210_SEQUENCE2_32B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="OrderingCustomer" type="MT210_SEQUENCE2_50_Type"/>
    <xs:element minOccurs="0" name="OrderingCustomer_C" type="MT210_SEQUENCE2_50C_Type"/>
    <xs:element minOccurs="0" name="OrderingCustomer_F" type="MT210_SEQUENCE2_50F_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="OrderingInstitution_A" type="MT210_SEQUENCE2_52A_Type"/>
    <xs:element minOccurs="0" name="OrderingInstitution_D" type="MT210_SEQUENCE2_52D_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermedairy_A" type="MT210_SEQUENCE2_56A_Type"/>
    <xs:element minOccurs="0" name="Intermedairy_D" type="MT210_SEQUENCE2_56D_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:element name="MT210">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SEQUENCE1" type="MT210_SEQUENCE1"/>
    <xs:element maxOccurs="unbounded" name="SEQUENCE2" type="MT210_SEQUENCE2"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

