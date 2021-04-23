""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/Autolink/src/Autolink.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FAutolink - Maintainance of database entities

DESCRIPTION
    Automatic handling and maintainance of yield curve, volatility
    surfaces, instrument pages and Mapping instrument fields to
    Instruments in database.

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import ael
import acm
import FLogger
import os
import os.path
import string
default_rules = 'Select Rules'
FASQL_Query = 30

#===============================================================================
# Main classes to handle mapping logic
#===============================================================================

#------------------------------------------------------------------------------
# Base classes
#------------------------------------------------------------------------------

class absRules:
    '''Base class for rule handling. Not to
       be instanciated.
       Inherited by YCRules, VolSurfaceRules etc.
    '''
    def checkRules(self,commit=0):
        '''Go through all rules, checking for insertion/removal
           of instruments from structures.'''
        logger.DLOG('In checkrules()')
        for rule in self.rules:
            logger.LOG("Processing rule <%s>" % rule.Name())
            struct = self.structures[self.ruleToStructName(rule.Name())]
            structInsNames = struct.getInstrumentNames()
            ruleInsNames = []
            qry = rule.Query()
            results = qry.Select()
            for ins in results:
                ruleInsNames.append(ins.Name())

            if ruleInsNames:
                logStr = \
                listToTableString("Unprocessed query instruments",
                                  ruleInsNames)
                logger.DLOG(logStr)

            removedNames, ruleInsNames = self.handle_acm_expiry(ruleInsNames)
            removedNames, addedNames, ruleInsNames = self.handle_explicit_rules(rule, ruleInsNames)

            # insertion pass

            addedNames = []
            if self.globalParams.get('InsName'):
                insName = self.globalParams['InsName']
                if not insName in structInsNames:
                    struct.insertInstrument(insName,commit)
                    addedNames.append(insName)
            else:
                for insName in ruleInsNames:
                    if not insName in structInsNames:
                        struct.insertInstrument(insName,commit)
                        addedNames.append(insName)

            # removal pass
            for insName in structInsNames:
                if not insName in ruleInsNames:
                    struct.removeInstrument(insName,commit)
                    removedNames.append(insName)
            if addedNames:
                logStr = listToTableString("Inserted instruments into <%s>" \
                                               % struct.name, addedNames)
                logger.LOG(logStr)
            if removedNames:
                logStr = listToTableString("Removed instruments from <%s>" \
                                               % struct.name, removedNames)
                logger.LOG(logStr)

    def handle_acm_expiry(self, ruleInsNames):
        # handle ACM expiry
        removedNames = None
        #ruleInsNames = None
        if globalParams["excludeACMExired"]:
            logger.LOG("Exluding ACM expired instruments")
            oldRuleInsNames = ruleInsNames
            ruleInsNames = [insName for insName in ruleInsNames \
                                if not isACMExpired(insName)]
            removedNames = [ins for ins in oldRuleInsNames \
                                if ins not in ruleInsNames]
            if removedNames:
                logStr = \
                listToTableString("Excluded ACM expired instruments",
                                      removedNames)
                logger.DLOG(logStr)
        return removedNames, ruleInsNames

    def handle_explicit_rules(self, rule, ruleInsNames):
        # handle explicit rules
        if explicitRuleMappingTable:
            if rule.Name() in explicitRuleMappingTable.keys():
                logger.LOG('Filter by explicit rule %s' % rule.Name())
                oldRuleInsNames = ruleInsNames
                try:
                    ruleInsNamesTemp = \
                        explicitRuleMappingTable[rule.Name()](ruleInsNames)
                    ruleInsNames = ruleInsNamesTemp
                except:
                    logger.ELOG('Error executing explicit rule %s' \
                                         % rule.Name)
                removedNames = [ins for ins in oldRuleInsNames \
                                    if ins not in ruleInsNames]
                addedNames = [ins for ins in ruleInsNames \
                                    if ins not in oldRuleInsNames]
                if removedNames:
                        logStr = \
                        listToTableString("Explicitly removed instruments",
                                          removedNames)
                        logger.DLOG(logStr)

                if addedNames:
                        logStr = \
                        listToTableString("Explicitly added instruments",
                                          addedNames)
                        logger.DLOG(logStr)
                return (removedNames, addedNames, ruleInsNames)
            else:
                return ([], [], ruleInsNames)
        else:
            return ([], [], ruleInsNames)

    def getStructures(self):
        '''Retrieves structure associated with the rules.
           Abstract method, must be implemented in the derived class.'''
        raise NotImplementedError('Abstract method, please override in derived class')

    def getRules(self):
        '''Extracts all query rules from the database.'''
        logger.DLOG('In getRules()')
        tmpRules = None

        textObjects = ael.TextObject.select('type=%s' %FASQL_Query)
        if textObjects:
            tmpRules = textObjects.members()

        if tmpRules == []:
            logger.LOG('Found no rules')
        for rule in tmpRules:
            acm_query = acm.FStoredASQLQuery[rule.name]
            if acm_query:
                self.rules.append(acm.FStoredASQLQuery[rule.name])
                self.ruleNames.append(rule.name)
        if self.ruleNames:
            logStr = \
            listToTableString("Query rules found",self.ruleNames)
            logger.LOG(logStr)

    def ruleToStructName(self,ruleName):
        """
        Extracts the struct name from the rule name.
        """
        escapes = {"__":"/"}
        # remove rule prefix
        name = ruleName.replace(self.nameStandard+'-','')
        for esc in escapes.keys():
            name = name.replace(esc,escapes[esc])
        return name

    def commitStructures(self,structureList=[]):
        logger.DLOG('In commitStructures()')
        if not structureList: structureList = self.structures.values()
        for structure in structureList:
            structure.commit()

    def commitInstruments(self, instrumentList=[]):
        logger.DLOG('In commitInstruments()')
        if not instrumentList:
            instrumentList = self.instruments
            for ins in instrumentList:
                try:
                    ins.Commit()
                except Exception as e:
                    logger.ELOG('Cannot commit Instrument <%s>\n %s'%(ins.Name(), e))
        logger.LOG('Instrument Fields mapping procedure Completed')

class absStructure:
    '''Base container class for ael structures. Not to be instanciated.
       Inherited by Page/VolSurface/YCurve etc.
    '''
    def getOid(self, name):
        oid = 0
        prefix = (name[:4]).upper()
        if prefix == 'OID:':
            try:
                oid = int(name[4:])
            except:
                oid = 0
        return oid

    def getInstrumentNames(self):
        '''Retrieves the names of instruments in
           instrument list.'''
        logger.DLOG('In getInstrumentNames()')
        insNameList = []
        if self.instruments:
            for ins in self.instruments:
                try:
                    if ins.insid:
                        insNameList.append(ins.insid)
                except Exception as e:
                    try:
                        if ins.Name():
                            insNameList.append(ins.Name())
                    except Exception as e:
                        logger.ELOG(str(e))
        return insNameList

    def getInstruments(self):
        '''Retrieves all instruments currently in the structure.'''
        raise NotImplementedError('Abstract method. Must be implemented in derived class')

    def insertInstrument(self,name,commit=0):
        '''Inserts an instrument into the structure.'''
        raise NotImplementedError('Abstract method. Must be implemented in derived class')

    def removeInstrument(self,name,commit=0):
        '''Removes an instrument from the structure.'''
        raise NotImplementedError('Abstract method. Must be implemented in derived class')

    def commit(self):
        '''Commit earlier add and remove'''
        logger.DLOG('In commit()')
        if self.struct:
            logger.LOG('Committing structure <%s>' % self.name)
            try:
                self.struct.commit()
            except:
                try:
                    self.struct.clone()
                except:
                    logger.ELOG('Commit failed for structure <%s>' % self.name)

#------------------------------------------------------------------------------
# Derived classes
#------------------------------------------------------------------------------

