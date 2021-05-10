"""-----------------------------------------------------------------------------
MODULE
    pcg_option_uploader

DESCRIPTION
    Date                : 2017-06-22
    Purpose             : Book simulated trades for monthly options.
    Department and Desk : PCG Valuations
    Requester           : Ryan Fagri (ryan.fagri@barclays.com)
    Developer           : Ondrej Bahounek
    CR Number           : 4673690
ENDDESCRIPTION

HISTORY
=============================================================================================
Date       Change no    Developer          Description
---------------------------------------------------------------------------------------------
2017-06-22 4673690      Ondrej Bahounek    Initial implementation
2017-07-11 4725287      Ondrej Bahounek    Create also instruments
------------------------------------------------------------------------------------------"""

from datetime import datetime
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PS_Functions import modify_asql_query


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
FIRST_DAY_STR = "FirstDayOfMonth"
FIRST_DAY = acm.Time.FirstDayOfMonth(acm.Time.DateToday())

ael_variables = AelVariableHandler()
ael_variables.add('query_folder',
    label='Query folder',
    cls='FStoredASQLQuery',
    default="PCG_OPTION_UPLOADER_QUERY",
    multiple=False,
    alt=("Instruments that will be used for booking"))
ael_variables.add('start_date',
    label='Start Date',
    cls='string',
    collection=[FIRST_DAY, FIRST_DAY_STR],
    default=FIRST_DAY,
    alt=("All instrument created from this date will be selected. "
         "Format: YYYY-MM-DD"))


def get_instrs(query_folder, start_date):
    query = query_folder.Query()
    new_q = modify_asql_query(query, 'CreateTime', False, 
        new_value=start_date, new_operator=5)
    return new_q.Select()


def save_addinfos(orig_instr, new_instr):
    new_oid = new_instr.Oid()
    orig_oid = orig_instr.Oid()
    ais = acm.FAdditionalInfo.Select('recaddr=%d' % orig_oid)
    for ai in ais:
        addinfo_spec = ai.AddInf()
        if addinfo_spec.RecType() == 'Instrument':
            ai_clone = ai.Clone()
            ai_clone.Recaddr(new_oid)
            ai_clone.Commit()


def create_instrument(instrument):
    new_name = instrument.Name() + "/TOTEM"
    if new_name.startswith("ZAR/FUT/"):
        new_name = new_name.replace("ZAR/FUT/", "ZAR/EQ/")
    
    instr = acm.FInstrument[new_name]
    if instr:
        LOGGER.warning("Instrument '%s' already exists", new_name)
        return instr
    
    # create same instrument with a different name
    instr = instrument.Clone()
    instr.Name(new_name)
    instr.Commit()
    
    save_addinfos(instrument, instr)
    
    return instr


def create_trade(instr):
    t = acm.FTrade()
    t.Instrument(instr)
    t.Currency(instr.Currency())
    t.Status('Simulated')
    
    spot_days = instr.SpotBankingDaysOffset()
    cal = instr.Currency().Calendar()
    val_date = cal.AdjustBankingDays(TODAY, spot_days)
    t.TradeTime(TODAY)
    t.ValueDay(val_date)
    t.AcquireDay(val_date)
    t.Commit()
    return t


def ael_main(ael_dict):
    query_folder = ael_dict['query_folder']
    start_date = ael_dict['start_date']
    if ael_dict['start_date'] == FIRST_DAY_STR:
        start_date = FIRST_DAY
    else:
        start_date = datetime.strptime(ael_dict['start_date'], '%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')

    LOGGER.info("Instruments info:")
    LOGGER.info("\t Create time greater than: '%s'", start_date)
    LOGGER.info("Searching for instruments...")
    
    instruments = get_instrs(query_folder, start_date)
    LOGGER.info("Instruments found: %d", len(instruments))
    
    for i, instr in enumerate(instruments, 1):
        LOGGER.info("%d) %s", i, instr.Name())
        new_instr = create_instrument(instr)
        trd = create_trade(new_instr)
        LOGGER.info("\t%s: %d", new_instr.Name(), trd.Oid())
        
    LOGGER.info("Completed successfully.")
