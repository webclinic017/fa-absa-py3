"""
    This module creates the Authorization Process state chart. This business process is used for authorizing mandate
    changes.

    It is possible to have more than one Authorizer Group.
"""


class StateChartAuthorizationProcess(object):
    """
    This state chart definition is used for the business processes created when a violation occurs.
    """

    # State chart properties
    NAME = 'GenericMandatesAuthorization_v3'
    LIMIT = 'Unlimited'
    LAYOUT = "Rejected,272,305;Ready,100,115;Authorization stage 1,272,116;Authorized,479,115;Apply Changes,729,503;"

    # State & event name config
    STATE_READY = 'Ready'
    STATE_AUTHORIZED = 'Authorized'
    STATE_REJECTED = 'Rejected'
    STATE_ERROR = 'Error'
    STATE_APPLY = 'Active'

    STATE_PENDING_ACTIVATION_APPROVAL = 'Pending activation approval'
    STATE_PENDING_UPDATE_APPROVAL = 'Pending update approval'

    EVENT_SAVE_MANDATE = 'Save to DB'
    EVENT_REVERT = 'Revert'
    EVENT_APPROVE = 'Approve'
    EVENT_DENY = 'Reject'
    EVENT_START = 'Start authorization process'
    EVENT_SUBMIT_UPDATE = 'Submit mandate update'
    EVENT_CREATE = 'Create mandate'
    EVENT_ACTIVATION_REQUEST = "Request mandate activation"

    def __init__(self, numberOfAuthorizations):
        # Set up custom state
        self.authorizationStates = map(lambda x: "Authorization stage %s" % (x + 1), list(range(0, numberOfAuthorizations)))

        level1Y = 100
        level2Y = 300
        level3Y = 500
        spaceX = 350
        startX = 100
        endX = startX + (spaceX * (numberOfAuthorizations + 1)) if numberOfAuthorizations > 1 else startX + (spaceX * (numberOfAuthorizations + 2))

        readyPosition = "%s,%s,%s;" % (self.STATE_READY, startX, level1Y)

        createdPosition = "%s,%s,%s;" % (self.STATE_PENDING_ACTIVATION_APPROVAL, startX + spaceX, level1Y)

        updateSubmittedPosition = "%s,%s,%s;" % (self.STATE_PENDING_UPDATE_APPROVAL, startX + spaceX, level3Y)

        rejectedPosition = "%s,%s,%s;" % (self.STATE_REJECTED, startX + spaceX + spaceX, level2Y) if numberOfAuthorizations > 0 else ""

        authorizedPosition = "%s,%s,%s;" % (self.STATE_AUTHORIZED, endX, level3Y)
        applyPosition = "%s,%s,%s;" % (self.STATE_APPLY, (endX - spaceX), level3Y)

        authorizationStagePositions = ""

        for i in range(0, numberOfAuthorizations):
            statePosition = "%s,%s,%s;" % (self.authorizationStates[i], startX + (spaceX * (2 + i)), level1Y)
            authorizationStagePositions = "%s%s" % (authorizationStagePositions, statePosition)

        self.LAYOUT = "%s%s%s%s%s%s%s" % (readyPosition, authorizationStagePositions, createdPosition,
                                          updateSubmittedPosition, authorizedPosition, rejectedPosition, applyPosition)

    def getDefinition(self):
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
        # Define ready state transitions
        definition = {
            self.STATE_READY: {
                self.EVENT_CREATE: self.STATE_PENDING_ACTIVATION_APPROVAL
            },

            self.STATE_PENDING_ACTIVATION_APPROVAL: {
                self.EVENT_APPROVE: self.STATE_AUTHORIZED if len(self.authorizationStates) == 0 else self.authorizationStates[0]
            },

            self.STATE_PENDING_UPDATE_APPROVAL: {
                self.EVENT_APPROVE: self.STATE_AUTHORIZED if len(self.authorizationStates) == 0 else
                self.authorizationStates[0]
            },

            self.STATE_AUTHORIZED: {
                self.EVENT_SAVE_MANDATE: self.STATE_APPLY
            },

            self.STATE_APPLY: {
                self.EVENT_SUBMIT_UPDATE: self.STATE_PENDING_UPDATE_APPROVAL
            }
        }

        if len(self.authorizationStates) > 0:
            # Define rejected state transitions
            definition[self.STATE_REJECTED] = {
                self.EVENT_SUBMIT_UPDATE: self.STATE_PENDING_UPDATE_APPROVAL,
                self.EVENT_ACTIVATION_REQUEST: self.STATE_PENDING_ACTIVATION_APPROVAL
            }

        # Define transitions for authorization stage states
        for i, authorizationState in enumerate(self.authorizationStates):
            definition[authorizationState] = {
                self.EVENT_APPROVE: self.STATE_AUTHORIZED if i == len(self.authorizationStates) - 1 else self.authorizationStates[i + 1],
                self.EVENT_DENY: self.STATE_REJECTED
            }

        return definition

    def getLayout(self):
        return self.LAYOUT

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def getLimit(cls):
        return cls.LIMIT
