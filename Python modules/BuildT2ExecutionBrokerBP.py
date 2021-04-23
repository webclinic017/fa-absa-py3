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

        stateChartName = 'LCH_Clearnet_T2_EB'
        # Valid perspectives are T2ExecutionBroker, T2Client, T2ClearingBroker
        perspective = 'T2ExecutionBroker'
        state_chart = {
            'Ready':       {'Submits'                      :       'Affirmed',
                                             'CptySubmits'                  :       'CptyAffirmed',
                                             'Withdraws'                    :       'Withdrawn'},
            'Affirmed':       {'Recalls'                      :       'Recalled',
                                             'ClientAffirmsWithModification':       'CptyAffirmed',
                                             'CptyAffirmsWithModification'  :       'CptyAffirmed',
                                             'ClientAffirms'                :       'Agreed',
                                             'Affirms'                      :       'Agreed',
                                             'Withdraws'                    :       'Withdrawn'},
            'CptyAffirmed':       {'AffirmsWithModification'      :       'Affirmed',
                                             'Affirms'                      :       'Agreed',
                                             'ClientAffirms'                :       'Agreed',
                                             'ClientRecalls'                :       'Recalled',
                                             'Withdraws'                    :       'Withdrawn'},
            'Recalled':       {'AffirmsWithModification'      :       'Affirmed',
                                             'ClientAffirmsWithModification':       'CptyAffirmed',
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
coString = 'Ready,-300,-300;Affirmed,0,-300;Recalled,600,-300;Withdrawn,1100,-200;CptyAffirmed,600,-50;Agreed,0,-100;Released,0,100;CHSubmitted,225,100;Registered,450,100;Cleared,650,100;Rejected,1100,-50;Alpha Cancelled,875,100;Beta Cleared,1100,100;'
FBuildStateChart.layOutStateChart(stateChartName, coString)

#Creates the clearing process for manual clearing
FBuildStateChart.createClearingProcess(stateChartName)





