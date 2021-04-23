"""-----------------------------------------------------------------------------
PROJECT                 : N/A
PURPOSE                 : Synchronises SOB contexts
DEPATMENT AND DESK      : Middle Office / Technical Support
REQUESTER               : Lourens Harmse
DEVELOPER               : Francois Truter
CR NUMBER               : 645864
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer               Description
--------------------------------------------------------------------------------
2010-11-18 498014    Francois Truter         Initial Implementation
2010-12-17 527183    Francois Truter         Increased sob name length to 31 
                                             for yield curves & dividend streams
2011-02-03 562280    Francois Truter         Added ATS user test
2011-02-24 582493    Francois Truter         Added Instrument Spread curves
2011-02-25 645864    Francois Truter         Dividend Streams copied to SPOT_SOB
2011-11-09 824435    Jaysen Naicker          Added section at end of MOPL upodate to relink REPO SOB curves properly
2012-02-13 891774    Paul Jacot-Guillarmod   Added functionality to update PrimeFlat_SOB on a daily basis
2013-10-21 1448685   Jan Sinkora             Pointing Attribute Spread curves' spreads to the correct points
"""

import acm
import sys
import traceback
from datetime import datetime
import FRunScriptGUI

LOG_FILE = None
SPOT_MARKET = 'SPOT'

class ContextLinkParameterDoesNotExist(Exception): pass

class SobParameterUpdateStatus:
    New = 0
    Updated = 1
    Nothing = 2
    Error = 3

class CustomContextLink:

    _sobSuffix = '_SOB'
    _paramClass = None
    _sobNameLength = 30
    
    @classmethod
    def _getSobParameterName(cls, parameterName):
        return parameterName + cls._sobSuffix

    @classmethod
    def _validateSobParameterCreate(cls, parameter):
        return True
        
    @classmethod
    def _beforeSobParameterCommit(cls, parameter, sobParameter):
        pass

    @classmethod
    def _getUpdatedSobParameter(cls, parameter):
        if not cls._validateSobParameterCreate(parameter):
            return None
        
        parameterName = '%(name)s (%(type)s)' % {'name': parameter.Name(), 'type': parameter.ClassName()}
        sobParameter = None
        sobName = cls._getSobParameterName(parameter.Name())
        maxLength = cls._sobNameLength
        if len(sobName) > maxLength:
            _log('Did not create SOB parameter for [%s] - SOB name [%s] is longer than %i characters.' % (parameterName, sobName, maxLength))
            return None

        try:            
            paramClass = cls._paramClass
            sobParameter = paramClass[sobName]
            status = SobParameterUpdateStatus.Error

            if not sobParameter:
                sobParameter = parameter.Clone()
                status = SobParameterUpdateStatus.New
            else:
                if parameter.UpdateTime() > sobParameter.UpdateTime() or not sobParameter.UpdateUser().Name().startswith('ATS'):
                    sobParameter.Apply(parameter)
                    status = SobParameterUpdateStatus.Updated
                else:
                    status = SobParameterUpdateStatus.Nothing
            
            sobParameter.Name(sobName)
            cls._beforeSobParameterCommit(parameter, sobParameter)
            sobParameter.Commit()

        except Exception, ex:
            _logError('An error occurred while updating %(sob_name)s:\n\t%(error)s' % \
                {'sob_name': sobName, 'error': str(ex)})
        else:
            if status == SobParameterUpdateStatus.New:
                _log('Successfully created new SOB parameter for %(name)s: %(sobName)s' % {'name': parameterName, 'sobName': sobName})
            elif status == SobParameterUpdateStatus.Updated:
                _log('Successfully updated SOB parameter for %(name)s: %(sobName)s' % {'name': parameterName, 'sobName': sobName})
            elif status == SobParameterUpdateStatus.Nothing:
                _log('Nothing to update for %(name)s: %(sobName)s is up to date' % {'name': parameterName, 'sobName': sobName})
                
        return sobParameter

    def __init__(self, contextLink):
        self._contextLink = contextLink
        self._parameter = self._getParameter()
        self._sobParameter = None
        self._sobParameterSet = False

        
    def __cmp__(self, other):
        if isinstance(other, CustomContextLink):
            rhs = other._contextLink
            rhsSobName = self._getSobParameterName(other.parameter.Name())
        elif other.IsKindOf(acm.FContextLink):
            rhs = other 
            rhsSobName = self._getSobParameterName(rhs.Name())
        else:
            return 1
            
        lhs = self._contextLink
        lhsSobName = self._getSobParameterName(self.parameter.Name())
        if lhs.Currency() == rhs.Currency() \
            and lhs.GroupChlItem() == rhs.GroupChlItem() \
            and lhs.Instrument() == rhs.Instrument() \
            and lhs.MappingType() == rhs.MappingType() \
            and (lhs.Name() == rhs.Name() or lhs.Name() == rhsSobName or lhsSobName == rhs.Name())\
            and lhs.Type() == rhs.Type():
            return 0
        else:
            return 1
            
    def _getParameter(self):
        cls = self.__class__
        paramClass = cls._paramClass
        name = self._contextLink.Name()
        parameter = paramClass[name]
        if not parameter:
            raise ContextLinkParameterDoesNotExist('Could not load %s [%s].' % (paramClass.Name(), name))
            
        return parameter
        
    @property
    def parameter(self):
        return self._parameter
    
    @property
    def sobParameter(self):
        if not self._sobParameterSet:
            cls = self.__class__
            self._sobParameter = cls._getUpdatedSobParameter(self._parameter)
            self._sobParameterSet = True
        return self._sobParameter
            
    def CreateSobContextLink(self, context):
        if self.sobParameter:
            try:
                newLink = self._contextLink.Clone()
                newLink.Context(context)
                newLink.Name(self.sobParameter.Name())
                newLink.Commit()
            except Exception, ex:
                _logError('An error occurred while creating the context link for %(name)s (%(type)s) in context %(context)s:\n\t%(error)s' % \
                    {'name': self.sobParameter.Name(), 'type': self._contextLink.Type(), 'context': context.Name(), 'error': str(ex)})
            else:
                _log('Context link successfully created for %(name)s in context %(context)s.' % \
                    {'name': self.sobParameter.Name(), 'context': context.Name()})
                return True
                
        return False
            
    def CreateOrUpdateSobParameter(self):
        if self.sobParameter:
            return True
                
        return False
        
