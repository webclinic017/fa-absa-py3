<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT598_902_GENL_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(ISIN {1}[A-Z0-9]{12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_902_GENL_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_902_GENL_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_902_GENL_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EROR)//.{4}/.{4}/.{4}/.{4}/.{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_902_GENL_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_902_GENL_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_902_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_902_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_902_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_902_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_902_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_902_GENL_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RELA)//.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_902_GENL_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_902_GENL_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_902_GENL_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_902_GENL_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_902_GENL_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_902_16R_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT598_902_GENL">
  <xs:sequence>
   <xs:element name="RelatedReference" type="MT598_902_GENL_20C_Type"/>
   <xs:element name="PreparationDateAndTime" type="MT598_902_GENL_98C_Type"/>
   <xs:element minOccurs="0" name="IdentificationOfSecurity" type="MT598_902_GENL_35B_Type"/>
   <xs:element name="ErrorDetails" type="MT598_902_GENL_70D_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:element name="MT598_902">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_902_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_902_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_902_77E_Type"/>
    <xs:element name="GENL" type="MT598_902_GENL"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
