""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAFileImportArtiQCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AAFileImportArtiQCalculationClasses - Performer class for performing AA CSV import file data
        calculation.

    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AAFileImportCalculationClasses
import importlib
importlib.reload(AAFileImportCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)

class CommonArtiQCalculation(AAFileImportCalculationClasses.CommonCalculation):

    def _getCatalogName(self):
        return self._cube_catalog[0]

    def _getCubeName(self):
        return self._cube_name[0]
        
class ArtiQCSVImportCalculation(CommonArtiQCalculation, AACalculationBase.ArtiQCalculationBase):

    def __init__(self, dictionary):
        AACalculationBase.ArtiQCalculationBase.__init__(self, dictionary)
        CommonArtiQCalculation.__init__(self, dictionary)

class ArtiQStoreCSVImportCalculation(CommonArtiQCalculation, AACalculationBase.ArtiQStoreCalculationBase):

    def __init__(self, dictionary):
        AACalculationBase.ArtiQStoreCalculationBase.__init__(self, dictionary)
        CommonArtiQCalculation.__init__(self, dictionary)


CLASSES = AAFileImportCalculationClasses.Manager.getAllCalculationClasses(
    manager=AAFileImportCalculationClasses.Manager, callee_module_attrs=globals()
)