class Page(absStructure):
    def __init__(self,name):
        self.struct = None
        if type(name) == type('string'):
            try:
                #id = int(name)
                pass
            except:
                logger.ELOG('Naming of pages must be by their primary keys')
                raise
            #name = id

        if type(name) != type(1):
            nodenumber = 0
            nodenumber = self.getOid(name)
            if not nodenumber:
                nodenumber = self.getNodeNumber(name)
            if nodenumber:
                name = str(nodenumber)

        found = False
        listNodes = ael.ListNode.select()
        for node in listNodes:
            if str(node.nodnbr) == str(name):
                try:
                    found = True
                    self.struct = node.clone()
                except Exception:
                    logger.ELOG('Cannot clone Node %s'%name)
                #break
                if self.struct:
                    self.name = self.struct.id
                    self.getInstruments()

        if not found:
            error_msg = '<rulePG-' + str(name) + '> Page structure does not exist'
            logger.ELOG(error_msg)


    def getNodeNumber(self,path):
        folders=path.split('|')
        folderCount=len(folders)-1
        found = False
        listNodes = ael.ListNode.select()
        for node in listNodes:
            count = 1
            if str(node.id) == folders[folderCount]:
                if folderCount ==0:
                    found = True
                else:
                    tmpNode = node
                    while count <=folderCount:
                        father_node = tmpNode.father_nodnbr
                        if str(father_node.id)== folders[folderCount-count]:
                            if count ==folderCount:
                                found = True
                                break
                            else:
                                count = count +1
                                tmpNode = father_node
                        else:
                            break
                if found:
                    return node.nodnbr

        return 0

    def getInstruments(self):
        '''Retrieves all instruments currently in the list
           leaf.
        '''
        logger.DLOG('In Page.getInstruments()')
        self.instruments = []
        for leaf in self.struct.leafs():
            self.instruments.append(leaf.insaddr)

    def insertInstrument(self,name,commit=0):
        '''Inserts a new list leaf into the node.'''
        logger.DLOG('In Page.insertInstruments()')
        ins = ael.Instrument[name]
        newLeaf = ael.ListLeaf.new(self.struct)
        newLeaf.insaddr = ins
        self.instruments.append(ins)

    def removeInstrument(self,name,commit=0):
        '''Removes a list leaf from the node.'''
        logger.DLOG('In Page.removeInstruments()')
        leaves = self.struct.leafs()
        for leaf in leaves:
            if leaf.insaddr.insid == name:
                leaf.delete()

class PageRules(absRules):
    def __init__(self):
        self.nameStandard = 'rulePG'
        self.rules = []
        self.ruleNames = []

        self.globalParams = globalParams
        if type(self.globalParams['PGRules']) == type(()):
            for ruleN in self.globalParams['PGRules']:
                self.ruleNames.append(ruleN)
        else:
            self.ruleNames = self.globalParams['PGRules'].split(',')
        self.nameStandard = 'rulePG'

        if self.globalParams.get('Page'):
            self.ruleNames.append(self.globalParams.get('Task_ruleName'))

        self.structureNames = []
        self.structures = {}
        self.getRules()
        self.getStructures()
        self.checkRules()

    def getStructures(self):
        '''Retrieves pages associated with the rules.'''
        logger.DLOG('In PageRules.getStructures()')
        for rule in self.rules:
            tempPGName = self.ruleToStructName(rule.Name())
            pgTemp = Page(tempPGName)
            if pgTemp.struct:
                self.structures[tempPGName] = pgTemp
            else:
                self.ruleNames.remove(rule.Name())
                self.rules.remove(rule)
        self.structureNames = self.structures.keys()

    def getRules(self):
        """ Get rules stroed in database"""
        logger.DLOG("in PageRules.getRules()")
        if default_rules in self.ruleNames:
            self.ruleNames = []
            absRules.getRules(self)
        else:
            if self.ruleNames and filter(None, self.ruleNames):
                for rules in self.ruleNames:
                    query = acm.FStoredASQLQuery[rules.strip()]
                    if query:
                        self.rules.append(query)
                    else:
                        logger.ELOG('Rule %s not found in database'%rules)

class VolSurface(absStructure):
    def __init__(self,name):
        self.instruments = []
        self.struct = None
        self.vol_oid = None
        if not name:
            logger.ELOG('Must supply volatility structure name')
            raise ValueError('Must supply volatility structure name')

        if type(name) != type(1):
            vol_nbr = 0
            vol_nbr = self.getOid(name)
            if vol_nbr:
                self.vol_oid = str(vol_nbr)

        if self.vol_oid:
            struct = ael.Volatility.read("seqnbr=%s" %self.vol_oid )
            if not struct :
                struct = ael.Volatility[name]
        else:
            struct = ael.Volatility[name]

        if not struct:
            logger.ELOG('Volatility structure <%s> does not exist'%name)
        else:
            try:
                self.struct = struct.clone()
            except Exception:
                logger.ELOG('Cannot clone VolSurface %s'%name)
            if self.struct:
                self.name = self.struct.vol_name
                self.type = self.struct.vol_type
                self.getInstruments()

    def getInstruments(self):
        '''Retrieves all instruments currently in the vol
           structure.
        '''
        logger.DLOG('In VolSurface.getInstruments()')
        self.instruments = []
        if self.type in ['Benchmark',
                         'Benchmark Spread',
                         'Benchmark Call/Put',
                         'Benchmark Spread Call/Put']:
            for pt in self.struct.points():
                self.instruments.append(pt.insaddr)
        # Here additional cases may be entered
        else:
            logger.ELOG('Vol structure type is unknown')
            raise TypeError('Vol structure type is unknown')

    def insertInstrument(self,name,commit=0):
        '''Insert instrument into structure.'''
        logger.DLOG('In VolSurface.insertInstruments()')
        if self.type in ['Benchmark',
                         'Benchmark Spread',
                         'Benchmark Call/Put',
                         'Benchmark Spread Call/Put']:
            #self.__addBenchmark(name)
            self.__insertBenchmark(name)

    def removeInstrument(self,name,commit=0):
        '''Removes an instrument from a yield curve.'''
        logger.DLOG('In VolSurface.removeInstruments()')
        if not name:
            logger.ELOG('Must supply instrument name for removal')
            raise ValueError('Must supply instrument name for removal')
        # remove according to surface type
        if self.type in ['Benchmark',
                         'Benchmark Spread',
                         'Benchmark Call/Put',
                         'Benchmark Spread Call/Put']:
            self.__removeBenchmark(name)
        else:
            logger.ELOG('Vol structure type is unknown')
            raise TypeError('Vol structure type is unknown')

    def __insertBenchmark(self,name):
        '''Private method to insert a new benchmark instrument
           into vol structure.'''
        ins = ael.Instrument[name]
        vp = ael.VolPoint.new(self.struct)
        vp.insaddr = ins
        self.instruments.append(ins)

    def __removeBenchmark(self,name):
        '''Private method to remove benchmarks instruments
           from benchmark surfaces. Called from
           YCurve.removeInstrument().'''
        ins = ael.Instrument[name]
        for pt in self.struct.points():
           if pt.insaddr.insaddr  == ins.insaddr:
                pt.delete()
                self.instruments.remove(ins)
                break

