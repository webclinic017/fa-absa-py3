""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/upgrade/FAccountingUpgradeUtils.py"
import acm

#-------------------------------------------------------------------------------
class AIType:
    MONEYFLOW                   = 1
    LEG                         = 2
    TRADE                       = 3
    COMBINATION                 = 4
    SETTLEMENT                  = 5

#-------------------------------------------------------------------------------
class TreatmentType:
    TRADE                       = 1
    SETTLEMENT                  = 2

#-------------------------------------------------------------------------------
class TAccountType:
    TRADE                       = 1
    SETTLEMENT                  = 2

#-------------------------------------------------------------------------------
AITypeNameDict= {
    AIType.MONEYFLOW            : "Money Flow",
    AIType.LEG                  : "Leg",
    AIType.TRADE                : "Trade",
    AIType.COMBINATION          : "Combination",
    AIType.SETTLEMENT           : "Settlement"
}


#-------------------------------------------------------------------------------
TreatmentTypeNameDict = {
    TreatmentType.TRADE         : "Trade",
    TreatmentType.SETTLEMENT    : "Settlement"
}

#-------------------------------------------------------------------------------
TAccountTypeNameDict = {
    TAccountType.TRADE         : "Trade",
    TAccountType.SETTLEMENT    : "Settlement"
}

#-------------------------------------------------------------------------------
class MappingBranchHandler(object):

    #-------------------------------------------------------------------------------
    @staticmethod
    def CreateMappingBranchList(mappings):
        branchList = []
        MappingBranchHandler.CreateMappingBranchListFromMappings(mappings, branchList)
        return branchList

    #-------------------------------------------------------------------------------
    @staticmethod
    def CreateMappingBranchListFromMappings(mappings, branchList):
        currentMapping = MappingBranchHandler.GetTopParent(mappings)
        while currentMapping:
            MappingBranchHandler.CreateMappingBranches(currentMapping, branchList, mappings)
            currentMapping = currentMapping.Next()

    """
    Use depth first to find last child in each branch, and then traverse all parents
    to create a list for each branch
    """

    #-------------------------------------------------------------------------------
    @staticmethod
    def CreateMappingBranches(parentMapping, branchList, mappings):
        currentChild = MappingBranchHandler.GetFirstChild(parentMapping, mappings)
        if currentChild:
            while currentChild:
                MappingBranchHandler.CreateMappingBranches(currentChild, branchList, mappings)
                currentChild = currentChild.Next()
        else:
            mappingBranch = MappingBranchHandler.TraverseParentsAndCreateMappingBranch(parentMapping)
            branchList.append(mappingBranch)

    #-------------------------------------------------------------------------------
    @staticmethod
    def GetFirstChild(parentMapping, mappings):
        firstChild = None
        childMappings = MappingBranchHandler.GetChildMappings(parentMapping, mappings)
        for child in childMappings:
            if child.Previous() == None:
                firstChild = child
                break
        return firstChild

    #-------------------------------------------------------------------------------
    @staticmethod
    def TraverseParentsAndCreateMappingBranch( mapping):
        mappingBranch = []
        while mapping:
            mappingBranch.insert(0, mapping)
            mapping = mapping.Parent()
        return mappingBranch

    #-------------------------------------------------------------------------------
    @staticmethod
    def GetChildMappings(parentMapping, mappings):
        childMappings = []
        for mapping in mappings:
            if mapping.Parent() and parentMapping.Oid() == mapping.Parent().Oid():
                childMappings.append(mapping)
        return childMappings

    #-------------------------------------------------------------------------------
    @staticmethod
    def GetTopParent(mappings):
        topParent = None
        for mapping in mappings:
            if mapping.Parent() == None and \
            mapping.Previous() == None:
                topParent = mapping
                break
        return topParent


#-------------------------------------------------------------------------------
# Create new treatment links
#-------------------------------------------------------------------------------
def CreateNewTreatmentLinks():
    existingTreatmentLinks = acm.FTreatmentLink.Select("book = 0")
    bookLinks = acm.FBookLink.Select("")
    newTreatmentLinks = CreateNewTreatmentLinksFromExistingTreatmentLinks(existingTreatmentLinks, bookLinks)
    return newTreatmentLinks

