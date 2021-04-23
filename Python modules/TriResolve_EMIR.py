# coding=ascii
"""
Creates TriResolve extract by joining trades in FA with trades in Midas file.

Source: //depot/AbsaCapital/SMIT/Other/paluzgal/EMIR
Documentation: http://confluence.barcapint.com/display/AbCapFxIT/FX+Try+Resolve+process

Date            CR Number   Developer               Description
2014-07-17      XXXXXX      Heinrich Cronje         Added the Front Arena run logic in to
                                                        split the Front Arena data run from the
                                                        Midas data run.
2014-08-07                  Sanele Macanda          Changed the name "error" to "fault", this was causing issues on
                                                        the backEnd.
2015-03-23      XXXXXX      Heinrich Cronje         updated cf_nominal to calculate the cash flow nominal via the
                                                        money flow and
                                                        not directly via the cash flow.
2015-06-17      MINT-164    Paseka Motsoeneng       Allow Barrier Crossed Options, Exclude equal but economically
                                                        opposite trades and include FX Spot trades.
2015-08-31      MINT-164.3  Brendan Bosman          1. Indention issues
                                                     2. Some PEP-8 fixes
2015-09-01      MINT-164.3  Brendan Bosman          1. Refactoring the Triresolve_EMIR file. Split this file into
                                                        multple files. This file is the main entry point for FA, so
                                                        all the FA specific entry points variables will stay here.
                                                     2. This File the main entry point from PyCharm/VS integration
                                                     3. There are test cases associated with this file that needs to
                                                        be respected
2015-09-03      MINT-164.3  Brendan Bosman          1. More refatoring, and making sure the run can be reach by context
                                                        information, so test cases can be written

2015/09/15      MINT-366    Brendan Bosman          Implement Non EU files

To the developers working on this file:
1. This file was taken rom FA where tabsstop was equal to 8 spaces. In FA, most of the indention was 4 space, so
   reading the outside of FA was difficult if tabstop was not 8 spaces. Please be aware of this
2. Going forward, all indentions are 4 spaces, but tabstop is still 8
"""

from datetime import datetime
import TriResolve_EMIR_Const
import at
import TriResolve_EMIR_Report
import TriResolve_EMIR_Context

ael_variables = at.ael_variables.AelVariableHandler()
# Output files
ael_variables.add(TriResolve_EMIR_Const.const_output_path, mandatory=1, label='Output path',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\Output\EMIR.xls')
ael_variables.add(TriResolve_EMIR_Const.const_issue_output_path, mandatory=1, label='Issues output path',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\Output\TriResolve_EMIR_Issues.txt')

# Configuration files
ael_variables.add(TriResolve_EMIR_Const.const_config_path, mandatory=1, label='Configuration File Path',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\TriResolve_EMIR.js')

# Legal Entities collatoral
ael_variables.add(TriResolve_EMIR_Const.const_le_sds_ids_path, mandatory=1, label='Legal Entity SDS IDs',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\LE_SDS_Collateral.csv')

# EU non collatoral parties
ael_variables.add(TriResolve_EMIR_Const.const_cp_sds_ids_path, mandatory=1, label='EU Counterparty SDS IDs',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\TriResolveMidbaseEU_CP_SDS.txt')

# Legal Entities NON collatoral
ael_variables.add(TriResolve_EMIR_Const.const_le_sds_non_coll_ids_path, mandatory=1, label='NON EU Counterparty',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\NON_EU_CounterParties.csv')

# Mappings
ael_variables.add(TriResolve_EMIR_Const.const_midas_map_path, mandatory=1, label='Midas/Midbase/FA Mapping',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\TriResolveMidbaseMidasFA_CP_Mapping.txt')

# Midas Trades
ael_variables.add(TriResolve_EMIR_Const.const_midas_extract_path, mandatory=1, label='Midas Trades',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\TriResolve_Midas_Live_Trades.txt')

# 4Front Exclusion List
ael_variables.add(TriResolve_EMIR_Const.const_fxf_filtered_clients_path, mandatory=1, label='4Front Exclusion List',
                  default=r'Y:\Jhb\FALanding\Dev\TriResolve\20150908\ForeFrontRoutedData.xml')

# Front area trades
ael_variables.add_bool('is_front_arena_data_run', mandatory=1, label='Front Arena Data Run', default=1)

def ael_main(params):
    """Main entry point for FA


    :param params: Dictionary
    """

    params[TriResolve_EMIR_Const.const_use_trade_filter] = True
    ctx = TriResolve_EMIR_Context.EMIRContext(params, True)
    
    main_run(ctx)


def main(params):
    """



    :param params:
    """
    ctx = TriResolve_EMIR_Context.EMIRContext(params, False)
    main_run(ctx)


def main_run(ctx):
    """ Entry point for the main run

    From here FA can enter as well as test cases

    :param ctx:BaseEMIRContext
    """

    em = TriResolve_EMIR_Report.EmirReportGenerator(ctx)
    start = datetime.now()
    em.run()
    elapsed = datetime.now() - start
    print("Output written to", ctx.get_params()[TriResolve_EMIR_Const.const_output_path])
    print("Issues Output written to", ctx.get_params()['issue_output_path'])
    print("Completed in", elapsed)
    print("Done")
