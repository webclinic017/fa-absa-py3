#the reporting conversion

#
#Compressed XML documents may interfere with this
#

Version = "Version 2009-09-28 reporting2T4Conv"

import ael

import FLogger
     
VERBOSITY = 2
     
logger = FLogger.FLogger()
#should display everything
logger.Reinitialize( level=VERBOSITY )

def callflogger(F,X):
        x = ""
        for i in X:
                x = x+" "+str(i)
        F(x)

def dbug(*X):
        #print "DBUG:   \t",
        #for i in X:
        #        print i,
        #print
        callflogger(logger.DLOG,X)

def warning(*X):
        #print "WARNING:\t",
        #for i in X:
        #        print i,
        #print
        callflogger(logger.WLOG,X)

def info(*X):
        #print "INFO:   \t",
        #for i in X:
        #        print i,
        #print
        callflogger(logger.LOG,X)


def getCands(optlist,noold=True):
    """Get available tasks to convert"""
    list = []
    #
    for i in ael.Task:
        if i.module in optlist and (i.name[-4:]!=".old" or noold==False):
            list.append(i.name)
    return list

def getCandsRevert():
    """Get candidates for reverting"""
    l = getCands(['FWorksheetReport'])
    o = getCands(['FPortfolioReport',  'FTradeReport','FRiskMatrix'],False)
    #dbug("getCandsRevert options",o)
    o = [X[:-4] for X in o if X[-4:]==".old"]
    #dbug("getCandsRevert filtered list",o)
    d = {}
    for i in l:
            d[i] = True
    for i in o:
            d[i] = True
    return d.keys()
    

CANDS = []
#getCands()

UCANDS = []

def setUsers():
        """Grab all system users"""
        v = ael.User.select()
        return [str(X.userid) for X in v]

UCANDS= setUsers()
        
def setTheCands(i,c):
        if(c[2]=="Revert to old"):
                dbug("changing cands to old!")
                ael_variables[0][3] = getCandsRevert()
        else:
                dbug("changing cands to new")
                # ['FPortfolioReport',  'FTradeReport','FRiskMatrix', 'FOrderBookReport']
                ael_variables[0][3] = getCands(['FPortfolioReport',  'FTradeReport','FRiskMatrix'])
        return c



ael_variables = [["scripts","Scripts to convert","string",CANDS, \
                "",0,1,"Select tasks to convert"],
                ["users","User that executes script","string",UCANDS, \
                "",0,1,"Select users for tasks"],
                 #["keepold","Keep old","int",[0,1],"0",1,0]
                 ["operation","Operation","string",["Upgrade & Backup",
                                                         "Upgrade",
                                                         "Revert to old"],
                                                         "Upgrade & Backup",1,0,
                                                         "What kind of operation to be used",
                                                         setTheCands],


                  ["prefix","New workbook prefix","string","","F4.",1,0,
                        "prefix of workbooks created during upgrade"],
                  ["atasks","add absa tasks","int",[0,1],"0",1,0]
                ]


#--------------------------------------------------------------------------------------
#
# Static portfolio and user data, will be added as extra parameter
#
#
#--------------------------------------------------------------------------------------

