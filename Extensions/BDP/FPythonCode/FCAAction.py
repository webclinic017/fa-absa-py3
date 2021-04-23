""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCAAction.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
import importlib
"""----------------------------------------------------------------------------
 MODULE
     FCAAction - Module which executes a Corporate Action.

 DESCRIPTION
     This module executes the Corporate Action.
 ---------------------------------------------------------------------------"""

import acm
import ael


import FCATypes
import FBDPGui
import FBDPCommon
import FBDPRollback
import time
import datetime
from FCorpActionStatesSetup import CorporateActionUsingBusinessProcess
from FCorpActionStatesSetup import GetStatus
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


def isSubclassOf(*args):
    def recursive(a, b):
        return a == b or a.Superclass() and recursive(a.Superclass(), b)
    a, b = [eval('acm.F' + klass.split('/')[0]) for klass in args]
    return recursive(a, b)

class FCAParameters(FBDPGui.Parameters):
    def __init__(self, dic, acmCA, rollback):
        self.__dict__ = dic.copy()
        self.rollback = rollback
        self.businessEvent = self.createBusinessEvent(acmCA)
        if float(self.NewQuantity) == 0.0 or float(self.OldQuantity) == 0.0:
            self.updateCaOnPayout(acmCA)

    def updateCaOnPayout(self, acmCA):
        choices = acmCA.CaChoices()
        if len(choices) != 1:
            return
        payout = choices[0].CaPayouts()
        if len(payout) != 1:
            return
        payoutRate = payout[0].PayoutRate()
        if payoutRate == 0:
            return
        self.OldQuantity = 1.0
        self.NewQuantity = payoutRate * self.OldQuantity
        newInst = payout[0].NewInstrument()
        if newInst:
            self.NewInstrument = newInst.Name()

    def derivativeType(self, insType):
        if insType == 'Repo':
            return getattr(FCATypes, 'Repo')(
                self.__dict__, self.businessEvent)
        elif insType == 'SecurityLoan':
            return getattr(FCATypes, 'SecurityLoan')(
                self.__dict__, self.businessEvent)
        elif insType == 'Total Return Swaps':
            return getattr(FCATypes, 'TotalReturnSwap')(
                self.__dict__, self.businessEvent)
        else:
            return getattr(FCATypes, 'Derivative')(
                self.__dict__, self.businessEvent)

    def runFCATypes(self):
        """ Create an instance of the class in FCATypes."""
        if self.tempName in ['Elective', 'ExerciseRights']:
            return FCATypes.CorpactExerciseAssign(self.__dict__,
                self.rollback, self.businessEvent)

        if self.tempName == 'ScripDividend':
            return FCATypes.CorpactScripDividend(self.__dict__,
                self.rollback, self.businessEvent)

        if self.tempName == 'DividendReinvestment':
            return FCATypes.CorpactDividendReinvestment(self.__dict__,
                self.rollback, self.businessEvent)

        self.attributesFromStrings()
        if isSubclassOf(self.InstrumentType, 'Derivative'):
            if hasattr(self, 'DerivativeTypes') and self.DerivativeTypes:
                for t in self.DerivativeTypes:
                    return self.derivativeType(t)
            elif hasattr(self, 'Derivatives') and self.Derivatives:
                for ins in self.Derivatives:
                    return self.derivativeType(ins.InsType())
            else:
                raise Exception("Either derivatives or"
                            "DerivativeTypes is required.")

        return FCATypes.CorpactType(self.__dict__, self.businessEvent)

    def createBusinessEvent(self, acmCA):
        bEvent = None
        if acmCA:
            bEvent = acmCA.BusinessEvent()
            if not bEvent:
                raise Exception("No business event associated with "
                      "the CorpAction %s." % (acmCA.Name()))

        if not bEvent:
            bEvent = acm.FBusinessEvent()
            self.rollback.add(bEvent)
            Summary().ok(bEvent, Summary().CREATE, bEvent.Oid())

        return bEvent

    def attributesFromStrings(self):
        self.StartDate = (FBDPCommon.toDateAEL(self.StartDate) or
                ael.date_from_time(0))
        self.Instr = ael.Instrument[self.Instrument]
        self.ExDate = FBDPCommon.toDateAEL(self.Exdate)
        self.SettleDate = FBDPCommon.toDateAEL(self.Settledate)
        if hasattr(self, 'Portfolio'):
            self.Portfolio = \
            [ael.Portfolio[portfolio.Oid()] for portfolio in self.Portfolio] \
            if len(self.Portfolio) > 0 else None
        else:
            self.Portfolio = None

        try:
            self.NewQuantity = float(self.NewQuantity)
        except ValueError:
            raise Exception("New Quantity missing or incorrectly specified. "
                    "Please correct and rerun.")
        try:
            self.OldQuantity = float(self.OldQuantity)
        except ValueError:
            raise Exception("Old Quantity missing or incorrectly specified. "
                    "Please correct and rerun.")
        self.ins = None
        if len(self.NewInstrument) > 0:
            self.ins = ael.Instrument[self.NewInstrument]
        self.NewPrice = (self.NewPrice and
                getattr(FCATypes.NewPrice, self.NewPrice))
        self.SpinoffCostFraction = (self.SpinoffCostFraction and
                float(self.SpinoffCostFraction) or 0)
        self.ClosingPrice = (self.ClosingPrice and
                getattr(FCATypes.ClosingPrice, self.ClosingPrice))
        self.InstrumentNameDecimals = (self.InstrumentNameDecimals and
                int(self.InstrumentNameDecimals))
        self.CashAmount = self.CashAmount and float(self.CashAmount) or 0

    def variablesFromCorpActToDic(self, ca):
        corpact = {}
        for vp in ca.ViewableProperties().split():
            corpact[vp] = ca.GetProperty(vp)

        corpact['Name'] = ca.Name()  # Not in ViewableProperties.
        corpact['ExDate'] = str(corpact['Exdate'])
        if corpact['ExDate'] == '':
            raise Exception('Corporate action %s has to have an ExDate.' %
                    corpact['Name'])
        if corpact['Instrument']:
            corpact['Instrument'] = corpact['Instrument'].Oid()
        else:
            raise Exception('Corporate action %s has to have an instrument.' %
                    corpact['Name'])
        corpact['CashCurrency'] = (corpact['CashCurrency'] and
                corpact['CashCurrency'].Name())
        corpact['NewInstrument'] = (corpact['NewInstrument'] and
                corpact['NewInstrument'].Oid())
        self.__dict__.update(corpact)

