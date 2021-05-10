
import acm
import os

class RunScriptGuiValidationError(Exception): pass


class FParameterManager( object ):
    """base class for retrieving FParameter values"""
    
    def __init__(self, name):
        self.params = FParameterManager._get_parameter_values(name)
    
    def get(self, attr_name):
        return self.params.get(attr_name)
            
    @classmethod
    def _get_parameter_values( cls, name ):
        """get values from FParameter by name"""
        values = {}
        template = None
        p = acm.GetDefaultContext().GetExtension( 'FParameters', 'FObject', name )
        try:
            template = p.Value()
        except AttributeError as e:
            acm.Log( "FParameters < %s > not defined." % name )
        if template:
            for k in template.Keys():
                k = str(k)
                value = str( template.At(k) )
                values[ str(k) ] = value
        return values
    
class FAptReportParameters( FParameterManager ):
    NAME        = 'FAptReportParameters'
    
    def __init__(self):
        FParameterManager.__init__(self, self.__class__.NAME)
    
class FAptPath(object):
    UNIVERSE = 'apt_universe.xml'
    COMPOSITION = 'apt_compostion.xml'
    LOG = 'apt_report_log.txt'
    OUTPUT_PATH = FAptReportParameters().get('OUTPUT_PATH')
    
    @staticmethod
    def get_customer_name():
        try:
            return acm.ADSAddress().split('_')[0]
        except IndexError:
            raise err
            
    @classmethod
    def get_composition_path(cls):
        return os.path.join(cls.OUTPUT_PATH, cls.COMPOSITION)

    @classmethod
    def get_universe_path(cls):
        return os.path.join(cls.OUTPUT_PATH, cls.UNIVERSE)
        
    @classmethod
    def get_apt_report_log_path(cls):
        return os.path.join(cls.OUTPUT_PATH, cls.LOG)

