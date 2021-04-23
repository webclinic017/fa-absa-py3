
import acm
import FUxCore
from DealPackageDevKit import CompositeAttributeDefinition, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, ValGroupChoices, InstrumentPart, AttributeDialog, UXDialogsWrapper, ContextMenu, ContextMenuCommand, ReturnDomainDecorator, DealPackageDialog, DealPackageUserException, DealPackageException
from CompositeAttributes import DealPackageAttributeDialog

def EventTypeChoices():
    return [e for e in acm.FEnumeration['enum(ExoticEventType)'].Enumerators()]

class ExoticEventsHolder():

    def __init__(self, instrument, filterTypes = None):
        self._instrument = instrument
        self._filterTypes = filterTypes
        self._exoticEvents = acm.FArray()
        self._regenerate = True
        self._instrument.ExoticEvents().AddDependent(self)
        self._blockUpdates = False

    def EventTypeFilter(self, exoticEvent):
        return (self._filterTypes is None) or exoticEvent.Type() in self._filterTypes

    def ExoticEvents(self):
        if self._regenerate:
            self._regenerate = False
            self._exoticEvents.Clear()
            events = acm.FFilteredSet(self._instrument.ExoticEvents())
            events.Filter(self.EventTypeFilter)
            tableAsArray = events.AsArray()
            self._exoticEvents.AddAll(tableAsArray.SortByProperty('Date'))
        return self._exoticEvents

    def BlockUpdates(self, value):
        self._blockUpdates = value

    def Regenerate(self):
        self._regenerate = True
        self.ExoticEvents()

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if not self._blockUpdates:
            if hasattr(parameter, 'IsKindOf') and parameter.IsKindOf(acm.FExoticEvent) and self.EventTypeFilter(parameter):
                self.Regenerate()

