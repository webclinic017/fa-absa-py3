""" AggregationArchiving:2.0.1 """

"""----------------------------------------------------------------------------
MODULE
    FAggregation - Perform aggregation

    (c) Copyright 2002 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        This module perform trade aggregation in a ARENA Database. It reads
        configuration information from the AggregationSpec and AggregationRule
        tables and the aggregation rules must have been set up before the
        aggregation can be performed.

NOTE    
    The modules uses the aggregation rules set up in the Aggregation
    Specification application.


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import ael

ael_variables = []

def ael_main(dictionary):

    ael.log("Started aggregation")

    ael.aggregate(ael.date_today())

    ael.log("Finished aggregation")



