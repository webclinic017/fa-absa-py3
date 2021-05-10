"""
Sales Credit calculation for Corporate bonds.

HISTORY
============================================================================================================================
Date       	Change no    		Developer           	Description
----------------------------------------------------------------------------------------------------------------------------
2018-12-06	ABITFA-5637		Shalini Lala		Add sales person parameters		
----------------------------------------------------------------------------------------------------------------------------
"""

from SAFI_SalesCredit import BondSalesCreditGenerator
import acm
from at_logging import getLogger, bp_start

LOGGER = getLogger(__name__)


class CorporateBondsSalesCredit(BondSalesCreditGenerator):
    """Generator for corporate-issued bonds.

    This only overrides the calculation formula.

    """

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        """Add specific variables for corporate bonds sales credit."""
        (super(CorporateBondsSalesCredit, cls)
         ._populate_ael_variables(variables, defaults))
	
	variables.add('person1',
                      label='Sales Person Name 1',
                      mandatory=True,
                      default='ABRP358',
                      tab='Sales Allocations')
              
        variables.add('personRatio1',
                      label='Ratio for sales person 1',
                      mandatory=True,
                      default=0.4,
                      tab='Sales Allocations')
                      
        variables.add('person2',
                      label='Sales Person Name 2',
                      mandatory=False,
                      default='ABJR456',
                      tab='Sales Allocations')
        variables.add('personRatio2',
                      label='Ratio for sales person 2',
                      mandatory=False,
                      default=0.4,
                      tab='Sales Allocations')
                      
        variables.add('person3',
                      label='Sales Person Name 3',
                      mandatory=False,
                      default='BARENDSM',
                      tab='Sales Allocations')
        variables.add('personRatio3',
                      label='Ratio for sales person 3',
                      mandatory=False,
                      default=0.2,
                      tab='Sales Allocations')          
                      
        variables.add('person4',
                      label='Sales Person Name 4',
                      mandatory=False,
                      tab='Sales Allocations')
        variables.add('personRatio4',
                      default=0,
                      label='Ratio for sales person 4',
                      mandatory=False,
                      tab='Sales Allocations')

        variables.add('sector_default_basis_points',
                      label='Default basis points',
                      tab='Corporate bonds parameters',
                      default=5,
                      cls='float')
        variables.add('sector_financial_basis_points',
                      label='Basis points for Financial issuers',
                      tab='Corporate bonds parameters',
                      default=5,
                      cls='float')
        variables.add('sector_corporate_basis_points',
                      label='Basis points for Corporate issuers',
                      tab='Corporate bonds parameters',
                      default=5,
                      cls='float')
        variables.add('sector_municipal_basis_points',
                      label='Basis points for Municipal issuers',
                      tab='Corporate bonds parameters',
                      default=5,
                      cls='float')
        variables.add('sector_SOE_basis_points',
                      label='Basis points for SOE issuers',
                      tab='Corporate bonds parameters',
                      default=3,
                      cls='float')
        variables.add('sector_SOV_basis_points',
                      label='Basis points for SOV issuers',
                      tab='Corporate bonds parameters',
                      default=2,
                      cls='float')

    def __init__(self, save_trades,
                 log_results, result_output_path, result_output_file_name,
                 log_errors, error_output_path, error_output_file_name,
                 issuer_basis_points, default_basis_points):
        """Initialize the generator.

        issuer_basis_points -- a dictionary mapping issuers to basis points
        default_basis_points -- basis points for issuers without sectors

        """

        (super(CorporateBondsSalesCredit, self).
         __init__(result_output_path, result_output_file_name,
                  error_output_path, error_output_file_name))

        self._save_trades = save_trades
        self._log_results = log_results
        self._log_errors = log_errors
        self._issuer_basis_points = issuer_basis_points
        self._default_basis_points = default_basis_points

    def _calculate_sales_credit(self, trade):
        """Calculates the corporate bond credit sales."""

        # The delta values are per 1m, so the credit needs to be divided by 1m.
        factor = 0.000001

        instrument = trade.Instrument()

        if instrument.Issuer().Name() in self._issuer_basis_points:
            # This is a corporate bond.
            def_ctxt = acm.GetDefaultContext()
            calc_space = (acm.Calculations()
                          .CreateCalculationSpace(def_ctxt, 'FTradeSheet'))
            valuation_date = trade.TradeTime()
            calc_space.SimulateGlobalValue('Valuation Date', valuation_date)
            calc = calc_space.CalculateValue(trade, 'Instrument Spread Delta')

            # The trade quantity is already included in the delta.
            delta = calc.Value().Number()

            # If the issuer doesn't have a sector, use the default bp value.
            issuer_name = instrument.Issuer().Name()
            basis_points = (self._issuer_basis_points
                            .get(issuer_name, self._default_basis_points))
            LOGGER.debug("Trade: %s, basis points: %s, delta: %s, contract size: %s, factor: %s",
                         trade.Oid(), basis_points, delta, instrument.ContractSize(), factor)
            return (basis_points * delta * instrument.ContractSize() * factor)
        return 0


