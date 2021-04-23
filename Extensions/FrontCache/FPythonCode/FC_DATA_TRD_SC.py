
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_SC
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for trade sales credit data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
#*********************************************************#
#Static Creator method for all sales credits of a trade (not use self)
#*********************************************************#

def CreateAllForTrade(trade):
    if not trade:
        raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)
    
    #no of sales credits
    noOfSalesCredits = 5
    
    #results list
    salesCredits = []
    
    
    #Grab the first (built-in) sales credit
    salesPersonName = ''
    standardSalesCredit=None
    totalValueAddSalesCredit=None
    salesCreditSubTeamName=''
    dataErrors={}
    #1st Sales person
    try:
        if trade.SalesPerson():
            salesPersonName = trade.SalesPerson().Name()
            #1st Sales credit
            try:
                if trade.SalesCredit():
                    standardSalesCredit = FC_UTILS.formatNumber(trade.SalesCredit())
                else:
                    standardSalesCredit = FC_UTILS.formatNumber(0)
            except Exception, e:
                dataErrors[UTILS.Constants.fcGenericConstants.STANDARD_SALES_CREDIT] = str(e)
            #1st Value add sales credit
            try:
                totalValueAddAddInfo = trade.add_info(UTILS.Constants.fcGenericConstants.VALUEADDCREDITS)
                if totalValueAddAddInfo and str(totalValueAddAddInfo)!='':
                    totalValueAddSalesCredit = FC_UTILS.formatNumber(float(totalValueAddAddInfo))
                else:
                    totalValueAddSalesCredit = FC_UTILS.formatNumber(0)
            except Exception, e:
                dataErrors[UTILS.Constants.fcGenericConstants.TOTAL_VALUE_ADD_SALES_CREDIT] = str(e)
            #1st sales credit sub team
            try:
                salesCreditSubTeamAddInfo = trade.add_info(UTILS.Constants.fcGenericConstants.SALESCREDITSUBTEAM1)
                if salesCreditSubTeamAddInfo and str(salesCreditSubTeamAddInfo)!='':
                    salesCreditSubTeamName = salesCreditSubTeamAddInfo
            except Exception, e:
                dataErrors[UTILS.Constants.fcGenericConstants.SALESCREDITSUBTEAM] = str(e)


            #Create the first sales credit
            salesCredit = FC_DATA_TRD_SC(salesPersonName, standardSalesCredit, totalValueAddSalesCredit, salesCreditSubTeamName, dataErrors)
            #Add the first sales credit entity to the collection
            salesCredits.append(salesCredit)
    except Exception, e:
        dataErrors[UTILS.Constants.fcGenericConstants.SALES_PERSON] = str(e)

    #Now go for the remainder of the sales credits (all add infos)
    salesCreditNo = 2
    while salesCreditNo <= noOfSalesCredits:

        #grab sales person and standard sales credit add infos to see if the sales credit must be created
        salesPersonName = None
        standardSalesCredit=None
        totalValueAddSalesCredit=None
        salesCreditSubTeamName=None
        dataErrors={}
        #next Sales person
        try:
            salesPersonAddInfo = trade.add_info(UTILS.Constants.fcGenericConstants.SALES_PERSON_S % salesCreditNo)
            if salesPersonAddInfo and str(salesPersonAddInfo)!='':
                salesPersonName = salesPersonAddInfo
                #next Sales credit
                try:
                    standardSalesCreditAddInfo = trade.add_info(UTILS.Constants.fcGenericConstants.SALES_CREDIT_S % salesCreditNo)
                    if standardSalesCreditAddInfo and str(standardSalesCreditAddInfo)!='':
                        standardSalesCredit = FC_UTILS.formatNumber(float(standardSalesCreditAddInfo))
                    else:
                        standardSalesCredit = FC_UTILS.formatNumber(0)
                except Exception, e:
                    dataErrors[UTILS.Constants.fcGenericConstants.STANDARD_SALES_CREDIT] = str(e)
                #next Value add sales credit
                try:
                    totalValueAddAddInfo = trade.add_info(UTILS.Constants.fcGenericConstants.VALUE_ADD_CREDITS_S % salesCreditNo)
                    if totalValueAddAddInfo and str(totalValueAddAddInfo)!='':
                        totalValueAddSalesCredit = FC_UTILS.formatNumber(float(totalValueAddAddInfo))
                    else:
                        totalValueAddSalesCredit = FC_UTILS.formatNumber(0)
                except Exception, e:
                    dataErrors[UTILS.Constants.fcGenericConstants.TOTAL_VALUE_ADD_SALES_CREDIT] = str(e)
                #1st sales credit sub team
                try:
                    salesCreditSubTeamAddInfo = trade.add_info(UTILS.Constants.fcGenericConstants.SALES_CREDIT_SUB_TEAM_S % salesCreditNo)
                    if salesCreditSubTeamAddInfo and str(salesCreditSubTeamAddInfo)!='':
                        salesCreditSubTeamName = salesCreditSubTeamAddInfo
                except Exception, e:
                    dataErrors[UTILS.Constants.fcGenericConstants.SALES_CREDIT_SUB_TEAM] = str(e)


                #Create the next sales credit
                salesCredit = FC_DATA_TRD_SC(salesPersonName, standardSalesCredit, totalValueAddSalesCredit, salesCreditSubTeamName, dataErrors)
                #Add the next sales credit entity to the collection
                salesCredits.append(salesCredit)
        except Exception, e:
            dataErrors[UTILS.Constants.fcGenericConstants.SALES_PERSON] = str(e)

        salesCreditNo = salesCreditNo + 1

    return salesCredits


