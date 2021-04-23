try:
    import FSecurityLendingBorrowingOutSC
    FSecurityLendingBorrowingOutSC.create_custom_message_sc()
except:
    print('failed FSecurityLendingBorrowingOutSC.create_custom_message_sc()')

try:    
    import FSecuritySettlementInSC
    FSecuritySettlementInSC.create_security_settlment_conf_sc()
except:
    print('failed FSecuritySettlementInSC.create_security_settlment_conf_sc()')
    
try:
    import FSecuritySettlementOutSC
    FSecuritySettlementOutSC.create_sec_settlement_conf_out_sc()
except:
    print('failed FSecuritySettlementOutSC.create_sec_settlement_conf_out_sc()')

try:
    import FSecuritySettlementOutSC
    FSecuritySettlementOutSC.create_narrative_out_sc()
except:
    print('failed FSecuritySettlementOutSC.create_narrative_out_sc()')
    
try:
    import FPTSSettlementCancellationSC
    FPTSSettlementCancellationSC.create_custom_message_sc()
except:
    print('failed FPTSSettlementCancellationSC.create_custom_message_sc()')

try:
    import FCashOutSC
    FCashOutSC.create_cash_settlement_conf_out_sc()
except:
    print('failed FCashOutSC.create_cash_settlement_conf_out_sc()')

try:
    import FFXMMConfirmationInSC
    FFXMMConfirmationInSC.create_fx_trade_conf_sc()
except:
    print('failed FFXMMConfirmationInSC.create_fx_trade_conf_sc()')
    
try:
    import FFXMMConfirmationOutSC
    FFXMMConfirmationOutSC.create_fxMM_conf_out_sc()
except:
    print('failed FFXMMConfirmationInSC.create_fxMM_conf_out_sc()')