#-------------------------------------------------------------------------------
def CreateNewTreatmentLinksFromExistingTreatmentLinks(existingTreatmentLinks, bookLinks):
    treatmentLinks = []
    for existingTreatmentLink in existingTreatmentLinks:
        newTreatmentLinks = CreateNewTreatmentLinksFromTreatmentLink(existingTreatmentLink, bookLinks)
        treatmentLinks.extend(newTreatmentLinks)
    return treatmentLinks

#-------------------------------------------------------------------------------
def CreateNewTreatmentLinksFromTreatmentLink(treatmentLink, bookLinks):
    newTreatmentLinks = []
    matchingBookLinks = FindMatchingBookLinksForTreatmentLink(treatmentLink, bookLinks)
    for bookLink in matchingBookLinks:
        newTreatmentLink = acm.FTreatmentLink()
        newTreatmentLink.Apply(treatmentLink)
        newTreatmentLink.Book(bookLink.Book())
        newTreatmentLinks.append(newTreatmentLink)
    return newTreatmentLinks

#-------------------------------------------------------------------------------
def FindMatchingBookLinksForTreatmentLink(treatmentLink, bookLinks):
    matchingBookLinks = []
    if treatmentLink and bookLinks:
        treatmentOid = treatmentLink.Treatment().Oid()
        for bookLink in bookLinks:
            if bookLink.Treatment().Oid() == treatmentOid:
                matchingBookLinks.append(bookLink)
    return matchingBookLinks




#-------------------------------------------------------------------------------
# Creating dictionaries for mappings
#-------------------------------------------------------------------------------
def GetMappingBranchListDict(mappings, keyObjectsFunction, *args):
    mappingBranchList = MappingBranchHandler.CreateMappingBranchList(mappings)
    mappingBranchListDict = {}
    for branch in mappingBranchList:
        keyObjects = keyObjectsFunction(branch, args)
        for key in keyObjects:
            if key not in mappingBranchListDict:
                mappingBranchListDict[key] = []
            mappingBranchListDict[key].append(branch)
    return mappingBranchListDict

#-------------------------------------------------------------------------------
def GetTreatmentMappingsDictGroupedByBooks(treatmentType):
    bookLinks = acm.FBookLink.Select("")
    mappings = acm.FTreatmentMapping.Select("type = %d" % treatmentType)
    mappingsDict = GetMappingBranchListDict(mappings, FindBooksInBranch, bookLinks)
    return mappingsDict

#-------------------------------------------------------------------------------
def GetAIMappingsDictGroupedByBookLinks(aiType, treatmentLinks):
    bookLinks = acm.FBookLink.Select("")
    mappings = acm.FAccountingInstructionMapping.Select("type = %d" % aiType)
    mappingsDict = GetMappingBranchListDict(mappings, FindBookLinksInBranch, treatmentLinks, bookLinks)
    return mappingsDict

#-------------------------------------------------------------------------------
def GetTAccountMappingsDictGroupedByTreatmentLinks(taccountType, treatmentLinks):
    mappings = acm.FTAccountMapping.Select("type = %d" % taccountType)
    mappingsDict = GetMappingBranchListDict(mappings, FindTreatmentLinksInBranch, treatmentLinks)
    return mappingsDict

#-------------------------------------------------------------------------------
def FindBooksInBranch(treatmentMappingBranch, args):
    bookLinks = args[0]
    books = []
    for treatmentMapping in treatmentMappingBranch:
        treatment = treatmentMapping.Treatment()
        if treatment:
            bookLinks = FindBookLinksForTreatment(treatment, bookLinks)
            for bookLink in bookLinks:
                book = bookLink.Book()
                if book not in books:
                    books.append(book)
    return books

#-------------------------------------------------------------------------------
def FindBookLinksInBranch(aiMappingBranch, args):
    treatmentLinks = args[0]
    bookLinks = args[1]
    foundBookLinks = []
    for aiMapping in aiMappingBranch:
        ai = aiMapping.AccountingInstruction()
        if ai:
            matchingTreatmentLinks = FindMatchingTreatmentLinksForAI(ai, treatmentLinks)
            for treatmentLink in matchingTreatmentLinks:
                book = treatmentLink.Book()
                treatment = treatmentLink.Treatment()
                errorMsg = "Expected one FBookLink but got multiple."
                bookLink = FindMatchingBookLinkForBookAndTreatment(book, treatment, bookLinks)
                if bookLink not in foundBookLinks:
                    foundBookLinks.append(bookLink)
    return foundBookLinks

