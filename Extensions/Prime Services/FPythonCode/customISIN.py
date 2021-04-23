
import acm, ael
import swift_functions


def customISIN(object, type):

    isCFD = False
    if type == 'CFD':
        isCFD = True
    else:
        isCFD = False

    customISIN = swift_functions._getCustomOtcOrIsin(object.Instrument(), isCFD)
    return customISIN

def ISINType(object):
    if object.Instrument().Isin():
        return 'ISIN'
    else:
        return 'Internal'

def ISINUnderlyingType(object):
    if object.Instrument().Underlying():
        if object.Instrument().Underlying().Instrument().Isin():
            return 'ISIN'
        elif not object.Instrument().Underlying().Instrument().Isin():
            if object.Instrument().Underlying().Instrument().Isin() != '':
                return 'Internal'
