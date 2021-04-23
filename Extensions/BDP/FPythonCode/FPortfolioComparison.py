""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FPortfolioComparison.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FPortfolioComparison

DESCRIPTION
    This module is used for comparing P/L values in xml-files.


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import collections
import os
import math
import sys
import xml.parsers.expat
from xml.etree import ElementTree
import time


import FReportOutput


class PCTException(Exception):
    pass


class PCTParser:
    """
    Class to parse XML files and find difference
    """

    def __init__(self, file1, file2, grouping,
                absPrec, relPrec, ignorePrec, requiredCols=None):

        self.__inFile1 = file1
        self.__inFile2 = file2
        self.__absPrecision = absPrec
        self.__relPrecision = relPrec
        self.__ignorePrec = ignorePrec
        self.__requiredCols = set(requiredCols or [])
        self.__resultDir = collections.defaultdict(list)
        self.__columns = []
        self.__difftree = 0
        self.__grouping = grouping

    def get_resultDir(self):
        """
        Get Method for result dir
        """
        return self.__resultDir

    def get_diffTree(self):
        """
        Get Method for difftree
        """
        return self.__difftree

    def parse(self):
        """
        Start parsing of two XML files
        """
        try:
            tree1 = ElementTree.parse(self.__inFile1)
            tree2 = ElementTree.parse(self.__inFile2)
            self.parseTrees(tree1, tree2)
        except IOError as e:
            raise PCTException("IOError: " + str(e))
        except xml.parsers.expat.ExpatError:
            raise PCTException("Input file is not in proper XML format.")
        except PCTException:
            raise
        except:
            raise PCTException(str(sys.exc_info()))

    # End function that Start parsing of two XML files

    # Function unittested by test_FPortfolioComparison

    def parseTrees(self, tree1, tree2):

        if ((tree1.find("ReportContents") is not None) and
                (tree2.find("ReportContents") is not None)):
            Table1 = tree1.find("ReportContents").find("Table")
            Table2 = tree2.find("ReportContents").find("Table")

            if (Table1.find("NumberOfColumns").text !=
                    Table2.find("NumberOfColumns").text):
                raise PCTException("Number of columns differ in both reports")
            Tab1Columns = Table1.find("Columns").findall("Column")
            Tab2Columns = Table2.find("Columns").findall("Column")
            for i in range(len(Tab2Columns)):
                if (Tab1Columns[i].find("Label").text ==
                        Tab2Columns[i].find("Label").text):
                    self.__columns.append(Tab1Columns[i].find("Label").text)
                else:
                    raise PCTException("Column names Differ")
            list1, list2 = self.__get_row_lists(Table1, Table2)
            is_diff = [0]
            self.__process_row_list(list1, list2, "", is_diff)
            self.__difftree = is_diff[0] and tree1
        else:
            raise PCTException("Input file is not in proper XML format.")

    def __get_row_lists(self, row1, row2):

        rowsList1 = row1.findall("Rows")
        rowsList2 = row2.findall("Rows")
        if len(rowsList1) != len(rowsList2):
            raise PCTException("Length of RowsList Mismatch.")
        list1 = rowsList1[0].findall("Row")
        list2 = rowsList2[0].findall("Row")
        if len(list1) != len(list2):
            raise PCTException("No of 'Row's in Rows differ.")
        return (list1, list2)

    def __process_row_list(self, list1, list2, fieldName="", is_diff=[0]):

        for j in range(len(list1)):
            self.__process_row(list1[j], list2[j], fieldName, is_diff)

    def __process_row(self, row1, row2, fieldName, is_diff=[0]):
        """
        Function to Process one Row
        """
        text1 = row1.find("Label").text
        text2 = row2.find("Label").text
        if text1 != text2:
            raise PCTException("Row name mismatch - %s vs. %s" % (text1,
                    text2))
        if not fieldName:
            fieldName = text1
        else:
            fieldName = fieldName + '^' + text1
        cells1 = row1.findall("Cells/Cell")
        cells2 = row2.findall("Cells/Cell")
        if self.__check_row_differnces(cells1, cells2, fieldName):
            is_diff[0] = 1
        list1, list2 = self.__get_row_lists(row1, row2)
        self.__process_row_list(list1, list2, fieldName, is_diff)

    # End Function to Process one Row

    def __check_row_differnces(self, cells1, cells2, fieldName):
        """
        If different values return list giving difference details
        """
        is_diff = 0
        absPrec = float(self.__absPrecision)
        relPrec = float(self.__relPrecision)
        for i in range(len(cells1)):
            raw1 = cells1[i].find("RawData")
            raw2 = cells2[i].find("RawData")
            cell1 = cells1[i].find("FormattedData")
            cell2 = cells2[i].find("FormattedData")
            enc = 'ISO-8859-1'
            value1 = (cell1.text and
                    cell1.text.strip().encode(enc).replace("\xa0", ""))
            value2 = (cell2.text and
                    cell2.text.strip().encode(enc).replace("\xa0", ""))
            rawValue1 = (raw1.text and
                    raw1.text.strip().encode(enc).replace("\xa0", ""))
            rawValue2 = (raw2.text and
                    raw2.text.strip().encode(enc).replace("\xa0", ""))
            col = self.__columns[i]
            if ((rawValue1 or rawValue2) and (rawValue1 != rawValue2)) or \
                (col in self.__requiredCols):
                is_diff = True
                try:
                    # Taking difference of only integer and float values
                    floatVal1 = float(rawValue1 if rawValue1 else 0)
                    floatVal2 = float(rawValue2 if rawValue2 else 0)
                    absDiff = math.fabs(floatVal2 - floatVal1)
                    if floatVal1 != 0.0:
                        relDiff = absDiff / math.fabs(floatVal1)
                    else:
                        relDiff = absDiff

                    if (self.__ignorePrec or
                        ((absDiff > absPrec) and (relDiff > relPrec))):
                        diffList = [fieldName, absDiff, relDiff, floatVal2,
                                floatVal1]
                        self.__resultDir[col].append(diffList)
                        diff_str = str(round(floatVal2 - floatVal1)).split('.')
                        diff_str = diff_str[0]
                        cell1.text = diff_str.decode('latin-1')
                except Exception:
                    # Handling Text values here as float()
                    # will throw ValueError for Text values
                    diffList = [fieldName, '', '', value2, value1]
                    self.__resultDir[col].append(diffList)
                r1 = raw1.text and raw1.text or ''
                r2 = raw2.text and '-%s' % raw2.text or ''
                raw1.text = r1 + r2
            else:
                cell1.text = ''
                raw1.text = ''
        return is_diff

    # End Function check_row_differnces

