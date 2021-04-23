
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_PARAMETERS_COMPONENT
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module retreives and sets the component variables from the environment
                                variables in Extension Manager.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import traceback

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as ENVIRONMENT_PARAMETERS
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
import at_type_helpers as TYPE_UTILS

'''----------------------------------------------------------------------------------------------------------
Class containing all the properties for the Specific ATS that is starting up.
----------------------------------------------------------------------------------------------------------'''
class FC_PARAMETERS_COMPONENT(object):
    def __init__(self, componentName):
        self._componentName = componentName
        self._componentAMBHost = None
        self._componentAMBPort = None
        self._componentBatchSizeForCollectionATS = None
        self._componentCollectionRequestMessageSubject = None
        self._componentHandlerAMBSenderFlag = None
        self._componentHandlerDBSenderFlag = None
        self._componentReceiverName = None
        self._componentReceiverSource = None
        self._componentSubscriptionSubjects = []
        self._componentSenderHandlers = {}
        self._componentDedicatedEod = None
        self._componentControlMeasureFlag = False
        self._setComponentParameters()
        
    @property
    def componentAMBHost(self):
        return self._componentAMBHost
    
    @property
    def componentAMBPort(self):
        return self._componentAMBPort

    @property
    def componentBatchSizeForCollectionATS(self):
        return self._componentBatchSizeForCollectionATS
    
    @property
    def componentCollectionRequestMessageSubject(self):
        return self._componentCollectionRequestMessageSubject
        
    @property
    def componentControlMeasureFlag(self):
        return self._componentControlMeasureFlag        
    
    @property
    def componentHandlerAMBSenderFlag(self):
        return self._componentHandlerAMBSenderFlag 
    
    @property
    def componentHandlerDBSenderFlag(self):
        return self._componentHandlerDBSenderFlag
        
    @property
    def componentReceiverName(self):
        return self._componentReceiverName

    @property
    def componentReceiverSource(self):
        return self._componentReceiverSource

    @property
    def componentSubscriptionSubjects(self):
        return self._componentSubscriptionSubjects

    @property
    def componentSenderHandlers(self):
        return self._componentSenderHandlers

    @property
    def componentDedicatedEod(self):
        return self._componentDedicatedEod       
    
    def _setComponentParameters(self):
        componentSettingsXML = ENVIRONMENT_PARAMETERS.environment.getElementsByTagName(self._componentName)
        if not componentSettingsXML:
            raise ValueError('The component settings for component %s could not be retreived from the environment settings in module %s' %(self._componentName, __name__))
        
        try:
            self._componentAMBHost = str(componentSettingsXML[0].getElementsByTagName('AMBHost')[0].firstChild.data)
        except Exception as e:
            raise EXCEPTION('The component variable AMB Host for component %s could not be retreived in module %s. No connection to the AMB can be made.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)
        
        try:
            self._componentAMBPort = str(componentSettingsXML[0].getElementsByTagName('AMBPort')[0].firstChild.data)
        except Exception as e:
            raise EXCEPTION('The component variable AMB Port for component %s could not be retreived in module %s. No connection to the AMB can be made.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)
                            
        try:
            self._componentControlMeasureFlag = TYPE_UTILS.to_bool(str(componentSettingsXML[0].getElementsByTagName('ControlMeasureFlag')[0].firstChild.data))
        except:
            self._componentControlMeasureFlag = False
        
        try:
            self._componentHandlerAMBSenderFlag = TYPE_UTILS.to_bool(str(componentSettingsXML[0].getElementsByTagName('HandlerAMBSenderFlag')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The component variable Handler AMB Sender Flag for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)
        
        try:
            self._componentHandlerDBSenderFlag = TYPE_UTILS.to_bool(str(componentSettingsXML[0].getElementsByTagName('HandlerDBSenderFlag')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The component variable Handler DB Sender Flag for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)
        
        try:
            self._componentReceiverName = str(componentSettingsXML[0].getElementsByTagName('ReceiverName')[0].firstChild.data)
        except Exception as e:
            raise EXCEPTION('The component variable Receiver Name for component %s could not be retreived in module %s.' %(self._componentName, __name__),
                            traceback, 'CRITICAL', e)
        
        try:
            self._componentReceiverSource = str(componentSettingsXML[0].getElementsByTagName('ReceiverSource')[0].firstChild.data)
        except Exception as e:
            raise EXCEPTION('The component variable Receiver Source for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)
            
        try:
            self._componentBatchSizeForCollectionATS = int(str(componentSettingsXML[0].getElementsByTagName('BatchSizeForCollectionATS')[0].firstChild.data))
        except:
            self._componentBatchSizeForCollectionATS = 0
            
        try:
            self._componentCollectionRequestMessageSubject = str(componentSettingsXML[0].getElementsByTagName('CollectionRequestMessageSubject')[0].firstChild.data)
        except Exception as e:
            raise EXCEPTION('The component variable Receiver Source for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)

        try:
            self._componentDedicatedEod = TYPE_UTILS.to_bool(str(componentSettingsXML[0].getElementsByTagName('DedicatedEOD')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The DedicatedEod for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)  
        
        try:
            subscriptionSubjects = componentSettingsXML[0].getElementsByTagName('SubscriptionSubjects')[0].getElementsByTagName('Subject')
        except Exception as e:
            raise EXCEPTION('The Subscription Subject for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                            traceback, 'CRITICAL', e)
            
        for subscriptionSubject in subscriptionSubjects:
            self._componentSubscriptionSubjects.append(str(subscriptionSubject.firstChild.data))
            
        #Retreive Sender Handlers
        ambSenderHandlersXML = componentSettingsXML[0].getElementsByTagName('AMBSenderHandlers')
        if ambSenderHandlersXML:
            ambSenderHandlers = ambSenderHandlersXML[0].getElementsByTagName('Handler')
            if not ambSenderHandlers:
                raise ValueError('No Sender Handlers for component %s could be retreived in module %s.' %(self._componentName, __name__))
                
            for ambSenderHandler in ambSenderHandlers:
                try:
                    handlerSenderName = str(ambSenderHandler.getElementsByTagName('SenderName')[0].firstChild.data)
                except Exception as e:
                    raise EXCEPTION('The Sender Handler Sender Name for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                    traceback, 'CRITICAL', e)
                
                try:
                    handlerSenderSource = str(ambSenderHandler.getElementsByTagName('SenderSource')[0].firstChild.data)
                except Exception as e:
                    raise EXCEPTION('The Sender Handler Sender Source for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                    traceback, 'CRITICAL', e)
                
                try:
                    multiSubjectEnable = TYPE_UTILS.to_bool(str(ambSenderHandler.getElementsByTagName('MultiSubjectEnable')[0].firstChild.data))
                except Exception as e:
                    raise EXCEPTION('The Sender Handler Multi Subject Enable for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                    traceback, 'CRITICAL', e)
                
                try:
                    numberOfSubjectAllocation = int(str(ambSenderHandler.getElementsByTagName('NumberOfSubjectAllocation')[0].firstChild.data))
                except Exception as e:
                    raise EXCEPTION('The Sender Handler Number Of Subject Allocation for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                    traceback, 'CRITICAL', e)
                
                try:
                    startingPoint = int(str(ambSenderHandler.getElementsByTagName('StartingPoint')[0].firstChild.data))
                except Exception as e:
                    raise EXCEPTION('The Sender Handler Starting Point for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                    traceback, 'CRITICAL', e)
                
                try:
                    handlerSenderSubjects = ambSenderHandler.getElementsByTagName('SenderSubjects')[0].getElementsByTagName('SenderSubject')
                except Exception as e:
                    raise EXCEPTION('The Sender Handler Sender Subjects for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                    traceback, 'CRITICAL', e)
                                                                                        
                for handlerSenderSubject in handlerSenderSubjects:
                    handlerSenderSubjectValue = str(handlerSenderSubject.firstChild.data)
                    if not handlerSenderSubjectValue:
                        raise ValueError('The Sender Helder Sender Subject Value for component %s could not be retreived in module %s.' %(self._componentName, __name__))
                        
                    self._componentSenderHandlers[handlerSenderSubjectValue] = (handlerSenderName, handlerSenderSource, multiSubjectEnable,\
                        numberOfSubjectAllocation, startingPoint)
