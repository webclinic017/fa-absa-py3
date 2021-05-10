"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterUtils_Override

DESCRIPTION:
    FSwiftWriterUtils is an encrypted core module. This module is created to override some of the functions in the
    core module. The overrides in this module should be evaluated with each upgrade to determine whether they are
    still required.
    
------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-02-23      FAOPS-1034      Willie vd Bank          Martin Wortmann         Updated FSwiftWriterUtils_Override to
                                                                                limit the field length
------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------"""
import acm


def allocate_space_for_name_and_address_with_constraint(name=[], address=[], address_details=[]):
    """
    This api does following:
        Step1: Allocates number of lines based on the prefix
        Step2: Takes required data from corresponding lists as per allocated space
    """
    str_prefix_1_len = len(name)
    str_prefix_2_len = len(address)
    str_prefix_3_len = len(address_details)
    space_for_1, space_for_2, space_for_3 = 0, 0, 0
    if str_prefix_1_len >= 1:
        # Condition: Number 2 must not be used without number 3
        if str_prefix_2_len >= 1 and str_prefix_3_len >= 1:
            # Numbers must appear in numerical order
            if str_prefix_1_len > 1:
                space_for_1 = min(3, str_prefix_1_len)  # Condition:The first line must start with number 1
                rem_space = 4 - space_for_1
                if rem_space == 2:
                    space_for_2, space_for_3 = 1, 1
                else:
                    space_for_2, space_for_3 = 0, 1
            else:
                space_for_1, space_for_2 = 1, min(str_prefix_2_len, 2)
                space_for_3 = 3 - space_for_2
        else:
            space_for_1, space_for_2, space_for_3 = min(4, str_prefix_1_len), 0, 4 - min(4, str_prefix_1_len)
    field_value = name[:space_for_1] + address[:space_for_2] + address_details[:space_for_3]
    name_address = ('\n').join(field_value)
    return name_address