class VolSurfaceRules(absRules):
    def __init__(self):
        self.nameStandard = 'ruleVS'
        self.rules = []
        self.ruleNames = []

        self.globalParams = globalParams
        if type(self.globalParams['VSRules']) == type(()):
            for rule in self.globalParams['VSRules']:
                self.ruleNames.append(rule)
        else:
            self.ruleNames = self.globalParams['VSRules'].split(',')
        self.nameStandard = 'ruleVS'
        self.rules = []
        if self.globalParams.get('VolatilitySurface'):
            self.ruleNames.append(self.globalParams.get('Task_ruleName'))
        self.structureNames = []
        self.structures = {}
        self.getRules()
        self.getStructures()
        self.checkRules()

    def getStructures(self):
        '''Retrieves volatility surfaces associated with the rules.'''
        logger.DLOG('In VolSurfaceRules.getStructures()')
        if self.rules:
            for rule in self.rules:
                tempVSName = self.ruleToStructName(rule.Name())
                vsTemp = VolSurface(tempVSName)
                if vsTemp.struct:
                    self.structures[tempVSName] = vsTemp
                else:
                    self.ruleNames.remove(rule.Name())
                    self.rules.remove(rule)
                self.structureNames = self.structures.keys()

    def calculate_implied_volatilities(self):
        """Caluclates the implied volatility points for volatility surfaces"""
        logger.DLOG('In VolSurfaceRules.calculate_implied_volatilities')
        if self.structureNames:
            ael.poll()
            for struct in self.structureNames:
                try:
                    vol_s = acm.FVolatilityStructure[struct]
                    if vol_s:
                        new_vol_s = vol_s.Clone()
                        new_vol_s.CalcImpliedVolatilities()
                        vol_s.Apply(new_vol_s)
                        vol_s.Commit()
                except Exception:
                    logger.ELOG('Cannot calculate volatility points for %s'%struct)

    def getRules(self):
        """ Get rules stroed in database"""
        logger.DLOG("in volsurfacesRules.getRules()")
        if default_rules in self.ruleNames:
            self.ruleNames = []
            absRules.getRules(self)
        else:
            if self.ruleNames and filter(None, self.ruleNames):
                for rules in self.ruleNames:
                    query = acm.FStoredASQLQuery[rules.strip()]
                    if query:
                        self.rules.append(query)
                    else:
                        logger.ELOG('Rule %s not found in database'%rules)

