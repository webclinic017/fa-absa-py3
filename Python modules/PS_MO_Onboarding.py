"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Automatically create the entities needed for
                           onboarding of new Prime Brokerage funds.
DEPATMENT AND DESK      :  Middle Office
REQUESTER               :  Merell Nair
DEVELOPER               :  Hynek Urban
CR NUMBER               :  1019492
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2013-05-16 1019492          Hynek urban           Initial Implementation
2018-05-25                  Reiss Tibor           Add RTM part
2018-10-02                  Reiss Tibor           Use transactions

Automation of the TCU's part of Prime Brokerage fund onboarding.
"""


import acm

from at_logging import bp_start, getLogger
import PS_MO_Onboarding_Config
from PS_PortfolioCreator import setup_portfolios
from PS_AddInfos import (setup_addinfos, setup_counterparty_task)
from PS_PswapCreator import setup_pswaps
from PS_AssetClasses import (AssetClass, CFD)
from PS_AccountCreator import setup_call_accounts
from PS_TaskCreator import setup_tasks
from PS_TradeFilterCreator import setup_trade_filters
from PS_WorkbookCreator import setup_workbooks
from PS_QueryFolderCreator import setup_query_folders
import PS_Onboarding_RTM


LOGGER = getLogger()


def __to_heading(text):
    """
    Return the provided text formatted as a heading.
    """
    return '\n{0}\n{1}\n'.format(text, '-' * len(text))


ael_variables = PS_MO_Onboarding_Config.get_main_config()
ael_variables.extend(PS_MO_Onboarding_Config.get_product_types_config())
ael_variables.extend(PS_MO_Onboarding_Config.get_pswaps_config())
ael_variables.extend(PS_MO_Onboarding_Config.get_pswaps_rate_bid_ask_config())
ael_variables.extend(PS_MO_Onboarding_Config.get_call_accounts_config())
ael_variables.extend(PS_MO_Onboarding_Config.get_fees_config())


def ael_main(ael_dict):
    config = PS_MO_Onboarding_Config.ConfigDict(ael_dict)
    config.preprocess()
    try:
        config.validate()
    except PS_MO_Onboarding_Config.ValidationError as exc:
        LOGGER.exception('Validation failed')
        message = 'Validation failed:\n{0}'.format(exc)
        message_box = acm.GetFunction('msgBox', 3)
        message_box('Error', message, 0)
        return
    process_name = 'ps.onboarding.tcu.{0}'.format(config['shortName'])
    with bp_start(process_name):
        # Set up general portfolios - does not depend on product type
        setup_portfolios(config, None)
        # Loop through ticked product types
        for ac in AssetClass.get_all():
            if config[ac.key]:
                LOGGER.info(__to_heading('Creating portfolio tree...'))
                setup_portfolios(config, ac)
                LOGGER.info(__to_heading('Creating portfolio swaps...'))
                setup_pswaps(config, ac)
        LOGGER.info(__to_heading('Creating call accounts...'))
        setup_call_accounts(config)
        LOGGER.info(__to_heading("Setting up portfolios' additional infos..."))
        setup_addinfos(config)
        LOGGER.info(__to_heading('Creating trade filters...'))
        setup_trade_filters(config)
        LOGGER.info(__to_heading('Creating workbooks...'))
        setup_workbooks(config)
        LOGGER.info(__to_heading('Creating query folders...'))
        setup_query_folders(config)
        LOGGER.info(__to_heading('Setting up counterparty...'))
        counterparty_setup_task_name = setup_counterparty_task(config)
        LOGGER.info(__to_heading('Creating tasks...'))
        setup_tasks(config)
        if not config['dryRun'] and config[CFD.key]:
            LOGGER.info("CFDs are traded, running RTM setup...")
            PS_Onboarding_RTM.setup_rtm(config)
        LOGGER.info('Finished successfully\n')
        LOGGER.info('IMPORTANT: Please run the task "%s" '
                    'in order to finish the onboarding.',
                    counterparty_setup_task_name)
        if config['dryRun']:
            LOGGER.warning('Please note that entities were '
                           'actually NOT created in the database '
                           'due to the "Dry Run" setting.')
