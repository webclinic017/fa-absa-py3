""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FApplyLimitTemplates.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FApplyLimitTemplates

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FRunScriptGUI
import FLimitTemplate
from FLimitActions import StartLimitWorkbench, CheckLimits
from FSelectLimitTemplatesDialog import SelectLimitTemplatesDialog

logger  = FAssetManagementUtils.logger
logDict = FAssetManagementUtils.logDict

limitNamingDict = {
    'None': 1,
    'Template Name': 2,
    'Spec Name / Template Name': 3,
    'Portfolio Name / Template Name' : 4,
    'Portfolio Name / Spec Name / Template Name': 5,
    'Spec Name / Portfolio Name / Template Name': 6
    }

LIMIT_NAME_LENGTH = 63


class ApplyLimitTemplateVariables(FRunScriptGUI.AelVariablesHandler):

    def AelVariables(self):
        variables = []
        variables.append(self.QueryfolderVariable())
        variables.append(self.PortfolioVariable())
        variables.append(self.LimitSpecificationVariable())
        variables.append(self.LimitNamesVariable())
        variables.append(self.OverrideAction())
        variables.append(self.LimitTemplatesVariable())
        variables.append(self.LogModeVariable())
        variables.append(self.CheckLimitsVariable())
        variables.append(self.ShowLimitsVariable())
        return variables

    @classmethod
    def IncludeTemplateInList(cls, _ext):
        return True

    @staticmethod
    def insertStoredFolder():
        q = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'AND')
        op = q.AddOpNode('OR')
        op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
        op = q.AddOpNode('AND')
        op.AddAttrNode('SubType', 'RE_LIKE_NOCASE', 'FTrade')
        return q

    def QueryfolderVariable(self):
        queryFolders = ApplyLimitTemplateVariables.insertStoredFolder()
        sQueryfolder = 'Query folder(s) to apply limits to. If selected, the run script asserts that no portfolio is chosen.'
        return ['QUERYFOLDER', 'Query Folder(s):', 'FStoredASQLQuery', None, queryFolders, 0, 1, sQueryfolder]
        
    def PortfolioVariable(self):
        sPortfolio = 'Portfolio(s) to apply limits to. If selected, the run script asserts that no query folder is chosen.'
        return ['PORTFOLIO',  'Portfolio(s):',    'FPhysicalPortfolio', None, None, 0, 1, sPortfolio]
    
    def LimitSpecificationVariable(self):
        sLimitSpecification = 'Choose a limit specification to apply the limit template to. If none is selected, the specification from the template will be used'
        return ['LIMIT_SPECIFICATION',  'Limit Specification:',  'FLimitSpecification', None, None, 0, 0, sLimitSpecification, None, 1]

    def GetSelectTemplatesDialog(self, *args):
        shell = args[0]
        selected = args[1].At('selected')
        builder = SelectLimitTemplatesDialog.CreateLayout()
        dialog = SelectLimitTemplatesDialog(selected)
        return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog )

    def LimitTemplatesVariable(self):
        sLimits = 'Choose the limit templates which are to be applied'
        return ['LIMIT_TEMPLATES', 'Limit Templates:', 'string', [], None, 0, 1, sLimits, None, 1, self.GetSelectTemplatesDialog]
        
    def LimitNamesVariable(self):
        sLimitNaming = 'Choose how to name created limits'
        return ['LIMIT_NAMING', 'Limit Names as:', 'string', limitNamingDict.keys(), 'None', 1, 0, sLimitNaming, None, 1]

    def OverrideAction(self):
        sOverrideAction = 'Try to override existing limits with the suggested names. Found limits are then inactivated.'
        return ['OVERRIDE_ACTION', 'Override:', 'bool', [0, 1], 0, 1, 0, sOverrideAction, None, 1]                           

    def LogModeVariable(self):
        sLog = 'Logmode 0 shows WARNING and ERROR messages. Logmode 1 shows INFORMATION messages, and also includes the messages from Logmode 0.\
                Logmode 2 shows DEBUG messages and includes all other message types. '
        return ['LOG_MODE', 'Logmode_Logging', 'string', sorted(logDict), '1. Normal', 2, 0, sLog]
    
    def CheckLimitsVariable(self):
        sCheckLimits = "If selected, the limits are checked upon creation"
        return ['CHECK_LIMITS', 'Check Limits', 'bool', [0, 1], 0, 1, 0, sCheckLimits, None, 1]
        
    def ShowLimitsVariable(self):
        sShowLimits = "If selected, a limit sheet is opened showing the created limits"
        return ['SHOW_LIMITS', 'Show Limits', 'bool', [0, 1], 0, 1, 0, sShowLimits, None, 1]    
        
    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, self.AelVariables())

ael_variables = ApplyLimitTemplateVariables()

