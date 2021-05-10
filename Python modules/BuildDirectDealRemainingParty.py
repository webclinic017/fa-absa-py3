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

        stateChartName = 'DirectDealNovationRemaining'        
        perspective = 'DirectDealNovationRemaining'
        state_chart = {
            'Ready'                 :       {'Initiates'                    :       'Novation Initiated'},
            'Novation Initiated'    :       {'Withdraws'                     :       'Withdrawn',
                                             'IncomingPartyAffirms'          :       'Agreed',
                                             'Agrees'                       :       'Affirmed',
                                             'Recalls'                      :       'Recalled'},
            #                                 'AffirmsWithModification'      :       'Modified'},
            'Agreed'                :       {'Withdraws'                    :       'Withdrawn',
                                             'Agrees'                       :       'Affirmed',
                                             'Releases'                     :       'Released', 
                                             'Recalls'                      :       'Recalled',
                                             'AffirmsWithModification'      :       'Novation Initiated'},
            'Affirmed'            :       {'Withdraws'                    :       'Withdrawn',
                                             'IncomingPartyAffirms'          :       'Agreed',                                            
                                             'Releases'                     :       'Released',
                                             'AffirmsWithModification'      :       'Novation Initiated',
                                             'Recalls'                      :       'Recalled'},
            #'Modified'              :       {'AffirmsWithModification'      :       'Novation Initiated',
            #                                 'Withdraws'                    :       'Withdrawn',
            #                                 'IncomingPartyAffirms'          :       'Agreed'},
            'Recalled'              :       {'AffirmsWithModification'      :       'Novation Initiated',
                                             'Agrees'                       :       'Affirmed',
                                             'Withdraws'                    :       'Withdrawn',
                                             'IncomingPartyAffirms'                    :       'Agreed'}
            
        }  
        return stateChartName, state_chart, perspective

stateChartName, stateChartDict, stateChartPerspective = defineStateTransition()
#Creates the state chart for manual clearing
stateChart= FBuildStateChart.getStateChartInstance(stateChartName, stateChartDict, stateChartPerspective)

# EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
coString = 'Ready,250,-540;Novation Initiated,250,-356;Recalled,525,-260;Withdrawn,-13,-260;Affirmed,-9,70;Agreed,525,70; Released,250,161;'
FBuildStateChart.layOutStateChart(stateChartName, coString)
    
#Creates the clearing process for manual clearing
FBuildStateChart.createClearingProcess(stateChartName)
#


