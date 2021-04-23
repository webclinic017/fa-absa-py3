'''
Created on 26 Feb 2014

@author: fabianpe
'''

# this is a config for moving positions to one strategy
from collections import namedtuple

MergingDesc = namedtuple('MergingDesc', ['merge_prf_name',
                                         'prfs_to_merge',
                                         ])

nit_tr_cfds = MergingDesc(merge_prf_name='60137_EqPairs_LT',
                        prfs_to_merge=['60137_CAMerger', '60137_Div_Arb', '60137_EqPairs_ST', '60137_EquityDriven', '60137_Illiq', '60137_L/SGen', '60137_LongOnly', '60137_MerArb', '60137_ShortOnly'],
                        )

nit_tr_fin_CE = MergingDesc(merge_prf_name='PB_CE_NIT_TR_LT_BK_ShortOnly_CR',
                          prfs_to_merge=['PB_CE_NIT_TR_LT_BK_ED_CR', 'PB_CE_NIT_TR_LT_BK_EqPairs_CR', 'PB_CE_NIT_TR_LT_BK_Illiq_CR', 'PB_CE_NIT_TR_LT_BK_LongOnly_CR', 'PB_CE_NIT_TR_ST_BK_CAMerger_CR', 'PB_CE_NIT_TR_ST_BK_Div_Arb_CR', 'PB_CE_NIT_TR_ST_BK_EqPairs_CR', 'PB_CE_NIT_TR_ST_BK_L/SGen_CR', 'PB_CE_NIT_TR_ST_BK_MerArb_CR']
                        )

nit_tr_ff_CE = MergingDesc(merge_prf_name='PB_CE_FF_NIT_TR_LT_BK_LongOnly_CR',
                         prfs_to_merge=['PB_CE_FF_NIT_TR_LT_BK_ED_CR', 'PB_CE_FF_NIT_TR_LT_BK_EqPairs_CR', 'PB_CE_FF_NIT_TR_LT_BK_Illiq_CR', 'PB_CE_FF_NIT_TR_LT_BK_ShortOnly_CR', 'PB_CE_FF_NIT_TR_ST_BK_CAMerger_CR', 'PB_CE_FF_NIT_TR_ST_BK_Div_Arb_CR', 'PB_CE_FF_NIT_TR_ST_BK_EqPairs_CR', 'PB_CE_FF_NIT_TR_ST_BK_L/SGen_CR', 'PB_CE_FF_NIT_TR_ST_BK_MerArb_CR']
                        )

nit_tr_safex = MergingDesc(merge_prf_name='PB_SAFEX_NIT_TR_CR',
                         prfs_to_merge=['PB_Safex_NIT_TR_LT_BK_ED_CR', 'PB_Safex_NIT_TR_LT_BK_EqPairs_CR', 'PB_Safex_NIT_TR_LT_BK_Illiq_CR', 'PB_Safex_NIT_TR_LT_BK_LongOnly_CR', 'PB_Safex_NIT_TR_LT_BK_ShortOnly_CR', 'PB_Safex_NIT_TR_ST_BK_CAMerger_CR', 'PB_Safex_NIT_TR_ST_BK_Div_Arb_CR', 'PB_Safex_NIT_TR_ST_BK_EqPairs_CR', 'PB_Safex_NIT_TR_ST_BK_L/SGen_CR', 'PB_Safex_NIT_TR_ST_BK_MerArb_CR']
                        )


m501_cfds = MergingDesc(merge_prf_name='60129_EqPairs_LT',
                        prfs_to_merge=['60129_Ca_Merger', '60129_Div_Arb', '60129_EqPairs_ST', '60129_EquityDriven', '60129_Illiq', '60129_L/SGen', '60129_LongOnly', '60129_MerArb', '60129_ShortOnly'],
                        )

m501_fin_CE = MergingDesc(merge_prf_name='PB_CE_M501_LT_BK_ShortOnly_CR',
                          prfs_to_merge=['PB_CE_M501_LT_BK_ED_CR', 'PB_CE_M501_LT_BK_EqPairs_CR', 'PB_CE_M501_LT_BK_Illiq_CR', 'PB_CE_M501_LT_BK_LongOnly_CR', 'PB_CE_M501_ST_BK_Ca_Merger_CR', 'PB_CE_M501_ST_BK_Div_Arb_CR', 'PB_CE_M501_ST_BK_EqPairs_CR', 'PB_CE_M501_ST_BK_L/SGen_CR', 'PB_CE_M501_ST_BK_MerArb_CR']
                        )

m501_ff_CE = MergingDesc(merge_prf_name='PB_CE_FF_M501_LT_BK_LongOnly_CR',
                         prfs_to_merge=['PB_CE_FF_M501_LT_BK_ED_CR', 'PB_CE_FF_M501_LT_BK_EqPairs_CR', 'PB_CE_FF_M501_LT_BK_Illiq_CR', 'PB_CE_FF_M501_LT_BK_ShortOnly_CR', 'PB_CE_FF_M501_ST_BK_Ca_Merger_CR', 'PB_CE_FF_M501_ST_BK_Div_Arb_CR', 'PB_CE_FF_M501_ST_BK_EqPairs_CR', 'PB_CE_FF_M501_ST_BK_L/SGen_CR', 'PB_CE_FF_M501_ST_BK_MerArb_CR']
                        )

m501_safex = MergingDesc(merge_prf_name='PB_SAFEX_M501_CR',
                         prfs_to_merge=['PB_Safex_M501_LT_BK_ED_CR', 'PB_Safex_M501_LT_BK_EqPairs_CR', 'PB_Safex_M501_LT_BK_Illiq_CR', 'PB_Safex_M501_LT_BK_LongOnly_CR', 'PB_Safex_M501_LT_BK_ShortOnly_CR', 'PB_Safex_M501_ST_BK_Ca_Merger_CR', 'PB_Safex_M501_ST_BK_Div_Arb_CR', 'PB_Safex_M501_ST_BK_EqPairs_CR', 'PB_Safex_M501_ST_BK_L/SGen_CR', 'PB_Safex_M501_ST_BK_MerArb_CR']
                        )
