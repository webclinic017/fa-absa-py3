"""----------------------------------------------------------------------------
MODULE
    FYieldCurveUpdateVariables - Module containing variables to the 
    FYieldCurveUpdate module.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

# List of yield curves to update
yield_curves = ['FRD_EUR_SWAP', 'FRD_INS_SPREAD', 'CE_ISSUER_SPREAD', 'ANY-EUR-SWAP']

# Epsilon, if changes are smaller than this the yield curves will not be updated
#instrument spread curves
epsilon = 0.05
# all other curves
epsilon2 = 0.005
