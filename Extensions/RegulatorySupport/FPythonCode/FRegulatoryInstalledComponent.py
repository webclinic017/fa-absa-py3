#grouping: installed component

'''---------------------------------------------------------------------------------
MODULE
    FRegulatoryInstalledComponent -
DESCRIPTION:
    The module that validates whether the installation
    has all the basic setup required for the expected functioning
     of the component
VERSION: 1.0.25(0.25.7)
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code
     within the core is not supported.
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to
     this module at user end
---------------------------------------------------------------------------------'''
import ast
import InstalledComponentBase
import FRegulatoryConfigParam
import FRegulatorySupportValidateSetup
import FRegulatoryLogger
config_param = FRegulatoryConfigParam.FRegulatoryConfigParam()

loggerName = 'FRegulatoryInstalledComponent'


class Diagnostics(InstalledComponentBase.InstalledComponentDiagnostics):
    """call to check the basic setup for RegulatorySupport"""
    def __init__(self):
        super(Diagnostics, self).__init__()
        self._name = 'RegulatorySupport'
        self._version = config_param.get_paramvalue('FREGULATORY_VERSION')
        self._moduleVersions = {'No dependency' : ''}
        self.validateSetup = FRegulatorySupportValidateSetup.FRegulatorySupportValidateSetup()
        self._testMeAreas = [{'TestRegulatoryAPIs' : ['InstrumentRegulatoryAPIs',\
                                'TradeRegulatoryAPIs', 'PartyRegulatoryAPIs',\
                                'ContactRegulatoryAPIs', 'PersonRegulatoryInfoAPIs']},\
                             {'TestAddInfosSpecsOn' : ['Trade', 'Instrument', 'Contact', 'Party']},\
                             {'TestTernaryAPIs' : ['TernaryRegulatoryAPIsOnInstrument',\
                                'TernaryRegulatoryAPIsOnTrade', 'TernaryRegulatoryAPIsOnParty',\
                                'TernaryRegulatoryAPIsOnAccount',]},\
                             'TestRegulatoryChoiceLists']
        self._description = "The RegulatorySupport provides the interface \
        and APIs to store Regulatory related data into Front Arena"
        self._releaseDate = '31-Jan-2020'
        self._isBuiltInModule = 'No'

    def testMe(self, area=None, subArea=None):
        """Test the setup of RegulatorySupport/Info"""
        complete_result = True
        try:
            if not area:
                for eachArea in self._testMeAreas:
                    if isinstance(eachArea, dict):
                        eachAreaValues = list(eachArea.values())
                        for eachSubArea in eachAreaValues[0]:
                            result = self.testMe(list(eachArea.keys())[0], eachSubArea)
                            if not result :
                                complete_result = False
                        else:
                            result = self.testMe(eachArea)
                            if not result :
                                complete_result = False
            else:
                FRegulatoryLogger.INFO(loggerName, 'Testing against "%s"' % area)
                if subArea:
                    #result = ast.literal_eval('self.validateSetup.' + subArea + '()')
                    result = eval('self.validateSetup.' + subArea + '()')
                else:
                    if not isinstance(area, dict):
                        result = eval('self.validateSetup.' + area + '()')
                        if not result:
                            complete_result = False
        except Exception as error:
            FRegulatoryLogger.INFO(loggerName, 'Testing status - FAIL. Error : <%s>'%str(error))
            complete_result = False
        return complete_result

    def logMe(self, area=None, subArea=None):
        """Log the setup of RegulatorySupport/Info"""
        FRegulatoryLogger.INFO(loggerName, 'Logging for %s' % self._name)
        result = []
        try:
            if not area:
                for eachArea in self._logMeAreas:
                    if isinstance(eachArea, dict):
                        for eachSubArea in list(eachArea.values())[0]:
                            self.logMe(list(eachArea.keys())[0], eachSubArea)
                    else:
                        self.logMe(eachArea)
            if area == 'FParameter':
                FRegulatoryLogger.INFO(loggerName, 'Logging for %s, (area=%s)' % (self._name, area))
                result = False
            elif area == 'Configuration':
                FRegulatoryLogger.INFO(loggerName, 'Logging for %s, (area=%s)' % (self._name, area))
                result = True
            return result
        except Exception as error:
            FRegulatoryLogger.ERROR(loggerName, error)

