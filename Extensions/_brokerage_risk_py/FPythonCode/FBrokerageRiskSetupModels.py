""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FBrokerageRiskSetupModels.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    Brokerage Risk

    (c) Copyright 2016 SunGard Front Arena AB. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm

# Check for portfolio type "Cash Account", add if missing
choiceList = 'PortfolioType'
entryName = 'Cash Account'

cashAccount = acm.FChoiceList.Select01( "list='%s' name='%s'" % ( choiceList, entryName ), None )

if not cashAccount:
    cashAccount = acm.FChoiceList()
    cashAccount.Name( entryName )
    cashAccount.List( choiceList )
    cashAccount.Description( entryName )
    cashAccount.Commit()


def log(info):
    if info:
        print(info)


def ModelCategorySetup(modelDefinitions, filterMethods):
    def FindOrCreateFilterList(categoryName, listName):
        filterList = acm.FConditionFilterList[ listName ]
        if filterList == None:
            # Create new FConditionFilterList
            filterList = acm.FConditionFilterList()
            filterList.Name( listName )
            filterList.Commit()
            log( '%s: Created new FConditionFilterList %s' % ( categoryName, listName ) )
        return filterList


    def FindFilter(existingFilters, requiredAttributes):
        for item in existingFilters:
            filter, filteredAttributes = item
            if not set( filteredAttributes ).symmetric_difference( requiredAttributes ):
                existingFilters.remove( item )
                return filter

    def FindOrCreateFilter(filterList, existingFilters, idx, requiredAttributes):
        info = []
        filter = FindFilter(existingFilters, requiredAttributes)
        if filter == None:
            # Create new FConditionFilter
            filter = acm.FConditionFilter()
            for name in requiredAttributes:
                getattr( filter, name )( True )
            filter.FilterList( filterList )
            info.append( '%s: Created new FConditionFilter with attributes %s' % ( filterList.Name(), requiredAttributes ) )

        elif filter.Priority() != idx + 1:
            info.append( '%s: Setting priority to %i for FConditionFilter with attributes %s' % ( filterList.Name(), idx + 1, requiredAttributes ) )

        else:
            return

        filter.Priority( idx + 1 )
        filter.Commit()
        log( '\n'.join( info ) )
        
    def LogConditionsMatchingUnusedFilters(filterMethods, unusedFilters, model):
        for cnd in model.Conditions():
            conditionFilters = [ a for a in filterMethods if getattr( cnd, a )() not in [ None, 'None', 'Undefined' ] ]
            for filter, filteredAttributes in unusedFilters:
                if set( conditionFilters ) == set( filteredAttributes ):
                    log( 'Model "%s" has condition "%s" mapped to filter %s which is no longer used (the filter will be deleted)' % ( model.Name(), cnd.Name(), filteredAttributes ) )

    def DeleteUnusedFilters(filterList, unusedFilters):
        for filter, filteredAttributes in unusedFilters:
            try:
                filter.Delete()
                log( '%s: Deleted filter with attributes %s' % ( filterList.Name(), filteredAttributes ) )
            except RuntimeError as msg:
                log( '%s: Could not delete filter with attributes %s - %s' % ( filterList.Name(), filteredAttributes, msg ) )


    # 1. FConditionFilterLists, shared by the corresponding group of FConditionalValueModels
    for categoryName, definition in modelDefinitions.copy().iteritems():
        definition[ 'filterList' ] = FindOrCreateFilterList( categoryName, definition[ 'listName' ] )

    # 2. FConditionFilters, added to the FConditionFilterList
    for categoryName, definition in modelDefinitions.iteritems():
        filterList = definition['filterList']
        existingFilters = [ [ filter, [ name for name in filterMethods if getattr( filter, name )() ] ] for filter in filterList.Filters() ]
        for idx, attributes in enumerate( definition['filterPropertiesList'] ):
            FindOrCreateFilter(filterList, existingFilters, idx, attributes)    # Removes entries from existingFilters list when found...
        for modelName in definition[ 'modelNames' ]:
            model = acm.FConditionalValueModel[ modelName ]
            if model:
                LogConditionsMatchingUnusedFilters( filterMethods, existingFilters, model )
        DeleteUnusedFilters( filterList, existingFilters )                                  # ... so that any remaining filters can be removed (unless referenced by FConditions)


    # 3. FConditionalValueModels, using the FConditionFilterList
    for categoryName, definition in modelDefinitions.iteritems():
        for modelName in definition[ 'modelNames' ]:
            model = acm.FConditionalValueModel[ modelName ]
            if model == None:
                model = acm.FConditionalValueModel()
                log( '%s: Created new FConditionalValueModel %s' % ( categoryName, modelName ) )
            model.Name( modelName )
            model.FilterList( definition['filterList'] )
            model.ModelCategory( categoryName )
            model.Commit()



