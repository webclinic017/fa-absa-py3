"""----------------------------------------------------------------------------
MODULE
    FFXViewTrades - Menu extensions to view expiries and cashflows from time bucket rows
    
        Copyright (c) 2010 by Sungard FRONT ARENA. All rights reserved.

DESCRIPTION

ENDDESCRIPTION
"""

# Import builtin modules

import acm

def findBucket(buckets, bucket):
    if not buckets:
        return None

    date = bucket.BucketDate()
    for b in buckets:
        if b.Includes(date):
            if b.StartDate() == bucket.StartDate() and b.EndDate() == bucket.EndDate():
                return b
            child = findBucket(b.ChildBuckets(), bucket)
            if child:
                return child
            else:
                return b 
    return None

def viewTradesAlternateTimeBucketsType(invokationInfo):
    selectedObjects = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedRowCells()
    toInsert = []
    lastOldDefAndConf = None
    lastNewTimeBuckets = None
    for cellInfo in selectedObjects:
        if cellInfo.RowObject().IsKindOf(acm.FTimeBucketAndObject):
            timeBucketAndObject = cellInfo.RowObject()
            timeBucket = timeBucketAndObject.TimeBucket()
            if not timeBucket:
                continue
            if timeBucket.TimeBuckets().GetBucketType() == acm.FEnumeration["enum(BUCKET_VALUE_TYPE)"].Enumeration("Maturity"):
                bucketType = acm.FEnumeration["enum(BUCKET_VALUE_TYPE)"].Enumeration("CashFlow")
            else:
                bucketType = acm.FEnumeration["enum(BUCKET_VALUE_TYPE)"].Enumeration("Maturity")
            
            treeSpec = cellInfo.TreeSpecification()
            if treeSpec or timeBucketAndObject.Object():
                oldDefAndConf = timeBucket.TimeBuckets().GetTimeBucketsDefinitionAndConfiguration()
                if oldDefAndConf == lastOldDefAndConf and lastNewTimeBuckets:
                    newTimeBuckets = lastNewTimeBuckets
                else:
                    oldConf = oldDefAndConf.TimeBucketsConfiguration()
                    conf = acm.TimeBuckets.CreateTimeBucketsConfiguration(None, None, bucketType)
                    if oldConf:
                        conf = oldConf.Merge(conf)
                    defAndConf = acm.TimeBuckets.CreateTimeBucketsDefinitionAndConfiguration(oldDefAndConf.TimeBucketsDefinition(), conf)
                    newTimeBuckets = acm.TimeBuckets.CreateTimeBuckets(defAndConf)
                    lastOldDefAndConf = oldDefAndConf
                    lastNewTimeBuckets = newTimeBuckets
                
                newTimeBucket = findBucket(newTimeBuckets, timeBucket)
                if newTimeBucket:
                    toInsert.append(acm.TimeBuckets.CreateAlternateTimeBucketInsertableObject(cellInfo, newTimeBucket))
            
    manager = invokationInfo.ExtensionObject()
    sheet = manager.ShowBuiltInUtilityView("TradeViewer")
    if sheet:
        sheet.InsertObject(toInsert, 'IOAP_LAST')
    
