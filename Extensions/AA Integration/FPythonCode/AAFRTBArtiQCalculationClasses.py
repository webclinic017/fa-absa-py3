""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAFRTBArtiQCalculationClasses.py"
from __future__ import print_function
import importlib
"""----------------------------------------------------------------------------
MODULE
    AAFRTBArtiQCalculationClasses - Performer class for performing AA FRTB data
        calculation.

    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AAFRTBCalculationClasses
importlib.reload(AAFRTBCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)
import AAIntegrationUtility
import FBDPCommon

class CommonArtiQCalculationBase(AAFRTBCalculationClasses.CommonCalculationBase):
    def __init__(self, dictionary):
        AAFRTBCalculationClasses.CommonCalculationBase.__init__(self, dictionary)

    def _getCatalogName(self):
        return 'Market Risk'
        #return 'Front Arena'
    
    def getDirPath(self, dictionary):
        print('getDirPath')
        return self._getFolderName(dictionary)
    
    def _getFolderName(self, dictionary):
        print('getfoldername')
        if self._INPUT_PATH_VARIABLE:
            print(dictionary[self._INPUT_PATH_VARIABLE])
            return dictionary[self._INPUT_PATH_VARIABLE]
        else:
            return None

class ArtiQCalculationBase(
    CommonArtiQCalculationBase, AACalculationBase.ArtiQCalculationBase
):
    def __init__(self, dictionary):
        AACalculationBase.ArtiQCalculationBase.__init__(self, dictionary)
        CommonArtiQCalculationBase.__init__(self, dictionary)

class ArtiQStoreCalculationBase(
    CommonArtiQCalculationBase, AACalculationBase.ArtiQStoreCalculationBase
):
    def __init__(self, dictionary):
        AACalculationBase.ArtiQStoreCalculationBase.__init__(self, dictionary)
        CommonArtiQCalculationBase.__init__(self, dictionary)

### SA SBA
class ArtiQSASBACalculation(
    AAFRTBCalculationClasses.CommonSASBACalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreSASBACalculation(
    AAFRTBCalculationClasses.CommonSASBACalculation,
    ArtiQStoreCalculationBase
):
    pass

### SA DRC
class ArtiQSADRCCalculation(
    AAFRTBCalculationClasses.CommonSADRCCalculation,
    ArtiQCalculationBase
):
    pass
    
class ArtiQStoreSADRCCalculation(
    AAFRTBCalculationClasses.CommonSADRCCalculation,
    ArtiQStoreCalculationBase
):
    pass

### SA RRAO
class ArtiQSARRAOCalculation(
    AAFRTBCalculationClasses.CommonSARRAOCalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreSARRAOCalculation(
    AAFRTBCalculationClasses.CommonSARRAOCalculation,
    ArtiQStoreCalculationBase
):
    pass

### IMA ES
class ArtiQIMAESCalculation(
    AAFRTBCalculationClasses.CommonIMAESCalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreIMAESCalculation(
    AAFRTBCalculationClasses.CommonIMAESCalculation,
    ArtiQStoreCalculationBase
):
    pass

### IMA SES
class ArtiQIMASESCalculation(
    AAFRTBCalculationClasses.CommonIMASESCalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreIMASESCalculation(
    AAFRTBCalculationClasses.CommonIMASESCalculation,
    ArtiQStoreCalculationBase
):
    pass

### IMA DRC
class ArtiQIMADRCCalculation(
    AAFRTBCalculationClasses.CommonIMADRCCalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreIMADRCCalculation(
    AAFRTBCalculationClasses.CommonIMADRCCalculation,
    ArtiQStoreCalculationBase
):
    pass

### IMA Hyp PL
class ArtiQIMAHypotheticalPLCalculation(
    AAFRTBCalculationClasses.CommonIMAHypotheticalPLCalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreIMAHypotheticalPLCalculation(
    AAFRTBCalculationClasses.CommonIMAHypotheticalPLCalculation,
    ArtiQStoreCalculationBase
):
    pass

### IMA Risk PL
class ArtiQIMARiskTheoreticalPLCalculation(
    AAFRTBCalculationClasses.CommonIMARiskTheoreticalPLCalculation,
    ArtiQCalculationBase
):
    pass

class ArtiQStoreIMARiskTheoreticalPLCalculation(
    AAFRTBCalculationClasses.CommonIMARiskTheoreticalPLCalculation,
    ArtiQStoreCalculationBase
):
    pass

### All External
class ArtiQFRTBAllCalculation(
    AAFRTBCalculationClasses.CommonFRTBAllCalculation,
    ArtiQCalculationBase
):
    def __init__(self, dictionary):
        ArtiQCalculationBase.__init__(self, dictionary)
        ext = dictionary['Extension']
        self._ext = ext.lower()
        self._dictionary = dictionary
        self._base_date = AAIntegrationUtility.getAAFormattedDate(date=FBDPCommon.toDate(dictionary.get('RefDate')))

class ArtiQStoreFRTBAllCalculation(
    AAFRTBCalculationClasses.CommonFRTBAllCalculation,
    ArtiQStoreCalculationBase
):
    def __init__(self, dictionary):
        ArtiQStoreCalculationBase.__init__(self, dictionary)
        ext = dictionary['Extension']
        self._ext = ext.lower()
        self._dictionary = dictionary
        self._base_date = AAIntegrationUtility.getAAFormattedDate(date=FBDPCommon.toDate(dictionary.get('RefDate')))

CLASSES = AAFRTBCalculationClasses.Manager.getAllCalculationClasses(
    manager=AAFRTBCalculationClasses.Manager, callee_module_attrs=globals()
)
