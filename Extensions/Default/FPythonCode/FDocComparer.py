from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FDocComparer - Runs FDocInspector Script against different version of acm from the Command Window
    for scaning the documentation.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION    

    FDocComparer is a command line tool. 

USE

    Copy this module to a local folder and name it FDocComparer.py. Copy the following text into a .ini
    file in the same folder with any name:
    
        [PARAMS]
        inspector = ACM classes
        context = Standard
        debug = False
        [PRIME VERSION 1]
        server1 = tux01:9042
        user1 = system
        password1 = intas
        acm_pyd1 = C:\Program Files\Front\Front Arena\Prime\4.2
        [PRIME VERSION 2]
        server2 = sundevil:9043
        user2 = system
        password2 = intas
        acm_pyd2 = C:\Program Files\Front\Front Arena\Prime\4.3
    
    This is a template for the init file. There is a command line option for specifying the ini file with the 
    give name.

-------------------------------------------------------------------------------------------------------"""

import sys
import getopt
import os
import ConfigParser
import traceback

class DocComparer( object ):

    def __init__( self ):
        self.statistic_type = [ 'Total:','Documented:', 'Public:', 'Private:',  'Unclassified:' ]
        self.command_formatter = 'python FDocComparer.py --inspector "%s" --server1 "%s" --user1 "%s" --password1 "%s" --acmpyd1 "%s" --context "%s" --perform "%s"'
        self.server1 = None
        self.user1 = None
        self.password1 = None
        self.acm_pyd1 = None
        self.server2 = None
        self.user2 = None
        self.password2 = None
        self.acm_pyd2 = None
        self.inspector = None
        self.context = None
        self.debug = None
        self.configfile = None
        self.perform = None
        
    def run( self ):
        """kick off script"""
        self.init()
        try:
            self.start_inspection()
        except Exception as e:
            print ("An error occured while building report: %s" % str( e ))
            print (traceback.print_exc())

    def start_inspection( self ):
        """start inspection"""
        if self.perform:
            self.run_doc_inspector()
        elif not self.server2:
            self.perform_single( self.inspector, self.server1, self.user1, self.password1, self.acm_pyd1, self.context )
        else:
            self.perform_comparison()

    def init( self ):
        """initialize doc inspector"""
        options_and_values, args = self.get_command_line_options()
        options_table = dict( [ (option, value) for option, value in options_and_values ] )
        if options_table.get( '--configfile' ) or options_table.get( '-c' ):
            self.init_from_config_file( options_table )
        else:
            self.init_from_command_line( options_and_values )
        
    def init_from_config_file( self, opts ):
        """initialize from config file"""
        self.configfile = opts.get( '--configfile' ) if opts.get( '--configfile' ) else opts.get( '-c' )
        configParser = ConfigParser.ConfigParser()
        configParser.read( self.configfile )
        self.server1 = configParser.get( "PRIME VERSION 1", "server1" )
        self.user1 = configParser.get( "PRIME VERSION 1", "user1" )
        self.password1 = configParser.get( "PRIME VERSION 1", "password1" )
        self.acm_pyd1 = configParser.get( "PRIME VERSION 1", "acm_pyd1" )
        self.server2 = configParser.get( "PRIME VERSION 2", "server2" )
        self.user2 = configParser.get( "PRIME VERSION 2", "user2" )
        self.password2 = configParser.get( "PRIME VERSION 2", "password2" )
        self.acm_pyd2 = configParser.get( "PRIME VERSION 2", "acm_pyd2" )
        self.inspector = configParser.get( "PARAMS", "inspector" )
        self.context = configParser.get( "PARAMS", "context" )
        self.debug = configParser.getboolean( "PARAMS", "debug" )
        debug_command_line = False
        if opts.has_key( '--debug' ) or opts.has_key( '-d' ):
            debug_command_line = True
        if debug_command_line:
            self.debug = debug_command_line
            
    def init_from_command_line( self, opts ):
        """initialize from command line args"""
        for o, a in opts:
            if o in ( "-h", "--help" ):
                self.usage()
                sys.exit()
            elif o in ( "-d", "--debug" ):
                self.debug = True
            elif o in ( "-s", "--server1" ):
                self.server1 = a
            elif o in ( "-u", "--user1" ):
                self.user1 = a
            elif o in ( "-p", "--password1" ):
                self.password1 = a
            elif o in ( "-a", "--acmpyd1" ):
                self.acm_pyd1 = a
            elif o in ( "-i", "--inspector" ):
                self.inspector = a
            elif o in ( "-t", "--context" ):
                self.context = a
            elif o in ( "-k", "--server2" ):
                self.server2 = a
            elif o in ( "-l", "--user2" ):
                self.user2 = a
            elif o in ( "-m", "--password2" ):
                self.password2 = a
            elif o in ( "-b", "--acmpyd2" ):
                self.acm_pyd2 = a
            elif o in ( "-z", "--perform" ):
                self.perform = a

    def get_command_line_options( self ):
        """get command line options"""
        try:
            opts, args = getopt.getopt( sys.argv[1:], "hds:u:p:a:i:t:k:l:m:b:c:z:", ["help", "debug", "server1=", "user1=", "password1=", "acmpyd1=", "inspector=", "context=", "server2=", "user2=", "password2=", "acmpyd2=", "configfile=", "perform=" ] )
        except getopt.GetoptError as err:
            print (str( err ))
            self.usage()
            sys.exit( 2 )
        return opts, args

    def usage( self ):
        """print command line options"""
        print "-h, --help", "get options"
        print "-d, --debug", "debug option"
        print "-s, --server1", "server1"
        print "-u, --user1", "username1"
        print "-p, --password1", "password1"
        print "-a, --acmpyd1", "directory for acm.pyd associated to server1"
        print "-i, --inspector", "\"ACM classes\", \"ACM methods\", \"ACM functions\""
        print "-t, --context", "context"
        print "-k, --server2", "server2"
        print "-l, --user2", "username2"
        print "-m, --password2", "password2"
        print "-b, --acmpyd2", "directory for acm.pyd associated to server2"
        print "-c, --configfile", "config file name"
        
    def run_doc_inspector( self ):
        """Connect to database and run FDocInspector module"""
        sys.path.insert( 0, self.acm_pyd1 )
        try:
            import acm
        except ImportError as e:
            raise Exception( "Error importing acm: %s" % str( e ) )
            
        try:
            acm.Connect( self.server1, self.user1, self.password1, "" )
        except Exception as e:
            raise Exception( "Error connecting to ads: %s" % str( e ) )
            
        if self.debug:
            print ("used acm.pyd:", acm)

        try:
            import FDocInspector
        except ImportError as e:
            raise Exception( "Error importing FDocInspector: %s" % str( e ) )

        dictParams = { 'inspector' : self.inspector, 'context' : self.context }

        try:
            FDocInspector.ael_main( dictParams )
        except Exception as e:
            raise Exception( "Error running FDocInspector.ael_main: %s" % str( e ) )

        if acm.IsConnected():
            acm.Disconnect()

    def parse_stats_output(  self, output ):
        """Parse output and store it in a dictionary"""
        output_table = {}
        try:
            for var in self.statistic_type:
                temp1 = output.find( var )
                temp2 = temp1 + output[ temp1: ].find( '\n' )
                temp3 = output[ temp1:temp2 ].rfind( ' ' )
                output_table[ var ] = int( output[ temp1 + temp3:temp2 ] )
            return output_table
        except Exception as e:
            print ("Error parsing output ( %s ). Try running with the --debug flag for more information." % str( e ))
            return None
                
    def spawn_python_process( self, command ):
        """spawn new process and pipe results back"""
        fi, fe = os.popen4( command )
        output_server = ''.join( [ '|' + msg for msg in fe.readlines() ] )
        return output_server

    def perform_single( self, inspector, server, user, password, acm_pyd, context ):
        """get results from one server and get statistics"""
        print ('\n')
        print ("%s, %s, %s, %s, %s" % ( inspector, server, user, password, context ))
        print ('-'*60)
        command = self.command_formatter % ( inspector, server, user, password, acm_pyd, context, True )
        output_server = self.spawn_python_process( command )
        if self.debug:
            print (output_server)
        
        output_table = self.parse_stats_output( output_server )
        if output_table:
            self.print_output_table( output_table )
        return output_table
        
    def perform_comparison( self ):
        """get results from two servers and compare results"""
        output_table1 = self.perform_single( self.inspector, self.server1, self.user1, self.password1, self.acm_pyd1, self.context)
        output_table2 = self.perform_single( self.inspector, self.server2, self.user2, self.password2, self.acm_pyd2, self.context )
        if output_table1 and output_table2:
            self.print_comparison_statistics( output_table1, output_table2 )

    def print_output_table(  self, output_table ):
        """Print dictionary"""
        try:
            for type in self.statistic_type:
                tab = '\t'
                if type == 'Total:':
                    tab = '\t\t'
                print (type, tab, output_table[ type ])
        except KeyError as e:
            raise Exception( "Error when extracting statistics from output. Verify that FDocInspector output hasn't changed. %s" % str( e ) )
                
    def print_comparison_statistics( self, output_table1, output_table2 ):
        """Compare output and return differences"""
        print ('\n')
        print ("Differences:")
        print ('-'*60)
        try:
            for type in self.statistic_type:
                tab = '\t'
                if type == 'Total:':
                    tab = '\t\t'
                if output_table2[ type ] - output_table1[ type ] > 0:
                    print (type, tab, "+%s" % ( output_table2[ type ] - output_table1[ type ] ))
                elif output_table2[ type ] - output_table1[ type ] < 0:
                    print (type, tab, "-%s" % ( output_table1[ type ] - output_table2[ type ] ))
                elif output_table2[ type ] - output_table1[ type ] == 0:
                    print (type, tab, 'Unchanged')
        except KeyError as e:
            raise Exception( "Error when extracting statistics from output. Verify that FDocInspector output hasn't changed. %s" % str( e ) )
        
            
c = DocComparer()
c.run()
        



