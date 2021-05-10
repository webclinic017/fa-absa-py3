<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MTx99_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MTx99_20_Type">
  <xs:simpleContent>
   <xs:extension base="MTx99_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MTx99_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MTx99_21_Type">
  <xs:simpleContent>
   <xs:extension base="MTx99_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MTx99_79_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,50}\n?){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MTx99_79_Type">
  <xs:simpleContent>
   <xs:extension base="MTx99_79_Type_Pattern">
    <xs:attribute fixed="79" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:element name="MTx99">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReferenceNumber" type="MTx99_20_Type"/>
    <xs:element minOccurs="0" name="RelatedReference" type="MTx99_21_Type"/>
    <xs:element id="narrative" name="Narrative" type="MTx99_79_Type"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