ael_variables = [('simulate', 'Only simulate - run script but do not commit changes, just log', 'bool', [False, True], False)]


def ael_main( parameters ):

    simulate = parameters['simulate']

    collateralFilters   = [
                            [ 'Client',          'Instrument'                   ],
                            [ 'Client',          'InsFilter'                    ],
                            [ 'ClientGroup',     'Instrument'                   ],
                            [ 'ClientGroup',     'InsFilter'                    ],
                            [ 'Portfolio',       'Instrument'                   ],
                            [ 'PortfolioFilter', 'Instrument'                   ],
                            [ 'Portfolio',       'InsFilter'                    ],
                            [ 'PortfolioFilter', 'InsFilter'                    ],
                            [                    'Instrument'                   ],
                            [                    'InsFilter'                    ],
                            [ 'Client'                                          ],
                            [ 'ClientGroup'                                     ],
                            [ 'Portfolio'                                       ],
                            [ 'PortfolioFilter'                                 ],
                            [                                                   ]
                        ]

    marginFilters       = [
                            [ 'Client',          'Instrument'                   ],
                            [ 'Client',          'InsFilter'                    ],
                            [ 'ClientGroup',     'Instrument'                   ],
                            [ 'ClientGroup',     'InsFilter'                    ],
                            [ 'Portfolio',       'Instrument'                   ],
                            [ 'PortfolioFilter', 'Instrument'                   ],
                            [ 'Portfolio',       'InsFilter'                    ],
                            [ 'PortfolioFilter', 'InsFilter'                    ],
                            [                    'Instrument'                   ],
                            [                    'InsFilter'                    ],
                            [ 'Client'                                          ],
                            [ 'ClientGroup'                                     ],
                            [ 'Portfolio'                                       ],
                            [ 'PortfolioFilter'                                 ],
                            [                                                   ]
                        ]
    
    """ Remove for now
    marginFiltersFX       = [
                            [ 'Client',          'Instrument',    'Currency'    ],
                            [ 'ClientGroup',     'Instrument',    'Currency'    ],
                            [ 'Portfolio',       'Instrument',    'Currency'    ],
                            [ 'PortfolioFilter', 'Instrument',    'Currency'    ],
                            [                    'Instrument',    'Currency'    ],
                            [                                                   ]
                        ]
    """

    amsFilters          = [
                            [ 'Depot'                                 ],
                            #[ 'Depot', 'Client'                       ],
                            [ 'Client'                                ],
                            [ 'ClientGroup'                           ],
                            [ 'Portfolio'                             ],
                            [ 'PortfolioFilter'                       ],
                            [ 'Counterparty', 'Contact'               ],
                            [ 'Counterparty'                          ],
                            [                                         ]
                        ]

    modelDefinitions    = {
                      'Collateral': {
                                        'modelNames'            : [ 'Haircut', 'Price Cap', 'Quantity Cap', 'Value Cap' ],
                                        'listName'              : 'Collateral Valuation',
                                        'filterPropertiesList'  : collateralFilters
                                      },
                      'Margin': {
                                        'modelNames'            : [ 'Initial Margin', 'Maintenance Margin Factor' ],
                                        'listName'              : 'Margin Parameters',
                                        'filterPropertiesList'  : marginFilters
                                      },
                      'AMS Limits': {
                                        'modelNames'            : [ 'Max Gross Value Per Day', 'Max Short Sell Value Per Day', 'Min Order Value', 'Max Order Value', 'Max Buy Value Per Day', 'Max Sell Value Per Day', 'Max Order Per Day', 'Max Order Activity' ],
                                        'listName'              : 'AMS Limits',
                                        'filterPropertiesList'  : amsFilters
                                      },
                    }
    """ Remove for now
    modelDefinitionsFX  = {
                      'Margin'      : {
                                        'modelNames'            : [ 'Initial Margin FX', 'Maintenance Margin Factor FX' ],
                                        'listName'              : 'Margin Parameters FX',
                                        'filterPropertiesList'  : marginFiltersFX
                                      },
                    }
    """

    filterMethods = [ m.Name().AsString() for m in acm.FConditionFilter.MethodsImplemented() if m.Domain().Name().AsString() == 'bool' ]

    if simulate:
        log( '*** Begin SIMULATED setup - changes will not be commited' )
        acm.BeginTransaction()

    ModelCategorySetup( modelDefinitions, filterMethods )
    """ Remove for now
    ModelCategorySetup( modelDefinitionsFX, filterMethods )
    """

    if simulate:
        acm.AbortTransaction()
        log( '*** End SIMULATED setup' )
