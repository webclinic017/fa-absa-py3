""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingMember.py"
import acm

from FOperationsAMBAMessage import CreateAmbaMessageFromString, CreateAmbaTableFromString

from FOperationsUtils import GetEnum

class ReferenceType:
    SINGLE_OBJECT    = 0
    COLLECTION       = 1
    CHILDREN         = 2

class MemberDefinition:
    def __init__(self, memberObject):
        assert memberObject != None
        self.__objectsThatDependOnMemberObject = acm.FArray()
        self.__memberObject = memberObject
        self.__objectsThatMemberObjectDependsOn = acm.FArray()

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        return self.MemberObject() == other.MemberObject()

    def MemberObject(self):
        return self.__memberObject

    def AddToObjectsThatDependOnMemberObject(self, obj):
        self.__objectsThatDependOnMemberObject.Add(obj)

    def AddToObjectsThatMemberObjectDependsOn(self, obj):
        self.__objectsThatMemberObjectDependsOn.Add(obj)

    def GetObjectsToExport(self):
        objectsToExport = acm.FArray()
        objectsToExport.AddAll(self.__objectsThatMemberObjectDependsOn)
        objectsToExport.Add(self.__memberObject)
        objectsToExport.AddAll(self.__objectsThatDependOnMemberObject)
        return objectsToExport

class AttributeMatcher:
    def __init__(self, ambaAttribute, acmAttribute, isEnum):
        self.__ambaAttribute = ambaAttribute
        self.__acmAttribute = acmAttribute
        self.__isEnum = isEnum

    def AddToQuery(self, query, ambaTable):
        value = ambaTable.GetAttribute(self.__ambaAttribute).GetCurrentValue()
        if self.__isEnum:
            enumType = self.__acmAttribute.split('.').pop() # e.g. Trade.TradeStatus -> TradeStatus
            value = GetEnum(enumType, value)
        query.AddAttrNode(self.__acmAttribute, 'EQUAL', value)

class Matcher:
    def __init__(self, acmClass, attributeMatchers):
        self.__acmClass = acmClass
        self.__attributeMatchers = attributeMatchers

    def __BuildQuery(self, ambaTable):
        query = acm.CreateFASQLQuery(self.__acmClass, 'AND')
        for attributeMatcher in self.__attributeMatchers:
            attributeMatcher.AddToQuery(query, ambaTable)
        return query

    def FindMatches(self, ambaTable):
        query = self.__BuildQuery(ambaTable)
        return query.Select()

class SeqnbrObjectFinder:
    def __init__(self, matcher, propertyToSet, seqnbrAttributeName):
        self.__matcher = matcher
        self.__propertyToSet = propertyToSet
        self.__seqnbrAttributeName = seqnbrAttributeName
        self.__seqnbrAndObjectMap = dict()
        self.__usedObjects = acm.FSet()

    def __FindUnusedObject(self, objects):
        for obj in objects:
            if not self.__usedObjects.Includes(obj):
                self.__usedObjects.Add(obj)
                return obj
        raise Exception('Could not find unused object.')
        return None

    def HasNullReference(self, messageString):
        ambaTable = CreateAmbaTableFromString(messageString)
        seqnbr = ambaTable.GetAttribute(self.__seqnbrAttributeName).GetCurrentValue()
        if seqnbr == '0':
            return True
        else:
            return False

    def FindAndAddToObject(self, obj, messageString):
        ambaTable = CreateAmbaTableFromString(messageString)
        seqnbr = ambaTable.GetAttribute(self.__seqnbrAttributeName).GetCurrentValue()
        if seqnbr not in self.__seqnbrAndObjectMap:
            matches = self.__matcher.FindMatches(ambaTable)
            if matches.IsEmpty():
                raise Exception('Could not find any matches in the database.')
            unusedObject = self.__FindUnusedObject(matches)
            self.__seqnbrAndObjectMap[seqnbr] = unusedObject
        if seqnbr not in self.__seqnbrAndObjectMap:
            raise Exception('Could not find object.')
        objectToAdd = self.__seqnbrAndObjectMap[seqnbr]
        obj.SetProperty(self.__propertyToSet, objectToAdd)

