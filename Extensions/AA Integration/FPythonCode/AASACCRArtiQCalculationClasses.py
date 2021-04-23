""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASACCRArtiQCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASACCRArtiQCalculationClasses - Performer class for performing AA SA-CCR data
        calculation.

    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AASACCRCalculationClasses
import importlib
importlib.reload(AASACCRCalculationClasses)
import AACalculationBase
importlib.reload(AACalculationBase)

class CommonArtiQCalculation(AASACCRCalculationClasses.CommonCalculation):
    def _getCatalogName(self):
        return 'SACCR'

class ArtiQSACCRCalculation(
    CommonArtiQCalculation, AACalculationBase.ArtiQCalculationBase
):
    def __init__(self, dictionary):
        AACalculationBase.ArtiQCalculationBase.__init__(
            self, dictionary
        )
        CommonArtiQCalculation.__init__(
            self, dictionary)


class ArtiQStoreSACCRCalculation(
    CommonArtiQCalculation, AACalculationBase.ArtiQStoreCalculationBase
):
    def __init__(
        self, market_data_path, deals_path,
        rate_fixings_path, currency, ref_date
    ):
        AACalculationBase.ArtiQStoreCalculationBase.__init__(
            self, base_date=ref_date
        )
        CommonArtiQCalculation.__init__(
            self,
            market_data_path=market_data_path,
            deals_path=deals_path,
            rate_fixings_path=rate_fixings_path,
            currency=currency
        )

CLASSES = AASACCRCalculationClasses.Manager.getAllCalculationClasses(
    manager=AASACCRCalculationClasses.Manager, callee_module_attrs=globals()
)
