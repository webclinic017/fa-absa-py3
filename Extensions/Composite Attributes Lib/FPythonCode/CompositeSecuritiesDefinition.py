import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object

class SecuritiesDefinition(CompositeAttributeDefinition):

    def OnInit(self, instrument, **kwargs):
        self._instrument = instrument 
    
    def Attributes(self):
        attributes = { 
                         'ipa'                  : Object( label='IPA',
                                                          objMapping=self._instrument+'.IssuingPayingAgent'),
                         'issueDay'             : Object( label='Issue Day',
                                                          objMapping=self._instrument+'.IssueDay',
                                                          transform=self.UniqueCallback('@TransformPeriodToDate')),     
                         'minimumIncremental'   : Object( label='Min Incremental',
                                                          objMapping=self._instrument+'.MinimumIncremental'),
                         'minimumPiece'         : Object( label='Minimum Piece',
                                                          objMapping=self._instrument+'.MinimumPiece'),
                         'shortSell'            : Object( label='Short Sell',
                                                          objMapping=self._instrument+'.ShortSell'),
                         'totalIssued'          : Object( label='Total Issue Size',
                                                          objMapping=self._instrument+'.TotalIssued')                                                
                    }
        if self.Instrument().IsCashFlowInstrument():
              attributes['redemptionType'] = Object( label='Redempt Type',
                                                     objMapping=self._instrument+'.RedemptionType')
        return attributes
    
    def Instrument(self):
        return self.GetMethod(self._instrument)()           
        
    # Transform
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
    
    def GetLayout(self):
        if self.Instrument().IsCashFlowInstrument():
            return self.UniqueLayout(
                        """
                        vbox[Securities;
                           totalIssued;
                            issueDay;
                            minimumPiece;
                            minimumIncremental;
                            shortSell;
                            ipa;
                            redemptionType;
                        );
                        """
                    )
        else:
            return self.UniqueLayout(
                        """
                        vbox[Securities;
                            totalIssued;
                            issueDay;
                            minimumPiece;
                            minimumIncremental;
                            shortSell;
                            ipa;
                        );
                        """
                    )
