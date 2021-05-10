<?xml version="1.0" ?>
<xs:schema elementFormDefault="qualified" targetNamespace="http://www.w3schools.com" xmlns="http://www.w3schools.com" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12A_Type_Pattern">
    <xs:attribute fixed="12A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(AMNT)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90A_Type_Pattern">
    <xs:attribute fixed="90A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceD_AdditionalInformation_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEOR|MERE|INVE|QFIN)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceD_AdditionalInformation_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceD_AdditionalInformation_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REDE|PAYM)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceD_AdditionalInformation_95C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(INVE)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceD_AdditionalInformation_95C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceD_AdditionalInformation_95C_Type_Pattern">
    <xs:attribute fixed="95C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE|CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_23G_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((CAST|INST|PENA)(/(CODU|COPY|DUPL))?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_23G_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_23G_Type_Pattern">
    <xs:attribute fixed="23G" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REPA|ASDP)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REPA|ASDP)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DACO)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SPRO)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_94L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLEA|TRAD|SAFE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_94L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_94L_Type_Pattern">
    <xs:attribute fixed="94L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_25D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MTCH/SETT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_25D_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_25D_Type_Pattern">
    <xs:attribute fixed="25D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|EXCH)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceD_AdditionalInformation_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEOR|MERE|INVE|QFIN)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceD_AdditionalInformation_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceD_AdditionalInformation_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_24B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CAND|CANP|CACK|CGEN|DEND|MOPN|NMAT|PACK|PEND|PENF|PPRC|REJT|REPR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_24B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_24B_Type_Pattern">
    <xs:attribute fixed="24B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|EXCH)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REAS)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_97B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_97B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_97B_Type_Pattern">
    <xs:attribute fixed="97B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_24B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACTV|REMO|UPDT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_24B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_24B_Type_Pattern">
    <xs:attribute fixed="24B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LIQU|SMEM)//(N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REAS)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern">
    <xs:attribute fixed="13B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXSE|SETT|ADEL|TRAD|EXVA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SEME)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REAS)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70D_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70D_Type_Pattern">
    <xs:attribute fixed="70D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CBON|GBON|GOMB|ILSH|LISH|NBON|OTHR)(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PRIC|TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//[^/](([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT)//(AMOR|FAMT|UNIT)/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLAS)/[A-Z0-9]{6})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12C_Type_Pattern">
    <xs:attribute fixed="12C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(AMCO)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_94F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z0-9]{4}/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_94F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_94F_Type_Pattern">
    <xs:attribute fixed="94F" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXSE|SETT|ADEL|TRAD|EXVA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXCH)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92B_Type_Pattern">
    <xs:attribute fixed="92B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PSET)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95C_Type_Pattern">
    <xs:attribute fixed="95C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_69B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(STAT)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_69B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_69B_Type_Pattern">
    <xs:attribute fixed="69B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_69A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(STAT)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_69A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_69A_Type_Pattern">
    <xs:attribute fixed="69A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_36B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PSTA)//(AMOR|FAMT|UNIT)/[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_36B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_36B_Type_Pattern">
    <xs:attribute fixed="36B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(OCMT|SETT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRTR|SETR)([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_94H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CLEA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_94H_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_94H_Type_Pattern">
    <xs:attribute fixed="94H" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PSTA)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(AMNT)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90B_Type_Pattern">
    <xs:attribute fixed="90B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW|CACO)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CMPU)//(N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REP)/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_94B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD|SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,30}[^/])?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_94B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_94B_Type_Pattern">
    <xs:attribute fixed="94B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PDRA)//(N)?[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92A_Type_Pattern">
    <xs:attribute fixed="92A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceD_AdditionalInformation_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceD_AdditionalInformation_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceD_AdditionalInformation_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXSE|SETT|ADEL|TRAD|EXVA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))|(:(ASTS|MTCH|CUTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(POOL|PREV|RELA|TRRF|COMM|CORP|TCTR|CLTR|CLCI|TRCI|NTSP|MITI|PCTI)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PEDA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_98B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETT|TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_98B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_98B_Type_Pattern">
    <xs:attribute fixed="98B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_17B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MRED)//(N|Y))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_17B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_17B_Type_Pattern">
    <xs:attribute fixed="17B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREF|PCOM)//(^/)([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}(^/))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRCA)//([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_94C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//[A-Z]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_94C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_94C_Type_Pattern">
    <xs:attribute fixed="94C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_25D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CPRC|IPRC|MTCH|SETT|SPRC|CALL|INMH|TPRC)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_25D_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_25D_Type_Pattern">
    <xs:attribute fixed="25D" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95R_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(BUYR|DEAG|DECU|DEI1|DEI2|REAG|RECU|REI1|REI2|SELL)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95R_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95R_Type_Pattern">
    <xs:attribute fixed="95R" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASH)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,34})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97E_Type_Pattern">
    <xs:attribute fixed="97E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PNTP)/(C)?{1,8}/(LMFP|SEEP))|(:(CALM)/([A-Z0-9]{1,8})?/(BOTH|CASH|MIXE|SECU))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceD_AdditionalInformation_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(MEOR|MERE|INVE|QFIN)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceD_AdditionalInformation_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceD_AdditionalInformation_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CASD|REPA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ACOW)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SECU|CASH)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_24B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(NMAT|PENF)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_24B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_24B_Type_Pattern">
    <xs:attribute fixed="24B" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(FIAN)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_11A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PECU)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_11A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_11A_Type_Pattern">
    <xs:attribute fixed="11A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_19A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(AGNT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9]{1,12},([0-9]{1,2})*)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_19A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_19A_Type_Pattern">
    <xs:attribute fixed="19A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_35B_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="((ISIN {1}[A-Z0-9]{12})?(\n)?((([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_35B_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_35B_Type_Pattern">
    <xs:attribute fixed="35B" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(LINK)//[A-Z0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern">
    <xs:attribute fixed="13A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_22H_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REDE|PAYM)//[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_22H_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_22H_Type_Pattern">
    <xs:attribute fixed="22H" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DACO)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRCA)//([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95Q_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(REPA)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95Q_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95Q_Type_Pattern">
    <xs:attribute fixed="95Q" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SAFE)//([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97A_Type_Pattern">
    <xs:attribute fixed="97A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ASDP)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(CODE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_98E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_98E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_98E_Type_Pattern">
    <xs:attribute fixed="98E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_22F_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(SETR|STCO|TRCA|STAM|RTGS|REGT|BENE|CASY|TCPI|REPT|MACL|BLOC|REST|SETS|NETT|CCPT|LEOG|COLA|COLE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_22F_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_22F_Type_Pattern">
    <xs:attribute fixed="22F" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PEDA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98C_Type_Pattern">
    <xs:attribute fixed="98C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(EXSE|SETT|ADEL|TRAD|EXVA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_25D_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PNST)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_25D_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_25D_Type_Pattern">
    <xs:attribute fixed="25D" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PEDA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRAD)/([A-Z0-9]{1,8})?//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94L_Type_Pattern">
    <xs:attribute fixed="94L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_98A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_98A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_98A_Type_Pattern">
    <xs:attribute fixed="98A" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(TRRF)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern">
    <xs:attribute fixed="20U" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_95L_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ALTE)//[A-Z0-9]{18}[0-9]{2})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_95L_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_95L_Type_Pattern">
    <xs:attribute fixed="95L" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95P_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ASDP|REPA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95P_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95P_Type_Pattern">
    <xs:attribute fixed="95P" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_20C_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,16}[^/])"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_20C_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_20C_Type_Pattern">
    <xs:attribute fixed="20C" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_70E_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(ADTX)//(([a-zA-Z0-9]|/|-|\?|:|\(|\)|\.|,|'|\+|\n|\s){1,35}\n?){1,10})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_70E_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_70E_Type_Pattern">
    <xs:attribute fixed="70E" name="swiftTag"/>
    <xs:attribute default="False" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_99A_Type_Pattern">
  <xs:restriction base="xs:string">
   <xs:pattern value="(:(DAAC)//(N)?[0-9]{3})"/>
  </xs:restriction>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_99A_Type">
  <xs:simpleContent>
   <xs:extension base="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_99A_Type_Pattern">
    <xs:attribute fixed="99A" name="swiftTag"/>
    <xs:attribute default="True" name="isMandatory"/>
   </xs:extension>
  </xs:simpleContent>
 </xs:complexType>
 <xs:simpleType name="MT548_16R_Type">
  <xs:restriction base="xs:string"/>
 </xs:simpleType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status">
  <xs:sequence>
   <xs:element name="StatusCode" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_25D_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceC1a1A2a1A_Reason" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="STAT" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason">
  <xs:sequence>
   <xs:element name="ReasonCode" type="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_24B_Type"/>
   <xs:element minOccurs="0" name="ReasonNarrative" type="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason_70D_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="REAS" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status">
  <xs:sequence>
   <xs:element name="StatusCode" type="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_25D_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceA2a_Reason" type="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status_SubSequenceA2a_Reason"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="STAT" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes">
  <xs:sequence>
   <xs:element name="IdentificationOfFinancialInstrument" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_35B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="TypeOfFinancialInstrument_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12A_Type"/>
    <xs:element minOccurs="0" name="TypeOfFinancialInstrument_C" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_12C_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Flag" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_17B_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Price_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90A_Type"/>
    <xs:element minOccurs="0" name="Price_B" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_90B_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_B" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_L" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_94L_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="DateTime_C" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_98C_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_B" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_92B_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="FinancialInstrumentAttributeNarrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="FIA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="StatementPeriod_A" type="MT548_SequenceC_Penalties_69A_Type"/>
    <xs:element minOccurs="0" name="StatementPeriod_B" type="MT548_SequenceC_Penalties_69B_Type"/>
   </xs:choice>
   <xs:element name="CompleteUpdatesIndicator" type="MT548_SequenceC_Penalties_22F_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT548_SequenceC_Penalties_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT548_SequenceC_Penalties_95P_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="SubSequenceC1_PenaltiesPerCurrencyForAParty" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty"/>
   <xs:element minOccurs="0" name="Narrative" type="MT548_SequenceC_Penalties_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="PENA" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PenaltyDateTime_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PenaltyDateTime_C" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="PenaltyDateTime_E" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_98E_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="MissingReferenceData" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_17B_Type"/>
   <xs:element minOccurs="0" name="SubSequenceC1a1A1_FinancialInstrumentAttributes" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A1_FinancialInstrumentAttributes"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Rate_B" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_92B_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_19A_Type"/>
   <xs:element minOccurs="0" name="SubSequenceC1a1A2_RelatedTransaction" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction"/>
   <xs:element minOccurs="0" name="Narrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="CALDET" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_B" type="MT548_SequenceB_SettlementTransactionDetails_94B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_C" type="MT548_SequenceB_SettlementTransactionDetails_94C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_F" type="MT548_SequenceB_SettlementTransactionDetails_94F_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_H" type="MT548_SequenceB_SettlementTransactionDetails_94H_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Place_L" type="MT548_SequenceB_SettlementTransactionDetails_94L_Type"/>
   </xs:choice>
   <xs:element name="IdentificationOfTheFinancialInstrument" type="MT548_SequenceB_SettlementTransactionDetails_35B_Type"/>
   <xs:element maxOccurs="unbounded" name="QuantityOfFinancialInstrumentToBeSettled" type="MT548_SequenceB_SettlementTransactionDetails_36B_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="Amount" type="MT548_SequenceB_SettlementTransactionDetails_19A_Type"/>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT548_SequenceB_SettlementTransactionDetails_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT548_SequenceB_SettlementTransactionDetails_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT548_SequenceB_SettlementTransactionDetails_95R_Type"/>
   </xs:choice>
   <xs:choice>
    <xs:element name="SafekeepingAccount_A" type="MT548_SequenceB_SettlementTransactionDetails_97A_Type"/>
    <xs:element name="SafekeepingAccount_B" type="MT548_SequenceB_SettlementTransactionDetails_97B_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Indicator_F" type="MT548_SequenceB_SettlementTransactionDetails_22F_Type"/>
    <xs:element maxOccurs="unbounded" name="Indicator_H" type="MT548_SequenceB_SettlementTransactionDetails_22H_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT548_SequenceB_SettlementTransactionDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT548_SequenceB_SettlementTransactionDetails_98B_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT548_SequenceB_SettlementTransactionDetails_98C_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_E" type="MT548_SequenceB_SettlementTransactionDetails_98E_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="SettlementInstructionProcessingNarrative" type="MT548_SequenceB_SettlementTransactionDetails_70E_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceB1_SettlementParties" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SETTRAN" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages">
  <xs:sequence>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="NumberIdentification_A" type="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type"/>
    <xs:element minOccurs="0" name="NumberIdentification_B" type="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="Reference_C" type="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type"/>
    <xs:element minOccurs="0" name="Reference_U" type="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="LINK" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason">
  <xs:sequence>
   <xs:element minOccurs="0" name="ReasonCode" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_24B_Type"/>
   <xs:element minOccurs="0" name="ReasonNarrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status_SubSequenceC1a1A2a1A_Reason_70D_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="REAS" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="Reference" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_20C_Type"/>
   <xs:element minOccurs="0" name="SubSequenceC1a1A2a_TransactionDetails" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="RELTRAN" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceA_GeneralInformation">
  <xs:sequence>
   <xs:element name="SendersMessageReference" type="MT548_SequenceA_GeneralInformation_20C_Type"/>
   <xs:element name="FunctionOfTheMessage" type="MT548_SequenceA_GeneralInformation_23G_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="PreparationDateTime_A" type="MT548_SequenceA_GeneralInformation_98A_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_C" type="MT548_SequenceA_GeneralInformation_98C_Type"/>
    <xs:element minOccurs="0" name="PreparationDateTime_E" type="MT548_SequenceA_GeneralInformation_98E_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" name="SubSequenceA1_Linkages" type="MT548_SequenceA_GeneralInformation_SubSequenceA1_Linkages"/>
   <xs:element maxOccurs="unbounded" name="SubSequenceA2_Status" type="MT548_SequenceA_GeneralInformation_SubSequenceA2_Status"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="True" name="isMandatory"/>
  <xs:attribute fixed="GENL" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Party_C" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95C_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_L" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_P" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_Q" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_R" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_95R_Type"/>
   </xs:choice>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="SafekeepingAccount_A" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97A_Type"/>
    <xs:element minOccurs="0" name="SafekeepingAccount_B" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_97B_Type"/>
   </xs:choice>
   <xs:element minOccurs="0" name="ProcessingReference" type="MT548_SequenceB_SettlementTransactionDetails_SubSequenceB1_SettlementParties_20C_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="SETPRTY" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails">
  <xs:sequence>
   <xs:element maxOccurs="unbounded" name="Reference" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_20C_Type"/>
   <xs:element name="PenaltyType" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_22F_Type"/>
   <xs:element minOccurs="0" name="AmountComputedFlag" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_17B_Type"/>
   <xs:element minOccurs="0" name="PenaltyStatus" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_25D_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="ReasonCode" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_24B_Type"/>
   <xs:element minOccurs="0" name="ReasonNarrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70D_Type"/>
   <xs:element name="AmountComputed" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_19A_Type"/>
   <xs:element name="CalculationMethod" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_22F_Type"/>
   <xs:element name="NumberDays" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_99A_Type"/>
   <xs:element name="SubSequenceC1a1A_CalculationDetails" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails"/>
   <xs:element minOccurs="0" name="Narrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="PENDET" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails">
  <xs:sequence>
   <xs:element name="TypeIndicator" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22F_Type"/>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="DateTime_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98A_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_B" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98B_Type"/>
    <xs:element maxOccurs="unbounded" name="DateTime_C" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98C_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97A_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_B" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97B_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Account_E" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_97E_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_Q" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95Q_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_95R_Type"/>
   </xs:choice>
   <xs:element maxOccurs="unbounded" name="Indicator" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_22H_Type"/>
   <xs:element maxOccurs="unbounded" name="QuantityOfFinancialInstrument" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_36B_Type"/>
   <xs:element minOccurs="0" name="PostingAmount" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_19A_Type"/>
   <xs:element maxOccurs="unbounded" name="DateTime" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_98C_Type"/>
   <xs:element maxOccurs="unbounded" minOccurs="0" name="SubSequenceC1a1A2a1_Status" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_SubSequenceC1a1A2a1_Status"/>
   <xs:element minOccurs="0" name="Narrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails_SubSequenceC1a1A_CalculationDetails_SubSequenceC1a1A2_RelatedTransaction_SubSequenceC1a1A2a_TransactionDetails_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="TRAN" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty">
  <xs:sequence>
   <xs:element minOccurs="0" name="CurrencyOfPenalties" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_11A_Type"/>
   <xs:choice minOccurs="0">
    <xs:element minOccurs="0" name="ComputationDateTime_A" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98A_Type"/>
    <xs:element minOccurs="0" name="ComputationDateTime_C" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_98C_Type"/>
   </xs:choice>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Party_L" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_P" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_Q" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_R" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_95R_Type"/>
   </xs:choice>
   <xs:element name="PartyCapacityIndicator" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_22F_Type"/>
   <xs:element minOccurs="0" name="SubSequenceC1a_PenaltiesPerCounterParty" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty"/>
   <xs:element minOccurs="0" name="Narrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="PENACUR" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceD_AdditionalInformation">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded" minOccurs="0">
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_C" type="MT548_SequenceD_AdditionalInformation_95C_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_L" type="MT548_SequenceD_AdditionalInformation_95L_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_P" type="MT548_SequenceD_AdditionalInformation_95P_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_Q" type="MT548_SequenceD_AdditionalInformation_95Q_Type"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="Party_R" type="MT548_SequenceD_AdditionalInformation_95R_Type"/>
   </xs:choice>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="ADDINFO" name="formatTag"/>
 </xs:complexType>
 <xs:complexType name="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty">
  <xs:sequence>
   <xs:choice maxOccurs="unbounded">
    <xs:element maxOccurs="unbounded" name="Party_L" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95L_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_P" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95P_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_Q" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95Q_Type"/>
    <xs:element maxOccurs="unbounded" name="Party_R" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_95R_Type"/>
   </xs:choice>
   <xs:element name="PartyCapacityIndicator" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_22F_Type"/>
   <xs:element name="BilateralNetAmount" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_19A_Type"/>
   <xs:element minOccurs="0" name="SubSequenceC1a1_PenaltyDetails" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_SubSequenceC1a1_PenaltyDetails"/>
   <xs:element minOccurs="0" name="Narrative" type="MT548_SequenceC_Penalties_SubSequenceC1_PenaltiesPerCurrencyForAParty_SubSequenceC1a_PenaltiesPerCounterParty_70E_Type"/>
  </xs:sequence>
  <xs:attribute fixed="16R" name="swiftTag"/>
  <xs:attribute default="False" name="isMandatory"/>
  <xs:attribute fixed="PENACOUNT" name="formatTag"/>
 </xs:complexType>
 <xs:element name="MT548">
  <xs:complexType>
   <xs:sequence>
    <xs:element name="SequenceA_GeneralInformation" type="MT548_SequenceA_GeneralInformation"/>
    <xs:element minOccurs="0" name="SequenceB_SettlementTransactionDetails" type="MT548_SequenceB_SettlementTransactionDetails"/>
    <xs:element minOccurs="0" name="SequenceC_Penalties" type="MT548_SequenceC_Penalties"/>
    <xs:element maxOccurs="unbounded" minOccurs="0" name="SequenceD_AdditionalInformation" type="MT548_SequenceD_AdditionalInformation"/>
   </xs:sequence>
  </xs:complexType>
 </xs:element>
</xs:schema>