absaTasks = """
QuantoIndex_SERVER        ATS
GM_Justin__SERVER        ATS
GT_Prime_SwapC_SERVER        ATS
GT_Prime_PrimeC_SERVER        ATS
Index_Options_overnight_SERVER        ATS
SEQ_skew_new_volgrid_SERVER        ATS
EQD_PL_IL_0522_SERVER        ATS
EQD_PL_IL_0524_SERVER        ATS
EQD_PL_IL_3016_SERVER        ATS
EQD_PL_IL_SERVER        ATS
EQD_PL_TL_0524_SERVER        ATS
EQD_PL_TL_0522_SERVER        ATS
EQD_PL_TL_3016_SERVER        ATS
EQD_PL_TL_SERVER        ATS
EQD_PL_IL_3016_LT_SERVER        ATS
VarSwap_SERVER        ATS
EQ_PL_DELTA_ONE_SERVER        ATS
Front_To_Front_M_SERVER        ATS
Int_Options_PnL_SERVER        ATS
CMD_PL_TL_SERVER        ATS
CMD_PL_Standard_SERVER        ATS
CMD_PL_Standard_TL_9196_SERVER        ATS
CMD_PL_Standard_TL_9196_2_SERVER        ATS
FX_PL_TL_SERVER        ATS
Africa_Total_FV_0545_SERVER        ATS
Party_Status_ValEnd_Combs_SERVER        ATS
Party_Status_ValEnd_Value_SERVER        ATS
Party_Status_ValEnd_Rest_SERVER        ATS
Party_Status_ValEnd_SW_BND_SERVER        ATS
FXOpts_CashEnd_AFRICA_SERVER        ATS
FXOpts_CashEnd_RND_SERVER        ATS
FXOpts_CashEnd_NLD_SERVER        ATS
FXOpts_TotalPL_AFRICA_SERVER        ATS
FXOpts_TotalPL_RND_SERVER        ATS
FXOpts_TotalPL_NLD_SERVER        ATS
SND_DEPOSIT_REPRICING_TradeSheet_SERVER        ATS
Party_Status_ValEnd_Combs_3PM_SERVER        ATS
Party_Status_ValEnd_Value_3PM_SERVER        ATS
Party_Status_ValEnd_Rest_3PM_SERVER        ATS
Party_Status_ValEnd_SW_BND_3PM_SERVER        ATS
DM_TradesView_CFD_V1_SERVER        ATS
FRONT_PL_PV_SERVER        ATS
DM_CFD_INTELLIMATCH_POS_SERVER        ATS
DM_TRADES_INTELLIMATCH_SERVER        ATS
PCG_TrdPnL_IRD_SWAPS_ALL_2am_SERVER        ATS4
SWIX_MTM_AT3_SERVER        ATSU1
FRONT_PL_COST_SERVER        ATSU1
TMS_UAT_Test_P&L_and_Risk_SERVER        ATSU2
TMS_TrdPnL_UAT_SERVER        ATSU2
TMS_TrdPnL_UAT_OPENonly_SERVER        ATSU2
FX_Tier2_SERVER        ATSU2
HEDG8_Tier2_SERVER        ATSU2
METALS_Base_SERVER        ATSU2
NEWGOLD_Pos_SERVER        ATSU2
METALS_Precious_SERVER        ATSU2
AFDandSunlight_FX_SERVER        ATSU3
MM_Derec_PullToPar_FRN_SERVER        ATSU3
MM_Derec_PullToPar_DEPCD_SERVER        ATSU3
MM_Derec_PullToPar_FRN_TPLD_SERVER        ATSU3
MM_Derec_PullToPar_DEPCD_TPLD_SERVER        ATSU3
AFRICA_Deposits_SERVER        ATSU3
AFRICA_Deposits_Inception_SERVER        ATSU3
Africa_Deposits_Primary_Market_FOY_SERVER        ATSU3
Africa_Deposits_Primary_Market_Inc_SERVER        ATSU3
Africa_FV_Deposits_SERVER        ATSU3
Business_Bank_Trades_SERVER        ATSU3
Call_Balance_Report_SERVER        ATSU3
Call_Balance_Report_YTD_SERVER        ATSU3
MM_Derec_PullToPar_DEPCD_Mid_SERVER        ATSU3
MM_Derec_PullToPar_FRN_Mid_SERVER        ATSU3
PCG_BNDNEW_PNL_IRD_BOND_DERV_NEW_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_BOND_DERV2_NEW_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_BOND_DERV3_NEW_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_BOND_MAN_NEW_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_BOND_MAN2_NEW_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_BOND_DERV_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_BOND_DERV2_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_BOND_DERV3_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_BOND_MAN_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_BOND_MAN2_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_FI_3179_BONDS_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_FI_9808_BONDS_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_FI_3179_BONDS_NEW_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_FI_9808_BONDS_NEW_10pm_SERVER        ATSU4
FI_TradeSheet_Cap_Mkt_Bonds_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_FOREX_SPOT_BONDS_NEW_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_FX_RND_BOND_TRADING_NEW_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_FOREX_SPOT_BONDS_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_FX_RND_BOND_TRADING_10pm_SERVER        ATSU4
PLOpts_Trading_SERVER        ATSU4
FI_BONDS_DETAIL_SERVER        ATSU4
FI_BONDS_ATS_SERVER        ATSU4
TM_Cap_Mkt_Bonds_DRA_SERVER        ATSU4
PCG_FUTNEW_PNL_Africa_Desk_EDFutures_SERVER        ATSU4
PCG_FUTPOS_PNL_Africa_Desk_EDFutures_SERVER        ATSU4
FI_TradeSheet_Cap_Mkt_BSB_SERVER        ATSU4
FX_STIRT_FRA_FLO_SERVER        ATSU4
TM_9808_DRA_SERVER        ATSU4
TM_CM_BSB_SERVER        ATSU4
FI_9808_Not_DRA_ATS_SERVER        ATSU4
TM_9808_Not_DRA_Barclays_SERVER        ATSU4
TM_9808_Not_DRA_SERVER        ATSU4
FI_9808_Not_DRA_DETAIL_SERVER        ATSU4
FI_9808_DRA_DETAIL_SERVER        ATSU4
FI_9808_DRA_ATS_SERVER        ATSU4
FI_TradeSheet_9808_not_DRA_SERVER        ATSU4
FI_BSB_DEP_ATS_SERVER        ATSU4
FI_BSB_DEP_DETAIL_SERVER        ATSU4
PCG_TrdPnL_FI_3179_exBR_2am_SERVER        ATSU4
PCG_TrdPnL_FI_9808_exBR_2am_SERVER        ATSU4
PCG_BNDPOS_PNL_FI_3179_BONDS_2am_SERVER        ATSU4
PCG_BNDPOS_PNL_FI_9808_BONDS_2am_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_PT_BONDS_2am_SERVER        ATSU4
PCG_TrdPnL_Africa_Desk_Trades_2AM_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_FOREX_SPOT_BONDS_2am_SERVER        ATSU4
IRD_TradeSheet-All_Trades_SERVER        ATSU4
TM_JOBX1_Futures_SERVER        ATSU4
GroupFin2_SERVER        ATSU4
FX_STIRT_FRA_TRADING_SERVER        ATSU4
FX_STIRT_FRA_FLO_SERVER        ATSU4
GroupFin_SERVER        ATSU4
TM_3179_Bonds_SERVER        ATSU4
TM_3179_Bonds_Barclays_SERVER        ATSU4
TM_CM_Bonds_SERVER        ATSU4
TM_CM_Bonds_Barclays_SERVER        ATSU4
PCG_TrdPnL_FI_3179_exBR_10pm_SERVER        ATSU4
PCG_TrdPnL_FI_9808_exBR_10pm_SERVER        ATSU4
PCG_BNDPOS_PNL_IRD_PT_BONDS_10pm_SERVER        ATSU4
PCG_BNDNEW_PNL_IRD_PT_BONDS_NEW_10pm_SERVER        ATSU4
PCG_FUTPOS_PNL_FI_Futures_STIRT_SERVER        ATSU4
PCG_FUTNEW_PNL_FI_Futures_STIRT_SERVER        ATSU4
PCG_TrdPnL_Africa_Desk_Trades_10PM_SERVER        ATSU4
PCG_BSBPOS_PNL_FI_3179_BSB_REPOS_10pm_SERVER        ATSU4
PCG_FUTNEW_PNL_FI_Futures_STIRT_SERVER        ATSU4
PCG_FUTPOS_PNL_FI_Futures_STIRT_SERVER        ATSU4
PCG_TrdPnL_IRD_CPI_2am_SERVER        ATSU4
PCG_TrdPnL_IRD_MAN_SWAP_2am_SERVER        ATSU4
PCG_TrdPnL_IRD_CPI_10pm_SERVER        ATSU4
PCG_TrdPnL_IRD_MAN_SWAP_10pm_SERVER        ATSU4
TManager_LandingArea_Fut_Fwd_SERVER        ATSU4
TManager_LandingArea_Options_SERVER        ATSU4
TManager_LandingArea_Combin_SERVER        ATSU4
TManager_LandingArea_FRN_SERVER        ATSU4
TManager_landingArea_Bonds_SERVER        ATSU4
EQ_PL_Equity_Exotics_SERVER        ATSU5
EQ_PL_Arbitrage_Baskets_SERVER        ATSU5
EQ_PL_Catch_All_SERVER        ATSU5
EQ_PL_Equity_Hybrid_Products_SERVER        ATSU5
EQ_PL_Equity_Index_SERVER        ATSU5
EQ_PL_Equity_Structures_SERVER        ATSU5
EQ_PL_Single_Stocks_SERVER        ATSU5
EQ_PL_Linear_Trading_SERVER        ATSU5
EQ_PL_Warrants_SERVER        ATSU5
Cash_Posting_0522CC_SERVER        ATSU5
Cash_Posting_0524CC_SERVER        ATSU5
Cash_Posting_3016CC_SERVER        ATSU5
AN_CMD_PL_SERVER        ATSU5
AN_CMD_ALL_PL_AGG_SERVER        ATSU5
EQ_Cash_Equities_SERVER        ATSU5
PCG_TrdPnL_RND_ALL_TRADES_SERVER        ATSU7
PCG_PrfPnL_RND_ALL_TRADES_SERVER        ATSU7
PCG_PrfPnL_RND_ALL_TRADES_NOGROUP_SERVER        ATSU7
PCG_TrdPnL_PCG_MODIFIED_TODAY_10pm_SERVER        ATSU8
MM_Derec_NoPTPar_FRN_SERVER        ATSU9
MM_Derec_NoPTPar_DEPCD_SERVER        ATSU9
MM_SecondaryMarkets_SERVER        ATSU9
MM_Derec_NoPTPar_FRN_TPLD_SERVER        ATSU9
MM_Derec_NoPTPar_DEPCD_TPLD_SERVER        ATSU9
SND_DEPOSIT_REPRICING_TradeSheet_OVR_SERVER        ATSU9
MM_Derec_NoPTPar_DEPCD_Mid_SERVER        ATSU9
MM_Derec_NoPTPar_FRN_Mid_SERVER        ATSU9
SND_Tradesheet_Incep_SERVER        USER
SND_Tradesheet_YTD_SERVER        USER
"""

