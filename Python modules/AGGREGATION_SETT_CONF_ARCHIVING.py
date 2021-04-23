"""
Date                    : 2019/05/09
Purpose                 : Archive settlements, confirmations and it's additional infos. 
                          Log the diary oid that is linked to the settlement/confirmation.
Department and Desk     : IT - Data Maintenance
Requester               : Gerhard Engelbrecht/Ridwaan Arbee
Developer               : Bhavnisha Sarawan

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
"""


from time import time

import acm
import ael

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_type_helpers import xrepr


LOGGER = getLogger()
AGGREGATION_USRNBR = acm.FUser['AGGREGATION'].Oid()

SQL_ARCHIVE_ADDINFOS = """
    UPDATE additional_info
    SET updat_usrnbr = {usrnbr}
        , updat_time = GETDATE()
        , archive_status = {archive_status}
    WHERE valnbr = {valnbr}
    """

SQL_ARCHIVE_SETTLEMENT = """
    UPDATE settlement
    SET updat_usrnbr = {usrnbr}
        , updat_time = GETDATE()
        , archive_status = {archive_status}
    WHERE seqnbr = {seqnbr}
    """

SQL_ARCHIVE_CONFIRMATION = """
    UPDATE confirmation
    SET updat_usrnbr = {usrnbr}
        , updat_time = GETDATE()
        , archive_status = {archive_status}
    WHERE seqnbr = {seqnbr}
    """


def CreateSettlementQuery():

    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('ValueDay', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('Trade.Instrument.Name', 'EQUAL', None)
    op4 = query.AddOpNode('OR')
    op4.AddAttrNode('Trade.Portfolio.Name', 'EQUAL', None)
    op5 = query.AddOpNode('OR')
    op5.AddAttrNode('Trade.Instrument.OpenEnd', 'EQUAL', None)
    op6 = query.AddOpNode('OR')
    op6.AddAttrNode('Trade.Instrument.InsType', 'EQUAL', None)
    
    return query

def CreateConfirmationQuery():

    query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('CreateTime', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('Trade.Instrument.Name', 'EQUAL', None)
    op4 = query.AddOpNode('OR')
    op4.AddAttrNode('Trade.Portfolio.Name', 'EQUAL', None)
    op5 = query.AddOpNode('OR')
    op5.AddAttrNode('Trade.Instrument.OpenEnd', 'EQUAL', None)
    op6 = query.AddOpNode('OR')
    op6.AddAttrNode('Trade.Instrument.InsType', 'EQUAL', None)
    
    return query

def set_archive_status(items, archive_sql, archive_status):
    items_count = len(items)
    addinfo_count = 0
    for item in items:
        try:
            for addinfo in item.AddInfos():
                sql = SQL_ARCHIVE_ADDINFOS.format(
                    valnbr=addinfo.Oid(),
                    usrnbr=AGGREGATION_USRNBR,
                    archive_status=archive_status)
                ael.dbsql(sql)
                addinfo_count += 1

            if item.Diary():
                # textobjects cannot be archived and will be orphaned. To Be Deleted via trade rollout.
                # A Diary can have a another diary linked to it via next_seqnbr
                LOGGER.info('{} : diary = {}'.format(xrepr(item), item.Diary().Oid()))

            sql = archive_sql.format(
                seqnbr=item.Oid(),
                usrnbr=AGGREGATION_USRNBR,
                archive_status=archive_status)
            ael.dbsql(sql)
        except Exception as err:
            LOGGER.error(
                'Could not update archive status for {}. '
                'Error: {}.'.format(xrepr(item), err))
    return items_count, addinfo_count

def change_archive_settlements_addinfo(settlements, archive_status):
    LOGGER.info(
    'Setting archive status to {} for settlements '
    'and related additional infos'.format(archive_status))
    start = time()
    
    sett_count, addinfo_count = set_archive_status(
        settlements, SQL_ARCHIVE_SETTLEMENT, archive_status)
        
    end = time()
    LOGGER.info('Time taken: {}'.format(end - start))
    LOGGER.info('Total settlement(s):{}'.format(sett_count))
    LOGGER.info('Total settlement additional info(s):{}'.format(addinfo_count))

def change_archive_confirmations_addinfo(confirmations, archive_status):
    LOGGER.info(
        'Setting archive status to {} for confirmations '
        'and related additional infos'.format(archive_status))
    start = time()

    conf_count, addinfo_count = set_archive_status(
        confirmations, SQL_ARCHIVE_CONFIRMATION, archive_status)

    end = time()
    LOGGER.info('Time taken: {}'.format(end - start))
    LOGGER.info('Total confirmation(s): {}'.format(conf_count))
    LOGGER.info('Total confirmation additional info(s): {}'.format(addinfo_count))
    

ael_variables = AelVariableHandler()
ael_variables.add(
    'settlements',
    label='Settlements',
    cls='FSettlement',
    default=CreateSettlementQuery(),
    mandatory=False,
    alt ='If unarchiving, ensure logged in as Archived mode.',
    multiple=True
)
ael_variables.add(
    'confirmations',
    label='Confirmations',
    cls='FConfirmation',
    default=CreateConfirmationQuery(),
    mandatory=False,
    alt ='If unarchiving, ensure logged in as Archived mode.',
    multiple=True
)
ael_variables.add_bool(
    'unarchive',
    label='Unarchive'
)

def ael_main(parameter):
    settlements = parameter['settlements']
    confirmations = parameter['confirmations']
    unarchive = parameter['unarchive']
    archive_status = 1
    if unarchive:
        archive_status = 0
        
    if settlements:
        change_archive_settlements_addinfo(settlements, archive_status)
    if confirmations:
        change_archive_confirmations_addinfo(confirmations, archive_status)
    
    LOGGER.info('Completed successfully.')
