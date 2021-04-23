"""
    This module contains all the code that will only be executed once initially during the setup process. The purpose
    of this is to contain the code separately for (i) ease of maintenance and (ii) to prevent unnecessary code being
    executed regularly in production.

    This module contains:
     (1) Class definitions of State Charts used in Business Processes as well as Limit Management.
     (2) Limit Specifications that are used when creating new limits for the mandates.
     (3) Choice List Definitions for the Limit Transform Functions.

"""

import acm

from GenericMandatesAuthorizationStateChart import StateChartAuthorizationProcess
from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import MANDATE_TYPES
from GenericMandatesATSApplyMandate import UserTracker, GetAllMandatedTraders, USER_TRACKER_TEXT_OBJECT


PROTECTION_LEVEL_STATE_CHARTS = 3504
PROTECTION_LEVEL_LIMIT_SPECIFICATIONS = 3504
PROTECTION_LEVEL_GROUPERS = 3504
PROTECTION_LEVEL_CHOICE_LISTS = 3504

SUPERVISOR_COMPONENTS = ["Business Process Details", "Operations Manager", "Run Query", "Run Script", "Trading Manager", "BusinessEvent", "BusinessProcess", "BusinessProcessStep", "Limit", "LimitSpec", "LimitValue", "TextObject", "Run Script"]
SUPERVISOR_ORGANISATION = "Front"
SUPERVISOR_PROFILE_NAME = "Africa Supervisor"
SUPERVISOR_GROUP_NAME = "Africa Supervisors"


class StateChartMandateViolation:
    """
    This state chart definition is used for the business processes created when a violation occurs.
    """

    # State chart properties
    NAME = 'GenericMandates_ViolationStates'
    LIMIT = 'Unlimited'
    LAYOUT = 'Closed,668,126;Ready,93,126;Breached,376,126;Investigation,329,82;'

    # State & event name config
    STATE_READY = 'Ready'
    EVENT_LIMIT_BREACH = 'Limit_Breached'
    STATE_BREACHED = 'Breached'
    EVENT_INVESTIGATED = 'Investigated'
    STATE_CLOSED = 'Closed'
    STATE_ERROR = 'Error'

    def __init__(self):
        pass

    @classmethod
    def getDefinition(cls):
        """ Accessor to return the state chart definition configuration

        Return: [Type=Dictionary]
            The definition parameter must completely define the content of the business
            process state chart, including all states and transitions between them. Its
            format is a dictionary of states mapped to a dictionary of transitions as
            event->next_state items, e.g.:

                {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

            All defined next_states values must be unique within a state's transitions
            (i.e. multiple events cannot lead to the same next_state).
        """

        definition = {cls.STATE_READY: {cls.EVENT_LIMIT_BREACH: cls.STATE_BREACHED},
                      cls.STATE_BREACHED: {cls.EVENT_INVESTIGATED: cls.STATE_CLOSED}}
        return definition

    @classmethod
    def getLayout(cls):
        return cls.LAYOUT

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def getLimit(cls):
        return cls.LIMIT


class StateChartMandateLimit:
    """
    This State Chart is used when creating custom FLimitSpecifications. It is a simplified version of the default Limits
    state chart.
    """
    NAME = 'GenericMandates_MandateStates'
    LIMIT = 'Single'
    LAYOUT = 'Active,114,-149;Ready,-67,-147;Breached,430,-153;Inactive,113,79;Warning,271,-246;'
    STATE_INACTIVE = 'Inactive'
    STATE_READY = 'Ready'

    DEFINITION = {STATE_READY:      {'Monitor Limit': 'Active'},
                  'Active':         {'Warn': 'Warning', 'Deactivate': 'Inactive'},
                  'Warning':        {'Breach': 'Breached', 'Recede': 'Active'},
                  'Breached':       {'Warn': 'Warning', 'Recede': 'Active'},
                  STATE_INACTIVE:   {'Activate': 'Active'}}

    def __init__(self):
        pass

    @classmethod
    def getDefinition(cls):
        return cls.DEFINITION

    @classmethod
    def getLimit(cls):
        return cls.LIMIT

    @classmethod
    def getLayout(cls):
        return cls.LAYOUT

    @classmethod
    def getName(cls):
        return cls.NAME


