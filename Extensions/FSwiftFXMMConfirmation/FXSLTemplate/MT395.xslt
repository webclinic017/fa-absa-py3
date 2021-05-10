<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT395_79_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,50}\n?){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_79_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_79_Type_Pattern">
    <xs:attribute fixed="79" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT395_11R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{3}(\n)?[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(\n)?([0-9]{4}[0-9]{6})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_11R_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_11R_Type_Pattern">
    <xs:attribute fixed="11R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT395_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT395_75_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_75_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_75_Type_Pattern">
    <xs:attribute fixed="75" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT395_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT395_77A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,20})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_77A_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_77A_Type_Pattern">
    <xs:attribute fixed="77A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT395_11S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{3}(\n)?[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(\n)?([0-9]{4}[0-9]{6})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT395_11S_Type">
  <xs:simpleContent>
   <xs:extension base="MT395_11S_Type_Pattern">
    <xs:attribute fixed="11S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:element name="MT395">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReferenceNumber" type="MT395_20_Type"/>
    <xs:element name="RelatedReference" type="MT395_21_Type"/>
    <xs:element name="Queries" type="MT395_75_Type"/>
    <xs:element minOccurs="0" name="Narrative" type="MT395_77A_Type"/>
    <xs:choice minOccurs="0">
     <xs:element minOccurs="0" name="MTAndDateOfTheOriginalMessage_R" type="MT395_11R_Type"/>
     <xs:element minOccurs="0" name="MTAndDateOfTheOriginalMessage_S" type="MT395_11S_Type"/>
    </xs:choice>
    <xs:element id="narrative" minOccurs="0" name="NarrativeDescriptionOfTheOriginalMessage" type="MT395_79_Type"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

