""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FRiskCubeCustomWriters.py"
from __future__ import print_function
import acm
import FRiskCubeWriterBase as RiskBase
from FRiskCubeScenarioWriters import BaseScenarioWriter


class CustomWriter(BaseScenarioWriter):
    @staticmethod
    def hasColumnParameters():
        return False

    @staticmethod
    def getColumnParameters():
        return []


class VectorWriter(CustomWriter):
    REPORT_TYPES = ["Sensitivity"]
    SCENARIO_TYPES = ["Group", "INTEREST RATE"]
    NAME = 'Stress Name'
    MAJORS = {'CHF', 'USD', 'EUR', 'JPY', 'GBP'}

    @staticmethod
    def hasColumnParameters():
        return True

    @staticmethod
    def getColumnParameters():
        currencies = acm.FCurrency.Select('').AsArray()
        currVector = []
        for currency in currencies:
            np = acm.FNamedParameters()
            np.Name(currency.Name())
            np.AddParameter("currency", currency)
            currVector.append(np)
        return currVector

    def _createReportHeader(self):
        if self.__class__.NOREPORT_HEADER:
            return None
            
        seps = self.separators
        nCols = 1
        headerFormat = seps[0].join(self.__class__.SCENARIO_TYPES
                + [RiskBase.CURVE_DATE, acm.Time.DateToday(),
                    RiskBase.MONEYNESS, "1.0",
                    RiskBase.STRESS_TYPE, 'Standard',])
        dataFormat = seps[0].join([RiskBase.DELTA, str(nCols), seps[1].join(
            [RiskBase.CURVE_ID, self.__class__.NAME,])])
        return RiskBase.Header(self.__class__.REPORT_TYPES,
                {RiskBase.COLUMN_COUNT: nCols,
                    RiskBase.HEADER_FORMAT: headerFormat,
                    RiskBase.DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        return ["Factor Currency", "Majors", "Delta"]

    def _getCalculatedValues(self, posID):
        """
        Returns an array of arrays (of strings), each with the same length (no.
        of columns) as the array from _getCalculatedColumnHeaders().
        """
        calcs = []
        for colID, colInfo in self.columnInfoTable.items():
            calcVect = self.output[(posID, colID)]
            currencies = colInfo.columnPartNames
            assert len(currencies) == len(calcVect), ("Expecting {0} "
                    "currencies, got {1}.".format(len(calcVect),
                        len(currencies)))
            for i, calc in enumerate(calcVect):
                assert len(calc.projectionCoordinates) == 1, ("Expecting just"
                        " 1 dimension on this column, got {0}.".format(
                            len(calc.projectionCoordinates)))
                val = RiskBase.BaseWriter._getStringValue(posID, colID,
                        calc.values, self._logger)
                currency = currencies[i]
                calcs.append([currency,
                    str(currency in self.__class__.MAJORS), val])
        return calcs

    def _writeDataRows(self, fp):
        """
        Writes the actual data rows.
        """
        positions = {nodeKey[0] for nodeKey in self.output.keys()}
        for posID in sorted(positions):
            attrs = self._getAttributeValues(posID)
            bs = self._getBookStructure(posID, attrs)
            rowID = self._getPositionID(str(attrs + bs))
            calcs = self._getCalculatedValues(posID)
            for cc in calcs:
                line = self.separators[0].join(rowID + attrs + bs + cc)
                line = self._encodeData(line)
                print(line, file=fp)

class ArtiQVectorWriter(VectorWriter):

    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
