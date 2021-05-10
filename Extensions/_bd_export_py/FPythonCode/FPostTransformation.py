""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FPostTransformation.py"
""" Compiled: 2017-08-02 17:42:32 """

#__src_file__ = "extensions/export/./etc/FPostTransformation.py"
import os
class FPostTransformation():

    def __init__(self, exportProcess):
        self._exportProcess = exportProcess

    def Execute(self):
        """

        """
        integration = self._exportProcess.Integration()
        for singleExport in self._exportProcess.SingleExportsAsList():
            if not singleExport.IsExportable() and not self._exportProcess.GenerateEmptyFile():
                continue
            filepath = os.path.join(singleExport.FilePath(), singleExport.Filename())
            if singleExport.Filename() == integration.TradeFile:
                postTransformationFunction = integration.PostTransformationFunction()
            else:
                postTransformationFunction = integration.iPostTransformationFunction()
            postTransformationFunction(filepath)
            
