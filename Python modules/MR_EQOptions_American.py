'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 707888

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    PositionFilename    = FileDir + PositionName
    
    outfileP            =  open(PositionFilename, 'w')
    
    outfileP.close()

    return PositionFilename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(t,FileDir,Filename,PositionName,*rest):
    
    #The instruments are creatyed by the ASQL called MR_EQOptions_American_Inst
    PositionFilename    = FileDir + PositionName
    
    #Position
    if MR_MainFunctions.ValidTradeNo(t) == 0:
        if MR_MainFunctions.IsExcludedPortfolio(t) == False:
            PositionFile.CreatePosition(t, PositionFilename)
    
    return 'TradeCreated'

# WRITE - FILE ######################################################################################################


