""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FTradeTagWriter.py"
from __future__ import print_function
import os, os.path
import sys
import inspect
import acm
import FDealTagsHook
import FRiskCubeWriterBase
import hashlib

DEFAULT_EXPORT_SUFFIX='csv'
SOURCE_ENCODING = 'latin1'
TARGET_ENCODING = 'utf8'
FILE_SUFFIXES = ('.dat', '.txt', '.csv', '.aap')

TagCls = FDealTagsHook.TAGCLASS

class TradeTagWriter(object):
    
    @staticmethod
    def _encodeData(line):
        if sys.version_info[0] >= 3:
            return line    
        else:
            return str(line, SOURCE_ENCODING
                ).encode(TARGET_ENCODING)
    
    def __init__(self, tradeNodeL, logger):
        self.tradeNodeL = tradeNodeL
        self._logger = logger
        

    def _getNewFileName(self, filename, overwrite):
        dirname = os.path.dirname(filename)
        filebasename = os.path.basename(filename)
        
        if filebasename.endswith(FILE_SUFFIXES):
            filebasename, suffix = filebasename.rsplit('.', 1)
        else:
            suffix =  DEFAULT_EXPORT_SUFFIX

        filepath = os.path.join(dirname, '{0}.{1}'.format(filebasename, suffix))
        if not os.path.exists(filepath) or overwrite:
            return filepath

        for i in range(1, MAX_FILES_IN_DIR + 1):
            f = os.path.join(dirname, '{0}{1}.{2}'.format(filebasename, i, suffix))

            if not os.path.exists(f):
                return f
        raise Exception("Maximum no. of {0} files found in {1}. Please clear "
                "out directory or allow overwrites.".format(filename, dirname))

    def _writeDataHeader(self, fp):
        tagHeader = TagCls.getTagTitles()
        header = '<Deals Tag_Titles="{0}">'.format(tagHeader)
        print('{0}'.format(header), file=fp)

    def _getDealStr(self, booknode, trade):
        tag = TagCls()._getTagVals(booknode, trade)
        line = '<Deal>Object=ZERODeal,Reference={0},MtM=&lt;undefined&gt;,Tags={1},Info=</Deal>'.format(trade.Oid(), tag)
        return line
  
    def _writeDataRows(self, fp):
        for trdNodeIndex in self.tradeNodeL:
            line = self._getDealStr(trdNodeIndex[0], trdNodeIndex[1])
            line = self._encodeData(line)
            print(line, file=fp)

        endline = self._encodeData('</Deals>')
        print(endline, file=fp)

    def write(self, overwrite, filepath=r'C:\Temp\Book Tags.csv'):
        """
        Writes the output in Risk Cube format in several parts - report header,
        data header, data rows.
        """
        FRiskCubeWriterBase.BaseWriter._initDirs(filepath)
        filename = self._getNewFileName(filepath, overwrite)
        id_ = int(hashlib.md5(filename.encode("utf-8")).hexdigest(), 16)
        try:
            with open(filename, 'w') as fp:
                self._writeDataHeader(fp)
                self._writeDataRows(fp)
            self._logger.logInfo("{0} successfully exports into file {1}".format(self.__class__.__name__, filename))
            self._logger.summaryAddOk("File", id_, "Export")
        except Exception as err:
            tb = inspect.getframeinfo(inspect.trace()[-1][0])
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(type(err).__name__,
                    err, tb.filename, tb.function, tb.lineno))
            self._logger.logError("{0} failed to export to file {1}".format(self.__class__.__name__, filename))
