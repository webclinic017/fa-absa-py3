
"""-----------------------------------------------------------------------------
Date:                   2010-06-09, 2010-07-27, 2010-09-23, 2012-01-12
Purpose:                Short End Curve Management
Department and Desk:    IRD Desk
Requester:              CTB
Developer:              Zaakirah kajee
CR Number:              336924, 382872, 441959, 550622, 870016 


Updated to convert all values to ZAR
CR870016 - Anil Parbhoo - Created a new ael variable for excel or csv output type


-------------------------------------------------------------------------------"""
import acm

from ShortEndProvisionReport import PSResetRiskReport
from PS_Functions import get_pb_fund_shortname
from at_logging import  getLogger, bp_start

LOGGER = getLogger()


ael_variables = [ ('InputType', 'Report Input Type: ', 'string', ['Filter', 'Portfolio'], 'Filter', 1),
                  ('Portfolio', 'Portfolio: ', 'FPhysicalPortfolio', None, None, 0, 1, 'Name of Portfolio'),
                 ('TrdFilter', 'Trade Filter: ', 'FTradeSelection', acm.FTradeSelection.Instances(), None, 1, 0, 'Name of Trade Filter'),  
                 ('OutputType', 'Output Type: ', 'string', ['Excel', 'CSV'], 'Excel'),
                 ('Outpath', 'Output Path: ', 'string', None, '/services/frontnt/Task/', 1),
                 ('Outfile', 'Output File: ', 'string', None, 'File_RiskResetDates', 1),
                 ('Currency', 'Currency: ', 'FCurrency', acm.FCurrency.Instances(), 'ZAR', 1, 0, 'Currency'),
                 ('Curve', 'Yield Curve: ', 'FYieldCurve', acm.FYieldCurve.Instances(), 'ZAR-SWAP', 1, 0, 'Yield Curve'),
                 ('shortName', 'Short Name', 'string', None, None, 1, 0)
                 ] 


def _convertToParamDictionary(configuration, report_name):
    paramDict = {}
    paramDict['InputType'] = 'Filter'
    paramDict['Portfolio'] = None
    paramDict['OutputType'] = 'Excel'
    
    paramDict['Currency'] = configuration['Currency_'+ report_name]
    paramDict['TrdFilter'] = configuration['TrdFilter_'+ report_name]
    
    paramDict['Outpath'] = configuration['OutputPath']
    paramDict['Outfile'] = configuration['Filename_'+ report_name]
    
    paramDict['Curve'] = configuration['Curve_'+ report_name]
    paramDict['fileID_SoftBroker'] = configuration['fileID_SoftBroker']
    paramDict['shortName'] = get_pb_fund_shortname(acm.FParty[configuration["clientName"]])
    return paramDict


#===========================================================Main================================================================================


def ael_main(config):
    process_name = "ps.reset_risk.{0}".format(config["shortName"])
    with bp_start(process_name):
            
        file_suffix = 'csv'
        csv_writer_parameters = None
        if 'fileID_SoftBroker' in config.keys():
            file_name = '_'.join([config['fileID_SoftBroker'], config['Outfile'], acm.Time.DateToday().replace('-', '')])
        else:
            file_name = '_'.join([config['filename'], acm.Time.DateToday().replace('-', '')])
        output_path = config['Outpath']
        input_type = config['InputType']
        if input_type == 'Portfolio':
            source = config['Portfolio']
        else:
            source = config['TrdFilter']
        
    
        yield_curve = config['Curve']
        currency = config['Currency']
        if 'frameworkVersion' in config.keys():
            frameworkVersion = config['frameworkVersion']
        else:
            frameworkVersion = 'N/A'
            
            
        collection = PSResetRiskReport(file_suffix, output_path,
                csv_writer_parameters, source, yield_curve,
                currency, frameworkVersion, file_name)
        collection.create_reports()
            
        return