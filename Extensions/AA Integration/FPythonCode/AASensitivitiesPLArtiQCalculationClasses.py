""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASensitivitiesPLArtiQCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASensitivitiesPLArtiQCalculationClasses - Performer class for performing Sensitivity PL External
        calculation.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AASensitivitiesPLCalculationClasses
import importlib
importlib.reload(AASensitivitiesPLCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)

class CommonArtiQCalculation(AASensitivitiesPLCalculationClasses.CommonCalculation):
    def _getCatalogName(self):
        return self._cube_catalog[0]

    def _getCubeName(self):
        return self._cube_name[0]
        
class ArtiQSensitivitiesPLCalculation(
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

class ArtiQStoreSensitivitiesPLCalculation(
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


CLASSES = AASensitivitiesPLCalculationClasses.Manager.getAllCalculationClasses(
    manager=AASensitivitiesPLCalculationClasses.Manager, callee_module_attrs=globals()
)