class ObjectFinder:
    def __init__(self):
        self.__seqnbrAndObjectMap = dict()
        self.__usedObjects = acm.FSet()

    def __FindUnusedObject(self, objects):
        for obj in objects:
            if not self.__usedObjects.Includes(obj):
                self.__usedObjects.Add(obj)
                return obj
        raise Exception('Could not find unused object.')
        return None

    def ParseMessage(self, messageString):
        ambaMessage = CreateAmbaMessageFromString(messageString)
        if ambaMessage.GetNameOfUpdatedTable() == 'JOURNALVALUEDEF':
            tables = ambaMessage.GetTableAndChildTables()
            assert len(tables) == 1
            table = tables[0]
            seqnbr = table.GetAttribute('SEQNBR').GetCurrentValue()
            if seqnbr not in self.__seqnbrAndObjectMap:
                debitOrCredit = table.GetAttribute('DEBIT_OR_CREDIT').GetCurrentValue()
                postingFieldName = table.GetAttribute('POSTING_FIELD_NAME').GetCurrentValue()
                accountingInstruction = table.GetAttribute('ACCOUNTING_INSTRUCTION.NAME').GetCurrentValue()
                query = acm.CreateFASQLQuery(acm.FJournalValueDefinition, 'AND')
                query.AddAttrNode('DebitOrCredit', 'EQUAL', GetEnum('DebitOrCredit', debitOrCredit))
                query.AddAttrNode('PostingFieldName', 'EQUAL', postingFieldName)
                query.AddAttrNode('AccountingInstruction.Name', 'EQUAL', accountingInstruction)
                result = query.Select()
                if result.IsEmpty():
                    raise Exception('Could not find the object in the database.')
                self.__seqnbrAndObjectMap[seqnbr] = self.__FindUnusedObject(result)

    def __FindObject(self, seqnbr):
        if seqnbr not in self.__seqnbrAndObjectMap:
            raise Exception('Could not find the object')
        return self.__seqnbrAndObjectMap[seqnbr]

    def AddMissingObjects(self, anObject, messageString):
        ambaMessage = CreateAmbaMessageFromString(messageString)
        if ambaMessage.GetNameOfUpdatedTable() == 'TACCOUNTALLOCLINK':
            tables = ambaMessage.GetTableAndChildTables()
            assert len(tables) == 1
            table = tables[0]
            seqnbr = table.GetAttribute('JVD').GetCurrentValue()
            jvd = self.__FindObject(seqnbr)
            anObject.JVD(jvd)

class FilterHandler:
    def __init__(self, filterValues, filterAttribute):
        self.__filterObjects = filterValues
        self.__filterObjectAttribute = filterAttribute

    def Includes(self, anObject):
        attributeValue = anObject.GetProperty(self.__filterObjectAttribute)
        if attributeValue in self.__filterObjects:
            return True
        return False

class MemberSpecification:
    def __init__(self, attributeName, attributeDomain, referenceType, memberSpecification = None, filterHandler = None, filteredObjects = None):
        self.__attributeName = attributeName
        self.__attributeDomain = attributeDomain
        self.__referenceType = referenceType
        self.__memberSpecification = memberSpecification
        self.__filterHandler = filterHandler
        self.__attributeObjectsPair = filteredObjects

    def GetAttributeName(self):
        return self.__attributeName

    def GetAttributeDomainName(self):
        return self.__attributeDomain

    def GetReferenceType(self):
        return self.__referenceType

    def AddToMemberDefinition(self, anObject, memberDefinition):
        referenceObject = anObject.GetProperty(self.__attributeName)
        if None != referenceObject:
            if None != self.__memberSpecification:
                if self.__referenceType == ReferenceType.COLLECTION:
                    for obj in referenceObject:
                        self.__memberSpecification.AddToMemberDefinition(obj, memberDefinition)
                elif self.__referenceType == ReferenceType.SINGLE_OBJECT:
                    self.__memberSpecification.AddToMemberDefinition(referenceObject, memberDefinition)
                elif self.__referenceType == ReferenceType.CHILDREN:
                    for obj in referenceObject:
                        self.__memberSpecification.AddToMemberDefinition(obj, memberDefinition)

            if self.__referenceType == ReferenceType.SINGLE_OBJECT:
                if not self.__filterHandler or (self.__filterHandler and self.__filterHandler.Includes(referenceObject)):
                    memberDefinition.AddToObjectsThatMemberObjectDependsOn(referenceObject)
            elif self.__referenceType == ReferenceType.COLLECTION:
                for o in referenceObject:
                    if not self.__filterHandler or (self.__filterHandler and self.__filterHandler.Includes(o)):
                        if self.__attributeObjectsPair != None:
                            if self.__attributeObjectsPair[1] != None:
                                if o.GetProperty(self.__attributeObjectsPair[0]) in self.__attributeObjectsPair[1]:
                                    memberDefinition.AddToObjectsThatDependOnMemberObject(o)
                            else:
                                memberDefinition.AddToObjectsThatDependOnMemberObject(o)
                        else:
                            memberDefinition.AddToObjectsThatDependOnMemberObject(o)
            elif self.__referenceType == ReferenceType.CHILDREN:
                # Since children are part of the parent message, we only add their references - see above.
                pass

class Member:
    def __init__(self, memberName, memberDomain, memberSpecifications, seqnbrObjectFinder = None):
        self.__memberName = memberName
        self.__memberDomain = memberDomain
        self.__memberSpecifications = memberSpecifications
        self.__seqnbrObjectFinder = seqnbrObjectFinder

    def GetSeqnbrObjectFinder(self):
        return self.__seqnbrObjectFinder

    def GetMemberName(self):
        return self.__memberName

    def GetMemberDomain(self):
        return self.__memberDomain

    def GetMemberSpecifications(self):
        return self.__memberSpecifications

    def CreateMemberDefinition(self, memberObject):
        memberDefinition = MemberDefinition(memberObject)
        for memberSpecification in self.__memberSpecifications:
            memberSpecification.AddToMemberDefinition(memberObject, memberDefinition)
        return memberDefinition

    def GetMemberDefinition(self, memberObject):
        memberDefinition = self.CreateMemberDefinition(memberObject)
        return memberDefinition


