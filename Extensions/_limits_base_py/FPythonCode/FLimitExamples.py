""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitExamples.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FLimitExamples

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Example code for how to perform actions programmatically using 
    the Limits Management framework.

    NOTE: Classes, methods and functions outside of the (public) ACM 
          library are subject to change without notice.

-----------------------------------------------------------------------------"""
import acm


def _PreventCall():
    # All functions in this module are not meant to be executed
    assert False, 'This function is for documentation purposes only. ' \
            'It will not work without prior modification and should ' \
            'not be called directly.'


def FindLimits():
    """Find FLimit objects.

    The following example shows how limits associated with a certain
    object (e.g. a trade) can be found in the system.

    """
    _PreventCall()

    # Limits pertaining to a particular trade can be found using the
    # FindByTrade function in the Limits namespace. 
    # In this case, searching across all limits in the system can take 
    # time, so a list of limits may optionally be passed in to check
    # against a smaller filtered subset.
    trade = acm.FTrade[1]
    query = acm.CreateFASQLQuery('FLimit', 'AND')
    query.AddAttrNode('Owner.Name', 'RE_LIKE_NOCASE', acm.User().Name())
    myLimits = query.Select()
    limits = acm.Limits.FindByTrade(trade, myLimits)
    for l in limits:
        print(l.Oid())

    # Limits on a similar row object to another limit can be found by
    # searching for limits based on TreeSpecification
    l = acm.FLimit[1]
    treeSpec = l.LimitTarget().TreeSpecification()
    limits = acm.Limits.FindByTreeSpecification(treeSpec)
    for l in limits:
        print(l.Oid())

    # From the Trading Manager, limits for the current row object
    # (FInstrumentAndTrades) can be found with the following function
    rowObject = acm.FInstrumentAndTrades() # e.g. from extension attribute
    limits = acm.Limits.FindByInstrumentAndTrades(rowObject)
    for l in limits:
        print(l.Oid())

def LimitProperties():
    """Accessing FLimit common properties.

    The following example shows how common attributes of the limit
    can be accessed.

    """
    _PreventCall()

    # Limits can be accessed like any other ACM object. Refer to the 
    # FindLimits() example for specialised ways of accessing them.
    limit = acm.FLimit[1]

    # The limit specification contains some categorisation information
    # and behavioural settings
    limitSpec = limit.LimitSpecification()
    print('Limit specification:', limitSpec.Name())
    print('Limit type:', limitSpec.LimitType().Name())
    print('Monitored in realtime?', limitSpec.RealtimeMonitored())

    # The limit target contains information on the limited calculation
    limitTarget = limit.LimitTarget()
    print('Target path:', limitTarget.Path())
    print('Column calculation:', limitTarget.ColumnLabel())

    # Some basic properties on the limit itself
    print('Is a parent limit?', limit.IsParent())
    print('Threshold value:', limit.Threshold())

    # The current state is determined by the business process
    print('Current state:', limit.BusinessProcess().CurrentStep().State().Name())

    # The latest checked calculated value is on the limit value object
    print('Last checked value:', limit.LimitValue().CheckedValue())

def CreateLimits():
    """Create FLimit objects programmatically.

    The following example shows how limits can be programmatically
    created using the Arena Calculation Interface (ACI). Refer to
    FCA 4102 "Developer Guide: Programmatic Access to Calculated
    Values" for more information about this API.

    """
    _PreventCall()

    # Prepare the calculation space, inserting the item (e.g.
    # portfolio, ASQL query, etc) to be limited in to a supported
    # sheet type. Apply any necessary grouping.
    calcSpace = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 'FPortfolioSheet')
    portfolio = acm.FPhysicalPortfolio['MY PORTFOLIO']
    node = calcSpace.InsertItem(portfolio)
    calcSpace.Refresh()

    # Create an FCalculation for the cell producing the calculation
    # to be limited. From this, an FLimitTarget can be produced.
    calculation = calcSpace.CreateCalculation(
            node, 'Portfolio Theoretical Value')
    limitTarget = acm.Limits.CreateLimitTarget(calculation)

    # An FLimitSpecification is needed to create the limit
    limitSpec = acm.FLimitSpecification['MY SPEC']
    limit = limitSpec.CreateLimit(limitTarget)

    # Set the attributes for the limit and commit it
    limit.ComparisonOperator('Greater or Equal')
    limit.Threshold(calculation.Value() * 1.5)
    limit.PercentageWarning(True)
    limit.WarningValue(5)
    limit.Commit()

def CreateParentLimits():
    """Create parent FLimit objects programmatically.

    The following example shows how parent limits --limits which
    result in an automatically created child limit under it in
    the calculation tree-- are created using the Arena Calculation
    Interface (ACI).

    """
    _PreventCall()

    # Prepare the calculation space, inserting the item (e.g.
    # portfolio, ASQL query, etc) to be limited in to a supported
    # sheet type.
    calcSpace = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 'FPortfolioSheet')
    portfolio = acm.FPhysicalPortfolio['MY PORTFOLIO']
    node = calcSpace.InsertItem(portfolio)
    calcSpace.Refresh()

    # Apply the grouper required to create the calculation tree,
    # including the nodes for which child limits will apply
    grouper = acm.FChainedGrouper([
            acm.Risk.GetGrouperFromName('Currency'),
            acm.Risk.GetGrouperFromName('Instrument Type'),
            acm.Risk.GetGrouperFromName('Issuer'),])
    node.ApplyGrouper(grouper)
    calcSpace.Refresh()

    # Browse down to where the limit cell will be located in the
    # tree (e.g. the first available currency)
    node = node.Iterator().FirstChild().Tree()

    # Create an FCalculation for the cell producing the calculation
    # to be limited. From this, an FLimitTarget can be produced.
    calculation = calcSpace.CreateCalculation(
            node, 'Portfolio Theoretical Value')
    limitTarget = acm.Limits.CreateLimitTarget(calculation)

    # The SubLevel attribute on the limit target will determine
    # if the limit will be a parent limit (SubLevel > 0) and where
    # the child limits will be created. It must specify the number
    # of sub-levels the child cells are below the parent limit
    # in the calculation tree.
    #
    # For example, in our example portfolio and grouping: 
    #
    # Lvl-1  /MY PORTFOLIO/
    # Lvl-2    +- /EUR/          <- Parent limit being created
    # Lvl-3      +- /Bond/ 
    # Lvl-4        +- /BMW/         <- Child limit auto created
    # Lvl-4        +- /BNP/         <- Child limit auto created
    # Lvl-3      +- /Stock/
    # Lvl-4        +- /BMW/         <- Child limit auto created
    #
    # The child limit level (4) minus the parent limit location 
    # (level 2) will give the SubLevel value that we must set (2).
    try:
        limitTarget.SubLevel(2)
    except ValueError as e:
        # SubLevel value is validated and will throw if invalid
        print('Error:', e)
    else:
        # An FLimitSpecification is needed to create the limit
        limitSpec = acm.FLimitSpecification['MY SPEC']
        limit = limitSpec.CreateLimit(limitTarget)

        # Set the attributes for the default limit values that the
        # child limits will inherit once created
        limit.ComparisonOperator('Greater or Equal')
        limit.Threshold(calculation.Value() / 10)
        limit.PercentageWarning(True)
        limit.WarningValue(5)
        limit.Commit()

def CreateLimitsFromTemplate():
    """Create FLimit objects using an FLimitTemplate.

    The following example shows how a limit template can be used to
    easily create limits on sheet insertable items, such as portfolios,
    stored insert item queries and trade filters.

    """
    _PreventCall()
    import FLimitTemplate

    # Load a pre-existing template from the stored extension or by
    # creating one from an existing limit (see CreateLimitTemplates())
    template = FLimitTemplate.FLimitTemplate.CreateFromExtension(
            'Pre-existing Limit Template')

    # The template can then be applied to any stored portfolio type
    # object (e.g. physical/compound portfolios, insert item queries,
    # trade filters), returning a new FLimit object.
    portfolio = acm.FPhysicalPortfolio['MY PORTFOLIO']
    try:
        limit = template.Apply(portfolio)
    except ValueError as e:
        print('Error:', e)
    else:        
        assert limit.Threshold() == template.Threshold()
        limit.Commit()

    # By default, the limit specification referenced by the template
    # will be used in creating the limit (if available). This can be
    # overridden by passing your own limit specification to Apply().
    asqlQuery = acm.FStoredASQLQuery['MY QUERY']
    limitSpec = acm.FLimitSpecification['MY LIMIT SPEC']
    try:
        limit = template.Apply(asqlQuery, limitSpec)
    except ValueError as e:
        print('Error:', e)
    else:
        assert limit.LimitSpecification().Name() != \
                template.LimitSpecificationName()
        limit.Commit()

def CreateLimitTemplates():
    """Create an FLimitTemplate from existing FLimit objects.

    The following example shows how a limit template can be created
    from an existing limit's definition and saved for later use.

    """
    _PreventCall()
    import FLimitTemplate

    # Only certain limits are capable of being used as the basis for 
    # a limit template. Use the IsValidForTemplate class method to
    # determine if this is the case.
    limit = acm.FLimit[1]
    assert FLimitTemplate.FLimitTemplate.IsValidForTemplate(limit)

    # Create the template using the CreateFromLimit class method
    try:
        template = FLimitTemplate.FLimitTemplate.CreateFromLimit(limit)
    except ValueError as e:
        print('Error:', e)
    else:
        assert template.Threshold() == limit.Threshold()

    # The template can then be saved to an extension module, but first
    # must be given an appropriate unique name.
    template.Name('My new template')
    module = acm.FExtensionModule['MY MODULE']
    try:
        template.SaveToModule(module)
    except ValueError as e:
        print('Error:', e)

def MonitorLimits():
    """Monitor a limit's current value and state.

    The following example shows how to monitor a limit's current
    value and state as it is being checked by a server or batch-
    checking process.

    """
    _PreventCall()
    
    # Limits can be monitored using the standard ACM notification
    # mechanism -- the ServerUpdate callback
    class MyLimitMonitor(object):

        def ServerUpdate(self, sender, aspect, _params):
            if str(aspect) == 'update':
                if sender.IsKindOf(acm.FLimit):
                    print('Limit:', sender)
                elif sender.IsKindOf(acm.FLimitValue):
                    print('Limit value:', sender.CheckedValue())
                elif sender.IsKindOf(acm.FBusinessProcess):
                    print('Limit state:', sender.CurrentStep().State().Name())

    limit = acm.FLimit[1]
    limitMonitor = MyLimitMonitor()

    # Monitor changes to the limit object (thresholds, etc)
    limit.AddDependent(limitMonitor)

    # Monitor changes to the limit state
    limit.BusinessProcess().AddDependent(limitMonitor)

    # Monitor checked limit values
    limit.LimitValue().AddDependent(limitMonitor)

def MonitorLimitsLocally():
    """Monitor the current value and state of a limit in the
    local client.

    The following example shows how to retrieve a limits current
    calculation value (locally) and how to determine its current
    state.

    NOTE: The calculation environment for the current user will
          be used in evaluating limit calculations. If this user
          has a different setup to that of the limit server, limit
          calculations may either not be creatable or may produce
          different (potentially invalid) values.

    """
    _PreventCall()
    import FLimitMonitor
    import FLimitExceptions
    
    # Implement parts of the ILimitListener interface to receive
    # notifications on changes when/if a limit is checked
    class MyLimitMonitor(FLimitMonitor.ILimitListener):

        # This method is called every time the limit is checked, with
        # the calculated current value being passed through
        def OnLimitValueChecked(self, checkResult):
            print('Limit', checkResult.Limit.Oid(), \
                    'has curent value', checkResult.CheckedValue)

        # The following methods will only be called if the checked limit
        # value would result in a limit state that differs to the 
        # currently stored state
        def OnLimitWarningEvent(self, checkResult):
            print('Limit', checkResult.Limit.Oid(), 'is now in a warning state')

        def OnLimitBreachedEvent(self, checkResult):
            print('Limit', checkResult.Limit.Oid(), 'is now in a breached state')

        def OnLimitActiveEvent(self, checkResult):
            print('Limit', checkResult.Limit.Oid(), 'is now in an active state')

        # This method is called if a monitored parent limit now has child
        # nodes that do not yet have a limit monitoring them
        def OnLimitUnmonitoredChildren(self, checkResult):
            print('Limit', checkResult.Limit.Oid(), \
                    'has new unmonitored children', checkResult.Children)

    limit = acm.FLimit[1]
    limitMonitor = MyLimitMonitor()
    try:
        # The FMonitoredLimit class wraps the limit with handling for creating
        # the target calculation and checking the value against thresholds.
        # Note that the calculation will be performed in the client making this
        # call (not server-side), so this has implications on performance.
        monitoredLimit = FLimitMonitor.FMonitoredLimit(limit, limitMonitor)
    except FLimitExceptions.LimitError as e:
        # If the target calculation could not be recreated (e.g. the row object
        # no longer exists any more), an EmptyCalculationError will be thrown.
        print('Error:', e)
    else:
        # Use GetCurrentValue to simply retrieve the current calculated value
        # of the limit's target cell. Listeners (e.g. our limitMonitor instance)
        # will not be notified with this call.
        # Note that this is different to getting the value stored in 
        # FLimit.LimitValue().CheckedValue(), which is the last value checked
        # and stored by the limit server or batch limit check script.
        currentValue = monitoredLimit.GetCurrentValue()
        print('Limit current value:', currentValue)

        # The CheckLimit call will cause the limits target calculation value to
        # be checked against stored warning and threshold values. The result
        # of the check will be given in callbacks to registered listeners 
        # (our limitMonitor instance).
        # Note that performing this check will not update the state of the limit
        # (i.e. its business process state will not change).
        monitoredLimit.CheckLimit()
    
def CheckAndUpdateLimitsLocally():
    """Check limits and update their state in the local client.

    The following example shows how to check a number of limits, updating
    their current state based on the checked value.

    NOTE: The calculation environment for the current user will
          be used in evaluating limit calculations. If this user
          has a different setup to that of the limit server, limit
          calculations may either not be creatable or may produce
          different (potentially invalid) values.

    """
    _PreventCall()
    import FLimitActions

    # Select the limits to be checked. Filter out realtime monitored limits
    # here, so that checks do not clash with those made by a server process.
    query = acm.CreateFASQLQuery('FLimit', 'AND')
    query.AddAttrNode('Owner.Name', 'RE_LIKE_NOCASE', acm.User().Name())
    myBatchLimits = [l for l in query.Select() 
            if not l.LimitSpecification().RealtimeMonitored()]

    # The following will check and update the state of all of these limits
    # within the client making the call, having implications on performance.
    # The check will cause new child limits to be created for parent limits, 
    # if required. New child limits will be checked and updated within the 
    # same call.
    FLimitActions.CheckLimits(myBatchLimits)

def CheckLimitsWithUncommittedTradesLocally():
    """Check limit value and state in the local client.

    The following example shows how to check limit values and state, 
    and test the result of introducing uncommitted trades in to their
    calcluations (e.g. for pre-deal checking).

    NOTE: The calculation environment for the current user will
          be used in evaluating limit calculations. If this user
          has a different setup to that of the limit server, limit
          calculations may either not be creatable or may produce
          different (potentially invalid) values.

    """
    _PreventCall()
    import FLimitMonitor

    limit = acm.FLimit[1]
    
    # The FMonitoredLimit class wraps the limit with handling for creating
    # the target calculation and checking the value against thresholds.
    # Note that the calculation will be performed in the client making this
    # call (not server-side), so this has implications on performance.
    monitoredLimit = FLimitMonitor.FMonitoredLimit(limit)

    # Perform a single check of the limit's current calculated value vs
    # its configured warning/threshold values. This check is performed
    # locally in the client, having implications on performance.
    # The returned LimitCheckResult object can be used to inspect the 
    # result of the check. The state of the limit (LimitValue, business 
    # process state, etc) is not changed.
    result = monitoredLimit.CheckLimit()
    print('Limit:', result.Limit.Oid())
    print('State before:', result.StateBefore)
    print('State after:', result.StateAfter)
    print('Checked value:', result.CheckedValue)

    # A hypothetical trade to be made, which should first be checked
    # against limits to ensure that they aren't breached
    trade = acm.FTrade()
    trade.Instrument(acm.FStock['BMW'])
    trade.Portfolio(acm.FPhysicalPortfolio['Portfolio1'])
    trade.Counterparty(acm.FParty['Counterparty1'])
    trade.Quantity(100)
    trade.Price(10)
    trade.Currency('EUR')
    trade.TradeTime(acm.Time().TimeNow())

    resultWithoutTrades = result
    try:
        # Check the limit again, with the new trade included in the 
        # calculation. All trades must be in an uncommitted state, or 
        # an exception will be thrown. Trades not applicable to the limit 
        # will not affect the calculated value.
        resultWithTrades = monitoredLimit.CheckLimit([trade, ])
    except Exception as e:
        print('Error:', e)
    else:
        if resultWithoutTrades.CheckedValue != resultWithTrades.CheckedValue:
            print('State with trades:', resultWithTrades.StateAfter)
            print('Change in value:', (resultWithTrades.CheckedValue - \
                resultWithoutTrades.CheckedValue))

    # Parent limits can also be checked to see if new child limits would be
    # created for the uncomitted trades
    parentLimit = acm.FLimit[2]
    assert parentLimit.IsParent()

    # The state of the parent limit is never updated by the limit check, so
    # the check result for this particular limit is not interesting. Instead, 
    # the check result's Children attribute will contain an array of 
    # LimitCheckResult objects for any new child limits that would be 
    # created by the trades, which can be inspected for their status
    monitoredParentLimit = FLimitMonitor.FMonitoredLimit(parentLimit)
    result = monitoredParentLimit.CheckLimit([trade, ])
    for childResult in result.Children:
        # The new child limit is in childResult.Limit and is uncommitted
        print('New child limit for:', childResult.Limit.LimitTarget().Path())
        print('Child limit state:', childResult.StateAfter)
        print('Child limit value:', childResult.CheckedValue)

