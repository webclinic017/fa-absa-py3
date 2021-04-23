""" AggregationArchiving:1.3.2.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
        agg_bond - aggregation of bonds and bond derivatives

    (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        
        This module is used to perform various aggregation tasks on bond like
        instruments.  The main part of the computations are done in the genagg
        module.

        The script can be run either from a command prompt or from the AEL
        Module Editor within ATLAS.  What actions that will be performed and
        what instruments and portfolios that will be affected are directed
        through a number of input variables.

        When the script is run from a command prompt the input variables are
        specified in a text file given as argument to the script.  In this
        case, the script is run as follows:

        ael <name of config file> agg_bond.py -f <name of inifile>

        When running the script from the AEL Module Editor the input variables
        are specified in a dialog box.

        The following input variables are only available when the script is run
        from a command prompt.
    -atlasuser,     <ARENA database user in CAPITAL LETTERS>
    -adsaddress,    <port>@<machine> 
    -atlaspassword, <ARENA database user's password>
    -archive,       <0 or 1, if 1 the script is run in archived mode so
                        that dearchiving/reaggregating can be performed>

        The following variables can be specified both when running the script
        from a command prompt or from the ATLAS client.
    -date,          <date>
    -daysalive,     <number>
    -portfolio,     <list of portfolio names>
    -instrument,    <list of instrument names>
    -instype,       <instrument type>
    -underlying,    <list of underlying instruments names>
    -ClearPLTime,   <date time>
    -positionsize,  <number>
        -action,        <one of Check, Aggregate, Correct, CorrectAndAggregate>
    -verbose,       <0 or 1, where 1 enables printouts>

        The script can be used to aggregate positions in bonds, and options and
        future/forwards on bonds.  The instype argument can be used if only
        positions in a specific instrument type should be aggregated.

        The script creates one aggregate trade for each position, that is, one
        aggregate for each instrument and portfolio.  The instrument argument
        can be used to specify one or several instruments to be aggregated.  If
        left empty all instruments will be considered for aggregation.  In the
        same way, the underlying argument can be used to aggregate derivatives
        on one or several underlyings.

        The portfolio argument is used to specify the portfolios in which
        positions should be aggregated.  More than one portfolio can be given
        at a time, and it is also possible to specify a compound portfolio as
        this argument.  In this case, positions in all physical portfolios
        below the compound portfolio will be aggregated.

        Important for how the aggregation is performed is if it takes place in
        archived mode or not.  In archived mode all archived trades are visible
        but not the aggregate trade, and vice versa if archived mode is not
        used.  If the script is run from a command prompt it is possible to
        choose which mode to run the script in by using the input variable
        -archive.  When running the script from an ATLAS client however, the
        archived mode is instead governed by if the archived mode of the client
        (an ATLAS client is started in archived mode by using the flag
        -archive).

        The date argument is the break date which decides which trades should
        be archived and which should be dearchived.  Also, the value day and
        trade time of the aggregate trade will be set to this date.  In
        non-archived mode all trades with value day (and trade time) before the
        date argument are archived.  In archived mode it is also possible to
        perform dearchiving of archived trades.  All trades with a value day
        before the date argument are archived and all archived trades with a
        value day after the date argument are dearchived.

        As an alternative to the date argument it is possible to use the
        daysalive argument.  Specifying a number such as 5 as this argument
        means that the break date should be set to 5 days before today.  The
        number of days is interpreted as calendar days, and not banking days.

        The ClearPLTime is the time when the last clearing of profit loss was
        performed.

        Only positions larger than the positionsize argument is aggregated.
        The default value is 3.

        When updating an archived trade the corresponding aggregate trade may
        become incorrect.  The action argument can be used for detecting and
        correcting such aggregate trades.  If this argument is set to 'Check'
        all aggregate trades that need to be updated are displayed, and by
        setting it to 'Correct' these aggregate trades are reaggregated to the
        same date as before.  Using the 'Aggregate' option means that only
        aggregatation according to the other input variables is performed,
        whereas 'CorrectAndAggregate' both corrects and aggregates.
        
        The verbose argument determines how much information will be written
        about the progress of the aggregation.  If set to 1 more information is
        written.
        

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import time
import ael

if __name__ == "__main__":
    import sys, getopt
    from genagg import *
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:h')
        if len(opts) != 1: raise getopt.error, ''
    except getopt.error, msg:
        print msg
        print 'Usage: agg_bond.py -f inifilename [-h help]',
        sys.exit(2)
            
    inifile = 0
    for o, a in opts:
        if o == '-f': inifile = a
        if o == '-h': help_text_bond()

    M = {}
    get_ini_values(M, 'bond', inifile)

    if M['arch_to'] == '1':
        ael.connect(M['ads_address'], M['atlas_user'], M['atlas_passwd'], '', 1)
    else:
        ael.connect(M['ads_address'], M['atlas_user'], M['atlas_passwd'])
    
    if perform_agg_and_arch(M, 'bond') == -1:
        print '\nArchiving & aggregation failed %s' % time.ctime(time.time())
        sys.exit(2)
    else:
        print '\nArchiving & aggregation finished %s' % time.ctime(time.time())
        ael.disconnect()

else:
    from GenAgg import *

    print 'Loading...'

    prf = []
    for p in ael.Portfolio.select():
        prf.append(p.prfid)

    q = '''select insid from instrument where instype in %s and
    und_instype in %s and archive_status <= %d''' % \
    (get_valid_instypes('bond', 0), get_valid_instypes('bond', 1),
     ael.archived_mode())

    res = ael.dbsql(q)
    ins = []
    for i in res[0]:
        ins.append(i[0])

    q = '''select insid from instrument where instype in %s and
    archive_status <= %d''' % \
    (get_valid_instypes('bond', 1), ael.archived_mode())

    res = ael.dbsql(q)
    und = []
    for i in res[0]:
        und.append(i[0])

    actions = ['Check', 'Aggregate']
    if ael.archived_mode():
        actions = actions + ['Correct', 'CorrectAndAggregate']

    ael_variables = \
    [('date', 'Date', 'date', [], str(ael.date_today()), 0),
     ('daysalive', 'Days Alive', 'int', [], '0', 0),
     ('portfolio', 'Portfolio', 'string', prf, None, 0, 1),
     ('instrument', 'Instrument', 'string', ins, None, 0, 1),
     ('underlying', 'Underlying', 'string', und, None, 0, 1),
     ('instype', 'Instype', 'string', ['Bond', 'Option', 'Future/Forward'],
      None, 0, 1),
     ('ClearPLTime', 'Clear PL Time', 'string', [], '1970-01-01 00:00:00', 0),
     ('positionsize', 'Position Size', 'int', [], '3', 0),
     ('correctagg', 'Action', 'string', actions, 'Aggregate', 1),
     ('verbose', 'Verbosity', 'int', [], '1', 0)]

    def ael_main(dictionary):
        M = {}

        result = 'finished'
        if store_variables(M, dictionary) == -1 or perform_agg_and_arch(M, 'bond')==-1:
            result = 'failed'

        print '\nArchiving & aggregation %s %s' % \
              (result, time.ctime(time.time()))


