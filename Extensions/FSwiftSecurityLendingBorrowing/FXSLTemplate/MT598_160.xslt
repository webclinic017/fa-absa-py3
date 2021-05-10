<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT598_160_CPRTDET_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INTR)//(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_CPRTDET_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_CPRTDET_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_160_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_GENL_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((NEWM))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_GENL_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_GENL_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_GENL_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INST)/STRA/(RATU))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_GENL_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_GENL_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_GENL_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_GENL_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_GENL_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_160_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_CPRTDET_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RESD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_CPRTDET_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_CPRTDET_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_CPRTDET_14F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ZAR)-(CPI|PRIME|SREPO|SABOR)(-[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_160_CPRTDET_14F_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_160_CPRTDET_14F_Type_Pattern">
    <xs:attribute fixed="14F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_160_16R_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT598_160_CPRTDET">
  <xs:sequence>
   <xs:element name="CouponRateNextResetDate" type="MT598_160_CPRTDET_98A_Type"/>
   <xs:element name="CouponRateSource" type="MT598_160_CPRTDET_14F_Type"/>
   <xs:element name="CurrentSourceRate" type="MT598_160_CPRTDET_92A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_160_GENL">
  <xs:sequence>
   <xs:element name="FunctionOfMessage" type="MT598_160_GENL_23G_Type"/>
   <xs:element name="PreparationDateAndTime" type="MT598_160_GENL_98C_Type"/>
   <xs:element name="TypeOfInstructionIndicator" type="MT598_160_GENL_22F_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:element name="MT598_160">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_160_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_160_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_160_77E_Type"/>
    <xs:element name="GENL" type="MT598_160_GENL"/>
    <xs:element maxOccurs="unbounded" name="CPRTDET" type="MT598_160_CPRTDET"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
