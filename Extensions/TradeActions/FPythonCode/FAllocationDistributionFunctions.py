"""----------------------------------------------------------------------------
    
    MODULE: FAllocationDistributionFunctions
    
    DESCRIPTION: 
    Trade allocation distribution functions.

----------------------------------------------------------------------------"""
import acm
import FLogger
import math

logger = FLogger.FLogger.GetLogger('Allocation')
# Level 2 is debug
logger.Reinitialize(level=1, logToPrime=True)

sheet_type = 'FPortfolioSheet'
context = acm.GetDefaultContext()
cs = acm.Calculations().CreateCalculationSpace(context, sheet_type)


def pro_rata(rule, trade):
    default_distribution_function(rule, trade, relative_bucket_weight_amounts, default_round_amount, default_handle_residual)
    

def percent_of_nav(rule, trade):
    default_distribution_function(rule, trade, net_asset_value_column_amounts, default_round_amount, default_handle_residual)

'''
Distribution functions can solve their task by whatever means necessary, as long as the sum of the allocated quantities is 
exactly the same as the original quantity. However, it will often be the case that you want to reuse the basic work flow
of Pro Rata or Percent of NaV, but override rounding or residual handling (or use a column other than NaV).

Here is an example of how to create a custom distribution function that has different (instrument-dependent) rounding behavior by passing
a custom rounding function callback to the default Pro Rata flow:


[MYUSER]FObject:MyAllocationDistributionFunctions 

def my_custom_distribution_function(rule, trade):
    default_distribution_function(rule, trade, relative_bucket_weight_amounts, custom_round_amount, default_handle_residual)
    
def custom_round_amount(rule, trade, raw_amount):
    if trade.Instrument().Class() == acm.FCurrency:
        return round(raw_amount, 2)
    else:
        return round(raw_amount, 0)
        
and an FAllocationDefinition:        

[MYUSER]FObject:My Custom Distribution Function =
  Function=MyAllocationDistributionFunctions.my_custom_distribution_function
  StaticWeights=true

'''

def default_round_amount(rule, trade, raw_amount):
    # Truncate towards zero, so 
    #  1.3 => 1
    # -1.3 => -1
    if raw_amount < 0:
        return math.ceil(raw_amount)
    else:
        return math.floor(raw_amount)

def default_handle_residual(rule, trade, residual):    
    if trade.Quantity() * residual >= 0:
        # Same sign: residual is added to bucket of LOWEST sort order
        bucket = rule.ChildBucketsSorted().First()
    else:
        # Opposite signs: residual is added to bucket of HIGHEST sort order
        bucket = rule.ChildBucketsSorted().Last()
    
    bucket.Drop(residual)
    logger.debug('Dropped residual %f into bucket %s', residual, bucket.Name())

def default_distribution_function(rule, trade, amounts_collector_func, rounding_func, residual_handling_func):
    amount_to_allocate = rule.AvailableAmount()

    raw_amounts = amounts_collector_func(rule, amount_to_allocate)
    rounded_amounts = [rounding_func(rule, trade, raw_amount) for raw_amount in raw_amounts]

    for i, amount in enumerate(rounded_amounts):
        bucket = rule.ChildBuckets().At(i)
        bucket.Drop(amount)
        logger.debug('Dropped %f into bucket %s', amount, bucket.Name())

    residual = amount_to_allocate - math.fsum(rounded_amounts)
    logger.debug('Residual: %f', residual)
    
    residual_handling_func(rule, trade, residual)

def relative_bucket_weight_amounts(rule, amount_to_allocate):
    amounts = []
    for bucket in rule.ChildBuckets():
        amount = rule.RelativeWeightOf(bucket) * amount_to_allocate
        amounts.append(amount)
    return amounts

def net_asset_value_column_amounts(rule, amount_to_allocate):        
    return by_column_amounts(rule, amount_to_allocate, 'Portfolio Net Asset Value')

def by_column_amounts(rule, amount_to_allocate, column_id):        
    # This DF only works for portfolios
    bc = rule.Dimension().BackingClass()
    if bc and not bc.IsSubtype(acm.FPortfolio):
        raise Exception('Dimension ' + str(rule.Dimension().BackingClass().Name()) + ' not supported')

    total = 0
    weight_by_portfolio = {}
    for bucket in rule.ChildBuckets():
        portfolio = bucket.Dimension()
        cval = calculate_column_value(portfolio.Name(), column_id)
        if math.isnan(cval):
            raise Exception('Column %s in portfolio %s is NaN' % (column_id, portfolio.Name()))
        else:
            weight_by_portfolio[portfolio] = cval
            total += cval
    
    amounts = []
    for bucket in rule.ChildBuckets():
        if total != 0:
            share = weight_by_portfolio[bucket.Dimension()] / total
        else:
            share = 0
        amount = share * amount_to_allocate
        amounts.append(amount)

    return amounts

def calculate_column_value(portfolio_name, column_id):
    portfolio = acm.FPhysicalPortfolio[portfolio_name]
    if portfolio:
        node = cs.InsertItem(portfolio)
        cs.Refresh()
        calc = cs.CreateCalculation(node, column_id)
        val = calc.Value().Number()
        return val
    else:
        return 0