def makeList(text):
        list = [(I.split("  ")[0].strip(),I.split("  ")[-1].strip()) for I in text.split("\n")]
        alist = [(N,U) for N,U in list if not (N=="" or U=="")]
        return alist

def allTasks():
        global absaTasks
        nlist = makeList(absaTasks)
        return nlist

#--------------------------------------------------------------------------------------
#
# Decoder for zipped data
#
#
#--------------------------------------------------------------------------------------

import StringIO
import uu
import zlib

s_trans=[
  '`', '!', '"', '#', '$', '%', '&', '\'',
  '(', ')', '*', '+', ',', '-', '.', '/',
  '0', '1', '2', '3', '4', '5', '6', '7',
  '8', '9', ':', ';', '<', '=', '>', '?',
  '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
  'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
  'X', 'Y', 'Z', '[', '\\', ']', '^', '_']




class textDecode:
        
        
        def stripFileHeader(self,S,n):
            O = S.read()
            O = O[n:]
            OF = StringIO.StringIO()
            OF.write(O)
            OF.seek(0,0)
            #print "File without header is",OF.getvalue()
            return OF
        

        def DEC(self,c):
            return ((ord(c) - ord(' ')) & 077) & 0xFF
        
        
        def BinDecodeSize(self,sz):
            return ((int(sz) + 3) / 4) * 3;
        
        # decode '\0' terminated chunks of 4x6bits as 3x8bits
        def BinDecode(self,buf):
            n = len(buf)
            decsz = self.BinDecodeSize(n);
        
            t = ""
            n = n -1
            p = 0 #pointer to buf
            while(n>0):
                ch = 0;
                if(n >= 3):
                    ch = (self.DEC(buf[p+0]) << 2 | self.DEC(buf[p+1]) >> 4) & 0xFF
                    t = t + chr(ch);
                    ch = (self.DEC(buf[p+1]) << 4 | self.DEC(buf[p+2]) >> 2) & 0xFF
                    t = t + chr(ch);
                    ch = (self.DEC(buf[p+2]) << 6 | self.DEC(buf[p+3])) & 0xFF
                    t = t + chr(ch);
                else:
                    if(n >= 1):
                        ch = (self.DEC(buf[p+0]) << 2 | self.DEC(buf[p+1]) >> 4) & 0xFF
                        t = t+chr(ch)
                    if(n >= 2):
                        ch = (self.DEC(buf[p+1]) << 4 | self.DEC(buf[p+2]) >> 2) & 0xFF
                        t = t + chr(ch);
                p+=4
                n-=4
                
            return t;
        

        def uudeflate(self,str):
            """
            Decode using deflate method
            """
            # strip header
            val = "!zipx!"
            if str[:len(val)] == val:
                # ok
                dist = str.find("!",len(val))
                data = str[dist+1:]
                # find the next ! sign
                
                return zlib.decompress(data)
            else:
                raise Exception("Unkown deflate format expected "+val+" got "+str[:len(val)])


        def uudecf(self,fo):
            """
            Decode using adapted uuencode from prime source
            """
            bf = StringIO.StringIO()
            fo = self.stripFileHeader(fo,len("!enc!"))
            str = fo.read()
            return self.BinDecode(str)


        def proc(self,data):
                """Needs error handling"""
                txt =StringIO.StringIO()    
                txt.write(data)
                txt.seek(0,0)
                dectxt = self.uudecf(txt)
                val = self.uudeflate(dectxt)
                return val
                
        def passThrough(self,data):
                #check if the data is encoded i.e prefix !enc!
                
                if("!enc!" == data[0:len("!enc!")]):
                        """Found encoded data decode"""
                        dbug("textDecode found data to decompress!!")
                        try:
                                res = self.proc(data)   
                                return res                     
                        except Exception,e:
                                warning("Could not decode input return data cause",e)
                                return data
                else:
                        return data


#--------------------------------------------------------------------------------------


class baseProcessor:
        
    def makeOldName(self,name):
        return name + ".old"        
        
    def genDuplicate(self,name,trgname,table="Task",oidkey="tasknbr"):
        """Duplicate name as object with name trgname"""
        ob = getattr(ael,table)[name]
        nob = getattr(ael,table).new()
        for c in ob.columns():
            dbug("duplicate processing",c)
            if c=="parameter" and hasattr(ob,"size") and ob.size==0:
                    #patch prime bugs with empty parameter on task table
                    dbug("Found buggy parameter value trying to patch")
                    nob.parameter = "nopt=23;"
            elif c == oidkey:
                pass
            elif c == "name":
                setattr(nob,c,trgname)
            else:
                setattr(nob,c,getattr(ob,c))
            
        return nob

    def duplicate(self,name):
            return self.genDuplicate(name,self.makeOldName(name)) 

    
    def param2dict(self,params):
        
        dlist = [(X.split("=")[0],X.split("=")[1]) for X in params.split(";")
                if X!=""]
        d = dict(dlist)
        return d

    def dict2param(self,params):
        l = [A+"="+str(B) for A,B in params.items()]
        res = ";".join(l) + ";"
        return res

class reverter(baseProcessor):
        
        def exists(self,name):
                """old entry exists"""
                oldn = self.makeOldName(name)
                ob = ael.Task[oldn]
                return ob!=None
        
        def remove(self,name):
                """delete old"""
                ob = ael.Task[name]
                if(ob):
                        ob.delete()
                        dbug("Deleted",name)
                
        def duplicateOld(self,name):
                """duplicate old"""
                no = self.genDuplicate(self.makeOldName(name),name)
                no.commit()

        def process(self,name):
                """Find an old entry and if present replace current with that"""
                dbug("reverting",name)
                if(self.exists(name)):
                        self.remove(name)
                        self.duplicateOld(name)
                        info("Reverted to old version of",name)


