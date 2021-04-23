""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationIdentification.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FReconciliationIdentification

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
from FPositionCreator import FPositionSpecification, FPositionDefinition
from FReconciliationValueMapping import GetCalculator
import hashlib, base64, itertools

logger = FAssetManagementUtils.GetLogger()


def PrintIdentificationReport(reconciliationItem, debug=False):
    """Print a report detailing the identification processing for a stored reconciliation item."""
    import pprint
    import FBusinessProcessUtils
    import FReconciliationSpecification

    # Report general information about the item
    doc = reconciliationItem.ReconciliationDocument()
    print('-' * 120)
    print('Identification information for Reconciliation Item', reconciliationItem.Oid())
    print()
    print('Reconciliation Specification:', doc.ReconciliationName())
    print('Reconciliation Document:', doc.SourceId())
    print('Start Date:', (doc.CustomStartDate() if doc.StartDate() == 'Custom Date' else doc.StartDate()))
    print('End Date:', (doc.CustomEndDate() if doc.EndDate() == 'Custom Date' else doc.EndDate()))
    try:
        reconSpec = FReconciliationSpecification.FReconciliationSpecification(doc.ReconciliationName(), relaxValidation = True)
    except Exception as e:
        print('Invalid Reconciliation Specification:', e)
        return
    bp = FBusinessProcessUtils.GetBusinessProcessWithCache(reconciliationItem, reconSpec.StateChartName())
    if bp:
        print('Business Process:', bp.Oid())
        print('Current State:', bp.CurrentStep().State().Name())

    attributeType = ''
    if reconciliationItem.ExternalValues().IsEmpty():
        attributeType = 'Internal'
        print('This item does not have any external values')
    elif reconciliationItem.InternalValues().IsEmpty():
        attributeType = 'External'
        print('This item does not have any internal values')

    storedValues = reconciliationItem.ExternalValues() if \
                   not reconciliationItem.ExternalValues().IsEmpty() else \
                   reconciliationItem.InternalValues()

    # Report attribute values before and after manipulation by hooks
    print()
    pp = pprint.PrettyPrinter(indent=4)

    storedAttributeValues = {}
    for key in storedValues.Keys():
        storedAttributeValues[str(key)] = str(storedValues.At(key))
    print('%s values of this reconciliation item' % attributeType)
    pp.pprint(storedAttributeValues)
    print()
    attributes = FIdentificationEngine.GetReconciliationItemAttributes(
        reconciliationItem,
        reconSpec.ExternalAttributeMap(),
       reconSpec.GetIdentificationValues)
    print('Attributes to be used in searching:')
    pp.pprint(attributes)
    print()

    def GetWildcardedAttributes(query):
        # Helper function for identifying incomplete ASQL queries
        def GetNodes(node, nodes=[]):
            # pylint: disable-msg=W0102
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    GetNodes(n, nodes)
            if node and node.IsKindOf(acm.FASQLNode):
                nodes.append(node)
            return nodes

        attributeNodes = (n for n in GetNodes(query) if n.IsKindOf(acm.FASQLAttrNode))
        return set([str(n.AsqlAttribute().AttributeString()) for n in attributeNodes \
                    if str(n.AsqlValue()) == 'None'])

    # Report the result of all identification rules applied to the item
    for i, rule in enumerate(reconSpec.IdentificationRules()):
        try:
            posSpec = FPositionSpecification(rule.StoredQuery())
        except ValueError as e:
            print('Rule %i "%s" is invalid: %s' % (i+1, rule.QueryName(), e))
        else:
            try:
                pos = posSpec.GetInfantPositionFromDict(attributes, False)
                itemCount = len(pos.InfantPositionStoredQuery().Query().Select())
                if itemCount:
                    print('Rule %i "%s" is a MATCH with %d trade(s).' % \
                        (i+1, rule.QueryName(), itemCount))
                else:
                    print('Rule %i "%s" returns 0 items.' % (i+1, rule.QueryName()))
            except ValueError:
                pos = posSpec.GetInfantPositionFromDict(attributes, True)
                query = pos.InfantPositionStoredQuery().Query()
                print('Rule %i "%s" gives an invalid query [missing: %s].' % \
                    (i+1, rule.QueryName(), ', '.join(GetWildcardedAttributes(query))))
                if debug:
                    print('Query:', query)


