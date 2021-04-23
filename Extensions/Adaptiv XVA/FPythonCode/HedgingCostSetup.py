""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/HedgingCostSetup.py"

import acm
from HedgingCostUtils import HedgingCostStateChartConstants

CHART_NAME = HedgingCostStateChartConstants.CHART_NAME
STATES     = HedgingCostStateChartConstants.STATES
EVENTS     = HedgingCostStateChartConstants.EVENTS

def CreateHedgingCostStateChart():

    state_chart = acm.FStateChart[ CHART_NAME ]
    if state_chart:
        print("State Chart with name %s already exists." % CHART_NAME)
    else:
        state_chart = acm.FStateChart(name = CHART_NAME)
        state_chart.BusinessProcessesPerSubject('Single Active') # Can be Single or Unlimited
        state_chart.Commit()

        # At this point, the state chart alread has two states: Ready and Error. 
        # Now, create three more states:
        state_chart.CreateState(STATES.PENDING_HEDGINGCOST)
        state_chart.CreateState(STATES.PENDING_CONFIRMATION)
        state_chart.CreateState(STATES.END)
        state_chart.Commit()

        # The Ready state has an explicit accessor
        ready_state = state_chart.ReadyState()

        # To access the other states, use the "states by name" dictionary
        states = state_chart.StatesByName()
        pending_incremental_hedgingcost_state = states[STATES.PENDING_HEDGINGCOST]
        pending_trade_confirmation_state = states[STATES.PENDING_CONFIRMATION]
        confirmed_state = states[STATES.END]

        trade_to_hedgingcost_desk_event = acm.FStateChartEvent(EVENTS.HEDGINGCOST_REQUESTED)
        create_payments_event = acm.FStateChartEvent(EVENTS.HEDGINGCOST_ASSIGNED)
        resend_trade_to_hedgingcost_desk_event = acm.FStateChartEvent(EVENTS.HEDGINGCOST_RE_REQUEST)
        confirm_payments_event = acm.FStateChartEvent(EVENTS.TRADE_CONFIRMED)

        # Please note that you cannot create transitions to or from
        # transient states, so always commit the state chart prior 
        # to creating transitions.

        # Transitions are created by the "from state - by event - to state" idiom.
        ready_state.CreateTransition( trade_to_hedgingcost_desk_event, pending_incremental_hedgingcost_state )
        pending_incremental_hedgingcost_state.CreateTransition( create_payments_event, pending_trade_confirmation_state )
        pending_trade_confirmation_state.CreateTransition( resend_trade_to_hedgingcost_desk_event, pending_incremental_hedgingcost_state )
        pending_trade_confirmation_state.CreateTransition( confirm_payments_event, confirmed_state)
        state_chart.Commit()
        print("Created new State Chart with name %s." % state_chart.Name())
        
        # Fix the layout
        layout = state_chart.Layout()
        layoutCords = '%s;%s;%s;%s;' % (STATES.START+',0,0',
                                        STATES.PENDING_HEDGINGCOST+',220,0',
                                        STATES.PENDING_CONFIRMATION+',440,0',
                                        STATES.END+',660,0')
        layout.Text(layoutCords)
        layout.Commit()

    
def CreateOperation( operationName ):
    
    st = "compName='%s' and type='Operation'" % operationName
    component = acm.FComponent.Select01(st, None)
    if component:
        print("Component of type %s with name %s already exists." % (component.Type(), component.CompName()))
    else:
        
        component = acm.FComponent()
        component.CompName( operationName )
        component.Type('Operation')
        component.Commit()
        print("Created new component of type %s with name %s." % (component.Type(), component.CompName()))

    return


def CreateAdditionalInfo( name, recType, dataTypeGroup , dataTypeType, description, subTypes = [] ):

    addInfoSpec = acm.FAdditionalInfoSpec[name]
    if addInfoSpec:
        print("AdditionalInfoSpec with name %s already exists." % name)
    else:
        addInfoSpec = acm.FAdditionalInfoSpec(name = name, 
                                              recType=recType,
                                              dataTypeGroup = dataTypeGroup,
                                              description = description)
        if dataTypeType in ['String']:
            dataTypeTypeAsInt = 3
        else:
            dataTypeTypeAsInt = acm.FEnumeration["enum(B92RecordType)"].Enumeration( dataTypeType )
        addInfoSpec.DataTypeType(dataTypeTypeAsInt)
        for subType in subTypes:
            addInfoSpec.AddSubType( subType )
        addInfoSpec.Commit()
        print("Created AdditionalInfoSpec %s" % (name))
    return
    

def Setup():
    # STATE CHART
    CreateHedgingCostStateChart()

    # ADDITIONAL INFOS
    CreateAdditionalInfo("HedgingCostDocument", "Instrument", "RecordRef", "ChoiceList", "Standard Document", ["Credit Balance"] )
    
    # OPERATIONS
    CreateOperation( "Trading Desk" )
    CreateOperation( "Hedging Cost Desk" )
