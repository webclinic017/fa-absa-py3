<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT564_GENL_28E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([0-9]{1,5}/(LAST|MORE|ONLY))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_28E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_28E_Type_Pattern">
    <xs:attribute fixed="28E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CORP|SEME|COAF)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ADDB|CANC|NEWM|REPE|REPL|RMDR|WITH)(/(CODU|COPY|DUPL))?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CAEP|CAEV|CAMV)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_25D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_25D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_25D_Type_Pattern">
    <xs:attribute fixed="25D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_LINK_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_LINK_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_LINK_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_LINK_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_LINK_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_LINK_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_LINK_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_LINK_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_LINK_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_GENL_LINK_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CORP|PREV|RELA|CANC|COAF)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_GENL_LINK_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_GENL_LINK_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PLIS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MICO)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_12B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OPST)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_12B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_12B_Type_Pattern">
    <xs:attribute fixed="12B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_12C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)//[A-Z0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_12C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_12C_Type_Pattern">
    <xs:attribute fixed="12C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DENO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|EXPI|FRNR|MATU|ISSU|CALD|PUTT|DDTE|CONV)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRFC|NWFC|INTR|NXRT|DECL)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_92D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(WAPA)//[0-9,(?0-9)]{1,15}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_92D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_92D_Type_Pattern">
    <xs:attribute fixed="92D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_92K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRFC|NWFC|INTR|NXRT|DECL)//(UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_92K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_92K_Type_Pattern">
    <xs:attribute fixed="92K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_FIA_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MINO|SIZE)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_FIA_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_FIA_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_97C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//(GENR))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_97C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_97C_Type_Pattern">
    <xs:attribute fixed="97C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//(CUST|ICSD|NCSD|SHHE)/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_93B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ELIG|BLOK|BORR|COLI|COLO|LOAN|PEND|PENR|REGO|SETT|SPOS|TRAD|TRAN|NOMI|UNBA|INBA|OBAL|AFFB|UNAF)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_93B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_93B_Type_Pattern">
    <xs:attribute fixed="93B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_USECU_ACCTINFO_93C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ELIG|BLOK|BORR|COLI|COLO|LOAN|PEND|PENR|REGO|SETT|SPOS|TRAD|TRAN|NOMI|UNBA|INBA|OBAL|AFFB|UNAF)//(AMOR|FAMT|UNIT)/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_USECU_ACCTINFO_93C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_USECU_ACCTINFO_93C_Type_Pattern">
    <xs:attribute fixed="93C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(QINT)//(UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_36E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(QINT)//(UNIT)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_36E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_36E_Type_Pattern">
    <xs:attribute fixed="36E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_93B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(UNBA|INBA)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_93B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_93B_Type_Pattern">
    <xs:attribute fixed="93B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_93C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(UNBA|INBA)//(AMOR|FAMT|UNIT)/(ELIG|NELG)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_93C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_93C_Type_Pattern">
    <xs:attribute fixed="93C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_22F-4!c_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DISF|SELL)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_22F-4!c_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_22F-4!c_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_92D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RTUN)//[0-9,(?0-9)]{1,15}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_92D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_92D_Type_Pattern">
    <xs:attribute fixed="92D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MRKT)//(ACTU)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXPI|POST)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXPI|POST)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_69A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_69A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_69A_Type_Pattern">
    <xs:attribute fixed="69A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_69B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}[0-9]{6}/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_69B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_69B_Type_Pattern">
    <xs:attribute fixed="69B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_69C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_69C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_69C_Type_Pattern">
    <xs:attribute fixed="69C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_69D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}[0-9]{6}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_69D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_69D_Type_Pattern">
    <xs:attribute fixed="69D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_69E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//(ONGO|UKWN)/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_69E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_69E_Type_Pattern">
    <xs:attribute fixed="69E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_INTSEC_69F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//(ONGO|UKWN)/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_INTSEC_69F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_INTSEC_69F_Type_Pattern">
    <xs:attribute fixed="69F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ANOU|CERT|XDTE|EFFD|FDAT|PROD|REGI|RESU|SPLT|MEET|RDTE|TAXB|TSDT|LOTO|UNCO|WUCO|MET2|MET3|EQUL|ECDT|IFIX|MFIX|COAP|MATU|OAPD|SXDT|GUPA|ECPD|LAPD|MCTD|PAYD|TPDT|ETPD|PLDT|FILL|HEAR|ECRD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ANOU|CERT|XDTE|EFFD|FDAT|PROD|REGI|RESU|SPLT|MEET|RDTE|TAXB|TSDT|LOTO|UNCO|WUCO|MET2|MET3|EQUL|ECDT|IFIX|MFIX|COAP|MATU|OAPD|SXDT|GUPA|ECPD|LAPD|MCTD|PAYD|TPDT|ETPD|PLDT|FILL|HEAR|ECRD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ANOU|CERT|XDTE|EFFD|FDAT|PROD|REGI|RESU|SPLT|MEET|RDTE|TAXB|TSDT|LOTO|UNCO|WUCO|MET2|MET3|EQUL|ECDT|IFIX|MFIX|COAP|MATU|OAPD|SXDT|GUPA|ECPD|LAPD|MCTD|PAYD|TPDT|ETPD|PLDT|ECRD)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEET|MET2|MET3|MCTD|PLDT|)//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//[0-9]{8}/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69A_Type_Pattern">
    <xs:attribute fixed="69A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//[0-9]{8}[0-9]{6}/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69B_Type_Pattern">
    <xs:attribute fixed="69B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//[0-9]{8}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69C_Type_Pattern">
    <xs:attribute fixed="69C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//[0-9]{8}[0-9]{6}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69D_Type_Pattern">
    <xs:attribute fixed="69D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//(ONGO|UKWN)/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69E_Type_Pattern">
    <xs:attribute fixed="69E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//(ONGO|UKWN)/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69F_Type_Pattern">
    <xs:attribute fixed="69F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_69J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|INPE|CSPD|BLOK|CLCP|DSWN|DSDE|DSBT|DSDA|DSWA|DSPL|DSSE|DSWS|BOCL|CODS|SPLP)//(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_69J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_69J_Type_Pattern">
    <xs:attribute fixed="69J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_99A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DAAC)//(N)?[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_99A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_99A_Type_Pattern">
    <xs:attribute fixed="99A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RDIS|INTR|BIDI|NWFC|PTSC|PRFC|RINR|RSPR|SHRT|RLOS|DEVI)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_92F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INTR|BIDI|SHRT|RLOS|DEVI)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_92F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_92F_Type_Pattern">
    <xs:attribute fixed="92F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_92K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RDIS|INTR|BIDI|NWFC|PTSC|PRFC|RINR|RSPR)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_92K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_92K_Type_Pattern">
    <xs:attribute fixed="92K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_92P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BIDI)//[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_92P_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_92P_Type_Pattern">
    <xs:attribute fixed="92P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MAXP|MINP)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MAXP|MINP)//(ACTU|DISC|PLOT|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MAXP|MINP)//(UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_90L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MAXP|MINP)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_90L_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_90L_Type_Pattern">
    <xs:attribute fixed="90L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MQSO|QTSO|NBLT|NEWD|BASE|INCR)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_36C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MQSO|QTSO|NBLT|NEWD|BASE|INCR)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_36C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_36C_Type_Pattern">
    <xs:attribute fixed="36C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}//[A-Z]{1})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DIVI|CONV|DITY|OFFE|SELL|ESTA|ADDB|CHAN|RHDI|ECIO|TDTA|ELCT|LOTO|CEFI|CONS|INFO)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_94E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="([A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_94E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_94E_Type_Pattern">
    <xs:attribute fixed="94E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFO|WEBB|NAME)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CADETL_70G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(WEBB)//(([a-zA-Z0-9]|\.|,|-|\(|\)|/|=|'|\+|:|\?|!|&quot;|%|&amp;|\*|&lt;|&gt;|;|\{|@|#|_|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CADETL_70G_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CADETL_70G_Type_Pattern">
    <xs:attribute fixed="70G" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CAON)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CAOP|DISF|OFFE|OPTF|OSTA|CETI)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NDOM|DOMI)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OPTN)//[A-Z]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DFLT|STIN|RCHG|CERT|WTHD|CHAN|APLI)//(N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DVCP|EARD|EXPI|MKDT|PODT|SUBS|RDDT|CVPR|BORD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DVCP|EARD|EXPI|MKDT|PODT|SUBS|RDDT|CVPR|BORD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DVCP|EARD|EXPI|MKDT|PODT|SUBS|RDDT|CVPR|BORD)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EARD|MKDT|PODT|RDDT|CVPR|BORD)//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(RDDT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98F_Type_Pattern">
    <xs:attribute fixed="98F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BORD)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98J_Type_Pattern">
    <xs:attribute fixed="98J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_98K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BORD)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_98K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_98K_Type_Pattern">
    <xs:attribute fixed="98K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//[0-9]{8}/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69A_Type_Pattern">
    <xs:attribute fixed="69A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//[0-9]{8}[0-9]{6}/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69B_Type_Pattern">
    <xs:attribute fixed="69B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//[0-9]{8}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69C_Type_Pattern">
    <xs:attribute fixed="69C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//[0-9]{8}[0-9]{6}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69D_Type_Pattern">
    <xs:attribute fixed="69D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//(ONGO|UKWN)/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69E_Type_Pattern">
    <xs:attribute fixed="69E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//(ONGO|UKWN)/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69F_Type_Pattern">
    <xs:attribute fixed="69F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_69J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|REVO|PWAL|PARL|SUSP|AREV|DSWO)//(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_69J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_69J_Type_Pattern">
    <xs:attribute fixed="69J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TAXR|ATAX|INDX|OVEP|PROR|INTP|TXIN|WITL)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(IDFX)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(GRSS|TAXR|ATAX|INDX|INTP|NETT|TXIN|WITL)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92F_Type_Pattern">
    <xs:attribute fixed="92F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NETT|GRSS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/(ACTU|INDI))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92H_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92H_Type_Pattern">
    <xs:attribute fixed="92H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(GRSS|NETT|TDMT|INTP)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}(/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92J_Type_Pattern">
    <xs:attribute fixed="92J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(GRSS|TAXR|ATAX|INDX|OVEP|PROR|INTP|NETT|TXIN|WITL)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92K_Type_Pattern">
    <xs:attribute fixed="92K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_92R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(WITL|TAXR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_92R_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_92R_Type_Pattern">
    <xs:attribute fixed="92R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CINL|OSUB)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CINL|OSUB)//(ACTU|DISC|PLOT|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CINL|OSUB)//(UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MAEX|MIEX|MILT|NBLT|NEWD|BOLQ|FOLQ)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_36C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MAEX|MIEX|MILT|NBLT|NEWD|BOLQ|FOLQ)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_36C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_36C_Type_Pattern">
    <xs:attribute fixed="36C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TEMP|NELP|TXAP|ITYP|ETYP)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})|(:(DISF)/([A-Z0-9]{1,8})?/(BUYU|CINL|DIST|RDDN|RDUP|STAN|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CRDB|NSIS)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PLIS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MICO)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_12B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OPST)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_12B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_12B_Type_Pattern">
    <xs:attribute fixed="12B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_12C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)//[A-Z0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_12C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_12C_Type_Pattern">
    <xs:attribute fixed="12C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DENO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COUP|FRNR|MATU|ISSU|CALD|PUTT|DDTE|CONV)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISSU)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISSU)//(ACTU|DISC|PLOT|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISSU)//(UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRFC|NWFC|INTR|NXRT)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_92K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRFC|NWFC|INTR|NXRT)//(UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_92K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_92K_Type_Pattern">
    <xs:attribute fixed="92K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_FIA_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MINO|MIEX|MILT|SIZE)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_FIA_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ENTL)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE|COIN)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z0-9]{4}/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OPTN)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69A_Type_Pattern">
    <xs:attribute fixed="69A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}[0-9]{6}/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69B_Type_Pattern">
    <xs:attribute fixed="69B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69C_Type_Pattern">
    <xs:attribute fixed="69C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//[0-9]{8}[0-9]{6}/(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69D_Type_Pattern">
    <xs:attribute fixed="69D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//(ONGO|UKWN)/[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69E_Type_Pattern">
    <xs:attribute fixed="69E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//(ONGO|UKWN)/[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69F_Type_Pattern">
    <xs:attribute fixed="69F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_69J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRDP)//(ONGO|UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_69J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_69J_Type_Pattern">
    <xs:attribute fixed="69J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|CINL|OFFR|PRPP)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|CINL|OFFR|PRPP|CAVA)//[A-Z0-9]{4}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INDC|MRKT|CINL|OFFR|PRPP|CAVA)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR)//(AMOR|FAMT|UNIT)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90F_Type_Pattern">
    <xs:attribute fixed="90F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR)//[A-Z0-9]{4}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90J_Type_Pattern">
    <xs:attribute fixed="90J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRPP)//[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90K_Type_Pattern">
    <xs:attribute fixed="90K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_90L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_90L_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_90L_Type_Pattern">
    <xs:attribute fixed="90L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAT|CHAR|FISC|RATE|TAXC|TRAX)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADEX|NEWO|ADSR)//[0-9,(?0-9)]{1,15}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92D_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92D_Type_Pattern">
    <xs:attribute fixed="92D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CHAR|TAXC)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92F_Type_Pattern">
    <xs:attribute fixed="92F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TAXC)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}(/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92J_Type_Pattern">
    <xs:attribute fixed="92J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADEX|NEWO|ADSR|CHAR|FISC|RATE|TAXC|TRAX)//(UKWN))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92K_Type_Pattern">
    <xs:attribute fixed="92K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADEX|NEWO|ADSR)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92L_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92L_Type_Pattern">
    <xs:attribute fixed="92L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NEWO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92M_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92M_Type_Pattern">
    <xs:attribute fixed="92M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_92N_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NEWO)//[0-9,(?0-9)]{1,15}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_92N_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_92N_Type_Pattern">
    <xs:attribute fixed="92N" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD|AVAL|DIVR|EARL|PPDT|LTRD)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD|AVAL|DIVR|EARL|PPDT|LTRD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD|AVAL|DIVR|EARL|PPDT|LTRD)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_SECMOVE_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EARL)//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_SECMOVE_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NELP|ITYP|TXAP|ETYP)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CRDB|CONT)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(COIN)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_19B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ENTL|RESU|OCMT|CAPG|INDM|CINL|CHAR|FLFR|UNFR|TXFR|TXDF|SOIC|GRSS|INTR|MKTC|NETT|PRIN|REIN|TAXC|TAXR|WITL|REDP|ATAX|INCO|EXEC|LOCO|PAMM|REGF|SHIP|SOFE|STAM|STEX|VATA|FISC|MFDV|TXRC|EUTR|ACRU|EQUL|FTCA|NRAT|BWIT|TXIN|TRAX|DEDI|DEEM|DEFP|DEIT|DERY)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_19B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_19B_Type_Pattern">
    <xs:attribute fixed="19B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD|VALU|EARL|FXDT)//[0-9]{8})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD|VALU|EARL|FXDT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PAYD|VALU|EARL|FXDT)//[0-9]{8}[0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EARL)//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ATAX|CHAR|ESOF|FLFR|FISC|INCE|INTP|NRES|RATE|SOFE|TAXC|TAXR|TXIN|TXPR|TXRC|WITL)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ATAX|CHAR|EQUL|ESOF|FLFR|GRSS|INCE|INTP|NETT|NRES|SOFE|TAXC|TAXR|TXIN|WITL)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92F_Type_Pattern">
    <xs:attribute fixed="92F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NETT|GRSS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92H_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92H_Type_Pattern">
    <xs:attribute fixed="92H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(GRSS|NETT|TAXC|INTP)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}(/[A-Z0-9]{4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92J_Type_Pattern">
    <xs:attribute fixed="92J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(WITL|TXRC|TXPR|TXIN|TAXR|TAXC|SOFE|RATE|NRES|NETT|INTP|INCE|GRSS|FISC|FLFR|ESOF|EQUL|CHAR|ATAX)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92K_Type_Pattern">
    <xs:attribute fixed="92K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92M_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ESOF|SOFE)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92M_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92M_Type_Pattern">
    <xs:attribute fixed="92M" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_92R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(WITL|TAXR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_92R_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_92R_Type_Pattern">
    <xs:attribute fixed="92R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR|PRPP)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR|PRPP)//(ACTU|DISC|PLOT|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR|PRPP)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90E_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90E_Type_Pattern">
    <xs:attribute fixed="90E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR)//(AMOR|FAMT|UNIT)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90F_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90F_Type_Pattern">
    <xs:attribute fixed="90F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90J_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR)//(ACTU|DISC|PLOT|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15}/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90J_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90J_Type_Pattern">
    <xs:attribute fixed="90J" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90K_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRPP)//[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90K_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90K_Type_Pattern">
    <xs:attribute fixed="90K" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_CASHMOVE_90L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OFFR)//(N)?[0-9,(?0-9)]{1,15})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE_90L_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_CASHMOVE_90L_Type_Pattern">
    <xs:attribute fixed="90L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_CAOPTN_70E-4!c_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX|TXNR|INCO|COMP|NSER|TAXE|DISC|CETI)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_CAOPTN_70E-4!c_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_CAOPTN_70E-4!c_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_ADDINFO_70E-4!c_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX|TXNR|REGI|INCO|COMP|PACO|TAXE|DISC|BAIN|CETI)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_ADDINFO_70E-4!c_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_ADDINFO_70E-4!c_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_ADDINFO_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ISAG|ISSU|OFFO|TAGT)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_ADDINFO_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_ADDINFO_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_ADDINFO_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEOR|MERE|ISAG|PAYA|CODO|REGR|DROP|PSAG|RESA|SOLA|INFA|ISSU|OFFO|TAGT)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_ADDINFO_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_ADDINFO_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_ADDINFO_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEOR|MERE|ISAG|PAYA|CODO|REGR|DROP|PSAG|RESA|SOLA|INFA|ISSU|OFFO|TAGT)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_ADDINFO_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_ADDINFO_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT564_ADDINFO_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEOR|MERE|ISAG|PAYA|CODO|REGR|DROP|PSAG|RESA|SOLA|INFA|ISSU|OFFO|TAGT)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT564_ADDINFO_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT564_ADDINFO_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:complexType name="MT564_GENL">
  <xs:sequence>
   <xs:element minOccurs="0" name="ContinuationIndicator" type="MT564_GENL_28E_Type"/>
   <xs:element maxOccurs="unbounded" name="Reference" type="MT564_GENL_20C_Type"/>
   <xs:element name="FunctionOfMessage" type="MT564_GENL_23G_Type"/>
   <xs:element maxOccurs="unbounded" name="Indicator" type="MT564_GENL_22F_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PreparationDateTime_A" type="MT564_GENL_98A_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_C" type="MT564_GENL_98C_Type"/>
   </xs:choice>
   <xs:element name="ProcessingStatus" type="MT564_GENL_25D_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="LINK" type="MT564_GENL_LINK"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="GENL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_GENL_LINK">
  <xs:sequence>
   <xs:element minOccurs="0" name="LinkageTypeIndicator" type="MT564_GENL_LINK_22F_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="LinkedMessage_A" type="MT564_GENL_LINK_13A_Type"/>
    <xs:element minOccurs="0" name="LinkedMessage_B" type="MT564_GENL_LINK_13B_Type"/>
   </xs:choice>
   <xs:element name="Reference" type="MT564_GENL_LINK_20C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="LINK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_USECU">
  <xs:sequence>
   <xs:element name="IdentificationOfFinancialInstrument" type="MT564_USECU_35B_Type"/>
   <xs:element minOccurs="0" name="FIA" type="MT564_USECU_FIA"/>
   <xs:element maxOccurs="unbounded" name="ACCTINFO" type="MT564_USECU_ACCTINFO"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="USECU" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_USECU_FIA">
  <xs:sequence>
   <xs:element minOccurs="0" name="PlaceOfListing" type="MT564_USECU_FIA_94B_Type"/>
   <xs:element minOccurs="0" name="MethodOfInterestComputationIndicator" type="MT564_USECU_FIA_22F_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_A" type="MT564_USECU_FIA_12A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_B" type="MT564_USECU_FIA_12B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_C" type="MT564_USECU_FIA_12C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="CurrencyOfDenomination" type="MT564_USECU_FIA_11A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime" type="MT564_USECU_FIA_98A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT564_USECU_FIA_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_D" type="MT564_USECU_FIA_92D_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_K" type="MT564_USECU_FIA_92K_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument" type="MT564_USECU_FIA_36B_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_USECU_ACCTINFO">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="AccountOwner_P" type="MT564_USECU_ACCTINFO_95P_Type"/>
    <xs:element minOccurs="0" name="AccountOwner_R" type="MT564_USECU_ACCTINFO_95R_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="SafekeepingAccount_A" type="MT564_USECU_ACCTINFO_97A_Type"/>
    <xs:element name="SafekeepingAccount_C" type="MT564_USECU_ACCTINFO_97C_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PlaceofSafekeeping_B" type="MT564_USECU_ACCTINFO_94B_Type"/>
    <xs:element minOccurs="0" name="PlaceofSafekeeping_C" type="MT564_USECU_ACCTINFO_94C_Type"/>
    <xs:element minOccurs="0" name="PlaceofSafekeeping_F" type="MT564_USECU_ACCTINFO_94F_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Balance_B" type="MT564_USECU_ACCTINFO_93B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Balance_C" type="MT564_USECU_ACCTINFO_93C_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="ACCTINFO" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_INTSEC">
  <xs:sequence>
   <xs:element name="IdentificationOfFinancialInstrument" type="MT564_INTSEC_35B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="QuantityOfIntermediateSecurities_B" type="MT564_INTSEC_36B_Type"/>
    <xs:element minOccurs="0" name="QuantityOfIntermediateSecurities_E" type="MT564_INTSEC_36E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Balance_B" type="MT564_INTSEC_93B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Balance_C" type="MT564_INTSEC_93C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT564_INTSEC_22F-4!c_Type"/>
   <xs:element minOccurs="0" name="IntermediateSecuritiesToUnderlying" type="MT564_INTSEC_92D_Type"/>
   <xs:element minOccurs="0" name="MarketPrice" type="MT564_INTSEC_90B_Type"/>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT564_INTSEC_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT564_INTSEC_98B_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="TradingPeriod_A" type="MT564_INTSEC_69A_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_B" type="MT564_INTSEC_69B_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_C" type="MT564_INTSEC_69C_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_D" type="MT564_INTSEC_69D_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_E" type="MT564_INTSEC_69E_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_F" type="MT564_INTSEC_69F_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="INTSEC" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_CADETL">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_A" type="MT564_CADETL_98A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_B" type="MT564_CADETL_98B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_C" type="MT564_CADETL_98C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_E" type="MT564_CADETL_98E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_A" type="MT564_CADETL_69A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_B" type="MT564_CADETL_69B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_C" type="MT564_CADETL_69C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_D" type="MT564_CADETL_69D_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_E" type="MT564_CADETL_69E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_F" type="MT564_CADETL_69F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_J" type="MT564_CADETL_69J_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="NumberofDaysAccrued" type="MT564_CADETL_99A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT564_CADETL_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_F" type="MT564_CADETL_92F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_K" type="MT564_CADETL_92K_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_P" type="MT564_CADETL_92P_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT564_CADETL_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT564_CADETL_90B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_E" type="MT564_CADETL_90E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_L" type="MT564_CADETL_90L_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument_B" type="MT564_CADETL_36B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument_C" type="MT564_CADETL_36C_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="CouponNumber_A" type="MT564_CADETL_13A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="CouponNumber_B" type="MT564_CADETL_13B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT564_CADETL_17B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Indicator" type="MT564_CADETL_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Place" type="MT564_CADETL_94E_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_E" type="MT564_CADETL_70E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative_G" type="MT564_CADETL_70G_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="CADETL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_CAOPTN">
  <xs:sequence>
   <xs:element name="NumberIdentification" type="MT564_CAOPTN_13A_Type"/>
   <xs:element maxOccurs="unbounded" name="Indicator" type="MT564_CAOPTN_22F_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Place" type="MT564_CAOPTN_94C_Type"/>
   <xs:element minOccurs="0" name="CurrencyOption" type="MT564_CAOPTN_11A_Type"/>
   <xs:element maxOccurs="unbounded" name="Flag" type="MT564_CAOPTN_17B_Type"/>
   <xs:element minOccurs="0" name="IdentificationOfFinancialInstrument" type="MT564_CAOPTN_35B_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_A" type="MT564_CAOPTN_98A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_B" type="MT564_CAOPTN_98B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_C" type="MT564_CAOPTN_98C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_E" type="MT564_CAOPTN_98E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_F" type="MT564_CAOPTN_98F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_J" type="MT564_CAOPTN_98J_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_K" type="MT564_CAOPTN_98K_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_A" type="MT564_CAOPTN_69A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_B" type="MT564_CAOPTN_69B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_C" type="MT564_CAOPTN_69C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_D" type="MT564_CAOPTN_69D_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_E" type="MT564_CAOPTN_69E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_F" type="MT564_CAOPTN_69F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Period_J" type="MT564_CAOPTN_69J_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT564_CAOPTN_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_B" type="MT564_CAOPTN_92B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_F" type="MT564_CAOPTN_92F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_H" type="MT564_CAOPTN_92H_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_J" type="MT564_CAOPTN_92J_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_K" type="MT564_CAOPTN_92K_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_R" type="MT564_CAOPTN_92R_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT564_CAOPTN_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT564_CAOPTN_90B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_E" type="MT564_CAOPTN_90E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument_B" type="MT564_CAOPTN_36B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument_C" type="MT564_CAOPTN_36C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SECMOVE" type="MT564_CAOPTN_SECMOVE"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="CASHMOVE" type="MT564_CAOPTN_CASHMOVE"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative" type="MT564_CAOPTN_70E-4!c_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="CAOPTN" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Indicator_F" type="MT564_CAOPTN_SECMOVE_22F_Type"/>
    <xs:element maxOccurs="unbounded" name="Indicator_H" type="MT564_CAOPTN_SECMOVE_22H_Type"/>
   </xs:choice>
   <xs:element name="IdentificationOfFinancialInstrument" type="MT564_CAOPTN_SECMOVE_35B_Type"/>
   <xs:element minOccurs="0" name="FIA" type="MT564_CAOPTN_SECMOVE_FIA"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="EntitledQuantity" type="MT564_CAOPTN_SECMOVE_36B_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_B" type="MT564_CAOPTN_SECMOVE_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_C" type="MT564_CAOPTN_SECMOVE_94C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PlaceOfSafekeeping_F" type="MT564_CAOPTN_SECMOVE_94F_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="Indicator_F" type="MT564_CAOPTN_SECMOVE_22F_Type"/>
   <xs:element minOccurs="0" name="CurrencyOption" type="MT564_CAOPTN_SECMOVE_11A_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="TradingPeriod_A" type="MT564_CAOPTN_SECMOVE_69A_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_B" type="MT564_CAOPTN_SECMOVE_69B_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_C" type="MT564_CAOPTN_SECMOVE_69C_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_D" type="MT564_CAOPTN_SECMOVE_69D_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_E" type="MT564_CAOPTN_SECMOVE_69E_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_F" type="MT564_CAOPTN_SECMOVE_69F_Type"/>
    <xs:element minOccurs="0" name="TradingPeriod_J" type="MT564_CAOPTN_SECMOVE_69J_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT564_CAOPTN_SECMOVE_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT564_CAOPTN_SECMOVE_90B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_E" type="MT564_CAOPTN_SECMOVE_90E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_F" type="MT564_CAOPTN_SECMOVE_90F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_J" type="MT564_CAOPTN_SECMOVE_90J_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_K" type="MT564_CAOPTN_SECMOVE_90K_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_L" type="MT564_CAOPTN_SECMOVE_90L_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT564_CAOPTN_SECMOVE_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_D" type="MT564_CAOPTN_SECMOVE_92D_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_F" type="MT564_CAOPTN_SECMOVE_92F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_J" type="MT564_CAOPTN_SECMOVE_92J_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_K" type="MT564_CAOPTN_SECMOVE_92K_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_L" type="MT564_CAOPTN_SECMOVE_92L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_M" type="MT564_CAOPTN_SECMOVE_92M_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_N" type="MT564_CAOPTN_SECMOVE_92N_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT564_CAOPTN_SECMOVE_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT564_CAOPTN_SECMOVE_98B_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT564_CAOPTN_SECMOVE_98C_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_E" type="MT564_CAOPTN_SECMOVE_98E_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SECMOVE" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_CAOPTN_SECMOVE_FIA">
  <xs:sequence>
   <xs:element minOccurs="0" name="PlaceOfListing" type="MT564_CAOPTN_SECMOVE_FIA_94B_Type"/>
   <xs:element minOccurs="0" name="MethodOfInterestComputationIndicator" type="MT564_CAOPTN_SECMOVE_FIA_22F_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_A" type="MT564_CAOPTN_SECMOVE_FIA_12A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_B" type="MT564_CAOPTN_SECMOVE_FIA_12B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="TypeOfFinancialInstrument_C" type="MT564_CAOPTN_SECMOVE_FIA_12C_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="CurrencyOfDenomination" type="MT564_CAOPTN_SECMOVE_FIA_11A_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime" type="MT564_CAOPTN_SECMOVE_FIA_98A_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="IssuePrice_A" type="MT564_CAOPTN_SECMOVE_FIA_90A_Type"/>
    <xs:element minOccurs="0" name="IssuePrice_B" type="MT564_CAOPTN_SECMOVE_FIA_90B_Type"/>
    <xs:element minOccurs="0" name="IssuePrice_E" type="MT564_CAOPTN_SECMOVE_FIA_90E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT564_CAOPTN_SECMOVE_FIA_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_K" type="MT564_CAOPTN_SECMOVE_FIA_92K_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="QuantityOfFinancialInstrument" type="MT564_CAOPTN_SECMOVE_FIA_36B_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_CAOPTN_CASHMOVE">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Indicator_F" type="MT564_CAOPTN_CASHMOVE_22F_Type"/>
    <xs:element maxOccurs="unbounded" name="Indicator_H" type="MT564_CAOPTN_CASHMOVE_22H_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="Place" type="MT564_CAOPTN_CASHMOVE_94C_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="CashAccount_A" type="MT564_CAOPTN_CASHMOVE_97A_Type"/>
    <xs:element minOccurs="0" name="CashAccount_E" type="MT564_CAOPTN_CASHMOVE_97E_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT564_CAOPTN_CASHMOVE_19B_Type"/>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT564_CAOPTN_CASHMOVE_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT564_CAOPTN_CASHMOVE_98B_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT564_CAOPTN_CASHMOVE_98C_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_E" type="MT564_CAOPTN_CASHMOVE_98E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT564_CAOPTN_CASHMOVE_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_B" type="MT564_CAOPTN_CASHMOVE_92B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_F" type="MT564_CAOPTN_CASHMOVE_92F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_H" type="MT564_CAOPTN_CASHMOVE_92H_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_J" type="MT564_CAOPTN_CASHMOVE_92J_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_K" type="MT564_CAOPTN_CASHMOVE_92K_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_M" type="MT564_CAOPTN_CASHMOVE_92M_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_R" type="MT564_CAOPTN_CASHMOVE_92R_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_A" type="MT564_CAOPTN_CASHMOVE_90A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_B" type="MT564_CAOPTN_CASHMOVE_90B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_E" type="MT564_CAOPTN_CASHMOVE_90E_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_F" type="MT564_CAOPTN_CASHMOVE_90F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_J" type="MT564_CAOPTN_CASHMOVE_90J_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_K" type="MT564_CAOPTN_CASHMOVE_90K_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Price_L" type="MT564_CAOPTN_CASHMOVE_90L_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="CASHMOVE" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT564_ADDINFO">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Narrative" type="MT564_ADDINFO_70E-4!c_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PARTY_L" type="MT564_ADDINFO_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PARTY_P" type="MT564_ADDINFO_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PARTY_Q" type="MT564_ADDINFO_95Q_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PARTY_R" type="MT564_ADDINFO_95R_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="ADDINFO" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT564">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="GENL" type="MT564_GENL"/>
    <xs:element name="USECU" type="MT564_USECU"/>
    <xs:element minOccurs="0" name="INTSEC" type="MT564_INTSEC"/>
    <xs:element minOccurs="0" name="CADETL" type="MT564_CADETL"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="CAOPTN" type="MT564_CAOPTN"/>
    <xs:element minOccurs="0" name="ADDINFO" type="MT564_ADDINFO"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

