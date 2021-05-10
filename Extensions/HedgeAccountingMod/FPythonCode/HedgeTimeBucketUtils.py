'''
===================================================================================================
PURPOSE: The HedgeTimeBucketUtils module provides helper functions to retrieve dates to be used in
            the Hedge Effictiveness Testing process. The logic will use configurable Front Arena
            Time Buckets to build and provide a date series if available, otherwise it will build
            a default date series based on default parameters defined in the HedgeConstants module.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import acm

import HedgeConstants


def create_definition(monthOffset):

    definition = acm.FDatePeriodTimeBucketDefinition()
    name = '%sm' % monthOffset
    definition.DatePeriod(name)
    definition.Name(name)
    definition.Adjust(False)
    definition.RelativeSpot(False)

    return definition


def get_time_buckets(referenceTimeBucketName, referenceStartDate=acm.Time().DateNow()):
    '''Get the timebucket from the DB
        - check if a time bucket with the specified name exist for the user
        - if not, use the default timebucket as reference
        - if a default bucket isn't found, create a temp time bucket based on HR periods default

        referenceTimeBucketName [string] - name of the time bucket to use
        referenceStartDate [datetime] - reference date from which to calculate the date series

        return [list(FTimeBuckets)] - list of TimeBuckets
    '''

    timeBuckets = None

    storedTimebuckets = None
    searchString = "name = '%s' and owner = '%s'" % (referenceTimeBucketName, acm.UserName())
    matchingTimeBucketList = acm.FStoredTimeBuckets.Select(searchString)

    if matchingTimeBucketList:
        storedTimebuckets = matchingTimeBucketList[0]
    else:
        # get global (ADS) user default list
        searchString = "name = '%s'" % (referenceTimeBucketName)
        matchingTimeBucketList = acm.FStoredTimeBuckets.Select(searchString)

        if matchingTimeBucketList:
            for storedBucket in matchingTimeBucketList:
                if storedBucket.Owner().Name() == HedgeConstants.STR_ADS_USERNAME:
                    storedTimebuckets = storedBucket

    if storedTimebuckets:
        # if the reference date is not equal to today, build a new timeBucket list with the new
        #       ref date as start date
        if referenceTimeBucketName and not referenceStartDate == acm.Time().DateNow():
            timeBucketDefinitions = acm.FArray()

            for timeBucket in storedTimebuckets.TimeBuckets():
                timeBucketDefinitions.Add(timeBucket.TimeBucketDefinition())

            timeBuckets = acm.Time().CreateTimeBucketsFromDefinitions(
                referenceStartDate,
                timeBucketDefinitions,
                None,
                0,
                0,
                0,
                0,
                0,
                0
            )

        else:
            timeBuckets = storedTimebuckets.TimeBuckets()

    else:
        # create a in-memory timebucket based on the default number of periods
        endDataPoint = HedgeConstants.INT_DATA_POINTS * -1
        currentBucket = 0

        timeBucketDefinitions = acm.FArray()

        while currentBucket > endDataPoint:
            timeBucketDefintion = create_definition(currentBucket)
            timeBucketDefinitions.Add(timeBucketDefintion)

            currentBucket -= 1

        timeBuckets = acm.Time().CreateTimeBucketsFromDefinitions(
            referenceStartDate,
            timeBucketDefinitions,
            None,
            0,
            0,
            0,
            0,
            0,
            0
        )

    return timeBuckets


def get_all_timebuckets_per_owner(user):
    '''Retrieve all Stored Time Buckets belonging to the specified user.

    user [acm.FUser]

    return  [FPersistantSet] - list of Stored Time Bucket Names
    '''

    searchString = 'owner = %s' % (user.Name())
    matchingTimeBucketList = acm.FStoredTimeBuckets.Select(searchString)

    if not matchingTimeBucketList:
        matchingTimeBucketList = acm.FArray()

    if HedgeConstants.STR_DEFAULT_TIME_BUCKETS not in matchingTimeBucketList:

        # get global (ADS) user default list
        searchString = 'name = %s' % (HedgeConstants.STR_DEFAULT_TIME_BUCKETS)
        defaultBucketLists = acm.FStoredTimeBuckets.Select(searchString)

        if defaultBucketLists:
            for storedBucket in defaultBucketLists:
                if storedBucket.Owner().Name() == HedgeConstants.STR_ADS_USERNAME:
                    matchingTimeBucketList.Add(storedBucket)

    return matchingTimeBucketList.SortByProperty('Name')


def get_time_bucket_dates(referenceTimeBucketName, referenceStartDate=acm.Time().DateNow()):
    '''Get an array of dates either from the specified Time Bucket if found or a default
        dates series otherwise.

        referenceTimeBucketName [string] - name of the time bucket to use
        referenceStartDate [datetime] - reference date from which to calculate the date series

        return [list(dates)] - list of dates
    '''
    dateList = []
    timeBuckets = get_time_buckets(referenceTimeBucketName, referenceStartDate)

    for timeBucket in timeBuckets:
        dateList.append(timeBucket.BucketDate())

    return dateList


def get_time_bucket_dates_sorted(referenceTimeBucketName, referenceStartDate=acm.Time().DateNow()):
    '''Get an sorted array of dates either from the specified Time Bucket if found or a default
        dates series otherwise.

        referenceTimeBucketName [string] - name of the time bucket to use
        referenceStartDate [datetime] - reference date from which to calculate the date series

        return [list(dates)] - list of dates, sorted
    '''

    dateList = []
    timeBuckets = get_time_buckets(referenceTimeBucketName, referenceStartDate)

    for timeBucket in timeBuckets:
        dateList.append(timeBucket.BucketDate())

    return sorted(dateList)


def get_retrospective_dates_sorted(referenceTimeBucketName,
                                   designation_date,
                                   referenceStartDate=acm.Time().DateNow()):
    '''Get an sorted array of dates either from the specified Time Bucket if found or a default
        dates series otherwise.

        referenceTimeBucketName [string] - name of the time bucket to use
        designation_date [datetime] - Hedge Relationship designation date
        referenceStartDate [datetime] - reference date from which to calculate the date series

        return [list(dates)] - list of dates, sorted
    '''

    dateList = []
    timeBuckets = get_time_buckets(referenceTimeBucketName, referenceStartDate)

    for timeBucket in timeBuckets:
        if designation_date <= timeBucket.BucketDate():
            dateList.append(timeBucket.BucketDate())

    # if the datelist is not of the same lenght as the time bucket list,
    # insert the designation date as the first date.
    if len(dateList) < len(timeBuckets):
        dateList.append(designation_date.strip())

    return sorted(dateList)
