"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2018-10-02                  Reiss Tibor           Initial implementation

Building the GUI.
"""


import re

import acm

from at_ael_variables import AelVariableHandler
from PS_AssetClasses import (AssetClass,
                             CASH_EQUITY,
                             CFD,
                             COMMODITIES,
                             SAFEX,
                             YIELDX)


SHORT_NAME_MAX_LENGTH = 9  # Fit into all the necessary columns (Portfolio name, etc.)

#TODO: change ael variable names to snake case, e.g. shortName to short_name
class ConfigDict(dict):
    """
    This class preprocesses and validates the ael parameters.
    For new a rule create a new function starting with check_.
    The function should return True/False and the error message
    as string.
    """

    def check_short_name_already_taken(self):
        check = acm.FPartyAlias.Select("type = 'SoftBroker' "
                "AND alias='%s'" % self['shortName']).Size() > 1
        msg = 'The short name chosen ({}) is already taken'.format(
              self['shortName'])
        return (check, msg)

    def check_counterparty_not_trading(self):
        check = self['counterparty'].NotTrading()
        msg = 'The chosen party ({0}) is non-trading.'.format(
              self['counterparty'].Name())
        return (check, msg)

    def check_no_special_characters_used(self):
        check = not re.match(r'^[a-zA-Z0-9_]*$', self['shortName'])
        msg = ("Forbidden characters in client's short name - please only use "
               "English alphabet characters, numbers and the underscore.")
        return (check, msg)

    def check_short_name_too_long(self):
        check = len(self['shortName']) > SHORT_NAME_MAX_LENGTH
        msg = ("Client's short name must be "
               "at most {} characters long.").format(SHORT_NAME_MAX_LENGTH)
        return (check, msg)

    def check_no_product_selected(self):
        traded_products = [asset_class for asset_class in AssetClass.get_all()
                           if self[asset_class.key]]
        check  = not traded_products
        msg = ('You need to specify at least one product type '
               'for the client to trade.')
        return (check, msg)

    def check_cfd_account(self):
        check = self[CFD.key] and not self['cfdAccount']
        msg = ('A CFD Hedge Equity Account has to be specified '
               'for a CFD-trading client.')
        return (check, msg)

    def check_cfd_for_rtm(self):
        check = (self[CFD.key] and
                    (not self["startDate"]
                     or not self["cfdAccount"]
                     or not self["shortName"])
                 )
        msg = ('For a CFD-trading client the start date, '
               'cfd account and short name must be specified.')
        return (check, msg)

    def check_ce_account(self):
        check = self[CASH_EQUITY.key] and not self['ceAccount']
        msg = ('For a Cash Equity trading client a CE stock '
               'account has to be specified.')
        return (check, msg)

    def check_commodities_account(self):
        msg = ('For a Commodities-trading client the following '
               'Commodities-specific parameters need to be specified: '
               'external account ID, rate index and spread.')
        check = (self[COMMODITIES.key] and
                    (not self['commoditiesCallAccountCode']
                     or self['commoditiesCallAccountRateIndex'] is None
                     or self['commoditiesCallAccountSpread'] is None)
                )
        return (check, msg)

    def check_safex_account(self):
        msg = ('For a SAFEX-trading client the following '
               'SAFEX-specific parameters need to be specified: '
               'external account ID, rate index and spread.')
        check = (self[SAFEX.key] and
                    (not self['safexCallAccountCode']
                     or self['safexCallAccountRateIndex'] is None
                     or self['safexCallAccountSpread'] is None)
                )
        return (check, msg)

    def check_yieldx_account(self):
        check = (self[YIELDX.key] and
                    (not self['yieldxCallAccountCode']
                     or self['yieldxCallAccountRateIndex'] is None
                     or self['yieldxCallAccountSpread'] is None)
                )
        msg = ('For a YIELDX-trading client the following '
               'YIELDX-specific parameters need to be specified: '
               'external account ID, rate index and spread.')
        return (check, msg)

    def validate(self):
        errors = []
        for func in [x for x in ConfigDict.__dict__.values() if callable(x)]:
            if func.__name__.startswith("check_"):
                (check, msg) = func(self)
                if check:
                    errors.append(msg)
        if errors:
            raise ValidationError('\n'.join(errors))

    def preprocess(self):
        """
        Perform initial preprocessing of the GUI parameter values.
        Note: Whitespace is stripped from the GUI input automatically.
        """
        for key, val in self.iteritems():
            # Convert 'Yes'/'No' to proper booleans.
            if val == 'Yes':
                self[key] = True
            elif val == 'No':
                self[key] = False
            # Get rid of rounding errors
            # introduced in Prime's GUI parameter processing.
            if isinstance(val, float):
                self[key] = float('%.5g' % val)


class ValidationError(Exception):
    pass


def short_name_hook(counterparty):
    """Use short name from the party definition."""
    short_name = counterparty.handler.get('shortName')
    party = acm.FParty[counterparty.value]
    if party is None:
        short_name.value = None
    else:
        short_name.value = party.Alias('SoftBroker')


def get_main_config():
    """
    Return AelVariableHandler populated with
    the ael variables for the main tab.
    """
    handler = AelVariableHandler()
    handler.add('counterparty',
                label='Client Party',
                cls='FParty',
                collection=acm.FParty.Select('').SortByProperty('Name'),
                hook=short_name_hook)
    handler.add('shortName',
                label='Client Short Name',
                alt="Client's short name to be used in portfolio name building.",
                enabled=False)
    handler.add('startDate',
                label='Start Date',
                cls='date',
                default=acm.Time.DateToday(),
                alt='Start date of the PortfolioSwaps and Call Loans/Deposits.')
    handler.add('cfdAccount',
                label='CFD Hedge Equity Account',
                mandatory=False)
    handler.add('ceAccount',
                label='CE Stock Account',
                mandatory=False)
    handler.add_bool('fundAllocations',
                     label='Fund Allocations',
                     default=False)
    handler.add_bool('sblAgreement',
                     label='SBL Agreement',
                     default=False)
    handler.add_bool('dualListed',
                     label='Dual Listed',
                     default=False,
                     alt='If checked, dual listed arb margin policy will be applied.')
    handler.add_bool('dryRun',
                     label='Dry Run',
                     default=True,
                     alt=('If checked, do a dry run only - i.e. '
                          'do not save anything to the DB.'))
    return handler


def get_product_types_config():
    """
    Return AelVariableHandler populated with
    the ael variables for the product types tab.
    """
    handler = AelVariableHandler()
    for asset_class in AssetClass.get_all():
        handler.add_bool(asset_class.key,
                         label=asset_class.verbose_name,
                         default=False,
                         tab='Product Types')
    return handler


def get_pswaps_config():
    """
    Return AelVariableHandler populated with
    the ael variables for the portfolio swaps tab.
    """
    handler = AelVariableHandler()
    for asset_class in AssetClass.get_all():
        handler.add('%s_premium' % asset_class.key,
                    label=asset_class.verbose_name,
                    cls='float',
                    default=0.0,
                    tab='SBL Fee')
    return handler


def get_pswaps_rate_bid_ask_config():
    """
    Return AelVariableHandler populated with
    the ael variables for the portfolio swaps bid and ask rate tab.

    These are rates for long/short position funding.
    """
    handler = AelVariableHandler()
    for asset_class in AssetClass.get_all():
        if asset_class in (SAFEX, YIELDX):
            # These two use already existing rate indices.
            continue
        handler.add('%s_bid_rate' % asset_class.key,
                    label='%s bid Rate index rate' % asset_class.verbose_name,
                    cls='float',
                    default=0.0,
                    tab='Overnight funding')
        handler.add('%s_ask_rate' % asset_class.key,
                    label='%s ask Rate index rate' % asset_class.verbose_name,
                    cls='float',
                    default=0.0,
                    tab='Overnight funding')
    return handler


def get_call_accounts_config():
    """
    Return AelVariableHandler populated with
    the ael variables for the call accounts tab.
    """
    handler = AelVariableHandler()
    handler.add('generalCallAccountRateIndex',
                label='General call account rate index',
                default='ZAR-SABOR',
                alt='Rate index of the general call account',
                tab='Call Accounts')
    handler.add('generalCallAccountSpread',
                label='General call account rate spread',
                cls='float',
                default=-0.4,
                alt='Spread on the general call account rate',
                tab='Call Accounts')
    handler.add('commoditiesCallAccountRateIndex',
                label='Commodities call account rate index',
                default='ZAR-SAFEX-ON-DEP',
                mandatory=False,
                alt='Rate index of the commodities call account',
                tab='Call Accounts')
    handler.add('commoditiesCallAccountSpread',
                label='Commodities call account rate spread',
                cls='float',
                default=0.2,
                mandatory=False,
                alt='Spread on the commodities call account rate',
                tab='Call Accounts')
    handler.add('commoditiesCallAccountCode',
                label='Commodities call account code',
                mandatory=False,
                alt='External ID of the commodities call account',
                tab='Call Accounts')
    handler.add('safexCallAccountRateIndex',
                label='SAFEX call account rate index',
                default='ZAR-SAFEX-ON-DEP',
                mandatory=False,
                alt='Rate index of the SAFEX call account',
                tab='Call Accounts')
    handler.add('safexCallAccountSpread',
                label='SAFEX call account rate spread',
                cls='float',
                default=0.2,
                mandatory=False,
                alt='Spread on the SAFEX call account rate',
                tab='Call Accounts')
    handler.add('safexCallAccountCode',
                label='SAFEX call account code',
                mandatory=False,
                alt='External ID of the SAFEX call account',
                tab='Call Accounts')
    handler.add('yieldxCallAccountRateIndex',
                label='YIELDX call account rate index',
                default='ZAR-SAFEX-ON-DEP',
                mandatory=False,
                alt='Rate index of the YIELDX call account',
                tab='Call Accounts')
    handler.add('yieldxCallAccountSpread',
                label='YIELDX call account rate spread',
                cls='float',
                default=0.2,
                mandatory=False,
                alt='Spread on the YIELDX call account rate',
                tab='Call Accounts')
    handler.add('yieldxCallAccountCode',
                label='YIELDX call account code',
                mandatory=False,
                alt='External ID of the YIELDX call account',
                tab='Call Accounts')
    return handler


def get_fees_config():
    """
    Return AelVariableHandler populated with
    the ael variables for the various fees tabs.
    """
    handler = AelVariableHandler()
    fee_types = [('DMA', 'Done with dma'),
                 ('Voice', 'With desk voice'),
                 ('NonDMA', 'Done away od')]
    for asset_class in AssetClass.get_all():
        for (short_type, verbose_type) in fee_types:
            handler.add('%s_%s_fee' % (asset_class.key, short_type),
                        label=asset_class.verbose_name,
                        cls='float',
                        default=0.0,
                        alt='Insert as percentage points.',
                        tab=verbose_type)
    # Field used in execution fee calculation for commodities
    handler.add('CommoditiesExecFee',
                label="Commodities Exec Fee",
                cls='float',
                default=0.0,
                alt='Insert as percentage points.',
                tab='Done with dma')
    return handler
