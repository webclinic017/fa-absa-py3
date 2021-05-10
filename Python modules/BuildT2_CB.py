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

        stateChartName = 'T2_CB'
        # Valid perspectives are T2ExecutionBroker, T2Client, T2ClearingBroker
        perspective = 'T2ClearingBroker'
        state_chart = {
            'Ready'                 :       {'CHSubmits'                    :       'Received'},
            'Received'              :       {'Rejects'                      :       'Rejected',
                                             'PickUps'                      :       'PickedUp',
                                             'Accepts'                      :       'Accepted'},
            'PickedUp'              :       {'Rejects'                      :       'Rejected',
                                             'Accepts'                      :       'Accepted'},
            'Accepted'              :       {'CHAcknowledge'                :       'CHAcknowledged'},
            'CHAcknowledged'        :       {'CHAccepts'                    :       'Registered'},
            'Registered'            :       {'CHClears'                     :       'Cleared'}
        }  
        return stateChartName, state_chart, perspective

stateChartName, stateChartDict, stateChartPerspective = defineStateTransition()
#Creates the state chart for manual clearing
stateChart= FBuildStateChart.getStateChartInstance(stateChartName, stateChartDict, stateChartPerspective)

# EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
coString = 'Ready,-300,0;Received,-100,0;PickedUp,-100,225;Accepted,100,0;CHAcknowledged,350,0;Registered,575,0;Cleared,775,0;Rejected,-300,225'
FBuildStateChart.layOutStateChart(stateChartName, coString)

#Creates the clearing process for manual clearing
FBuildStateChart.createClearingProcess(stateChartName)


