<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT192_11S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{3}(\n)?[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(\n)?([0-9]{4}[0-9]{6})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT192_11S_Type">
  <xs:simpleContent>
   <xs:extension base="MT192_11S_Type_Pattern">
    <xs:attribute fixed="11S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT192_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT192_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT192_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT192_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT192_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT192_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT192_79_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,50}\n?){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT192_79_Type">
  <xs:simpleContent>
   <xs:extension base="MT192_79_Type_Pattern">
    <xs:attribute fixed="79" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:element name="MT192">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReferenceNumber" type="MT192_20_Type"/>
    <xs:element name="RelatedReference" type="MT192_21_Type"/>
    <xs:element name="MTAndDateOfTheOriginalMessage" type="MT192_11S_Type"/>
    <xs:element id="narrative" minOccurs="0" name="NarrativeDescriptionOfTheOriginalMessage" type="MT192_79_Type"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