class YCurve(absStructure):

    benchmarkTypes = ['Benchmark', 'Price', 'Spread']
    insSpreadTypes = ['Instrument Spread',
                      'Instrument Spread Bid/Ask']
    attributeSpreadType = ['Attribute Spread']

    def __init__(self,name):
        self.instruments = []
        self.attributes = []
        self.struct = None
        self.yc_oid = None
        if not name:
            logger.ELOG('Must supply yield curve name')
            raise ValueError('Must supply yield curve name')

        if type(name) != type(1):
            yc_nbr = 0
            yc_nbr = self.getOid(name)
            if yc_nbr:
                self.yc_oid = str(yc_nbr)

        if self.yc_oid:
            struct = ael.YieldCurve.read("seqnbr=%s" %self.yc_oid )
            if not struct :
                struct = ael.YieldCurve[name]
        else:
            struct = ael.YieldCurve[name]

        if not struct:
            logger.ELOG('Yield curve %s does not exist' % name)
        else:
            try:
                self.struct = struct.clone()
            except Exception:
                logger.ELOG('Cannot clone YieldCurve %s' % name)
            if self.struct:
                self.name = self.struct.yield_curve_name
                self.type = self.struct.yield_curve_type
                self.getInstruments()

    def getInstruments(self):
        '''Retrieves all instruments currently in the yield curve.'''
        logger.DLOG('In YCurve.getInstruments()')
        structNames = []
        if self.type in YCurve.benchmarkTypes:
            for b in self.struct.benchmarks():
                self.instruments.append(b.instrument)
                structNames.append(b.instrument.insid)
        elif self.type in YCurve.insSpreadTypes:
            for ins in self.struct.instrument_spreads():
                self.instruments.append(ins.instrument)
                structNames.append(ins.instrument.insid)
        elif self.type in YCurve.attributeSpreadType:
            for repo_und_attrib in self.struct.attributes():
                #db_ins = acm.FInstrument.Select01("oid=%s"%ins, 'not found')
                self.instruments.append(repo_und_attrib.insaddr)
                structNames.append(repo_und_attrib.insaddr.insid)

        # Here additional cases may be entered
        else:
            logger.ELOG('YC type <%s> is unknown' % self.type)
            raise TypeError('YC type <%s> is unknown' % self.type)
        if structNames:
            logStr = \
            listToTableString("Instruments present in <%s>" \
                              % self.name, structNames)
            logger.DLOG(logStr)

    def insertInstrument(self,name,commit=0):
        '''Inserts an instrument into the yield curve'''
        logger.DLOG('In YCurve.insertInstruments()')
        if not name:
            raise ValueError('Must supply instrument name for insertion')
        # insert according to type
        if self.type in YCurve.benchmarkTypes:
            self.__insertBenchmark(name)
        elif self.type in YCurve.insSpreadTypes:
            self.__insertInstrumentSpread(name)
        elif self.type in YCurve.attributeSpreadType:
            self.__insertAttributeSpread(name)
        else: return # unknown/unsupported curve type

    def removeInstrument(self,name,commit=0):
        '''Removes an instrument from a yield curve.'''
        logger.DLOG('In YCurve.removeInstruments()')
        if not name:
            raise ValueError('Must supply instrument name for removal')
        # remove according to curve type
        if self.type in YCurve.benchmarkTypes:
            self.__removeBenchmark(name)
        elif self.type in YCurve.insSpreadTypes:
            self.__removeInstrumentSpread(name)
        elif self.type in YCurve.attributeSpreadType:
            self.__removeAttributeSpread(name)
        else: return # unknown/unsupported curve type

    def __insertBenchmark(self,name):
        '''Private method to insert benchmarks instruments
           into benchmark yield curves. Called from
           YCurve.insertInstrument().'''
        ins = ael.Instrument[name]
        bc = ael.Benchmark.new(self.struct)
        bc.instrument = ins
        self.instruments.append(ins)

    def __insertInstrumentSpread(self,name):
        '''Private method to insert instrument spreads
           into instrument spread curves. Called from
           YCurve.insertInstrument().

           The script uses a standard set of parameters
           for instrument spread insertion. These are:
               instrument = <instrument from rule>
               price_type = <as choosen in GUI>
               spread = 1000 (to assure that the spread will be handled later)
               spread_type = <as choosen in GUI>
               underlying_yield_curve_seqnbr = <same as ins spread curve>

           Spreads should be updated by automatic or
           manual calibration.
        '''
        ins = ael.Instrument[name]
        if not ins:
            logger.ELOG('Could not find instrument %s' % name)
            raise RuntimeError('Could not find instrument %s' % name)
        isc = ael.InstrumentSpread.new(self.struct)
        if not isc:
            logger.ELOG('Could not create new instrument spread')
            raise RuntimeError('Could not create new instrument spread')
        isc.instrument = ins
        isc.price_type = globalParams['spreadPriceType']
        isc.spread = 0.00111111 # absurd dummy value, to be calibrated
        isc.spread_type = globalParams['spreadType']
        if globalParams.get('askSpreadType', None):
            isc.spread_type_ask = globalParams['askSpreadType']
        else:
            isc.spread_type_ask = globalParams['spreadType']
        isc.underlying_yield_curve_seqnbr = \
            self.struct.underlying_yield_curve_seqnbr
        self.instruments.append(ins)

        try:
            self.struct.commit()
        except Exception:
            logger.ELOG('cannot commit structure %s'%self.struct.name)

        if globalParams.get('calibrationEnabled') or globalParams.get('calibrationEnabledAll'):
            ael.poll()
            if globalParams['calibrationPriceType'] == "Market":
                calPriceType = 1
            else:
                calPriceType = 0
            self.calibrateSpread(isc,calPriceType)
            self.calibrate_all_instrument()

    def __insertAttributeSpread(self, name):
        ins = ael.Instrument[name]
        bc = ael.YCAttribute.new(self.struct)
        bc.insaddr = ins
        bc.curr = ins.curr
        bc.underlying_yield_curve_seqnbr = self.struct.underlying_yield_curve_seqnbr
        self.instruments.append(ins)

    def calibrate_all_instrument(self):
        if globalParams.get('calibrationEnabledAll'):
            ael.poll()
            if globalParams['calibrationPriceType'] == "Market":
                calPriceType = 1
            else:
                calPriceType = 0

            for ins in self.struct.instrument_spreads():
                self.calibrateSpread(ins,calPriceType)


    def __removeBenchmark(self,name):
        '''Private method to remove benchmarks instruments
           from benchmark yield curves. Called from
           YCurve.removeInstrument().'''
        ins = ael.Instrument[name]
        for b in self.struct.benchmarks():
            if b.instrument == ins:
                b.delete()
                self.instruments.remove(ins)
                break

    def __removeInstrumentSpread(self,name):
        '''Private method to remove instrument spread instruments
           from instrument spread curves. Called from
           YCurve.removeInstrument().'''
        ins = ael.Instrument[name]
        for isp in self.struct.instrument_spreads():
            if isp.instrument == ins:
                isp.delete()
                self.instruments.remove(ins)
                break

    def __removeAttributeSpread(self,name):
        '''Private method to remove attribute spread instruments
           from instrument spread curves. Called from
           YCurve.removeInstrument().'''
        ins = ael.Instrument[name]
        for repo_und_attrib in self.struct.attributes():
            if repo_und_attrib.insaddr == ins:
                repo_und_attrib.delete()
                self.instruments.remove(ins)
                break

    def generateDays(self):
        """
        Updates the date table for the curve.
        """
        logger.DLOG('In YCurve.generateDays()')

        if self.struct.yield_curve_type not in YCurve.benchmarkTypes:
            return

        # Retrieve point in yield curve
        oldDates = self.__getOldDates()

        #first delete all the old points
        for point in oldDates.values():
            point.delete()

        #now create the new ones
        instrumentDates = []
        for ins in self.instruments:
            newDatePeriod = '0d'
            newAbsDate = 'None'

            #Special treatment for none Future/Forwards
            if ins.instype != 'Future/Forward':
                dateTuple = self.__calcDateGeneral(ins)
            else:
                dateTuple = self.__calcDateFuture(ins)
            if not dateTuple:
                continue
            newAbsDate, newDatePeriod = dateTuple

            if not (newAbsDate, newDatePeriod) in instrumentDates:
                instrumentDates.append((newAbsDate, newDatePeriod))

        for date in instrumentDates:
            newPoint = ael.YieldCurvePoint.new(self.struct)
            newPoint.date = date[0]
            newPoint.date_period = date[1]

    def __periodToDays(self,datePeriod):
        """
        Convert a period to number of days.
        """
        today = ael.date_today()
        endDate = today.add_period(datePeriod)
        nbrDays = today.days_between(endDate)
        return int(nbrDays)

    def __periodToDate(self,datePeriod):
        """
        Convert a period to an absolute date.
        """
        today = ael.date_today()
        endDate = today.add_period(datePeriod)
        return endDate

    def __getOldDates(self):
        """
        Retrieve a dictionary containing the old
        yield curve dates.
        Key is a tuple with an absolute date and
        the date period. Value is the acual point.
        """
        points = self.struct.points()

        oldDates = {}
        for point in points:
            date = point.date
            datePeriod = point.date_period

            if date == "None":
                date = self.__periodToDate(datePeriod)

            oldDates[(str(date),datePeriod)] = point

        return oldDates

    def __calcDateFuture(self,ins):
        """
        Calculate a yield curve date for a future/forward.
        """

        underlier = ins.und_insaddr
        #the dates are in the legs - assuming only one leg
        legs = underlier.legs()

        # if no leg on underlier, no date generation
        if not legs:
            return

        leg = legs[0]
        cal = leg.pay_calnbr

        legPeriod = leg.end_period
        insExpDate = ins.exp_day

        newAbsDate = insExpDate. \
                     add_period(legPeriod). \
                     add_days(underlier.spot_banking_days_offset). \
                     adjust_to_banking_day(cal,'Mod. Following')
        newDatePeriod = '0d'

        return newAbsDate, newDatePeriod

    def __calcDateGeneral(self,ins):
        """
        Calculate a yield curve date
        """

        insSpotOffset = ins.spot_banking_days_offset
        legs = ins.legs()

        # if no leg on instrument, no date generation
        if not legs:
            return

        leg = legs[0]
        cal = leg.pay_calnbr

        legEndDay = leg.end_day
        legEndDaySpot = legEndDay.add_days(insSpotOffset)

        # special treatment on generic ins
        if ins.generic:
            if leg.end_period.endswith('d'):
                nbrDays = getattr(leg, 'end_period.count')
                totalPeriod = legEndDay. \
                              days_between(legEndDaySpot) + \
                              nbrDays
                strTotalPeriod = str(totalPeriod)
                strTotalPeriodUnit = strTotalPeriod + 'd'
                newDatePeriod = strTotalPeriodUnit
            else:
                newDatePeriod = leg.end_period
            newAbsDate = self.__periodToDate(newDatePeriod)

        else:
            unadjDate = legEndDay.add_days(insSpotOffset)
            newAbsDate = unadjDate. \
                         adjust_to_banking_day(cal,'Mod. Following')
            newDatePeriod = '0d'

        return newAbsDate, newDatePeriod



    def calibrateSpread(self,insSpread,priceType = 1):
        '''Calibrates instrument spreads to market values.
            priceType = 0: theoretical price
            priceType = 1: market price
        '''
        logger.DLOG('In YCurve.calibrateSpread()')
        calSpread = insSpread.instrument.get_spread(priceType)
        insSpread.spread = calSpread
        if self.type == 'Instrument Spread':
            logger.ELOG('Cannot calibrate instrument spread_ask for (%s)'\
                         % self.name)

        elif self.type == 'Instrument Spread Bid/Ask':
            insSpread.spread_ask = calSpread - 0.0001

        return calSpread

    def calculateCurve(self):
        '''
        Calculates the curve.
        '''
        logger.DLOG('In YCurve.calculateCurve()')
        if self.type not in YCurve.benchmarkTypes:
            return
        try:
            self.struct.calculate()
        except:
            logger.ELOG('Calculation failed for struct %s' % self.name)


    def generate_points(self):
        '''
        Generates benchmark points for curve
        '''
        logger.DLOG('In YCurve.generate_benchmark_points()')
        ael.poll()
        yc = None

        if self.type not in YCurve.benchmarkTypes:
            return
        try:
            yc = acm.FYieldCurve[self.struct.yield_curve_name.strip()]
        except Exception:
            logger.DLOG("Cannot found FYield curve %s" %(self.struct.yield_curve_name))
        if yc:
            try:
                yc.GenerateAndLinkPointsFromBenchmarks()
                yc.Commit()
            except Exception as e:
                logger.DLOG("Cannot generate benchmark points: %s" %(str(e)))
        if globalParams['calculationEnabled']:
            if yc:
                try:
                    yc.Calculate()
                    yc.Commit()
                except Exception:
                    try:
                        self.struct.calculate()
                    except Exception:
                        logger.ELOG('Calculation failed for struct %s' % self.name)

            else:
                try:
                    self.struct.calculate()
                except Exception:
                    logger.ELOG('Calculation failed for struct %s' % self.name)