def _LoadStoredQuery(name):
    """Load a stored query by name. A shared query should be loaded in preference to
    user stored versions, with a fallback to support legacy setups."""
    storedQuery = acm.FStoredASQLQuery.Select01('name="%s" and user=None' % name,
                    'Failed to load shared query "%s"' % name)
    if not storedQuery:
        storedQuery = acm.FStoredASQLQuery[name]
        if storedQuery:
            logger.warn('Using a user-specific query "%s".' +
                    ' This should be converted to a shared equivalent.', name)
    return storedQuery


class FIdentificationRules(list):
    """Represents an ordered collection of stored Identification Rule objects.
    Has a FindPosition method that returns the first non empty ACM query spawned by
    these Identification Rules """

    def __init__(self, ruleName):
        super(FIdentificationRules, self).__init__()
        self._ruleName = ruleName
        try:
            self._parameter = acm.GetDefaultContext().GetExtension(
                'FParameters',
                'FObject',
                self.Name()).Value()
        except AttributeError:
            raise AssertionError("Cannot find FParameter named %s" % self.Name())
        self._LoadRules()

    def Name(self):
        return self._ruleName

    def FindPosition(self, attributeValueDict = None, trade = None,
                           relaxValidation = False, allowIncompletePositions = False):
        """Finds the first position specification (ACM query) with a matching filter part.
        Then returns a position found or spawned by that position specification and the
        attributeValueDict (taken from the external file or a FTrade).
        """
        errorList = []
        if relaxValidation is False:
            assert attributeValueDict or trade

        for rule in self:
            position = None

            try:
                position = rule.FindPosition(attributeValueDict or trade, allowIncompletePositions)
            except Exception as e:
                # Don't abort if a single rule check fails. Instead, track the errors to be raised
                # if no match is ultimately found.
                errorList.append(str(e))
            if position:
                # Make sure the Rule returned some objects
                try:
                    if len(position.InfantPositionStoredQuery().Query().Select()) > 0:
                        logger.debug('Match found using identification rule "%s"', rule.QueryName())
                    else:
                        logger.debug('Identification rule "%s" yielded no results', rule.QueryName())
                        position = None
                except Exception as e:
                    position = None
                    errorList.append(str(e))
            if errorList:
                error = 'Error(s) while searching - ' + ', '.join(errorList)
                raise Exception(error)
            return position
            

    def _GenerateQueries(self):
        i = 1
        queryFunc = lambda i: self._parameter.GetString('Rule' + str(i), '<NOT_FOUND>').strip()
        while queryFunc(i) != '<NOT_FOUND>':
            yield i, queryFunc(i)
            i += 1

    def _LoadRules(self):
        """
        Identification rules are stored as FParameter extensions. Parameters are named
        "RuleX" where X is a sequentially increasing number (e.g. "Rule1", "Rule2" ...)
        and set to a position specification (ACM queryName)
        """
        del self[:]
        for ruleNumber, queryName in self._GenerateQueries():
            storedQuery = _LoadStoredQuery(queryName)
            assert storedQuery, "Rule %i is specified as %s, but no such query exists" % (ruleNumber, queryName)
            self.append(FIdentificationRule(storedQuery))
        assert len(self) > 0, 'At least one query parameter (Rule1) must be defined'


class FIdentificationRule(object):

    def __init__(self, storedQuery):
        # Make sure that each identification rule has a unique copy of the ID rules query
        self._storedQuery = storedQuery.StorageImage()
        self._storedQuery.StorageSetNew()

    def QueryName(self):
        return self._storedQuery.Name()

    def StoredQuery(self):
        return self._storedQuery

    def FindPosition(self, externalValuesDictOrACMObject, allowIncompletePositions = False):
        """Returns the FPositionDefinition that matches the position specification and the
        externalValuesDictOrACMObject likely coming from an external file or a FTrade.
        This method uses PositionCreator code.
        """
        posSpec = FPositionSpecification(self.StoredQuery(), allowIncompletePositions)
        if isinstance(externalValuesDictOrACMObject, dict):
            #In case we have an external value to make a position from
            return posSpec.GetInfantPositionFromDict(externalValuesDictOrACMObject, allowIncompletePositions)
        elif isinstance(externalValuesDictOrACMObject, acm._pyClass(acm.FTrade)):
            #In case we have a trade instead
            return posSpec.GetPosition(externalValuesDictOrACMObject)
        else:
            raise ValueError("Must supply trade or dictionary to find position for rule")
        return None


