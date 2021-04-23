
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

global manualSummary
manualSummary = {}

def resetSummaryTracker():
    global manualSummary
    manualSummary = {}
           

def writeSummaryInst():
    global manualSummary
    Logme()('%s Summary of non trade (de)-archiving %s' %('-'*25, '-'*25), 'INFO')
    for objectType, action in list(manualSummary.keys()):
        values = manualSummary[(objectType, action)]
        if action == 0:
            act = 'dearchive'
        else:
            act = 'archive'
        Logme()('%-30s %-10s %i' %(objectType, act, values), 'INFO')
    Logme()('%s Summary complete %s' %('-'*25, '-'*25), 'INFO')

