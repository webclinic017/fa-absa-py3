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
        stateChartName = 'DirectDeal'        
        perspective = 'DirectDeal'
        state_chart = {
            'Ready':       {'Submits'                      :       'Affirmed',
                                             'CptySubmits'                  :       'CptyAffirmed',
                                             'Withdraws'                    :       'Withdrawn'},
            'Affirmed':       {'Recalls':       'Recalled',                                             
                                             'Affirms':       'Agreed',
                                             'Withdraws':       'Withdrawn',
                                             'CptyAffirmsWithModification':       'CptyAffirmed',
                                             'CptyAffirms':       'Agreed',},            
            'CptyAffirmed':       {'AffirmsWithModification'      :       'Affirmed',
                                             'Affirms'                      :       'Agreed',
                                             'CptyAffirms'                  :       'Agreed',
                                             'CptyRecalls'                  :       'Recalled',
                                             'Withdraws'                    :       'Withdrawn'},
            'Recalled':       {'AffirmsWithModification'      :       'Affirmed',
                                             'CptyAffirmsWithModification'  :       'CptyAffirmed',
                                             'Withdraws'                    :       'Withdrawn'},
            'Agreed':       {'Releases'                     :       'Released',
                                             'Withdraws'                    :       'Withdrawn'},
            'Released':       {'Exits'                        :       'Exit'},
            'Exit':       {'Affirms'                      :       'Agreed',
                                             'ExitWithdraws'                :       'Released'},
            'Withdrawn':      {'Resubmits':       'Ready',},
        }
        return stateChartName, state_chart, perspective

stateChartName, stateChartDict, stateChartPerspective = defineStateTransition()
#Creates the state chart for manual clearing
stateChart= FBuildStateChart.getStateChartInstance(stateChartName, stateChartDict, stateChartPerspective)

# EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
coString = 'Withdrawn,168,150;Recalled,436,-313;CptyAffirmed,-148,160;Agreed,629,-48;Released,629,197;Ready,-301,-412;Affirmed,-148,-313;Exit,333,209'


FBuildStateChart.layOutStateChart(stateChartName, coString)

#Creates the clearing process for manual clearing
FBuildStateChart.createClearingProcess(stateChartName)




