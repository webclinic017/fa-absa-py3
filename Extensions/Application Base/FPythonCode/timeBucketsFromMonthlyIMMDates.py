
import acm
import FUxCore
import TimeBucketHelperFunctions

def ael_custom_label( parameters, dictExtra ):
    numberOfBucketInput =  parameters.At('buckets')
    if numberOfBucketInput:
       return '(' + str(numberOfBucketInput) + ' buckets)'
    return None

def ael_custom_dialog_show(shell, params):

    return TimeBucketHelperFunctions.ShowCreateBucketsFromCDSOrIMMDialog(shell, params, 'Monthly IMM Adjusted Buckets')

def ael_custom_dialog_main( parameters, dictExtra ):

    return CreateBuckets( parameters )


def CreateBuckets( parameters ):

    numberOfBucketInput = parameters.At('buckets')
    key = acm.FSymbol('StartDate')
    if parameters.HasKey(key):
        startDate = parameters.At(key);
    else:
        startDate = acm.Time().DateToday()
    
    return TimeBucketHelperFunctions.CreateMonthlyIMMTimeBucketDefinitions(startDate, numberOfBucketInput, 'Monthly IMM')