class FExternalAttributeMap(dict):
    """A stored mapping of externally defined attribute names (e.g. those used in
       reconciliation items) to ACM attribute or column names.
    """
    def __init__(self, name):
        super(FExternalAttributeMap, self).__init__()
        self._name = name
        if self._name:
            self._LoadMap()

    def Name(self):
        return self._name

    def _LoadMap(self):
        self.clear()
        ext = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', self._name)
        if ext:
            parameters = ext.Value()
            for k in parameters.Keys():
                self[str(k)] = self._GetParameterValue(parameters.At(k))
        else:
            raise ValueError('Failed to load FParameters extension with name ' + self._name + '"')

    @staticmethod
    def _GetParameterValue(value):
        values = str(value).strip().split(',')
        if len(values) == 1:
            return values[0]
        return [v.strip() for v in values]


class FIdentificationEngine(object):
    """An engine for the identification of reconciliation items as ACM objects."""

    def __init__(self, reconciliationInstance):
        self.reconciliationInstance = reconciliationInstance
        self._universe = None
        self._identifiedItemsDict = dict()

    def ReconciliationInstance(self):
        return self.reconciliationInstance

    @staticmethod
    def Identified(workflow, acmObject):
        workflow.ReconciliationItem().Subject(acmObject)
        workflow.ACMObject(acmObject)
        workflow.IsIdentified(True)

    def IdentifiedObjects(self):
        return list(itertools.chain(*[obj for obj in self._identifiedItemsDict.values()]))

    def AddIdentifiedObject(self, reconItem, obj):
        assert reconItem and obj
        if not self._identifiedItemsDict.has_key(reconItem):
            self._identifiedItemsDict[reconItem] = list()
        self._identifiedItemsDict[reconItem].append(obj)

    def GetUniverse(self):
        if self._universe is None:
            self._universe = FReconciliationUniverse(self.reconciliationInstance)
        return self._universe

    def MissingObjects(self):
        for missingObj in self.GetUniverse().GetMissingObjects():
            yield missingObj

    def InternalValuesForMissingObject(self, missingObject):
        return self.GetUniverse().InternalValuesAt(missingObject)

    @staticmethod
    def _QueryHash(query):
        ''' Parent FObject.Hash() doesn't appear to behave correctly. Use an MD5 hash
            instead, encoding to base64 to work around name length limitations (31 chars).
        '''
        def GetNodes(node, nodes=[]):
            # pylint: disable-msg=W0102
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    GetNodes(n, nodes)
            if node and node.IsKindOf(acm.FASQLNode):
                nodes.append(node)
            return nodes

        attributeNodeValues = [str(node.AsqlValue()) for node in GetNodes(query) if
                               node.IsKindOf(acm.FASQLAttrNode)]

        h = hashlib.md5()
        h.update(str(attributeNodeValues))
        return base64.standard_b64encode(h.digest())

    def IdentifyItems(self):
        ''' Attempt to identify ACM objects for reconciliation items requiring identification.
        '''
        reconItems = self.ReconciliationInstance().ReconciliationItems()
        workflows = self.ReconciliationInstance().Workflows()
        if reconItems:
            document = reconItems[0].ReconciliationDocument()
            documentItems = document.ReconciliationItems()
        else:
            documentItems = list()

        # The logic is slightly different in a position reconciliation setting
        previouslyIdentifiedSubjects = set([])
        if self.ReconciliationInstance().ReconciliationDocument().ObjectType() == 'Position':
            previouslyIdentifiedSubjects.update([self._QueryHash(item.Subject().Query())
                                                 for item in documentItems
                                                 if item.Subject() is not None
                                                 and not item in reconItems])
        else:
            previouslyIdentifiedSubjects.update([item.Subject() for item in documentItems
                                                 if not item.IsInfant()
                                                 and item.Subject() is not None
                                                 and not item in reconItems])
        for reconItem, workflow in zip(reconItems, workflows):
            if reconItem.Subject():
                ''' In case the recon item already is associated with an ACM object it needs
                    no identification work.
                '''
                previouslyIdentifiedSubject = self._QueryHash(reconItem.Subject().Query()) if reconItem.Subject().IsKindOf(acm.FStoredASQLQuery) else reconItem.Subject()
                if previouslyIdentifiedSubject in previouslyIdentifiedSubjects:
                    logger.debug('Subject of recon item %i (of class %s) already identified on previous line or run.' % (reconItem.Oid(), reconItem.Subject().ClassName()))
                    reconItem.Subject(None)
                    workflow.ErrorMessage('Subject already identified on previous line or run')
                    workflow.IsIdentified(False)
                else:
                    previouslyIdentifiedSubjects.add(previouslyIdentifiedSubject)
                    self.Identified(workflow, reconItem.Subject())
                    self.AddIdentifiedObject(reconItem, previouslyIdentifiedSubject)
            else:
                try:
                    self.Execute(reconItem, workflow)
                    if reconItem.Subject():
                        previouslyIdentifiedSubject = self._QueryHash(reconItem.Subject().Query()) if reconItem.Subject().IsKindOf(acm.FStoredASQLQuery) else reconItem.Subject()
                        if previouslyIdentifiedSubject in previouslyIdentifiedSubjects:
                            logger.info('Subject of recon item %i (of class %s) already identified on previous line or run.' \
                                    % (reconItem.Oid(), reconItem.Subject().ClassName()))
                            reconItem.Subject(None)
                            workflow.IsIdentified(False)
                            workflow.ErrorMessage('Subject already identified on previous line or run')
                        else:
                            previouslyIdentifiedSubjects.add(previouslyIdentifiedSubject)
                except Exception as err:
                    workflow.ErrorMessage(str(err))

    def Execute(self, reconItem, workflow):
        """Attempts to locate ACM objects for reconciliation items requiring identification.

        The reconciliation business process associated with the reconciliation item will be transitioned
        based on the outcome of the identification attempt. Returns a dictionary mapping
        identified reconciliation items to their located object.

        """

        reconciliationSpecification = self.reconciliationInstance.ReconciliationSpecification()
        logger.debug('Attempting to identify object(s) represented by reconciliation item %i',
                     workflow.ReconciliationItem().Oid())
        try:
            reconciliationItemAttributes = self.GetReconciliationItemAttributes(
               workflow.ReconciliationItem(),
                reconciliationSpecification.ExternalAttributeMap(),
                reconciliationSpecification.GetIdentificationValues)
            if reconciliationItemAttributes:
                position = reconciliationSpecification.IdentificationRules().FindPosition( reconciliationItemAttributes )
                identifiedObject = self._GetIdentifiedObjectFromPosition(workflow, position) or \
                                        self._GetIdentifiedObjectFromIdentificationHook(workflow, position)
                if identifiedObject:
                    self.Identified(workflow, identifiedObject)
                    self.AddIdentifiedObject(reconItem, identifiedObject)
                    logger.debug('Identified reconciliation item (row number {0}) as {1} (oid={2})'
                                ''.format(workflow.RowNumber() if workflow.RowNumber() else 'n/a',
                                          identifiedObject.Class().Name(),
                                          identifiedObject.Oid()))
        except Exception as err:
            msg = ('Failed identification processing reconciliation item %d: %s' %
                  (workflow.ReconciliationItem().Oid(), err))
            logger.error(msg)
            raise ValueError(msg)

    def _GetIdentifiedObjectFromPosition(self, workflow, position):
        objectType = workflow.ReconciliationInstance().ReconciliationDocument().ObjectType() if workflow else "Position"
        if position and position.InfantPositionStoredQuery():
            return position.InfantPositionStoredQuery() if objectType == "Position" else \
                self._GetIdentifiedObjectFromMatch(position.InfantPositionStoredQuery().Query().Select())

    def _GetIdentifiedObjectFromIdentificationHook(self, workflow, position):
        try:
            logger.debug("Calling identification hook if defined.")
            reconciliationItem = workflow.ReconciliationItem()
            reconciliationSpecification = workflow.ReconciliationInstance().ReconciliationSpecification()
            matchedObjects = position.InfantPositionStoredQuery().Query().Select() if \
                position and position.InfantPositionStoredQuery() else None
            return reconciliationSpecification.IdentifyReconciliationItem(
                None if matchedObjects is None else matchedObjects.InverseFilter(self.IdentifiedObjects()),
                reconciliationItem)
        except Exception as e:
            logger.error("Exception while calling custom identification hook: %s" % (e))

    @staticmethod
    def _GetIdentifiedObjectFromMatch(matchedObjects):
        identifiedObject = None
        if matchedObjects is None or matchedObjects.Size() == 0:
            logger.debug('Could not identify object')
        elif matchedObjects.Size() == 1:
            identifiedObject = matchedObjects[0]
        else:
            logger.debug("No single identified object. Matched: %s" % matchedObjects)
        return identifiedObject

    @staticmethod
    def GetReconciliationItemAttributes(reconciliationItem, attributeMapping=None, transformFunction=None):
        reconciliationItemAttributes = dict()
        try:
            externalValues = reconciliationItem.ExternalValues() or acm.FDictionary()
            if transformFunction:
                externalValues = transformFunction(externalValues.Clone())
            for key in externalValues.Keys():
                value = externalValues.At(key)
                if attributeMapping and key in attributeMapping:
                    key = attributeMapping[key]
                if isinstance(key, str):
                    # Do not overwrite pre-existing keys, which may have been set by the transform function
                    reconciliationItemAttributes[key] = reconciliationItemAttributes.get(key, value)
                else:
                    # Value may map to multiple keys (attributes)
                    for k in key:
                        reconciliationItemAttributes[k] = reconciliationItemAttributes.get(k, value)
        except Exception as e:
            msg = 'Failed to load attributes: ' + str(e)
            logger.error(msg)
            raise
        return reconciliationItemAttributes


