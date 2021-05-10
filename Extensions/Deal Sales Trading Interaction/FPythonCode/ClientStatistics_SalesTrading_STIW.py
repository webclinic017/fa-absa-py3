import acm


from ClientStatistics_SalesTrading import ClientStatistics


class ClientStatistics_STIW(ClientStatistics):
    
    '''********************************************************************
    * Layout
    ********************************************************************'''                    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_ClientStatistics_STIW")
