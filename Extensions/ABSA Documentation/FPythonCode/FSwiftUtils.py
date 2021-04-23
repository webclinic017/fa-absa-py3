""" Compiled: 2020-06-22 15:41:27 """

#__src_file__ = "extensions/swift/etc/FSwiftUtils.py"
from __future__ import print_function
"""---------------------------------------------------------------------------------------------------------------------
MODULE
    FSwiftUtils - General utility functions

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester           Description
------------------------------------------------------------------------------------------------------------------------
2020-08-13      FAOPS-885       Tawanda Mukhalela       Kgomotso Gumbo      Removed Rounding function to use FNumFormat
                                                                            this was done to mitigate floating point 
                                                                            issues with the python round function
------------------------------------------------------------------------------------------------------------------------
"""

import re
from math import ceil, floor, modf

import acm
import FOperationsUtils as Utils

FORMATTER = acm.FNumFormatter('NumDefault')


def SwiftNumericFormatter(value):
    # slicing for SWIFT std 12d. #
    value = str(value)
    if len(value) > 12:
        value = value[:12]
    return value


def ApplyCurrencyPrecision(curr, amount):
    """
    Round decimal amount according to the precision for a currency stated
    in ROUND_PER_CURR in swift params
    """

    import FSwiftParameters as Params

    if not curr and not amount:
        Utils.LogVerbose('FSwiftUtils: could not do rounding, None returned')
        return

    rounding_precision = Params.ROUND_PER_CURR.get(curr, 2)
    FORMATTER.NumDecimals(rounding_precision)
    if rounding_precision == 0:
        return apply_zero_precision(amount)

    return float(FORMATTER.Format(amount).replace(',', ''))


def apply_zero_precision(amount):
    formatted_amount = 0.0
    absolute_amount = abs(amount)
    fraction, _ = modf(absolute_amount)
    if 1.0 - fraction < 1e-6:
        if absolute_amount - int(absolute_amount) > 0:
            formatted_amount = ceil(absolute_amount)
        elif absolute_amount - int(absolute_amount) < 0:
            formatted_amount = floor(absolute_amount)
    else:
        formatted_amount = int(absolute_amount)

    if amount < 0:
        formatted_amount *= -1

    return formatted_amount


def check_newline(newline_string, separator="newline", line_characters=35, rows=4, codeword_newline="codeword"):
    """
    Wrapper over SwiftNarrativeTextFormatter only for backword compatibility with
    2013.1 and below. Users have swift hooks that calls this function.
    """
    return SwiftNarrativeTextFormatter.Format(newline_string, separator, line_characters, rows, codeword_newline)


def GetUTINamespace(trade):
    value = ''
    if trade:
        try:
            uti = trade.UniqueTradeIdentifier()
            if uti:
                value = uti[:20]
        except Exception as e:
            print("An exception occured in GetUTINamespace: %s" % str(e))
    return value


def GetTransactionIdentifier(trade):
    value = ''
    if trade:
        try:
            uti = trade.UniqueTradeIdentifier()
            if uti:
                value = uti[20:52]
        except Exception as e:
            print("An exception occured in GetTransactionIdentifier: %s" % str(e))
    return value


def GetPriorUTINamespace(trade):
    correctionTrade = GetCorrectionTrade(trade)
    return GetUTINamespace(correctionTrade)


def GetPriorTransactionIdentifier(trade):
    correctionTrade = GetCorrectionTrade(trade)
    return GetTransactionIdentifier(correctionTrade)


def GetCorrectionTrade(trade):
    correctionTrade = None
    if trade and trade.CorrectionTrade():
        if trade.CorrectionTrade().Oid() != trade.Oid():
            correctionTrade = trade.CorrectionTrade()
    return correctionTrade