class FReconciliationUniverse(object):

    def __init__(self, reconInstance):
        self._reconInstance = reconInstance
        self._maxQueries = None
        self._identifiedObjects = set()
        self._internalObjects = set()
        self._missingObjectsIntValsMap = dict()

    def ReconciliationInstance(self):
        return self._reconInstance

    def ReconciliationSpecification(self):
        return self.ReconciliationInstance().ReconciliationSpecification()

    def InternalObjects(self):
        """Returns all internal ACM objects that should be reconciled based on universe queries."""
        if not self._internalObjects:
            for queryName in self.ReconciliationSpecification().UniverseQueries():
                query = _LoadStoredQuery(queryName)
                if query:
                    objects = query.Query().Select()
                    logger.debug('Universe query "%s" contains %i items to be reconciled',
                        queryName, objects.Size())
                    self._internalObjects.update(objects)
                else:
                    logger.warn('Universe query "%s" could not be found', queryName)

        logger.debug('Found %i internal ACM object(s) requiring reconciliation',
            len(self._internalObjects))
        return self._internalObjects

    def IdentifiedObjects(self):
        if not self._identifiedObjects:
            for workflow in self.ReconciliationInstance().Workflows():
                if workflow.IsIdentified():
                    self._identifiedObjects.add(workflow.ACMObject())
        return self._identifiedObjects

    def MissingObjects(self):
        return self._missingObjectsIntValsMap.keys()

    def MissingObjectsInternalValues(self):
        return self._missingObjectsIntValsMap.items()

    def InternalValuesAt(self, missingObj):
        return self._missingObjectsIntValsMap.get(missingObj, None)

    def AddInternalValuesForObj(self, obj, internalValuesDict):
        self._missingObjectsIntValsMap[obj] = internalValuesDict

    def MaxSizeBreached(self):
        return len(self.MissingObjects()) >= self.MaxQueries()

    def MaxQueries(self):
        if self._maxQueries is None:
            self._maxQueries = int(self.ReconciliationSpecification().MaxUniverseQueries())
        return self._maxQueries

    def _LogBreachedLimit(self):
        logger.warn('The maximum number of allowed items to be missing in document is %i.' % self.MaxQueries())
        logger.warn('Found at least %i item(s) missing in document. Aborting 2-way reconciliation.' % len(self.MissingObjects()))

    def _CollectSimpleTypeMissingObjects(self):
        ''' No position reconciliation, we can find the missing (in the file)
            objects just by subtracting the Python sets
         '''
        missingObjects = self.InternalObjects() - self.IdentifiedObjects()
        for missingObj in missingObjects:
            try:
                position = self.ReconciliationSpecification().IdentificationRules().FindPosition(None, missingObj)
                positionQuery = position.InfantPositionStoredQuery() if position else None
                internalValues = FPositionSpecification.GetInternalValuesDict(positionQuery, missingObj)
            except:
                internalValues = {}
            self.AddInternalValuesForObj(missingObj, internalValues)
            if self.MaxSizeBreached():
                self._LogBreachedLimit()
                break

    def _CollectPositionMissingObjects(self):
        ''' Select all the trades from the internal universe queries and subtract the
            trades from the identified queries of the external file. Yield the set of
            missing positions from the internal universe that are missing in the
            reconciliation document.
        '''
        allIdentifiedExternalTrades = set()
        for i in self.IdentifiedObjects():
            # In a pos recon, these are queries
            allIdentifiedExternalTrades.update(i.Query().Select())
        missingTrades = self.InternalObjects() - allIdentifiedExternalTrades
        while missingTrades:
            trade = missingTrades.pop()

            # Check if we can create a position definition from this trade
            position = self.ReconciliationSpecification().IdentificationRules().FindPosition(None, trade)
            positionQuery = position.InfantPositionStoredQuery() if position else None
            if positionQuery:
                siblingTrades = positionQuery.Query().Select()
                assert trade in siblingTrades # Check that the trade itself is in the position
                logger.debug('Trade %i is part of a position (with %i trades) that is not among incoming positions.',
                             trade.Oid(), len(siblingTrades))
                missingTrades.difference_update(siblingTrades)
            else:
                logger.warn('Trade %i does not fit any of the identification rules!', trade.Oid())
                storedQuery = acm.FStoredASQLQuery()
                query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
                query.AddAttrNodeNumerical('Oid', trade.Oid(), trade.Oid())
                storedQuery.Query(query)
                positionQuery = FPositionDefinition.GetPosition(storedQuery).InfantPositionStoredQuery()

            assert positionQuery is not None, 'Stored position query is missing, which is not allowed.'

            # Check if missing position is a zero position
            calculator = GetCalculator(self.ReconciliationInstance())
            calculator.InsertItem(positionQuery)
            if not calculator.IsInactivePos():
                # Consider the position query to be missing in document only if it is a non-zero position
                internalValues = FPositionSpecification.GetInternalValuesDict(positionQuery, trade)
                self.AddInternalValuesForObj(positionQuery, internalValues)
            calculator.Clear()

            if self.MaxSizeBreached():
                self._LogBreachedLimit()
                # Rationale: Keep a subset for inspection/record keeping purposes
                break

    def _CollectMissingObjects(self):
        if self.ReconciliationInstance().ReconciliationDocument().ObjectType() == 'Position':
            try:
                if self.MaxQueries() < 0:
                    raise ValueError('The maximum number of missing items is a negative number')
            except ValueError:
                pass
            self._CollectPositionMissingObjects()
        else:
            self._CollectSimpleTypeMissingObjects()

    def GetMissingObjects(self):
        if not self.MissingObjects():
            universeQueries = self.ReconciliationSpecification().UniverseQueries()
            if universeQueries:
                logger.info('Running 2-way reconciliation. ')
                logger.info('Searching for items missing in document...')
                self._CollectMissingObjects()
                if self.MaxSizeBreached():
                    logger.info('Returning a subset (%i) of objects missing in document' %
                                 len(self.MissingObjects()))
                else:
                    logger.info('Found %i object(s) missing in document' %
                                len(self.MissingObjects()))
        return self.MissingObjects()