class YCRules(absRules):
    def __init__(self):
	global acm_version
        self.ruleNames = []
        self.globalParams = globalParams
        if type(self.globalParams['YCRules']) == type(()):
            for rule in self.globalParams['YCRules']:
                self.ruleNames.append(rule)
        else:
            self.ruleNames = self.globalParams['YCRules'].split(',')
        self.nameStandard = 'ruleYC'
        self.rules = []
        if self.globalParams.get('YieldCurve'):
            self.ruleNames.append(self.globalParams.get('Task_ruleName'))
        self.structureNames = []
        self.structures = {}
        self.getRules()
        self.getStructures()
        self.checkRules()

        for struct in self.structures.values():
                struct.calibrate_all_instrument()

        if float(acm_version) < 2011.2:
	    for struct in self.structures.values():
                struct.generateDays()
                if globalParams['calculationEnabled']:
                    struct.calculateCurve()

    def getStructures(self):
        '''Retrieves yield curves associated with the rules.'''
        logger.DLOG('In YCRules.getStructures()')
        if self.rules:
            for rule in self.rules:
                tempYCName = self.ruleToStructName(rule.Name())
                #tempYCName = rule.Name().replace(self.nameStandard+'-','')
                ycTemp = YCurve(tempYCName)
                if ycTemp.struct:
                    self.structures[tempYCName] = ycTemp
                else:
                    self.ruleNames.remove(rule.Name())
                    self.rules.remove(rule)
            self.structureNames = self.structures.keys()
        else:
            logger.LOG('No rules found...')

    def getRules(self):
        """ Get rules stroed in database"""
        logger.DLOG("in InsRules.getRules()")
        if default_rules in self.ruleNames:
            self.ruleNames = []
            absRules.getRules(self)
        else:
            if self.ruleNames and filter(None, self.ruleNames):
                for rules in self.ruleNames:
                    query = acm.FStoredASQLQuery[rules.strip()]
                    if query:
                        self.rules.append(query)
                    else:
                        logger.ELOG('Rule %s not found in database'%rules)

    def generate_benchmark_points(self):
        '''
        Generates benchmark points for curve
        '''
        logger.DLOG('In YCurve.generate_benchmark_points()')
        for struct in self.structures.values():
            struct.generate_points()


class Instrument(absStructure):
    def __init__(self, name):
        self.name = name
        self.instruments = []
        self.getInstruments()
        self.insNames = self.getInstrumentNames()


    def getInstruments(self):
        """ get instruments from a stored sql query"""
        ins = acm.FStoredASQLQuery[self.name].Query().Select()
        for i in ins:
            self.instruments.append(i)



class InsRules(absRules):
    def __init__(self):

        self.globalParams = globalParams

        if type(self.globalParams['InsRules']) == type(()):
            self.ruleNames = self.globalParams['InsRules']
        else:
            self.ruleNames = self.globalParams['InsRules'].split(',')

        self.instrumentNames = []
        if self.globalParams.get('InsName'):
            self.instrumentNames.append(self.globalParams['InsName'])
            taskName = self.globalParams.get('Task_taskName')
            ruleName = self.globalParams.get('Task_ruleName')
            insName_task = self.globalParams.get('InsName')
            logStr = "Processing Task <%s> with Rule <%s> for Instrument <%s>" \
                                      % (taskName, ruleName, insName_task)
            logger.LOG(logStr)

        self.rules = []
        self.ins_fields = {}
        self.instruments = []
        self.getRules()
        self.RuleIns()
        self.user_def_fields = get_parameters()
        self.get_fields_to_map()
        self.acm_ins_attributes = getAllFInstrumentAttributes()
        self.MapInstruments(self.instrumentNames)

    def getRules(self):
        """ Get rules stroed in database"""
        logger.DLOG("in InsRules.getRules()")
        if self.ruleNames and filter(None, self.ruleNames):
            for rules in self.ruleNames:
                query = acm.FStoredASQLQuery[rules.strip()]
                if query:
                    self.rules.append(query)
                else:
                    logger.ELOG('Rule %s not found in database'%rules)

    def RuleIns(self):
        # If to process all instruments from rule
        instrNames = None
        if self.rules:
            for rule in self.rules:
                #logger.LOG("Processing rule <%s>"%rule.Name())
                tempruleName = Instrument(rule.Name())
                if tempruleName.insNames:
                    instrNames = tempruleName.insNames
                    for ins in tempruleName.insNames:
                        if ins not in self.instrumentNames:
                            self.instrumentNames.append(ins)
                    for ins in tempruleName.instruments:
                        if ins not in self.instruments:
                            self.instruments.append(ins)
                if instrNames:
                    logStr = "Processing rule <%s> for instruments <%s>" \
                                      % (rule.Name(), instrNames)
                    logger.LOG(logStr)
        # If to process a single instrument not rule
        else:
            for names in self.instrumentNames:
                instrument = acm.FInstrument.Select01('name="%s"'%names, '')
                if instrument:
                    self.instruments.append(instrument)

    def get_fields_to_map(self):
        """ Get fields/values as selected in GUI"""
        logger.DLOG("in InsRules.get_fields_to_map()")
        ins_fields = []
        field_values = []
        for i in range(1,6):
            field = 'InsField' + str(i)
            value = 'FieldValue' + str(i)
            ins_fields.append(self.globalParams[field])
            field_values.append(self.globalParams[value])
        field_val_dic = dict(list(zip(ins_fields, field_values)))
        self.ins_fields = field_val_dic

    def MapInstruments(self, ins_list):
        """ Maps selected fields/values in GUI to
        Instruments in selected rules

        """

        logger.DLOG("in InsRules.MapInstruments()")
        # For all instruments in rule
        new_ins = None
        for ins in ins_list:
            acm_ins = acm.FInstrument.Select01('name="%s"'%ins, '')
            if acm_ins:
                try:
                    new_ins = acm_ins.Clone()
                except Exception:
                    logger.ELOG('Cannot clone Instrument %s'%acm_ins.Name())
                if new_ins:
                    for fields in self.ins_fields:
                        # fields selected in GUI matches with fields defined in FParameters
                        if fields in self.user_def_fields.keys():
                            acm_field = self.user_def_fields[fields]
                            if str(acm_field).upper() in self.acm_ins_attributes.keys():
                                field_typ = self.acm_ins_attributes[str(acm_field).upper()][0]
                                # get existing value for field in database
                                txt = 'new_ins.%s()'%(acm_field)
                                try:
                                    old_val = eval(txt)
                                except Exception as e:
                                    old_val = None
                                    logger.ELOG("Field <%s> may not exists for instrument" %(acm_field))
                                try:
                                    old_val_name = old_val.Name()
                                except Exception as e:
                                    old_val_name = str(old_val)
                                if old_val_name == 'True':
                                    old_val_name = 'Yes'
                                elif old_val_name == 'False':
                                    old_val_name = 'No'

                                mapping_entitiy, new_name = self.get_mapping_value(field_typ, \
                                                        fields, self.ins_fields[fields], old_val_name)

                            if mapping_entitiy:
                                logger.LOG("Updating field <%s> from <%s> to <%s> for instrument <%s>"\
                                                %(acm_field, old_val_name, new_name, acm_ins.Name()))
                                try:
                                    txt = "new_ins.%s= '%s'"%(acm_field, mapping_entitiy)
                                    exec(txt)
                                    acm_ins.Apply(new_ins)
                                except Exception as e:
                                    logger.ELOG(e)

    def get_mapping_value(self, field_typ, field, new_field_val, old_field_val):
        if 'FChoiceList' in field_typ:
            choice_list = acm.FChoiceList.Select("name=%s" % new_field_val)
            for ch in choice_list:
                if ch.List() == field:
                    mapping_entitiy = ch
                    if mapping_entitiy.Name() == old_field_val:
                        return None, None
                    else:
                        name = mapping_entitiy.Name()
                        return (mapping_entitiy.Oid(), name.strip())
        else:
            if str(new_field_val).strip() == str(old_field_val).strip():
                return None, None
            else:
                return (str(new_field_val).strip(), str(new_field_val).strip())



#===============================================================================
# Explicit rules
#===============================================================================
'''
Here additional logic for rules may be inserted. The architecture is as
follows:

Autolink extracts a list of intrument names from the FASQL query. This list is
passed into a function in this section. Here instrument names may be added or
removed from the list. The function then returns the instrument list back
to the main program.

The mapping between a rule and a function takes place in a dictionary
with the name 'explicitRuleMappingTable'. The keys in the dictionary
are strings containing the name of the rule. The values connected with
the keys are the connected function objects.

The function must be on a special form:
    - must take a list of instruments as the only argument
    - must return a list of instruments upon successful completion

The regular expression module is preimported if more advanced string
filtering is needed.

Keeping the explicit rule modifiers in a separate module is a good idea.
Then the corresponding function objects will have to be referenced by
the namespace they are residing in.

Example:
    def ExplicitRuleLogicFunction1(instrumentNameList):
        """Explicit rule logic for rule ruleYC-autolinkTestCurve."""
        <perform logic here>
        return instrumentNameList

    explicitRuleMappingTable = {
        "ruleYC-autolinkTestCurve":ExplicitRuleLogicFunction1
        }
'''

