"""
Sales Credit calculation for Govi bonds.

This should be further refactored later:
1) Move specific bond delta elsewhere (addinfo?).
2) Move hardcoded rules elsewhere.

HISTORY
============================================================================================================================
Date       	Change no    		Developer           	Description
----------------------------------------------------------------------------------------------------------------------------
2018-12-06	ABITFA-5637		Shalini Lala		Add sales person parameters
								Remove default delta values
								Change sales credit calculation method		
----------------------------------------------------------------------------------------------------------------------------
"""

from SAFI_SalesCredit import BondSalesCreditGenerator
import ael
import acm
from collections import defaultdict
from at_logging import getLogger, bp_start

LOGGER = getLogger(__name__)

calc_space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

class GovernmentBondsSalesCredit(BondSalesCreditGenerator):
    """Govi bond sales credit generating class.

    This is equivalent to the former SAFI_SalesCredit contents.

    """

    # Basis Points adjustment for instrument types.
    _instype_basis_points = {'Bond': 0.5, 'IndexLinkedBond': 1}

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        """Add specific variables for corporate bonds sales credit."""
        (super(GovernmentBondsSalesCredit, cls)
         ._populate_ael_variables(variables, defaults))
         
        variables.add('person1',
                      label='Sales Person Name 1',
                      mandatory=True,
                      default='ABJR456',
                      tab='Sales Allocations')
        variables.add('personRatio1',
                      label='Ratio for sales person 1',
                      mandatory=True,
                      default=1,
                      tab='Sales Allocations')
                      
        variables.add('person2',
                      label='Sales Person Name 2',
                      mandatory=False,
                      tab='Sales Allocations')
        variables.add('personRatio2',
                      default=0,
                      label='Ratio for sales person 2',
                      mandatory=False,
                      tab='Sales Allocations')

        for instype, basis_points in \
                GovernmentBondsSalesCredit._instype_basis_points.items():
            variables.add('basis_point_adjustment_{0}'.format(instype),
                          label=('Basis point adjustment for {0}'
                                 .format(instype)),
                          tab='Government bonds parameters',
                          default=basis_points,
                          cls='float')


    def _choose_sales_person(self, trade, sales_persons):
        portfolio = trade.Portfolio().Name()
        if (portfolio == 'JOB11' or portfolio == 'DERV3'):
            if 'ABJR456' in sales_persons:
                return 'ABJR456'                
        else:
            return (super(GovernmentBondsSalesCredit, self)
                    ._choose_sales_person(trade, sales_persons))
                
    
    def _add_info_psd(self, trade):
        """Further filtering based on business requirements."""

        if trade.Counterparty().Name() == 'PRIME SERVICES DESK':
            trade.AdditionalInfo().Relationship_Party('MARBLE ROCK H4 ROCKSOLID FI QIF')
            
            trade.Commit()
            
            return trade
    
            

    def __init__(self, save_trades,
                 log_results, result_output_path, result_output_file_name,
                 log_errors, error_output_path, error_output_file_name,
                 basis_point_adjustment):
        (super(GovernmentBondsSalesCredit, self)
         .__init__(result_output_path, result_output_file_name,
                   error_output_path, error_output_file_name))

        self._save_trades = save_trades
        self._log_results = log_results
        self._log_errors = log_errors
        self._basis_point_adjustment = basis_point_adjustment
        
    
    def _delta(self, trade):
        """Calculate the maturity and lookup the sales credit."""

        calc = trade.Calculation().InterestRateBenchmarkDelta(calc_space)
        delta = calc.Number()
        
        return delta


    def _calculate_sales_credit(self, trade):
        """ Calculate the govi bond sales credit.

        The trade has already passed all validations.

        """
        instrument = trade.Instrument()
        
        LOGGER.debug("Trade: %s, contract size: %s, quantity: %s, delta: %s, factor: %s, basis points adj: %s",
                         trade.Oid(), trade.Quantity(), self._delta(trade), 
                         self._basis_point_adjustment[instrument.InsType()])
        
        return (self._delta(trade) * self._basis_point_adjustment[instrument.InsType()])
        

ael_variables = (GovernmentBondsSalesCredit
                 .ael_variables
                 (error_output_filename='SAFI_SalesCredit_Govi_Errors.txt',
                  result_output_filename='SAFI_SalesCredit_Govi_Results.csv'))


def ael_main(params):
    with bp_start("safi.sales_credit_govi", ael_main_args=params):
        if params['start_date'] == 'Custom Date':
            start_date = params['start_date_custom']
        else:
            start_date = BondSalesCreditGenerator.START_DATES[params['start_date']]
    
        if params['end_date'] == 'Custom Date':
            end_date = params['end_date_custom']
        else:
            end_date = BondSalesCreditGenerator.END_DATES[params['end_date']]
    
        trade_filter = acm.FTradeSelection[params['trade_filter']]
    
        # Govibond-specific variables.
        basis_point_adjustment = {}
        for instype in GovernmentBondsSalesCredit._instype_basis_points:
            basis_point_adjustment[instype] = \
                params['basis_point_adjustment_{0}'.format(instype)]
    
        save_trades = params['save_trades']
    
        log_results = params['log_results']
        result_output_path = params['result_output_path'].SelectedDirectory()
        result_output_filename = params['result_output_filename']
    
        log_errors = params['log_errors']
        error_output_path = params['error_output_path'].SelectedDirectory()
        error_output_filename = params['error_output_filename']
    
        generator = GovernmentBondsSalesCredit(save_trades,
                                               log_results, result_output_path,
                                               result_output_filename,
                                               log_errors, error_output_path,
                                               error_output_filename,
                                               basis_point_adjustment)
                                               
        sales_person_filters = generator.getSalesSplit(params, 2)
        generator.calculate_sales_credit(start_date, end_date, trade_filter, sales_person_filters)
    
        # This only gets printed if nothing raises an exception.
        if generator.wrote_error_output:
            LOGGER.info("Wrote error output to %s", generator.full_error_output_path)
        LOGGER.info("Completed successfully.")
