"""-----------------------------------------------------------------------
MODULE
    counterparty_export_csv

DESCRIPTION
    Specification:
        Create a daily drop file in excel format containing the following counterparty data: 
    short name, name, barcap eagle sdsid, barcap cp sdsid, barcap sms le, party number

    The location in which to drop this file daily will be:

    UAT: Y:\Jhb\LFMP\Qlikview\QVData\Drop\Collateral Optimisation\SDS to Front ID Mapping\UAT
    PRD: Y:\Jhb\LFMP\Qlikview\QVData\Drop\Collateral Optimisation\SDS to Front ID Mapping\PRD

    Implementation:
        In each of the locations, try to create temporary file with data dump, if it succeeds,
    remove original file and rename new file to proper file name. 
    



    Project             : ABCAP IT Front Arena Minor Works
    Date                : 2011-12-02
    Purpose             : Create a daily drop file containing specified counterparty data 
    Department and Desk : Collateral optimization
    Requester           : Haasbroek, Tian
    Developer           : Peter Fabian
    CR Number           : C852658

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2011-12-02           Peter Fabian        Initial implementation 
ENDDESCRIPTION
-----------------------------------------------------------------------"""

import sys
import csv

import acm


# Purpose: Write the counterparty information to specified csv files 
# Params: file_names    : list of paths where to write report files
#         print_header  : indication whether to write table header row or not (1/0)
#         separator     : string delimiting fields in csv file (e.g. ";")
# Return: Nothing, writes 2 csv files to specified locations
def counterparty_export(file_names, print_header, separator, *rest):
    acm.Log("Separator chosen: " + separator)
    if separator == '':
        separator = ';'
    acm.Log("Separator used: " + separator)
    
    all_parties = acm.FParty.Select('')

    # heading for columns
    heading_cols = [ "Short name",
                     "Name", 
                     "BarCap eagle sdsid", 
                     "BarCap sms cp sdsid", 
                     "BarCap sms le sdsid",
                     "Party number" ]

    

    for file_name in file_names:
        try:
            # open csv file, needs to be open in binary mode for csv writer
            acm.Log("Trying to open file " + file_name)
            csv_file = open(file_name, 'wb')
            csv_writer = csv.writer(csv_file, delimiter=separator)
            
            # print header if requested
            if print_header:
                csv_writer.writerow(heading_cols)

            # dump requested info
            for party in all_parties:
                # define columns to export to file
                columns = [ party.Id(),   #ptyid
                            party.Fullname(), 
                            party.add_info('BarCap_Eagle_SDSID'), 
                            party.add_info('BarCap_SMS_CP_SDSID'), 
                            party.add_info('BarCap_SMS_LE_SDSID'),
                            party.Oid() ] #ptynbr 
                
                csv_writer.writerow(columns)

            # close csv file
            csv_file.close()
            acm.Log("File " + file_name + " finished and closed")
        except IOError, (errno, strerror):
            error_str = "I/O error(%s): %s" % (errno, strerror)
            acm.Log(error_str)
            raise
        except:
            error_str = "Unexpected error: %s" % sys.exc_info()[0] 
            acm.Log(error_str)
            raise

    acm.Log("Export finished.")
    

#########################
#          main         #
#########################


ael_gui_parameters = {'windowCaption':'Counterparty export to csv'}

ael_variables = [
                    ['Outpaths',    'Output Paths', 'string', None, 'Y:/Jhb/LFMP/Qlikview/QVData/Drop/Collateral Optimisation/SDS to Front ID Mapping/UAT/,Y:/Jhb/LFMP/Qlikview/QVData/Drop/Collateral Optimisation/SDS to Front ID Mapping/PRD/',
                     1, 0,    'Comma separated paths where the csv files should be written'],
                    ['FileName',    'File Name',    'string', None, 'counterparty_data.csv', 
                     1, 0,    'Name of the output csv file'],
                    ['Separator',   'Separator',    'string', None, ";",
                     0, 0,    'Value separator for the output csv file (Semicolon will be used if nothing is specified)'],
                    ['PrintHeader', 'Print Header', 'int',   [0, 1], '1', 
                     1, None, 'Do you want the header to be written into csv file?' ]
                ]


def ael_main(parameters):
    # specify locations where to write the report
    paths = parameters['Outpaths'].split(',');
    
    file_names = map(lambda path: path + '/' + parameters['FileName'], paths)
    
    # separator for csv file
    # can not choose comma since some of the fullname-s contain commas
    separator = parameters['Separator']
    
    # set to 0 if you do not want to write header (colnames) for the data
    print_header = parameters['PrintHeader']
    
    # log input parameters
    acm.Log("Outpaths=|" + parameters['Outpaths'] + "|")
    acm.Log("FileName=|" + parameters['FileName'] + "|")
    acm.Log("Separator=|" + parameters['Separator'] + "|")
    acm.Log("PrintHeader=|" + str(parameters['PrintHeader']) + "|")
    
    
    # dump the information to files
    counterparty_export(file_names, print_header, separator)

    print "Completed Successfully ::"
