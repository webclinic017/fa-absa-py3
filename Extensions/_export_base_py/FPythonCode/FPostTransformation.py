""" Compiled: 2020-09-18 10:38:52 """

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
            postTransformationFunction = integration.PostTransformationFunction()
            postTransformationFunction(filepath)