ael_variables = (CorporateBondsSalesCredit.ael_variables
                 (error_output_filename='SAFI_SalesCredit_Corp_Errors.txt',
                  result_output_filename='SAFI_SalesCredit_Corp_Results.csv'))


def ael_main(params):
    """Module to calculate the sales credit for
    FRNs, Bonds, IndexLinkedBonds."""
    
    with bp_start("safi.sales_credit_corp", ael_main_args=params):
        if params['start_date'] == 'Custom Date':
            start_date = params['start_date_custom']
        else:
            start_date = BondSalesCreditGenerator.START_DATES[params['start_date']]
    
        if params['end_date'] == 'Custom Date':
            end_date = params['end_date_custom']
        else:
            end_date = BondSalesCreditGenerator.END_DATES[params['end_date']]
    
        trade_filter = acm.FTradeSelection[params['trade_filter']]
    
        # Corporate Bonds constants.
        # Keys: sector oids. Values: basis points for SC calculation.
        sector_points_financial = (3942, params['sector_financial_basis_points'])
        sector_points_corporate = (3947, params['sector_corporate_basis_points'])
        sector_points_municipal = (3948, params['sector_municipal_basis_points'])
        sector_points_soe = (3946, params['sector_SOE_basis_points'])
        sector_points_sov = (3943, params['sector_SOV_basis_points'])
    
        issuer_sector_basis_points = [sector_points_financial,
                                      sector_points_corporate,
                                      sector_points_municipal,
                                      sector_points_soe,
                                      sector_points_sov]
    
        issuer_basis_points = {}
        query_text = 'free4ChoiceList = "{0}"'
        for (sector_name, sector_basis_points) in issuer_sector_basis_points:
            issuers = acm.FParty.Select(query_text.format(sector_name))
            issuer_names = [issuer.Name() for issuer in issuers]
    
            for issuer in issuer_names:
                issuer_basis_points[issuer] = sector_basis_points
    
        save_trades = params['save_trades']
    
        log_results = params['log_results']
        result_output_path = params['result_output_path'].SelectedDirectory()
        result_output_filename = params['result_output_filename']
    
        log_errors = params['log_errors']
        error_output_path = params['error_output_path'].SelectedDirectory()
        error_output_filename = params['error_output_filename']
    
        default_basis_points = params['sector_default_basis_points']
        generator = CorporateBondsSalesCredit(save_trades,
                                              log_results, result_output_path,
                                              result_output_filename,
                                              log_errors, error_output_path,
                                              error_output_filename,
                                              issuer_basis_points,
                                              default_basis_points)
    
        sales_person_filters = generator.getSalesSplit(params, 4)
        
        generator.calculate_sales_credit(start_date, end_date, trade_filter,
                                         sales_person_filters)
    
        # This only gets printed if nothing raises an exception.
        if generator.wrote_error_output:
            LOGGER.info("Wrote error output to %s", generator.full_error_output_path)
            LOGGER.info("Completed successfully.")
