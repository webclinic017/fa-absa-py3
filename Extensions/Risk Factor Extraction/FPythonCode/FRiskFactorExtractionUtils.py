
import exceptions
import math
import itertools
import os
import FRiskFactorFileProcessing
import FFileUtils

import acm

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

risk_factor_is_arithmetic = acm.GetFunction("riskFactorIsArithmetic", 1)

NEWLINE_TOKEN = "\n"

class RiskFactorDynamicsEnum(object):
    """
    Enum describing the risk factor process dynamics.
    """
    GEOMETRIC = 10
    ARITHMETIC = 20

EPS = 0.00000005

risk_factor_type_dynamics_mapping = {
    'Benchmark Price' : RiskFactorDynamicsEnum.GEOMETRIC,
    'Benchmark Volatility' : RiskFactorDynamicsEnum.ARITHMETIC,
    
    'Commodity': RiskFactorDynamicsEnum.GEOMETRIC,
    'Dividend' : RiskFactorDynamicsEnum.GEOMETRIC,
    'Equity': RiskFactorDynamicsEnum.GEOMETRIC,
    'FX': RiskFactorDynamicsEnum.GEOMETRIC,
    
    'Inflation Benchmark Price' : RiskFactorDynamicsEnum.GEOMETRIC,
    'Inflation Rate' : RiskFactorDynamicsEnum.ARITHMETIC,
    'Equity Repo Rate' : RiskFactorDynamicsEnum.ARITHMETIC,
    
    'Par CDS Rate' :  RiskFactorDynamicsEnum.ARITHMETIC,
    'Stored Instrument Spread' : RiskFactorDynamicsEnum.ARITHMETIC,
    'Volatility Skew Parameters (SVI)' : RiskFactorDynamicsEnum.GEOMETRIC,
    
    'Zero Coupon' : RiskFactorDynamicsEnum.ARITHMETIC,
    'Volatility': RiskFactorDynamicsEnum.ARITHMETIC
}

def construct_risk_factor_instance_dict(setup):
    external_id_to_instance_dictionary = {}
    for collection in setup.RiskFactorCollections():
        for instance in collection.RiskFactorInstances():
            ext_id = instance.AdditionalInfo().External_Id() 
            if ext_id and not ext_id in external_id_to_instance_dictionary:
                external_id_to_instance_dictionary[ext_id] = instance
    
    return external_id_to_instance_dictionary 

def risk_factor_dynamics_mapper_from_risk_factor_setup(external_id, setup, ext_id_to_instance_dict):
    try:
        rf_instance = ext_id_to_instance_dict[external_id]
    except:
        rf_instance = None 
        
    if rf_instance:
        collection = rf_instance.RiskFactorCollection()
        type = collection.RiskFactorType()
        try:
            dynamics = risk_factor_type_dynamics_mapping[type]
        except:
            err_msg = "No dynamic type set for risk factor collection: \'%s\', with risk factor type: %s" %(rf_instance.RiskFactorCollection().DisplayName(), rf_instance.RiskFactorCollection().RiskFactorType())
            raise RiskFactorMappingError(err_msg)
        return dynamics
        
    return None

class RiskFactorMappingError(exceptions.Exception):
    pass

class SourceDataError(exceptions.Exception):
    pass
    
class SourceDataOutOfRange(SourceDataError):
    pass
    
class SourceDataInvalidValueError(SourceDataError):
    pass
    
def is_zero(x):
    """Do not want to test x == 0.0 (float precision)."""
    return abs(x) < EPS
    
def validated_value(x, rf_dynamics):
    """Do not accept degenerate values in the scenario."""
    x = float(x)
    if (math.isnan(x) or 
        (is_zero(x) and rf_dynamics == RiskFactorDynamicsEnum.GEOMETRIC)):
        raise SourceDataInvalidValueError("'%s' is not a valid value" % x)
    return x
    
