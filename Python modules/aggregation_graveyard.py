import ael, acm
from aggregation import TradeAggregation, TradeArchivist, LOG, AggregationConfig
from SAGEN_IT_Functions import get_Port_Struct_from_Port as check_portfolio_parent
import at_dbsql

GRAVEYARD_NAME = 'GRAVEYARD'

def get_physical_portfolios(portfolio_name):
    portfolio = acm.FPhysicalPortfolio[portfolio_name]
    if portfolio.Compound():
        return portfolio.AllPhysicalPortfolios()
    return [portfolio]

class GraveyardAggregationConfig(AggregationConfig):
    CONFIG_NAME_TPL = 'GraveyardAggregation_{0}'

class GraveyardAggregation(TradeAggregation):

    AGGREGATION_TYPE = 'trade_graveyard'
    CONFIG_CLASS = GraveyardAggregationConfig

    @classmethod
    def add_ael_variables(cls, ael_variables):
        ael_variables.add(cls._type_prefix('include_prfs'),
                        'Include portfolios (compound)_Graveyard Trades',
                        multiple=True,
                        collection=acm.FCompoundPortfolio.Select(''))
        ael_variables.add(cls._type_prefix('exclude_prfs'),
                        'Exclude portfolios (compound)_Graveyard Trades',
                        multiple=True,
                        collection=acm.FPhysicalPortfolio.Select(''))


    def set_ael_variable_values(self, ael_variables):
        var_include_portfolios = ael_variables.get(self._type_prefix('include_prfs'))
        var_exclude_portfolios = ael_variables.get(self._type_prefix('exclude_prfs'))
        var_include_portfolios.value = self.config['aggregate_portfolios']
        var_exclude_portfolios.value = self.config['aggregate_portfolios_exclude']

    def get_values_from_ael_params(self, params):
        return [params[self._type_prefix(param)] for param in ('include_prfs', 'exclude_prfs')]

    @staticmethod
    def _get_trade_numbers(portfolio_names):
        query = """
        SELECT trdnbr
        FROM trade
        WHERE archive_status = 0
        AND aggregate = 0
        AND prfnbr IN {0}
        """
        res = ael.dbsql(query.format(at_dbsql.portfolio_ids(portfolio_names)))

        return [int(trdnbr[0]) for trdnbr in res[0]]

    def setup(self, portfolio_names_compound, exclude_portfolio_names_compound):
        """Sets the entities of the aggregations (i.e. trades).

        This must be called before any operations can be performed on the object.

        """

        # Process the portfolio names.
        exclude_portfolio_names= [p.Name()
                for parent_prf in exclude_portfolio_names_compound
                for p in get_physical_portfolios(parent_prf)]

        self._include_portfolio_names = [p.Name()
                for parent_prf in portfolio_names_compound
                for p in get_physical_portfolios(parent_prf)
                if not p.Name() in exclude_portfolio_names]

        self._trade_numbers = self._get_trade_numbers(self._include_portfolio_names)

        # Load the trades for archiving.
        self._entities = [ael.Trade[trdnbr] for trdnbr in self._trade_numbers]

        self._trade_chunks = self._chunkify(self._entities)
        self._archivists = [GraveyardArchivist(chunk,
            self._log) for chunk in self._trade_chunks]
        self._initialized = True
        self.config['aggregate_portfolios'] = ','.join(self._include_portfolio_names)
        self.config['aggregate_portfolios_exclude'] = ','.join(exclude_portfolio_names)


    def _check_inputs(self):
        """Check that the portfolios are under GRAVEYARD."""
        self.errors = []
        for name in self._include_portfolio_names:
            portfolio = ael.Portfolio[name]
            if not portfolio:
                self.errors.append("Portfolio {0} not found.".format(name))
                continue

            if not check_portfolio_parent(portfolio, GRAVEYARD_NAME):
                self.errors.append("Portfolio {0} is not under {1}".format(name, GRAVEYARD_NAME))

        return not self.errors

    def _prepare(self):
        """No need for preparation with GRAVEYARD aggregation."""


    def _cancel(self):
        """No need for cancelling since there is no preparation."""


    def _reset(self):
        """Reset is not possible for GRAVEYARD aggregation."""
        raise self.GeneralError("Reset is not possible for GRAVEYARD aggregation.")


    def _finalize(self):
        """No finalization needed - no aggregate trades are present."""

class GraveyardArchivist(TradeArchivist):
    """Graveyard-specific trade chunk archivist."""
    def __init__(self, entities, log=LOG):
        """Initialize with the input files."""
        super(GraveyardArchivist, self).__init__(entities, None)

    def _check_entity(self, trade):
        """Worker checking one trade."""
        errors = []

        if trade.archive_status != 0:
            errors.append("Trade {0} is already archived.".format(trade.trdnbr))

        return errors

    def _archive_entity(self, trade):
        """Archive the trade."""
        trade_clone = trade.clone()
        if self._set_entity_archived(trade_clone, archive_flag=True):
            trade_clone.commit()

    def _unarchive_entity(self, trade):
        """No unarchiving is to be done - this is a one way process only."""

    def _rollback_entities(self):
        """No rollback is allowed - this is a one-way process only."""