class VolatilityContextLink(CustomContextLink):

    _paramClass = acm.FVolatilityStructure
    
    @classmethod
    def _beforeSobParameterCommit(cls, parameter, sobParameter):
        underlying = parameter.UnderlyingStructure()
        if underlying:
            sobUnderlying = cls._getUpdatedSobParameter(underlying)
            if not sobUnderlying:
                raise Exception('Could not create underlying [%(underlying)s] for SOB Volatility Structure [%(name)s].' % {'underlying': underlying.Name(), 'name': sobParameter.Name()})
            sobParameter.UnderlyingStructure(sobUnderlying)
        
class YieldCurveContextLink(CustomContextLink):

    _sobSuffix = '-SOB'
    _paramClass = acm.FYieldCurve
    _sobNameLength = 31
    
    @classmethod
    def _validateSobParameterCreate(cls, parameter):
        if parameter.Type() in ('Attribute Spread', 'Instrument Spread'):
            return True
        else:
            return False
    
    @classmethod
    def _getCorrectPeriodPoint(cls, curve, oldPoint):
        for p in curve.Points():
            if (p.DatePeriod_count() == oldPoint.DatePeriod_count()
                    and p.DatePeriod_unit() == oldPoint.DatePeriod_unit()
                    and p.Date() == oldPoint.Date()):
                return p
        
    @classmethod
    def _beforeSobParameterCommit(cls, parameter, sobParameter):
        if sobParameter.Type() == 'Attribute Spread':
            attrs = sobParameter.Attributes()
            for attr in attrs:
                for spread in attr.Spreads():
                    if spread.Point().Curve().Name() != sobParameter.Name():
                        spread.Point(cls._getCorrectPeriodPoint(sobParameter, spread.Point()))
        
class PriceFindingContextLink(CustomContextLink):
    _spotMarket = acm.FMarketPlace[SPOT_MARKET]
    _sobMarket = acm.FMarketPlace['SPOT_SOB']
    _paramClass = acm.FPriceFinding
    _sobNameLength = 39
    
    @classmethod
    def _validateSobParameterCreate(cls, parameter):
        if not PriceFindingContextLink._spotMarket:
            _log('Did not create SOB parameter for Price Finding [%s]: SPOT Market did not load.' % parameter.Name())
            return False
             
        if not PriceFindingContextLink._sobMarket:
            _log('Did not create SOB parameter for Price Finding [%s]: SPOT_SOB Market did not load.' % parameter.Name())
            return False
            
        market = parameter.Market()
        
        if not market:
            # no direct market is defined, look in the search order
            searchOrder = parameter.MarketSearchOrder()
            if searchOrder:
                searchOrder = map(lambda m: m.strip(), searchOrder.split(','))
                # search order is defined, look for SPOT
                if searchOrder[0] == SPOT_MARKET:
                    # SPOT is first in the search order
                    return True
                else:
                    # the search order does not start with SPOT
                    return False
                    _log('Did not create SOB parameter for Price Finding [%s], the original does not start with SPOT.' % parameter.Name())
            else:
                # no search order, therefore no market at all
                _log('Did not create SOB parameter for Price Finding [%s], no market is set.' % parameter.Name())
                return False
        else:
            if market == PriceFindingContextLink._spotMarket:
                # market is spot, needs to be copied
                return True
            else:
                # direct market is defined, but is not spot
                _log('Did not create SOB parameter for Price Finding [%s], Market [%s] - only SPOT Market links to be copied.' % (parameter.Name(), market.Name()))
                return False
    
    @classmethod
    def _beforeSobParameterCommit(cls, parameter, sobParameter):
        sobParameter.Market(PriceFindingContextLink._sobMarket)
        sobParameter.MarketSearchOrder('')
        