def extract_value_on_date(ext_id, date, input_data, labels_token, rf_dynamics):
    """
    Main data extraction function for historical time series data.
    Throws SourceDataError if data is not available on ext_id*date
    """
    dates = input_data[labels_token]
    try:
        vidx = dates.index(date)
    except ValueError:
        err_msg = "Date '%s' is out of range" % date
        raise SourceDataOutOfRange(err_msg)
    if vidx is None:
        err_msg = "No risk factor data on %s" % date
        raise SourceDataError(err_msg)
    try:
        vals = input_data[ext_id]
    except KeyError:
        err_msg = "No risk factor data for '%s'" % ext_id
        raise SourceDataError(err_msg)
    try:
        return validated_value(vals[vidx], rf_dynamics)
    except IndexError:
        err_msg = "%s is out of range for extid '%s'" % (date, ext_id)
        raise SourceDataOutOfRange(err_msg)
         
def read_risk_factor_specs(extern_id, spec_header):
    """
    Reads the corresponding risk factor specification for the
    external id and the risk factor specification header.
    """
    constraint = "name = '%s' and rfspec = '%s'" % \
                 (extern_id, spec_header.Name())
    rf_specs = acm.FRiskFactorSpec.Select(constraint)\
                                  .AsArray()\
                                  .SortByProperty("Rfg")
    return rf_specs
         
def first_risk_factor_from_ext_id(ext_id, spec_header):
    specs = read_risk_factor_specs(ext_id, spec_header)
    if len(specs) == 0:
        spec_header_name = spec_header.Name()
        err_msg = "%s does not exist in %s" % (ext_id, spec_header_name)
        raise RiskFactorMappingError(err_msg)
    else:
        return specs[0]
   
def risk_factor_dynamics_from_ext_id(ext_id, spec_header):
    rf = first_risk_factor_from_ext_id(ext_id, spec_header)
    if risk_factor_is_arithmetic(rf):
        return RiskFactorDynamicsEnum.ARITHMETIC
    else:
        return RiskFactorDynamicsEnum.GEOMETRIC
            
def do_write(text, ostream=None):
    if ostream:
        ostream.write(text)

def get_output_filename_simple(dir_path, filename, overwrite=False, extension=".txt"):
    if hasattr(dir_path, "AsString"):
        dir_path = dir_path.AsString()
    if hasattr(filename, "AsString"):
        filename = filename.AsString()
    dir_path = FFileUtils.expandEnvironmentVar(dir_path)
    createPath(dir_path)
    return getFileName(dir_path, overwrite, filename, extension)

def is_date(strdate):
    try:
        return acm.Time().IsValidDateTime(strdate)
    except RuntimeError:
        return False

def adjust_date(date, base_date, calendar, bdmethod):
    strdate = str(date).strip()
    if strdate.upper() in ["TODAY", "NOW"]:
        day = acm.Time.DateToday()
    elif is_date(strdate):
        day = strdate
    else:
        try:
            day = acm.Time().PeriodSymbolToRebasedDate(strdate, base_date)
            if not day:
                raise ValueError("")
        except:
            raise ValueError("Date must be either a date,"
                             " 'TODAY' or a dateperiod, not %s" % strdate)
    return calendar.ModifyDate(None, None, day, bdmethod)

def createPath(outputDir):
    if not os.path.exists(outputDir):
        try:
            os.makedirs(outputDir)
            logger.LOG('Created report output directory:' + outputDir)
        except:
            msg = 'Failed to create report directory:' + outputDir
            logger.ELOG( msg )
            raise
                        
def getFileName(outputDir, overwrite, fileName, ext):
    for i in range(1, 100):
        if i == 1:
            numbering = ''
        else:
            numbering = '_' + str(i)
        testFile = os.path.join(outputDir, fileName + numbering + ext)
        if overwrite or not os.path.exists(testFile):
            return testFile
        else:
            msg = 'File already exists:' + testFile
            logger.ELOG(msg)
            raise IOError(msg)
    return 0

