""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/CorpActionElectionStateChart.py"

"""----------------------------------------------------------------------------
 MODULE
     CorpActionElectionStateChart - Module which define the callback functions for 
     Corporate Action Election States

 DESCRIPTION
     This module defines the Corporate Action transition callback functions
 ---------------------------------------------------------------------------"""
import acm
import FCorpActionElectionStatesSetup
from collections import namedtuple
import FCorpActionElectionPerform

def processCorpActionElection(context):
    print('Processing Corporate Action Election')
    election = context.Subject()
    choice = election.CaChoice()
    corpAct = choice.CorpAction()
    params = {}
    params['corp_action'] = corpAct
    params['corp_action_elections'] = [election]
    params['Testmode'] = 0
    FCorpActionElectionPerform.perform(params)

def on_entry_state_ready(context):
    print('on_entry_state_ready')

def on_entry_state_deadline_received(context):
    print('on_entry_state_deadline_received')

def on_entry_state_pending_lender_election(context):
    print('on_entry_state_pending_lender_election')

def on_entry_state_lender_election_received(context):
    print((context.Subject()))
    params = context.Parameters()
    print('on_entry_state_lender_response_received')

def on_entry_state_borrower_instructed(context):
    print((context.Subject()))
    params = context.Parameters()
    print('on_entry_state_borrower_instructed')

def on_entry_state_processed(context):
    print('on_entry_state_processed')
    params = context.Parameters()
    processCorpActionElection(context)

def condition_entry_state_ready(context):
    print('condition_entry_state_ready')    
    return True

def condition_exit_state_ready(context):
    print('condition_exit_state_ready')
    return True

def condition_entry_state_lender_election_received(context):
    print('condition_entry_state_lender_election_received')
    return True

def condition_exit_state_lender_election_received(context):
    print('condition_exit_state_lender_election_received')
    return True
