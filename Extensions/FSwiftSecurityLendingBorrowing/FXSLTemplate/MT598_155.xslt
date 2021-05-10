<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT598_155_MMID_FIA_98A-ISSU_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISSU)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_98A-ISSU_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_98A-ISSU_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_95R-CSDP_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CSDP)/STRA/[A-Z]{2}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_95R-CSDP_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_95R-CSDP_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((.{1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_36B-MINO_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MINO)//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_36B-MINO_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_36B-MINO_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_17B-ACPC_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACPC)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_17B-ACPC_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_17B-ACPC_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_95R-ISSR_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISSR)/STRA/[A-Z]{2}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_95R-ISSR_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_95R-ISSR_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_92D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FLCP)//[0-9]{1,12},([0-9]{1,2})*/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_92D_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_92D_Type_Pattern">
    <xs:attribute fixed="92D" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_22F-CPDI_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CPDI)/STRA/(CLDT|ISDT))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_22F-CPDI_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_22F-CPDI_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_17B-WITI_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(WITI)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_17B-WITI_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_17B-WITI_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_13B-CPYD_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CPYD)/STRA/[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_13B-CPYD_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_13B-CPYD_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/STRA/IORT/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_22F-RTYP_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RTYP)/STRA/(FIXD|VLIN|VLDY|VNDY))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_22F-RTYP_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_22F-RTYP_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_GENL_22F-INST_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INST)/STRA/(ISSU|DISS|TOPU|REDU))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_GENL_22F-INST_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_GENL_22F-INST_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_17B-ACPO_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACPO)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_17B-ACPO_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_17B-ACPO_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_22F-PFRE_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PFRE)/STRA/(DAYC|ANNU|MNTH|QUTR|SEMI|TERM|ISDF))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_22F-PFRE_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_22F-PFRE_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_GENL_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((NEWM))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_GENL_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_GENL_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_17B-FCPM_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FCPM)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_17B-FCPM_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_17B-FCPM_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(QISS)//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_13B-CPCM_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CPCM)/STRA/(1|2|3))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_13B-CPCM_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_13B-CPCM_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_14F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ZAR)-(JIBAR1|JIBAR3|JIBAR6|JIBAR9|JIBAR12|CPI|PRIME|SREPO|SABOR)(-[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_14F_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_14F_Type_Pattern">
    <xs:attribute fixed="14F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TYPE)//(BA|BL|CPB|PN|TB|NOT|ZB|BB|DEB|NCD|LNCD|CLN|FRN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_22F-RESF_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RESF)/STRA/(WEEK|MNTH|QUTR|SEMI|ANNU|DALY|ISDF|ADHC))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_22F-RESF_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_22F-RESF_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_CRDDET_98A-RESD_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RESD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_CRDDET_98A-RESD_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_CRDDET_98A-RESD_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_36B-MINI_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MINI)//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_36B-MINI_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_36B-MINI_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_155_12_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="12" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_17B-CPMI_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CPMI)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_17B-CPMI_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_17B-CPMI_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_13B-CCYC_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CCYC)/STRA/[0-9]{1,3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_13B-CCYC_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_13B-CCYC_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_77B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((.{1,35}\n?){1,3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_77B_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_77B_Type_Pattern">
    <xs:attribute fixed="77B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_95R-ISSA_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISSA)/STRA/[A-Z]{2}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_95R-ISSA_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_95R-ISSA_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_GENL_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_GENL_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_GENL_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_98A-CRSD_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CRSD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_98A-CRSD_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_98A-CRSD_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_92A-INTR_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INTR)//(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_92A-INTR_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_92A-INTR_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_20_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(.{1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_20_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_20_Type_Pattern">
    <xs:attribute fixed="20" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_22F-CCFR_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CCFR)/STRA/(WEEK|MNTH|QUTR|SEMI|ANNU|NONE))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_22F-CCFR_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_22F-CCFR_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT598_155_77E_Type">
  <xs:simpleContent>
   <xs:extension base="xs:string">
    <xs:attribute fixed="77E" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_25_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((PLUS|MINUS|GT|LT|EQUAL|NONE|OF)(-[0-9]{1,12},([0-9]{1,2})*)?(-[A-Z0-9]{1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_25_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_25_Type_Pattern">
    <xs:attribute fixed="25" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_36B-AUTH_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(AUTH)//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_36B-AUTH_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_36B-AUTH_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_98A-MATU_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MATU)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_98A-MATU_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_98A-MATU_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CATG)//(1|2|3))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_92A-TAXR_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TAXR)//(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_92A-TAXR_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_92A-TAXR_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_17B-OVER_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OVER)//(Y|N))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_17B-OVER_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_17B-OVER_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_95R-ACCP_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACCP)/STRA/[A-Z]{2}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_95R-ACCP_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_95R-ACCP_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_MMID_FIA_CPDDET_98A-PAYD_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_CPDDET_98A-PAYD_Type">
  <xs:simpleContent>
   <xs:extension base="MT598_155_MMID_FIA_CPDDET_98A-PAYD_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT598_155_16R_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT598_155_MMID_FIA_CRDDET">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="ResetDate" type="MT598_155_MMID_FIA_CRDDET_98A-RESD_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_155_GENL">
  <xs:sequence>
   <xs:element name="FunctionOfMessage" type="MT598_155_GENL_23G_Type"/>
   <xs:element name="PreparationDateAndTime" type="MT598_155_GENL_98C_Type"/>
   <xs:element name="TypeOfInstructionIndicator" type="MT598_155_GENL_22F-INST_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_155_MMID_FIA">
  <xs:sequence>
   <xs:element minOccurs="0" name="CouponPaymentFrequency" type="MT598_155_MMID_FIA_22F-PFRE_Type"/>
   <xs:element minOccurs="0" name="CouponPaymentDay" type="MT598_155_MMID_FIA_13B-CPYD_Type"/>
   <xs:element minOccurs="0" name="CouponPaymentCycle" type="MT598_155_MMID_FIA_13B-CCYC_Type"/>
   <xs:element name="GenericCategory" type="MT598_155_MMID_FIA_12A_Type"/>
   <xs:element name="MMSecurityType" type="MT598_155_MMID_FIA_22H_Type"/>
   <xs:element name="MaturityDate" type="MT598_155_MMID_FIA_98A-MATU_Type"/>
   <xs:element name="IssueDate" type="MT598_155_MMID_FIA_98A-ISSU_Type"/>
   <xs:element minOccurs="0" name="InterestRate" type="MT598_155_MMID_FIA_92A-INTR_Type"/>
   <xs:element minOccurs="0" name="CouponRateTypeIndicator" type="MT598_155_MMID_FIA_22F-RTYP_Type"/>
   <xs:element name="MiniumNominalValue" type="MT598_155_MMID_FIA_36B-MINO_Type"/>
   <xs:element minOccurs="0" name="AuthorisedAmount" type="MT598_155_MMID_FIA_36B-AUTH_Type"/>
   <xs:element minOccurs="0" name="AcceptorOfMMSecurity" type="MT598_155_MMID_FIA_95R-ACCP_Type"/>
   <xs:element minOccurs="0" name="MinimumIssuerDenomination" type="MT598_155_MMID_FIA_36B-MINI_Type"/>
   <xs:element minOccurs="0" name="FloorCapRate" type="MT598_155_MMID_FIA_92D_Type"/>
   <xs:element minOccurs="0" name="CouponPaymentDayIndicator" type="MT598_155_MMID_FIA_22F-CPDI_Type"/>
   <xs:element minOccurs="0" name="WithholdingTaxOnInterestIndicator" type="MT598_155_MMID_FIA_17B-WITI_Type"/>
   <xs:element minOccurs="0" name="WithholdingTaxOnInterestRate" type="MT598_155_MMID_FIA_92A-TAXR_Type"/>
   <xs:element minOccurs="0" name="FinalCouponPaymentOnMaturity" type="MT598_155_MMID_FIA_17B-FCPM_Type"/>
   <xs:element minOccurs="0" name="CouponPaymentIndicator" type="MT598_155_MMID_FIA_17B-CPMI_Type"/>
   <xs:element minOccurs="0" name="AutomatedCouponPaymentCalculation" type="MT598_155_MMID_FIA_17B-ACPC_Type"/>
   <xs:element minOccurs="0" name="AutomatedCouponPaymentOnly" type="MT598_155_MMID_FIA_17B-ACPO_Type"/>
   <xs:element minOccurs="0" name="CouponRateCalculationDescription" type="MT598_155_MMID_FIA_77B_Type"/>
   <xs:element minOccurs="0" name="OverrideIndicator" type="MT598_155_MMID_FIA_17B-OVER_Type"/>
   <xs:element minOccurs="0" name="CouponPaymentCalculationMethod" type="MT598_155_MMID_FIA_13B-CPCM_Type"/>
   <xs:element minOccurs="0" name="CouponRateSource" type="MT598_155_MMID_FIA_14F_Type"/>
   <xs:element minOccurs="0" name="CouponRateVarianceFromSource" type="MT598_155_MMID_FIA_25_Type"/>
   <xs:element minOccurs="0" name="CouponCompoundFrequency" type="MT598_155_MMID_FIA_22F-CCFR_Type"/>
   <xs:element minOccurs="0" name="CouponResetFrequency" type="MT598_155_MMID_FIA_22F-RESF_Type"/>
   <xs:element minOccurs="0" name="CouponResetStartDate" type="MT598_155_MMID_FIA_98A-CRSD_Type"/>
   <xs:element minOccurs="0" name="CRDDET" type="MT598_155_MMID_FIA_CRDDET"/>
   <xs:element minOccurs="0" name="CPDDET" type="MT598_155_MMID_FIA_CPDDET"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_155_MMID">
  <xs:sequence>
   <xs:element minOccurs="0" name="IssuersCSDParticipantCode" type="MT598_155_MMID_95R-CSDP_Type"/>
   <xs:element name="IssuersParticipantCode" type="MT598_155_MMID_95R-ISSR_Type"/>
   <xs:element minOccurs="0" name="IssuingAgentsParticipantCode" type="MT598_155_MMID_95R-ISSA_Type"/>
   <xs:element name="IdenitficationOfSecurities" type="MT598_155_MMID_35B_Type"/>
   <xs:element name="NominalValueIssued" type="MT598_155_MMID_36B_Type"/>
   <xs:element name="IssuersSORAccountAtCSD" type="MT598_155_MMID_97B_Type"/>
   <xs:element minOccurs="0" name="FIA" type="MT598_155_MMID_FIA"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:complexType name="MT598_155_MMID_FIA_CPDDET">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="PaymentDate" type="MT598_155_MMID_FIA_CPDDET_98A-PAYD_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
 </xs:complexType>
 <xs:element name="MT598_155">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="TransactionReference" type="MT598_155_20_Type"/>
    <xs:element name="SubMessageType" type="MT598_155_12_Type"/>
    <xs:element name="ProprietaryMessage" type="MT598_155_77E_Type"/>
    <xs:element name="GENL" type="MT598_155_GENL"/>
    <xs:element name="MMID" type="MT598_155_MMID"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>
