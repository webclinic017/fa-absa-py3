<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_28E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,5}/(ONLY|LAST|MORE))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_28E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_28E_Type_Pattern">
    <xs:attribute fixed="28E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_13a_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="13a" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_13J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_13J_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_13J_Type_Pattern">
    <xs:attribute fixed="13J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}(/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceA_GeneralInformation_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{1})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceA_GeneralInformation_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})|(:[A-Z0-9]{4}//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)|(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{1})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//([A-Z]{2})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern">
    <xs:attribute fixed="94D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern">
    <xs:attribute fixed="12B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern">
    <xs:attribute fixed="12C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{3}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern">
    <xs:attribute fixed="13K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{1})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern">
    <xs:attribute fixed="93B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern">
    <xs:attribute fixed="93B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern">
    <xs:attribute fixed="93C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)|(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern">
    <xs:attribute fixed="99A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{3}/[A-Z]{3}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern">
    <xs:attribute fixed="70C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern">
    <xs:attribute fixed="93B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern">
    <xs:attribute fixed="99A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{3}/[A-Z]{3}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern">
    <xs:attribute fixed="93B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceC_AdditionalInformation_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceC_AdditionalInformation_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceC_AdditionalInformation_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceC_AdditionalInformation_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceC_AdditionalInformation_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceC_AdditionalInformation_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceC_AdditionalInformation_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT535_SequenceC_AdditionalInformation_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT535_SequenceC_AdditionalInformation_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT535_SequenceC_AdditionalInformation_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="PageNumber" type="MT535_SequenceA_GeneralInformation_28E_Type"/>
   <xs:element minOccurs="0" name="StatementNumber" type="MT535_SequenceA_GeneralInformation_13a_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="StatementNumber_A" type="MT535_SequenceA_GeneralInformation_13A_Type"/>
    <xs:element minOccurs="0" name="StatementNumber_J" type="MT535_SequenceA_GeneralInformation_13J_Type"/>
   </xs:choice>
   <xs:element name="SendersMessageReference" type="MT535_SequenceA_GeneralInformation_20C_Type"/>
   <xs:element name="FunctionOfMessage" type="MT535_SequenceA_GeneralInformation_23G_Type"/>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT535_SequenceA_GeneralInformation_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT535_SequenceA_GeneralInformation_98C_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_E" type="MT535_SequenceA_GeneralInformation_98E_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" name="Indicator" type="MT535_SequenceA_GeneralInformation_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceA1_Linkages" type="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT535_SequenceA_GeneralInformation_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT535_SequenceA_GeneralInformation_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT535_SequenceA_GeneralInformation_95R_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="SafekeepingAccount_A" type="MT535_SequenceA_GeneralInformation_97A_Type"/>
    <xs:element name="SafekeepingAccount_B" type="MT535_SequenceA_GeneralInformation_97B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" name="Flag" type="MT535_SequenceA_GeneralInformation_17B_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="GENL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LinkedMessage_A" type="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type"/>
    <xs:element minOccurs="0" name="LinkedMessage_B" type="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type"/>
   </xs:choice>
   <xs:element name="Reference" type="MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="LINK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT535_SequenceB_SubSafekeepingAccount_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT535_SequenceB_SubSafekeepingAccount_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT535_SequenceB_SubSafekeepingAccount_95R_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="SafekeepingAccount_A" type="MT535_SequenceB_SubSafekeepingAccount_97A_Type"/>
    <xs:element minOccurs="0" name="SafekeepingAccount_B" type="MT535_SequenceB_SubSafekeepingAccount_97B_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_B" type="MT535_SequenceB_SubSafekeepingAccount_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_C" type="MT535_SequenceB_SubSafekeepingAccount_94C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_F" type="MT535_SequenceB_SubSafekeepingAccount_94F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_L" type="MT535_SequenceB_SubSafekeepingAccount_94F_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ActivityFlag" type="MT535_SequenceB_SubSafekeepingAccount_17B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1_FinancialInstrument" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SUBSAFE" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument">
  <xs:sequence>
   <xs:element name="IdentificationOfFinancialInstrument" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type"/>
   <xs:element minOccurs="0" name="SubsequenceB1a_FinancialInstrumentAttributes" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes"/>
   <xs:element minOccurs="0" name="CorporateActionOptionCodeIndicator" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Price_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type"/>
    <xs:element minOccurs="0" name="Price_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type"/>
    <xs:element minOccurs="0" name="Price_E" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="SourceOfPrice" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PriceQuotationDateTime_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type"/>
    <xs:element minOccurs="0" name="PriceQuotationDateTime_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" name="Balance" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1b_Subbalance" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance"/>
   <xs:element minOccurs="0" name="NumberofDaysAccrued" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type"/>
   <xs:element minOccurs="0" name="ExchangeRate" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type"/>
   <xs:element minOccurs="0" name="HoldingsNarrative" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1c_QuantityBreakdown" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIN" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_D" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="CurrencyOfDenomination" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="NumberIdentification_K" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="IdentificationOfFinancialInstrument" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type"/>
   <xs:element minOccurs="0" name="FinancialInstrumentAttributeNarrative" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Balance_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type"/>
    <xs:element maxOccurs="unbounded" name="Balance_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ExposureTypeIndicator_F" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type"/>
    <xs:element minOccurs="0" name="ExposureTypeIndicator_H" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_F" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_L" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Price_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type"/>
    <xs:element minOccurs="0" name="Price_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type"/>
    <xs:element minOccurs="0" name="Price_E" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PriceQuotationDateTime_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type"/>
    <xs:element minOccurs="0" name="PriceQuotationDateTime_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="NumberOfDaysAccrued" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type"/>
   <xs:element minOccurs="0" name="ExchangeRate" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type"/>
   <xs:element minOccurs="0" name="SubbalanceDetailsNarrative" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceB1b1_QuantityBreakdown" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SUBBAL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown">
  <xs:sequence>
   <xs:element minOccurs="0" name="LotNumber" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type"/>
   <xs:element minOccurs="0" name="LotBalance" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LotDateTime_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type"/>
    <xs:element minOccurs="0" name="LotDateTime_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type"/>
    <xs:element minOccurs="0" name="LotDateTime_E" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BookLotPrice_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type"/>
    <xs:element minOccurs="0" name="BookLotPrice_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="TypeofPriceIndicator" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="BREAK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown">
  <xs:sequence>
   <xs:element minOccurs="0" name="LotNumber" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type"/>
   <xs:element minOccurs="0" name="LotBalance" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LotDateTime_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type"/>
    <xs:element minOccurs="0" name="LotDateTime_C" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type"/>
    <xs:element minOccurs="0" name="LotDateTime_E" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BookLotPrice_A" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type"/>
    <xs:element minOccurs="0" name="BookLotPrice_B" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="TypeofPriceIndicator" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="BREAK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT535_SequenceC_AdditionalInformation">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT535_SequenceC_AdditionalInformation_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_Q" type="MT535_SequenceC_AdditionalInformation_95Q_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT535_SequenceC_AdditionalInformation_95R_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT535_SequenceC_AdditionalInformation_19A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="ADDINFO" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT535">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT535_SequenceA_GeneralInformation"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="SequenceB_SubSafekeepingAccount" type="MT535_SequenceB_SubSafekeepingAccount"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="SequenceC_AdditionalInformation" type="MT535_SequenceC_AdditionalInformation"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

