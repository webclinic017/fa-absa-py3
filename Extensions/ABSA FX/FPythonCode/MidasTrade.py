class MidasTrade():
    def __init__(self):
        self.__dealNo = None
        self.__status = None
        self.__rate = None
        self.__buyAmount = None
        self.__buyCurrency = None
        self.__sellAmount = None
        self.__sellCurrency = None
        self.__desk = None
        
    @property
    def dealNo(self):
        return self.__dealNo

    @dealNo.setter
    def dealNo(self, value):
        self.__dealNo = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        
    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, value):
        self.__rate = value
        
    @property
    def buyAmount(self):
        return self.__buyAmount

    @buyAmount.setter
    def buyAmount(self, value):
        self.__buyAmount = value
        
    @property
    def buyCurrency(self):
        return self.__buyCurrency

    @buyCurrency.setter
    def buyCurrency(self, value):
        self.__buyCurrency = value
        
    @property
    def sellAmount(self):
        return self.__sellAmount

    @sellAmount.setter
    def sellAmount(self, value):
        self.__sellAmount = value
        
    @property
    def sellCurrency(self):
        return self.__sellCurrency

    @sellCurrency.setter
    def sellCurrency(self, value):
        self.__sellCurrency = value
        
    @property
    def desk(self):
        return self.__desk

    @desk.setter
    def desk(self, value):
        self.__desk = value