class DividendStreamContextLink(CustomContextLink):

    _paramClass = acm.FDividendStream
    _sobNameLength = 31
        
def _strTime(time = datetime.now()):
    return time.strftime('%Y-%m-%d %H:%M:%S')
    
def _log(message):
    message = '%(time)s: %(message)s' % {'time': _strTime(datetime.now()), 'message': message}
    print(message)
    if LOG_FILE:
        try:
            LOG_FILE.write(message + '\n')
        except Exception, ex:
            print('An error occurred writing to the log file: ' + str(ex))
    
def _logError(message):
    _log(message + '\n\t' + traceback.format_exc())

def _getContext(name):
    context = acm.FContext[name]
    if not context:
        raise Exception('Could not load context [%s].' % name)
    
    return context
    
def _asList(_iterable):
    _list = []
    for i in _iterable:
        _list.append(i)
    return _list

def _iterable(obj):
    iterable = False
    try:
        iter(obj)
    except:
        pass
    else:
        iterable = not isinstance(obj, basestring)
    
    return iterable
    
def _loadFContextLinks(context, types):
    _list = []
    if _iterable(types):
        for type in types:
            _list.extend(_loadFContextLinks(context, type))
    else:
        if types:
            return _asList(acm.FContextLink.Select("context = %i and type = '%s'" % (context.Oid(), types)))
        else:
            return _asList(acm.FContextLink.Select("context = %i" % context.Oid()))
            
    return _list
        
    
def _getGlobalContextLinks():
    _list = []
    types = []
    globalContext = _getContext('ACMB Global')
    
    for cls in [VolatilityContextLink, YieldCurveContextLink, PriceFindingContextLink, DividendStreamContextLink]:
        if cls == VolatilityContextLink:
            types = ['Volatility']
        elif cls == YieldCurveContextLink:
            types = ['Yield Curve', 'Repo']
        elif cls == PriceFindingContextLink:
            types = ['Price Finding']
        elif cls == DividendStreamContextLink:
            types = ['Dividend Stream']
    
        for link in _loadFContextLinks(globalContext, types):
            customContextLink = None
            try:
                customContextLink = cls(link)
            except ContextLinkParameterDoesNotExist, ex:
                _log(str(ex))
            else:
                 _list.append(customContextLink)
                 
    return _list
    
def _updateSobParameters(globalLinks):
    stopProcessing = []
    alreadyUpdated = []
    for globalLink in globalLinks:
        if globalLink.parameter not in alreadyUpdated:
            if not globalLink.CreateOrUpdateSobParameter():
                stopProcessing.append(globalLink)
            else:
                alreadyUpdated.append(globalLink.parameter)
                    
    for link in stopProcessing:
        globalLinks.remove(link)

def _removeLinksNotInGlobalContext(globalLinks, sobLinks):
    for sobLink in sobLinks:
        if not sobLink in globalLinks:
            try:
                sobLink.Delete()
            except:
                _log('An error occurred trying to delete context link for %(name)s (%(type)s) in context %(context)s:\n\t%(error)s' %\
                    {'name': sobLink.Name(), 'type': sobLink.Type(), 'context': sobLink.Context().Name(), 'error': str(ex)})
            else:
                _log('Successfully deleted context link for %(name)s (%(type)s) in context %(context)s.' %\
                    {'name': sobLink.Name(), 'type': sobLink.Type(), 'context': sobLink.Context().Name()})

def _addPrimeFlatMapping(context):
    ''' Create a mapping that maps the FLAT - 0% curve to the ZAR money market curve in the context
    '''
    currency = acm.FInstrument['ZAR']
    parameterType = 'Yield Curve'
    parameterName = 'FLAT - 0%'
    mappingType = 'Instrument'
    
    flatMapping = acm.FContextLink.Select("context = %i and mappingType = '%s'and type = '%s' and name = '%s' and currency = %i and instrument = %i" % \
                                        (context.Oid(), mappingType, parameterType, parameterName, currency.Oid(), currency.Oid()))    
    if not flatMapping:
        try:
            primeFlatLink = acm.FContextLink()
            primeFlatLink.Context(context)
            primeFlatLink.Currency(currency)
            primeFlatLink.Instrument(currency)
            primeFlatLink.MappingType(mappingType)
            primeFlatLink.Name(parameterName)
            primeFlatLink.Type(parameterType)
            primeFlatLink.Commit()
        except Exception, ex:
            print('An error occured in adding the Flat mapping to the context ' + context.Name() + ': ' + str(ex))
            
