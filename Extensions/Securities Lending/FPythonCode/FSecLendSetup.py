""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendSetup.py"
from __future__ import print_function
"""------------------------------------------------------------
MODULE
    FSecLendSetup

    (c) Copyright 2017 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Setup script for the installation of items required by
    the Security Lending Solution
--------------------------------------------------------------"""
import traceback
import acm
import FSecLendUtils
from FStateChartUtils import CreateStateChart, FStateChartUpdate
import DealCaptureSetup
import FSecLendHooks
import CreateOrderMappingHierarchy
from ACMPyUtils import Transaction


def InitialiseSecLendStateChart():
    try:
        wss = FSecLendHooks.WorkflowStateChart()
        if wss:
            if acm.FStateChart[wss.NAME]:
                renamedStates = {'Pending': 'Ready for processing',
                                'SL Export':'BO Export'}
                FStateChartUpdate(wss.NAME).UpdateStateChart(wss.DEFINITION, wss.LAYOUT, renamedStates)
            else:
                CreateStateChart(wss.NAME, wss.DEFINITION, wss.LAYOUT, limit='Single')
                print('Created Securities Lending state chart {}'.format(wss.NAME))
    except StandardError:
        print('Could not create standard securities lending state chart:{}'.format(traceback.format_exc()))


def UpdateCoverReturnTrades():
    query = FSecLendUtils.ActiveLoansBaseQuery()
    query.AddAttrNodeEnum('Market.Name', 'CoverReturn')
    trades = query.Select()
    print("Updating {} trades from CoverReturn Order Source to Manual...".format(len(trades)))
    for chuned_trades in [trades[x:x + 50] for x in range(0, len(trades), 50)]:
        with Transaction():
            for trade in chuned_trades:
                si = trade.StorageImage()
                si.Market('Manual')
                si.Commit()
    print("Updating Done.")


def RenameStateChart():
    wss = FSecLendHooks.WorkflowStateChart()
    sc = acm.FStateChart[wss.NAME]
    if sc:
        with Transaction():
            sc.Name("{}_{}".format(sc.Name(), acm.Time.DateToday()))
            sc.Commit()
    else:
        print("State Chart not existant with Name '{}'".format(wss.NAME))


#An example of deletion of statechart and connected BPs:
def DeleteStateChart():
    wss = FSecLendHooks.WorkflowStateChart()
    sc = acm.FStateChart[wss.NAME]
    acm.BeginTransaction()
    try:
        for bp in acm.BusinessProcess.FindByStateChart(wss.NAME):
            bp.Delete()
        sc.Delete()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        print('Error deleting state chart {}:{}'.format(sc, traceback.format_exc()))


def CreateOrderSources(names = None):
    def RenameIfThere(_from, _to):
        market = acm.FMarketPlace[_from]
        if market:
            updated = market.StorageImage()
            updated.Name(_to)
            updated.Commit()

    names = names or ['Arena Web', 'Manual', 'Markit', 'NGT', 'E-mail Service', 'FTP Service']
    RenameIfThere('OrderEntry', 'Manual')
    RenameIfThere('Web', 'Arena Web')
    acm.BeginTransaction()
    try:
        for name in names:
            if not acm.FMarketPlace[name]:
                p = acm.FMarketPlace()
                p.Name(name)
                p.Commit()
        acm.CommitTransaction()
    except StandardError:
        acm.AbortTransaction()
        print('Error inserting market places {}:{}'.format(names, traceback.format_exc()))

def createStoredTimeBuckets():

    def createTimeBuckets(relativeSpot, dayStartsBuckets, adjust, periods, includeRest, spotDays):
        bucketDefinitions = acm.FArray()
        for p in periods:
            bucketDefinition = acm.FDatePeriodTimeBucketDefinition()
            if isinstance(p, tuple):
                bucketDefinition.DatePeriod(p[1])
                bucketDefinition.Name = p[0]
            else:
                bucketDefinition.DatePeriod(p)
            bucketDefinition.Adjust(adjust)
            bucketDefinition.RelativeSpot(relativeSpot)
            bucketDefinitions.Add( bucketDefinition )
        if includeRest:
            bucketDefinitions.Add(acm.FRestTimeBucketDefinition())
        return acm.Time().CreateTimeBucketsFromDefinitions(0,
            bucketDefinitions,
            None,
            spotDays,
            False,
            False,
            False,
            False,
            dayStartsBuckets)

    timeBuckets = {'Security Loan Positions Buckets': createTimeBuckets(
                                                                False,
                                                                False,
                                                                True,
                                                                ['1d', '1w', '1m', '1y'],
                                                                True,
                                                                2),
                   'Security Loan Inventory Buckets': createTimeBuckets(
                                                                False,
                                                                False,
                                                                True,
                                                                [('T+0', '0d'), ('T+1', '1d'), ('T+2', '2d'), ('T+3', '3d'), ('T+4', '4d')],
                                                                False,
                                                                2),
                    }
    for k, v in timeBuckets.iteritems():
        if acm.FStoredTimeBuckets[k] is None:
            buckets  = acm.FStoredTimeBuckets()
            buckets.TimeBuckets(v)
            buckets.Name = k
            buckets.AutoUser = False
            buckets.User = None
            buckets.Commit()

