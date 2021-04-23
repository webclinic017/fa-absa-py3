import acm
from DealPackageDevKit import CompositeAttributeDefinition
from DealPackageDevKit import List, Str, Object
from RFQUtils import Direction, HistoryDirectionMap, Time, MethodDirection
from RFQHistoryProvider import QrHistoryHandler
from math import isnan
import datetime
        
class RFQHistory(CompositeAttributeDefinition):

    def Attributes(self):
        attributes = {}
        
        ''' Reply '''
        attributes.update({

                'history'               : List(   label='History',
                                                  elementDomain='FAccount',
                                                  addNewItem =['First', 'Sorted'],
                                                  sortIndexCallback=self.UniqueCallback('@HistorySortIndexCallback'),
                                                  columns=self.UniqueCallback('@Columns'))
        })
        
        return attributes
        
    
    def Columns(self, *args):
        columns      =        [{'methodChain': 'Depository2', 'label': 'Time'}, 
                               {'methodChain': 'Account',     'label': 'Initiator'}, 
                               {'methodChain': 'Account2',    'label': 'Status'}, 
                               {'methodChain': 'Depository',  'label': 'Side'},
                               {'methodChain': 'Account3',    'label': 'Price'}]
        if self.QRData().IsMultiRFQ():
            columns.append({'methodChain': 'Depository3',  'label': 'Orderbook'})
        columns.append({'methodChain': 'Account5',    'label': 'Comment'})
        return columns
        
    
    '''********************************************************************
    * Deal Definition
    ********************************************************************'''    
    def OnInit(self, **kwargs):
        self._qrData = kwargs['qrDataMethod']
        self._instrument = kwargs['instrumentMethod']
        self._historyProvider = None

    '''********************************************************************
    * When a new RFQ is created from existing window
    ********************************************************************'''
    def ClearHistoryList(self):
        self.history.Clear()
        if self._historyProvider:
            self.QrQueryHandler().RemoveObserverCallback(self._historyProvider.OnQueryResult)
        self._historyProvider = None

    '''********************************************************************
    * Misc
    ********************************************************************'''       
    def QRData(self):
        return self.GetMethod(self._qrData)()

    def QrQueryHandler(self):
        return self.QRData().QrQueryHandler()

    def Instrument(self):
        return self.GetMethod(self._instrument)()

    def HistoryProvider(self):
        if not self._historyProvider:
            self._historyProvider = QrHistoryHandler(self.AddHistoryItem, self.QRData().QuantityToNominal)
            self.QrQueryHandler().AddObserverCallback(self._historyProvider.OnQueryResult)
        return self._historyProvider

    '''********************************************************************
    * Update history
    ********************************************************************'''    
    def FetchHistoryNeeded(self, val = MethodDirection.asGetMethod):
        return self.HistoryProvider().QueryNeeded(val)
        
    def FetchHistoryIfNeeded(self):
        if self.HistoryProvider().QueryNeeded():
            quoteRequest = self.QRData().CustomerQuoteRequestInfo()
            if quoteRequest:
                self.UpdateHistoryRowItems(quoteRequest.CustomerRequest())
    
    def UpdateHistoryRowItems(self, customerRequest):
        try:
            self.QrQueryHandler().ExecuteQuery(customerRequest)
        except Exception as e:
            print(('Update  History Row Items', e))
    
    def AddQuoteRequestToHistory(self, quoteRequest):
        try:
            self.HistoryProvider()
            self.QrQueryHandler().AddQuoteRequestToHistory(quoteRequest)
        except Exception as e:
            print(('Add Quote Request To History', e))

    def AddHistoryItem(self, entry):
        self.history.AtInsert(0, entry)

    '''********************************************************************
    * List Sorting
    ********************************************************************'''
    def TimeComparator(self, timeStr):
        try:
            parsedTime = Time.OnlyIfTodayParse(timeStr)
            return acm.Time.DateTimeToTime(parsedTime)
        except Exception as e:
            return 0

    def HistorySortIndexCallback(self, attrName, columnNbr, value, formatter, obj):
        if columnNbr <= 0:
            return -self.TimeComparator(value)
        else:
            return value

    '''********************************************************************
    * Layout
    ********************************************************************'''
    def GetLayout(self):
        return self.UniqueLayout(
                    '''
                    hbox(;
                        history;
                        vbox(;
                            space(110);
                        );
                    );
                    ''')