def CreateStateChart(name, definition, layout=None, limit='Unlimited'):
    """
    Creates a state chart with the given name, if required.

    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).

    :param name: string
    :param definition: dict
    :param layout: string
    :param limit: string
    :return: FStateChart
    """

    stateChart = acm.FStateChart[name]
    if stateChart:
        return stateChart

    stateChart = acm.FStateChart(name=name)
    stateChart.BusinessProcessesPerSubject(limit)

    # Create all states, including those referenced in transitions
    state_names = list(definition.keys())
    for all_transitions in list(definition.values()):
        state_names.extend([s for s in list(all_transitions.values()) if s not in state_names])

    for state_name in (s for s in state_names if s not in ('Ready', 'Error')):
        stateChart.CreateState(state_name)
    stateChart.Protection(PROTECTION_LEVEL_STATE_CHARTS)
    stateChart.Commit()
    states = stateChart.StatesByName()

    # Link states based on transitions, creating events as required
    for state_name, transitions in list(definition.items()):
        state = states.At(state_name)
        for event_name, to_state_name in list(transitions.items()):
            event = acm.FStateChartEvent(event_name)
            to_state = states.At(to_state_name)
            state.CreateTransition(event, to_state)
    stateChart.Commit()

    if layout:
        stateChart.Layout().Text(layout)
        stateChart.Commit()

    return stateChart


def CreateAllStateCharts():
    """
    Create all the state charts required.
    """
    stateCharts = [StateChartMandateViolation(), StateChartMandateLimit(), StateChartAuthorizationProcess(1)]

    for stateChart in stateCharts:
        exists = acm.FStateChart[stateChart.getName()]
        if not exists:
            CreateStateChart(stateChart.getName(),
                             stateChart.getDefinition(),
                             stateChart.getLayout(),
                             stateChart.getLimit())
            getLogger().info('Created state chart (%s)' % stateChart.getName())
        else:
            getLogger().info('State Chart already exists (%s)' % stateChart.getName())


def CreateLimitSpecification(specData):
    # Check if the Limit Specification already exists
    if not acm.FLimitSpecification[specData["name"]]:
        # Check if the State Chart exists
        if acm.FStateChart[specData["chart"]]:
            spec = acm.FLimitSpecification()
            spec.Name(specData["name"])
            spec.Description(specData["description"])
            spec.StateChart(acm.FStateChart[specData["chart"]])
            spec.RealtimeMonitored(specData["realtime"])
            spec.LimitType('Mandate')
            spec.Protection(PROTECTION_LEVEL_LIMIT_SPECIFICATIONS)
            spec.Commit()
        else:
            getLogger().error("[ERROR] State chart does not exist (%s)." % specData["name"])
    else:
        getLogger().warn("The limit specification already exists (%s)" % specData["name"])


def CreateAllLimitSpecifications():
    chart = StateChartMandateLimit()
    chartName = chart.getName()

    for mandateType in MANDATE_TYPES:
        specData = {"name": mandateType["name"], "description": mandateType["description"],
                    "chart": chartName, "realtime": False}
        CreateLimitSpecification(specData)


def CreateChoiceList(listName, name, description):
    # Check if choice list exists
    exists = acm.FChoiceList.Select('name="%s" list="%s"' % (name, listName))
    if not exists:
        choiceList = acm.FChoiceList()
        choiceList.Name(name)
        choiceList.List(listName)
        choiceList.Description(description)
        choiceList.Protection(PROTECTION_LEVEL_CHOICE_LISTS)
        choiceList.Commit()
        getLogger().info("Choice list created (%s)" % name)
    else:
        getLogger().warn("Choice list already exists (%s)" % name)