class genProcessor(baseProcessor):
    """super class of all processors"""
    def modName(self):
        return self.__class__.__name__
        #return "none"

    def myKind(self,name):
        task = ael.Task[name]
        return task.module == self.modName()

    def process(self,name):
        raise Exception("abstract method")



    def removeOldKeepOld(self,name):
        oldn = self.makeOldName(name)
        ob = ael.Task[oldn]
        if ob:
            ob.delete()


    def keepold(self,name):
        """Create a copy with process name .old"""
        dbug("keepold removeOldKeppOld")
        self.removeOldKeepOld(name)
        dbug("keepold duplicate")
        cval = self.duplicate(name)
        #cval.name = self.makeOldName(name)
        dbug("Commiting changes")
        cval.commit()
        dbug("Done with keepold!")


    def consider(self,name,keepold):
        cname = self.__class__.__name__
        if self.myKind(name):
            dbug("Processing",name,"using",cname)
            if keepold:
                self.keepold(name)
            self.process(name) 
            return True
        return False
            
    def worksheetDefV(self):
        """Standard values of worksheet"""
        #could possiibly grab these values from the module itself
        val = {'function': '', 'Print template (XSL)': 'FStandardTemplate', 'gridOutput': 'False',
                'Print style sheet (CSS)': 'FStandardCSS', 
                'FPortfolioSheet_Portfolio Profit Loss End Date Custom': '', 
                'File date format': '', 'FTradeSheet_Portfolio Profit Loss Start Date Custom': '',
                'Date format': '%d%m%y', 'Include Default Data': 'False', 
                'FPortfolioSheet_Portfolio Profit Loss Use MtM Today': '', 
                'zeroPositions': 'False', 'FTradeSheet_Portfolio Profit Loss End Date': '', 
                'FTimeSheet_PL Valuation Date Custom': '', 
                'Include Formatted Data': 'True', 'FTradeSheet_overrideSheetSettings': 'False', 
                'Include Full Data': 'False', 
                'FPortfolioSheet_Portfolio Hide Expired Positions Choice': '', 
                'AMB Subject': '', 'Performance Strategy': 'Periodic full GC to save memory', 
                'gridRowPartitionCbClass': 'FReportGridCallbacks.RowPartitionManager', 
                'FPortfolioSheet_Portfolio Trade Filter Match Choice': '', 
                'FPortfolioSheet_Credit Delta RateType': '', 
                'gridAggregateXmlCbClass': 'FReportGridCallbacks.AggregateXmlManager', 
                'FTimeSheet_overrideSheetSettings': 'False', 'Include Raw Data': 'True', 
                'portfolioRowOnly': 'False', 
                'FTradeSheet_Portfolio Profit Loss End Date Custom': '', 
                'FPortfolioSheet_Portfolio Profit Loss Start Date': '', 'param': '', 
                'FTradeSheet_Portfolio Profit Loss Use MtM Today': '', 'AMB Address': '', 
                'HTML to File': 'True', 'FTradeSheet_Portfolio Profit Loss Start Date': '', 
                'template': [], 'XML to File': 'False', 'HTML to Screen': 'True', 
                'HTML to Printer': 'False', 'Compress Output': 'False', 
                'gridRowPartitionCbArg': '', 'Create directory with date': 'True', 
                'Secondary file extension': '.xls', 'AMB XML Message': 'True', 
                'Overwrite if file exists': 'True', 'instrumentParts': 'False', 
                'Secondary output': 'False', 'clearSheetContent': 'False', 'preProcessXml': '', 
                'portfolios': [], 'Secondary template': 'FTABTemplate', 'AMB Sender Name': '', 
                'FTimeSheet_PL Valuation Date': '', 'File Path': '', 'wbName': None, 
                'gridUseLoopbackGridClient': 'False', 'tradeFilters': [], 
                'FPortfolioSheet_Portfolio Profit Loss End Date': '', 'updateInterval': 60, 
                'FPortfolioSheet_Valuation Date': '', 
                'FPortfolioSheet_Portfolio Price Source': '', 
                'FPortfolioSheet_Credit Delta Displayed Rate': '', 'expiredPositions': 'False', 
                'FPortfolioSheet_Portfolio Hide Zero Positions Choice': '', 'File Name': '', 
                'trades': [], 'instrumentRows': 'True', 
                'FPortfolioSheet_Portfolio Profit Loss Start Date Custom': '', 
                'multiThread': 'True', 'FPortfolioSheet_overrideSheetSettings': 'False', 
                'FPortfolioSheet_Credit Delta DayCount': '', 'snapshot': 'True', 
                'Send XML File to AMB': 'False', 'numberOfReports': 5, 
                'File date beginning': 'False', 'gridTimeout': 60, 'grouping': []}
        for i in val.keys():
                if(val[i]==[]):
                        val[i] = ''
        return val




    def valMapping(self):
            raise Exception("abstract method")
    
    def processMappings(self,nparams,dparams):
        """Change all mappings, utility function for processing"""
        mapping = self.valMapping()
        for k in dparams.keys():
            if k in mapping:
                nk = mapping[k]
                if nk == "WARNEMPTY":   
                        if(dparams[k]=="0" or dparams[k]=="False" or dparams[k]=="No"):
                                warning("ignoring parameter",k,"with value",dparams[k])
                elif nk == "DBUG":
                        dbug("unmapped value",k,"(",dparams[k],")")
                elif nk == "WARNING":
                        if not (dparams[k]=="" or dparams[k]==None or dparams[k]=="None" or
                                        dparams[k]=="No"):
                                warning("ignoring parameter",k,"with value",dparams[k])
                else:
                        nparams[nk] = dparams[k]
                        dbug("map",nk,"=",k,"(",dparams[k],")")
                        
        dbug("postprocesing of params")
        if('Secondary template' in nparams 
                and nparams['Secondary template']=='FStandardTemplate'):
                        nparams['Secondary template'] = 'FTABTemplate'
                        dbug('Changed secondary template from FStandardTemplate to FTABTemplate')
        return nparams

        
    def getFName(self,text):
            """Changing parameter value File Name """
            #the slow but safe method
            x = ""
            for c in text:
                    #keep only sane symbols in the filename
                    if((ord(c)>=ord("A") and ord(c)<=ord("Z"))
                       or (ord(c)>=ord("0") and ord(c)<=ord("9"))
                       or (ord(c)>=ord("a") and ord(c)<=ord("z"))):
                            x = x + c
                    else:
                            x = x + "_" #spaces and everything else gets squashed
            return x

