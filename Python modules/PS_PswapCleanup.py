"""
DEPARTMENT: Prime Services

HISTORY
Date       CR Number     Who                    Description
-------------------------------------------------------------------------------------------------------------
2019-04-12 CHG1001622197 Tibor Reiss            Initial implementation: archive legs with no more active trades
                                                (TPL and funding does not have to be moved)
2019-04-17 CHG1001639975 Tibor Reiss            Sweeping needs to run at least once after aggregation to cater
                                                for TPL movement of aggregated trades, thus don't remove legs
                                                which were updated couple of days ago
2019-05-28 CHG1001786026 Tibor Reiss            Moving functionality into new function for reusability
"""


import time

import acm
import ael
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_fund_shortname,
                          get_pb_fund_counterparty,
                          get_pb_fund_pswaps)
from PS_MoveFundingToCashPayment import archive_legs


LOGGER = getLogger(__name__)


def get_short_name_list(short_name_list):
    if not short_name_list:
        client_list = []
        for client in get_pb_fund_counterparties():
            short_name = get_pb_fund_shortname(client)
            client_list.append(short_name)
        return client_list
    else:
        return short_name_list


def get_trades(ins_name):
    query = acm.CreateFASQLQuery("FTrade", "AND")
    query.AddAttrNode("Instrument.Name", "EQUAL", ins_name)
    trades = query.Select()
    return trades


def get_trades_from_db(ins_name):
    sql = """SELECT COUNT(*)
             FROM trade t, instrument i
             WHERE 1 = 1
                   AND t.insaddr = i.insaddr
                   AND i.insid = '{ins_name}'
                   AND CAST(t.updat_time AS DATE) >= CAST(GETDATE() - 12 AS DATE)
          """
    result = ael.dbsql(sql.format(ins_name=ins_name))
    return result[0][0][0]


def pswap_to_process(pswap_name, name_list_to_process):
    for name_like in name_list_to_process:
        if name_like in pswap_name:
            return True
    return False


ael_variables = AelVariableHandler()
ael_variables.add("short_names",
                  label="Short names of funds",
                  cls="string",
                  mandatory=False,
                  multiple=True)
ael_variables.add("ins_types",
                  label="Instrument types",
                  cls="string",
                  mandatory=True,
                  multiple=True,
                  collection=acm.FEnumeration['enum(InsType)'].Values()
                  )
ael_variables.add("pswap_name_like",
                  label="Portfolio swap name contains",
                  cls="string",
                  mandatory=True,
                  multiple=True)


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    client_list = get_short_name_list(ael_dict["short_names"])
    for short_name in client_list:
        start = time.time()
        LOGGER.info("START client {}".format(short_name))
        client = get_pb_fund_counterparty(short_name)
        for pswap in get_pb_fund_pswaps(client):
            pswap_name = pswap.Name()
            if pswap_to_process(pswap_name, ael_dict["pswap_name_like"]):
                LOGGER.info("\tProcessing pswap {}...".format(pswap_name))
                legs = pswap.Legs()
                legs_to_archive = []
                for leg in legs:
                    leg_oid = leg.Oid()
                    indexref = leg.IndexRef()
                    indexref_name = indexref.Name()
                    if indexref.InsType() in ael_dict["ins_types"]:
                        trades = get_trades(indexref_name)
                        trades_from_db = get_trades_from_db(indexref_name)
                        if len(trades) == 0 and trades_from_db == 0:
                            legs_to_archive.append(leg_oid)
                            LOGGER.info("\t\tLeg {} {} marked for archiving".format(leg_oid, indexref_name))
                archive_legs(legs_to_archive)
                LOGGER.info("\tNumber of legs archived = {}".format(len(legs_to_archive)))
        end = time.time()
        LOGGER.info("TOTAL TIME for client {} = {}".format(short_name, end-start))

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully.")
