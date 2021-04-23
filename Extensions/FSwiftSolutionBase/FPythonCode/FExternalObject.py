"""----------------------------------------------------------------------------
MODULE:
    FExternalObject

DESCRIPTION:
    Wraparound to simplify external object storage in the ADS. The idea is to
    use existing tables in 2016.2, and then possibly add read tables for
    external objects in 2016.4.

FUNCTIONS:
    Derived classes from this class implements following methods.
    Read():
        Read the existing FExternalObject from database using its Oid().
    New():
        Creates a new FExternalObject.
    Commit():
        Commits the FExternalObject in the database.
    Delete():
        Deletes the FExternalObject from the database.
    pp():
        Prints the details of created / Committed FExternalObject
    ExtType():
        Get and Set FExternalObject Type.
    Subject():
        Set or Get ACM object for which the FExternalObject is created.
    SubjectType():
        Get and Set type of ACM object like FInstrument, FTrade.
    SubType():
        Get and Set the sub message type for ExternalObject like "MT545".
        Possible values in extendable ChoiceList XOBJextType
    Data():
        Get and Set data to the FExternalObject.
    DataSize():
        Get method for fetching size of data in FExternalObject.
    StorageType():
        Get and Set the type of data to store in FExternalObject like
        "PythonDict", "TXT" etc. Possible values in extendable ChoiceList
        XOBJstorageType
    Source():
        Get and Set the source of the data stored in the FExternalObject,
        a string like the AMB message ID, file name, etc.
    SourceType():
        Get and Set the type of the External source id like "ISIN", or
        "CustodianID" of the FExternalObject. Possible values in extendable
        ChoiceList XOBJsourceType
    ReconciliationDocument():
        Get and Set the ReconciliationDocument to created FExternalObject.
    ReconciliationItem():
        Get and Set the ReconciliationItem linked to FExternalObject
    Oid():
        Get unique oid for created FExternalObject.
    ExtReferences(sourceKey=None, subject=None, extType=None, sourceType=None,
        subtype=None, subjectType=None):
        Get the external item based on the search criteria.
    GetExtObjectFromReconItem(rItem=None):
        Get FExternalObject object from given ReconciliationItem

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

