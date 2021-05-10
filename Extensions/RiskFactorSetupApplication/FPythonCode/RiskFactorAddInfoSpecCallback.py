import acm

# Callback hook that will be called from the Risk Factor Setup Applications 
# context menu (Custom Value) in the Risk Factors list

def CustomValue(riskFactorInstance, addInfoSpec) :
    value = None
    if str(addInfoSpec.Name()) == 'External Id' :
        value = riskFactorInstance.StringKey()

    return value
