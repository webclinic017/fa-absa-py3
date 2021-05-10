import acm
def openSelectDeliverables( invokationInfo ):
    instruments = invokationInfo.ExtensionObject()
    for instrument in instruments:
        acm.StartApplication( "Select Deliverables", instrument )
