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

        stateChartName = 'DirectDealNovationStepOut'        
        perspective = 'DirectDealNovationStepOut'
        state_chart = {
            'Ready'                 :       {'Initiates'                    :       'Novation Affirmed'},
            'Novation Affirmed'    :       {'Withdraws'                    :       'Withdrawn',
                                             'Agrees'                       :       'Agreed',
                                             'CptyAgrees'                   :       'CptyAgreed',
                                             'Recalls'                      :       'Recalled'},
            #                                 'AffirmsWithModification'      :       'Modified'},
            'Agreed'                :       {'Withdraws'                    :       'Withdrawn',
                                             'CptyAgrees'                   :       'CptyAgreed',
                                             'Releases'                     :       'Released'},
            'CptyAgreed'            :       {'Withdraws'                    :       'Withdrawn',
                                             'Agrees'                       :       'Agreed',                                            
                                             'Releases'                     :       'Released',
                                             'AffirmsWithModification'      :       'Novation Affirmed',
                                             'Recalls'                      :       'Recalled'},
            #'Modified'              :       {'AffirmsWithModification'      :       'Novation Initiated',
            #                                 'Withdraws'                    :       'Withdrawn',
            #                                 'Agrees'                       :       'Agreed'},
            'Recalled'              :       {'AffirmsWithModification'      :       'Novation Affirmed',
                                             'CptyAgrees'                   :       'CptyAgreed',
                                             'Withdraws'                    :       'Withdrawn'}
            
        }  
        return stateChartName, state_chart, perspective

stateChartName, stateChartDict, stateChartPerspective = defineStateTransition()
#Creates the state chart for manual clearing
stateChart= FBuildStateChart.getStateChartInstance(stateChartName, stateChartDict, stateChartPerspective)

# EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
coString = 'CptyAgreed,522,-82;Withdrawn,-90,-317;Released,271,93;Ready,248,-540;Agreed,56,-82;Novation Affirmed,248,-392;Recalled,522,-317;'
FBuildStateChart.layOutStateChart(stateChartName, coString)

#Creates the clearing process for manual clearing
FBuildStateChart.createClearingProcess(stateChartName)
#


