'''--------------------------------------------------------------------------------------
MODULE
    Hedge_relationship_type_filter

DESCRIPTION
    Date                : 2020-03-24
    Purpose             : There are 4 types of hedge relationships, Cash Flow, Fair Value AFS, Fair Value AC and Net Investment. 
                          This detail is stored in text objects which this code will retrieve to then be filtered by for reporting purposes
    Department and Desk : PCG Group Treasury
    Requester           : James Moodie
    Developer           : Khaya Mbebe
    JIRA                : PCGDEV-219

HISTORY
=========================================================================================
Date            JIRA no                 Developer               Description
-----------------------------------------------------------------------------------------
2020-03-24     PCGDEV-219               Khaya Mbebe             Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''

import HedgeRelation


def deal_package(textobject, hedgerelationship_name, hedgerelationship_type, *rest):   
    hedgerelationship = HedgeRelation.HedgeRelation(hedgerelationship_name)
    hedgerelationship.read()
    

    if hedgerelationship.get_type() == hedgerelationship_type:
        return 1
    return 0
