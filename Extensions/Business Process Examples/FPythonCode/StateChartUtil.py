
import acm

def create_sample_state_chart():
    # This is how the state chart depicted in the introduction to State Charts 
    # and Buiness Processes is created.

    state_chart = acm.FStateChart(name = 'A Sample State Chart')
    state_chart.BusinessProcessesPerSubject('Single Active') # Can be Single or Unlimited
    state_chart.Commit()

    # At this point, the state chart alread has two states: Ready and Error. 
    # Now, create three more states:
    state_chart.CreateState('A')
    state_chart.CreateState('B')
    state_chart.CreateState('C')
    state_chart.Commit()

    # The Ready state has an explicit accessor
    ready_state = state_chart.ReadyState()

    # To access the other states, use the "states by name" dictionary
    states = state_chart.StatesByName()
    state_a = states['A']
    state_b = states['B']
    state_c = states['C']

    alpha_event = acm.FStateChartEvent('Alpha')
    beta_event = acm.FStateChartEvent('Beta')
    gamma_event = acm.FStateChartEvent('Gamma')

    # Please note that you cannot create transitions to or from
    # transient states, so always commit the state chart prior 
    # to creating transitions.

    # Transitions are created by the "from state - by event - to state" idiom.
    ready_state.CreateTransition(alpha_event, state_a)
    state_a.CreateTransition(beta_event, state_b)
    state_b.CreateTransition(beta_event, state_c)
    state_a.CreateTransition(gamma_event, state_c)
    state_chart.Commit()


def create_business_process(subject, state_chart):
    return acm.BusinessProcess.InitializeProcess(subject, state_chart)


def find_business_processes_and_handle_event(subject, state_chart, event):
    # Either subject or state chart can be omitted to find all processes
    # for a given subject or all processes for using given state chart
    processes = acm.BusinessProcess.FindBySubjectAndStateChart(subject, state_chart)

    for process in processes:
        process.HandleEvent(event)
        process.Commit()








