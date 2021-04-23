from __future__ import print_function
import csv
import os

def parseFile(fileName, delimiter):
    reader = csv.reader(open(fileName, "rb"), delimiter=delimiter)
    row = None
    try:
        row = next(reader)
    except StopIteration:
        pass
    dictionary = {}
    while row != None:
        if hasValues(row):
            nextRow = parseRow(row, reader, dictionary)
            row = nextRow
        try:
            if not hasValues(row):
                row = next(reader)
        except:
            break
    testName = os.path.splitext(os.path.split(fileName)[1])[0]
    dictionary['TestFileName'] = testName
    return dictionary

def hasValues(row):
    if len(row) == 0:
        return False
    if row[0] == 'comment':
        return False
    for value in row:
        if value != '':
            return True
    return False

def addToDictionary(rowName, rowValue, dic):
    for i in range(len(rowName)):
        if i > 0:
            if rowName[i] != '':
                value = ''
                if len(rowValue) > i:
                    value = rowValue[i]
                dic[rowName[i]] = value

def addToDictionaryList(rowKeys, rowLine, list):
    dic = {}
    addToDictionary(rowKeys, rowLine, dic)
    list.append(dic)
    return list

def addMultiValues(rowKeys, rowValues, dic):
    for i in range(len(rowValues)):
        if i > 0:
            value = rowValues[i]
            if value != '':
                key = rowKeys[i]
                values = dic[key]
                if type(values) == type([]):
                    values.append(value)
                else:
                    values = [values, value]
                dic[key] = values

def createDictionary(reader):
    dic = {}
    list = []
    rowKeys = []
    rowValues = []
    rowLine = []
    while True:
        try:
            row = next(reader)
        except:
            return [dic, []]
        if hasValues(row):
            break
    type = row[0]
    if type == 'key':
        rowKeys = row
        multiValuesToSameKey = False
    else:
        return [dic, row]
    while True:
        try:
            row = next(reader)
        except:
            row = []
            break
        if len(row) == 0:
            row = []
            break
        type = row[0]
        if type == 'comment':
            continue
        if type == 'key':
            rowKeys = row
            multiValuesToSameKey = False
            continue
        if type == 'value':
            rowValues = row
            if multiValuesToSameKey:
                addMultiValues(rowKeys, rowValues, dic)
            else:
                addToDictionary(rowKeys, rowValues, dic)
            multiValuesToSameKey = True
            continue
        if type == 'line':
            rowLine = row
            addToDictionaryList(rowKeys, rowLine, list)
            continue
        break
    nextRow = row
    if len(list) > 0:
        return [list, nextRow]
    else:
        return [dic, nextRow]

def parseRow(row, reader, dict):
    name = row[0]
    if name == 'key' or name == 'value' or name == 'line':
        print ('Dictionary id are NOT allowed to be: %s.' %name)
        return
    try:
        list = createDictionary(reader)
        dict[name] = list[0]
        nextRow = list[1]
        return nextRow
    except Exception as ex:
        print ('Error reading %s' %name)
        raise ex
    




