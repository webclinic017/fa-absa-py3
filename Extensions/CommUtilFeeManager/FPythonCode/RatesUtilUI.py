'''
MODULE
    RatesUtilUI - This module prvoides Commitment fees details
   
HISTORY
    Date        Developer               Notes
    2017-03-27  Ntuthuko Matthews       created
'''


from acm import FUxLayoutBuilder


def RatesPane(cls):
    b = FUxLayoutBuilder()
    b.BeginVertBox('EtchedIn', '% Utilized')
    b. BeginVertBox('None')
    for i in range(1, 5):
        b.  BeginHorzBox('None')
        getattr(cls, 'txtRateUtilizedFrom{0}Ctrl'.format(i)).BuildLayoutPart(b, 'From')
        getattr(cls, 'txtRateUtilizedTo{0}Ctrl'.format(i)).BuildLayoutPart(b, 'To')
        getattr(cls, 'txtRate{0}Ctrl'.format(i)).BuildLayoutPart(b, 'Rate')
        b.  EndBox()
    b. EndBox()
    b. AddCheckbox('chkShowCtrl', 'Show additional fields')
    b. BeginVertBox('None')
    for i in range(5, 11):
        b.  BeginHorzBox('None')
        getattr(cls, 'txtRateUtilizedFrom{0}Ctrl'.format(i)).BuildLayoutPart(b, 'From')
        getattr(cls, 'txtRateUtilizedTo{0}Ctrl'.format(i)).BuildLayoutPart(b, 'To')
        getattr(cls, 'txtRate{0}Ctrl'.format(i)).BuildLayoutPart(b, 'Rate')
        b.  EndBox()
    b. EndBox()
    b.EndBox()
    
    return b

