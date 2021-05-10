<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT598_171_BANDET_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT)//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_BANDET_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_BANDET_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_GENL_LINK_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RELA)//[A-Z]{2}[0-9]{6}/[0-9]{1,7}|:(UTRN)//.{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_GENL_LINK_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_GENL_LINK_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_BANDET_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/STRA/IORT/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_BANDET_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_BANDET_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_BANDET_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT)//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_BANDET_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_BANDET_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_BANDET_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BANN)//.{9})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_BANDET_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_BANDET_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_171_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_GENL_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_GENL_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_GENL_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_171_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_171_GENL_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((NEWM))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_171_GENL_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_171_GENL_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_171_GENL_LINK">
  <xs:sequence>
   <xs:element name="InternalTrdRef_UTI" type="MT598_171_GENL_LINK_20C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_171_GENL">
  <xs:sequence>
   <xs:element name="FunctionOfMessage" type="MT598_171_GENL_23G_Type"/>
   <xs:element name="PreparationDateAndTime" type="MT598_171_GENL_98C_Type"/>
   <xs:element maxOccurs="unbounded" name="LINK" type="MT598_171_GENL_LINK"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_171_BANDET">
  <xs:sequence>
   <xs:element name="BANReference" type="MT598_171_BANDET_20C_Type"/>
   <xs:element name="SORAccount" type="MT598_171_BANDET_97B_Type"/>
   <xs:element name="NominalValue" type="MT598_171_BANDET_36B_Type"/>
   <xs:element minOccurs="0" name="SettlementAmount" type="MT598_171_BANDET_19A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:element name="MT598_171">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_171_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_171_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_171_77E_Type"/>
    <xs:element name="GENL" type="MT598_171_GENL"/>
    <xs:element maxOccurs="unbounded" name="BANDET" type="MT598_171_BANDET"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
