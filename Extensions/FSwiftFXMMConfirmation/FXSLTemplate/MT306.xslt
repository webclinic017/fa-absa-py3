<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_21_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_21_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_21_Type_Pattern">
    <xs:attribute fixed="21" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_22A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMND|CANC|NEWT))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_22A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_22A_Type_Pattern">
    <xs:attribute fixed="22A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_94A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AGNT|BILA|BROK))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_94A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_94A_Type_Pattern">
    <xs:attribute fixed="94A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_22C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_22C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_22C_Type_Pattern">
    <xs:attribute fixed="22C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_21N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_21N_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_21N_Type_Pattern">
    <xs:attribute fixed="21N" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_21B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_21B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_21B_Type_Pattern">
    <xs:attribute fixed="21B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_12F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AVRF|AVRO|AVSF|AVSO|BINA|DAVF|DAVO|DIGI|NOTO|VANI))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_12F_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_12F_Type_Pattern">
    <xs:attribute fixed="12F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_12E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMER|ASIA|BERM|EURO))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_12E_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_12E_Type_Pattern">
    <xs:attribute fixed="12E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_12D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((CALL|PUTO))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_12D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_12D_Type_Pattern">
    <xs:attribute fixed="12D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_17A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_17A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_17A_Type_Pattern">
    <xs:attribute fixed="17A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_17F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_17F_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_17F_Type_Pattern">
    <xs:attribute fixed="17F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_22K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((CLST|CONF|KNIN|KNOT|OTHR|TRIG)(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_22K_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_22K_Type_Pattern">
    <xs:attribute fixed="22K" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_30U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_30U_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_30U_Type_Pattern">
    <xs:attribute fixed="30U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_29H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ARBA|ATVI|AUME|AUSY|BEBR|BRSP|CAMO|CATO|CHGE|CHZU|CLSA|CNBE|CZPR|DECB|DEFR|DKCO|EETA|ESMA|EUTA|FIHE|FRPA|GBLO|GRAT|HKHK|HUBU|IDJA|IEDU|ILTA|INMU|ITMI|ITRO|JPTO|KRSE|LBBE|LKCO|LULU|MXMC|MYKL|NLAM|NOOS|NYFD|NYSE|NZAU|NZWE|PAPC|PHMA|PLWA|PTLI|ROBU|RUMO|SARI|SEST|SGSI|SKBR|THBA|TRAN|TRIS|TWTA|USCH|USGS|USLA|USNY|VNHA|ZAJO))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_29H_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_29H_Type_Pattern">
    <xs:attribute fixed="29H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_82A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_82A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_82A_Type_Pattern">
    <xs:attribute fixed="82A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_82D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_82D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_82D_Type_Pattern">
    <xs:attribute fixed="82D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_82J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_82J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_82J_Type_Pattern">
    <xs:attribute fixed="82J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_87A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_87A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_87A_Type_Pattern">
    <xs:attribute fixed="87A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_87D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_87D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_87D_Type_Pattern">
    <xs:attribute fixed="87D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_87J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_87J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_87J_Type_Pattern">
    <xs:attribute fixed="87J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_83A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_83A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_83A_Type_Pattern">
    <xs:attribute fixed="83A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_83D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_83D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_83D_Type_Pattern">
    <xs:attribute fixed="83D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_83J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_83J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_83J_Type_Pattern">
    <xs:attribute fixed="83J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_77H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))?(//[0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_77H_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_77H_Type_Pattern">
    <xs:attribute fixed="77H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_77D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_77D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_77D_Type_Pattern">
    <xs:attribute fixed="77D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceA_GeneralInformation_14C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation_14C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceA_GeneralInformation_14C_Type_Pattern">
    <xs:attribute fixed="14C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_17V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((B|S))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_17V_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_17V_Type_Pattern">
    <xs:attribute fixed="17V" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_30T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_30T_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_30T_Type_Pattern">
    <xs:attribute fixed="30T" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_30X_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_30X_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_30X_Type_Pattern">
    <xs:attribute fixed="30X" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_29E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_29E_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_29E_Type_Pattern">
    <xs:attribute fixed="29E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_30J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{1}[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_30J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_30J_Type_Pattern">
    <xs:attribute fixed="30J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_39M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_39M_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_39M_Type_Pattern">
    <xs:attribute fixed="39M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SubsequenceB1_PremiumDetails_37K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD|PCT)[0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SubsequenceB1_PremiumDetails_37K_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SubsequenceB1_PremiumDetails_37K_Type_Pattern">
    <xs:attribute fixed="37K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_30V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_30V_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_30V_Type_Pattern">
    <xs:attribute fixed="30V" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_34B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_34B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_34B_Type_Pattern">
    <xs:attribute fixed="34B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84A_Type_Pattern">
    <xs:attribute fixed="84A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84B_Type_Pattern">
    <xs:attribute fixed="84B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84D_Type_Pattern">
    <xs:attribute fixed="84D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84J_Type_Pattern">
    <xs:attribute fixed="84J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceD_VanillaBlock_30P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock_30P_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceD_VanillaBlock_30P_Type_Pattern">
    <xs:attribute fixed="30P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceD_VanillaBlock_30Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock_30Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceD_VanillaBlock_30Q_Type_Pattern">
    <xs:attribute fixed="30Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceD_VanillaBlock_26F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((NETCASH|PRINCIPAL))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock_26F_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceD_VanillaBlock_26F_Type_Pattern">
    <xs:attribute fixed="26F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceD_VanillaBlock_32B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock_32B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceD_VanillaBlock_32B_Type_Pattern">
    <xs:attribute fixed="32B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceD_VanillaBlock_36_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock_36_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceD_VanillaBlock_36_Type_Pattern">
    <xs:attribute fixed="36" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceD_VanillaBlock_33B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock_33B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceD_VanillaBlock_33B_Type_Pattern">
    <xs:attribute fixed="33B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_33E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_33E_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_33E_Type_Pattern">
    <xs:attribute fixed="33E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_30H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_30H_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_30H_Type_Pattern">
    <xs:attribute fixed="30H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_58A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_58A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_58A_Type_Pattern">
    <xs:attribute fixed="58A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_58D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_58D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_58D_Type_Pattern">
    <xs:attribute fixed="58D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceE_PayoutAmount_58J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount_58J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceE_PayoutAmount_58J_Type_Pattern">
    <xs:attribute fixed="58J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_22G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((DKIN|DKOT|KIKO|KOKI|SKIN|SKOT))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_22G_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_22G_Type_Pattern">
    <xs:attribute fixed="22G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_37J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_37J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_37J_Type_Pattern">
    <xs:attribute fixed="37J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_37L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_37L_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_37L_Type_Pattern">
    <xs:attribute fixed="37L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_30G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_30G_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_30G_Type_Pattern">
    <xs:attribute fixed="30G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ARBA|ATVI|AUME|AUSY|BEBR|BRSP|CAMO|CATO|CHGE|CHZU|CLSA|CNBE|CZPR|DECB|DEFR|DKCO|EETA|ESMA|EUTA|FIHE|FRPA|GBLO|GRAT|HKHK|HUBU|IDJA|IEDU|ILTA|INMU|ITMI|ITRO|JPTO|KRSE|LBBE|LKCO|LULU|MXMC|MYKL|NLAM|NOOS|NYFD|NYSE|NZAU|NZWE|PAPC|PHMA|PLWA|PTLI|ROBU|RUMO|SARI|SEST|SGSI|SKBR|THBA|TRAN|TRIS|TWTA|USCH|USGS|USLA|USNY|VNHA|ZAJO)(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29J_Type_Pattern">
    <xs:attribute fixed="29J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ARBA|ATVI|AUME|AUSY|BEBR|BRSP|CAMO|CATO|CHGE|CHZU|CLSA|CNBE|CZPR|DECB|DEFR|DKCO|EETA|ESMA|EUTA|FIHE|FRPA|GBLO|GRAT|HKHK|HUBU|IDJA|IEDU|ILTA|INMU|ITMI|ITRO|JPTO|KRSE|LBBE|LKCO|LULU|MXMC|MYKL|NLAM|NOOS|NYFD|NYSE|NZAU|NZWE|PAPC|PHMA|PLWA|PTLI|ROBU|RUMO|SARI|SEST|SGSI|SKBR|THBA|TRAN|TRIS|TWTA|USCH|USGS|USLA|USNY|VNHA|ZAJO)(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29K_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29K_Type_Pattern">
    <xs:attribute fixed="29K" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceG_TriggerBlock_TRIGGER_22J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((DBTR|SITR))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock_TRIGGER_22J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceG_TriggerBlock_TRIGGER_22J_Type_Pattern">
    <xs:attribute fixed="22J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceG_TriggerBlock_TRIGGER_37U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock_TRIGGER_37U_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceG_TriggerBlock_TRIGGER_37U_Type_Pattern">
    <xs:attribute fixed="37U" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceG_TriggerBlock_TRIGGER_37P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,12})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock_TRIGGER_37P_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceG_TriggerBlock_TRIGGER_37P_Type_Pattern">
    <xs:attribute fixed="37P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceG_TriggerBlock_TRIGGER_32Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock_TRIGGER_32Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceG_TriggerBlock_TRIGGER_32Q_Type_Pattern">
    <xs:attribute fixed="32Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceG_TriggerBlock_TRIGGER_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock_TRIGGER_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceG_TriggerBlock_TRIGGER_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceH_NonDeliverableOptionBlockOPT_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceH_NonDeliverableOptionBlockOPT_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceH_NonDeliverableOptionBlockOPT_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceH_NonDeliverableOptionBlockOPT_32E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceH_NonDeliverableOptionBlockOPT_32E_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceH_NonDeliverableOptionBlockOPT_32E_Type_Pattern">
    <xs:attribute fixed="32E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_12G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AMER|BERM|EURO))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_12G_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_12G_Type_Pattern">
    <xs:attribute fixed="12G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_30T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_30T_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_30T_Type_Pattern">
    <xs:attribute fixed="30T" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_22Y_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ANNU|BIAN|BIMO|FIVE|MONT|TENN|WEEK))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_22Y_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_22Y_Type_Pattern">
    <xs:attribute fixed="22Y" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_85A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_85A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_85A_Type_Pattern">
    <xs:attribute fixed="85A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_85D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_85D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_85D_Type_Pattern">
    <xs:attribute fixed="85D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_85J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_85J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_85J_Type_Pattern">
    <xs:attribute fixed="85J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_88A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_88A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_88A_Type_Pattern">
    <xs:attribute fixed="88A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_88D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_88D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_88D_Type_Pattern">
    <xs:attribute fixed="88D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_88J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_88J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_88J_Type_Pattern">
    <xs:attribute fixed="88J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_84A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_84A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_84A_Type_Pattern">
    <xs:attribute fixed="84A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_84B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_84B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_84B_Type_Pattern">
    <xs:attribute fixed="84B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_84D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_84D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_84D_Type_Pattern">
    <xs:attribute fixed="84D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_84J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_84J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_84J_Type_Pattern">
    <xs:attribute fixed="84J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_30Y_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_30Y_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_30Y_Type_Pattern">
    <xs:attribute fixed="30Y" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_29L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/[A-Z0-9]{4}/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_29L_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_29L_Type_Pattern">
    <xs:attribute fixed="29L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_29E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_29E_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_29E_Type_Pattern">
    <xs:attribute fixed="29E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_29M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_29M_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_29M_Type_Pattern">
    <xs:attribute fixed="29M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_17I_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_17I_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_17I_Type_Pattern">
    <xs:attribute fixed="17I" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_29N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/[A-Z0-9]{4}/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_29N_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_29N_Type_Pattern">
    <xs:attribute fixed="29N" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_30Z_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_30Z_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_30Z_Type_Pattern">
    <xs:attribute fixed="30Z" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceI_EarlyTermination_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceI_EarlyTermination_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_14S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_14S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_14S_Type_Pattern">
    <xs:attribute fixed="14S" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_14B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AD|PC))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_14B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_14B_Type_Pattern">
    <xs:attribute fixed="14B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_16C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_16C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_16C_Type_Pattern">
    <xs:attribute fixed="16C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SPOT_18B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SPOT_18B_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SPOT_18B_Type_Pattern">
    <xs:attribute fixed="18B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_30M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_30M_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_30M_Type_Pattern">
    <xs:attribute fixed="30M" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_19Y_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_19Y_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_19Y_Type_Pattern">
    <xs:attribute fixed="19Y" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_STRIKE_18C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_STRIKE_18C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_STRIKE_18C_Type_Pattern">
    <xs:attribute fixed="18C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_30N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_30N_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_30N_Type_Pattern">
    <xs:attribute fixed="30N" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_19Z_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_19Z_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_19Z_Type_Pattern">
    <xs:attribute fixed="19Z" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_19C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_19C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_19C_Type_Pattern">
    <xs:attribute fixed="19C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceJ_AveragingOptionsandForwards_23C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((FLIPPED|NORMAL))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_23C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceJ_AveragingOptionsandForwards_23C_Type_Pattern">
    <xs:attribute fixed="23C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_29A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_29A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_29A_Type_Pattern">
    <xs:attribute fixed="29A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_24D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((BROK|ELEC|FAXT|PHON|TELX)(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_24D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_24D_Type_Pattern">
    <xs:attribute fixed="24D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_88A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_88A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_88A_Type_Pattern">
    <xs:attribute fixed="88A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_88D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_88D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_88D_Type_Pattern">
    <xs:attribute fixed="88D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_71F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_71F_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_71F_Type_Pattern">
    <xs:attribute fixed="71F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_21G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_21G_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_21G_Type_Pattern">
    <xs:attribute fixed="21G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceK_AdditionalInformation_72_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation_72_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceK_AdditionalInformation_72_Type_Pattern">
    <xs:attribute fixed="72" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_18A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_18A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_18A_Type_Pattern">
    <xs:attribute fixed="18A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_AMOUNT_30F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_AMOUNT_30F_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_AMOUNT_30F_Type_Pattern">
    <xs:attribute fixed="30F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_AMOUNT_32H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_AMOUNT_32H_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_AMOUNT_32H_Type_Pattern">
    <xs:attribute fixed="32H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_53A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_53A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_53A_Type_Pattern">
    <xs:attribute fixed="53A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_53D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_53D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_53D_Type_Pattern">
    <xs:attribute fixed="53D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_53J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_53J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_53J_Type_Pattern">
    <xs:attribute fixed="53J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_86A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_86A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_86A_Type_Pattern">
    <xs:attribute fixed="86A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_86D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_86D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_86D_Type_Pattern">
    <xs:attribute fixed="86D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_86J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_86J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_86J_Type_Pattern">
    <xs:attribute fixed="86J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_56A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_56A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_56A_Type_Pattern">
    <xs:attribute fixed="56A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_56D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_56D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_56D_Type_Pattern">
    <xs:attribute fixed="56D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_56J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_56J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_56J_Type_Pattern">
    <xs:attribute fixed="56J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_57A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_57A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_57A_Type_Pattern">
    <xs:attribute fixed="57A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_57D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_57D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_57D_Type_Pattern">
    <xs:attribute fixed="57D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceL_AdditionalAmounts_57J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_57J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceL_AdditionalAmounts_57J_Type_Pattern">
    <xs:attribute fixed="57J" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_22L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_22L_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_22L_Type_Pattern">
    <xs:attribute fixed="22L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91A_Type_Pattern">
    <xs:attribute fixed="91A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91D_Type_Pattern">
    <xs:attribute fixed="91D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91J_Type_Pattern">
    <xs:attribute fixed="91J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22M_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22M_Type_Pattern">
    <xs:attribute fixed="22M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22N_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22N_Type_Pattern">
    <xs:attribute fixed="22N" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22P_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern">
    <xs:attribute fixed="22P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,32})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22R_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern">
    <xs:attribute fixed="22R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_96A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_96A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_96A_Type_Pattern">
    <xs:attribute fixed="96A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_96D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})?(\n)?(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_96D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_96D_Type_Pattern">
    <xs:attribute fixed="96D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_96J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,40}\n?){1,5})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_96J_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_96J_Type_Pattern">
    <xs:attribute fixed="96J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_22S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((C|P)/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_22S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_22S_Type_Pattern">
    <xs:attribute fixed="22S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_22T_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_22T_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_22T_Type_Pattern">
    <xs:attribute fixed="22T" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17E_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17E_Type_Pattern">
    <xs:attribute fixed="17E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_22U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((FXCOEX|FXNDOP|FXSEBA|FXSEDI))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_22U_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_22U_Type_Pattern">
    <xs:attribute fixed="22U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((A|P|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17H_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17H_Type_Pattern">
    <xs:attribute fixed="17H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((F|O|P|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17P_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17P_Type_Pattern">
    <xs:attribute fixed="17P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_22V_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_22V_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_22V_Type_Pattern">
    <xs:attribute fixed="22V" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_98D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_98D_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_98D_Type_Pattern">
    <xs:attribute fixed="98D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17W_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17W_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17W_Type_Pattern">
    <xs:attribute fixed="17W" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17Y_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((F|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17Y_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17Y_Type_Pattern">
    <xs:attribute fixed="17Y" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17Z_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17Z_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17Z_Type_Pattern">
    <xs:attribute fixed="17Z" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_22Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_22Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_22Q_Type_Pattern">
    <xs:attribute fixed="22Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17L_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17L_Type_Pattern">
    <xs:attribute fixed="17L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((A|C|F|I|L|O|R|U))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17M_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17M_Type_Pattern">
    <xs:attribute fixed="17M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17Q_Type_Pattern">
    <xs:attribute fixed="17Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17S_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17S_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17S_Type_Pattern">
    <xs:attribute fixed="17S" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_17X_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_17X_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_17X_Type_Pattern">
    <xs:attribute fixed="17X" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_34C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_34C_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_34C_Type_Pattern">
    <xs:attribute fixed="34C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT306_SequenceM_ReportingInformation_77A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,20})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_77A_Type">
  <xs:simpleContent>
   <xs:extension base="MT306_SequenceM_ReportingInformation_77A_Type_Pattern">
    <xs:attribute fixed="77A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersReference" type="MT306_SequenceA_GeneralInformation_20_Type"/>
   <xs:element minOccurs="0" name="RelatedReference" type="MT306_SequenceA_GeneralInformation_21_Type"/>
   <xs:element name="TypeOfOperation" type="MT306_SequenceA_GeneralInformation_22A_Type"/>
   <xs:element minOccurs="0" name="ScopeOfOperation" type="MT306_SequenceA_GeneralInformation_94A_Type"/>
   <xs:element name="CommonReference" type="MT306_SequenceA_GeneralInformation_22C_Type"/>
   <xs:element name="ContractNumberPartyA" type="MT306_SequenceA_GeneralInformation_21N_Type"/>
   <xs:element minOccurs="0" name="ContractNumberPartyB" type="MT306_SequenceA_GeneralInformation_21B_Type"/>
   <xs:element name="OptionStyle" type="MT306_SequenceA_GeneralInformation_12F_Type"/>
   <xs:element name="ExpirationStyle" type="MT306_SequenceA_GeneralInformation_12E_Type"/>
   <xs:element minOccurs="0" name="OptionType" type="MT306_SequenceA_GeneralInformation_12D_Type"/>
   <xs:element name="BarrierIndicator" type="MT306_SequenceA_GeneralInformation_17A_Type"/>
   <xs:element name="NonDeliverableIndicator" type="MT306_SequenceA_GeneralInformation_17F_Type"/>
   <xs:element name="TypeOfEvent" type="MT306_SequenceA_GeneralInformation_22K_Type"/>
   <xs:element minOccurs="0" name="DateOfTriggerHit" type="MT306_SequenceA_GeneralInformation_30U_Type"/>
   <xs:element minOccurs="0" name="LocationOfTriggerHit" type="MT306_SequenceA_GeneralInformation_29H_Type"/>
   <xs:choice>
    <xs:element name="PartyA_A" type="MT306_SequenceA_GeneralInformation_82A_Type"/>
    <xs:element name="PartyA_D" type="MT306_SequenceA_GeneralInformation_82D_Type"/>
    <xs:element name="PartyA_J" type="MT306_SequenceA_GeneralInformation_82J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="PartyB_A" type="MT306_SequenceA_GeneralInformation_87A_Type"/>
    <xs:element name="PartyB_D" type="MT306_SequenceA_GeneralInformation_87D_Type"/>
    <xs:element name="PartyB_J" type="MT306_SequenceA_GeneralInformation_87J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_A" type="MT306_SequenceA_GeneralInformation_83A_Type"/>
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_D" type="MT306_SequenceA_GeneralInformation_83D_Type"/>
    <xs:element minOccurs="0" name="FundOrBeneficiaryCustomer_J" type="MT306_SequenceA_GeneralInformation_83J_Type"/>
   </xs:choice>
   <xs:element name="TypeDateVersionOfTheAgreement" type="MT306_SequenceA_GeneralInformation_77H_Type"/>
   <xs:element minOccurs="0" name="AdditionalConditions" type="MT306_SequenceA_GeneralInformation_77D_Type"/>
   <xs:element minOccurs="0" name="YearOfDefinitions" type="MT306_SequenceA_GeneralInformation_14C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15A" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails">
  <xs:sequence>
   <xs:element name="BuySellIndicator" type="MT306_SequenceB_TransactionDetails_17V_Type"/>
   <xs:element name="TradeDate" type="MT306_SequenceB_TransactionDetails_30T_Type"/>
   <xs:element name="ExpirationDate" type="MT306_SequenceB_TransactionDetails_30X_Type"/>
   <xs:element name="ExpirationLocationAndTime" type="MT306_SequenceB_TransactionDetails_29E_Type"/>
   <xs:choice>
    <xs:element name="FinalSettlementDate_F" type="MT306_SequenceB_TransactionDetails_30F_Type"/>
    <xs:element name="FinalSettlementDate_J" type="MT306_SequenceB_TransactionDetails_30J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SettlementRateSource" type="MT306_SequenceB_TransactionDetails_14S_Type"/>
   <xs:element minOccurs="0" name="PaymentClearingCentre" type="MT306_SequenceB_TransactionDetails_39M_Type"/>
   <xs:element minOccurs="0" name="SubsequenceB1_PremiumDetails" type="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails"/>
   <xs:element name="SubsequenceB2_CalculationAgent" type="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent"/>
  </xs:sequence>
  <xs:attribute fixed="15B" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails">
  <xs:sequence>
   <xs:element minOccurs="0" name="PremiumPrice" type="MT306_SubsequenceB1_PremiumDetails_37K_Type"/>
   <xs:element name="PremiumPaymentDate" type="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_30V_Type"/>
   <xs:element name="PremiumCurrencyAndAmount" type="MT306_SequenceB_TransactionDetails_SubsequenceB1_PremiumDetails_34B_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent">
  <xs:sequence>
   <xs:choice>
    <xs:element name="CalculationAgent_A" type="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84A_Type"/>
    <xs:element name="CalculationAgent_B" type="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84B_Type"/>
    <xs:element name="CalculationAgent_D" type="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84D_Type"/>
    <xs:element name="CalculationAgent_J" type="MT306_SequenceB_TransactionDetails_SubsequenceB2_CalculationAgent_84J_Type"/>
   </xs:choice>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceC_SettlementInstructionsforPaymentofPremium">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15C" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceD_VanillaBlock">
  <xs:sequence>
   <xs:element minOccurs="0" name="EarliestExerciseDate" type="MT306_SequenceD_VanillaBlock_30P_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="IntermediateExerciseDate" type="MT306_SequenceD_VanillaBlock_30Q_Type"/>
   <xs:element name="SettlementType" type="MT306_SequenceD_VanillaBlock_26F_Type"/>
   <xs:element name="PutCurrencyAndAmount" type="MT306_SequenceD_VanillaBlock_32B_Type"/>
   <xs:element name="StrikePrice" type="MT306_SequenceD_VanillaBlock_36_Type"/>
   <xs:element name="CallCurrencyAndAmount" type="MT306_SequenceD_VanillaBlock_33B_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15D" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceE_PayoutAmount">
  <xs:sequence>
   <xs:element name="CurrencyAmount" type="MT306_SequenceE_PayoutAmount_33E_Type"/>
   <xs:element minOccurs="0" name="TouchPaymentDate" type="MT306_SequenceE_PayoutAmount_30H_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT306_SequenceE_PayoutAmount_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT306_SequenceE_PayoutAmount_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT306_SequenceE_PayoutAmount_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT306_SequenceE_PayoutAmount_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT306_SequenceE_PayoutAmount_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT306_SequenceE_PayoutAmount_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT306_SequenceE_PayoutAmount_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT306_SequenceE_PayoutAmount_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT306_SequenceE_PayoutAmount_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT306_SequenceE_PayoutAmount_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT306_SequenceE_PayoutAmount_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT306_SequenceE_PayoutAmount_57J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BeneficiaryInstitution_A" type="MT306_SequenceE_PayoutAmount_58A_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_D" type="MT306_SequenceE_PayoutAmount_58D_Type"/>
    <xs:element minOccurs="0" name="BeneficiaryInstitution_J" type="MT306_SequenceE_PayoutAmount_58J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15E" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock">
  <xs:sequence>
   <xs:element name="TypeOfBarrier" type="MT306_SequenceF_BarrierBlock_22G_Type"/>
   <xs:element name="BarrierLevel" type="MT306_SequenceF_BarrierBlock_37J_Type"/>
   <xs:element minOccurs="0" name="LowerBarrierLevel" type="MT306_SequenceF_BarrierBlock_37L_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceF1_BarrierWindowBlock" type="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock"/>
  </xs:sequence>
  <xs:attribute fixed="15F" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock">
  <xs:sequence>
   <xs:element name="BarrierWindowStartDateAndEndDate" type="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_30G_Type"/>
   <xs:element name="LocationAndTimeForStartDate" type="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29J_Type"/>
   <xs:element name="LocationAndTimeForEndDate" type="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_29K_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SettlementRateSource" type="MT306_SequenceF_BarrierBlock_SubsequenceF1_BarrierWindowBlock_14S_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock">
  <xs:sequence>
   <xs:element name="TRIGGER" type="MT306_SequenceG_TriggerBlock_TRIGGER"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceG_TriggerBlock_TRIGGER">
  <xs:sequence>
   <xs:element name="TypeOfTrigger" type="MT306_SequenceG_TriggerBlock_TRIGGER_22J_Type"/>
   <xs:element name="TriggerLevel" type="MT306_SequenceG_TriggerBlock_TRIGGER_37U_Type"/>
   <xs:element minOccurs="0" name="LowerTriggerLevel" type="MT306_SequenceG_TriggerBlock_TRIGGER_37P_Type"/>
   <xs:element name="CurrencyPair" type="MT306_SequenceG_TriggerBlock_TRIGGER_32Q_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SettlementRateSource" type="MT306_SequenceG_TriggerBlock_TRIGGER_14S_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15G" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceH_NonDeliverableOptionBlockOPT">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="SettlementRateSource" type="MT306_SequenceH_NonDeliverableOptionBlockOPT_14S_Type"/>
   <xs:element name="SettlementCurrency" type="MT306_SequenceH_NonDeliverableOptionBlockOPT_32E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15H" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceI_EarlyTermination">
  <xs:sequence>
   <xs:element name="EarlyTerminationStyle" type="MT306_SequenceI_EarlyTermination_12G_Type"/>
   <xs:element minOccurs="0" name="EarlyTerminationDate" type="MT306_SequenceI_EarlyTermination_30T_Type"/>
   <xs:element minOccurs="0" name="FrequencyOfEarlyTermination" type="MT306_SequenceI_EarlyTermination_22Y_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ExercisingParty_A" type="MT306_SequenceI_EarlyTermination_85A_Type"/>
    <xs:element minOccurs="0" name="ExercisingParty_D" type="MT306_SequenceI_EarlyTermination_85D_Type"/>
    <xs:element minOccurs="0" name="ExercisingParty_J" type="MT306_SequenceI_EarlyTermination_85J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="NonExercisingParty_A" type="MT306_SequenceI_EarlyTermination_88A_Type"/>
    <xs:element minOccurs="0" name="NonExercisingParty_D" type="MT306_SequenceI_EarlyTermination_88D_Type"/>
    <xs:element minOccurs="0" name="NonExercisingParty_J" type="MT306_SequenceI_EarlyTermination_88J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="CalculationAgent_A" type="MT306_SequenceI_EarlyTermination_84A_Type"/>
    <xs:element name="CalculationAgent_B" type="MT306_SequenceI_EarlyTermination_84B_Type"/>
    <xs:element name="CalculationAgent_D" type="MT306_SequenceI_EarlyTermination_84D_Type"/>
    <xs:element name="CalculationAgent_J" type="MT306_SequenceI_EarlyTermination_84J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="CommencementDate" type="MT306_SequenceI_EarlyTermination_30Y_Type"/>
   <xs:element minOccurs="0" name="ExpiryDetails" type="MT306_SequenceI_EarlyTermination_29L_Type"/>
   <xs:element minOccurs="0" name="EarliestExerciseTime" type="MT306_SequenceI_EarlyTermination_29E_Type"/>
   <xs:element minOccurs="0" name="LatestExerciseTime" type="MT306_SequenceI_EarlyTermination_29M_Type"/>
   <xs:element minOccurs="0" name="CashSettlement" type="MT306_SequenceI_EarlyTermination_17I_Type"/>
   <xs:element minOccurs="0" name="CashSettlementValuationDetails" type="MT306_SequenceI_EarlyTermination_29N_Type"/>
   <xs:element minOccurs="0" name="CashSettlementPaymentDate" type="MT306_SequenceI_EarlyTermination_30Z_Type"/>
   <xs:element minOccurs="0" name="SettlementRateSource" type="MT306_SequenceI_EarlyTermination_14S_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15I" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards">
  <xs:sequence>
   <xs:element name="SettlementRateSource" type="MT306_SequenceJ_AveragingOptionsandForwards_14S_Type"/>
   <xs:element minOccurs="0" name="AverageStrikePriceCalculation" type="MT306_SequenceJ_AveragingOptionsandForwards_14B_Type"/>
   <xs:element name="DecimalPlaces" type="MT306_SequenceJ_AveragingOptionsandForwards_16C_Type"/>
   <xs:element minOccurs="0" name="SPOT" type="MT306_SequenceJ_AveragingOptionsandForwards_SPOT"/>
   <xs:element minOccurs="0" name="STRIKE" type="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE"/>
   <xs:element minOccurs="0" name="Adjustment" type="MT306_SequenceJ_AveragingOptionsandForwards_19C_Type"/>
   <xs:element minOccurs="0" name="CalculationOfSettlementAmount" type="MT306_SequenceJ_AveragingOptionsandForwards_23C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15J" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_SPOT">
  <xs:sequence>
   <xs:element minOccurs="0" name="NumberOfSpotAveragingDates" type="MT306_SPOT_18B_Type"/>
   <xs:element maxOccurs="unbounded" name="SubsequenceJ1_SpotAverageDatesandWeightings" type="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings">
  <xs:sequence>
   <xs:element name="SpotAveragingDate" type="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_30M_Type"/>
   <xs:element name="SpotAveragingWeightingFactor" type="MT306_SequenceJ_AveragingOptionsandForwards_SPOT_SubsequenceJ1_SpotAverageDatesandWeightings_19Y_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE">
  <xs:sequence>
   <xs:element minOccurs="0" name="NumberOfStrikeAveragingDates" type="MT306_STRIKE_18C_Type"/>
   <xs:element maxOccurs="unbounded" name="SubsequenceJ2_StrikeAverageDatesandWeightings" type="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings">
  <xs:sequence>
   <xs:element name="StrikeAveragingDate" type="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_30N_Type"/>
   <xs:element name="StrikeAveragingWeightingFactor" type="MT306_SequenceJ_AveragingOptionsandForwards_STRIKE_SubsequenceJ2_StrikeAverageDatesandWeightings_19Z_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceK_AdditionalInformation">
  <xs:sequence>
   <xs:element minOccurs="0" name="ContactInformation" type="MT306_SequenceK_AdditionalInformation_29A_Type"/>
   <xs:element minOccurs="0" name="DealingMethod" type="MT306_SequenceK_AdditionalInformation_24D_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="BrokerIdentification_A" type="MT306_SequenceK_AdditionalInformation_88A_Type"/>
    <xs:element minOccurs="0" name="BrokerIdentification_D" type="MT306_SequenceK_AdditionalInformation_88D_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="BrokersCommission" type="MT306_SequenceK_AdditionalInformation_71F_Type"/>
   <xs:element minOccurs="0" name="BrokersReference" type="MT306_SequenceK_AdditionalInformation_21G_Type"/>
   <xs:element minOccurs="0" name="SenderToReceiverInformation" type="MT306_SequenceK_AdditionalInformation_72_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15K" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts">
  <xs:sequence>
   <xs:element name="NumberOfRepetitions" type="MT306_SequenceL_AdditionalAmounts_18A_Type"/>
   <xs:element maxOccurs="unbounded" name="AMOUNT" type="MT306_SequenceL_AdditionalAmounts_AMOUNT"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="DeliveryAgent_A" type="MT306_SequenceL_AdditionalAmounts_53A_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_D" type="MT306_SequenceL_AdditionalAmounts_53D_Type"/>
    <xs:element minOccurs="0" name="DeliveryAgent_J" type="MT306_SequenceL_AdditionalAmounts_53J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary2_A" type="MT306_SequenceL_AdditionalAmounts_86A_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_D" type="MT306_SequenceL_AdditionalAmounts_86D_Type"/>
    <xs:element minOccurs="0" name="Intermediary2_J" type="MT306_SequenceL_AdditionalAmounts_86J_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Intermediary_A" type="MT306_SequenceL_AdditionalAmounts_56A_Type"/>
    <xs:element minOccurs="0" name="Intermediary_D" type="MT306_SequenceL_AdditionalAmounts_56D_Type"/>
    <xs:element minOccurs="0" name="Intermediary_J" type="MT306_SequenceL_AdditionalAmounts_56J_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="ReceivingAgent_A" type="MT306_SequenceL_AdditionalAmounts_57A_Type"/>
    <xs:element name="ReceivingAgent_D" type="MT306_SequenceL_AdditionalAmounts_57D_Type"/>
    <xs:element name="ReceivingAgent_J" type="MT306_SequenceL_AdditionalAmounts_57J_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="15L" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceL_AdditionalAmounts_AMOUNT">
  <xs:sequence>
   <xs:element name="PaymentDate" type="MT306_SequenceL_AdditionalAmounts_AMOUNT_30F_Type"/>
   <xs:element name="CurrencyPaymentAmount" type="MT306_SequenceL_AdditionalAmounts_AMOUNT_32H_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceM1_ReportingParties" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ClearingExceptionParty_A" type="MT306_SequenceM_ReportingInformation_96A_Type"/>
    <xs:element minOccurs="0" name="ClearingExceptionParty_D" type="MT306_SequenceM_ReportingInformation_96D_Type"/>
    <xs:element minOccurs="0" name="ClearingExceptionParty_J" type="MT306_SequenceM_ReportingInformation_96J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="ClearingBrokerIdentification" type="MT306_SequenceM_ReportingInformation_22S_Type"/>
   <xs:element minOccurs="0" name="ClearedProductIdentification" type="MT306_SequenceM_ReportingInformation_22T_Type"/>
   <xs:element minOccurs="0" name="ClearingThresholdIndicator" type="MT306_SequenceM_ReportingInformation_17E_Type"/>
   <xs:element minOccurs="0" name="UnderlyingProductIdentifier" type="MT306_SequenceM_ReportingInformation_22U_Type"/>
   <xs:element minOccurs="0" name="AllocationIndicator" type="MT306_SequenceM_ReportingInformation_17H_Type"/>
   <xs:element minOccurs="0" name="CollateralisationIndicator" type="MT306_SequenceM_ReportingInformation_17P_Type"/>
   <xs:element minOccurs="0" name="ExecutionVenue" type="MT306_SequenceM_ReportingInformation_22V_Type"/>
   <xs:element minOccurs="0" name="ExecutionTimestamp" type="MT306_SequenceM_ReportingInformation_98D_Type"/>
   <xs:element minOccurs="0" name="NonStandardFlag" type="MT306_SequenceM_ReportingInformation_17W_Type"/>
   <xs:element minOccurs="0" name="FinancialNatureOfTheCounterpartyIndicator" type="MT306_SequenceM_ReportingInformation_17Y_Type"/>
   <xs:element minOccurs="0" name="CollateralPortfolioIndicator" type="MT306_SequenceM_ReportingInformation_17Z_Type"/>
   <xs:element minOccurs="0" name="CollateralPortfolioCode" type="MT306_SequenceM_ReportingInformation_22Q_Type"/>
   <xs:element minOccurs="0" name="PortfolioCompressionIndicator" type="MT306_SequenceM_ReportingInformation_17L_Type"/>
   <xs:element minOccurs="0" name="CorporateSectorIndicator" type="MT306_SequenceM_ReportingInformation_17M_Type"/>
   <xs:element minOccurs="0" name="TradewithNonEEACounterpartyIndicator" type="MT306_SequenceM_ReportingInformation_17Q_Type"/>
   <xs:element minOccurs="0" name="IntragroupTradeIndicator" type="MT306_SequenceM_ReportingInformation_17S_Type"/>
   <xs:element minOccurs="0" name="CommercialorTreasuryFinancingIndicator" type="MT306_SequenceM_ReportingInformation_17X_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CommissionAndFees" type="MT306_SequenceM_ReportingInformation_34C_Type"/>
   <xs:element minOccurs="0" name="AdditionalReportingInformation" type="MT306_SequenceM_ReportingInformation_77A_Type"/>
  </xs:sequence>
  <xs:attribute fixed="15M" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="False" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="ReportingJurisdiction" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_22L_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ReportingParty_A" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91A_Type"/>
    <xs:element minOccurs="0" name="ReportingParty_D" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91D_Type"/>
    <xs:element minOccurs="0" name="ReportingParty_J" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_91J_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceM1a_UniqueTransactionIdentifier" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="UTINamespaceIssuerCode" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22M_Type"/>
   <xs:element name="TransactionIdentifier" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_22N_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubsequenceM1a1_PriorUniqueTransactionIdentifier" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier"/>
  </xs:sequence>
 </xs:complexType>
 <xs:complexType name="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier">
  <xs:sequence>
   <xs:element name="PUTINamespaceIssuerCode" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22P_Type"/>
   <xs:element name="PriorTransactionIdentifier" type="MT306_SequenceM_ReportingInformation_SubsequenceM1_ReportingParties_SubsequenceM1a_UniqueTransactionIdentifier_SubsequenceM1a1_PriorUniqueTransactionIdentifier_22R_Type"/>
  </xs:sequence>
 </xs:complexType>
 <xs:element name="MT306">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT306_SequenceA_GeneralInformation"/>
    <xs:element name="SequenceB_TransactionDetails" type="MT306_SequenceB_TransactionDetails"/>
    <xs:element minOccurs="0" name="SequenceC_SettlementInstructionsforPaymentofPremium" type="MT306_SequenceC_SettlementInstructionsforPaymentofPremium"/>
    <xs:element minOccurs="0" name="SequenceD_VanillaBlock" type="MT306_SequenceD_VanillaBlock"/>
    <xs:element minOccurs="0" name="SequenceE_PayoutAmount" type="MT306_SequenceE_PayoutAmount"/>
    <xs:element minOccurs="0" name="SequenceF_BarrierBlock" type="MT306_SequenceF_BarrierBlock"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="SequenceG_TriggerBlock" type="MT306_SequenceG_TriggerBlock"/>
    <xs:element minOccurs="0" name="SequenceH_NonDeliverableOptionBlockOPT" type="MT306_SequenceH_NonDeliverableOptionBlockOPT"/>
    <xs:element minOccurs="0" name="SequenceI_EarlyTermination" type="MT306_SequenceI_EarlyTermination"/>
    <xs:element minOccurs="0" name="SequenceJ_AveragingOptionsandForwards" type="MT306_SequenceJ_AveragingOptionsandForwards"/>
    <xs:element minOccurs="0" name="SequenceK_AdditionalInformation" type="MT306_SequenceK_AdditionalInformation"/>
    <xs:element minOccurs="0" name="SequenceL_AdditionalAmounts" type="MT306_SequenceL_AdditionalAmounts"/>
    <xs:element minOccurs="0" name="SequenceM_ReportingInformation" type="MT306_SequenceM_ReportingInformation"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