def ael_main(params):
    logger.Reinitialize(level=logDict[ params['LOG_MODE'] ],
                        keep=None,
                        logOnce=None,
                        logToConsole=1,
                        logToPrime=None,
                        logToFileAtSpecifiedPath=None,
                        filters=None,
                        lock=None
                    )
                    
    limitNaming = limitNamingDict[ params['LIMIT_NAMING'] ]
    logger.info('--Limit Application Started--')
    portfolios = acm.FArray()
    if params['PORTFOLIO']:
        portfolios.AddAll(params['PORTFOLIO'])
    if params['QUERYFOLDER']:
        portfolios.AddAll(params['QUERYFOLDER'])
    if portfolios.IsEmpty():
        raise ApplyLimitTemplateError('No portfolios selected')
    templates = GetTemplatesFromTemplateNames(params['LIMIT_TEMPLATES'])
    if not templates:
        logger.info('No templates were found. Aborting.')
    else:
        logger.info('Found %d limit template(s).' % len(templates))
    if templates:
        limitSpec = params['LIMIT_SPECIFICATION']
        override = params['OVERRIDE_ACTION']
        factory = LimitCreator(portfolios, limitSpec, templates, limitNaming, override)
        factory.CreateLimits()
        AfterApplicationActions(factory, params)
    logger.info('--Limit Application Finished--\n')

def GetTemplatesFromTemplateNames(templateNames):
    return [FLimitTemplate.FLimitTemplate.CreateFromExtension(templateName) for templateName in templateNames]

def AfterApplicationActions(factory, params):
    result = factory.Results()
    LogConclusionMessage(result)
    limits = [ limitSpec.Limit() for limitSpec in result.AllLimits() ]
    if params['CHECK_LIMITS']:
        if len(limits) == 0:
            logger.WLOG('No limits were created: limits will not be checked')
        else:
            CheckLimits(limits)
    if params['SHOW_LIMITS']:
        if len(limits) == 0:
            logger.WLOG('No limits were created: limit sheet will not be opened')
        else:
            StartLimitWorkbench(limits)
            
def LogConclusionMessage(result):
    if len(result.FoundLimits()) != 0:
        logger.LOG(' - Found existing limits:')
    for foundLimitSpec in result.FoundLimits():
        logger.LOG(' --- %s'%str(foundLimitSpec))
    if len(result.DeactivatedLimits()) != 0:
        logger.LOG(' - Deactivated limits:')
    for deactivatedLimitSpec in result.DeactivatedLimits():
        logger.LOG(' --- %s'%str(deactivatedLimitSpec))
    if len(result.CreatedLimits()) != 0:
        logger.LOG(' - Created the following limits:')
    for createdLimitSpec in result.CreatedLimits():
        logger.LOG(' --- %s'%str(createdLimitSpec))
    if len(result.FailedLimits()) != 0:
        logger.LOG(' - Failed to create the following limits:')
    for failedLimitSpec in result.FailedLimits():
        logger.LOG(' --- %s'%str(failedLimitSpec))

class ApplyLimitTemplateError(Exception):
    pass