class CorporateAction(FBDPRollback.RollbackWrapper):

    def perform(self, templates, acmCA, manyCA, caAttr):
        try:
            caParameters = FCAParameters(self.ael_variables_dict, acmCA, self)
            preview = self.ael_variables_dict['Preview']
            if len(templates) > 1 or (manyCA and templates):
                for template in templates:
                    caParameters.getData('FTemplateBasis', template)
                    caParameters.tempName = template
                    if manyCA:
                        caParameters.variablesFromCorpActToDic(acmCA)
                    caParameters.runFCATypes()
            else:
                if templates:
                    caParameters.tempName = templates[0]
                else:
                    caParameters.tempName = ""
                if manyCA:
                    caParameters.variablesFromCorpActToDic(acmCA)
                caParameters.runFCATypes()
            status = 'Pending' if preview else 'Processed'
            self.changeStatus(acmCA, caAttr, status)
        except Exception as e:
            Logme()(e, "WARNING")
            try:
                self.changeStatus(acmCA, caAttr, "Inactive", False)
            except Exception:
                pass
        self.end()

    def changeStatus(self, ca, caAttrList, newStatus,
            rollback=True):
        #if CorporateActionUsingBusinessProcess():
        #    return
        if ca and not self.Testmode:
            ca.Status = newStatus
            if rollback:
                if not caAttrList.count("Status"):
                    caAttrList.append("Status")
                if self.add(ca, caAttrList):
                    FBDPCommon.Summary().ok(ca, FBDPCommon.Summary().UPDATE)
            else:
                eval(FBDPRollback.encapsulateAttribute(ca)).Apply(ca)
                ca.Commit()

    def isActive(self, ca):
        if ca:
            if CorporateActionUsingBusinessProcess():
                return GetStatus(ca) == 'Active'
            else:
                return ca.Status() == 'Active'