def main(logFilepath):
    try:
        global LOG_FILE
        with open(logFilepath, "w") as LOG_FILE:
            try:
                ZAR_CALENDAR = 'ZAR Johannesburg'
                zarCalendar = acm.FCalendar[ZAR_CALENDAR]
                if not zarCalendar:
                    raise Exception('Could not load calendar [%s].' % ZAR_CALENDAR)

                yesterday = acm.Time().DateAddDelta(acm.Time().DateToday(), 0, 0, -1)
                if zarCalendar.IsNonBankingDay(None, None, yesterday):
                    _log('Yesterday was not a banking day - script will not continue.')
                    return

                startTime = datetime.now()
                _log('MOPL SOB copy script started.')

                globalLinks = _getGlobalContextLinks()
          
                volSobContext = _getContext('VOL_SOB')
                volSobLinks = _loadFContextLinks(volSobContext, None)
                
                divSobContext = _getContext('DIV_SOB')
                divSobLinks = _loadFContextLinks(divSobContext, None)
                
                spotSobContext = _getContext('SPOT_SOB')
                spotSobLinks = _loadFContextLinks(spotSobContext, None)
                
                primeFlatSobContext = _getContext('PrimeFlat_SOB')
                primeFlatSobLinks = _loadFContextLinks(primeFlatSobContext, None)
                
                _updateSobParameters(globalLinks)
                _removeLinksNotInGlobalContext(globalLinks, volSobLinks + spotSobLinks + divSobLinks + primeFlatSobLinks)
                            
                for globalLink in globalLinks:
                    if isinstance(globalLink, DividendStreamContextLink) and not globalLink in divSobLinks:
                        globalLink.CreateSobContextLink(divSobContext)
                    if isinstance(globalLink, VolatilityContextLink) and not globalLink in volSobLinks:
                        globalLink.CreateSobContextLink(volSobContext)
                    if not globalLink in spotSobLinks:
                        globalLink.CreateSobContextLink(spotSobContext)
                    if not globalLink in primeFlatSobLinks:
                        globalLink.CreateSobContextLink(primeFlatSobContext)
                
                # Map the flat curve to the PrimeFlat_SOB context
                _addPrimeFlatMapping(primeFlatSobContext)
                
                endTime = datetime.now()
                timeTaken = endTime - startTime
                _log('MOPL SOB copy script completed. Time to run: ' + str(timeTaken))
            except Exception, ex:
                _logError('A fatal error has occurred, MOPL SOB copy script aborted:\n\t' + str(ex))
    except Exception, ex:
        print('A fatal error has occurred, MOPL SOB copy script aborted:\n\t' + str(ex))
        
    try:
        curves = {}
        curves['USD-S&P500_REPO'] = 'USD-S&P500_REPO-SOB'
        curves['EUR-EUROSTOXX_REPO'] = 'EUR-EUROSTOXX_REPO-SOB'
        curves['GBP-FTSE_REPO'] = 'GBP-FTSE_REPO-SOB'

        for k in curves.keys():
            yc = acm.FYieldCurve[k]
            sob = acm.FYieldCurve[curves[k]]

            sob_list = {}
            
            for pt in yc.Points():        
                spread = acm.FYCSpread.Select("point = '%s'" %pt.Oid())      
                for sp in spread:
                    if curves[k] == sp.Attribute().Curve().Name():
                        yc_pnt = sp.Point().Oid()
                        for sob_pnt in sob.Points():
                            if sob_pnt.Date() == sp.Point().Date():
                                print(sp.Point().Oid(), sob_pnt.Oid())
                                sp.Point(sob_pnt)
                                sp.Commit()
    except Exception, ex:
        print('A fatal error has occurred, MOPL REPO SOB re-linking aborted:\n\t' + str(ex))



fileSelection = FRunScriptGUI.OutputFileSelection("All Files (*.*)|*.*||")
logFileKey = '0'
ael_variables = [
    [logFileKey, 'Log File', fileSelection, None, fileSelection, 1, 1, 'The file to which this process will write log details', None, 1]
]

def ael_main(parameters):
    try:
        logFile = parameters[logFileKey]  
        filepath = logFile.SelectedFile().Text()
        main(filepath)
        print('Wrote secondary output to:::' + filepath)
    except Exception, ex:
        print(ex)
