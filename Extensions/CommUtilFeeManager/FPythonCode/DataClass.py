'''
MODULE
    DataClass - A class that allows you to create/amend the classes used in the CommUtilFeeManager. 
   
HISTORY
    Date        Developer               Notes
    2017-10-09  Ntuthuko Matthews       created
    2018-03-27  Ntuthuko Matthews       added the RatesUtilFee class
'''


class CommUtilFee(object):
    def __init__(self):
        attributes =[
            'FeeType',
            'CalcUtilFee',
            'CalcCommFee',
            'FacilityMax',
            'Limit',
            'CommitFeeRate',
            'UtilFeeRate',
            'Utilised',
            'FacilityExpiry',
            'CommitFeeBase',
            'CommitPeriod',
            'RollingConvention',
            'DayCount',
            'Linked',
            'PreviousRunDate',
            'LastRunDate'
        ]

        for i in attributes:
            self.__dict__[i] = None

    def __getatrr__(self, key):
        return self.__dict__[key]

    def __setatrr__(self, key, value):
        self.__dict__[key] = value

    def Items(self):
        return self.__dict__

    def IsEmpty(self):
        try:
            return len([i for i in self.__dict__.values() if i != None and i != '']) == 0
        except:
            return True

class RatesUtilFee(object):
    def __init__(self):
        for i in range(1, 11):
            self.__dict__['RateFrom{0}'.format(i)] = None
            self.__dict__['RateTo{0}'.format(i)] = None
            self.__dict__['Rate{0}'.format(i)] = None
        
    def __getatrr__(self, key):
        return self.__dict__[key]

    def __setatrr__(self, key, value):
        self.__dict__[key] = value

    def Items(self):
        return self.__dict__

    def Count(self):
        #this is a hack based on 3 distinct attributes in the class namely rateFrom, rateTo and rate
        #when adding a new attribute to the class update 3 to reflect the number of attributes
        return len([i for i in self.__dict__.keys()]) / 3

    def Size(self):
        return self.Count()+1
        
    def IsEmpty(self):
        try:
            return len([i for i in self.__dict__.values() if i]) == 0
        except:
            return True
