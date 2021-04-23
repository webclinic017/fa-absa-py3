'''-----------------------------------------------------------------------------
Facilitates the creation of tasks for the PB new client setup.

Note: multistrategy clients are currently ignored.
Their setup would eventually have to be amended by hand.

HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2018-10-02                 Tibor Reiss        Use transactions
2020-01-20  FAPE-173       Tibor Reiss        New ATS for PS mirroring
2020-05-18  FAPE-175       Marcus Ambrose     Portal parallel run tasks, remove in June
2020-06-04  FAPE-401       Marcus Ambrose     Remove old portal live views task creator class
2021-02-04  FAPE-468       Katerina Frickova  Use query folder in the Instrument field of FRerate tasks
--------------------------------------------------------------------------------
'''

import acm

from at_logging import getLogger
from PS_AssetClasses import AssetClass, CFD, CORPBONDS
from PS_Mixins import DescendantAware, AlwaysRelevant, relevant_for_products
from PS_Names import (CALLACCNT_TYPES,
                      get_callaccnt_name,
                      get_portfolio_name,
                      get_pswap_name,
                      get_top_cr_portfolio_name,
                      get_portfolio_name_by_id)


__all__ = ['setup_tasks']


LOGGER = getLogger(__name__)


## Helper functions


def _set_task_param(acm_task, key, value, commit=False):
    params = acm_task.Parameters()
    params.AtPutStrings(key, value)
    acm_task.Parameters(params)
    if commit:
        acm_task.Commit()


def _get_default_portfolio_name(config):
    """Return an arbitrary product portfolio for the client."""
    # Config validation PS_MO_Onboarding ensures that a porftolio will always
    # be found.
    traded_products = [product for product in AssetClass.get_all() if config[product.key]]
    for product in traded_products:
        for fullyfunded in (True, False):
            prf_name = get_portfolio_name(product, config['shortName'], cr=True,
                fullyfunded=fullyfunded)
            if acm.FPhysicalPortfolio[prf_name]:
                return prf_name


## Abstract classes.


class Task(DescendantAware):
    """
    An abstract descendant-aware class.

    Once a subclass is created, it will be automatically included in the
    list of tasks to be created for new clients by the setup_tasks function.
    Subclasses should supply the following attributes and methods:

    update_task - a bool attribute controlling if the task should be
    updated if it already exists

    template - a string attribute holding the name of the template from
        which the task should be created.

    is_relevant - a method accepting client configuration (as specified
        in PS_MO_Onboarding), returning True or False - is the task represented
        by the subclass relevant to the given client?

    get_data - a method accepting client configuration returning the task name
        and parameter values that should override the ones in the template.

    DO NOT SUBCLASS IN OTHER MODULES!

    """

    update_task = False

    @classmethod
    def to_acm(cls, config):
        name, params = cls.get_data(config)
        # Return if task with same name already exitst
        if acm.FAelTask[name]:
            if cls.update_task:
                LOGGER.warning("Task with name {} already exists - updating...".format(name))
                template_task = acm.FAelTask[name]
                task_acm = template_task.Clone()
                task_params = task_acm.Parameters()
                for key, val in params.iteritems():
                    task_params.AtPutStrings(key, val)
                    print(key, val)
                task_acm.Parameters(task_params)
                template_task.Apply(task_acm)
                template_task.Commit()
        else:
            template_task = acm.FAelTask[cls.template]
            task_acm = template_task.Clone()
            task_acm.Name(name)
            # Avoid propagating of template descriptions to task instances (the
            # vast majority of the existing tasks don't have any description anyway).
            task_acm.Description('')
            task_params = task_acm.Parameters()
            for key, val in params.iteritems():
                task_params.AtPutStrings(key, val)
            task_acm.Parameters(task_params)
            task_acm.Commit()


## Classes representing the individual tasks.


class PS_AddTradeFees(Task, AlwaysRelevant):

    template = 'PS_Template_AddTradeFees'

    @staticmethod
    def get_data(config):
        short_name = config['shortName']
        name = 'PS_AddTradeFees_%s_SERVER' % short_name
        params = {
            'compoundPropPortfolio': get_portfolio_name_by_id("RISK_FV", short_name),
            'compoundAgencyPortfolio': get_top_cr_portfolio_name(short_name),
            'clientName': config['counterparty'].Name(),
        }
        return name, params


class PS_Generate(Task, relevant_for_products(CFD)):

    template = 'PS_Template_Generate'

    @staticmethod
    def get_data(config):
        name = 'PS_Generate_%s_SERVER' % config['shortName']
        params = {'portfolioSwaps': get_pswap_name(CFD, config['shortName']),
                  'clientName':config['shortName']
                  }
        return name, params