def CreateChoiceLists():
    def Populate(chioicelist):
        for cl in chioicelist:
            DealCaptureSetup.ChoiceListSetUp(*cl).DoSetUp()

    chioicelistOrderType = [('MASTER', 'SBL_OrderType', ''),
        ('SBL_OrderType', 'Firm', 'A Firm order.'),
        ('SBL_OrderType', 'Soft', 'An IOI or Targeted Availability.'),
        ]
    chioicelistProductType = [('Product Type', 'Rebate Security Loan', ''), ('Product Type', 'Master Security Loan', 'Master loan for the underlying')]
    choicelistDvP = [('Settle Category', 'DvP', 'Delivery vs Payment'), ('Settle Category', 'Payment DvP', 'Delivery vs Payment')]

    Populate(chioicelistOrderType)
    Populate(chioicelistProductType)
    Populate(choicelistDvP)

def CreateAddInfos():
    mandatory = False
    subTypes = []
    defaultValue = None
    description = None

    # Parameters in tuple are recordType, fieldName, dataType, description, dataTypeGroup, subTypes, defaultValue, mandatory
    addinfos = [('Trade', 'SBL_HoldTime', 'Time', 'Availablilty is reserved until this time', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_OrderExpiryTime', 'Time', 'Order is valid until this time', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_OrderType', 'ChoiceList', 'SBL_OrderType', 'RecordRef', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_PendingOrder', 'Boolean', 'Is the order waiting for a reply', 'Standard',['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_RequestHold', 'Boolean', 'The client is interested in getting a reservation of the underlying security', 'Standard',['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'CollateralAgreement', 'CollateralAgreement', 'Collateral agreement add info', 'RecordRef', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SL_PrePay', 'Boolean', 'Collateral is settled in advance', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SL_Account', 'String', 'Account in SL system', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_ToDoList', 'String', 'SBL_ToDoList', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_TradeOriginId', 'Integer', 'The storage id of an acm.FCustomTextObject', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Trade', 'SBL_LimitFee', 'Double', 'Maximum fee accepted by the customer', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('User', 'SL_Counterparty', 'Party', description, 'RecordRef', subTypes, defaultValue, mandatory),
                ('Instrument', 'SL_MinimumFee', 'Double', description, 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Instrument', 'SL_Sector', 'String', description, 'Standard', ['Stock'], defaultValue, mandatory),
                ('Instrument', 'SL_Temperature', 'Double', 'Indicator of market interest', 'Standard', subTypes, defaultValue, mandatory),
                ('Instrument', 'SL_IsSpecial', 'String', description, 'Standard', ['Stock', 'Bond'], defaultValue,mandatory),
                ('Instrument', 'SL_NonBreakable', 'Boolean', 'Agreement is not breakable', 'Standard', ['SecurityLoan'], defaultValue, mandatory),
                ('Instrument', 'SL_TradingStock', 'Boolean', 'Stock position is actively traded', 'Standard',['SecurityLoan'], defaultValue, mandatory),
                ('Instrument', 'ID_ISIN', 'String', 'ID_ISIN', 'Standard', ['Bond', 'IndexLinkedBond', 'Stock'], None, False),
                ('Instrument', 'ID_CUSIP', 'String', 'ID_CUSIP', 'Standard', ['Bond', 'IndexLinkedBond', 'Stock'], None, False),
                ('Instrument', 'SL_Exchange', 'ChoiceList', 'SL_Exchange', 'RecordRef', ['Bond', 'IndexLinkedBond', 'Stock'], None, False),
                ('Alert', 'Notes', 'String', 'Alert Notes', 'Standard', subTypes, defaultValue, mandatory) 
                ]
    
    for addinfo in addinfos:
        DealCaptureSetup.AddInfoSetUp(*addinfo).DoSetUp()

def CreateAliases():
    aliases = [('SL Loan ID', 'TradeGroup.Id from SLS'),
               ('SEDOL', 'SEDOL'),
               ('BBG_Ticker', 'Bloomberg Ticker')
               ]

    for alias_type_name, alias_type_description in aliases:
        alias_type = acm.FInstrAliasType[alias_type_name]
        if not alias_type:
            alias_type = acm.FInstrAliasType()
            alias_type.Name = alias_type_name
            alias_type.AliasTypeDescription = alias_type_description
            alias_type.Commit()


class PortfolioHierarchyCreator:
    # Class to generate a default Portfolio Router Hierarchy Table.
    # The Hierarchy Type includes 3 columns: Instrument Type, Trader and Portfolio.
    # The Hierarchy Table is populated with the portfolio 'DEFAULT_POOL' as default portfolio.

    HIERARCHY_NAME = 'Portfolio Router'
    HIERARCHY_TYPE_NAME = 'Portfolio Mapping'
    RESULT_COLUMN = 'Portfolio'
    standardDomains = acm.FEnumeration['enum(B92StandardType)'].EnumeratorStringsSkipFirst().Sort()
    enumDomains = acm.FEnumeration['enum(B92EnumType)'].EnumeratorStringsSkipFirst().Sort()
    refsDomains = acm.FEnumeration['enum(B92RecordType)'].EnumeratorStringsSkipFirst().Sort()

    columnDictOrderList = ['Instrument Type','Trader','Portfolio']
    columnsDict = {'Instrument Type': ['Enum', 'InsType','','Instrument.InsType', False, False],
                   'Trader': ['RecordRef', 'User', '','Trader', False, False],
                   'Portfolio': ['RecordRef', 'Portfolio', '','Portfolio', False, False]
                            }

    hierarchyDict = {HIERARCHY_TYPE_NAME: columnsDict}
    defaultPortfolio = acm.FPhysicalPortfolio['DEFAULT_POOL']

    def GetDataTypeInteger(self, domainType, dataTypeString):
        enumeration = 0
        if domainType == 'Standard':
            enumeration = acm.FEnumeration['enum(B92StandardType)']
        elif domainType == 'Enum':
            enumeration = acm.FEnumeration['enum(B92EnumType)']
        elif domainType == 'RecordRef':
            enumeration = acm.FEnumeration['enum(B92RecordType)']
        return enumeration.Enumeration(dataTypeString) if enumeration else 0

    def CreateHierarchyType(self, name, columnDict):
        print('Creating hierarchy type for %s...' % name)
        ht = acm.FHierarchyType()
        ht.Name(name)
        ht.Commit()
        for column in self.columnDictOrderList:
            hierarchyColumnSpec = acm.FHierarchyColumnSpecification()
            hierarchyColumnSpec.Name(column)
            hierarchyColumnSpec.LeafsOnly(columnDict[column][4])
            hierarchyColumnSpec.UniqueValues(columnDict[column][5])
            hierarchyColumnSpec.Description(columnDict[column][3])
            hierarchyColumnSpec.DataTypeGroup(columnDict[column][0])
            hierarchyColumnSpec.DataTypeInfo(columnDict[column][2])
            hierarchyColumnSpec.DataTypeType(self.GetDataTypeInteger(
                hierarchyColumnSpec.DataTypeGroup(), columnDict[column][1]))

            hierarchyColumnSpec.HierarchyType(ht)
            hierarchyColumnSpec.Commit()
            print('Created column for %s' % column)
        print('HierarchyType %s created.' % name)

    def GetHierarchyColumnSpec(self, columnName):
        return acm.FHierarchyColumnSpecification.Select('name = "%s"\
            and hierarchyType = "%s"' % (columnName, self.HIERARCHY_TYPE_NAME))

    def SetDataValue(self, node, value, columnName):
        # Using try/except since dataValue doesn't accept empty strings.
        try:
            columnSpec = self.GetHierarchyColumnSpec(columnName)
            dataValue = acm.FHierarchyDataValue()
            dataValue.HierarchyNode(node)
            dataValue.HierarchyColumnSpecification(columnSpec)
            dataValue.DataValueVA(value)
            node.HierarchyDataValues().Add(dataValue)
        except Exception as e:
            print(e)

    def Setup(self):
        for key in self.hierarchyDict:
            if not acm.FHierarchyType[key]:
                self.CreateHierarchyType(key, self.hierarchyDict[key])
        #Create Hierarchy Table
        hierarchy = acm.FHierarchy()
        hierarchy.Name(self.HIERARCHY_NAME)
        hierarchy.HierarchyType(self.HIERARCHY_TYPE_NAME)
        hierarchyTree = acm.FHierarchyTree()
        hierarchyTree.Hierarchy(hierarchy)
        rootNode = hierarchyTree.Add(hierarchy.Name(), None)
        self.SetDataValue(rootNode, self.defaultPortfolio, self.RESULT_COLUMN )
        rootNode.IsLeaf(False)
        hierarchy.HierarchyNodes().Add(rootNode)

        hierarchy.Commit()

    def Cleanup(self):
        for key in self.hierarchyDict:
            type = acm.FHierarchyType[key]
            hs = None
            if type:
                hs = acm.FHierarchy.Select('hierarchyType=%s'%type.Oid())
            if hs:
                for h in hs:
                    h.Delete()
            if type:
                type.Delete()


def PortfolioHierarchyCleanupAndSetup():
    h = PortfolioHierarchyCreator()
    h.Cleanup()
    h.Setup()

def PortfolioHierarchySetup():
    h = PortfolioHierarchyCreator()
    if not acm.FHierarchy[h.HIERARCHY_NAME]:
        h.Setup()
   

def Setup():
    print("=======================================================================")
    print("Setup script running for Security Lending Solution installation")
    print("=======================================================================")
    InitialiseSecLendStateChart()
    CreateOrderSources()
    CreateChoiceLists()
    CreateAddInfos()
    createStoredTimeBuckets()
    CreateAliases()
    PortfolioHierarchySetup()
    CreateOrderMappingHierarchy.Run()
    print("=======================================================================")
    print("Setup script Sucessfully finished!")
    print("=======================================================================")
