import acm

def getStates(definition):
    """Get state names from transition dictionary."""
    state_names = set(definition.keys()) # Get from_state
    for all_transitions in definition.values(): # Get to_state for each from_state
        to_states = set(all_transitions.values()) 
        state_names = state_names | to_states # Add to_state to from_state
    return state_names

def createStates(sc, state_names):
    """Create states for given state chart"""
    existingStates = sc.StatesByName()
    for state_name in state_names:
        if state_name not in existingStates:
            sc.CreateState(state_name)
    sc.Commit()

def createTransitions(sc, definition):
    """Create events for given state chart from transition dictionary."""
    states = sc.StatesByName()
    for state_name, transitions in definition.items():
        state = states.At(state_name)
        for event_name, to_state_name in transitions.items():
            event = acm.FStateChartEvent(event_name)
            if not state.TransitionForEvent(event):
                to_state = states.At(to_state_name)
                state.CreateTransition(event, to_state)
    sc.Commit()

def createStateChart(stateChartName, definition, stateChartPerspective):
    """Creates a state chart with the given name, if required.

    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).

    """
    sc = acm.FStateChart[stateChartName]
    if not sc:
        sc = acm.FStateChart(name=stateChartName)
    state_names = getStates(definition)
    createStates(sc, state_names)
    createTransitions(sc, definition)
    updateAdditionalInfo('CCPperspective', sc, stateChartPerspective)
    
def updateAdditionalInfo(addInfoSpec, subject, addInfoValue):
    """update the additional info on an subject Trade"""
    ais = acm.FAdditionalInfoSpec[addInfoSpec]
    query = 'addInf=%d and recaddr=%d ' % (ais.Oid(), subject.Oid())
    aiSel = acm.FAdditionalInfo.Select(query)
    if aiSel:
        ai = aiSel[0]
        if addInfoValue:
            aiC = ai.Clone()
            aiC.FieldValue(addInfoValue)
            ai.Apply(aiC)
    else:
        ai = acm.FAdditionalInfo()
        ai.Recaddr = subject.Oid()
        ai.AddInf = ais.Oid()
        ai.FieldValue(addInfoValue)
    ai.Commit()
    
def getStateChartInstance(stateChartName, stateChartDict, stateChartPerspective):
    """ Creates a state chart with the given name from given dictionary, if required. """
    state_chart = None
    if validatePerspective(stateChartPerspective):
        state_chart = createStateChart(stateChartName, stateChartDict, stateChartPerspective)
        print('The state chart '+ stateChartName + ' is created/Updated. Perspective is : ' + stateChartPerspective)
    else:
        print('Invalid perspective <'+ stateChartPerspective + '> Check valid perspective in choice list CCPPerspective') 
        
    return state_chart 

def validatePerspective(perspective):
    choicelist = acm.FChoiceList.Select("list=CCPPerspective")
    bValid = False
    for eachChoice in choicelist:
        if perspective.upper() == eachChoice.Name().upper():
            bValid = True
            break
    return bValid    
    
def layOutStateChart(stateChartName, coString):
    """ Layout state chart with the given name from given coordinate string. """
    state_chart = acm.FStateChart[stateChartName]
    if not state_chart:
        print('The state chart '+ stateChartName + ' is not present in ADS.')
    else:
        state_chart.Layout().Text(coString)
        state_chart.Layout().Commit()
        print('Done with layout of state chart '+ stateChartName + '.')

def createClearingProcess(stateChartName):
    """ Add newly created state chart in drop down list of clearing process. """
    keyVal = 'CCPWorkFlow'
    query = "list = '%s' and name = '%s'" %(keyVal, stateChartName)
    choiceExists = acm.FChoiceList.Select(query)
    if not choiceExists:
        try:
            newcl = acm.FChoiceList()
            newcl.List = keyVal
            newcl.Name = stateChartName
            newcl.Commit()
            print("'%s' clearing process added into the list of clearing processes in ADS" %stateChartName)
        except Exception, e:
            print(e)
    else:
        print("'%s' clearing process already exists in in ADS" %stateChartName)


