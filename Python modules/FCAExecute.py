""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE 
    FCAExecute - Module which executes the Corp Actions listed in the
    CorpAction table.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module executes the Corporate Actions listed in the Corporate Action
    table which have not already been executed, and which have an Ex Date set
    which is on or before the date specified on the command line, or in the
    Macro variables window of this module.
    
NOTE
    The Acquire Day of any trade has to be the same or less than the Record
    Date entered in the Corporate Action table, or they will not be included.
    Furthermore, the Ex Date has to be on or before the 'CorpAct Date' provided
    in the macro variables window in order for the script to include the
    Corporate Action.  Portfolios with a total position of zero, are not
    included.  Trades which are Void, Confirmed Void, Simulated, Reserved or
    Terminated are not included.  Only Corporate Actions with one or both of
    the Statuses Instrument or Trade set to 'Script Update' are included.
----------------------------------------------------------------------------"""
try:
    import string
except ImportError:
    print 'The module string was not found.'
    print
try:
    import math
except ImportError:
    print 'The module math was not found.'
    print
try:
    import time
except ImportError:
    print 'The module time was not found.'
    print
try:
    from os import environ
except ImportError:
    print 'The module os was not found.'
    print
try:
    import FCARollback
except ImportError:
    print 'The module FCARollback was not found.'
    print
import ael
try:
    import FCAVariables
    reload(FCAVariables)
    import FCAAction
    reload(FCAAction)
    import FCAGeneral
    reload(FCAGeneral)
except AttributeError, msg:
    print 'WARNING! All FCAVariables have to be defined. Undefined:', msg
    print 'Maybe you need to merge FCAVariablesTemplate and FCAVariables.'

from FCAVariables import *
#if log:
    #logfile = FCAVariables.logfile #'c:\\temp\\corpact.txt'
    #lf = open(logfile, 'a')
    #FCAGeneral.close_log(lf)
    #lf = open(logfile, 'a')
#else: lf = None
try: Default_Portfolio
except NameError: Default_Portfolio = None
  
"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""

if __name__ == "__main__":
    import sys, getopt

    sys.path.append('/tmp')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:p:d:f:')
        if len(opts) < 2: raise getopt.error, ''
    except getopt.error, msg:
        print msg
        print 'Usage: ael <config name> FCAExecute.py -u <ARENA user> '\
              '-p <ARENA password>\n-d <for how many days before today '\
              'corp actions should be run> -f <"portf name">',
        sys.exit(2)

    ### Default Values:
    user = 0
    passw = 0
    days = 0
    pf = 0

    for o, a in opts:
        if o == '-p': passw = a
        if o == '-u': user = a
        if o == '-d': days = a
        if o == '-f': pf = a

    ### Recommend: Run in -archive mode. Please rearchive using the ExDate as
    ### date.
    ael.connect(environ['ADS_ADDRESS'], user, passw, '', 1)

    a = ael.date_today()
    d = -int(days)
    date = a.add_days(d)
    if not pf: pf = None

    if verb:
        s = '\nFind Corporate Actions to be performed on or before %s.\n'\
        % (date)
        FCAGeneral.logme(s)

    try:
        for ca in FCAGeneral.get_corp_actions(date, corpacts):
            FCAAction.perform_actions(verb, commit, ca, pf, date, 
                DefaultMethod)
    except:
        #if log: FCAGeneral.close_log(lf)
        raise

else:
    #"""
    pfs = FCAGeneral.pf()
    cas = FCAGeneral.scr_upd('Script Update')
    
    CorpActError = '\nNOTE! ALL Corporate Actions listed will be changed. '\
                   'Please select from the Corporate Action application which'\
                   ' Corporate Actions should be performed.'

    
    ael_variables = [('date', 'CorpAct Date', 'string',\
                      [str(ael.date_today()), 'Today'], 
                      FCAVariables.defaultCorpActDate, 0, 0),
                      ('cod', 'CutOff Date', 'string',\
                      ['2001-05-22', '2001-05-15'], 
                      '1970-01-01',),
                    #('pf', 'Portfolio to place Trades', 'string', pfs,
                     #Default_Portfolio, 0,0),
                    ('commit', 'Commit', 'string', ['0', '1'], `commit`),
                    ('verb', 'Verbose Printouts', 'string', ['0', '1'], `verb`),
                    ('method', 'Method', 'string',
                     ['Close', 'Adjust'], FCAVariables.DefaultMethod, 0, 0),
                    ('corpacts', 'CorpActs to be Performed', 'string', cas,\
                        '', 0, 1)]

    def ael_main(ael_variables_dict):
        series_difference = ael_variables_dict.get('series_difference')
        if series_difference:
            series_difference = int(series_difference)
        _date = ael_variables_dict.get('date')
        try:
            if _date and 'TODAY'.find(_date.upper()) <> -1:
                _date = str(ael.date_today())
        except AttributeError:  # Old Python Version.
            if _date and string.find('TODAY', string.upper(_date)) <> -1:
                _date = str(ael.date_today())
        _pf = None
        _commit = int(ael_variables_dict.get('commit'))
        _verb = int(ael_variables_dict.get('verb'))
        corpacts = ael_variables_dict.get('corpacts')
        if not corpacts:
            corpacts = ['All listed']

        #CA_Method = str(ael_variables_dict.get('method'))
        if ael_variables_dict.get('method'):
            CA_Method = ael_variables_dict.get('method')
        else:
            CA_Method = FCAVariables.DefaultMethod

        if _verb and _date:
            _s = 'Find Corporate Actions to be performed on or before %s.'\
            % (_date)
            FCAGeneral.logme(_s)
    #def run(e, pfid, corpacts, _commit, *rest): 
    ### If want to run from ASQL-query.
        #_pf = ael.Portfolio[pfid] ### If want to run from ASQL-query.
        #_date = '2222-02-22'
        #CA_Method = FCAVariables.DefaultMethod
                
        try:
            old_CA_Method = CA_Method
            for ca in FCAGeneral.get_corp_actions(_date, corpacts):
                if ca.seqnbr > 0:
                    ca = ca.clone()
                CA_Method = old_CA_Method #So default will be kept.
                ### Maybe in the future we want to let the value in the 
                ### macro window override the value in the GUI. But since the
                ### reason for adding a method in the GUI is to be able to have
                ### different methods per each corpact, for now the GUI method
                ### will override the macro variable. 
                try:
                    if ca.method != 'None':
                        CA_Method = ca.method
                except AttributeError, msg:
                    _string = 'CorpAct GUI field %s does not exist.' % msg
                    FCAGeneral.logme(_string)
                if CA_Method == 'Adjust':
                    AggError = FCAGeneral.aggregate_check(ca)
                    if AggError != None:
                        FCAGeneral.logme(AggError)
                    else:
                        FCAAction.perform_actions(ca, _verb, _commit, _pf,
                                                 _date, CA_Method)
                else:
                    FCAAction.perform_actions(ca, _verb, _commit, _pf, _date,
                        CA_Method)
            #if log:
                #FCAGeneral.close_log(lf)
        except:
            #if log: FCAGeneral.close_log(lf)
            raise
        #return 'Successful' ### If want to run from ASQL-query.