#-------------------------------------------------------------------------------
def FindTreatmentLinksInBranch(taccountMappingbranch, args):
    foundTreatmentLinks = []
    treatmentLinks = args[0]
    for taccountMapping in taccountMappingbranch:
        taal = taccountMapping.TAccountAllocationLink()
        if taal:
            matchingTreatmentLinks = FindMatchingTreatmentLinksForTAccAllocLink(taal, treatmentLinks)
            for matchingTreatmentLink in matchingTreatmentLinks:
                if matchingTreatmentLink not in foundTreatmentLinks:
                    foundTreatmentLinks.append(matchingTreatmentLink)
    return foundTreatmentLinks

#-------------------------------------------------------------------------------
def FindMatchingTreatmentLinksForAI(ai, treatmentLinks):
    matchingTreatmentLinks = []
    for treatmentLink in treatmentLinks:
        if ai == treatmentLink.AccountingInstruction():
            matchingTreatmentLinks.append(treatmentLink)
    return matchingTreatmentLinks

#-------------------------------------------------------------------------------
def FindMatchingTreatmentLinksForTAccAllocLink(taal, treatmentLinks):
    matchingTreatmentLinks = []
    chartOfAccount = taal.ChartOfAccount()
    book = chartOfAccount.Book()
    treatment = taal.Treatment()
    jvd = taal.JVD()
    ai = jvd.AccountingInstruction()
    for treatmentLink in treatmentLinks:
        if book.Oid() == treatmentLink.Book().Oid() and \
        treatment.Oid() == treatmentLink.Treatment().Oid() and \
        ai.Oid() == treatmentLink.AccountingInstruction().Oid():
            if treatmentLink not in matchingTreatmentLinks:
                matchingTreatmentLinks.append(treatmentLink)

    return matchingTreatmentLinks

#-------------------------------------------------------------------------------
def FindBookLinksForTreatment(treatment, bookLinks):
    treatmentOid = treatment.Oid()
    foundBookLinks = []
    for bookLink in bookLinks:
        if bookLink.Treatment().Oid() == treatmentOid:
            foundBookLinks.append(bookLink)
    return foundBookLinks

#-------------------------------------------------------------------------------
def FindMatchingBookLinkForBookAndTreatment(book, treatment, bookLinks):
    foundBookLink = None
    for bookLink in bookLinks:
        if bookLink.Treatment().Oid() == treatment.Oid() and \
        bookLink.Book().Oid() == book.Oid():
            foundBookLink = bookLink
            break
    return foundBookLink

#-------------------------------------------------------------------------------
# Creating and updating mappings
#-------------------------------------------------------------------------------
def CreateNewMappingsDictFromBranchDict(branchDict, mappingBranchFunc, *args):
    newMappingsDict = {}
    for refObject, branchList in branchDict.items():
        newMappingBranchList = CreateNewMappingsFromRefObject(refObject, branchList, mappingBranchFunc, args)
        newMappingsDict[refObject] = newMappingBranchList
    return newMappingsDict

#-------------------------------------------------------------------------------
def CreateNewMappingsFromRefObject(refObject, branchList, mappingBranchFunc, args):
    newBranchList = []
    prevMapping = None
    for branch in branchList:
        newBranch = mappingBranchFunc(refObject, branch, args)
        topParentMapping = newBranch[0]
        topParentMapping.Previous(prevMapping)
        prevMapping = topParentMapping
        newBranchList.append(newBranch)
    return newBranchList


#-------------------------------------------------------------------------------
def CreateNewTreatmentMappingsDictFromBranchDict(branchDict):
    bookLinks = acm.FBookLink.Select("")
    return CreateNewMappingsDictFromBranchDict(branchDict, CreateNewTreatmentMappingBranch, bookLinks)

#-------------------------------------------------------------------------------
def CreateNewAIMappingsFromBranchDict(branchDict, treatmentLinks):
    return CreateNewMappingsDictFromBranchDict(branchDict, CreateNewAIMappingBranch, treatmentLinks)

#-------------------------------------------------------------------------------
def UpdateFAccountMappingsFromBranchDict(branchDict):
    return CreateNewMappingsDictFromBranchDict(branchDict, CreateTAccountBranch)