# End class PCTParser


def remove_zero_from_row(row, zero_RowList):
    cells = row.findall("Cells/Cell")
    found = 0
    for i in range(len(cells)):
        cell = cells[i].find("FormattedData")
        enc = 'ISO-8859-1'
        value = (cell.text and
                cell.text.strip().encode(enc).replace("\xa0", ""))
        try:
            if value and float(value):
                found = 1
                break
        except (ValueError, TypeError):
            # handle text values as not requiring removal of zero
            continue
    if not found:
        zero_RowList.append(row)
    else:
        zero_RowList_Children = []
        rowsList = row.findall("Rows")
        rowList = rowsList[0].findall("Row")
        remove_zero_from_row_list(rowList, zero_RowList_Children)
        for row_c in zero_RowList_Children:
            rowsList[0].remove(row_c)

def remove_zero_from_row_list(rowList, zero_RowList):
    for j in range(len(rowList)):
        remove_zero_from_row(rowList[j], zero_RowList)

def remove_zero_diffs_from_tree(tree):
    if tree.find("ReportContents") is not None:
        Table = tree.find("ReportContents").find("Table")
        rowsList = Table.findall("Rows")
        rowList = rowsList[0].findall("Row")
        zero_RowList = []
        remove_zero_from_row_list(rowList, zero_RowList)
        for row in zero_RowList:
            rowsList[0].remove(row)
    else:
        raise PCTException("Input file is not in proper XML format.")

def diff(inFile1, inFile2, outFile="OutPut", grouping=False,
        absPrec=0.0001, relPrec=0.0001, ignorePrec=0, requiredCols=None):
    """
    Main Function when called from other Python module
    """
    try:
        parser = PCTParser(inFile1, inFile2, grouping,
                float(absPrec), float(relPrec), ignorePrec, requiredCols)
    except ValueError:
        raise PCTException("Precisions should be float values.")

    parser.parse()
    result_diff = parser.get_resultDir()
    diff_tree = parser.get_diffTree()
    if diff_tree:
        diff_tree.find("Name").text = "Aggregation difference"
        diff_tree.find("Time").text = str(time.strftime("%Y-%m-%d %H:%M:%S",
                time.gmtime()))
        diff_tree.find("ReportContents").find("Table").find("Name").text = (
                "Aggregation Difference")
        remove_zero_diffs_from_tree(diff_tree)
    try:
        if not outFile == 'OutPut' and result_diff:

            filePath, fileName = os.path.split(outFile)
            trueFalse = ['False', 'True']
            reportOutput = FReportOutput.getAelVariables()
            outputDict = {'HTML to Screen': trueFalse[False]}
            outputDict['File Path'] = filePath
            outputDict['XML to File'] = trueFalse[True]
            outputDict['HTML to File'] = trueFalse[True]
            outputDict['Create directory with date'] = trueFalse[False]
            dct = {}
            for row in reportOutput:
                key = row[0]
                value = row[4]
                if key in outputDict:
                    dct[key] = outputDict[key]
                else:
                    dct[key] = value
            XML = ElementTree.tostring(diff_tree.getroot())
            FReportOutput.produceOutput(XML, fileName, dct)
    except Exception as e:
        print(('Could not create XML-diff. {0}'.format(e)))
    return result_diff