class ExoticEvent(CompositeAttributeDefinition):

    # ############################################
    # Dev kit methods
    # ############################################

    def Attributes(self):
        attributes =  { 

            'eventsButton'      : Action ( label=self.UniqueCallback('@EventButtonLabel'),
                                           sizeToFit=True,
                                           dialog=AttributeDialog( 
                                              label='Exotic Events...', 
                                              customPanes=self.UniqueCallback('@GetEventPanes'))),

            'events'            : Object(  objMapping = InstrumentPart(self.UniqueCallback('ExoticEvents')),
                                           label = self.UniqueCallback("@EventLabel"),
                                           width = 80,
                                           height = 15,
                                           columns=self.UniqueCallback('@DisplayColumns'),
                                           onSelectionChanged=self.UniqueCallback('@SetSelectedEvent'),
                                           dialog=AttributeDialog( label='Update Exotic Event', 
                                                                   customPanes=self.UniqueCallback('@AddEditDialogCustomPanes'),
                                                                   btnLabel = 'OK'),
                                           onDoubleClick = self.UniqueCallback('@EditEventCB'),
                                           onRightClick = ContextMenu(self.UniqueCallback('@EditLinkContextMenuItem'), 
                                                                      self.UniqueCallback('@RemoveLinkContextMenuItem') )
                                            ),

            'addEvent'          : Action ( label = 'Add...',
                                           dialog=self.UniqueCallback('@StartAddDialog'),
                                           action=self.UniqueCallback('@AddEventCB')),
            
            'removeEvent'       : Action ( label= 'Remove',
                                           action=self.UniqueCallback('@RemoveEventCB'),
                                           enabled=self.UniqueCallback('@HasSelectedEvent')),
                                            
            'editEvent'         : Action ( label= 'Update...',
                                           dialog=AttributeDialog( label='Update Exotic Event', 
                                                                   customPanes=self.UniqueCallback('@AddEditDialogCustomPanes'),
                                                                   btnLabel = 'OK'),
                                           enabled=self.UniqueCallback('@HasSelectedEvent'),
                                           action = self.UniqueCallback('@EditEventCB') ),
                                           
            'generateEvent'     : Action ( label= 'Generate...',
                                           dialog=self.UniqueCallback('@StartGenerateDialog'),
                                           action = self.UniqueCallback('@GenerateEventCB') ),
                                            
            # Attributes part of dialog, showing the Exotic Event (EE)
            'selectedEvent'         : Object ( domain='FExoticEvent',
                                               onChanged=self.UniqueCallback('@SetFieldsFromSelectedEvent')),
            
            'compIns'         : Object ( label='Und Instrument',
                                         domain="FInstrument",
                                         defaultValue=self.Instrument().Underlying(),
                                         transform=self.UniqueCallback('@TransformToDomain'),
                                         choiceListSource=self.UniqueCallback('@OptionInstruments'),
                                         visible=self.UniqueCallback('@CompInsVisible')),
            
            'eventType'       : Object ( label='Type',
                                         enabled = self.UniqueCallback('@MoreThanOneEventType'),
                                         domain='enum(ExoticEventType)',
                                         defaultValue = self._defaultEventType,
                                         choiceListSource=self.UniqueCallback('@EventTypeChoices')),
            
            'startDate'       : Date   ( transform = self.UniqueCallback('@TransformStartDate'),
                                         objMapping=self.UniqueCallback("PrivateStartDate"),
                                         label='Start Date',
                                         defaultValue='0d'),
            
            'endDate'         : Date   ( transform = self.UniqueCallback('@TransformEndDate'),
                                         objMapping=self.UniqueCallback("PrivateEndDate"),
                                         label='End Date'),

            'eventValue'      : Float  ( label='Value',
                                         defaultValue = -1),
            
            'eventValueSecond': Float  ( label='Value 2',
                                         defaultValue = -1,
                                         visible=self.UniqueCallback('@EventValue2Visible')),

            'eventValueThird' : Float  ( label='Value 3',
                                         defaultValue = -1,
                                         visible=self.UniqueCallback('@EventValue2Visible')),
            
            'runNo'           : Int    ( label='Rung Number',
                                         visible=self.UniqueCallback('@LadderRungVisible')),
            
            'rolling'         : DatePeriod( label='Rolling',
                                         defaultValue = '1d'),
                                         
            'calendar'        : Object ( label='Calendar',
                                         domain='FCalendar'),
                                         
            'businessDayMethod': Object( label='Adjust Method',
                                         defaultValue='Following',
                                         domain='enum(BusinessDayMethod)'),
                                         
            
            # Attributes needed to be able to use a dialog asking to adjust non banking days
            'privateStartDate': Date   (   ),

            'privateEndDate'  : Date   (   )
 
        }
        return attributes

    #Visibility callbacks
    def CompInsVisible(self, attributeName):
        return False
    
    def EventValue2Visible(self, attributeName):
        return self.eventType in ['Price Fixing', 'Initial Fixing']
        
    def LadderRungVisible(self, attributeName):
        return self.eventType in ['Ladder rung', 'Initial Fixing']

    def OnInit(self, 
               optionName, 
               underlyingName, 
               displayColumns = None, 
               eventTypes = None,
               eventLabel = 'Exotic Events',
               showAsButton = True,
               eventUpdateAction = None, 
               **kwargs):
        
        self._exoticEventsHolder = None
        self._instrumentName = optionName
        self._underlyingName = underlyingName
        self._displayColumns = displayColumns
        self._eventUpdateAction = eventUpdateAction
        self._eventTypes = eventTypes
        self._eventLabel = eventLabel
        self._showAsButton = showAsButton
        self._defaultEventType = self._eventTypes[0] if self._eventTypes is not None else EventTypeChoices()[0]

    # #######################################################
    # Methods that can be called to modify the list of events
    # #######################################################
    def StartAddDialog(self,*args):
        self.compIns=self.Instrument().Underlying()
        return DealPackageAttributeDialog(self.GetMethod('DealPackage')(), 'Add Exotic Event', self.AddEditDialogCustomPanes(None), 'Ok') 

    def AddExoticEvent(self, 
                 componentInstrument,
                 eventType,
                 date,
                 endDate = '',
                 eventValue = -1.0,
                 eventValueSecond = -1.0,
                 eventValueThird = -1.0,
                 runNo = None ):

        if eventType not in self.EventTypeChoices(None):
            raise DealPackageException ('Exotic Event Type "%s" not allowed in this instance' % (eventType) )

        eeNew = acm.FExoticEvent()
        eeNew.Instrument(self.Instrument())
        ee = self._SetExoticEventData(eeNew, componentInstrument, eventType, date, endDate, eventValue, eventValueSecond, eventValueThird, runNo)
        for event in self.Instrument().ExoticEvents():
            if ee.Date()==event.Date() and ee.Type()==event.Type() and ee.EndDate()==event.EndDate() and ee.ComponentInstrument()==event.ComponentInstrument():
                return
        self.Instrument().ExoticEvents().Add(ee)
        ee.RegisterInStorage()
        return ee

    def EditExoticEvent(self,
                  event, 
                  componentInstrument,
                  eventType,
                  date,
                  endDate = '',
                  eventValue = -1.0,
                  eventValueSecond = -1.0,
                  eventValueThird = -1.0,
                  runNo = None ):

        if eventType not in self.EventTypeChoices(None):
            raise DealPackageException ('Exotic Event Type "%s" not allowed in this instance' % (eventType) )

        self._SetExoticEventData(event, componentInstrument, eventType, date, endDate, eventValue, eventValueSecond, eventValueThird, runNo)
    
    def RemoveExoticEvent(self, event):
        event.Unsimulate()
        
    def StartGenerateDialog(self,*args):
        self.compIns=self.Instrument().Underlying()
        self.endDate=self.Instrument().ExpiryDate()
        self.calendar=self.Instrument().Underlying().Currency().Calendar()
        return DealPackageAttributeDialog(self.GetMethod('DealPackage')(), 'Generate Exotic Event', self.GenerateDialogCustomPanes(None), 'Ok')    
    
    def GenerateExoticEvents( self, 
                        eventType, 
                        startDate, 
                        endDate, 
                        rolling,
                        calendar,
                        businessDayMethod,
                        cutOffDate = None, 
                        includeStartDate = True, 
                        regenerate = True,
                        generatePerUnderlying = True):

        if eventType not in self.EventTypeChoices(None):
            raise DealPackageException ('Exotic Event Type "%s" not allowed in this instance' % (eventType) )

        if cutOffDate not in (None, '') and acm.Time.DateDifference(startDate, cutOffDate) >= 0:
            raise DealPackageException ('Cut off date must be after start date' )
        
        if acm.Time.DateDifference(startDate, endDate) > 0:
            raise DealPackageException ('End date must be after start date' )

        self._exoticEventsHolder.BlockUpdates(True)

        #Method can be called for either a basket or a single underlying
        if generatePerUnderlying and self.Instrument().Underlying().IsKindOf(acm.FCombination):
            underlyings = self.Instrument().Underlying().Instruments()
        else:
            underlyings = [self.Instrument().Underlying()]
        
        if regenerate:
            currentEvents = self.events
            for event in currentEvents:
                if event.Type() == eventType:
                    self.RemoveExoticEvent(event)
        #New version with helpmethod
        dates=acm.DealCapturing().GenerateStripOfOptionDates(startDate, endDate, rolling, startDate, businessDayMethod, calendar, False)
        for date in dates:
            for undIns in underlyings:
                self.AddExoticEvent(undIns, eventType, date)
        
        '''
        currentDate = startDate
        nbrPeriods = 0
        count = acm.Time.DatePeriodCount(rolling)
        unit  = acm.Time.DatePeriodUnit(rolling)
        firstPeriod = True
        if cutOffDate in ('', None):
            cutOffDate = endDate
        while acm.Time.DateDifference(currentDate, cutOffDate) < 0.0 or firstPeriod:
            for undIns in underlyings:
                print 'adding', currentDate
                self.AddExoticEvent(undIns, eventType, currentDate)

            nbrPeriods += 1
            nextPeriod = '%i%s' % (count * nbrPeriods, unit) 
            currentDate = acm.Time.DateAdjustPeriod(endDate, nextPeriod, calendar, businessDayMethod)
            #currentDate = self._GetInstrumentCurrency().Calendar().ModifyDate(None, None, currentDate)
            firstPeriod = False
        
        # Add the first date equal to the start date
        if includeStartDate and acm.Time.DateDifference(startDate, endDate) <> 0:
            for undIns in underlyings:
                self.AddExoticEvent(undIns, eventType, startDate)
        '''
        self._exoticEventsHolder.BlockUpdates(False)
        self._exoticEventsHolder.Regenerate()
        

    def TransformStartDate(self, attrName, value):
        value = self._PeriodToDateTransform(value)
        value = self._ValidateDate(value, 'Start')
        return value

    def TransformEndDate(self, attrName, value):
        value = self._PeriodToDateTransform(value)
        value = self._ValidateDate(value, 'End')
        return value

    def TransformToDomain(self, attrName, value):
        if value and isinstance(value, basestring):
            domain = self.GetMethod("GetAttributeMetaData")(attrName, "domain")()
            try:
                value = domain[value]
            except:
                pass
        return value

    def EventLabel(self, attrName, *rest):
        return self._eventLabel

    def EventButtonLabel(self, attrName, *rest):
        return '%s*' % self._eventLabel if self.events else self._eventLabel

    @ReturnDomainDecorator('FArray(FExoticEvent)')
    def ExoticEvents(self):
        if self._exoticEventsHolder is None:
            self._exoticEventsHolder = ExoticEventsHolder(self.Instrument(), self._eventTypes)
        return self._exoticEventsHolder.ExoticEvents()

    def EventTypeChoices(self, attrName, *rest):
        if self._eventTypes:
            return [e for e in EventTypeChoices() if e in self._eventTypes]
        return EventTypeChoices()
    
    def OptionInstruments(self, attrName, *rest):
        listOfInstruments = []
        underlying = self.Instrument().Underlying()
        if underlying:
            listOfInstruments.append(underlying)
            if underlying.IsKindOf(acm.FCombination):
                for component in underlying.Instruments():
                    listOfInstruments.append(component)
        return listOfInstruments

    def EventUpdateAction(self, attrName, event = None):
        if self._eventUpdateAction is not None:
            self.GetMethod(self._eventUpdateAction)(attrName, event)

    def GetLayout(self):
        if self._showAsButton:
            return self.UniqueLayout("eventsButton;")
        else:
            return self.GetEventsLayout()

    def GetEventPanes(self, *args):
        return [{self._eventLabel: self.GetEventsLayout()}]

    def GetEventsLayout(self):
        return self.UniqueLayout(
               """
                hbox(;
                    events;
                    vbox{;
                        addEvent;
                        editEvent;
                        removeEvent;
                        generateEvent;
                    };
                );
                """ )


    # ####################
    # Handling the add and edit dialogs
    # ####################

    def SetDialogFields(self, event):
        self.compIns = event.ComponentInstrument()
        self.eventType = event.Type()
        self.privateStartDate = event.Date()
        self.privateEndDate = event.EndDate()
        self.eventValue = event.EventValue()
        self.eventValueSecond = event.EventValueSecond()
        self.eventValueThird = event.EventValueThird()
        self.runNo = event.RunNo()

    def SetDialogFieldsOnNoSelection(self):
        event = acm.FExoticEvent()
        typeChoices = self.EventTypeChoices(None)
        if len(typeChoices) >= 1:
            event.Type(typeChoices[0])
        event.EventValue(-1.0)
        event.EventValueSecond(-1.0)
        event.EventValueThird(-1.0)
        self.SetDialogFields(event)

    def SetFieldsFromSelectedEvent(self, attrName, *rest):
        selectedEvent = self.selectedEvent
        if selectedEvent:
            self.SetDialogFields(selectedEvent)
        else:
            self.SetDialogFieldsOnNoSelection()

    def AddEditDialogCustomPanes(self, attrName):

        layoutString = self.UniqueLayout("""
                        compIns;
                        eventType;
                        startDate;
                        eventValue;
                        eventValueSecond;
                        eventValueThird;
                        runNo;
                    """)

        return [{'Exotic Event' : layoutString}]

    def GenerateDialogCustomPanes(self, attrName):

        layoutString = self.UniqueLayout("""
                        compIns;
                        eventType;
                        startDate;
                        endDate;
                        calendar;
                        rolling;
                        businessDayMethod;
                    """)

        return [{'Exotic Event' : layoutString}]

    # ############################################
    # Methods for handling the grid columns
    # ############################################

    def DefaultColumns(self):
        return [{'methodChain': 'Type',                             'label': 'Type'},
                {'methodChain': 'ComponentInstrument.VerboseName',  'label': 'Und Instrument'},
                {'methodChain': 'Date',                             'label': 'Start Date'},
                {'methodChain': 'EndDate',                          'label': 'End Date'},
                {'methodChain': 'EventValue',                       'label': 'Value'},
                {'methodChain': 'EventValueSecond',                 'label': 'Value 2'},
                {'methodChain': 'EventValueThird',                  'label': 'Value 3'},
                {'methodChain': 'RunNo',                            'label': 'Rung Number'}]

    def DisplayColumns(self, *rest):
        if self._displayColumns is not None:
            return self._displayColumns
        else:
            return self.DefaultColumns()

    # ###################################
    # Action callbacks
    # ###################################
    def AddEventCB(self, attrName, add):
        if add:
            ee = self.AddExoticEvent( self.compIns,
                                      self.eventType,
                                      self.privateStartDate,
                                      self.privateEndDate,
                                      self.eventValue,
                                      self.eventValueSecond,
                                      self.eventValueThird,
                                      self.runNo )
            self.EventUpdateAction(attrName, ee)

    def RemoveEventCB(self, attrName):
        self.RemoveExoticEvent(self.selectedEvent)
        self.EventUpdateAction(attrName)

    def EditEventCB(self, attrName, update, *rest):
        if update:
            self.EditExoticEvent( self.selectedEvent,
                                  self.compIns,
                                  self.eventType,
                                  self.privateStartDate,
                                  self.privateEndDate,
                                  self.eventValue,
                                  self.eventValueSecond,
                                  self.eventValueThird,
                                  self.runNo )
            self.EventUpdateAction(attrName, self.selectedEvent)

    def GenerateEventCB(self, attrName, update, *rest):
        if update:
            self.GenerateExoticEvents( self.eventType, 
                                       self.privateStartDate, 
                                       self.privateEndDate, 
                                       self.rolling,
                                       self.calendar,
                                       self.businessDayMethod,
                                       cutOffDate = None, 
                                       includeStartDate = True, 
                                       regenerate = False,
                                       generatePerUnderlying = False )
            self.EventUpdateAction(attrName, self.selectedEvent)

    def SetSelectedEvent(self, attrName, selectedObj, *rest):
        self.selectedEvent = selectedObj

    def EditLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Edit..', 
                                  dialog      = AttributeDialog( label       = 'Update Exotic Event', 
                                                                 customPanes = self.UniqueCallback('@AddEditDialogCustomPanes'),
                                                                 btnLabel = 'OK'),
                                  default     = True,
                                  enabled     = self.UniqueCallback('@HasSelectedEvent') )

    def RemoveLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Remove', 
                                  invoke      = self.UniqueCallback('@RemoveEventCB'),
                                  default     = False,
                                  enabled     = self.UniqueCallback('@HasSelectedEvent') )

    # ######################
    # Convenience methods
    # ######################

    def SelectedEvent(self):
        return self.selectedEvent

    def Instrument(self):
        return self.GetMethod(self._instrumentName)()

    def Underlying(self):
        return self.GetMethod(self._underlyingName)()

    def HasSelectedEvent(self, *args):
        return self.selectedEvent!= None

    def MoreThanOneEventType(self, attrName, *rest):
        return len(self.EventTypeChoices(attrName)) > 1

    def _SetExoticEventData(self, ee, componentInstrument, eventType, startDate, endDate, eventValue, eventValueSecond, eventValueThird, runNo):
        if not startDate:
            raise DealPackageUserException('Start Date required')
        if not eventType:
            raise DealPackageUserException('Event Type required')
    
        ee.ComponentInstrument(componentInstrument)
        ee.Type(eventType)
        ee.Date(startDate)
        ee.EndDate(endDate)
        ee.EventValue(eventValue)
        ee.EventValueSecond(eventValueSecond)
        ee.EventValueThird(eventValueThird)
        ee.RunNo(runNo)

        return ee

    def _PeriodToDateTransform(self, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = acm.Time().PeriodSymbolToDate(newDate)
        return date

    def PrivateStartDate(self, value="Reading"):
        if value == "Reading":
            return self.privateStartDate
        else:
            self.privateStartDate = value

    def PrivateEndDate(self, value="Reading"):
        if value == "Reading":
            return self.privateEndDate
        else:
            self.privateEndDate = value

    # Methods for checking and making sure that date is on a banking date
    def _GetInstrumentCurrency(self):
        currency = self.Instrument().Currency()
        if not currency:
            mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
            currency = mappedValuationParameter().Parameter().AccountingCurrency()
        return currency

    def _GetInstrumentCalendar(self):
        return self._GetInstrumentCurrency().Calendar()

    def _ValidateDate(self, date, dateName):
        adjustedDate = date
        calendar = self._GetInstrumentCalendar()
        if date and calendar and calendar.IsNonBankingDay(None, None, date):
            if self._ShowAdjustDateDialog(dateName, calendar, date):
                adjustedDate = calendar.ModifyDate(None, None, date, "Following")
        return adjustedDate
    
    def _ShowAdjustDateDialog(self, name, calendar, date):
        return self.GetMethod('DealPackage')().GUI().AskAdjustDate(name, calendar, date)
