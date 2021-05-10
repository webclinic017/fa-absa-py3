"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Introduce product classes used by PS_MO_Onboarding.py.
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
2018-10-12                  Tibor Reiss           No financed MONEYMARKET

"""


class AssetClass(object):
    _instances = []

    def __init__(self, **kwargs):
        """
        Create a new asset class (in the context of Python, it is an instance).

        You can specify the following attributes:

        <key> - Unique ID of the class, used in ael_variables.
        <verbose_name> - Name to be shown in the GUI.
        <portfolio_infix> - Asset-related part of portfolio name.
        <pswap_suffix> - Asset-related part of portfolioswap name.
        <index_suffix> - Asset-related part of the rate index name.
        <financed> - Is this asset class traded in the "financed" mode?
        <fullyfunded> - Is this asset class traded in the "fullyfunded" mode?
        <risk> - Is this asset class traded in the "risk" mode?
        <equities> - Does the asset class fall into the "Equities" category?
        <fixed_income> - Does the asset class fall into the "Fixed Income" category?

        """
        required = ['key', 'verbose_name', 'portfolio_infix', 'pswap_suffix',
                    'index_suffix']
        if not set(kwargs.keys()).issuperset(set(required)):
            msg = 'Some of the following arguments are missing: %s' % required
            raise ValueError(msg)
        attrs = {'financed': False, 'fullyfunded': False, 'risk': False,
                 'equities': False, 'fixed_income': False}
        attrs.update(kwargs)  # Overwrite defaults with specified values.
        self.__dict__.update(attrs)  # Make the attributes easily accessible.
        self._instances.append(self)

    @classmethod
    def get(cls, key):
        try:
            return [ac for ac in cls._instances if ac.key == key][0]
        except IndexError:
            raise KeyError('Unknown asset class with key: %s' % key)

    @classmethod
    def get_all(cls):
        return cls._instances[:]

    @classmethod
    def get_fullyfunded(cls):
        return [ac for ac in cls._instances if ac.fullyfunded]

    @classmethod
    def get_financed(cls):
        return [ac for ac in cls._instances if ac.financed]

    @classmethod
    def get_risk(cls):
        return [ac for ac in cls._instances if ac.risk]

    @classmethod
    def get_equities(cls):
        return [ac for ac in cls._instances if ac.equities]

    @classmethod
    def get_fixed_income(cls):
        return [ac for ac in cls._instances if ac.fixed_income]


# Now declare all the asset classes

CASH_EQUITY = AssetClass(
    key='cashEquity',
    verbose_name='Cash Equity',
    portfolio_infix='CE',
    pswap_suffix='CE',
    index_suffix='CE',
    financed=True,
    fullyfunded=True,
    equities=True,
    sweeping_class='Cash equity',
)

CFD = AssetClass(
    key='cfd',
    verbose_name='CFD',
    portfolio_infix='CFD',
    pswap_suffix='CFD',
    index_suffix='CFD',
    risk=True,
    equities=True,
    sweeping_class='CFDs',
)

COMMODITIES = AssetClass(
    key='commodities',
    verbose_name='Commodities',
    portfolio_infix='AGRIS',
    pswap_suffix='APD',
    index_suffix='APD',
    financed=True,
    sweeping_class='Commodities',
)

CORPBONDS = AssetClass(
    key='corpBonds',
    verbose_name='Credit - Corporate Bonds',
    portfolio_infix='CORPBOND',
    pswap_suffix='CORPBOND',
    index_suffix='CORPBOND',
    financed=True,
    fullyfunded=True,
    fixed_income=True,
    sweeping_class='Corporate bonds',
)

FRA = AssetClass(
    key='fra',
    verbose_name='FRA',
    portfolio_infix='FRA',
    pswap_suffix='FRA',
    index_suffix='FRA',
    risk=True,
    fixed_income=True,
    sweeping_class='FRAs',
)

GOVIBONDS = AssetClass(
    key='bonds',
    verbose_name='Bonds',
    portfolio_infix='GOVIBOND',
    pswap_suffix='GOVIBOND',
    index_suffix='GOVIBOND',
    financed=True,
    fullyfunded=True,
    fixed_income=True,
    sweeping_class='Government bonds',
)

IRS = AssetClass(
    key='irs',
    verbose_name='IRS',
    portfolio_infix='IRS',
    pswap_suffix='IRS',
    index_suffix='IRS',
    risk=True,
    fixed_income=True,
    sweeping_class='Swaps',
)

MONEYMARKET = AssetClass(
    key='moneyMarket',
    verbose_name='Money Market',
    portfolio_infix='MONEYMARKET',
    pswap_suffix='MONEYMARKET',
    index_suffix='MONEYMARKET',
    fullyfunded=True,
    financed=False,
    fixed_income=True,
    sweeping_class='Money market',
)

OTC_FI = AssetClass(
    key='otcFIOptions',
    verbose_name='OTC FI Options',
    portfolio_infix='OPTION_FI',
    pswap_suffix='OTCFIOPT',
    index_suffix='OTCFIOPT',
    risk=True,
    fixed_income=True,
    sweeping_class='FI Options',
)

SAFEX = AssetClass(
    key='safex',
    verbose_name='SAFEX',
    portfolio_infix='SAFEX',
    pswap_suffix='SAFEX',
    index_suffix=None,
    financed=True,
    equities=True,
    sweeping_class='SAFEX exchange',
)

YIELDX = AssetClass(
    key='yieldx',
    verbose_name='YIELDX',
    portfolio_infix='YIELDX',
    pswap_suffix='YIELDX',
    index_suffix=None,
    financed=True,
    fixed_income=True,
    sweeping_class='YieldX exchange',
)
