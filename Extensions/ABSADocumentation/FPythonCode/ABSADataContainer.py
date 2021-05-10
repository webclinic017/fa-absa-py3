""" Compiled: NONE NONE """

class ABSADataContainer(object):
    import acm
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    #TRX nbr
    TRXNumber = 0
    @staticmethod
    def GetTRXNumber():
        return ABSADataContainer.TRXNumber

    @staticmethod
    def SetTRXNumber(number):
        ABSADataContainer.TRXNumber = number
    
    #Confirmation
    Confirmation = 0
    @staticmethod
    def GetConfirmation():
        return ABSADataContainer.Confirmation

    @staticmethod
    def SetConfirmation(object):
        ABSADataContainer.Confirmation = object
    
    #Operations Document
    OperationsDocument = 0
    @staticmethod
    def GetDocument():
        return ABSADataContainer.OperationsDocument

    @staticmethod
    def SetDocument(object):
        ABSADataContainer.OperationsDocument = object
    
    #Calculation Space
    @staticmethod
    def GetCalculationSpace():
        return ABSADataContainer.calcSpace
