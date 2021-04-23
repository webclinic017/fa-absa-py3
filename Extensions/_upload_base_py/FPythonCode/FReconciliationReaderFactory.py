""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationReaderFactory.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationReaderFactory

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import FAssetManagementUtils
import FBusinessDataImportHook

logger = FAssetManagementUtils.GetLogger()

def _ParseCSVReconciliationDocument(fp):
    """Function for parsing reconciliation documents in CSV format."""
    import csv
    try:
        sniffedDialect = csv.Sniffer().sniff(fp.read(4012), ',;:\t|.')
    except csv.Error:
        sniffedDialect = csv.excel
    fp.seek(0)
    reader = csv.DictReader(fp, dialect=sniffedDialect)
    for row in reader:
        yield dict((k.strip(), v.strip()) for k, v in row.items())

def GetReconciliationDocumentReader(readerType, parserHook):
    """ Given a reader type and a parser hook string, determine the reader function to use
    and return it. If the reader cannot be determined, raise a ValueError. """
    
    if readerType == 'CSV':
        return _ParseCSVReconciliationDocument
    elif readerType == 'Custom':
        if parserHook and isinstance(parserHook, str):
            return FBusinessDataImportHook.FBusinessDataImportHook(parserHook)
        else:
            raise ValueError("Custom file format requires a file format hook")
    else:
        return _ParseCSVReconciliationDocument
