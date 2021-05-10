""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingExportImportStrategy.py"
import acm
import itertools
import FOperationsAMBAMessage
from FAccountingMember import Member, MemberSpecification, ReferenceType, Matcher, AttributeMatcher, SeqnbrObjectFinder, FilterHandler

class ExportImportStrategy:

    @staticmethod
    def BookExportImportStrategy(partialExport = False):
        memberSpecification0 = MemberSpecification("AccountingPeriods", acm.FAccountingPeriod, ReferenceType.CHILDREN)
        memberSpecification1 = MemberSpecification("CategoryChlItem", acm.FChoiceList, ReferenceType.SINGLE_OBJECT)
        memberSpecification2 = MemberSpecification("TAccount", acm.FTAccount, ReferenceType.SINGLE_OBJECT, memberSpecification1)
        memberSpecification3 = MemberSpecification("ChartOfAccounts", acm.FChartOfAccount, ReferenceType.CHILDREN, memberSpecification2)
        bookMembers = [Member("Book", acm.FBook, [memberSpecification0, memberSpecification3])]

        strategy = ExportImportStrategy(partialExport,
                                        acm.FBookMapping,
                                        "BookMappings",
                                        bookMembers,
                                        '{{AccountingPeriod,seqnbr}, {BookMapping, next_seqnbr}, {BookMapping, parent_seqnbr}, {BookMapping, previous_seqnbr}, {BookMapping, next_id}, {BookMapping, parent_id}, {BookMapping, previous_id}}')
        return strategy

    @staticmethod
    def TreatmentExportImportStrategy(filteredBooks, partialExport = False):
        bookFilterHandler = FilterHandler(filteredBooks, "Book")
        memberSpecification0 = MemberSpecification("BookLinks", acm.FBookLink, ReferenceType.COLLECTION, None, bookFilterHandler)
        treatmentMembers = [Member("Treatment", acm.FTreatment, [memberSpecification0])]

        strategy = ExportImportStrategy(partialExport,
                                        acm.FTreatmentMapping,
                                        "TreatmentMappings",
                                        treatmentMembers,
                                        '{{BookLink,seqnbr}, {TreatmentMapping, next_seqnbr}, {TreatmentMapping, parent_seqnbr}, {TreatmentMapping, previous_seqnbr}}',
                                        'BookLinks',
                                        filteredBooks,
                                        ['Book'])
        return strategy

    @staticmethod
    def AccountingInstructionExportImportStrategy(filteredTreatments, filteredBooks=None, partialExport = False):
        treatmentFilterHandler = FilterHandler(filteredTreatments, "Treatment")
        memberSpecification0 = MemberSpecification("TreatmentLinks", acm.FTreatmentLink, ReferenceType.COLLECTION, None, treatmentFilterHandler, ['Book', filteredBooks])
        memberSpecification1 = MemberSpecification("CategoryChlItem", acm.FChoiceList, ReferenceType.SINGLE_OBJECT)
        accountingInstructionMembers = [Member("AccountingInstruction", acm.FAccountingInstruction, [memberSpecification0, memberSpecification1])]

        strategy = ExportImportStrategy(partialExport,
                                        acm.FAccountingInstructionMapping,
                                        "AccountingInstructionMappings",
                                        accountingInstructionMembers,
                                        '{{TreatmentLink,seqnbr}, {AccInstructionMapping, next_seqnbr}, {AccInstructionMapping, parent_seqnbr}, {AccInstructionMapping, previous_seqnbr}}',
                                        'TreatmentLinks',
                                        filteredBooks,
                                        ['BookLink', 'Book'])
        return strategy

    @staticmethod
    def TAccountExportImportStrategy(partialExport = False):
        attributeMatchers = list()

        attributeMatchers.append(AttributeMatcher('JVD.DEBIT_OR_CREDIT', 'DebitOrCredit', True))
        attributeMatchers.append(AttributeMatcher('JVD.POSTING_FIELD_NAME', 'PostingFieldName', False))
        attributeMatchers.append(AttributeMatcher('JVD.ACCOUNTING_INSTRUCTION.NAME', 'AccountingInstruction.Name', False))
        matcher = Matcher(acm.FJournalValueDefinition, attributeMatchers)
        seqnbrObjectFinder = SeqnbrObjectFinder(matcher, 'JVD', 'JVD')
        taccountMembers = [Member("TAccountAllocationLink", acm.FTAccountAllocationLink, [], seqnbrObjectFinder)]

        strategy = ExportImportStrategy(partialExport,
                                        acm.FTAccountMapping,
                                        "TAccountMappings",
                                        taccountMembers,
                                        '{{TAccountAllocLink,seqnbr}, {TAccountMapping, next_seqnbr}, {TAccountMapping, parent_seqnbr}, {TAccountMapping, previous_seqnbr}}')
        return strategy

    def __init__(self, partialExport, mappingClass, mappingAttribute, rootMembers, fieldsToRemoveFromMessage='', mappingObjectAttribute='', selectedObjects = None, filterProperties = None):
        self.__referenceMap = {}
        self.__partialExport = partialExport
        self.__mappingObjectClass = mappingClass
        self.__mappingAttribute = mappingAttribute
        self.__rootMembers = rootMembers
        self.__fieldsToRemoveFromMessage = fieldsToRemoveFromMessage
        self.__mappingObjectsToConnect = {}
        self.__messageGenerator = acm.FAMBAMessageGenerator()
        self.__mappingObjectAttribute = mappingObjectAttribute
        self.__selectedObjects = selectedObjects
        self.__filterProperties = filterProperties


    def __GetObjectsToExport(self, objectToExport):
        memberObjectsToExport = []
        for member in self.__rootMembers:
            memberDefinition = member.GetMemberDefinition(objectToExport)
            if memberDefinition != None:
                memberObjectsToExport.extend(memberDefinition.GetObjectsToExport())
        return memberObjectsToExport

    def GetObjectsToExport(self, objectsToExport):
        memberObjectsToExport = []
        for objectToExport in objectsToExport:
            derivedObjects = self.__GetObjectsToExport(objectToExport)
            for derivedObject in derivedObjects:
                if not derivedObject in memberObjectsToExport:
                    memberObjectsToExport.append(derivedObject)
        return memberObjectsToExport

    def __ExtractProperty(self, anObject, propertyList):
        for property in propertyList:
            anObject = anObject.GetProperty(property)
        if anObject in self.__selectedObjects:
            return True
        return False

    def GetMappingsAndQueriesToExport(self, objectsToExport):
        keyfunc = (lambda mapping: mapping.GetProperty("Type"))

        if self.__mappingObjectAttribute:
            objectsToExport = list(itertools.chain(*[objectToExport.GetProperty(self.__mappingObjectAttribute) for objectToExport in objectsToExport]))

        rawMappings = list(itertools.chain(*[objectToExport.GetProperty(self.__mappingAttribute) for objectToExport in objectsToExport]))

        mappings = list()
        if self.__selectedObjects:
            for mapping in rawMappings:
                if(self.__ExtractProperty(mapping, self.__filterProperties)):
                    mappings.append(mapping)
        else:
            mappings = rawMappings

        sortedMappingKeyTuples = [(key, list(group)) for key, group in itertools.groupby(sorted(mappings, key=keyfunc), keyfunc)]

        mappingsToExport = list()

        for mappingType, sortedListOfMappings in sortedMappingKeyTuples:
            if self.__mappingObjectClass != acm.FBookMapping:
                self.__AddParentMappings(sortedListOfMappings)
            mappingsToExport.extend(sortedListOfMappings)

        mappingsToExport = [mapping.Clone() for mapping in mappingsToExport]
        self.__RemoveUnExportedIdReferences(mappingsToExport)

        mappingsAndQueriesToExport = self.__AddQueries(mappingsToExport)

        return mappingsAndQueriesToExport

    def __GetMappingFromId(self, id):
        mapping = None
        if id != '':
            mapping = self.__mappingObjectClass.Select01("id = %s" % id, None)
        return mapping

    def __AddParentMappings(self, mappingsToExport):
        parentMappings = list()

        for mapping in mappingsToExport:
            parentId = mapping.ParentId()
            while parentId:
                parent = self.__GetMappingFromId(parentId)
                if parent not in parentMappings:
                    parentMappings.append(parent)
                parentId = parent.ParentId()

        parentMappings.reverse()

        parentMappings = [mapping for mapping in parentMappings if mapping not in mappingsToExport]
        mappingsToExport.extend(parentMappings)

        mappingsToExport.reverse()

    def __RemoveUnExportedIdReferences(self, mappingsToExport):
        ids = {mapping.Id() for mapping in mappingsToExport}

        for mapping in mappingsToExport:
            if mapping.ParentId() and mapping.ParentId() not in ids:
                mapping.ParentId("")
            if mapping.PreviousId() and mapping.PreviousId() not in ids:
                mapping.PreviousId("")
            if mapping.NextId() and mapping.NextId() not in ids:
                mapping.NextId("")

    def __GetQueries(self, mappingsToExport):
        for mapping in mappingsToExport:
            if mapping.Query():
                yield mapping.Query()

    def __AddQueries(self, mappingsToExport):
        queriesToExport = list()
        for query in self.__GetQueries(mappingsToExport):
            if query not in queriesToExport:
                queriesToExport.append(query)
        mappingsToExport.reverse()
        mappingsToExport.extend(queriesToExport)
        mappingsToExport.reverse()
        return mappingsToExport

    def CustomizeMessageGenerator(self, showAll = True):
        self.__messageGenerator.ShowAll(showAll)
        if self.__fieldsToRemoveFromMessage != '':
            self.__messageGenerator.RemoveFields(self.__fieldsToRemoveFromMessage)
        self.__messageGenerator.ShowNiceEnumNames(True)

        self.__messageGenerator.AddRefFields('{{TAccountAllocLink, jvd, JournalValueDef, debit_or_credit}, {TAccountAllocLink, jvd, JournalValueDef, posting_field_name}, {TAccountAllocLink, jvd, JournalValueDef, accounting_instruction}, {TAccountMapping, t_account_alloc_link, TAccountAllocLink, jvd}, {TAccountMapping, t_account_alloc_link, TAccountAllocLink, chart_of_account}, {TAccountMapping, t_account_alloc_link, TAccountAllocLink, treatment}, {TreatmentMapping, book_link, BookLink, treatment}, {TreatmentMapping, book_link, BookLink, book}, {AccInstructionMapping, book_link, BookLink, treatment}, {AccInstructionMapping, book_link, BookLink, book}, {AccInstructionMapping, treatment_link, TreatmentLink, book}, {AccInstructionMapping, treatment_link, TreatmentLink, treatment}, {AccInstructionMapping, treatment_link, TreatmentLink, accounting_instruction}, {TAccountMapping, treatment_link, TreatmentLink, book}, {TAccountMapping, treatment_link, TreatmentLink, treatment}, {TAccountMapping, treatment_link, TreatmentLink, accounting_instruction}}')

    def GetMessageGenerator(self):
        return self.__messageGenerator

    def ManageMappingObject(self, mappingObject, msg):
        if mappingObject.IsKindOf(acm.FTreatmentMapping):
            self.__AddBookLink(mappingObject, msg)
        if mappingObject.IsKindOf(acm.FAccountingInstructionMapping):
            self.__AddBookLink(mappingObject, msg)
            self.__AddTreatmentLink(mappingObject, msg)
        if mappingObject.IsKindOf(acm.FTAccountMapping):
            self.__AddTAccountLink(mappingObject, msg)
            self.__AddTreatmentLink(mappingObject, msg)

    def AddSeqnbrObjects(self, anObject, messageString):
        for member in self.__rootMembers:
            if member.GetMemberDomain() == anObject.Class():
                seqnbrObjectFinder = member.GetSeqnbrObjectFinder()
                if seqnbrObjectFinder:
                    seqnbrObjectFinder.FindAndAddToObject(anObject, messageString)

    def __AddTAccountLink(self, mappingObject, msg):
        attributeMatchers = list()
        attributeMatchers.append(AttributeMatcher('T_ACCOUNT_ALLOC_LINK.CHART_OF_ACCOUNT.BOOK.NAME', 'ChartOfAccount.Book.Name', False))
        attributeMatchers.append(AttributeMatcher('T_ACCOUNT_ALLOC_LINK.CHART_OF_ACCOUNT.T_ACCOUNT.NUMBER', 'ChartOfAccount.TAccount.Number', False))
        attributeMatchers.append(AttributeMatcher('T_ACCOUNT_ALLOC_LINK.JVD.ACCOUNTING_INSTRUCTION.NAME', 'JVD.AccountingInstruction.Name', False))
        attributeMatchers.append(AttributeMatcher('T_ACCOUNT_ALLOC_LINK.JVD.DEBIT_OR_CREDIT', 'JVD.DebitOrCredit', True))
        attributeMatchers.append(AttributeMatcher('T_ACCOUNT_ALLOC_LINK.JVD.POSTING_FIELD_NAME', 'JVD.PostingFieldName', False))
        attributeMatchers.append(AttributeMatcher('T_ACCOUNT_ALLOC_LINK.TREATMENT.NAME', 'Treatment.Name', False))
        matcher = Matcher(acm.FTAccountAllocationLink, attributeMatchers)
        seqnbrObjectFinder = SeqnbrObjectFinder(matcher, 'TAccountAllocationLink', 'T_ACCOUNT_ALLOC_LINK')
        if(not seqnbrObjectFinder.HasNullReference(msg)):
            seqnbrObjectFinder.FindAndAddToObject(mappingObject, msg)

    def __AddBookLink(self, mappingObject, msg):
        attributeMatchers = list()
        attributeMatchers.append(AttributeMatcher('BOOK_LINK.TREATMENT.NAME', 'Treatment.Name', False))
        attributeMatchers.append(AttributeMatcher('BOOK_LINK.BOOK.NAME', 'Book.Name', False))
        matcher = Matcher(acm.FBookLink, attributeMatchers)
        seqnbrObjectFinder = SeqnbrObjectFinder(matcher, 'BookLink', 'BOOK_LINK')
        if(not seqnbrObjectFinder.HasNullReference(msg)):
            seqnbrObjectFinder.FindAndAddToObject(mappingObject, msg)

    def __AddTreatmentLink(self, mappingObject, msg):
        attributeMatchers = list()
        attributeMatchers.append(AttributeMatcher('TREATMENT_LINK.TREATMENT.NAME', 'Treatment.Name', False))
        attributeMatchers.append(AttributeMatcher('TREATMENT_LINK.BOOK.NAME', 'Book.Name', False))
        attributeMatchers.append(AttributeMatcher('TREATMENT_LINK.ACCOUNTING_INSTRUCTION.NAME', 'AccountingInstruction.Name', False))
        matcher = Matcher(acm.FTreatmentLink, attributeMatchers)
        seqnbrObjectFinder = SeqnbrObjectFinder(matcher, 'TreatmentLink', 'TREATMENT_LINK')
        if(not seqnbrObjectFinder.HasNullReference(msg)):
            seqnbrObjectFinder.FindAndAddToObject(mappingObject, msg)
