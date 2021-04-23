import acm

'''

rename old mtm tasks

coded by Anil Parbhoo

13 Jan 2014

'''

task_list =['291559 Warrants',
'291559_Warrants',
'ALL Asians',
'ALL Warrants',
'ALL Warrants MTM',
'ALLEQIndexDerivatives',
'ALL_ALSI',
'ALL_Asians',
'ALL_RUT',
'ALL_RateIndex',
'ALL_Warrants_MTM',
'AOPT All',
'AOPT_All',
'Agri_Forward_9196',
'Agri_Options_9196',
'All Asians',
'Base_Metals',
'BondOpts',
'CurrSwap',
'DTOP',
'EQ MTM ONLY',
'EQIndex',
'EQ_FWD_STRUCTURES',
'EQ_Fwd_Structures_FF',
'EQ_MTM_TEST',
'EQ_MTM_TEST_PORTFOLIOS',
'EQ_OFP',
'EQ_Structures',
'EQ_Structures_SSO',
'FXBarriers_BVOE',
'FXOptions',
'Forwards_on_Stocks',
'IRGs',
'JMPF10 MTM',
'Metals MTM Day trades',
'NEW_EquityIndex',
'NEW_EquityOptions_Curr',
'NEW_EquityOptions_EquityIndex',
'NEW_EquityOptions_Stock',
'NEW_Equity_TEST',
'NEW_Test',
'New_CFE_Africa',
'Opt_FutForw',
'Quanto Trade',
'Quanto_Trade',
'SSFO_All',
'SSFT_All',
'SWIX_MTM_AT3',
'SWIX_MTM_AT3_SERVER',
'SwapsFras',
'Swaptions',
'TEST',
'Trade_1013820',
'Trade_270366',
'UPGRADE_CSWAP',
'UP_CDS',
'UP_CDS_FRI',
'UP_CDS_ME',
'UP_CDS_SAT',
'UP_CDS_THU',
'UP_CDS_YE',
'UP_CURRSWAPS',
'UP_CURRSWAPS_FRI',
'UP_CURRSWAPS_ME',
'UP_CURRSWAPS_SAT',
'UP_CURRSWAPS_THU',
'UP_CURRSWAPS_YE',
'UP_DEPOS',
'UP_DEPOS_FRI',
'UP_DEPOS_ME',
'UP_DEPOS_SAT',
'UP_DEPOS_THU',
'UP_DEPOS_YE',
'UP_FRNS',
'UP_FRNS_FRI',
'UP_FRNS_ME',
'UP_FRNS_SAT',
'UP_FRNS_THU',
'UP_FRNS_YE',
'UP_ILS',
'UP_ILS_FRI',
'UP_ILS_ME',
'UP_ILS_SAT',
'UP_ILS_THU',
'UP_ILS_YE',
'UP_SWAPS',
'UP_SWAPS_FRI',
'UP_SWAPS_ME',
'UP_SWAPS_SAT',
'UP_SWAPS_THU',
'UP_SWAPS_YE',
'UsdCbt',
'VarSwaps',
'VolCalc_Equity_SERVER',
'ss_test',
'Caps_floor_create_new_ins_trades_adjust_nominals_SERVER']

for t in task_list:

    task = acm.FAelTask[t]
    
    print('before', task.Name())
    
    try:
        new_name = 'TBR_'+ task.Name()
        task.Name(new_name)
        task.Commit()
        print('after', task.Name())
    except:
        print('% task could not be renamed' % t)
    