#*********************************************************#
#Class definition
#*********************************************************#
class FC_DATA_TRD_SC(): 
    
    #**********************************************************#
    #Properties
    #*********************************************************#
    #SalesPersonName
    @property
    def SalesPersonName(self):
        return self._salesPersonName
    
    @SalesPersonName.setter
    def SalesPersonName(self, value):
        self._salesPersonName = value 
        
    #StandardSalesCredit
    @property
    def StandardSalesCredit(self):
        return self._standardSalesCredit
    
    @StandardSalesCredit.setter
    def StandardSalesCredit(self, value):
        self._standardSalesCredit = value   
        
    #TotalValueAddSalesCredit
    @property
    def TotalValueAddSalesCredit(self):
        return self._totalValueAddSalesCredit
    
    @TotalValueAddSalesCredit.setter
    def TotalValueAddSalesCredit(self, value):
        self._totalValueAddSalesCredit = value
        
    #SalesCreditSubTeamName
    @property
    def SalesCreditSubTeamName(self):
        return self._salesCreditSubTeamName
    
    @SalesCreditSubTeamName.setter
    def SalesCreditSubTeamName(self, value):
        self._salesCreditSubTeamName = value
    
    #CalculationResults
    @property
    def CalculationResults(self):
        return self._calculationResults 

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors
    
    #SerializedCalculationResults
    @property
    def SerializedCalculationResults(self):
        return self._serializedCalculationResults 
        
    #SerializedCalculationErrors
    @property
    def SerializedCalculationErrors(self):
        return self._serializedCalculationErrors
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, salesPersonName, standardSalesCredit, totalValueAddSalesCredit, salesCreditSubTeamName, calcErrors):
        self._salesPersonName = salesPersonName
        self._standardSalesCredit = standardSalesCredit
        self._totalValueAddSalesCredit = totalValueAddSalesCredit
        self._salesCreditSubTeamName = salesCreditSubTeamName
        self._calculationErrors = calcErrors
        self._calculationResults=None
        self._serializedCalculationResults  = None
        self._serializedCalculationErrors = None
        
    
    #*********************************************************#
    #Methods
    #*********************************************************#
    def Calculate(self):
        self._calculationResults = {}
        if self.SalesPersonName is not None and self.SalesPersonName != '':
            self._calculationResults[UTILS.Constants.fcGenericConstants.SALES_PERSON_NAME]= self.SalesPersonName
        if self.StandardSalesCredit is not None and self.StandardSalesCredit != '':
            self._calculationResults[UTILS.Constants.fcGenericConstants.STANDARD_SALES_CREDIT]= self.StandardSalesCredit
        if self.TotalValueAddSalesCredit is not None and self.TotalValueAddSalesCredit != '':
            self._calculationResults[UTILS.Constants.fcGenericConstants.TOTAL_VALUE_ADD_SALES_CREDIT]= self.TotalValueAddSalesCredit
        if self.SalesCreditSubTeamName is not None and self.SalesCreditSubTeamName != '':
            self._calculationResults[UTILS.Constants.fcGenericConstants.SALES_CREDIT_SUB_TEAM_NAME]= self.SalesCreditSubTeamName

        
    #Serialize the calculation results
    def SerializeCalculationResults(self, serializationType):
        try:
            self._serializedCalculationResults = FC_UTILS.SerializeDictionary(serializationType, UTILS.Constants.fcGenericConstants.CALCULATION_RESULTS, self.CalculationResults)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_SERIALIZE_THE_CALC_RESULT % str(e))
    
    #Serialize the calculation errors
    def SerializeCalculationErrors(self, serializationType):
        try:
            self._serializedCalculationErrors = FC_UTILS.SerializeDictionary(serializationType, UTILS.Constants.fcGenericConstants.CALCULATION_ERRORS, self.CalculationErrors)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_SERIALIZE_THE_CALC_RESULT % str(e))
            
    
    
            
   
        