def CreateAllChoiceLists():
    choiceLists = [{"list": "MASTER", "name": "Limit Transform Function", "description": "Limit Transform Functions"},
                   {"list": "Limit Transform Function", "name": "Mandate", "description": "limitMandate"},
                   {"list": "Limit Type", "name": "Mandate", "description": "Mandate Limit Type"}]

    for choiceList in choiceLists:
        CreateChoiceList(choiceList["list"], choiceList["name"], choiceList["description"])


def CreateUserProfile(name, description):
    exists = acm.FUserProfile.Select('name="%s"' % name)
    if not exists:
        newProfile = acm.FUserProfile()
        newProfile.Name(name)
        newProfile.Description(description)
        newProfile.Commit()
        getLogger().debug('Created new User Profile (%s)' % name)
    else:
        getLogger().warn('[Warning] User Profile already exists. Name: %s' % name)


def CreateAllUserProfiles():
    # Create all the Admin user profiles
    CreateUserProfile('Mandate_Admin_PS', 'Profile enabling user to create, modify, authorize and disable mandates.')

    # Create all the Signer user profiles
    CreateUserProfile('Mandate_Sign_PS', 'Profile enabling user to only authorize mandates.')

    # Create the System user profile
    CreateUserProfile('Mandate_System', 'Profile enabling system user to save mandates to DB. Linked to ATS user.')

    # Create Product Supervisor profiles
    CreateUserProfile('PS_ADMIN', 'Profile for Product Supervisor of ADMIN user group.')
    CreateUserProfile('PS_CREDIT', 'Profile for Product Supervisor of CREDIT user group.')
    CreateUserProfile('PS_MANDATES', 'Profile for Product Supervisor of MANDATES user group.')

    # Create Africa Supervisor profile
    CreateUserProfile(SUPERVISOR_PROFILE_NAME, 'Profile for Africa Supervisors.')


def CreateOperation(name):
    exists = acm.FComponent.Select01('name="%s"' % name, None)
    if not exists:
        newComponent = acm.FComponent()
        newComponent.Name(name)
        newComponent.Type('Operation')
        newComponent.Commit()
        getLogger().debug('Create new Operation %s (Oid: %s)' % (name, newComponent.Oid()))
        return newComponent
    else:
        getLogger().warn('[Warning] Operation already exists. Name %s (Oid: %s)' % (name, exists.Oid()))
        return exists


def CreateProfileComponent(component, userProfile):
    """
    Create a new Profile Component
    :param component: FComponent
    :param userProfile: FUserProfile
    """
    exists = acm.FProfileComponent.Select01('component="%s" userProfile="%s"' % (component.Oid(), userProfile.Oid()),
                                            None)
    if not exists:
        profileComponent = acm.FProfileComponent()
        profileComponent.Component(component)
        profileComponent.UserProfile(userProfile)
        profileComponent.AllowCreate("YES")
        profileComponent.AllowDelete("YES")
        profileComponent.AllowWrite("YES")
        profileComponent.Commit()
        getLogger().debug('Create new Profile Component (Oid: %s)' % profileComponent.Oid())
    else:
        getLogger().warn('[Warning] Profile Component already exists (Oid: %s)' % exists.Oid())


def CreateAllOperations():
    # Create operations
    authorization = CreateOperation('Mandate Authorization')
    creation = CreateOperation('Mandate Creation')
    modification = CreateOperation('Mandate Modification')
    saving = CreateOperation('Mandate Save to DB')

    # Admin Product Supervisor
    CreateProfileComponent(authorization, acm.FUserProfile['Mandate_Admin_PS'])
    CreateProfileComponent(creation, acm.FUserProfile['Mandate_Admin_PS'])
    CreateProfileComponent(modification, acm.FUserProfile['Mandate_Admin_PS'])
    CreateProfileComponent(saving, acm.FUserProfile['Mandate_Admin_PS'])

    # Signer Product Supervisor
    CreateProfileComponent(authorization, acm.FUserProfile['Mandate_Sign_PS'])

    # Save to DB (System user for ATS)
    profile = acm.FUserProfile['Mandate_System']
    CreateProfileComponent(saving, profile)