class PS_MTM(Task, relevant_for_products(CFD)):

    template = 'PS_Template_MTM'

    @staticmethod
    def get_data(config):
        name = 'PS_MTM_%s_SERVER' % config['shortName']
        params = {'portfolioSwaps': get_pswap_name(CFD, config['shortName']),
                  'clientName':config['shortName']
                  }
        return name, params


class PS_Sweeping(Task, relevant_for_products(CFD)):

    template = 'PS_Template_Sweeping'

    @staticmethod
    def get_data(config):
        name = 'PS_Sweeping_%s_SERVER' % config['shortName']
        params = {'portfolioSwaps': get_pswap_name(CFD, config['shortName']),
                  'clientName': config['shortName'],
                  'output_dir': '/services/frontnt/Task/',
                  'output_filename': 'CFD_Sweeping'
                  }
        return name, params


class PS_Extend_General_PSwaps(Task, AlwaysRelevant):

    template = 'PS_Template_Extend_General_PSwaps'

    @staticmethod
    def get_data(config):
        name = 'PS_Extend_General_PSwaps_%s_SERVER' % config['shortName']
        params = {
            'portfolioSwaps': '?PS_General_PSwaps_%s' % config['shortName'],
            'compoundPortfolio': get_top_cr_portfolio_name(config['shortName']),
            'collateralPortfolios': get_portfolio_name_by_id("COLL", config['shortName'], cr=True),
            'clientName' : config['shortName']
        }
        return name, params


class PS_TPLSweep_General_PSwaps(Task, AlwaysRelevant):

    template = 'PS_Template_TPLSweep_General_PSwaps'

    @staticmethod
    def get_data(config):
        name = 'PS_TPLSweep_General_PSwaps_%s_SERVER' % config['shortName']
        params = {
            'portfolioSwaps': '?PS_General_PSwaps_%s' % config['shortName'],
            'sweepingReport': (
                '/services/frontnt/Task/'
                '%s_CallAccountSweepingReport_$DATE.csv') % config['shortName'],
            'clientName': config['shortName']
        }
        return name, params


class PS_SetAddInfoDate(Task, AlwaysRelevant):

    template = 'PS_Template_SetAddInfoDate'

    @staticmethod
    def get_data(config):
        name = 'PS_SetAddInfoDate_%s_SERVER' % config['shortName']
        params = {
            'tradeFilters': 'PS_SetAddInfoDate_%s' % config['shortName'],
            'clientName': config['shortName']
        }
        return name, params


class PS_Portal_LIVE_PrfView(Task, AlwaysRelevant):

    template = 'PS_Portal_Template_LIVE_PrfView'

    @staticmethod
    def get_data(config):
        name = 'PS_Portal_%s_LIVE_PrfView_SERVER' % config['shortName']
        params = {
            'tradeFilters': '%s~Positions' % config['shortName'],
            'File Name': 'PS_%s_LIVE_PrfView' % config['shortName'],
        }
        return name, params


class PS_Portal_LIVE_TrdView(Task, AlwaysRelevant):

    template = 'PS_Portal_Template_LIVE_TrdView'

    @staticmethod
    def get_data(config):
        name = 'PS_Portal_LIVE_TrdView_%s_SERVER' % config['shortName']
        params = {
            # Note: The queryfolder name is prescribed by Portal requirements
            # to be <client_name>~Trades.
            'storedASQLQueries': '%s~Trades' % config['shortName'],
            'File Name': 'PS_LIVE_TrdView_%s' % config['shortName'],
        }
        return name, params


class PS_LoanAccountSweeper(Task, AlwaysRelevant):

    template = 'PS_Template_LoanAccountSweeper'

    @staticmethod
    def get_data(config):
        short_name = config['shortName']
        name = 'PS_LoanAccountSweeper_%s_SERVER' % short_name
        params = {
            'counterparty': '%s' % config['counterparty'].Name(),
            'sweepingReport': (
                '/services/frontnt/Task/'
                '%s_LoanAccountSweepingReport_$DATE.csv') % short_name,
        }
        return name, params


class PS_FRerate(Task, AlwaysRelevant):

    template = 'PS_Template_FRerate'

    @staticmethod
    def get_data(config):
        name = 'PS_FRerate_%s_SERVER' % config['shortName']
        params = {'instruments': '?PS_CallAccounts_%s' % config['shortName'], }

        return name, params