class FPortfolioReport(genProcessor):
    """Convert FPortfolioReports to FWorksheetReport"""

 
    def prfdef(self):
        """Default Front 2 values for FPortfolioReport"""
        val = {'IR Delta Include All Currency': '1', 'Print style sheet (CSS)': 'FStandardCSS', 
               'includeInactive': 'False', 'Credit Delta Displayed Rate': 'Par CDS Rate', 
               'Secondary file extension': '.xls', 
               'Portfolio Hide Zero Positions Choice': 'P/L Period Position', 
               'Credit Delta DayCount': 'Act/360', 'Include Formatted Data': 'True', 
               'Credit Delta AttributeType': 'Issuer', 'IR Delta DayCount': 'None', 
               'forceGCPeriod': 0, 'Credit Delta Include All Currency': '1', 
               'Vega Bucket Include All Currency': '1', 
               'Portfolio Profit Loss Start Date Custom': '1970-01-01', 
               'Portfolio Profit Loss End Date Custom': '2009-08-11', 
               'Portfolio Profit Loss End Date': 'Now', 'HTML to File': 'True', 
               'XML to File': 'True', 'HTML to Screen': 'True', 'includeExpired': 'False', 
               'tst': None, 'Compress Output': 'False', 
               'Create directory with date': 'True', 'PL Decomp Detailed View': 'No', 
               'Overwrite if file exists': 'True', 'Secondary output': 'False', 'pf': [], 
               'Secondary template': 'FTABTemplate', 'disableEvalCache': 'False', 
               'IR Delta RateType': 'None', 'buildInstrumentParts': 'False', 'tf': [], 
               'File Path': 'c:\\', 'wbName': None, 'IR Delta Displayed Rate': 'None', 
               'HTML to Printer': 'False', 'BM Delta YieldCurve': '', 'updateInterval': 60, 
               'Portfolio Profit Loss Start Date': 'Inception', 
               'Credit Delta RateType': 'Quarterly', 
               'Portfolio Profit Loss Use MtM Today': 'No', 'Translation Dictionary File': '', 
               'Print template (XSL)': 'FStandardTemplateClickable', 'Include Raw Data': 'True', 
               'PL Decomp Recalc': '1', 'multiThread': 'True', 
               'Alternative YieldCurve': 'ALL-SWAP', 'snapshot': 'True', 'onlyPort': 'True', 
               'IR Delta Forward Period': '1d', 'numberOfReports': 10, 
               'Portfolio Hide Expired Positions Choice': 'Valuation Date', 
               'showSingleRows': 'True', 'grouping': "[Default]"}
        return val



 

    def valMapping(self):
        return {'wbName':'wbName',                        #Workbook
                'tst':'template',                         #Trading Sheet Template
                'pf':'portfolios',                        #portfolios
                'tf':'tradeFilters',                      #tradefilters
                'onlyPort':'portfolioRowOnly',            #portfolio row only
                'grouping':'grouping',                    #grouping
                'showSingleRows':'instrumentRows',        #show instrument rows
                'buildInstrumentParts':'instrumentParts', #include instrument parts
                'includeInactive':'zeroPositions',        #zero positions
                'includeExpired':'expiredPositions',      #include expired
                'snapshot':'snapshot',                    #run as sheet snapshot
                'multiThread':'multiThread',              #multithread but which label?
                'numberOfReports':'numberOfReports',      #nbr of reports
                'updateInterval':'updateInterval',        #update interval
                'Include Raw Data':'Include Raw Data',    # include unformated output
                'Include Formatted Data':'Include Formatted Data', # formated data
                'HTML to File':'HTML to File',            # write html to file
                'HTML to Screen':'HTML to Screen',        # open explorer
                'HTML to Printer':'HTML to Printer',      # send html to printer
                'XML to File':'XML to File',              # write xml
                'File Path':'File Path',                  # file path
                'Compress Output':'Compress Output',      # compress output 
                'Create directory with date':'Create directory with date', # directory date
                'Overwrite if file exists':'Overwrite if file exists', # overwrite
                'Print template (XSL)':'Print template (XSL)', #XSLT transform of output
                'Print style sheet (CSS)':'Print style sheet (CSS)', # style sheet
                'Secondary output':'Secondary output',          # do secondary output?
                'Secondary template':'Secondary template',# secondary template
                'Secondary file extension':'Secondary file extension', #file extension
                'Translation Dictionary File':"WARNING", #warn if this is used
                'Alternative YieldCurve':"WARNING",       # yield curve, not relevant in new version
                'IR Delta DayCount':"WARNING",            # obsolete since F4
                'IR Delta Displayed Rate':"WARNING",      # obsolete since F4
                'IR Delta RateType':"WARNING",            # obsolete since F4
                'IR Delta Include All Currency':"WARNEMPTY",# obsolete since F4
                'IR Delta Forward Period':"WARNING",      # obsolete since F4
                'Credit Delta AttributeType':"DBUG",      # obsolete default issuer
                'Credit Delta DayCount':'FPortfolioSheet_Credit Delta DayCount', # portfolio daycount
                'Credit Delta Displayed Rate':'FPortfolioSheet_Credit Delta Displayed Rate', # portfolio
                'Credit Delta RateType' : 'FPortfolioSheet_Credit Delta RateType', # portfolio ratetype
                'PL Decomp Detailed View' : "WARNING",    # obsolete
                'PL Decomp Recalc' : "DBUG",              # obsolete
                'Vega Bucket Include All Currency' :  "WARNEMPTY", # obsolete
                'BM Delta YieldCurve' : "WARNING", #obsolete
                'Portfolio Profit Loss Start Date': 'FPortfolioSheet_Portfolio Profit Loss Start Date', #portfolio start day
                'Portfolio Profit Loss Start Date Custom' : 'FPortfolioSheet_Portfolio Profit Loss Start Date Custom', #portfolio start date custom
                'Portfolio Profit Loss End Date' : 'FPortfolioSheet_Portfolio Profit Loss End Date', # portfolio
                'Portfolio Profit Loss End Date Custom':'FPortfolioSheet_Portfolio Profit Loss End Date Custom', #portfolio
                'Portfolio Profit Loss Use MtM Today' : 'FPortfolioSheet_Portfolio Profit Loss Use MtM Today', #portfolio
                'Portfolio Hide Expired Positions Choice' : 'FPortfolioSheet_Portfolio Hide Expired Positions Choice', # zero position
                'Portfolio Hide Zero Positions Choice' : 'FPortfolioSheet_Portfolio Hide Zero Positions Choice', # portfolio
                #performance settings left out
                }




    def process(self,name):
        """Make translation"""
        o  = ael.Task[name]
        oc = o.clone()
        oc.module = "FWorksheetReport"
        
        #patch prime bug that crashes prime
        if(oc.size == 0):
                params = "noopt=-1;"
        else:
                params = oc.parameter
        #we need to rebuild them to 
        dparams = self.param2dict(params)
        nparams = self.worksheetDefV()
        mapping = self.valMapping()

        #always override sheet settings
        nparams['FPortfolioSheet_overrideSheetSettings'] =  'True'
        nparams["File Name"] = self.getFName(name)
        nparams["Include Default Data"] = 'True'
        nparams = self.processMappings(nparams, dparams)        
        #dbug("process Trades where",nparams["trades"])
        #not available in nparams
        #nparams["trades"] = ''        
        oc.parameter = self.dict2param(nparams)        
        # wait with commit
        oc.commit()
        info("Upgraded",name)