class SwiftNarrativeTextFormatter(object):
    """
    This class is responsible for applying swift narrative rules on a given text.
    It makes a note of existing 'newline' and 'codeword' separators and inserts few
    by itself if required. These separators will be replaced as 'carriage return' by
    Adaptiv Documentation module.

    Default configuration is 4 lines with maximum of 35 characters each.
    Note that some narrative fields such as field 72 must start with two slashes.
    In that case set maxLineLen to 33.
    """

    def __init__(self, text, separator, maxLineLen, maxLines, codeword):
        self.__text = text
        self.__separator = separator
        self.__maxLineLen = maxLineLen
        self.__maxLines = maxLines
        self.__codeword = codeword
        self.__pattern = re.compile('|'.join([self.__separator, self.__codeword]))
        self.__forbiddenLineStarters = ["-", ":"]

    @staticmethod
    def Format(text, separator = 'newline', maxLineLen = 35, maxLines = 4, codeword = 'codeword'):
        formatter = SwiftNarrativeTextFormatter(text, separator, maxLineLen, maxLines, codeword)
        return formatter.Compute()

    def Compute(self):

        self.__PreprocessText()

        givenText = self.__text
        computedText = ''

        matchObject = self.__pattern.search(givenText)

        while matchObject:
            existingSeparator = matchObject.group()
            textPart = givenText[:matchObject.start()]
            givenText = givenText[matchObject.end():]
            givenText = givenText.strip()
            textPart = self.__InsertLineSeparator(textPart)
            computedText = ''.join([computedText, textPart, existingSeparator])
            matchObject = self.__pattern.search(givenText)

        givenText = self.__InsertLineSeparator(givenText)
        computedText = ''.join([computedText, givenText])

        computedText = self.__TruncateText(computedText)

        return computedText

    def __PreprocessText(self):
        self.__text = self.__text.replace("\\r", self.__separator)
        self.__text = self.__text.replace("\\n", self.__separator)
        self.__text = self.__text.strip()
        self.__StripLeadingSeparators()
        self.__StripTrailingSeparators()
        self.__text = self.__AdjustLineForForbiddenChars(self.__text)

    def __StripLeadingSeparators(self):
        pattern = re.compile('^' + self.__separator + '|' + '^' + self.__codeword)
        matchObject = pattern.search(self.__text)
        while matchObject:
            self.__text = self.__text[matchObject.end():]
            self.__text = self.__text.lstrip()
            matchObject = pattern.search(self.__text)

    def __StripTrailingSeparators(self):
        pattern = re.compile(self.__separator + '$' + '|' + self.__codeword + '$')
        matchObject = pattern.search(self.__text)
        while matchObject:
            self.__text = self.__text[:matchObject.start()]
            self.__text = self.__text.rstrip()
            matchObject = pattern.search(self.__text)

    def __InsertLineSeparator(self, textPart):
        text = textPart
        textWithSeparator = ''
        while len(text) > self.__maxLineLen:
            firstPart, secondPart = self.__SplitText(text)
            textWithSeparator = ''.join([textWithSeparator, firstPart, self.__separator])
            text = secondPart.strip()
            text = self.__AdjustLineForForbiddenChars(text)

        textWithSeparator = ''.join([textWithSeparator, text])
        return textWithSeparator

    def __AdjustLineForForbiddenChars(self, line):
        SPACE = ' '
        for forbiddenChar in self.__forbiddenLineStarters:
            if line.startswith(forbiddenChar):
                line = SPACE + line
                break

        return line

    def __SplitText(self, text):
        SPACE = ' '
        breakPos = text.rfind(SPACE, 0, self.__maxLineLen)
        if breakPos < 1:
            breakPos = self.__maxLineLen
        firstPart = text[:breakPos]
        secondPart = text[breakPos:]
        return (firstPart, secondPart)

    def __TruncateText(self, computedText):
        separators = self.__pattern.findall(computedText)
        noOfSeparators = len(separators)
        if noOfSeparators >= self.__maxLines:
            computedText = self.__RemoveExtraLines(computedText)
        return computedText

    def __RemoveExtraLines(self, computedText):
        expectedLines = self.__maxLines
        computedLines = 0
        matchStart = 0
        matchEnd = 0
        matchObject = self.__pattern.search(computedText, matchEnd)
        while matchObject and (computedLines != expectedLines):
            matchStart = matchObject.start()
            matchEnd = matchObject.end()
            computedLines += 1
            matchObject = self.__pattern.search(computedText, matchEnd)

        return computedText[:matchStart]