class PS_Reporting(Task, AlwaysRelevant):

    template = 'PS_Template_Reporting'

    @staticmethod
    def get_data(config):
        short_name = config['shortName']
        name = 'PS_Reporting_%s_SERVER' % short_name
        params = {
            'clientName': '%s' % config['counterparty'].Name(),
            'fileID_SoftBroker': short_name,
            'TradeFilter_Heavy Cash': 'PB_CashAnalysis_%s' % short_name,
            'Workbook_Heavy Cash': 'PB_CashAnalysis_%s' % short_name,
            'tradeFilters_Heavy Cashflows': 'PB_CashInstr_%s' % short_name,
            'TradeFilter_Heavy Collateral Positions': 'PB_CollateralPos_%s' % short_name,
            'TradeFilter_Heavy Collateral Trades': 'PB_CollTrade_%s' % short_name,
            'TradeFilter_Heavy Corporate Actions': 'PB_CorpActions_%s' % short_name,
            'TradeFilter_Heavy Instrument Position': 'PB_PositionIns_%s' % short_name,
            'TradeFilter_Heavy Position': 'PB_Positions_%s' % short_name,
            'TrdFilter_Heavy Risk Bond Attribution Report': 'PB_RiskBondAttr_%s' % short_name,
            'TradeFilter_Heavy Risk FX': 'PB_RiskFX_%s' % short_name,
            'TrdFilter_Heavy Risk Report - Reset Dates': 'Position_View_%s' % short_name,
            'TrdFilter_Heavy Risk Swap Attribution Report': 'PB_RiskSwapAttr_%s' % short_name,
            'TradeFilter_Heavy Risk Yield Delta': 'Position_View_%s' % short_name,
            'TradeFilter_Heavy Trade': 'PB_TradeRoll_%s' % short_name,
            'TradeFilter_Light Collateral Positions': 'PB_CollateralPos_%s' % short_name,
            'TradeFilter_Light Corporate Actions': 'PB_CorpActions_%s' % short_name,
            'TradeFilter_Light Performance': 'PB_Positions_%s' % short_name,
            'TradeFilter_Light Position': 'PB_Positions_%s' % short_name,
            'TradeFilter_Light Trade': 'PB_TradeActivity_%s' % short_name,
            'eqTradeFilter_Light Valuations': 'PB_NAV_Eq_%s' % short_name,
            'fiTradeFilter_Light Valuations': 'PB_NAV_FI_%s' % short_name,
            'cashTradeFilter_Light Valuations': 'PB_NAV_Cash_%s' % short_name,
            'storedASQLQuery_Light Financing': 'PS_Financing_%s' % short_name,
            'storedASQLQuery_Heavy Financing': 'PS_Financing_%s' % short_name,
            'storedASQLQuery_Heavy Valuations': 'PS_Valuations_%s' % short_name,
        }
        return name, params


class PS_CallAccountReports(Task, AlwaysRelevant):

    template = 'PS_Template_CallAccountReports'

    @staticmethod
    def get_data(config):
        name = 'PS_CallAccountReports_%s_SERVER' % config['shortName']
        is_fixed_income = any(config[p.key] for p in AssetClass.get_fixed_income())
        is_equity = any(config[p.key] for p in AssetClass.get_equities())
        params = {
            'clientName': '%s' % config['counterparty'].Name(),
            'fileID_SoftBroker': config['shortName'],
            'checkCreditMargin': 'Yes' if config[CORPBONDS.key] else 'No',
            'checkEqMargin': 'Yes' if is_equity else 'No',
            'checkFiMargin': 'Yes' if is_fixed_income else 'No',
            'TradeFilter_Heavy cash': 'PB_CallAccount_%s' % config['shortName'],
            'TradeFilter_Light cash': 'PB_CallAccount_%s' % config['shortName'],
        }
        return name, params


class PS_Payments(Task, AlwaysRelevant):
    """Off tree payments."""

    template = 'PS_Template_Payments'

    @staticmethod
    def get_data(config):
        name = 'PS_Payments_%s_SERVER' % config['shortName']
        params = {
            'counterparty': config['shortName']
        }
        return name, params

## <--


## Main body.

def setup_tasks(config):
    """
    Create tasks for the new PB client.

    <config> is the ael_variables instance from PS_MO_Onboarding.
    """
    if config['dryRun']:
        LOGGER.warning('Skipping the actual creation according to the Dry Run setting.')
        return
    acm.BeginTransaction()
    try:
        for task_cls in Task.get_descendants():
            if not task_cls.is_relevant(config):
                continue
            LOGGER.info('Processing %s...', task_cls.template)
            task_cls.to_acm(config)
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        LOGGER.exception("Could not create tasks")
        raise e