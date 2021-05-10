<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT598_132_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_132_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_132_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_132_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_132_26H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([A-Z]{1,2}[0-9]{1,6})?/[0-9]{1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_132_26H_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_132_26H_Type_Pattern">
    <xs:attribute fixed="26H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_132_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:element name="MT598_132">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_132_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_132_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_132_77E_Type"/>
    <xs:element name="SAFIRESLoanReference" type="MT598_132_26H_Type"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
