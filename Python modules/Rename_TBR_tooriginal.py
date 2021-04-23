import acm

#rename task names that start with TBR_ to its original name

rename_list =[
'TBR_AGGREGATION_OPT_SWAP_OTCF_VOID',
'TBR_AGGREGATION_OPT_SWAP_OTCT_CASH_POSTING',
'TBR_AGGREGATION_OPT_SWAP_OTCT_EXTERN_EXP',
'TBR_AGGREGATION_OPT_SWAP_OTCT_EXTERN_TERM',
'TBR_AGGREGATION_OPT_SWAP_OTCT_GRAVEYARD',
'TBR_AGGREGATION_OPT_SWAP_OTCT_INTERN_EXP',
'TBR_AGGREGATION_OPT_SWAP_OTCT_INTERN_TERM',
'TBR_AGGREGATION_OPT_SWAP_OTCT_SIM',
'TBR_AGGREGATION_OPT_SWAP_OTCT_VOID',
'TBR_AGGREGATION_SL_ARCHIVE',
'TBR_AGGREGATION_SL_DEARCHIVE',
'TBR_Aggregation_Stocks_CRUXHF_off-tree',
'TBR_Aggregation_Stocks_CRUXHF_on-tree',
'TBR_Aggregation_Stocks_MAP_109_off-tree',
'TBR_Aggregation_Stocks_MAP_109_on-tree',
'TBR_Aggregation_Stocks_MAP_111_off-tree',
'TBR_Aggregation_Stocks_MAP_111_on-tree',
'TBR_Aggregation_Stocks_PRESCIENT_alloc',
'TBR_Aggregation_Stocks_PRSTARBHF_off-tree',
'TBR_Aggregation_Stocks_PRSTARBHF_on-tree',
'TBR_Aggregation_Stocks_TOWER_alloc',
'TBR_Aggregation_Stocks_TOWNOVA_off-tree',
'TBR_Aggregation_Stocks_TOWNOVA_on-tree',
'TBR_Aggregation_Stocks_TOWNOVLS_off-tree',
'TBR_Aggregation_Stocks_TOWNOVLS_on-tree',
'TBR_Aggregation_Stocks_TOWNOVSBI_off-tree',
'TBR_Aggregation_Stocks_TOWNOVSBI_on-tree',
'TBR_Aggregation_Stocks_TOWNOVTEM_off-tree',
'TBR_Aggregation_Stocks_TOWNOVTEM_on-tree',
'TBR_AGGREGATION_SWAP_ARCHIVE',
'TBR_AGGREGATION_SWAP_DEARCHIVE'
]

for t in rename_list:

    task_name = acm.FAelTask[t]

    print('existing task name = ', task_name.Name())

    existing = task_name.Name()

    original = existing.replace('TBR_', "") #replace with double quotes
    try:
        task_name.Name(original)
        task_name.Commit()
        print('after removing TBR_ from existing name the new name is = ', task_name.Name())
    except:
        print('could not rename %s' % existing) 

    


