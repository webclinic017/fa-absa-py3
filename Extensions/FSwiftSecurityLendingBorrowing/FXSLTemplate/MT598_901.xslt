<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:complexType name="MT598_901_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_901_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_901_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_901_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_901_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_901_13E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{8}[0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_901_13E_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_901_13E_Type_Pattern">
    <xs:attribute fixed="13E" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_901_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_901_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_901_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_901_79_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{4}/[A-Z0-9]{1,3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_901_79_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_901_79_Type_Pattern">
    <xs:attribute fixed="79" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:element name="MT598_901">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_901_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_901_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_901_77E_Type"/>
    <xs:element name="Narrative" type="MT598_901_79_Type"/>
    <xs:element name="DateTimeIndicator" type="MT598_901_13E_Type"/>
    <xs:element name="RelatedReference" type="MT598_901_21_Type"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
