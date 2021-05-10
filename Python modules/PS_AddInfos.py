"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Additional Infos for various PS portfolios.
DEPATMENT AND DESK      :  Middle Office
REQUESTER               :
DEVELOPER               :  Hynek Urban
CR NUMBER               :  1019492
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2013-16-05 1019492          Hynek urban           Initial Implementation
2018-10-02                  Tibor Reiss           Use transactions

"""


import re

import acm

from at_logging import getLogger
from at_choice import (get as choice_get, add as choice_add)
from PS_AssetClasses import (AssetClass,
                             CFD,
                             CORPBONDS,
                             GOVIBONDS,
                             COMMODITIES,
                             CASH_EQUITY,
                             SAFEX,
                             YIELDX)
from PS_Mixins import DescendantAware, AlwaysRelevant
from PS_Names import (get_portfolio_name,
                      get_pswap_name,
                      get_callaccnt_name,
                      get_top_cr_portfolio_name,
                      get_top_coll_portfolio_name,
                      get_portfolio_name_by_id,
                      CALLACCNT_GENERAL,
                      CALLACCNT_LOAN,
                      CALLACCNT_SAFEX,
                      CALLACCNT_YIELDX,
                      CALLACCNT_COMMODITIES)
from pb_quirk import (CallAccountQuirk,
                      CollateralPortfolioQuirk,
                      CommoditiesCallAccountQuirk,
                      LoanAccountQuirk,
                      ReportingPortfolioQuirk,
                      SafexCallAccountQuirk,
                      YieldXCallAccountQuirk)
from PS_Onboarding_RTM import (PF_PREFIX_ACS, PF_PREFIX_BANK)


LOGGER = getLogger()


__all__ = ['setup_addinfos',]


def check_account(product_type_key, account_type, client_name, dry_run):
    account_name = get_callaccnt_name(client_name, account_type)
    if acm.FInstrument[account_name]:
        return account_name
    elif product_type_key and not dry_run:
            msg = "Account {} does not exist".format(account_name)
            LOGGER.error(msg)
            raise RuntimeError(msg)
    return None


def setup_counterparty_task(config):
    fund_id = config['shortName']
    counterparty = config['counterparty']
    reporting_portfolio = get_top_cr_portfolio_name(fund_id)
    collateral_portfolio = get_top_coll_portfolio_name(fund_id)

    call_account = get_callaccnt_name(fund_id, CALLACCNT_GENERAL)
    loan_account = get_callaccnt_name(fund_id, CALLACCNT_LOAN)
    commodities_call_account = check_account(config[COMMODITIES.key], CALLACCNT_COMMODITIES, fund_id, config['dryRun'])
    safex_call_account = check_account(config[SAFEX.key], CALLACCNT_SAFEX, fund_id, config['dryRun'])
    yieldx_call_account = check_account(config[YIELDX.key], CALLACCNT_YIELDX, fund_id, config['dryRun'])

    info_message = ('Counterparty-level additional infos '
                    'which need to be set up:\n\n')
    quirks = [ReportingPortfolioQuirk,
              CollateralPortfolioQuirk,
              CallAccountQuirk,
              LoanAccountQuirk,
              CommoditiesCallAccountQuirk,
              SafexCallAccountQuirk,
              YieldXCallAccountQuirk]
    variables = [reporting_portfolio,
                 collateral_portfolio,
                 call_account,
                 loan_account,
                 commodities_call_account,
                 safex_call_account,
                 yieldx_call_account]
    for quirk, variable in zip(quirks, variables):
        info_message += '{0}:\t"{1}"\n'.format(
            quirk.ADD_INFO_NAME, variable)
    LOGGER.info(info_message)

    task_name = 'PB_cpty_setup_{0}'.format(fund_id)
    if config['dryRun']:
        LOGGER.warning('Skipping the actual creation according to the Dry Run setting.')
        return task_name

    acm.BeginTransaction()
    try:
        # Needed to store the initial entry
        # of the newly created fund to the text object 'database'.
        text_parameters = ('call_account=%s;\n'
                           'collateral_portfolio=%s;\n'
                           'commodities_call_account=%s;\n'
                           'counterparty=%s;\n'
                           'loan_account=%s;\n'
                           'reporting_portfolio=%s;\n'
                           'safex_call_account=%s;\n'
                           'yieldx_call_account=%s;\n') % (
                               call_account,
                               collateral_portfolio,
                               commodities_call_account if commodities_call_account else '',
                               counterparty.Name(),
                               loan_account,
                               reporting_portfolio,
                               safex_call_account if safex_call_account else '',
                               yieldx_call_account if yieldx_call_account else '')
        acm_task = acm.FAelTask[task_name]
        if acm_task:
            LOGGER.warning("Task {} already exists - updating!".format(task_name))
            task = acm_task.Clone()
            task.ParametersText(text_parameters)
            acm_task.Apply(task)
            acm_task.Commit()
        else:
            LOGGER.info('Creating task "%s"', task_name)
            task = acm.FAelTask['PS_cpty_setup_sample'].Clone()
            task.Name(task_name)
            task.ParametersText(text_parameters)
            task.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        LOGGER.exception("Could not create task {}".format(task_name))
        raise e

    return task_name


class PortfolioAddInfo(DescendantAware):
    """
    The base class for Additional Infos.

    Once a subclass is created, it will be automatically included in the
    additional info list to be added to new protfolios by the 'setup_addinfos'
    function. Mentioned subclasses may/should supply the following attributes
    and methods:

    _is_relevant - a method accepting a portfolio and client configuration,
        returning True or False - is the additional info represented by the
        subclass in question relevant to the given portfolio/client combination?

    _get_value - a method accepting a portfolio and client configuration
        returning the actual addinfo value.

    _abstract - a class attribute - if present and set to True, the subclass
        doesn't get to the additional info list. However, it's descendans do.

    _name - specifies the addinfo spec name. If ommited, the class name will be
        used.

    DO NOT SUBCLASS IN OTHER MODULES!

    """

    @staticmethod
    def _is_relevant(prf, cfg):
        """
        Should this addinfo be set on the portfolio in question?

        Overide this in child classes if necessary.

        """
        return True

    @staticmethod
    def _get_value(prf, cfg):
        """
        Get value of this addinfo for the specified portfolio.

        Override this in descendant classes.

        """
        raise NotImplementedError()

    @classmethod
    def apply_(cls, portfolio, client_config):
        """Create the AddInfo for the portfolio if relevant."""
        # If the additional info alredy exists, through a warning and overwrite with new value.
        if cls._is_relevant(portfolio, client_config):
            add_infos = acm.FAdditionalInfo.Select("recaddr = %i" % portfolio.Oid())
            ai_spec = cls.__dict__.get('_name') or cls.__name__
            new_value = cls._get_value(portfolio, client_config)
            # First check if add info is already present for portfolio
            for ai in add_infos:
                if ai.AddInf().Name() == ai_spec:
                    if new_value != ai.FieldValue():
                        LOGGER.warning("Updating already existing add info {} "
                                       "on portfolio {} from {} to {}".format(ai_spec,
                                       portfolio.Name(), ai.FieldValue(), new_value))
                        ai.FieldValue(new_value)
                        ai.Commit()
                    return
            # Not found so create it
            LOGGER.info("Creating add info {} with value {}".format(ai_spec, new_value))
            ai = acm.FAdditionalInfo()
            ai.Recaddr(portfolio.Oid())
            ai.AddInf(acm.FAdditionalInfoSpec[ai_spec])
            ai.FieldValue(new_value)
            ai.Commit()


## Helper functions

def _get_parent_portfolio(prf):
    """Retrieve parent portfolio, if any."""
    try:
        return prf.MemberLinks()[0].OwnerPortfolio()
    except IndexError:
        return None


def _get_product_for_portfolio(prf, cfg):
    """
    Get the product corresponding to the given portfolio and configuration.

    'None' is returned in case no product directly corresponds to the portfolio.

    """
    if prf.Name() == cfg['cfdAccount']:
        return CFD
    for product in AssetClass.get_all():
        for cr in (True, False):
            for ff in (True, False):
                prfname = get_portfolio_name(product, cfg['shortName'], cr, ff)
                if prf.Name() == prfname:
                    return product


def _is_fullyfunded(prf):
    parent = _get_parent_portfolio(prf)
    if parent is None:
        return False
    return re.match('^PB_FULLYFUNDED_.*_CR$', parent.Name()) is not None

## <--

## Here the declarations of individual AddInfos begin.

class Parent_Portfolio(PortfolioAddInfo):
    _get_value = staticmethod(lambda prf, cfg: 'Prime Services Desk')


class PSClientName(PortfolioAddInfo):

    @staticmethod
    def _is_relevant(prf, cfg):
        if re.match('^PB_RISK_.*_CR$', prf.Name()) is not None:
            return True
        return prf.Name().startswith('PB_RISK_FV_')

    _get_value = staticmethod(lambda prf, cfg: cfg['counterparty'].Name())


class AssetClassSpecificAddInfo(PortfolioAddInfo):
    """Abstract AddInfo relevant for asset-class related portfolios only."""

    _abstract = True

    @staticmethod
    def _get_value(prf, cfg):
        raise NotImplementedError()

    @staticmethod
    def _is_relevant(prf, cfg):
        return _get_product_for_portfolio(prf, cfg) is not None


class PS_PortfolioType(AssetClassSpecificAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        product = _get_product_for_portfolio(prf, cfg)
        return 'CFD' if product == CFD else 'General'


class PSExtExecPremRate(AssetClassSpecificAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        product = _get_product_for_portfolio(prf, cfg)
        return cfg['%s_DMA_fee' % product.key]


class PSSimpleRateFactor(PortfolioAddInfo):
    # Factor used in execution fee calculation for commodities
    @staticmethod
    def _is_relevant(prf, cfg):
        return prf.Name() == get_portfolio_name(COMMODITIES, cfg['shortName'], cr=True)

    @staticmethod
    def _get_value(prf, cfg):
        return cfg['CommoditiesExecFee']


class PSExtExecPremNonDMA(AssetClassSpecificAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        product = _get_product_for_portfolio(prf, cfg)
        return cfg['%s_NonDMA_fee' % product.key]


class PSExtExecPremVoice(AssetClassSpecificAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        product = _get_product_for_portfolio(prf, cfg)
        return cfg['%s_Voice_fee' % product.key]


class PS_FundingIns(AssetClassSpecificAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        product = _get_product_for_portfolio(prf, cfg)
        return get_pswap_name(product, cfg['shortName'], _is_fullyfunded(prf))


class PSClientCallAcc(PortfolioAddInfo):

    @staticmethod
    def _is_relevant(prf, cfg):
        compound_prfs = (
            get_top_cr_portfolio_name(cfg['shortName']),
            'PB_RISK_FV_%s' % cfg['shortName'],
        )
        return (_get_product_for_portfolio(prf, cfg) is not None or
                prf.Name() in compound_prfs)

    @staticmethod
    def _get_value(prf, cfg):
        if prf.Name() == get_top_cr_portfolio_name(cfg['shortName']):
            return get_callaccnt_name(cfg['shortName'], CALLACCNT_LOAN)
        return get_callaccnt_name(cfg['shortName'], CALLACCNT_GENERAL)


class PS_ClientFundName(PortfolioAddInfo):

    @classmethod
    def _is_relevant(cls, prf, cfg):
        """Relevant mostly for asset-specific portfolios in the CR subtree."""
        callaccnt_prf = get_portfolio_name_by_id("CALLACCNT", cfg['shortName'])
        return prf.Name() == callaccnt_prf or prf.Name() in (
            get_portfolio_name(product, cfg['shortName'], cr=True, fullyfunded=ff)
            for product in AssetClass.get_all() for ff in (True, False)
        )

    @staticmethod
    def _get_value(prf, cfg):
        return cfg['counterparty'].Alias('SoftBroker')


class PSMarginFactor(PortfolioAddInfo):

    @staticmethod
    def _is_relevant(prf, cfg):
        return prf.Name() in (
            get_portfolio_name_by_id("RISK_FV", cfg['shortName']),
            get_portfolio_name_by_id("RISK", cfg['shortName'], cr=True),
        )

    _get_value = staticmethod(lambda prf, cfg: 1.0)


class PS_FullyFunded(PortfolioAddInfo):

    @staticmethod
    def _is_relevant(prf, cfg):
        if re.match('^PB_FULLYFUNDED_.*_CR$', prf.Name()) is not None:
            return True
        return (_get_product_for_portfolio(prf, cfg) is not None and
                _is_fullyfunded(prf))

    _get_value = staticmethod(lambda prf, cfg: 'Yes')


class CollationAddInfo(PortfolioAddInfo):

    _abstract = True
    _regex = re.compile('^PB_CAT_([A-E])_.*_CR$')

    @staticmethod
    def _get_value(prf, cfg):
        raise NotImplementedError()

    @classmethod
    def _is_relevant(cls, prf, cfg):
        return cls._regex.match(prf.Name()) is not None


class PS_DualListed(PortfolioAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        return cfg['dualListed'] and 'Yes' or 'No'

    @classmethod
    def _is_relevant(cls, prf, cfg):
        return prf.Name() == get_top_cr_portfolio_name(cfg['shortName'])


class PS_CollCategory(CollationAddInfo):

    @classmethod
    def _get_value(cls, prf, cfg):
        return cls._regex.match(prf.Name()).groups()[0]


class PS_CollHaircut(CollationAddInfo):

    @classmethod
    def _get_value(cls, prf, cfg):
        category = cls._regex.match(prf.Name()).groups()[0]
        return {'A': 0, 'B': 10, 'C': 15, 'D': 20, 'E': 25}[category]


class SLAddInfo(PortfolioAddInfo):

    _abstract = True

    @staticmethod
    def _get_value(prf, cfg):
        raise NotImplementedError()

    @staticmethod
    def _is_relevant(prf, cfg):
        """Returns True if this portfolio is of interest to Securities Lending."""
        if prf.Name() == cfg['cfdAccount']:
            return True
        return prf.Name() in (
            get_portfolio_name(CORPBONDS, cfg['shortName']),
            get_portfolio_name(GOVIBONDS, cfg['shortName']),
            get_portfolio_name(CASH_EQUITY, cfg['shortName'], cr=True),
            get_portfolio_name(CASH_EQUITY, cfg['shortName'], cr=True,
                               fullyfunded=True),
        )


class SL_AllocatedDesk(SLAddInfo):

    @staticmethod
    def _get_value(prf, cfg):
        if _get_product_for_portfolio(prf, cfg) in (GOVIBONDS, CORPBONDS):
            value = get_portfolio_name_by_id("AGENCY", cfg['shortName'], cr=True)
            # Add choice list if it doesn't exist
            if choice_get('AllocatedDesk', value) is None:
                choice_add('AllocatedDesk', value)
            return value
        return 'LinTradingCFD'


class SL_Portfolio_Type(SLAddInfo):
    _get_value = staticmethod(lambda prf, cfg: 'Equity')


class SL_ReservedStock(SLAddInfo):
    _get_value = staticmethod(lambda prf, cfg: 'Yes')


class SL_Sweeping(SLAddInfo):
    _get_value = staticmethod(lambda prf, cfg: 'Yes')


class Prt_BDA_AccountNum(PortfolioAddInfo):

    _name = 'prt_BDA AccountNum'

    @staticmethod
    def _is_relevant(prf, cfg):
        ce = (cfg['ceAccount'] and
              _get_product_for_portfolio(prf, cfg) == CASH_EQUITY)
        cfd = (cfg['cfdAccount'] and prf.Name() == cfg['cfdAccount'])
        return ce or cfd

    @staticmethod
    def _get_value(prf, cfg):
        if cfg['cfdAccount'] and prf.Name() == cfg['cfdAccount']:
            return cfg['cfdAccount']
        return cfg['ceAccount']


class Prt_BDA_AccountName(PortfolioAddInfo):

    _name = 'prt_BDA AccountName'

    @staticmethod
    def _is_relevant(prf, cfg):
        return cfg['cfdAccount'] and prf.Name() == cfg['cfdAccount']

    _get_value = staticmethod(lambda prf, cfg: cfg['cfdAccount'])


class MoPL_Population(PortfolioAddInfo):

    @staticmethod
    def _is_relevant(prf, cfg):
        parent = _get_parent_portfolio(prf)
        return parent.Name() in (
            get_portfolio_name_by_id("RISK_FV", cfg['shortName']),
            'PB_%s_FINANCING' % cfg['shortName'],
        )

    _get_value = staticmethod(lambda prf, cfg: 'Yes')


class Portfolio_Status(PortfolioAddInfo, AlwaysRelevant):

    _name = 'Portfolio Status'
    _get_value = staticmethod(lambda prf, cfg: 'Active')


class PS_SafexAccount(PortfolioAddInfo):

    @staticmethod
    def _is_relevant(prf, cfg):
        return prf.Name() in (
            get_portfolio_name(SAFEX, cfg['shortName'], cr=True),
            get_portfolio_name(YIELDX, cfg['shortName'], cr=True),
        )

    @staticmethod
    def _get_value(prf, cfg):
        if prf.Name() == get_portfolio_name(SAFEX, cfg['shortName'], cr=True):
            return get_callaccnt_name(cfg['shortName'], CALLACCNT_SAFEX)
        else:
            return get_callaccnt_name(cfg['shortName'], CALLACCNT_YIELDX)

## <--

def setup_addinfos(client_config):
    """
    Set up the additional infos for the client's Pending portfolios.
    """
    if client_config["dryRun"]:
        return

    query = acm.CreateFASQLQuery("FPhysicalPortfolio", "AND")
    op = query.AddOpNode("OR")
    op.AddAttrNodeString("AdditionalInfo.Portfolio_Status", "Pending", "EQUAL")
    op.AddAttrNodeString("AdditionalInfo.Portfolio_Status", "Active", "EQUAL")
    op = query.AddOpNode("OR")
    op.AddAttrNodeString("Name", client_config["cfdAccount"], "EQUAL")
    op.AddAttrNodeString("Name", PF_PREFIX_ACS + client_config["cfdAccount"], "EQUAL")
    op.AddAttrNodeString("Name", PF_PREFIX_BANK + client_config["cfdAccount"], "EQUAL")
    op.AddAttrNodeString("Name", "*" + client_config["shortName"] + "*", "RE_LIKE_NOCASE")
    result = query.Select()
    for pf in result:
        if pf.AdditionalInfo().Portfolio_Status() == "Active":
            LOGGER.warning("Changing add info on active portfolio!")
        acm.BeginTransaction()
        try:
            for addinfo in PortfolioAddInfo.get_descendants():
                addinfo.apply_(pf, client_config)
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            LOGGER.exception("Couldn't commit addinfos for portfolio {}".format(pf.Name()))
            raise e
