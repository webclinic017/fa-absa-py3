""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASensitivitiesArtiQCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASensitivityArtiQCalculationClasses - Performer class for performing Sensitivity External
        calculation.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AASensitivitiesCalculationClasses
import importlib
importlib.reload(AASensitivitiesCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)

class CommonArtiQCalculation(AASensitivitiesCalculationClasses.CommonCalculation):
    def _getCatalogName(self):
        return self._cube_catalog[0]

    def _getCubeName(self):
        return self._cube_name[0]
        
class ArtiQSensitivitiesCalculation(
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

class ArtiQStoreSensitivitiesCalculation(
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


CLASSES = AASensitivitiesCalculationClasses.Manager.getAllCalculationClasses(
    manager=AASensitivitiesCalculationClasses.Manager, callee_module_attrs=globals()
)
