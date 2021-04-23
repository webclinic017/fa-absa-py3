""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAPLRatesArtiQCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AAPLRatesArtiQCalculationClasses - Performer class for performing PL Rates External
        calculation.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AAPLRatesCalculationClasses
import importlib
importlib.reload(AAPLRatesCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)

class CommonArtiQCalculation(AAPLRatesCalculationClasses.CommonCalculation):
    def _getCatalogName(self):
        return self._cube_catalog[0]

    def _getCubeName(self):
        return self._cube_name[0]
        
class ArtiQPLRatesCalculation(
    CommonArtiQCalculation, AACalculationBase.ArtiQCalculationBase
):
    def __init__(
        self, dictionary
    ):
        AACalculationBase.ArtiQCalculationBase.__init__(
            self, dictionary
        )
        CommonArtiQCalculation.__init__(
            self, dictionary
        )

class ArtiQStorePLRatesCalculation(
    CommonArtiQCalculation, AACalculationBase.ArtiQStoreCalculationBase
):
    def __init__(
        self, dictionary
    ):
        AACalculationBase.ArtiQStoreCalculationBase.__init__(
            self, dictionary
        )
        CommonArtiQCalculation.__init__(
            self, dictionary
        )


CLASSES = AAPLRatesCalculationClasses.Manager.getAllCalculationClasses(
    manager=AAPLRatesCalculationClasses.Manager, callee_module_attrs=globals()
)