class FTradeReport(genProcessor):
        
        def dtp(self):
                """default values for FTradeReport"""
                val = {'Print style sheet (CSS)': 'FStandardCSS', 
                       'Portfolio Profit Loss End Date Custom': '2009-08-14', 
                       'Include Formatted Data': 'True', 
                       'Secondary output': 'False', 
                       'Portfolio Profit Loss Start Date Custom': '1970-01-01', 
                       'Portfolio Profit Loss End Date': 'Now', 
                       'HTML to File': 'True', 
                       'XML to File': 'True', 
                       'HTML to Screen': 'True', 
                       'HTML to Printer': 'False', 
                       'tst': '', 
                       'Translation Dictionary File': '', 
                       'Create directory with date': 'True', 
                       'Overwrite if file exists': 'True', 
                       'wb': 'rolf_map_wb_ts', 
                       'Secondary template': 'FTABTemplate', 
                       'buildInstrumentParts': 'False', 
                       'File Path': 'c:\\', 
                       'Secondary file extension': '.xls', 
                       'updateInterval': 60, 
                       'Portfolio Profit Loss Start Date': 'Inception', 
                       'Portfolio Profit Loss Use MtM Today': 'No', 
                       'Compress Output': 'False', 
                       'Print template (XSL)': 'FStandardTemplate', 
                       'Include Raw Data': 'True', 
                       'snapshot': 'True'}
                return val


        
        def valMapping(self):
                """mapping for FTrade sheets"""
                
                return {'wb':'wbName',
                        'tst':'template',
                        'snapshot':'snapshot',
                        'updateInterval':'updateInterval',
                        'Include Raw Data':'Include Raw Data',
                        'Include Formatted Data':'Include Formatted Data',
                        'HTML to File':'HTML to File',
                        'HTML to Screen':'HTML to Screen',
                        'HTML to Printer':'HTML to Printer',
                        'XML to File':'XML to File',
                        'File Path':'File Path',
                        'Compress Output':'Compress Output',
                        'Create directory with date':'Create directory with date',
                        'Overwrite if file exists':'Overwrite if file exists',
                        'Print template (XSL)':'Print template (XSL)',
                        'Print style sheet (CSS)':'Print style sheet (CSS)',
                        'Secondary output':'Secondary output',
                        'Secondary template':'Secondary template',
                        'Secondary file extension':'Secondary file extension',
                        'Translation Dictionary File':'Translation Dictionary File',
                        'Portfolio Profit Loss Start Date':'FTradeSheet_Portfolio Profit Loss Start Date',
                        'Portfolio Profit Loss Start Date Custom':'FTradeSheet_Portfolio Profit Loss Start Date Custom',
                        'Portfolio Profit Loss End Date':'FTradeSheet_Portfolio Profit Loss End Date',
                        'Portfolio Profit Loss End Date Custom' : 'FTradeSheet_Portfolio Profit Loss End Date Custom',
                        'Portfolio Profit Loss Use MtM Today' : 'FTradeSheet_Portfolio Profit Loss Use MtM Today',
                        
                        }
                
        def process(self,name):
                """Make translation"""
                o  = ael.Task[name]
                oc = o.clone()
                oc.module = "FWorksheetReport"
                
                #patch prime bug that crashes prime
                if(oc.size == 0):
                        params = "noopt=-1;"
                else:
                        params = oc.parameter
                                                
                #we need to rebuild them to 
                dparams = self.param2dict(params)
                nparams = self.worksheetDefV()
                mapping = self.valMapping()
        
                #always override sheet settings
                nparams['FTradeSheet_overrideSheetSettings'] =  'True'
                nparams["File Name"] = self.getFName(name)
                #patch an error in reporting
                #is this true in all reports
                nparams["numberOfReports"] = 1
                nparams["Include Default Data"] = 'True'
                nparams = self.processMappings(nparams, dparams)        
                #not available in nparams
                nparams["trades"] = ''
                if(nparams["updateInterval"]==""):                        
                        nparams["updateInterval"] = 60        
                        dbug("process updateInterval set to 60 ")
                else:
                        dbug("updateInterval kept already set to",nparams["updateInterval"])
                oc.parameter = self.dict2param(nparams)        
                
                dbug("process parameter result",oc.parameter)
                oc.commit()
                info("Upgraded",name)



def getAllProcessors():
    return [FPortfolioReport(),FTradeReport()]


         
#------------------- classes to process workbooks ---------------------
    

class workbookArmyKnife:
    """misc base class for workbook managment"""

    def getTextObject(self,elem):
            td = textDecode()
            return td.passThrough(elem.get_text())

    def getElems(self,item,tagname,d=0):
            list = []
            #print "--"*d,"Examining",item.tag
            if(item.tag == tagname):
                list.append(item)
            for i in item.getchildren():
                list.extend(self.getElems(i,tagname,d+1))
            return list

    def getChild(self,item,tagname,d=0):
            """Get all children with tagname"""
            if(item==None):
                    return
            list = []
            for i in item.getchildren():
                    if(i.tag==tagname):
                            list.append(i)
            return list

    def getChildByPath(self,item,path,d=0):
            if(path==[]):
                    return [item]
            else:
                    celem = path[0]
                    tail  = path[1:]
                    clist = []
                    for c in item.getchildren():
                            if(c.tag == celem):
                                    clist.extend(self.getChildByPath(c,tail,d+1))
                    return clist
            
    def getElemsByPath(self,item,path):
            """Same thing as //atag/btag/ctag/etag return empty list if not found"""
            #first tag is on global level
            glob = path[0]
            spath = path[1:]
            list = self.getElems(item,glob)
            #
            retlist = []
            for i in list:
                retlist.extend(self.getChildByPath(i,spath))
            return retlist

    def getASQL(self,q):
            dbug("getASQL query",q)
            res = ael.asql(q)
            dbug("getASQL res",res)
            if(res[1]!=[] and res[1][0]!=[] and
               res[1][0][0]!=[] and res[1][0][0][0]!=[]):
                    return res[1][0][0][0]
            else:
                    return None
    
    def getASQLL(self,q):
            """Return list of values"""
            dbug("getASQL query",q)
            res = ael.asql(q)
            dbug("getASQL res",res)
            al = res[1][0]
            if(al==[]):
                    return None
            return res[1][0][0]

    def sheetNames(self):
            return ["FPortfolioSheet","FOrderBookSheet","FTradeSheet"]


#TODO: getWorkb needs to include user?
    def getWorkb(self,wb,userName):
            """get workbook"""
            user = ael.User[userName]
            if(not user):
                    return None
            usrnbr = user.usrnbr
            q = "select seqnbr from textobject where name = '%s' and type = '%s' and usrnbr = %s"  \
                % (wb,"Workbook",usrnbr)
            res = self.getASQL(q)
            if(not res):
                    return None
            to = ael.TextObject[res]
            return to



    def getIntFromFGuiTree(self,elem):
        """Get ptrint or int from a tree"""
        t = self.getElemIntFromGuiTree(elem)
        return [i.text for i in t]
        
    def getElemIntFromGuiTree(self,elem):
        """Get ptrint or int from a tree"""
        intv = self.getElems(elem,"ptrint")
        inta = self.getElems(elem,"int")
        if(intv==[] and inta!=[]):
                return inta
        return intv           



    def fetchSheetOids(self,wbName,userName):
        wbt = self.getWorkb(wbName,userName)
        if(not wbt):
                warning("fetchSheetOids could not find workbook",wbName,
                        "of user",userName,"skipping workbook")
                return []
        text = self.getTextObject(wbt)
        import xml.etree.ElementTree as ET
        #this may break, catch in above levels
        tree = ET.fromstring(text)
        pers = self.getElems(tree,"FPersistent")
        #dbug("fetchSheetOids",text)
        dbug("fetchSheetOids found",pers,"FPersistent") 
        retlist = []
        for i in pers:
                stros = self.getElems(i,"string")
                #values internal to text
                val = [V.text for V in stros]
                #fetch oid val that may be stored in different ways

                intv = self.getIntFromFGuiTree(i)
                dbug("fetchSheetOids val",val)
                dbug("fetchSheetOids intv",intv)
                if(len(val)==2 and val[1]=="oid" and len(intv) == 1 ):
                        if(val[0] in self.sheetNames()):
                                #return oids of sheets to duplicate
                                retlist.append(int(intv[0]))
                        else:
                                warning("fetchSheetOids Ignoring sheet",val[0],"in",wbName)
                        
        return retlist
    