class LimitCreator(object):

    def __init__(self, portfolios, limitSpecification, templates, limitNaming, override):
        self.portfolios = portfolios
        self.limitSpec = limitSpecification
        self.templates = templates
        self.limitNaming = limitNaming
        self.override = override
        self.createdLimits = []
        self.foundLimits = []
        self.failedLimits = []
        self.deactivatedLimits = []

    def GetLimitStateChart(self):
        return acm.FStateChart['Limits']

    def LimitSpecification(self):
        return self.limitSpec

    def Results(self):
        return ApplyLimitsResults(self.createdLimits, 
                                  self.foundLimits,
                                  self.failedLimits,
                                  self.deactivatedLimits
                                  )
                                  
    def _DeactivateBusinessProcess(self, businessProcess, comment):
        businessProcessImage = businessProcess.StorageImage()
        businessProcessImage.ForceToState('Inactive', comment)
        businessProcessImage.Commit()
        
    def _DeactivateLimit(self, limit, deactivatedBy):
        limitImage = limit.StorageImage()
        limitImage.Name = "Replaced by %s" % str(deactivatedBy.Oid())
        limitImage.Commit()
        self._DeactivateBusinessProcess(limit.BusinessProcess(), "Limit %s replaced by limit %s" % (limit.Oid(), deactivatedBy.Oid()))
        self.deactivatedLimits.append( LimitDeactivationSpecification(limit, deactivatedBy) )
        for childLimit in limit.Children():
            self._DeactivateBusinessProcess(childLimit.BusinessProcess(), "Parent Limit %s replaced by limit %s" % (limit.Oid(), deactivatedBy.Oid()))            
            
    def _CreateLimitFromTemplate(self, template, portfolio, name):
        limit = template.Apply(portfolio, self.LimitSpecification())
        limit.Name = name
        limit.Commit()
        self.createdLimits.append( CreatedLimitSpecification(limit) )
        return limit
        
    def _RemoveLimitName(self, limit):
        limitImage = limit.StorageImage()
        limitImage.Name = None
        limitImage.Commit()
        
    def CreateLimits(self):
        for template in self.templates:
            for portfolio in self.portfolios:
                try:
                    limitName = self.LimitNameFromTemplate(template, portfolio)
                    if limitName:
                        existingLimit = acm.FLimit[limitName]
                        if existingLimit:
                            if self.override:
                                try:
                                    self._RemoveLimitName(existingLimit)
                                    limit = self._CreateLimitFromTemplate(template, portfolio, limitName)
                                    self._DeactivateLimit(existingLimit, limit)
                                except Exception as e:
                                    raise ApplyLimitTemplateError('Failed to override limit %s. Reason: %s.' % (limitName, str(e)))
                            else:
                                self.foundLimits.append( FoundLimitSpecification(existingLimit) )
                            continue
                    limit = self._CreateLimitFromTemplate(template, portfolio, limitName)
                    logger.DLOG('Successfully created limit %s from template %s' % (limit.Name(), template.Name()))
                except Exception as e:
                    self.failedLimits.append( FailedLimitApplicationSpecification(template, e) )

    def LimitSpecificationName(self, template):
        if self.LimitSpecification():
            return self.LimitSpecification().Name()
        else:
            return template.LimitSpecificationName()

    def StrippedLimitName(self, name):
        if name and len(name) > LIMIT_NAME_LENGTH:
            logger.WLOG('The suggested limit name was above 63 characters. Name will be stripped')
            return name[0:LIMIT_NAME_LENGTH-1]
        return name
        
    def LimitNameFromTemplate(self, template, portfolio):
        suggestedName = None
        if self.limitNaming == 1:
            pass
        elif self.limitNaming == 2:
            suggestedName = template.Name()
        elif self.limitNaming == 3:
            suggestedName = '/'.join([self.LimitSpecificationName(template), 
                             str(template.Name())])
        elif self.limitNaming == 4:
            suggestedName = '/'.join([portfolio.Name(), 
                             str(template.Name())])
        elif self.limitNaming == 5:
            suggestedName = '/'.join([portfolio.Name(),
                             self.LimitSpecificationName(template), 
                             str(template.Name())])
        elif self.limitNaming == 6:
            suggestedName = '/'.join([self.LimitSpecificationName(template), 
                             portfolio.Name(), 
                             str(template.Name())])
        else:
            raise ApplyLimitTemplateError('Could not recognize the picked limit naming convention')
        return self.StrippedLimitName(suggestedName)

class ApplyLimitsResults(object):

    def __init__(self, createdLimits, foundLimits, failedLimits, deactivatedLimits):
        self.createdLimits = createdLimits
        self.foundLimits = foundLimits
        self.failedLimits = failedLimits
        self.deactivatedLimits = deactivatedLimits
    
    def CreatedLimits(self):
        return self.createdLimits
        
    def FoundLimits(self):
        return self.foundLimits
    
    def AllLimits(self):
        return self.CreatedLimits() + self.FoundLimits()

    def FailedLimits(self):
        return self.failedLimits
        
    def DeactivatedLimits(self):
        return self.deactivatedLimits

        
class FailedLimitApplicationSpecification(object):

    def __init__(self, template, error):
        self.template = template
        self.error = error
        
    def TemplateName(self):
        return self.template.Name()
        
    def Message(self):
        return str(self.error)
    
    def Details(self):
        return "Limit Template: %s. Reason: %s" % (self.TemplateName(), self.Message())
    
    def __str__(self):
        return self.Details()

class LimitActionSpecification(object):

    def __init__(self, limit):
        self.oid = limit.Oid()
        self.name = limit.Name()
        self.spec = limit.LimitSpecification()
        self.path = limit.LimitTarget().Path()
        self.type = self.GetType(limit)
        self.limit = limit
    
    def Limit(self):
        return self.limit
    
    @staticmethod
    def GetType(limit):
        if limit.IsParent():
            return 'Parent Limit'
        elif limit.Parent():
            return 'Child Limit'
        return 'Limit'
        
    def Details(self):
        return '%s %s, "%s" with path "%s" in specification "%s"' % (self.type, self.oid, self.name, self.path, self.spec.Name())

    def __str__(self):
        return self.Details()

class FoundLimitSpecification(LimitActionSpecification):
    pass

class CreatedLimitSpecification(LimitActionSpecification):
    pass
        
class LimitDeactivationSpecification(LimitActionSpecification):

    def __init__(self, limit, newLimit):
        LimitActionSpecification.__init__(self, limit)
        self.newLimit = newLimit
        
    def __str__(self):
        return self.Details() + '. Replaced by limit %s with name "%s"' % (str(self.newLimit.Oid()), self.newLimit.Name())