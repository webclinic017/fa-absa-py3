'''
Date                    : 2010-03-30
Purpose                 : Python code to check if string contains a certain substring. (Used to test for DivSwaps)
Department and Desk     : FO Eq Arb Trader
Requester               : Brad Stransky
Developer               : Rohan van der Walt
CR Number               : 269463
'''
def contains(s, sub_str, case_sensitive=False):
    if case_sensitive:
        return str(sub_str) in str(s)
    else:
        return str(sub_str).lower() in str(s).lower()