def CreateUserTracker():
    """
    Set up the initial text object containing the user groups for all the mandated traders in the DB.
    """
    mandatedTraders = GetAllMandatedTraders()
    tracker = UserTracker(USER_TRACKER_TEXT_OBJECT)
    tracker.InitialSetup(mandatedTraders)
    getLogger().info('Created text object (%s) that stores user and user group data.' % USER_TRACKER_TEXT_OBJECT)


def CreateUserGroups():
    """
    Create the Africa Supervisor user group.
    """
    exist = acm.FUserGroup[SUPERVISOR_GROUP_NAME]
    if not exist:
        organisation = acm.FOrganisation[SUPERVISOR_ORGANISATION]
        if organisation:
            group = acm.FUserGroup()
            group.Name(SUPERVISOR_GROUP_NAME)
            group.Description('')
            group.Organisation(organisation)
            group.Commit()
            getLogger().info('Created User Group - %s' % SUPERVISOR_GROUP_NAME)
        else:
            getLogger().error('[ERROR] Could not find organisation (%s)' % SUPERVISOR_ORGANISATION)
    else:
        getLogger().info('Did not create User Group - already exists (%s)' % SUPERVISOR_GROUP_NAME)


def AddComponentsToSupervisorProfile():
    """
    Add all the specified components to the Africa Supervisor profile.
    """
    profile = acm.FUserProfile[SUPERVISOR_PROFILE_NAME]
    if profile:
        for componentName in SUPERVISOR_COMPONENTS:
            component = acm.FComponent.Select('name="%s"' % componentName)[0]
            if component:
                CreateProfileComponent(component, profile)
            else:
                getLogger().error("[ERROR] Could not select component (%s)" % componentName)
    else:
        getLogger().error('[ERROR] %s profile does not exist.' % SUPERVISOR_PROFILE_NAME)


def CreateViolationsTextObject():
    selection = acm.FCustomTextObject.Select('name="Violations" subType="Mandates"')
    if len(selection) == 0:
        getLogger().info('Creating Violations Text Object')

        to = acm.FCustomTextObject()
        to.Name('Violations')
        to.SubType('Mandates')
        to.Text('{}')
        to.Commit()

        getLogger().info('Violations Text Object has been created.')
    elif len(selection) > 1:
        getLogger().error('[ERROR] Multiple Violations text objects are present in the DB')
    else:
        getLogger().info('Violations Text Object already exists')


def PrintHeader():
    getLogger().info('*****************************************************')
    getLogger().info('FIS Global (Ltd)')
    getLogger().info('Generic Trader Mandates - Once-off Installation Script\n')


def PrintFooter():
    getLogger().info('*****************************************************')


ael_variables = []
ael_gui_parameters = {'runButtonLabel':   '&&Install Mandates',
                      'hideExtraControls': False,
                      'windowCaption': 'RunScript to install Mandates package'}


def ael_main(ael_variables):
    PrintHeader()
    try:
        # Create all the required state charts
        CreateAllStateCharts()
        CreateAllChoiceLists()
        CreateAllLimitSpecifications()
        # CreateAllUserProfiles()
        # CreateAllOperations()
        CreateUserTracker()
        # CreateUserGroups()
        # AddComponentsToSupervisorProfile()
        CreateViolationsTextObject()
    except Exception as e:
        import sys
        import traceback

        getLogger().error('Exception occurred. %s' % e)
        getLogger().error('*****************************************************')
        getLogger().error(traceback.print_exc(file=sys.stdout))
        getLogger().error('*****************************************************')

    PrintFooter()
