""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementCutOff - Module which executes cut-off checks for settlements

    (c) Copyright 2006 by Front Capital Systems AB. All rights reserved.

DESCRIPTION

DATA-PREP

REFERENCES
    See modules FSettlementVariables and FSettlementEOD

----------------------------------------------------------------------------"""

def start(check_historical):
    global param
    global ZoneInfoImported

    log(1, '------------------------------------------------------------')
    pr = 'Check Settlement cut-off times...STARTED %s' % \
         time.asctime(time.localtime())
    log(1, pr)

    if ZoneInfoImported == 0:
        log(0, FSettlementGeneral2.noZoneinfoMsg())

    hist_day = ael.enum_from_string('StatusExplanation', 'Historic Value Date')
    settle_card = 0

    for s in ael.Settlement.select():
        if s.status == 'Authorised':
            if not s.check_day() and \
               (check_historical == 'Yes' or s.value_day >= ael.date_today()):
                clone = s.clone()
                clone.status = 'Exception'
                clone.status_explanation |= pow(2, hist_day)
                clone.commit()
                pr = 'Settlement %d has passed its cut-off time. Status set to Exception' % s.seqnbr
                log(1, pr)
                settle_card += 1
                
    pr = 'Processed %d settlements that had passed cut-off time' % settle_card
    log(1, pr)
    pr = 'Check Settlement cut-off times...FINISHED %s' % \
         time.asctime(time.localtime())
    log(1, pr)
    log(1, '------------------------------------------------------------')


def log(level, s):
    return FSettlementGeneral.log(level, s)

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt

    import ael, time
    import FSettlementParams, FSettlementGeneral, FSettlementGeneral2

    param = FSettlementParams.get_default_params()
    ZoneInfoImported = param.ZoneInfoImported

    ael_variables = [('check_historical', 'Check historical settlements',
                      'string', ['Yes', 'No'], 'No', 0)]

    def ael_main(dict):
        start(dict["check_historical"])

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    log(1, 'Could not run FSettlementCutOff due to ')
    log(1, str(e))


