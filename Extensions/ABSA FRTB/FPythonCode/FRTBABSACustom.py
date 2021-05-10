
def BankLevel(portfolio):
    bank_level = "Front Arena"
    
    return bank_level
    
def BookNode(portfolio):
    bank_level = BankLevel(portfolio)
    oid        = portfolio.Oid()
    book_node  = bank_level + "_" + str(oid)
    
    return book_node
