"""----------------------------------------------------------------------------

----------------------------------------------------------------------------"""
import acm
from FValidation_core import show_validation_warning

MAPPINGS = {
    "NO_ORIGINAL_LOAN_REF": { "code" : 130,
                               "description" : "No original loan reference."
        
    },
    "NO_CP_ACC_NO": { "code" : 130,
                       "description" : "No counter party account."
        
    },
    "NO_STRATE_POOL_REF": { "code" : 130,
                             "description" : "No STRATE pool reference."
        
    },
    "NO_CP": { "code" : 130,
                "description" : "No counterparty."
        
    },
    "NO_CUSTODIAN": { "code" : 130,
                       "description" : "Custodian not set."
        
    },
    "NO_ACQUIRERS_BP_ID":  { "code" : 130,
                                "description" : "No Aqcuirers BP ID."
        
    },
    "NO_SENDERS_BIC": { "code" : 130,
                           "description" : "No senders BIC."
        
    },
    "NO_RECEIVER_BIC": { "code" : 130,
                            "description" : "No receiver BIC."
        
    },
}

class FSwiftMessageValidation(Exception):
    def __init__(self, settlement, flag):
        self.flag = flag
        self.settlement = settlement
        self.updateInvalidSettlement()
        
    def __str__(self):
        return repr(MAPPINGS[self.flag]["description"])
        
    def updateInvalidSettlement(self):
        validationData = MAPPINGS.get(self.flag, "")
        statusCode = validationData["code"]
        statusDescription = validationData["description"]
        
        settlementSI = self.settlement.StorageImage()
        settlementSI.Status('Hold')
        settlementSI.StatusExplanation(statusCode)
        settlementSI.Commit()
        
        show_validation_warning("""SWIFT message generation failed\n\n
    %s\n\n
Settlement %s set to Hold status\n""" % (statusDescription, self.settlement.Oid()), popup=True)