# mapping table for rules
# entries should be on the form: <rule name>:function object
explicitRuleMappingTable = {}

#===============================================================================
#Helper functions
#===============================================================================

def LogSetup():
    '''
        Set up the logging environment. If logging not enabled,
        just return the logger with no handlers. This will trigger
        a warning message but do not affect the functionality
        of the script.

    '''
    global logger


    # if not enabled, do not create handlers
    try:
        if not globalParams['loggingEnabled']:
            return
    except:
        logger.exception("Parameter validation error - aborting")
        return

    level = 1
    # set the log level
    if globalParams['loggingLevel'] == 'INFO':
        level = 1
    if globalParams['loggingLevel'] == 'DEBUG':
        level = 2
    if globalParams['loggingLevel'] == 'WARN':
        level = 3
    if globalParams['loggingLevel'] == 'ERROR':
        level = 4

    logger.Reinitialize(level = level)



def isACMExpired(ins):
    """
    Check whether an instrument is expired in the
    Trading Manager sense.
    Input: instrument name <str> or
           instrument <acm.FInstrument subclassed object>
    """
    if isinstance(ins,basestring):
        insName = ins
        ins = acm.FInstrument.Select01('name="%s"'%insName, '')
        if not ins:
            raise RuntimeError("No instrument <%s> found" % insName)
    if not hasattr(ins, 'IsKindOf') or not ins.IsKindOf(acm.FInstrument):
        raise TypeError("Supplied instrument is not an ACM entity")
    if ins.IsExpired():
        return True
    else:
        return False

def listToTableString(header,cmpList):
    """
    Makes a pretty logging of a list of strings (like ins names).
    if list is list of sequence types, each component is tabulated.
    """
    logString = header + "\n" + "-"*80 + "\n"
    for cmp in cmpList:
        logString = logString + " "*5
        if isinstance(cmp,(tuple,list)):
            for i in cmp:
                logString = logString + "%-20s" % str(i)
        else:
            logString = logString + str(cmp)
        logString = logString + "\n"
    logString = logString + "-"*80 + "\n"
    return logString

def setAddInfo(object,specName,value):
    """
    Sets an additional info on a cloned object.
    If addinfo already exist, it is updated. Otherwise
    it is created.
    Returns FALSE if any error occurs. Otherwise TRUE.
    """
    if not type(object) == ael.ael_entity and not object.original():
        eMsg = "Object must be a cloned ael entity"
        raise ValueError(eMsg)
    try:
        found = False
        addInfoSpec = ael.AdditionalInfoSpec[str(specName)]
        for addInfo in object.additional_infos():
            if addInfo.addinf_specnbr == addInfoSpec:
                found = True
                break
        if found:
            addInfo.value          = value
        else:
            addInfo                = ael.AdditionalInfo.new(object)
            addInfo.addinf_specnbr = addInfoSpec
            addInfo.value          = value
    except Exception:
        logger.ELOG("Failed to set addInfo <%s> on object" % str(value))
        return False
    return True

def getAddInfo(object,name):
    """
    Gets an additional info from the object. Returns
    the value as a string if present.
    Otherwise return FALSE.
    """
    name = str(name)
    try:
        addInfo = object.add_info(name)
    except:
        logger.ELOG("Could not read addinfo <%s> from object" % name)
        return False
    return addInfo

def getChoiceList():
    """Gets MASTER ChoiceLists from database"""
    choice_list = []
    choicelist = acm.FChoiceList.Select("list=MASTER")
    for i in choicelist:
        choice_list.append(i.Name())
    return choice_list

def allEnumValuesExcludeNone(enum):
    enumValues = acm.FEnumeration['enum(%s)' % enum]
    if enumValues:
        return [e for e in enumValues.Values() if (e != 'None')]
    else:
        return None

def getAllFInstrumentAttributes():
    attributes = {}
    attr = acm.FInstrument.Attributes()
    for atr in attr:
        attributes.setdefault(str(atr.Name()).upper(), []).append(str(atr))
        attributes.setdefault(str(atr.Name()).upper(), []).append(type(atr))
    return attributes



#===============================================================================
# Global variables
#===============================================================================

# logger object
logger = FLogger.FLogger('FAutolink')

# parameter dictionary
globalParams = {}

#===============================================================================
# Run program from here
#===============================================================================

#------------------------------------------------------------------------------
# AEL Variables callback functions
#------------------------------------------------------------------------------

def DisableYCHook(index, fieldValues):
    if fieldValues[index] == '0':
        for i in range(index+1,index+10):
            ael_variables[i][9] = 0
        ael_variables[index+1][5] = 0
        fieldValues[index+1] = default_rules

    if fieldValues[index] == '1':
        for i in range(index+1,index+10):
            ael_variables[i][9] = 1
        ael_variables[index+1][5] = 1
        if fieldValues[index+1] == default_rules:
            fieldValues[index+1] = ''
        ael_variables[index+1][3] = getYCDbRules()
    return fieldValues

def DisableVolHook(index, fieldValues):
    if fieldValues[index] == '0':
        ael_variables[index+1][9] = 0
        ael_variables[index+1][5] = 0
        fieldValues[index+1] = default_rules

    if fieldValues[index] == '1':
        ael_variables[index+1][9] = 1
        ael_variables[index+1][5] = 1
        if fieldValues[index+1] == default_rules:
            fieldValues[index+1] = ''
        ael_variables[index+1][3] = getVSDbRules()
    return fieldValues

def DisablePageHook(index, fieldValues):
    if fieldValues[index] == '0':
        ael_variables[index+1][9] = 0
        ael_variables[index+1][5] = 0
        fieldValues[index+1] = default_rules

    if fieldValues[index] == '1':
        ael_variables[index+1][9] = 1
        ael_variables[index+1][5] = 1
        if fieldValues[index+1] == default_rules:
            fieldValues[index+1] = ''
        ael_variables[index+1][3] = getPGDbRules()
    return fieldValues

def DisableLoggingHook(index, fieldValues):
    if fieldValues[index] == '0':
        for i in range(index+1,index+3):
            ael_variables[i][9] = 0
    if fieldValues[index] == '1':
        for i in range(index+1,index+3):
            ael_variables[i][9] = 1

    return fieldValues

def getDbRules():
    rules = []
    ael.poll()
    tmpRules = None

    textObjects = ael.TextObject.select('type=%s' %FASQL_Query)
    if textObjects:
        tmpRules = textObjects.members()

    if tmpRules == []:
        logger.LOG('Found no rules')
    for rule in tmpRules:
        insert_query = acm.FStoredASQLQuery[rule.name]
        if insert_query:
            rules.append(rule.name)
    return rules

def getYCDbRules():
    '''Extracts all query rules from the database.'''
    rule_name = 'ruleYC'
    yc_rules = []
    logger.DLOG('In getYCDbRules()')
    ael.poll()
    tmpRules = None

    textObjects = ael.TextObject.select('type=%s' %FASQL_Query)
    if textObjects:
        tmpRules = textObjects.members()

    if tmpRules == []:
        logger.LOG('Found no rules')
    for rule in tmpRules:
        insert_query = acm.FStoredASQLQuery[rule.name]
        if insert_query:
            #yc_rules.append(insert_query)
            yc_rules.append(rule.name)
    return yc_rules

