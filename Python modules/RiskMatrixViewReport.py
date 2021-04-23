"""
Created on 20 Jun 2013

@author: conicova

Contains the classes used to generate a Risk Matrix View report.
Creates the front arena input form, which offers the possibility to
specify the parameters that have to be used when generating the report.  
"""


# import startup

import acm, os
from datetime import date
import WBXMLReport, FDateTime
from at_ael_variables import AelVariableHandler
from RiskMatrixViewSimpleReport import RiskMatrixGen
from RiskMatrixViewFormattedReport import RiskMatrixFormattedReport

# Default values for the input parameters
SCENARIO_TITLE = 'Spot Time Long'
TRADE_FILTER_TITLE = 'EQ Index EQ Derivs'
COLUMN_IDS = ['Portfolio Gamma Implicit Cash Equity'
               , 'Theta From Gamma'
               , 'Portfolio Vega'
               , 'TermVega'
               , 'Portfolio Equity Vanna Cash'
               , 'Portfolio Volga'
               ]

GROUPER_NAMES = ['Underlying']
XSLT_TEMPLATE_NAME = 'FTABTemplate'  # FXMLSpreadsheetTemplate'
XSLT_FORMATTED_TEMPLATE_NAME = 'RiskMatrixViewFormatted'  # requires special class
FILE_NAME_TEMPLATE = "RiskMatrixViews-{0}.xls" 

#--------------------------------------------------------------------------
def _gen_prime_report_obj(tables):
    """
    Initialises and returns a new instance of the PrimeReport class
    """
    prime_report = WBXMLReport.PrimeReport()
    prime_report.name = "Risk Matrix Views"
    prime_report.tables = tables
    prime_report.rtype = "RiskMatrixView"
    prime_report.time = FDateTime.iso_utc_now()
    prime_report.local_time = FDateTime.iso_utc_now_tz()
    prime_report.arena_data_server = acm.ADSAddress()  # '10.110.92.110:9101'
    
    return prime_report

def _gen_simple_report_content(sc_title, tf_title, col_ids, gr_names, xslt_templ_name):
    """
    Generates a string representation of the required report.
    """
    rmx = RiskMatrixGen()
    rmx.gen_risk_matrixes(sc_title, tf_title, col_ids, gr_names)
    
    tables = [risk_matrix.get_fprimetable() for risk_matrix in rmx.calc_risk_matrixes] 
    
    prime_report = _gen_prime_report_obj(tables)
    
    xml_report = WBXMLReport.WBXMLReport()
    report_content_xml = xml_report.get_xml_str(prime_report)
    
    xslt_template = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', xslt_templ_name)
    xslt_transformer = acm.CreateWithParameter('FXSLTTransform', xslt_template.Value())
    report_content = xslt_transformer.Transform(report_content_xml)
    
    return report_content

def _gen_formatted_report_content(sc_title, tf_title, col_ids, gr_names, xslt_templ_name):
    """
    Generates a string representation of the required formatted report.
    """
    rmx = RiskMatrixGen()
    rmx.gen_risk_matrixes(sc_title, tf_title, col_ids, gr_names)
    
    if len(rmx.calc_risk_matrixes) == 0:
        raise Exception("No data to write to xls.")
   
    formated_rm = RiskMatrixFormattedReport().get_formated_risk_matrixes(rmx.calc_risk_matrixes, col_ids)
    
    report_content_xml = RiskMatrixFormattedReport.get_xml_formated_risk_matrixes(formated_rm)
   
    xslt_template = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', xslt_templ_name)
    xslt_transformer = acm.CreateWithParameter('FXSLTTransform', xslt_template.Value())
    report_content = xslt_transformer.Transform(report_content_xml)
    
    return report_content

#--------------------------------------------------------------------------               
xslt_template_names = sorted(acm.GetDefaultContext().ExtensionNames(
    'FXSLTemplate', 'FObject', True, True))
trade_filter_names = sorted([f.Name() for f in acm.FTradeSelection.Select("")])

ael_variables = AelVariableHandler()

ael_variables.add(
    'tf_title',
    label='TradeFilter',
    collection=trade_filter_names,
    default=TRADE_FILTER_TITLE,
    alt='The trade filter title that will be used to create trade rows' 
    )
ael_variables.add(
    'gr_names',
    label='Groupers',
    default=','.join(GROUPER_NAMES),
    mandatory=False,
    alt='The groupers that have to be used, comma separated.',
    multiple=True 
    )
ael_variables.add(
    'sc_title',
    label='Scenario',
    default=SCENARIO_TITLE,
    alt='The two dimensional scenario that will be used when calculating the values.' 
    )
ael_variables.add(
    'col_ids',
    label='Column ids',
    default=','.join(COLUMN_IDS),
    mandatory=False,
    alt=('The columns ids (see column properties in Workbook) for which the '
         'Risk Matrix View has to be created. The columns order is important'
         ' in the formatted report.'),
    multiple=True               
   )
ael_variables.add(
    'path',
    label='Output Folder',
    default=r'c:\tmp\ABITFA-2068',
    alt='The directory where to which the file will be dropped.' 
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='RiskMatrixView',
    alt='The directory where to which the file will be dropped.' 
    )
ael_variables.add(
    'xslt_templ_name',
    label='Template',
    collection=xslt_template_names,
    default=XSLT_TEMPLATE_NAME,
    alt='The xslt template title , which will be used when generating the final file.' 
    )

def ael_main(dict_arg):
    """Main entry point for FA"""
    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}".format(t, m))
    
    tf_title = dict_arg['tf_title']
    path = dict_arg['path']
    gr_names = dict_arg['gr_names']
    col_ids = dict_arg['col_ids']
    sc_title = dict_arg['sc_title']
    xslt_templ_name = dict_arg['xslt_templ_name']
    file_name = dict_arg['file_name']
    
    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return 
    
    tf = acm.FTradeSelection[tf_title]
    if not tf:
        warning_function("Warning",
            "Could not find the specified trade fitler!", 0)
        return
    
    filename = "{0}-{1}.xls".format(file_name, date.today().strftime("%Y-%m-%d"))
    file_path = os.path.join(path, filename)
    
    if xslt_templ_name == XSLT_FORMATTED_TEMPLATE_NAME:
        report_content = _gen_formatted_report_content(sc_title, tf_title, col_ids
                                                        , gr_names, xslt_templ_name)
    else:
        report_content = _gen_simple_report_content(sc_title, tf_title, col_ids
                                                    , gr_names, xslt_templ_name)
    
    with open(file_path, 'w') as file_w:
        file_w.write(report_content)
        
    print ("Wrote secondary output to {0}".format(file_path))
    print ("completed successfully")