#-------------------------------------------------------------------------------
def CreateNewTreatmentMappingBranch(book, branch, args):
    newTreatmentMappingBranch = []
    bookLinks = args[0]
    parentMapping = None
    for orgTreatmentMapping in branch:
        newTreatmentMapping = CreateNewTreatmentMappingFromOld(book, orgTreatmentMapping, bookLinks)
        if parentMapping:
            newTreatmentMapping.Parent(parentMapping)
        newTreatmentMappingBranch.append(newTreatmentMapping)
        parentMapping = newTreatmentMapping
    return newTreatmentMappingBranch

#-------------------------------------------------------------------------------
def CreateNewTreatmentMappingFromOld(book, treatmentMapping, bookLinks):
    treatment = treatmentMapping.Treatment()
    bookLink = None
    if treatment:
        bookLink = FindMatchingBookLinkForBookAndTreatment(book, treatment, bookLinks)
    newTreatmentMapping = acm.FTreatmentMapping()
    newTreatmentMapping.Apply(treatmentMapping)
    newTreatmentMapping.Previous(None)
    newTreatmentMapping.Next(None)
    newTreatmentMapping.Parent(None)
    newTreatmentMapping.Book(book)
    newTreatmentMapping.BookLink(bookLink)
    newTreatmentMapping.Treatment(None)

    return newTreatmentMapping

#-------------------------------------------------------------------------------
def CreateNewAIMappingBranch(bookLink, branch, args):
    treatmentLinks = args[0]
    newAIMappingBranch = []
    parentMapping = None
    for orgAIMapping in branch:
        newAIMapping = CreateNewAIMappingFromOld(bookLink, treatmentLinks, orgAIMapping)
        newAIMapping.Parent(parentMapping)
        newAIMappingBranch.append(newAIMapping)
        parentMapping = newAIMapping
    return newAIMappingBranch

#-------------------------------------------------------------------------------
def CreateNewAIMappingFromOld(bookLink, treatmentLinks, aiMapping):
    ai = aiMapping.AccountingInstruction()
    treatmentLink = None
    if ai:
        treatmentLink = FindMatchingTreatmentLink(bookLink.Book(), bookLink.Treatment(), ai, treatmentLinks)

    newAIMapping = acm.FAccountingInstructionMapping()
    newAIMapping.Apply(aiMapping)
    newAIMapping.Previous(None)
    newAIMapping.Next(None)
    newAIMapping.Parent(None)
    newAIMapping.BookLink(bookLink)
    newAIMapping.TreatmentLink(treatmentLink)
    newAIMapping.AccountingInstruction(None)

    return newAIMapping

#-------------------------------------------------------------------------------
def FindMatchingTreatmentLink(book, treatment, ai, treatmentLinks):
    foundTreatmentLink = None
    for treatmentLink in treatmentLinks:
        if book == treatmentLink.Book() and \
            treatment == treatmentLink.Treatment() and \
            ai == treatmentLink.AccountingInstruction():
                foundTreatmentLink = treatmentLink
                break
    return foundTreatmentLink

#-------------------------------------------------------------------------------
def CreateTAccountBranch(treatmentLink, branch, args):
    newBranch = acm.FList()
    newBranch.AddAll(branch)
    return newBranch



#-------------------------------------------------------------------------------
# Merging individual branches into hierarchies
#-------------------------------------------------------------------------------
class MappingTree(object):
    rootNode = None

    def __init__(self, rootMapping):
        self.rootNode = MappingNode(rootMapping)

    def Root(self):
        return self.rootNode

#-------------------------------------------------------------------------------
class MappingNode(object):
    mapping = None
    children = None
    parentNode = None

    def __init__(self, mapping):
        self.mapping = mapping
        self.children = []

    def AddChildMapping(self, childMapping):
        node = MappingNode(childMapping)
        node.SetParentNode(self)
        self.children.append(node)
        childMapping.Parent(self.GetMapping())  #might be unnecessary
        return node

    def Children(self):
        return self.children

    def SetParentNode(self, parentNode):
        self.parentNode = parentNode

    def GetMapping(self):
        return self.mapping

    def HasChildren(self):
        return len(self.children) > 0

#-------------------------------------------------------------------------------
def CreateTreatmentMappingTreesDict(mappingsDict):
    return CreateMappingTreesDict(mappingsDict, AreTreatmentMappingsEquivalent)

