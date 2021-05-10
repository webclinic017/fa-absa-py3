<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT598_131_SEQUENCE_30P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_30P_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_30P_Type_Pattern">
    <xs:attribute fixed="30P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_131_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_18A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_18A_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_18A_Type_Pattern">
    <xs:attribute fixed="18A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_82B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{1,2}[0-9]{1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_82B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_82B_Type_Pattern">
    <xs:attribute fixed="82B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_35A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{1,3}[0-9]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_35A_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_35A_Type_Pattern">
    <xs:attribute fixed="35A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_26H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([A-Z]{1,2}[0-9]{1,6})?/[0-9]{1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_26H_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_26H_Type_Pattern">
    <xs:attribute fixed="26H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_87C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(/[A-Z]{1,2}[0-9]{1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_87C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_87C_Type_Pattern">
    <xs:attribute fixed="87C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_23_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((DVP|DFP|RVP|RFP|PMO|RMO)(/[A-Z]{1,2}([0-9]{1,1})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_23_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_23_Type_Pattern">
    <xs:attribute fixed="23" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{1,3}[0-9]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_131_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_SEQUENCE_79_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/(LOANTAX)/(Y|N))?(\n)?/(GRPREF)/[A-Z]{1,2}[0-9]{1,6}/[0-9]{1,7}(\n)?/(SLBIND)/(LOAN|RETN|DEPO|WITH)(\n)?(/(LOANREF)/[A-Z]{1,2}[0-9]{1,6}/[0-9]{1,10})?(\n)?(/(POOLREF)/[A-Z]{1,2}[0-9]{1,6}/[A-Z0-9]{1,1}/[0-9]{1,10})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE_79_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_131_SEQUENCE_79_Type_Pattern">
    <xs:attribute fixed="79" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_131_16R_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT598_131_SEQUENCE">
  <xs:sequence>
   <xs:element name="FurtherIdentification" type="MT598_131_SEQUENCE_23_Type"/>
   <xs:element name="SettlementDate" type="MT598_131_SEQUENCE_30F_Type"/>
   <xs:element name="TradeDate" type="MT598_131_SEQUENCE_30P_Type"/>
   <xs:element name="QuantityOfSecurities" type="MT598_131_SEQUENCE_35A_Type"/>
   <xs:element name="IdentificationOfSecurities" type="MT598_131_SEQUENCE_35B_Type"/>
   <xs:element minOccurs="0" name="SettlementAmount" type="MT598_131_SEQUENCE_32B_Type"/>
   <xs:element name="Narrative" type="MT598_131_SEQUENCE_79_Type"/>
   <xs:element name="SAFIRESLoanReference" type="MT598_131_SEQUENCE_26H_Type"/>
   <xs:element name="TradingParty" type="MT598_131_SEQUENCE_82B_Type"/>
   <xs:element name="CounterParty" type="MT598_131_SEQUENCE_87C_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:element name="MT598_131">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_131_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_131_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_131_77E_Type"/>
    <xs:element maxOccurs="unbounded" name="SEQUENCE" type="MT598_131_SEQUENCE"/>
    <xs:element name="NumberOfRepetitiveParts" type="MT598_131_18A_Type"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
