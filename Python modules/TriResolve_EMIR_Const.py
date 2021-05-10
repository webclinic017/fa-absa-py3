# coding=ascii
"""
Brendan Bosman      MINT-164.3      2015/09/01      Created as part of a refactoring process of TriResolve_EMIR.py
Brendan Bosman      MINT-366        2015/0915       Implement Non EU files

Main Purpose:
1. Constant declarations used in the TriResolve EMIR Process
2. Named Tuple declarations used in the TriResolve EMIR Process


To the developers working on this file:
1. This file was taken rom FA where tabsstop was equal to 8 spaces. In FA, most of the indention was 4 space, so
   reading the outside of FA was difficult if tabstop was not 8 spaces. Please be aware of this
2. Going forward, all indentions are 4 spaces, but tabstop is still 8
"""

from collections import namedtuple

# Input params constants. This will help to mimimize faults
const_fxf_filtered_clients_path = 'fxf_filtered_clients_path'
const_output_path = 'output_path'
const_issue_output_path = 'issue_output_path'
const_config_path = 'config_path'
const_le_sds_ids_path = 'le_sds_ids_path'
const_cp_sds_ids_path = 'cp_sds_ids_path'
const_le_sds_non_coll_ids_path = 'NON_EU_CP_path'
const_midas_map_path = 'midas_map_path'
const_midas_extract_path = 'midas_extract_path'
const_is_front_arena_data_run = 'is_front_arena_data_run'

const_inc_fa_trades = 'inc_fa_trades'
const_exc_fa_trades = 'exc_fa_trades'
const_inc_midas_trades = 'inc_midas_trades'
const_exc_midas_trades = 'exc_midas_trades'
const_exc_fa_acquirers = 'exc_fa_acquirers'
const_coll_fa_trades = 'coll_fa_trades'
const_noncoll_fa_trades = 'noncoll_fa_trades'
const_coll_midas_trades = 'coll_midas_trades'
const_noncoll_midas_trades = 'noncoll_midas_trades'
const_noncoll_nonotc_pf = 'noncoll_nonotc_pf'
const_exclude_instypes = 'exclude_instypes'
const_non_coll_instypes = 'non_coll_instypes'
const_midas_moved_pf = 'midas_moved_pf'
const_midas_stl_pf = 'midas_stl_pf'

CONST_WRITE_TO_LOG_FILE = "WRITE_TO_LOG_FILE"

const_use_trade_filter = 'use_trade_filter'

# Additional (non Tri-Optima standardized) columns
XCOL_OPTIONAL_KEY = 'OPTIONAL_KEY'
XCOL_COLLATERALIZED = 'COLLATERALIZED'
XCOL_OTC = 'OTC'
XCOL_INSTYPE = 'INSTYPE'

# Column values for (non)collateralized trades.
COLLATERALIZED = 'Coll'
NON_COLLATERALIZED = 'Non-coll'

# Trade filtering
FLT_ENABLE = True
FLT_DISABLE = False

# MDK Counter party Name (trades pumped from Midas using CFR)
MDK_CPTY_NAME = 'MIDAS DUAL KEY'

# Regex used to parse Midas ID from OptionalKey or Source Trade Id addinfo
# Modified to include only main trade (not shadow trades)
MIDAS_ID_REGEX = '^\\d+_(\\d+)_0$'

# Contains multi-directional mapping for parties among different systems.
MappingItem = namedtuple('MappingItem', ['front_id', 'le_name', 'le_sdsid', 'cp_sdsid', 'midas_id'])


# Retrieves all live trades for specified counter party oid
# Combination added as ASQL returns 01/01/0000 for combination's expiry dates
CPTY_TRADES_QUERY = """
SELECT t.trdnbr
FROM Trade t, Instrument i
WHERE
t.insaddr = i.insaddr
AND t.counterparty_ptynbr={1}
AND t.status NOT IN ('Void', 'Simulated', 'Terminated')
AND t.time < '{0}'
AND (
    (t.value_day >= '{0}' AND t.value_day < '3000-01-01')
    OR (i.exp_day >= '{0}' AND i.exp_day < '3000-01-01')
    OR i.instype = 'Combination')"""


# Will exclude trades with abs(mtm) < threshold
MTM_THRESHOLD = 0.005