#-------------------------------------------------------------------------------
def CreateAIMappingTreesDict(mappingsDict):
    return CreateMappingTreesDict(mappingsDict, AreAIMappingsEquivalent)

#-------------------------------------------------------------------------------
def CreateTAccountMappingTreesDict(mappingsDict):
    return CreateMappingTreesDict(mappingsDict, AreTAccountMappingsEquivalent)

#-------------------------------------------------------------------------------
def CreateMappingTreesDict(mappingsDict, compareFunc):
    treeDict = {}
    for refObj, branchList in mappingsDict.items():
        mappingTrees = CreateMappingTrees(branchList, compareFunc)
        treeDict[refObj] = mappingTrees
    return treeDict

#-------------------------------------------------------------------------------
def CreateMappingTrees(branchList, compareFunc):
    mappingTrees = []
    queryMappingBranchTupleList = []
    for mappingBranch in branchList:
        MatchMappingBranchesWithCommonTopParent(mappingBranch, compareFunc, queryMappingBranchTupleList)

    for mapping, branches in queryMappingBranchTupleList:
        mappingTrees.append(CreateMappingTree(branches, compareFunc))
    return mappingTrees

#-------------------------------------------------------------------------------
def MatchMappingBranchesWithCommonTopParent(branch, compareFunc, tupleList):
    found = False
    parentMapping = branch[0]
    for mapping, branchList in tupleList:
        if compareFunc(parentMapping, mapping):
            branchList.append(branch)
            found = True
    if not found:
        tupleList.append((parentMapping, [branch]))

#-------------------------------------------------------------------------------
def CreateMappingTree(branchList, compareFunc):
    rootMapping = branchList[0][0]
    mappingTree = MappingTree(rootMapping)
    rootNode = mappingTree.Root()

    branch = branchList[0]
    parentNode = rootNode
    for mapping in branch[1:]:
        parentNode = parentNode.AddChildMapping(mapping)

    for branch in branchList[1:]:
        parentNode = rootNode
        for mapping in branch[1:]:
            if parentNode.HasChildren():
                lastChildNode = parentNode.Children()[-1]
                lastChildMapping = lastChildNode.GetMapping()
                if compareFunc(lastChildMapping, mapping):
                    parentNode = lastChildNode
                    continue
                else:
                    parentNode = parentNode.AddChildMapping(mapping)
            else:
                parentNode = parentNode.AddChildMapping(mapping)
    return mappingTree

#-------------------------------------------------------------------------------
def AreTreatmentMappingsEquivalent(mapping1, mapping2):
    equivalent = False
    if mapping1.Query() == mapping2.Query():
        bl1 = mapping1.BookLink()
        bl2 = mapping2.BookLink()
        if bl1 == bl2 or (bl1 == None and bl2 == None):
            equivalent = True

    return equivalent

#-------------------------------------------------------------------------------
def AreAIMappingsEquivalent(mapping1, mapping2):
    equivalent = False
    if mapping1.Query() == mapping2.Query():
        tl1 = mapping1.TreatmentLink()
        tl2 = mapping2.TreatmentLink()
        if tl1 == tl2 or (tl1 == None and tl2 == None):
            equivalent = True
    return equivalent

#-------------------------------------------------------------------------------
def AreTAccountMappingsEquivalent(mapping1, mapping2):
    equivalent = False
    if mapping1.Query() == mapping2.Query():
        tal1 = mapping1.TAccountAllocationLink()
        tal2 = mapping2.TAccountAllocationLink()
        if tal1 == tal2 or (tal1 == None and tal2 == None):
            equivalent = True
    return equivalent

#-------------------------------------------------------------------------------
# Utility functions
#-------------------------------------------------------------------------------
def CheckIfEnvironmentIsAlreadyUpgraded():
    alreadyUpgraded = False
    treatmentMappings = acm.FTreatmentMapping.Select("bookLink <> 0")

    if len(treatmentMappings) > 0:
        alreadyUpgraded = True

    if not alreadyUpgraded:
        aiMappings = acm.FAccountingInstructionMapping.Select("treatmentLink <> 0")
        if len(aiMappings) > 0:
            alreadyUpgraded = True

    if not alreadyUpgraded:
        accountMappings = acm.FTAccountMapping.Select("treatmentLink <> 0")
        if len(accountMappings) > 0:
            alreadyUpgraded = True

    return alreadyUpgraded