class SwiftTrans(object):
    """
    Adopts dict_trans from swift parameters. Translates non-swift characters
    to characters mentioned in dict_trans.
    """

    def __init__(self):
        import FSwiftParameters as Global
        import FDocumentationParameters as DocParams

        self.translateTo = ''.join(Global.dict_trans.values())
        self.translateTo = self.translateTo.decode(DocParams.defaultCodePage)

    def Compute(self, data):
        return data.translate(self.translateTo)

    @staticmethod
    def Translate(data):
        swiftTrans = SwiftTrans()
        return swiftTrans.Compute(data)


class SwiftMessageHandler(object):

    def __init__(self, mt_message, mt_type):
        self.__mtMessage = mt_message
        self.__mtType = mt_type
        self.__mtTypeProvided = False
        self.__block1 = ""
        self.__block2 = ""
        self.__block3 = ""
        self.__block4 = ""
        self.__block5 = ""
        self.__extraAfterBlock5 = ""
        self.__blockFieldList = []
        self.__Swiftify()
        self.__CreateBlockFieldList()

    def __Swiftify(self):
        """
        Input string (MT) is send through block parsers that in its turn
        all the time return the rest of it.
        """
        try:
            mt = self.__mtMessage
            mt = self.__SetBlock1(mt)
            mt = self.__SetBlock2(mt)
            mt = self.__SetBlock3(mt)
            mt = self.__SetBlock4(mt)
            mt = self.__SetBlock5(mt)
            self.__extraAfterBlock5 = mt
        except Exception as e:
            print("Error: could not parse MT message\n", self.__mtMessage, str(e))

    def __GetSubstringByStartAndEndString(self, mtMessageToParse, startString, endString, rfind = False):
        try:
            if mtMessageToParse.startswith(startString):
                if rfind:
                    endPos = mtMessageToParse.rfind(endString)
                else:
                    endPos = mtMessageToParse.find(endString)
                if endPos > -1:
                    endPos = endPos + len(endString)
                    return mtMessageToParse[:endPos], mtMessageToParse[endPos:]
                else:
                    return "", mtMessageToParse
            else:
                return "", mtMessageToParse
        except Exception as e:
            print("An exception occurred in __GetSubstringByStartAndEndString:\n", str(e))
        return "", mtMessageToParse

    def __SetBlock1(self, mtMessageToParse):
        lr = self.__GetSubstringByStartAndEndString(mtMessageToParse, "{1:", "}")
        self.__block1 = lr[0]
        return lr[1]

    def __SetBlock2(self, mtMessageToParse):
        lr = self.__GetSubstringByStartAndEndString(mtMessageToParse, "{2:", "}")
        self.__block2 = lr[0]
        return lr[1]

    def __SetBlock3(self, mtMessageToParse):
        lr = self.__GetSubstringByStartAndEndString(mtMessageToParse, "{3:", "}}")
        self.__block3 = lr[0]
        return lr[1]

    def __SetBlock4(self, mtMessageToParse):
        lr = self.__GetSubstringByStartAndEndString(mtMessageToParse, "{4:", "-}")
        self.__block4 = lr[0]
        return lr[1]

    def __SetBlock5(self, mtMessageToParse):
        lr = self.__GetSubstringByStartAndEndString(mtMessageToParse, "{5:", "}", True)
        self.__block5 = lr[0]
        return lr[1]

    def __CreateBlockFieldList(self):

        #block 1
        dict1 = {}
        block1val = self.__GetSimpleBlockValue(self.GetBlock1())
        dict1['Block'] = 1
        dict1['Field'] = 0
        dict1['Value'] = self._HandleSpecialFields(0, block1val)
        dict1['Occurrence'] = 0
        self.__blockFieldList.append(dict1)


        #block 2
        dict2 = {}
        block2val = self.__GetSimpleBlockValue(self.GetBlock2())
        dict2['Block'] = 2
        dict2['Field'] = 0
        dict2['Value'] = self._HandleSpecialFields(0, block2val)
        dict2['Occurrence'] = 0
        self.__blockFieldList.append(dict2)


        #block 3
        block3fields = self.__GetSubBlockFields((self.GetBlock3()))

        for fieldval in block3fields:
            tempdict = {}
            tempdict['Block'] = 3
            tempdict['Field'] = fieldval[0]
            tempdict['Value'] = self._HandleSpecialFields(fieldval[0], fieldval[1])
            tempdict['Occurrence'] = 0
            self.__blockFieldList.append(tempdict)

        #block 4
        block4dict = self.__GetMultiLineFields(self.GetBlock4())
        for field, valueList in block4dict.iteritems():
            occurrence = 0
            for value in valueList:
                tempdict = {}
                tempdict['Block'] = 4
                tempdict['Field'] = field
                tempdict['Value'] = self._HandleSpecialFields(field, value)
                tempdict['Occurrence'] = occurrence
                self.__blockFieldList.append(tempdict)
                occurrence = occurrence + 1


        #block 5
        block5fields = self.__GetSubBlockFields((self.GetBlock5()))
        for fieldval in block5fields:
            tempdict = {}
            tempdict['Block'] = 5
            tempdict['Field'] = fieldval[0]
            tempdict['Value'] = self._HandleSpecialFields(fieldval[0], fieldval[1])
            tempdict['Occurrence'] = 0
            self.__blockFieldList.append(tempdict)

    def GetBlock1(self):
        return self.__block1

    def GetBlock2(self):
        return self.__block2

    def GetBlock3(self):
        return self.__block3

    def GetBlock4(self):
        return self.__block4

    def GetBlock5(self):
        return self.__block5

    def GetBlockFieldList(self):
        return self.__blockFieldList

    def GetMTType(self):
        return self.__mtType

    def __GetSimpleBlockValue(self, block):
        return block[3:-1]

    def __GetSubBlockFields(self, block):
        '''
        {3:{108:FAS-54843-1}} --> {108:FAS-54843-1}
        '''
        fieldlist = []
        try:
        # Remove block, keep fields: {3:{108:FAS-54843-1}} ---> {108:FAS-54843-1}
            if len(block) >= 4:
                fields = block [3:-1]
                while fields != "" and fields != "\n" and fields != "\r\n":
                    field, fields = self.__GetSubstringByStartAndEndString(fields, '{', '}')
                    if field != "":
                        field = field[1:-1] #remove braces
                        keyval = field.split(':')
                        if keyval and len(keyval) > 1:
                            key = keyval[0]
                            val = keyval[1]
                            fieldlist.append((key, val))
        except Exception as e:
            print("An exception occurred in __GetSubBlockFields:\n", str(e))
        return fieldlist

    def __GetMultiLineFields(self, block):
        keysAndValues = {}
        currentKey = ""
        currentValue = ""
        previousKey = ""

        # remove block headers "{X:\r\n", "\r\n-}"
        block = block[5:-4]

        rows = block.split("\r\n")
        try:
            for row in rows:
                splits = row.split(":")

                #a field and its value looks like this: ":field:value"
                if splits[0] == "" and row.count(":") >= 2 and len(splits) >= 3:   #we have a field
                    currentKey = splits[1]
                    currentValue = ''
                    if row.count(":") == 2:        # :field:value
                        currentValue = splits[2]
                    elif row.count(":") == 3:      # :field::value
                        currentValue = splits[3]
                    if currentKey in keysAndValues:   #if more than one of the same field, append value to list
                        keysAndValues[currentKey].append(currentValue)
                    else:
                        keysAndValues[currentKey] = [currentValue]
                    previousKey = currentKey
                else:   #a value without field, must belong to previous field or be empty row
                    currentValue = row
                    keysAndValues[previousKey][-1] = keysAndValues[previousKey][-1] + "\n" + currentValue
        except Exception as e:
            print("An exception occurred in __GetMultiLineFields:\n", str(e))
        return keysAndValues

    def _HandleSpecialFields(self, field, value):
        """
        Derived classes can override this function to pre-process values
        """
        return value
