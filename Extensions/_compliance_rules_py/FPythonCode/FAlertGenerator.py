""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FAlertGenerator.py"
"""--------------------------------------------------------------------------
MODULE
    FAlertGenerator

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
        
-----------------------------------------------------------------------------"""
import acm
from FComplianceRulesUtils import RuleInterface, GetAlert, logger


def Create(rule, params=None):
    interface = RuleInterface(rule.ComplianceRule())
    if hasattr(interface, 'CreateAlertGenerator'):
        return interface().CreateAlertGenerator(params)
    return DefaultGenerator(params)
    
    
    
class GeneratorParams(object):

    def __init__(self, params=None):
        self._params = params

    def CreateWhenCompliant(self):
        try:
            return self._params.CreateWhenCompliant()
        except AttributeError:
            return False
        
    def CreateWhenMissing(self):
        try:
            return self._params.CreateWhenMissing()
        except AttributeError:
            return False
        
    def CreateWhenError(self):
        try:
            return self._params.CreateWhenError()
        except AttributeError:
            return True
        
    def RecedeWhenNotFound(self):
        try:
            return self._params.RecedeWhenNotFound()
        except AttributeError:
            return True
            
    def SaveAlerts(self):
        try:
            return self._params.SaveAlerts()
        except AttributeError:
            return False
        
        
class Interface(object):

    def ToSubject(self, entity):
        raise NotImplementedError
        
    def AlertsFromCheck(self, check):
        raise NotImplementedError
        
    def AlertFromResult(self, result):
        raise NotImplementedError
    
    
class Generator(Interface):

    STATES = {
        'Missing': 'Receded',    
        'Compliant': 'Receded',
        'Breached': 'Active',
        'Error': 'Error'
        }
    
    def __init__(self, params=None):
        self._params = GeneratorParams(params)
    
    def AlertsFromCheck(self, check):
        collection = AlertCollection()
        for result in check.Results():
            alert = self._GetOrCreateAlert(result)
            collection.Add(alert)
        if self._params.RecedeWhenNotFound():
            self._RecedeNotFound(collection, check)
        alerts = collection.Alerts()
        if self._params.SaveAlerts():
            self.CommitAlerts(alerts)
            alerts = collection.Originators()
        return alerts
        
    def AlertFromResult(self, result):
        alert = self._GetOrCreateAlert(result)
        if alert and self._params.SaveAlerts():
            self.CommitAlerts([alert])
            alert = alert.Originator()
        return alert
        
    @classmethod
    def CommitAlerts(cls, alerts):
        cls._CommitSubjects(alerts)
        cls._CommitAlerts(alerts)

    @staticmethod
    def _CommitSubjects(alerts):
        try:
            acm.BeginTransaction()
            for alert in alerts:
                alert.Subject().Commit()
            acm.CommitTransaction()
        except RuntimeError as err:
            acm.AbortTransaction()
            logger.error('Failed to commit alerts subject(s): {0}'.format(err))
            raise err
            
    @staticmethod
    def _CommitAlerts(alerts):
        try:
            acm.BeginTransaction()
            for alert in alerts:
                subject = alert.Subject().Originator()
                alert.Subject(subject)
                alert.Commit()
            acm.CommitTransaction()
            
            for alert in alerts:
                logger.debug('Processed alert {0} for rule {1} with target {2}'.format(alert.Originator().Oid(),
                              alert.AppliedRule().ComplianceRule().Name(), alert.AppliedRule().Target().Name()))
        except RuntimeError as err:
            acm.AbortTransaction()
            logger.error('Failed to commit alert(s): {0}'.format(err))
            raise err
                    
    def _RecedeNotFound(self, alerts, check):
        for alert in check.AppliedRule().Alerts():
            if alert not in alerts.Originals():
                alerts.Add(self._RecedeAlert(alert))   
            
    def _ShouldCreateAlert(self, result):
        if result.State() == 'Compliant':
            return self._params.CreateWhenCompliant()
        if result.State() == 'Missing':
            return self._params.CreateWhenMissing()
        if result.State() == 'Error':
            return self._params.CreateWhenError()
        return True

    def _CreateAlert(self, result):
        alert = acm.FAlert()
        alert.RegisterInStorage()
        alert.AppliedRule(result.RuleCheck().AppliedRule())
        alert.Threshold(result.Threshold())
        alert.State(self.STATES[result.State()])
        alert.Information(result.CheckedValue().Info())
        subject = self.ToSubject(result.CheckedValue().Entity())
        alert.Subject(subject)
        return alert

    def _UpdateAlert(self, alert, result):
        image = alert.StorageImage()
        if image.State() != 'Inactive':
            if not image.State() == self.STATES[result.State()]:
                image.Acknowledged(False)
            image.State(self.STATES[result.State()])
            image.Information(result.CheckedValue().Info())
            return image
        
    def _GetAlert(self, result):
        rule = result.RuleCheck().AppliedRule()
        threshold = result.Threshold()
        subject = self.ToSubject(result.CheckedValue().Entity())
        return GetAlert(rule, threshold, subject)
        
    def _GetOrCreateAlert(self, result):
        alert = self._GetAlert(result)
        if alert is not None:
            alert = self._UpdateAlert(alert, result)   
        elif self._ShouldCreateAlert(result):
            alert = self._CreateAlert(result)
        return alert
        
    def _RecedeAlert(self, alert):
        image = alert.StorageImage()
        image.State('Receded')
        image.Information(None)
        return image
        

class DefaultGenerator(Generator):

    def ToSubject(self, entity):
        return entity


class AlertCollection(object):

    def __init__(self):
        self._alerts = []
        self._originals = set()
        
    def Add(self, alert):
        if alert:
            self._alerts.append(alert)
            if alert.Original():
                self._originals.add(alert.Original())
            
    def Alerts(self):
        return self._alerts
        
    def Originals(self):
        return self._originals
        
    def Originators(self):
        return [a.Originator() for a in self.Alerts()]
