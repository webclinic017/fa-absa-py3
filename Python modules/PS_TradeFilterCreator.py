"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2018-10-02                  Reiss Tibor           Use transactions

Facilitates the creation of trade filters for the PB new client setup.
"""


import acm

from at_logging import getLogger
from PS_AssetClasses import CFD
from PS_Mixins import (AlwaysRelevant,
                       DescendantAware)
from PS_Names import (get_call_margin_trdnbr,
                      get_top_cr_portfolio_name,
                      get_top_coll_portfolio_name,
                      get_call_accnt_portfolio_name,)


__all__ = ['setup_trade_filters']


LOGGER = getLogger()


## Abstract classes.

class TradeFilter(DescendantAware):
    """
    An abstract descendant-aware class.

    Once a subclass is created, it will be automatically included in the
    list of trade filters to be created for new clients by the
    setup_trade_filters function. Subclasses may/should supply the following
    attributes and methods:

    is_relevant - a method accepting client configuration (as specified
        in PS_MO_Onboarding), returning True or False - is the trade filter
        represented by the subclass relevant to the given client?

    _template - a template for the TradeFilter conditiones
        or
    _get_template - a dynamic method for creating the template based on
        client config.

    _get_data - return TF's name and parameters based on client config.


    DO NOT SUBCLASS IN OTHER MODULES!

    """

    @classmethod
    def _get_template(cls, config):
        """Override this to enable config-based template modifications."""
        return cls._template

    @staticmethod
    def _get_filtering_matrix(template, params):
        """
        Get an FMatrix filter condition from the supplied template and params.
        """
        matrix = acm.FMatrix()
        for template_row in template:
            row = [
                (item % params) if isinstance(item, str) else item
                for item in template_row
            ]
            matrix.AddRow(row)
        return matrix

    @classmethod
    def _get_data(cls, config):
        """Return trade filter name and the dictionary of parameters."""
        raise NotImplementedError()

    @classmethod
    def to_acm(cls, config, name, params):
        template = cls._get_template(config)
        filtering_matrix = cls._get_filtering_matrix(template, params)
        # FTradeSelection "cannot be instantiated", therefore we use cloning here:
        tf = acm.FTradeSelection.Select('')[-1].Clone()  # ACM caches this somehow.
        tf.Name(name)
        tf.FilterCondition(filtering_matrix)
        tf.Query(None)
        return tf


## Classes representing the individual trade filters.

class PB_Onboarding_trades(TradeFilter, AlwaysRelevant):

    @classmethod
    def _get_template(cls, config):
        template = [('', '(', 'Portfolio', 'equal to', '%(financing_prf)s', '')]
        if config[CFD.key]:
            template.append(
                ('Or', '', 'Portfolio', 'equal to', '%(cfd_pswap_prf)s', ''))
        template.extend([
            ('Or', '', 'Portfolio', 'equal to', '%(pswap_CR_prf)s', ')'),
            ('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
            ('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')])
        return template

    @staticmethod
    def _get_data(config):
        name = 'PB_Onb_tr_%s' % config['shortName']
        params = {
            'financing_prf': 'PB_%s_FINANCING' % config['shortName'],
            'pswap_CR_prf': 'PB_PSWAP_%s_CR' % config['shortName'],
        }
        if config[CFD.key]:
            params['cfd_pswap_prf'] = 'PB_CFD_' + config['shortName']
        return name, params


class Positions(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '(', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('Or', '', 'Trade number', 'equal to', '%(call_margin_trdnbr)i', ')'),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = '%s~Positions' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
            'call_margin_trdnbr': get_call_margin_trdnbr(config['shortName']),
        }
        return name, params


class PS_SetAddInfoDate(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '(', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('Or', '', 'Portfolio', 'equal to', '%(noncash_coll_prf)s', ')'),
        ('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'Terminated', ''),
        ('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'Void', ')')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PS_SetAddInfoDate_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
            'noncash_coll_prf': get_top_coll_portfolio_name(config['shortName']),
        }
        return name, params


## New reporting

class Position_View(TradeFilter, AlwaysRelevant):  # TODO: rename?

    _template = [
        ('', '(', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('Or', '', 'Trade number', 'equal to', '%(call_margin_trdnbr)i', ')'),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'Position_View_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
            'call_margin_trdnbr': get_call_margin_trdnbr(config['shortName']),
        }
        return name, params


class PB_NAV2_Cash(TradeFilter, AlwaysRelevant):

    _template =[
        ('', '', 'Portfolio', 'equal to', '%(call_accnt_prf)s', ''),
        ('And', '', 'Instrument.Type', 'equal to', 'Deposit', ''),
        ('And', '(', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ')'),
        ('And', '', 'Counterparty', 'equal to', '%(counterparty)s', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_NAV_Cash_%s' % config['shortName']
        params = {
            'counterparty': config['counterparty'].Name(),
            'call_accnt_prf': get_call_accnt_portfolio_name(config['shortName']),
        }
        return name, params


class PB_NAV2_Equity(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '(', 'Instrument.Underlying type', 'equal to', 'Stock', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'Stock', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'ETF', ''),
        ('Or', '', 'Instrument.Underlying type', 'equal to', 'EquityIndex', ')'),
        ('And', '', 'Instrument.Type', 'not equal to', 'Deposit', ''),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_NAV_Eq_%s' % config['shortName']
        params = {'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),}
        return name, params


class PB_NAV2_FI(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '(', 'Instrument.Underlying type', 'not equal to', 'Stock', ''),
        ('And', '', 'Instrument.Underlying type', 'not equal to', 'EquityIndex', ''),
        ('And', '', 'Instrument.Type', 'not equal to', 'Deposit', ''),
        ('And', '', 'Instrument.Type', 'not equal to', 'ETF', ''),
        ('And', '', 'Instrument.Type', 'not equal to', 'Stock', ')'),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_NAV_FI_%s' % config['shortName']
        params = {'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),}
        return name, params


class PB_CashAnalysis(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(call_accnt_prf)s', ''),
        ('And', '', 'Instrument.Type', 'equal to', 'Deposit', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_CashAnalysis_%s' % config['shortName']
        params = {'call_accnt_prf': get_call_accnt_portfolio_name(config['shortName']),}
        return name, params


class PB_CashInstr(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '(', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('Or', '', 'Trade number', 'equal to', '%(call_accnt_trdnbr)s', ')'),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_CashInstr_%s' % config['shortName']
        params = {
            'call_accnt_trdnbr': get_call_margin_trdnbr(config['shortName']),
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


class PB_CollateralPos(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(noncash_coll_prf)s', ''),
        ('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'Void', ''),
        ('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'FO Confirmed', ')')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_CollateralPos_%s' % config['shortName']
        params = {'noncash_coll_prf': get_top_coll_portfolio_name(config['shortName'])}
        return name, params


class PB_CollTrade(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(noncash_coll_prf)s', ''),
        ('And', '', 'Additional Info.PS_MsgSentDate', 'greater equal', '-1m', ''),
        ('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'Void', ')')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_CollTrade_%s' % config['shortName']
        params = {'noncash_coll_prf': get_top_coll_portfolio_name(config['shortName'])}
        return name, params


class PB_CorpActions(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '(', 'Instrument.Type', 'equal to', 'CFD', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'Stock', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'FRN', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'CFD', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'BuySellback', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'Bond', ')')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_CorpActions_%s' % config['shortName']
        params = {'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),}
        return name, params


class PB_PositionIns(TradeFilter, AlwaysRelevant):

    _template = [('', '(', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('Or', '', 'Trade number', 'equal to', '%(call_accnt_trdnbr)s', ')'),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_PositionIns_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
            'call_accnt_trdnbr': get_call_margin_trdnbr(config['shortName']),
        }
        return name, params


class PB_Positions(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'less than', '1d', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_Positions_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


class PB_RiskSwapAttr(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '', 'Acquirer', 'equal to', 'PRIME SERVICES DESK', ''),
        ('And', '(', 'Instrument.Type', 'equal to', 'IndexLinkedSwap', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'Swap', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'FRA', ')'),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_RiskSwapAttr_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


class PB_RiskBondAttr(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '(', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ')'),
        ('And', '(', 'Instrument.Type', 'equal to', 'Bond', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'FRN', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'CD', ')')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_RiskBondAttr_%s' % config['shortName']
        params = {'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),}
        return name, params


class PB_TradeActivity(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Time', 'greater than', '-1d', '')
    ]
    @staticmethod
    def _get_data(config):
        name = 'PB_TradeActivity_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


class PB_TradeRoll(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '', 'Instrument.Type', 'not equal to', 'Deposit', ''),
        ('And', '', 'Additional Info.PS_MsgSentDate', 'greater equal', '-1m', ''),
        ('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'Terminated', ''),
        ('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
        ('Or', '', 'Status', 'equal to', 'Void', ')')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_TradeRoll_%s' % config['shortName']
        params = {'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),}
        return name, params


class PB_CallAccount(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(call_accnt_prf)s', ''),
        ('And', '', 'Instrument.Type', 'equal to', 'Deposit', ''),
        ('And', '(', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ')'),
        ('And', '', 'Counterparty', 'equal to', '%(counterparty)s', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_CallAccount_%s' % config['shortName']
        params = {
            'counterparty': config['counterparty'].Name(),
            'call_accnt_prf': get_call_accnt_portfolio_name(config['shortName']),
        }
        return name, params


class PB_RiskFX(TradeFilter, AlwaysRelevant):

    _template = [
        ('', '', 'Portfolio', 'equal to', '%(compound_CR_prf)s', ''),
        ('And', '(', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
        ('Or', '', 'Instrument.Type', 'equal to', 'Option', ')'),
        ('And', '(', 'Instrument.Underlying type', 'equal to', 'Bond', ''),
        ('Or', '', 'Instrument.Underlying type', 'equal to', 'Curr', ')'),
        ('And', '', 'Status', 'not equal to', 'Void', ''),
        ('And', '', 'Status', 'not equal to', 'Simulated', ''),
        ('And', '', 'Instrument.Expiry day', 'greater equal', '-1m', '')
    ]

    @staticmethod
    def _get_data(config):
        name = 'PB_RiskFX_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


## <--


## Main body.

def setup_trade_filters(config):
    """
    Create trade filters for the new PB client.

    <config> is the ael_variables instance from PS_MO_Onboarding.

    """
    if config['dryRun']:
        return
    
    acm.BeginTransaction()
    try:
        for tf_cls in TradeFilter.get_descendants():
            if not tf_cls.is_relevant(config):
                continue
            LOGGER.info('Processing %s...', tf_cls.__name__)
            name, params = tf_cls._get_data(config)
            tf = acm.FTradeSelection.Select01("name = %s" % name, None)
            if tf is not None:
                LOGGER.info("Trade filter {} already exists".format(name))
                continue
            tf = tf_cls.to_acm(config, name, params)
            tf.Owner("ATS")
            tf.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        LOGGER.exception("Couldn't create trade filter")
        raise e