class PerformCorporateActions(object):

    def __init__(self):
        self.acmFCorpAct = None
        self.templates = None
        self.manyCorpActs = False
        self.dic = None
        self.CA_attr = []
        self.Name = 'User defined'

    def perform(self, dic):
        self.dic = dic
        corpAct = dic.get('Corpact', [])
        template = dic.get('Template', [])
        corpactions, CA_attributes = self.getCorpActList(corpAct, template)
        if corpAct and not corpactions:
            Logme()(None, 'START')
            Summary().setStartTime(time.time())
            errMsg = 'There were no active corporate actions specified.'\
                    '\n        Either make sure at least one of the ' \
                    'corporate actions are active,' \
                    '\n        or leave the Corpact field empty.'
            Logme()(errMsg, 'ERROR')
            Summary().log(dic)
            Logme()(None, 'FINISH')
            return

        oneCorpAct = False
        oneTemplate = False
        if corpactions:
            if corpAct and len(corpAct) == 1:
                oneCorpAct = True
            else:
                self.manyCorpActs = True
        elif not corpAct and template:
            oneTemplate = True

        if self.manyCorpActs:
            for acmFCorpAct in corpactions:
                try:
                    self.CA_attr = CA_attributes[corpactions.index(
                            acmFCorpAct)]
                except Exception:
                    pass
                self.acmFCorpAct = acmFCorpAct.Clone()
                self.templates = self.acmFCorpAct.Template().split(',')
                try:
                    self.createCorporateAction()
                except FCATypes.SkipCorpact:
                    continue
        else:
            if oneCorpAct:
                self.acmFCorpAct = corpactions[0].Clone()
                self.Name = corpAct and corpAct[0].Name()
            elif oneTemplate:
                self.Name = "Template"
            else:
                if 'Name' in self.dic:
                    self.Name = self.dic['Name']

            # check if exists and converts instrument, NewInstrument
            # and CashCurrency to string
            self.convertInsToName()
            self.templates = template
            # create and execute coporate action
            corpActPython = self.createCorporateAction()
            try:
                self.connectCorpActionAndRollbackSpec(self.acmFCorpAct,
                                                      corpActPython.spec)
            except Exception as e:
                print(str(e))

    def connectCorpActionAndRollbackSpec(self, fCorpAction, aelRollbackSpec):
        #this should become ACM but for now is AEL
        acmRollbackSpec = FBDPCommon.ael_to_acm(aelRollbackSpec)
        connectionObject = acm.FCustomTextObject()
        connectionObject.Name(self.formatName(fCorpAction))
        connectionObject.Text(acmRollbackSpec.Name())
        connectionObject.Commit()

    def formatName(self, acmRollbackSpec):
        retVal = 'corporate_action_oid = {0} {1}'.format(acmRollbackSpec.Oid(),
                                            str(datetime.datetime.utcnow()))
        return retVal

    def isActive(self, ca):
        if ca:
            if CorporateActionUsingBusinessProcess():
                return GetStatus(ca) == 'Active'
            else:
                return ca.Status() == 'Active'

    def isSupportedCorpAction(self, ca):
        choices = ca.CaChoices()
        if len(choices) == 0:
            return True

        if len(choices) > 1:
            Logme()('Corporate action {0} is not supported, as it has'
                    ' multiple choices, please try the advanced corporate'
                    ' action processing.'.format(ca.Name()), 'WARNING')
            return False

        choiceType = ca.CaChoiceType()
        if choiceType == 'Voluntary':
            Logme()('Corporate action {0} is not supported, as it has'
                    ' choice type {1}, please try the advanced corporate'
                    ' action processing.'.format(ca.Name(), choiceType), 'WARNING')
            return False

        payouts = choices[0].CaPayouts()
        if len(payouts) > 1:
            Logme()('Corporate action {0} is not supported, as its choice'
            ' has multiple payouts, please try the  advanced corporate action'
            ' processing.'.format(ca.Name(), choiceType), 'WARNING')
            return False

        return True

    def getProcessingCAs(self, caLists):
        if not caLists:
            return []

        not_active = [ca for ca in caLists if not self.isActive(ca)]
        if not_active:
            text = ("The following corporate actions are not active, and "
                    "therefore ignored:\n")
            for s in not_active:
                text = ''.join([text, s.Name(), ', '])
            Logme()(text.rstrip(', '), 'INFO')

        not_support = [ca for ca in caLists if not self.isSupportedCorpAction(ca)]
        if not_support:
            text = ("The following corporate actions are not supported, and "
                    "therefore ignored:\n")
            for s in not_support:
                text = ''.join([text, s.Name(), ', '])
            Logme()(text.rstrip(', '), 'INFO')

        return [ca for ca in caLists if ca not in not_active + not_support]

    def createCorporateAction(self):
        longName = 'CA ' + self.Name
        caRollback = CorporateAction(longName, self.dic['Testmode'], self.dic)
        FBDPCommon.execute_script(caRollback.perform, self.templates,
                self.acmFCorpAct, self.manyCorpActs, self.CA_attr)
        return caRollback

    def getCorpActList(self, corpAct, template):
        date = FBDPCommon.toDateAEL(self.dic['Date'])
        corpactions = []
        CA_attributes = None
        if corpAct:
            corpactions = self.getProcessingCAs(corpAct)
        elif not template and date:
            try:
                import FBDPHook
                importlib.reload(FBDPHook)
                hook = FBDPHook.get_corporate_actions
            except AttributeError:
                if date:
                    caList = [ca for ca in self.getProcessingCAs(acm.FCorporateAction.Instances()) if
                            ca.ExDate()]
                    corpactions = [(FBDPCommon.toDateAEL(ca.ExDate()),
                            ca.UpdateTime(), ca.Clone()) for ca in caList]
                    corpactions.sort()
                    corpactions = [c[2] for c in corpactions if c[0] <= date]
                    if not corpactions:
                        raise Exception('There are no corporate actions with '
                                'ExDate prior to the given Date.')
                else:
                    raise Exception('There was no Date specified.')
            else:
                Logme()('############# Running hook \'get_corporate_actions\' '
                        '#############', 'DEBUG')
                (corpactions, CA_attributes) = hook(self.dic)
                Logme()('#####################################################'
                        '###########', 'DEBUG')
        return (corpactions, CA_attributes)

    def convertInsToName(self):
        try:
            self.dic['Instrument'] = self.dic['Instrument'][0].Name()
        except IndexError:
            raise Exception("No instrument specified. Please correct and "
                    "rerun.")
        except TypeError:
            raise Exception("Instrument seems to be inactive. Try to press "
                    "enter in the Date field.")
        self.dic['NewInstrument'] = (self.dic['NewInstrument'] and
                self.dic['NewInstrument'][0].Name())
        self.dic['CashCurrency'] = (self.dic['CashCurrency'] and
                self.dic['CashCurrency'][0].Name())