def getVSDbRules():
    '''Extracts all query rules from the database.'''
    rule_name = 'ruleVS'
    vs_rules = []
    logger.DLOG('In getVSDbRules()')
    ael.poll()

    tmpRules = None
    textObjects = ael.TextObject.select('type=%s' %FASQL_Query)
    if textObjects:
        tmpRules = textObjects.members()

    if tmpRules == []:
        logger.LOG('Found no rules')
    for rule in tmpRules:
        insert_query = acm.FStoredASQLQuery[rule.name]
        if insert_query:
            #yc_rules.append(insert_query)
            vs_rules.append(rule.name)
    return vs_rules

def getPGDbRules():
    '''Extracts all query rules from the database.'''
    rule_name = 'rulePG'
    pg_rules = []
    logger.DLOG('In getPageDbRules()')
    ael.poll()
    tmpRules = None

    textObjects = ael.TextObject.select('type=%s' %FASQL_Query)
    if textObjects:
        tmpRules = textObjects.members()

    if tmpRules == []:
        logger.LOG('Found no rules')
    for rule in tmpRules:
        insert_query = acm.FStoredASQLQuery[rule.name]
        if insert_query:
            pg_rules.append(rule.name)
    return pg_rules

def getInsFields():
    adm_fields_to_popup = [' ']
    user_fields = get_parameters()
    if user_fields:
        for fields in user_fields:
            adm_fields_to_popup.append(fields)
    adm_fields_to_popup.sort()
    return adm_fields_to_popup

def get_parameters():
    """ Get instrument fields as specified in FParameters by user"""
    data = None
    user_fields = {}
    context = acm.GetDefaultContext()
    params = context.GetExtension('FParameters', 'FObject', 'FAutolinkInstrumentFields').Value()
    data = params.At('instrument_fields_to_map')
    if data:
        user_fields = eval(str(data))
    return user_fields


def DisableINSHook(index, fieldValues):
    global gui_fields_flag
    if fieldValues[index] == '0':
        for i in range(index+1,index+13):
            ael_variables[i][9] = 0
        for i in range(index+1, index+4):
            ael_variables[i][5] = 0

        fieldValues[index+1] = default_rules
        fieldValues[index+2] = 'Select a Field'
        fieldValues[index+3] = 'Provide Field Value'


    if fieldValues[index] == '1':
        for i in range(index+1,index+13):
            ael_variables[i][9] = 1
        for i in range(index+1, index+4):
            ael_variables[i][5] = 1

        if fieldValues[index+1] == default_rules:
            fieldValues[index+1] = ''
            fieldValues[index+2] = ''
            fieldValues[index+3] = ''

    if fieldValues[index+2] != '':
        gui_fields_flag = 0
    else:
        gui_fields_flag = 1
    return fieldValues


def disable_calibrate_all(index, fieldValues):
    if fieldValues[index] == '1':
        fieldValues[index-1] = 0
    return fieldValues

def disable_calibrate_new(index, fieldValues):
    if fieldValues[index] == '1':
        fieldValues[index+1] = 0
    return fieldValues

def getFieldValue(index, fieldValues):
    global gui_fields_flag
    if gui_fields_flag == 1:
        fieldValues[index+1] = ' '
        values = []
        inst_attrbs = getAllFInstrumentAttributes()
        acm_field = None
        persistent_cls = acm.FPersistentAttribute.Select('')
        relation_cls = acm.FPersistentRelation.Select('')
        data_types = ['char', 'int', 'double']
        user_fields = get_parameters()
        if fieldValues[index].strip() != '':
            gui_field = fieldValues[index]
            nice_name = gui_field
            if gui_field in user_fields.keys():
                acm_field = user_fields[gui_field]

        if acm_field:
            if str(acm_field).upper() in inst_attrbs.keys():
                attr_type = inst_attrbs[str(acm_field).upper()][1]
                if attr_type == type(persistent_cls[0]):
                    persis_class = inst_attrbs[acm_field.upper()][0]
                    if 'enum' in persis_class:
                        nice_name = persis_class[persis_class.find("(")+1:persis_class.find(")")]
                        values = allEnumValuesExcludeNone(nice_name)
                        if values:
                            fieldValues[index+1] = values[0]
                        else:
                            fieldValues[index+1] = 'No Values found in database'
                    elif 'bool' in persis_class:
                        values = ['Yes ', 'No ']
                        fieldValues[index+1] = values[0]
                    else:
                        for i in data_types:
                            if i in persis_class:
                                ael_variables[index+1][3] = None
                                fieldValues[index+1] = 'Enter some %s value'%i

                elif attr_type == type(relation_cls[0]):
                    relation_class = inst_attrbs[acm_field.upper()][0]
                    if 'FChoiceList' in relation_class:
                        choice_list = acm.FChoiceList.Select("list=%s"%nice_name)
                        if choice_list:
                            for choice in choice_list:
                                values.append(choice)
                            fieldValues[index+1] = values[0]
                        else:
                            fieldValues[index+1] = 'No values found in database'
                    else:
                        acm_class = str(relation_class).split()[0]
                        fstr = "acm.%s.Select('')"%acm_class
                        try:
                            fclass = eval(fstr)
                        except Exception as e:
                            logger.ELOG(e)
                        vals = fclass
                        for i in vals:
                            values.append(i)
                        if values:
                            fieldValues[index+1] = values[0]
                        else:
                            fieldValues[index+1] = 'No values found in database'
            else:
                logger.LOG('No Instrument Attribute <%s> found in database' %(acm_field))
                fieldValues[index+1] = ''
        values.sort()
        ael_variables[index+1][3] = values

    return fieldValues

def enable_task(index, fieldValues):
    global gui_fields_flag
    gui_fields_flag = 1

gui_fields_flag = 0




#------------------------------------------------------------------------------
# Additional information for AEL Variables
#------------------------------------------------------------------------------

# tooltip for excludeACMExired toggle button
expiredToolTip = \
"""Exclude all instruments that are expired in the Trading Manager sense.
That is, the ACM method IsExpired() returns TRUE for the instrument.
Not always aligned with ADM expiry (which is used by the insert items-folder)
"""
expiredToolTip = expiredToolTip.replace("\n"," ")

ins_enable_tooltip = \
"""
Enable if need to perform Instrument fields mapping
"""

ins_rules_tooltip = \
"""
Select rules from database to perform required mapping on instruments
from rule.
"""

ins_rules_tooltip = ins_rules_tooltip.replace("\n"," ")

yc_rules_tooltip = \
"""
Select rules from database to perform required mapping on Yield Curves
from rule.
"""

vol_rules_tooltip = \
"""
Select rules from database to perform required mapping on
Volatility Surfaces from rule.
"""

page_rules_tooltip = \
"""
Select rules from database to perform required mapping on
Page from rule.
"""

yc_rules_tooltip = yc_rules_tooltip.replace("\n"," ")

ins_field_tooltip = \
"""
Select a Instrument field to Map.
"""

field_val_tooltip = \
"""
Enter / Select required field value to Map for instruments
"""
run_task_tooltip = \
"""
Enable if want to run the saved task continuosly. ATS will run the saved task
continuously when any Instrument creation / Instrument updates are found in database.
"""
run_task_tooltip = run_task_tooltip.replace("\n"," ")

yc_calibrate_new_tooltip = \
"""
Select this field to calibrate spread curves for new instruments
"""

yc_calibrate_all_tooltip = \
"""
Select this field to calibrate spread curves for all instruments
"""



#------------------------------------------------------------------------------
# AEL Variables
#------------------------------------------------------------------------------

