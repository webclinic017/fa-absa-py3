import acm
import FBuildStateChart
def defineStateTransition():
        """
        Creates a state chart with the given name, if required.
        The definition parameter must completely define the content of the business
        process state chart, including all states and transitions between them. Its
        format is a dictionary of states mapped to a dictionary of transitions as
        event->next_state items, e.g.:
    
            {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}
    
        All defined next_states values must be unique within a state's transitions
        (i.e. multiple events cannot lead to the same next_state).
        """

        stateChartName = 'LCH_Clearnet_T2_Client'
        # Valid perspectives are T2ExecutionBroker, T2Client, T2ClearingBroker
        perspective = 'T2Client'
        state_chart = {
            'Ready':       {'EBSubmits'                    :       'CptyAffirmed',
                                             'Submits'                      :       'Affirmed',
                                             'Withdraws'                    :       'Withdrawn'},
            'CptyAffirmed':       {'EBRecalls'                    :       'Recalled',
                                             'AffirmsWithModification'      :       'Affirmed',
                                             'PickUp'                       :       'PickedUp',
                                             'Affirms'                      :       'Agreed',
                                             'EBAffirms'                    :       'Agreed',
                                             'Withdraws'                    :       'Withdrawn'},
            'Affirmed':       {'EBAffirmsWithModification'    :       'CptyAffirmed',
                                             'EBAffirms'                    :       'Agreed',
                                             'Affirms'                      :       'Agreed',
                                             'Recalls'                      :       'Recalled',
                                             'Withdraws'                    :       'Withdrawn'},
            'PickedUp':       {'Affirms'                      :       'Agreed',
                                             'AffirmsWithModification'      :       'Affirmed',
                                             'EBAffirmsWithModification'    :       'CptyAffirmed',
                                             'EBRecalls'                    :       'Recalled',
                                             'Withdraws'                    :       'Withdrawn'},
            'Recalled':       {'EBAffirmsWithModification'    :       'CptyAffirmed',
                                             'AffirmsWithModification'      :       'Affirmed',
                                             'PickUp'                       :       'PickedUp',
                                             'Withdraws'                    :       'Withdrawn'},
            'Agreed':       {'Releases'                     :       'Released'},                                             
            'Released':       {'ClearingInitiate'             :       'CHSubmitted'},
            'CHSubmitted':       {'CHRejects'                    :       'Rejected',
                                             'CHAccepts'                    :       'Registered'},
            'Rejected':       {'Withdraws'                    :       'Withdrawn'},
            'Registered':       {'Releases'                     :       'Cleared'},
            'Cleared':       {'TradeDivision'                :       'Alpha Cancelled',
                                             'CHClearsBeta'                 :       'Beta Cleared'},
            'Alpha Cancelled':       {'CHClearsBeta'                 :       'Beta Cleared'},
            'Withdrawn':       {'Resubmits'                    :       'Ready'},
        }  
        return stateChartName, state_chart, perspective

stateChartName, stateChartDict, stateChartPerspective = defineStateTransition()
#Creates the state chart for manual clearing
stateChart= FBuildStateChart.getStateChartInstance(stateChartName, stateChartDict, stateChartPerspective)

# EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
coString = 'Ready,-400,-300;CptyAffirmed,0,-300;Recalled,800,-300;Withdrawn,1100,-150;PickedUp,-500,-25;Affirmed,800,0;Agreed,0,50;Released,0,175;CHSubmitted,225,175;Registered,450,175;Cleared,650,175;Rejected,1100,50;Alpha Cancelled,875,175;Beta Cleared,1100,175;'
FBuildStateChart.layOutStateChart(stateChartName, coString)

#Creates the clearing process for manual clearing
FBuildStateChart.createClearingProcess(stateChartName)