class workbookInvestigator(workbookArmyKnife,baseProcessor):
        """Check if a workbook has a none empty sheet"""


        def workbookExists(self,wbName,uName):
                return self.getWorkb(wbName, uName)!=None

        def getParam(self,t,w):
                if(t.size==0):
                        return None
                else:
                        params = self.param2dict(t.parameter)
                        return params[w]
                
        def getWorkbookName(self,t):
                return self.getParam(t,"wbName")

        def getTradeFilter(self,t):
                #TODO: fix
                return self.getParam(t,"tradeFilters")

        def examineDataInSheet(self,to):
                    """Count entries in the FGuiTree"""
                    """
                            <FGuiTree type ="AcmDomain">
                              <item type ="Property">
                                <FSymbol type ="AcmDomain">
                                  <Text type ="Property">
                                    <string type ="AcmDomain">Root</string>
                                  </Text>
                                </FSymbol>
                              </item>
                            </FGuiTree>
                    """
                    import xml.etree.ElementTree as ET
                    text = self.getTextObject(to)
        
                    try:
                            tree = ET.fromstring(text)
                    except Exception,e:
                            warning("illegal XML found for sheet",to.name,"skipping")
                            return 0
                    guit = self.getElems(tree,"FGuiTree")
                    
                    #remove anything in sheet parts
                    quant = 0
                    for elem in guit:
                            quant = quant + len(elem[1:])
                            dbug("examineDataInSheets Found quantity", \
                                        quant,"of elems in sheet")
                    
                    return quant != 0
                    
        
        def investigateSheets(self,wbName,userName):
                sheetoids = self.fetchSheetOids(wbName,userName)
                res = 0
                dbug("investigateSheets number of sheets",len(sheetoids))
                for sheet in sheetoids:
                        txt = ael.TextObject[sheet]
                        valSheet = self.examineDataInSheet(txt)
                        res = res + valSheet
                        dbug("investigateSheets sheet",sheet,"quant",valSheet)
                return res != 0

        def considerNewWB(self,taskName,userName,prefix):
                dbug("Examining",taskName,"using",userName,"and prefix",prefix)
                ael.poll() # get the commited values
                t = ael.Task[taskName]
                wbName = self.getWorkbookName(t)
                tft    = self.getTradeFilter(t)
                #we don't want to create workbooks if its not needed
                if(tft==None or tft==''):
                        dbug("no trade filter means no additional workbooks required")
                        return False

                #TODO: move after workbook exists?
                dataInSheets = self.investigateSheets(wbName,userName)

                
                #ensure new workbook names fit into database
                newWbName = (prefix + wbName)[:31]
                
                #check if a workbook already exists with proper name
                #and do not create a new workbook
                if(self.workbookExists(newWbName,userName)):
                        dbug("additional workbook already created skipping")
                        return True

                #workbook needs to be set
                if(dataInSheets):
                        dbug("Found that",taskName,"with workbook as userName",userName,"needs new workbooks")                
                        #duplicate sheet
                        clm = workbookCloneMachine()
                        #DEBUG clm.duplicate
                        clm.duplicate(wbName, newWbName, userName, userName)
                return True

        def considerTask(self,taskName, userName, prefix):
                """Link task to new workbook"""
                #ensure commited changes can be seen from python
                ael.poll()
                t = ael.Task[taskName]
                #get workBook
                wbName = self.getWorkbookName(t)
                if(wbName == None or wbName==''):
                        return
                
                addWbName = (prefix + wbName)[:31]
                dbug("considerTask addWbName",addWbName,"prefix",prefix,"wbName",wbName)
                #check if there is a new workbook
                wb  = self.getWorkb(addWbName, userName) 
                # t.size!= 0 proctes against prime bug with parameter field
                if(wb and t.size!=0):
                        #assume that we should link
                        
                        tc = t.clone()                        
                        pars = self.param2dict(tc.parameter)
                        #change wbName
                        pars["wbName"] = addWbName 
                        tc.parameter = self.dict2param(pars)
                        tc.commit()
                        dbug("considerTask Changed workbook of task",taskName,"from",wbName,"to",addWbName)


        def consider(self,taskName,userName,prefix):
                """taskName - name of task to consider
                   userName - user of workbook of task
                   prefix   - prefix of possible new workbook
                """
                dbug("consider",taskName,userName,prefix)
                chgwb = self.considerNewWB(taskName, userName, prefix)
                if(chgwb):
                        #consider attaching workbook (will always attach if workbook exists)
                        self.considerTask(taskName, userName, prefix)
                

                
