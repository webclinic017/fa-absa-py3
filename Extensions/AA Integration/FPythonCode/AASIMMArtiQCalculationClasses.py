""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASIMMArtiQCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASIMMArtiQCalculationClasses - Performer class for performing AA SIMM data
        calculation.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AASIMMCalculationClasses
import importlib
importlib.reload(AASIMMCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)

class CommonArtiQCalculation(AASIMMCalculationClasses.CommonCalculation):
    def _getCatalogName(self):
        return self._cube_catalog[0]

    def _getCubeName(self):
        return self._cube_name[0]
        
class ArtiQSIMMCalculation(
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

class ArtiQStoreSIMMCalculation(
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


CLASSES = AASIMMCalculationClasses.Manager.getAllCalculationClasses(
    manager=AASIMMCalculationClasses.Manager, callee_module_attrs=globals()
)
