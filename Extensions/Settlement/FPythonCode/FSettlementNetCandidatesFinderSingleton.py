""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementNetCandidatesFinderSingleton.py"
from FSettlementNetCandidatesFinder import NetCandidatesFinder

CONST_NetCandidatesFinder = None

#-------------------------------------------------------------------------
def GetNetCandidatesFinder():
    global CONST_NetCandidatesFinder
    if CONST_NetCandidatesFinder != None:
        return CONST_NetCandidatesFinder
    CONST_NetCandidatesFinder = NetCandidatesFinder()
    return CONST_NetCandidatesFinder