""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/scripts/FOperationsDocumentXMLPreview.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FOperationsDocumentXMLPreview - Module for previewing xml for settlement/confirmation
    that would be sent to the Documentation module.

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    In order to use a certain settlement/confirmation either enter seqnbr or
    choose from the list. Drop down list only displays those settlements/
    confirmations that are in status Authorised. You can manually enter any
    settlement/confirmation number to view its xml even if it is not in
    Authorised status.

USAGE FROM PYTHON
import acm
import FOperationsDocumentXMLPreview

FOperationsDocumentXMLPreview.PreviewSettlementXML(acm.FSettlement[<Oid>])
FOperationsDocumentXMLPreview.PreviewConfirmationXML(acm.FConfirmation[<Oid>])
----------------------------------------------------------------------------"""

import acm
import os
from tempfile import gettempdir
from FConfirmationXML import FConfirmationXML
from FSettlementXML import FSettlementXML
import FSwiftMessageTypeCalculator
from FSwiftExceptions import SwiftWriterAPIException


def PreviewConfirmationsXMLs(confirmations):
    for aConfirmation in confirmations:
        mt = 0
        if aConfirmation.IsApplicableForSWIFT():
            mt = FSwiftMessageTypeCalculator.Calculate(aConfirmation)
            if mt == 0:
                print('No XML generated for:')
            else:
                xml = FConfirmationXML(aConfirmation).GenerateXmlFromTemplate()
                OpenXML(xml, "Confirmation_" + str(aConfirmation.Oid()))
        else:
            xml = FConfirmationXML(aConfirmation).GenerateXmlFromTemplate()
            OpenXML(xml, "Confirmation_" + str(aConfirmation.Oid()))
        PrintDetails('Confirmation', aConfirmation.Oid(), mt)

def PreviewSettlementsXMLs(settlements):
    for aSettlement in settlements:
        mt = FSwiftMessageTypeCalculator.Calculate(aSettlement)
        if mt:
            xml = FSettlementXML(aSettlement).GenerateXmlFromTemplate()
            OpenXML(xml, "Settlement_" + str(aSettlement.Oid()))
        else:
            print('No XML generated for:')

        PrintDetails('Settlement', aSettlement.Oid(), mt)

def PrintDetails(objectType, Oid, mt):
    print('%s = %d' % (objectType, Oid))
    print('Swift Message Type = %d' % mt)
    print('==============')

def OpenXML(xmlData, fileName):
    filePath = os.path.join(gettempdir(), fileName + ".xml")
    with open(filePath, 'w') as f:
        f.write(xmlData)
    f.close()
    os.startfile(filePath)

def CreateSettlementQuery():
    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('Status', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('Trade.Oid', 'EQUAL', None)
    return query

def CreateConfirmationQuery():
    query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('Status', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('Trade.Oid', 'EQUAL', None)
    return query

ael_variables = [['settlements', 'Settlements to Preview', 'FSettlement',
                  None, CreateSettlementQuery(), 0, 1, ''],
                 ['confirmations', 'Confirmations to Preview', 'FConfirmation',
                  None, CreateConfirmationQuery(), 0, 1, '']]

def ael_main(dictionary):
    try:
        if dictionary.get('settlements'):
            PreviewSettlementsXMLs(dictionary.get('settlements'))
        if dictionary.get('confirmations'):
            PreviewConfirmationsXMLs(dictionary.get('confirmations'))
    except SwiftWriterAPIException as e:
        Utils.LogAlways('Error generating XML(s): {}'.format(e))

