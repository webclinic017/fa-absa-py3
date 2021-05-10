""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramUploadEngine.py"
'''
Created on 17 apr 2015

@author: marcus.lundin
'''
try:
    from FExternalDataImportEngine import FExternalDataImportEngine
except ImportError:
    FExternalDataImportEngine = object

from FTradeProgramUploadWorkflow import FTradeProgramUploadWorkflow

class FTradeProgramUploadEngine(FExternalDataImportEngine):

    def __init__(self, filename, reconciliationSpecification):
        if FExternalDataImportEngine is object:
            raise ImportError('Module Upload base is needs '
                              'to be loaded to run TradeProgram Upload')
        self._filename = filename
        super(FTradeProgramUploadEngine, self).__init__(reconciliationSpecification, None)

    def Run(self):
        self.CreateReconciliationInstance(self._filename)
        with open(self._filename, 'rb') as fp:
            valDict = self.LoadFromFile(fp)
            valDict = self.ApplyImportHook(valDict)

            for (i, fields) in enumerate(valDict):
                try:
                    externalValues = self.ApplyDataTypeConvertion(fields)
                    workflow = FTradeProgramUploadWorkflow(self.ReconciliationInstance(),
                                                           externalValues)
                    workflow.RowNumber(i)
                    self.AddWorkflow(workflow)
                except (ValueError, TypeError, AttributeError) as err:
                    raise err.__class__('Error on row %d: %s'%(i, err))
        for wf in self.ReconciliationInstance().Workflows():
            wf.CreateBusinessObject()


        return self.ReconciliationInstance()

