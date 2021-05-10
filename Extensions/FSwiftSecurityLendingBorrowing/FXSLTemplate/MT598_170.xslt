<?xml version="1.0"?>
<xs:schema xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.w3schools.com" elementFormDefault="qualified">
	<xs:simpleType name="MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SAFE/STRA/IORT/[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="97B"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_FIA_98A-MATU_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:MATU//[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_FIA_98A-MATU_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_FIA_98A-MATU_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_FIA_98A-COUP_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:COUP//[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_FIA_98A-COUP_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_FIA_98A-COUP_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SETT//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="19A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_98A-SETT_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SETT//[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_98A-SETT_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_98A-SETT_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_SETDET_22F_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SETR/STRA/(XRFP|XRVP|XDFP|XDVP))"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_22F_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_SETDET_22F_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="22F"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_70E_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SPRO//)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_70E_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_70E_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="70E"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_12_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="([0-9]{3})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_12_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_12_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="12"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:(REAG|DEAG)/STRA/[A-Z]{2}[0-9]{6})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_SETPRTY_95R_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="95R"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_35B_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(ISIN {1}[A-Z0-9]{12}(\n)?((.{1,35}\n?){1,1})?(\n)?((.{1,35}\n?){1,3})?)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_35B_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_35B_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="35B"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_GENL_98C_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:PREP//[0-9]{8}[0-9]{6})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_GENL_98C_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_GENL_98C_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98C"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_20C-TRRF_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:TRRF//[A-Z]{2}[0-9]{6}/[0-9]{1,7})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_20C-TRRF_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_20C-TRRF_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="20C"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_GENL_23G_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="((NEWM|CANC))"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_GENL_23G_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_GENL_23G_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="23G"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_FIA_92A_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:INTR//(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_FIA_92A_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_FIA_92A_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="92A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:BULK//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_AMT_19A_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="19A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SETT//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_ALLOCDTLS_36B_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="36B"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_20_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(.{1,16})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_20_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_20_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="20"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_FIA_98A-FRNR_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:FRNR//[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_FIA_98A-FRNR_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_FIA_98A-FRNR_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:TRTE//[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_REPO_19A_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="19A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:TRTE//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="19A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_98B-SETT_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:SETT//OPEN)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_98B-SETT_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_98B-SETT_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98B"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_98A-TRAD_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:TRAD//[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_98A-TRAD_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_98A-TRAD_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:BULK//FAMT/[0-9]{1,12},([0-9]{1,2})*)|(:TTUN//FAMT/[0-9]{1,12},([0-9]{1,2})*)"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_AMT_36B_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="36B"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_REPO_98B-TERM_Type">
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="swiftTag" fixed="98B"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:TERM//[0-9]{8})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="98A"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:simpleType name="MT598_170_GENL_LINK_20C-RELA_Type_Pattern">
		<xs:restriction base="xs:string">
			<xs:pattern value="(:RELA//[A-Z]{2}[0-9]{6}/[0-9]{1,7})"/>
		</xs:restriction>
	</xs:simpleType>
	<xs:complexType name="MT598_170_GENL_LINK_20C-RELA_Type">
		<xs:simpleContent>
			<xs:extension base="MT598_170_GENL_LINK_20C-RELA_Type_Pattern">
				<xs:attribute name="swiftTag" fixed="20C"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_25D_Type">
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="swiftTag" fixed="25D"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:complexType name="MT598_170_77E_Type">
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="swiftTag" fixed="77E"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_SETPRTY">
		<xs:sequence>
			<xs:element name="ReceivingorDeliveringTradersCSDBPID" type="MT598_170_TRADDET_SETDET_SETPRTY_95R_Type"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_REPO">
		<xs:sequence>
			<xs:element name="RepurchaseDateFixed" type="MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type" minOccurs="0"/>
			<xs:element name="RepurchaseDateOpen" type="MT598_170_TRADDET_SETDET_REPO_98B-TERM_Type" minOccurs="0"/>
			<xs:element name="RepurchaseAmount" type="MT598_170_TRADDET_SETDET_REPO_19A_Type" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_SETDET_AMT">
		<xs:sequence>
			<xs:element name="NominalValue" type="MT598_170_TRADDET_SETDET_AMT_36B_Type"/>
			<xs:element name="SettlementAmount" type="MT598_170_TRADDET_SETDET_AMT_19A_Type" minOccurs="0"/>
			<xs:element name="TapTonUpNominalValue" type="MT598_170_TRADDET_SETDET_AMT_36B_Type" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_FIA">
		<xs:sequence>
			<xs:element name="CurrentInterestRate" type="MT598_170_TRADDET_FIA_92A_Type" minOccurs="0"/>
			<xs:element name="NextResetDate" type="MT598_170_TRADDET_FIA_98A-FRNR_Type" minOccurs="0"/>
			<xs:element name="MaturityDate" type="MT598_170_TRADDET_FIA_98A-MATU_Type" minOccurs="0"/>
			<xs:element name="NextPaymentDate" type="MT598_170_TRADDET_FIA_98A-COUP_Type" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_ALLOCDTLS">
		<xs:sequence>
			<xs:element name="SORAccount" type="MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type"/>
			<xs:element name="NominalValue" type="MT598_170_TRADDET_ALLOCDTLS_36B_Type"/>
			<xs:element name="SettlementAmount" type="MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type" minOccurs="0"/>
			<xs:element name="RepurchaseAmount" type="MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_GENL_LINK">
		<xs:sequence>
			<xs:element name="InternalTradeReference" type="MT598_170_GENL_LINK_20C-RELA_Type"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_GENL">
		<xs:sequence>
			<xs:element name="FunctionOfMessage" type="MT598_170_GENL_23G_Type"/>
			<xs:element name="PreparationDateAndTime" type="MT598_170_GENL_98C_Type" minOccurs="0"/>
			<xs:element name="LINK" type="MT598_170_GENL_LINK" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET_SETDET">
		<xs:sequence>
			<xs:element name="SettlementTransactionType" type="MT598_170_TRADDET_SETDET_22F_Type"/>
			<xs:element name="SETPRTY" type="MT598_170_TRADDET_SETDET_SETPRTY" maxOccurs="unbounded"/>
			<xs:element name="AMT" type="MT598_170_TRADDET_SETDET_AMT"/>
			<xs:element name="REPO" type="MT598_170_TRADDET_SETDET_REPO" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:complexType name="MT598_170_TRADDET">
		<xs:sequence>
			<xs:element name="InternalTradeReference" type="MT598_170_TRADDET_20C-TRRF_Type"/>
			<xs:element name="TradeDate" type="MT598_170_TRADDET_98A-TRAD_Type"/>
			<xs:element name="SettlementDate" type="MT598_170_TRADDET_98A-SETT_Type" minOccurs="0"/>
			<xs:element name="SettlementDateOpen" type="MT598_170_TRADDET_98B-SETT_Type" minOccurs="0"/>
			<xs:element name="IdentificationOfSecurities" type="MT598_170_TRADDET_35B_Type"/>
			<xs:element name="FIA" type="MT598_170_TRADDET_FIA" minOccurs="0"/>
			<xs:element name="AffirmationIndicator" type="MT598_170_TRADDET_25D_Type"/>
			<xs:element name="SettlementInstuctionProcessingNarrative" type="MT598_170_TRADDET_70E_Type" minOccurs="0"/>
			<xs:element name="SETDET" type="MT598_170_TRADDET_SETDET"/>
			<xs:element name="ALLOCDTLS" type="MT598_170_TRADDET_ALLOCDTLS" maxOccurs="unbounded"/>
		</xs:sequence>
		<xs:attribute name="swiftTag" fixed="16R"/>
	</xs:complexType>
	<xs:element name="MT598_170">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="TransactionReference" type="MT598_170_20_Type"/>
				<xs:element name="SubMessageType" type="MT598_170_12_Type"/>
				<xs:element name="ProprietaryMessage" type="MT598_170_77E_Type"/>
				<xs:element name="GENL" type="MT598_170_GENL"/>
				<xs:element name="TRADDET" type="MT598_170_TRADDET"/>
			</xs:sequence>
		</xs:complexType>
	</xs:element>
</xs:schema>