ael_variables = [
                 # Instrument tab
                 # enable mapping of Instrument fields
                 ['InsEnabled','Instrument Fields Mapping Enabled_Instrument','int',
                  [1,0],0, 0, 0, ins_enable_tooltip, DisableINSHook, 1],

                 # Execut Rules
                 ['InsRules', 'Execute rules_Instrument', 'string', \
                  getDbRules(), default_rules, 1, 1, ins_rules_tooltip, None, None],

                 # Instrument Field map 1
                 ['InsField1','Instrument field 1_Instrument','string',\
                  getInsFields(),'Select a Field', 1, 0, ins_field_tooltip,getFieldValue, 1],
                 # Field 1 value
                 ['FieldValue1','       Field value 1_Instrument','string',\
                  [],'Provide Field Value', 1, 0, field_val_tooltip, None, 1],

                 # Instrument Field map 2
                 ['InsField2','Instrument field 2_Instrument','string',\
                  getInsFields(),'', 0, 0, None, getFieldValue, 1],
                 # Field 2 value
                 ['FieldValue2','       Field value 2_Instrument','string',\
                  [],'', 0, 0, None, None, 1],

                 # Instrument Field map 3
                 ['InsField3','Instrument field 3_Instrument','string',\
                  getInsFields(),'', 0, 0, None, getFieldValue, 1],
                 # Field 3 value
                 ['FieldValue3','       Field value 3_Instrument','string',\
                  [],'', 0, 0, None, None, 1],

                 # Instrument Field map 4
                 ['InsField4','Instrument field 4_Instrument','string',\
                  getInsFields(),'', 0, 0,\
                   None, getFieldValue, 1],
                 # Field 4 value
                 ['FieldValue4','       Field value 4_Instrument','string',\
                  [],'', 0, 0,\
                   None, None, 1],

                 # Instrument Field map 5
                 ['InsField5','Instrument field 5_Instrument','string',\
                  getInsFields(),'', 0, 0,\
                   None, getFieldValue, 1],
                 # Field 5 value
                 ['FieldValue5','       Field value 5_Instrument','string',\
                  [],'', 0, 0,\
                   None, None, 1],

                 # Checkbox Run ATS Contonuously
                 ['continuous_task','Run Task Continuously_Instrument','int',\
                 [1,0],0, 0, 0, run_task_tooltip, enable_task, 1],

                 # Yield curve tab
                 # enable mapping of yield curves
                 ['ycEnabled','Curve Mapping Enabled_Yield Curves','int',
                  [1,0],0, 0, 0, None, DisableYCHook, 1],

                  # Execut Rules
                 ['YCRules', 'Execute rules_Yield Curves', 'string', \
                  getYCDbRules(), default_rules, 0, 1, yc_rules_tooltip, None, None],

                 # should ACM expired instruments be exluded?
                 ['excludeACMExired',\
                  'Exclude ACM expired instruments_Yield Curves','int',\
                  [1,0],0, 0, 0, expiredToolTip,None, None],
                 # should the yield curve be recalculated
                 ['calculationEnabled','Calculate Benchmark Curves_Yield Curves',\
                  'int', [1,0], 0, 0, 0, None, None, None],
                 # calibrate spread curves for new instruments?
                 ['calibrationEnabled',\
                  'Calibrate new Instrument Spreads_Yield Curves','int',\
                  [1,0],0, 0, 0, yc_calibrate_new_tooltip, disable_calibrate_new, 1],
                 # calibrate spread curves for all instruments?
                 ['calibrationEnabledAll',\
                  'Calibrate All Instrument Spreads_Yield Curves','int',\
                  [1,0],0, 0, 0, yc_calibrate_all_tooltip, disable_calibrate_all, 1],
                 # price type for calibrations
                 ['calibrationPriceType',\
                  'Calibration Price Type_Yield Curves','string',\
                  ['Market','Theoretical'],'Market', 0, 0, None, None, None],
                 # price type field for new spreads
                 ['spreadPriceType',\
                  'Instrument Spread Price Type_Yield Curves','string',\
                  ['None','MtM','Market','Theoretical'],'Market', 0, 0,\
                   None, None, None],
                 # type of spread
                 ['spreadType','Instrument Spread Type_Yield Curves','string',\
                  ['None','Yield','Price','Gross Basis','YTM','Asset Swap',\
                   'Disc Margin','Spread Bid','Price Bid','OAS'],\
                  'Yield', 0, 0, None, None, None],
                  # type of ask spread
                 ['askSpreadType','Instrument Ask Spread Type_Yield Curves','string',\
                  ['None','Yield','Price','Gross Basis','YTM','Asset Swap',\
                   'Disc Margin','Spread Bid','Price Bid','OAS'],\
                  'Yield', 0, 0, None, None, None],
                  # Checkbox Run ATS Contonuously
                 ['continuous_task_yc','Run Task Continuously_Yield Curves','int',\
                 [1,0],0, 0, 0, run_task_tooltip, None, None],

                 # Volaility Surface tab
                 # enable volatility autolinking
                 ['volEnabled',\
                  'Volatility Surface Mapping Enabled_Volatility Surfaces',\
                  'int',[1,0],0, 0, 0, None, DisableVolHook, 1],
                 ['VSRules', 'Execute rules_Volatility Surfaces', 'string', \
                  getVSDbRules(), default_rules, 0, 1, vol_rules_tooltip, None, None],

                  # Checkbox Run ATS Contonuously
                 ['continuous_task_vol','Run Task Continuously_Volatility Surfaces','int',\
                 [1,0],0, 0, 0, run_task_tooltip, enable_task, 1],

                 # Page tab
                 # enable autolinking of pages
                 ['pageEnabled','Instrument Page Mapping Enabled_Pages',\
                  'int',[1,0],0, 0, 0, None, DisablePageHook, 1],

                 # enable volatility autolinking
                 ['PGRules', 'Execute rules_Pages', 'string', \
                  getPGDbRules(), default_rules, 0, 1, page_rules_tooltip, None, None],

                  # Checkbox Run task page Contonuously
                 ['continuous_task_page','Run Task Continuously_Pages','int',\
                 [1,0],0, 0, 0, run_task_tooltip, enable_task, 1],

                 # Administration tab
                 # enable logging
                 ['loggingEnabled','Enable Logging_Administration',\
                  'int',[1,0],0, 0, 0, None, DisableLoggingHook, None],
                 ['loggingPath','Log file_Administration','string',\
                  None,'c:/TEMP/autolink.log', 0, 0, None, None, None],
                 ['loggingLevel','Log level_Administration','string',\
                  ['INFO','DEBUG','WARN','ERROR'], 'INFO', 0, 0, None, None, None]
                 ]

#===============================================================================
# Main program
#===============================================================================

def ael_main(dict):
    ycEnabled = dict['ycEnabled']
    volEnabled = dict['volEnabled']
    pageEnabled = dict['pageEnabled']
    InsMapEnabled = dict['InsEnabled']

    log_levl_dict = {'INFO' : 1, 'DEBUG' : 2, 'WARN' : 3, 'ERROR' : 4}
    if dict.get('loggingEnabled', None):
        loggingPath = dict['loggingPath']
        directory = os.path.expandvars(loggingPath)
        log_level = log_levl_dict.get(dict['loggingLevel'], 1)
        logger.Reinitialize(level = log_level, logToFileAtSpecifiedPath = directory)

    global globalParams
    globalParams = dict
    global acm_version
    acm_version = acm.Version().split(',')[0][:6]

    # Set up logging
    #LogSetup()
    logger.DLOG('Logger set up')
    # yield curve mapping
    if ycEnabled:
        logger.DLOG('Starting yield curve mapping procedure')
        yr = YCRules()
        yr.commitStructures()
        if float(acm_version) >= 2011.2:
            yr.generate_benchmark_points()

    # volatility surface mapping
    if volEnabled:
        logger.DLOG('Starting volatility surface mapping procedure')
        volr = VolSurfaceRules()
        volr.commitStructures()
        volr.calculate_implied_volatilities()

    # page mapping
    if pageEnabled:
        logger.DLOG('Starting page mapping procedure')
        pager = PageRules()
        pager.commitStructures()

    # Instrument Fields Mapping
    if InsMapEnabled:
        logger.DLOG('Starting Instrument Fields mapping procedure')
        instr = InsRules()
        instr.commitInstruments()
