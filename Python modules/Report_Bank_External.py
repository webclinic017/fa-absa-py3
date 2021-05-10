"""
-------------------------------------------------------------------------------
MODULE
    Report_Bank_External

DESCRIPTION
    Date                : 2018-03-09
    Purpose             : This module generates a CSV report based on the
                          specifications from M. Wortmann
    Requester           : Martin Wortmann
    Developer           : Tibor Reiss
    ABITFA              : 5305

HISTORY
===============================================================================
2018-03-09    Tibor Reiss    ABITFA-5305: initial implementation
-------------------------------------------------------------------------------
"""

import acm
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from datetime import datetime
from os import path

LOGGER = getLogger(__name__)

class WriteCSV(CSVReportCreator):
    def __init__(self, data, file_name, file_suffix, path):
        super(WriteCSV, self).__init__(file_name, file_suffix, path)
        self.content = data
    def _collect_data(self):
        pass
    def _header(self):
        return ["Trdnbr", "Insaddr", "UndInsaddr", "Insid", "InsType"
                , "ExpDay", "ValueDay", "Acquirer", "Trader"
                , "ExecutionTime", "Nominal", "Portfolio", "Counterparty"
                , "CounterpartyType", "TradeStatus", "TradeType"
                , "TrxTrdnbr", "Isin", "UndIsin", "RespPerson"
                , "RespArea", "FundingInstype", "MMInstype"
                , "Approx. load", "MidasSettleEnabled"
                , "InsOverride", "DematIns", "DISIns"]

def is_owner_pf(pf, owner_name):
    #top level portfolios - no parent
    if not pf:
        return False
    
    if isinstance(pf, str):
        pf_name = pf
    else:
        pf_name = pf.Name()
        
    if pf_name == owner_name:
        return True    
    
    acm_pf = acm.FPhysicalPortfolio[pf_name]
    for ml in acm_pf.MemberLinks():
        return is_owner_pf(ml.OwnerPortfolio(), owner_name)
    #If no pf-link
    return False
    
ael_variables = AelVariableHandler()
ael_variables.add('owner',
                  label='Parent portfolio',
                  alt='Compound portfolio whose trades should be queried',
                  cls='string',
                  default='ABSA BANK LTD')
ael_variables.add('path',
                  label='Output path',
                  alt='Location for output',
                  default='/services/frontnt/Task/')

def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    
    #Query all portfolios in the database
    all_pf = acm.FPhysicalPortfolio.Select('compound = 0')
    
    #Only keep portfolios under 'owner'
    LOGGER.info("Selecting trades under portfolio {}".format(ael_params['owner']))
    valid_pf = []
    for pf in all_pf:
        prfid = pf.Name()
        if is_owner_pf(prfid, ael_params['owner']):
            valid_pf.append(pf)
    
    query_trades = acm.FStoredASQLQuery["Trade_Buckets"].Query().Clone()
    query_trades.AddAttrNodeString("Portfolio.Name", [pf.Name() for pf in valid_pf], "EQUAL")
    res = query_trades.Select()
    LOGGER.info("Number of trades selected: {}".format(len(res)))
    
    #Container for trades to be reported
    all_trades = []
    
    exceptions = False
    for trade in res:
        try:
            pf_name = trade.Portfolio().Name()
            instr = trade.Instrument()
            instr_isin = instr.Isin()
            ins_type = instr.InsType()
            is_demat = instr.add_info("Demat_Instrument")
            is_dis = instr.add_info("DIS_Instrument")
            ins_override = trade.add_info("InsOverride")
            if not instr.Underlying():
                und_instr_isin = ''
                und_instr_oid = ''
            else:
                und_instr_isin = instr.Underlying().Isin()
                und_instr_oid = instr.Underlying().Oid()
            if not trade.TrxTrade():
                trx_trade_oid = ''
            else:
                trx_trade_oid = trade.TrxTrade().Oid()
            #Additional conditions
            if (instr_isin.startswith('ZAG') or und_instr_isin.startswith('ZAG')) \
                    and (not trx_trade_oid or not ins_override):
                pass
            elif is_demat == "Yes":
                pass
            elif is_dis == "Yes":
                pass
            elif ins_type == 'Curr' \
                    and trade.Portfolio().add_info("MidasSettleEnabled") == "Yes":
                pass
            elif is_owner_pf(pf_name, "GROUP TREASURY"):
                pass
            elif is_owner_pf(pf_name, "AFRICA TRADING") \
                 and ins_type not in ['CurrSwap', 'FRA', 'Option', 'Swap']:
                pass
            elif is_owner_pf(pf_name, "PRIME SERVICES TRADING") \
                 and ins_type not in ['FRA', 'Option', 'Swap', 'TotalReturnSwap']:
                pass
            elif is_owner_pf(pf_name, "MONEY MARKET TRADING") \
                 and ins_type not in ['FRA', 'Option', 'Swap', 'TotalReturnSwap']:
                pass
            elif is_owner_pf(pf_name, "MONEY MARKET BANKING") \
                 and ins_type not in ['FRA', 'Option', 'Swap', 'TotalReturnSwap']:
                pass
            else:
                all_trades.append( [ trade.Oid()
                                     , instr.Oid()
                                     , und_instr_oid
                                     , instr.Name()
                                     , ins_type
                                     , instr.ExpiryDate()
                                     , trade.ValueDay()
                                     , trade.Acquirer().Name()
                                     , trade.Trader().Name()
                                     , trade.ExecutionTime()
                                     , trade.Nominal()
                                     , pf_name
                                     , trade.Counterparty().Name()
                                     , trade.Counterparty().Type()
                                     , trade.Status()
                                     , trade.Type()
                                     , trx_trade_oid
                                     , instr_isin
                                     , und_instr_isin
                                     , trade.add_info("Responsible Person")
                                     , trade.add_info("Responsible Area")
                                     , trade.add_info("Funding Instype")
                                     , trade.add_info("MM_Instype")
                                     , trade.add_info("Approx. load")
                                     , trade.Portfolio().add_info("MidasSettleEnabled")
                                     , ins_override
                                     , is_demat
                                     , is_dis ] )
        except Exception as e:
            exceptions = True
            LOGGER.exception("""Exception occurred while processing 
                                trade {}: {}""".format(trade.Oid(), str(e)))
    report_name = "FAExtract_" + \
                  datetime.now().strftime("%Y%m%d_%H%M%S")
    report = WriteCSV(all_trades, report_name, "csv", ael_params['path'])
    report.create_report()
    LOGGER.output(path.join(ael_params['path'], report_name + ".csv"))
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")    
    LOGGER.info("Report generated successfully")
