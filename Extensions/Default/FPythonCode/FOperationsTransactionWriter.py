""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTransactionWriter.py"

from FOperationsWriter import Writer

#-------------------------------------------------------------------------
class TransactionWriter(Writer):

    #-------------------------------------------------------------------------
    def __init__(self, committerIF, modifierIF):
        self.__committerIF = committerIF
        self.__modifierIF = modifierIF
        self.__transactionSet = set()
        self.__provider = None

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__committerIF.PO_Init(provider)
        self.__modifierIF.PO_Init(provider)
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__transactionSet.clear()
        self.__committerIF.PO_Clear()
        self.__modifierIF.PO_Clear()

    #-------------------------------------------------------------------------
    def WR_CreateResult(self):
        self.PO_Clear()
        return self.__committerIF.CO_CreateResult()

    #-------------------------------------------------------------------------
    def WR_AddItem(self, op, obj):        
        self.__transactionSet.add((op, obj))

    #-------------------------------------------------------------------------
    def WR_Commit(self):
        preparedTransaction = self.__modifierIF.MO_Prepare(self.__transactionSet)
        result = self.__committerIF.CO_Commit(preparedTransaction)
        self.PO_Clear()
        
        return result