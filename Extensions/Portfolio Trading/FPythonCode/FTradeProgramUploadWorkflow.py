""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramUploadWorkflow.py"
import acm
try:
    import FBusinessDataCreator
    from FExternalDataImportWorkflow import FExternalDataImportWorkflowBase
except ImportError:
    FExternalDataImportWorkflowBase = object

class FTradeProgramUploadWorkflow(FExternalDataImportWorkflowBase):

    def __init__(self, reconciliationInstance, externalValues):
        if FExternalDataImportWorkflowBase is object:
            raise ImportError('Module Upload base is needs '
                              'to be loaded to run TradeProgram Upload')
        self._ACMObject = None
        self._businessObjectValidationMessage = ''
        self._businessObjectCommitErrorMessage = ''
        self._originatesFromADS = False

        reconciliationItem = acm.FReconciliationItem()
        reconciliationItem.ExternalValues(externalValues)
        reconciliationItem.ReconciliationDocument(reconciliationInstance.ReconciliationDocument())
        super(FTradeProgramUploadWorkflow, self).__init__(reconciliationInstance,
                                                          reconciliationItem)

    def OriginatesFromADS(self, fromADS=None):
        if fromADS is None:
            return self._originatesFromADS
        self._originatesFromADS = fromADS

    def BusinessObjectValidationMessage(self, message=None):
        if message is None:
            if self._businessObjectValidationMessage != '' and self.RowNumber() != None:
                return 'Validation error on row number %d: %s'%(self.RowNumber(),
                                                                self._businessObjectValidationMessage)
            return self._businessObjectValidationMessage
        self._businessObjectValidationMessage = message

    def BusinessObjectCommitErrorMessage(self, message=None):
        if message is None:
            if self._businessObjectCommitErrorMessage != '' and self.RowNumber() != None:
                return 'Commit error on row number %d: %s'%(self.RowNumber(),
                                                            self._businessObjectCommitErrorMessage)
            return self._businessObjectCommitErrorMessage
        self._businessObjectCommitErrorMessage = message

    def BusinessDataCreator(self, creator=None):
        if creator is None:
            return self._businessDataCreator
        self._businessDataCreator = creator

    def CreateBusinessObject(self):
        if self.ErrorMessage():
            self.BusinessObjectValidationMessage('Validation not possible '
                                                 'because of previous errors')
            return

        reconSpec = self.ReconciliationInstance().ReconciliationSpecification()
        creator = FBusinessDataCreator.GetCreator(reconSpec, self.ReconciliationItem(), self.ACMObject())
        creator.MandatoryFields(['Currency', 'Instrument', 'Portfolio', 'Quantity', 'Price'])
        self.BusinessDataCreator(creator)
        try:
            creator.PreCommitHook()
        except Exception as err:
            self.ErrorMessage(str(err))
            return None
        try:
            creator.Validate()
        except ReferenceError as err:
            self.BusinessObjectValidationMessage(str(err))
            return None
        self.ACMObject(creator.BusinessObject())