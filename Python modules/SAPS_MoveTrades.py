'''
Date                    : 2011-05-25
Purpose                 : Script to move trades on a future to a corresponding
                          future (mtm priced) (creates the future instrument
                          if it doesn't exist)
Department and Desk     : Prime Service
Requester               : Francois Henrion
Developer               : Rohan van der Walt
CR Number               : 667407

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2011-05-25      667407          Rohan van der Walt      Initial Development
2011-06-08      680200          Paul Jacot-Guillarmod   Generalised script to work for Options as well as Futures
2011-07-01      699989          Herman Hoon             Amended to look for instruments with the /MTM postfix instead of the MTMFromFeed flag.
2011-07-12      710203          Herman Hoon             Cleared the unique fields on the new instrument.
2014-07-17      2126420         Libor Svoboda           Added ETF instype.
2014-11-20      2450799         Ondrej Bahounek         Report errors/exceptions correctly.
                                                        Include all Production names from environment.
2015-09-11      3090331         Jakub Tomaga            Portfolio independent sweeping
2016-05-05      3635471         Jakub Tomaga            Email info about missing price links.
2016-06-20      3743397         Jakub Tomaga            Env name simplified, email only for ETFs, caching removed.
2016-09-27      3977095         Libor Svoboda           Added specific logic for agri derivatives.
'''
import sys
from collections import defaultdict

import acm
from at_ael_variables import AelVariableHandler
from at_email import EmailHelper
import at_choice

from at_logging import  getLogger, bp_start
LOGGER = getLogger()

CUSTOM_AGRIS_MODEL = 'theorAgrisTheoreticalPrice'


class MoveTradeException(Exception):
    """Custom exception for errors."""
    pass


ael_variables = AelVariableHandler()
ael_variables.add_bool("send",
                       label="Send Mails",
                       default=False,
                       alt="Should instrument creation emails be sent")
ael_variables.add("emails",
                  label="Emails",
                  default="AbCapEQDMO@barclayscapital.com",
                  multiple=True,
                  alt="Email destinations. Use comma seperated email addresses \
                       if you want to send report to multiple users.")
ael_variables.add("query_folder",
                  label="Query Folder",
                  cls=acm.FStoredASQLQuery,
                  collection=acm.FStoredASQLQuery.Select(
                      "subType='FTrade'"))


def getCurrentEnvironment():
    """Return current env instance name."""
    return acm.FDhDatabase['ADM'].InstanceName()


def moveTrade(trade, newIns):
    """Move trade ot new MtM instrument."""
    trade.Instrument(newIns)
    trade.Commit()


def getPriceFindingGroupItem(choiceName):
    """Get given choice from price finding choice list."""
    value = at_choice.get("PriceFindingGroup", choiceName)
    if value:
        return value
    else:
        err_msg = "ERROR: ChoiceList '{0}' not found."
        MoveTradesException(err_msg.format(choiceName))


def getMTMInstrument(theorInstrument):
    """Return MTM instrument for given theoretical one. Create if needed."""
    is_new = False
    mtmInstrument = acm.FInstrument['%s/MTM' % theorInstrument.Name()]
    isinMtmInstrument = acm.FInstrument.Select('isin=%s_MTM' % theorInstrument.Isin())
    if isinMtmInstrument:
        return (isinMtmInstrument, is_new)
    elif not mtmInstrument:
        LOGGER.info('\tMTM priced instrument not found, creating %s/MTM' % theorInstrument.Name())
        mtmInstrument = theorInstrument.Clone()
        mtmInstrument.Name('%s/MTM' % theorInstrument.Name())
        mtmInstrument.MtmFromFeed(1)
        mtmInstrument.PriceFindingChlItem(getPriceFindingGroupItem('EQ_Deriv'))
        if theorInstrument.Isin():
            mtmInstrument.Isin('%s_MTM' % theorInstrument.Isin())
        else:
            mtmInstrument.Isin('')
        mtmInstrument.ExternalId1('')
        mtmInstrument.ExternalId2('')
        valuation_extension = theorInstrument.MappedValuationExtensionLink().Link()
        if valuation_extension == CUSTOM_AGRIS_MODEL:
            # Copy also add infos that are required by the valuation model.
            mtmInstrument.RegisterInStorage()
            cbot_ref = theorInstrument.AdditionalInfo().CBOT_Reference()
            comm_type = theorInstrument.AdditionalInfo().Commodity_Type()
            comm_unit = theorInstrument.AdditionalInfo().Commodity_Unit()
            mtmInstrument.AdditionalInfo().CBOT_Reference(cbot_ref)
            mtmInstrument.AdditionalInfo().Commodity_Type(comm_type)
            mtmInstrument.AdditionalInfo().Commodity_Unit(comm_unit)

        try:
            mtmInstrument.Commit()
        except Exception:
            msg = 'ERROR: MTM instrument {0} could not be found and created' \
                'for instrument {1}: {2}'.format(mtmInstrument.Name(),
                                                 theorInstrument.Name(),
                                                 sys.exc_info())
            raise MoveTradeException(msg)
        LOGGER.info(' - Instrument Created')
        is_new = True
    return (mtmInstrument, is_new)


def send_email(send_to, ins_list):
    """Send e-mail to TCU about currently created instruments."""
    env = getCurrentEnvironment()
    subject = "SAPS_MoveTrades: New instruments ({0})".format(env)
    body = "Hi TCU,<BR><BR>" \
            "The following instruments were created in {0}:<BR>".format(env)
    for ins in ins_list:
        body = body + "<BR>" + ins
    body = body + "<BR><BR>" \
           "Please create price links.<BR><BR>" \
           "Regards,<BR>" \
           "Prime and Equities BTB team"
    email = EmailHelper(body, subject, send_to)
    if str(acm.Class()) == "FACMServer":
        email.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email.host = EmailHelper.get_acm_host()
    try:
        email.send()
    except Exception as ex:
        LOGGER.exception("Error while sending e-mail: {0}\n".format(ex))


def ael_main(dict):
    """Entry point of the script."""

    process_name = "saps_move_trades"
    with bp_start(process_name):

        move_dict = defaultdict(lambda: defaultdict(list))
        trades = dict["query_folder"].Query().Select()
        for trade in trades:
            if trade.Instrument().Name().split('/')[-1] != "MTM":
                move_dict[trade.Portfolio().Name()][trade.Instrument().Name()].append(trade)

        insList = []
        exceptionList = []
        for portfolio_name in move_dict:
            LOGGER.info("Portfolio: {0}".format(portfolio_name))
            for instrument_name in move_dict[portfolio_name]:
                try:
                    LOGGER.info("\tInstrument: {0}".format(instrument_name))
                    (mtm_instrument, is_new) = getMTMInstrument(acm.FInstrument[instrument_name])
                    if is_new:
                        if mtm_instrument.InsType() == "ETF":
                            insList.append(mtm_instrument.Name())
                    for trade in move_dict[portfolio_name][instrument_name]:
                        LOGGER.info("\t\tTrade: {0}".format(trade.Name()))
                        moveTrade(trade, mtm_instrument)
                except Exception as ex:
                    LOGGER.exception(ex)
                    exceptionList.append(sys.exc_info())

        if dict['send'] and len(insList) > 0:
            send_email(list(dict["emails"]), insList)

        if len(exceptionList) > 0:
            raise RuntimeError('Errors occurred. See the log for details.')
        LOGGER.info('Completed successfully')