class workbookCloneMachine(workbookArmyKnife):
    """Clone workbooks including the sheets"""

    def genOidDup(self,oid,trgname,table="Task",oidkey="tasknbr"):
        """Duplicate object with oid and name as object with name trgname"""
        ob = getattr(ael,table)[oid]
        nob = getattr(ael,table).new()
        for c in ob.columns():
            dbug("genOidDup processing",c)
            if c=="parameter" and hasattr(ob,"size") and ob.size==0:
                    #patch prime bugs with empty parameter on task table
                    dbug("Found buggy parameter value trying to patch")
                    nob.parameter = "nopt=23;"
            elif c == oidkey:
                pass
            elif c == "name":
                print "SETATTR",nob,c,trgname
                print "SETATTR type(",type(nob),type(c),type(trgname),")"
                print "SETATTR len(",len(trgname),")"
                setattr(nob,c,trgname)
            else:
                setattr(nob,c,getattr(ob,c))
            
        return nob


    def filterDataInSheets(self,to):
            """Remove any rows in report and keep only columns"""
            """
                    <FGuiTree type ="AcmDomain">
                      <item type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Root</string>
                          </Text>
                        </FSymbol>
                      </item>
                    </FGuiTree>
            """
            import xml.etree.ElementTree as ET
            text = self.getTextObject(to)

            tree = ET.fromstring(text)
            guit = self.getElems(tree,"FGuiTree")
            dbug("filterDataInSheets FGuiTree",guit)
            #remove anything in sheet parts
            for elem in guit:
                    prevl = len(elem.getchildren())
                    del elem[1:]
                    nlen  = len(elem.getchildren())
                    dbug("filterDataInSheets removed",prevl-nlen,"rows, had",prevl,"rows in",
                         elem.tag)
            data = ET.tostring(tree)
            #assume that we must add the header
            to.set_text("<?xml version='1.0' encoding='ISO-8859-1'?>\n"+data)
            return to
            
            
    def removeTextObject(self,name):
            """remove text object"""
            q = "select seqnbr from textobject where name = '%s' " % (name)
            list = self.getASQLL(q)
            if(not list):
                    return
            for i in list:
                    to = ael.TextObject[int(val)]                    
                    if(to):
                            to.delete()
                            dbug("Deleted textobject with name",name)

    def replicateSheets(self,list):
            """Produce sheets from list"""
            oidl = []
            for s in list:
                    dbug("replicateSheets of oid",s)
                    txt = ael.TextObject[s]
                    if(txt == None):
                        raise Exception("replicateSheets no txt")
                    #simply copy the sheet to a new name
                    name = txt.name
                    dbug("replicateSheets genDuplicate of",name,"with oid",s,"to","-1"+name)                    
                    
                    #use a temporary name first
                    self.removeTextObject("-1"+name)
                    to = self.genOidDup(s,"-1"+name,"TextObject","seqnbr")                    
                    to.commit()
                    
                    #ensure conformance to the standard name
                    toc = to.clone()
                    #use same name without numbers
                    filteredName = "".join([c for c in name if not (c>="0" and c<="9")])
                    toc.name = filteredName + str(to.seqnbr)
                    #apply changes here to ensure those changes go through
                    self.filterDataInSheets(toc)
                    toc.commit()
                    dbug("replicateSheets Commited textobject",toc.name,"with oid",toc.seqnbr)
                    oidl.append(toc.seqnbr)
                                    
            #return copied sheets (need for workbook connection)
            
            return oidl
            


    def duplicateWorkbook(self,wbName,newWbName,oldUserName):
        """Workbook is not commited in this method"""
        wo  = self.getWorkb(wbName,oldUserName)
        if(not wo):
                warning("Cannot locate workbook",wbName,"with user name",
                        oldUserName)
                return None
        dup = self.genOidDup(wo.seqnbr,newWbName,"TextObject","seqnbr")
        #dup.commit()
        dbug("Duplicated workbook",wo.name,"with oid",wo.seqnbr,"as",newWbName)
        return  dup

    def duplicateSheets(self,wbName,userName):
        #----- sheets ----
        list  = self.fetchSheetOids(wbName,userName)
        dbug("list of sheet oids",list)
        olist = self.replicateSheets(list)
        dbug("Found sheets ",olist)
        return olist

    def linkSheets(self,wbt,list,user):
        """link sheets input wbt should be a copy of an uncommited workbook"""
        #wbt  = self.getWorkb(wbName)
        text = self.getTextObject(wbt)
        import xml.etree.ElementTree as ET
        #this may break, catch in above levels
        tree = ET.fromstring(text)
        pers = self.getElems(tree,"FPersistent")
        #dbug("linkSheets",text)
        dbug("linkSheets found",pers,"FPersistent") 
        #must match in number
        zlist = list(zip(pers,list))
        for i,noid in zlist:
                stros = self.getElems(i,"string")
                #values internal to text
                val  = [V.text for V in stros]
                inte = self.getElemIntFromGuiTree(i)                
                intv = self.getIntFromFGuiTree(i)
                
                dbug("fetchSheetOids val",val)
                dbug("fetchSheetOids intv",intv)
                if(len(val)==2 and val[1]=="oid" and len(intv) == 1 ):
                        if(val[0] in self.sheetNames()):
                                #return oids of sheets to duplicate
                                #change the value
                                inte[0].text = str(noid)
                                dbug("linkSheets linking",noid)                                
                        else:
                                warning("Ignoring sheet (%s)" % val[0],"in",wbName)
        data = ET.tostring(tree)
        
        #skip this part for now
        wbt.set_text("<?xml version='1.0' encoding='ISO-8859-1'?>\n"+data)
        wbt.usrnbr = user # change user to correct user
        wbt.commit()
        #return retlist
        #dbug("linkSheet final result of data",data)
        
            

    def duplicate(self,wbName,newWbName,oldUserName,newUserName):
        """duplicate a workbook as another name"""
        nuser = ael.User[newUserName]
        if(nuser==None):
                raise Exception("user",newUserName,"could not be found")

        ouser = ael.User[oldUserName]
        if(ouser==None):
                raise Exception("user",oldUserName,"could not be found")

        list = self.duplicateSheets(wbName,oldUserName)        
        
        #create workbook
        wbt = self.duplicateWorkbook(wbName,newWbName,oldUserName)
        if(wbt):
                self.linkSheets(wbt,list,nuser)   
        else:
                warning("not linking sheets to workbook no workbook found")

def testClone():
        wcm = workbookCloneMachine()
        #wcm.duplicate("rolf_map_wb","rolf_map_wb.clone")
        wcm.duplicate("rolf_wb_dupt","rolf_wb_dupt.clone","ROLF.STENHOLM","ATS")
        
#---------------------     ael main    --------------------------------

def procEntry(keepold,s,prefix,userName):
    """s        - task to convert 
       prefix   - workbook prefix
       userName - the user of the workbook
    """
    
    dbug("ProcEntry",keepold,s)
    #try to fetch the task
    task = ael.Task[s]
    if(not task):
            warning("No task named",s,"found skipping!!")
            return
    
    
    l = getAllProcessors()
    #check if something was converted
    nproc = False
    for i in l:
        nproc = nproc or i.consider(s,keepold)
    if(not nproc):
            warning("No conversion available for Task",s) 
        
        
    dbug("Considering all workbooks")
    if(nproc):
            wi = workbookInvestigator()
            wi.consider(s,userName,prefix)
    else:
        warning("Task",s,"has not been converted properly or is unsupported, ignoring workbooks!")


def procRevert(s):
    dbug("ProcRevert ",s)
    reverter().process(s)
    

def proc(g):
    """process all items"""
    keepold = False
    prefix  = g["prefix"]
    tasks = g["scripts"] #tasks actually
    unames = g["users"] # user names
    acclist = list(zip(tasks,unames))
    #check if using absalist
    if(g["atasks"]):
            acclist.extend(allTasks())
    dbug("tasks and users names",acclist)
    if(prefix == ""):
            info("Cannot use empty prefix for new workbooks")
    if(g["operation"]=="Upgrade & Backup"):
            keepold = True
            for s,u in acclist:
                    procEntry(keepold,s,prefix,u)
    elif(g["operation"] == "Upgrade"):
            keepold = False
            for s,u in acclist:
                    procEntry(keepold,s,prefix,u)
    elif(g["operation"] == "Revert to old"):
            for s,u in acclist:
                    procRevert(s)


def ael_main(g):
    global Version
    global logger
    logger.Reinitialize( level=VERBOSITY )
    info(Version)
    proc(g)

