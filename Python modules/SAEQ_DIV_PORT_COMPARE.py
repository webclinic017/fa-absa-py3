""" Compiled: 2009-10-19 14:09:50 """

"""----------------------------------------------------------------------------
MODULE
    FPortfolioComparison
    
    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module is used for comparing P/L values in xml-files.    


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import sys, xml.parsers.expat

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import os, unicodedata
import time
class PCTException(Exception): pass

class PCTParser:
    """Class to parse XML files and find difference"""
    def __init__(self, file1, file2, absPrec, relPrec):
        self.__inFile1 = file1
        self.__inFile2 = file2
        self.__absPrecision = absPrec
        self.__relPrecision = relPrec
        self.__resultDir = {}
        self.__columns = []
        self.__difftree = 0

    def get_resultDir(self):
        """Get Method for result dir"""
        return self.__resultDir


    def get_diffTree(self):
        """Get Method for difftree"""
        return self.__difftree

    def parse(self):
        """Start parsing of two XML files"""
        try:
            tree1 = ElementTree.parse(self.__inFile1)
            tree2 = ElementTree.parse(self.__inFile2)
        
            self.parseTrees(tree1, tree2)
            
        except IOError, e:
            raise PCTException("IOError: " + str(e))
        except xml.parsers.expat.ExpatError:
            raise PCTException("Input file is not in proper XML format.")
        except:
            raise PCTException(str(sys.exc_value))    
    # End function that Start parsing of two XML files
    
    # Function unittested by test_FPortfolioComparison
    def parseTrees(self, tree1, tree2):
        if (tree1.find("ReportContents") <> None) and (tree2.find("ReportContents") <> None):
            Table1 = tree1.find("ReportContents").find("Table")
            Table2 = tree2.find("ReportContents").find("Table")            
            
            if Table1.find("NumberOfColumns").text <> Table2.find("NumberOfColumns").text :
                raise PCTException("Number of columns differ in both reports")

            Tab1Columns = Table1.find("Columns").findall("Column")
            Tab2Columns = Table2.find("Columns").findall("Column")

            for i in range(len(Tab2Columns)):
                if Tab1Columns[i].find("Label").text == Tab2Columns[i].find("Label").text:
                    self.__columns.append(Tab1Columns[i].find("Label").text)
                else:
                    raise PCTException("Column names Differ")
            rowsList1 = Table1.findall("Rows")
            rowsList2 = Table2.findall("Rows")


            if len(rowsList1) <> len(rowsList2):
                raise PCTException("Length of RowsList Mismatch.")

            for i in range(len(rowsList1)):
                rows1 = rowsList1[i].findall("Row")
                rows2 = rowsList2[i].findall("Row")
                #print 'PARSER TREE', len(rows1) 
            if len(rows1) <> len(rows2):
                raise PCTException("No of 'Row's in Rows differ.")
            is_diff = False
            for j in range(len(rows1)):
                #print rows1[j].find("Label").text, is_diff
                is_diff = self.__process_row(rows1[j], rows2[j], "")
                 
            self.__difftree = is_diff and tree1
        else:
            raise PCTException("Input file is not in proper XML format.") 

    def __process_row(self, row1, row2, fieldName):
        """Function to Process one Row"""
        #print 'PROCESS ROW', row1.find("Label").text 
        if row1.find("Label").text <> row2.find("Label").text:
            raise PCTException("Row name mismatch - " + row1.find("Label").text \
                               + " vs. " + row2.find("Label").text)
        
        if(fieldName==""):
            fieldName = row1.find("Label").text
        else:
            fieldName = fieldName + '^' + row1.find("Label").text


        cells1 = row1.findall("Cells/Cell")
        cells2 = row2.findall("Cells/Cell")
        #print 'here'
        is_diff = self.__check_row_differnces(cells1, cells2, fieldName)
        #print 'here also', is_diff
        rowsList1 = row1.findall("Rows")
        rowsList2 = row2.findall("Rows")
        #print 'Row', row1.find("Label").text, 'len', len(rowsList1)
        if len(rowsList1) <> len(rowsList2):
            raise PCTException("Length of RowsList Mismatch.")

        for i in range(len(rowsList1)):
            rows1 = rowsList1[i].findall("Row")
            rows2 = rowsList2[i].findall("Row")

            if len(rows1) <> len(rows2):
                raise PCTException("No of 'Row's in Rows differ.")
            #print 'Rows', 'len', len(rows1)
            for j in range(len(rows1)):
                #print 'LAST LEVEL: ', rows1[j].find("Label").text
                d = self.__process_row(rows1[j], rows2[j], fieldName)
                #print fieldName, d, is_diff
                is_diff = is_diff or d
        return is_diff
    # End Function to Process one Row

    def __check_row_differnces(self, cells1, cells2, fieldName):
        """If different values return list giving difference details"""
        is_diff = 0
        for i in range(len(cells1)):
            raw1 = cells1[i].find("RawData")
            raw2 = cells2[i].find("RawData")
            cell1 = cells1[i].find("FormattedData")
            cell2 = cells2[i].find("FormattedData")
            enc = 'ISO-8859-1'
            value1 = cell1.text and cell1.text.strip().encode(enc).replace("\xa0", "")
            value2 = cell2.text and cell2.text.strip().encode(enc).replace("\xa0", "")
            if (value1 or value2) and value1 <> value2:
                col = self.__columns[i]    
                is_diff = True
                try:
                    # Taking difference of only integer and float values
                    floatVal1= value1 and float(value1.replace(',', '')) or 0
                    floatVal2= value2 and float(value2.replace(',', '')) or 0
                    """ SHOULD USE PRIME FUNCTIONALITY!!! """
                    absDiff = abs(floatVal2-floatVal1)
                    if floatVal1 <> 0:
                        relDiff = abs(floatVal2-floatVal1)/abs(floatVal1)
                    else:
                        relDiff = absDiff
                        
                    if (float(absDiff) > float(self.__absPrecision)) and (float(relDiff) > float(self.__relPrecision)):
                        
                        diffList = [fieldName, absDiff, relDiff, floatVal2, floatVal1]
                        if self.__resultDir.has_key(col):
                            self.__resultDir[col].append(diffList)
                        else:
                            self.__resultDir[col] = [diffList]        

                        diff_str = str(floatVal2-floatVal1).split('.')
                        diff_str = diff_str[1].strip('0') and ','.join(diff_str) or\
                                    diff_str[0]
                        cell1.text = diff_str.decode('latin-1')
                except Exception, e:       
                    # Handling Text values here as float()
                    # will throw ValueError for Text values
                    
                    diffList = [fieldName, '', '', value2, value1]
                     
                    if self.__resultDir.has_key(col):
                        self.__resultDir[col].append(diffList)
                    else:
                        self.__resultDir[col] = [diffList]   
                r1 = raw1.text and raw1.text or '' 
                r2 = raw2.text and '-%s' % raw2.text or ''
                raw1.text = r1+r2
            else:
                cell1.text = ''
                raw1.text = ''
        return is_diff
    # End Function check_row_differnces
# End class PCTParser


def diff(inFile1,inFile2,outFile = "OutPut",absPrec = 0.0001,relPrec = 0.0001):
    """ Main Function when called from other Python module """
    try:
        parser = PCTParser(inFile1, inFile2, float(absPrec), float(relPrec))
    except ValueError:
        raise PCTException("Precisions should be float values.")

    parser.parse()
    result_diff = parser.get_resultDir()
    diff_tree = parser.get_diffTree()
    if diff_tree:
        diff_tree.find("Name").text = "Aggregation difference"
        diff_tree.find("Time").text = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        diff_tree.find("ReportContents").find("Table").find("Name").text = "Aggregation Difference"
    try:
        if not outFile == 'OutPut' and result_diff:
            import FReportOutput
            filePath, fileName = os.path.split(outFile)
            trueFalse=['False', 'True']
            reportOutput = FReportOutput.getAelVariables()
            outputDict = {'HTML to Screen':trueFalse[False]}
            outputDict['File Path'] = filePath
            outputDict['XML to File'] = trueFalse[True]
            outputDict['HTML to File'] = trueFalse[True]
            outputDict['Create directory with date'] = trueFalse[False]
            dict = {}
            for row in reportOutput:
                key = row[0]
                value = row[4]
                if outputDict.has_key(key):
                    dict[key] = outputDict[key]
                else:
                    dict[key] = value
            XML = ElementTree.tostring(diff_tree.getroot())
            FReportOutput.produceOutput(XML, fileName, dict)
        
    except Exception, e:
        print "Could not create XML-diff", e
    return result_diff



