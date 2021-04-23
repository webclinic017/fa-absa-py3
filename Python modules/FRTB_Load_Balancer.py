"""--------------------------------------------------------------------
MODULE:         FRTB_Load_Balancer
    
DESCRIPTION:    This module contains a ael task that is used for load balancing query folders used in FRTB and VaR.

                Methodology:
                
                1. Get Valid Positions:         (if GetValidPositionsFromPortfolio is selected) the script will retrieve all valid positions for valid portfolios (i.e. MR_Eligible add-info =  True),
                2. Rank Portfolios:             The script ranks valid profolios based on their cost of calculation, which is determined by a deterministic weigthing for various instypes.
                3. Create Queries:              Based on the cost of calculations, portfolios are assigned to query folders. 
                                                The user can select the number of partitions to use, as well as provide a list of exceptions (portfolios to be treated seperate from valid portfolios).
                4. Check Queries:               This check ensure that all portfolios have been assigned to a newly created query folder.
                5. Create Tasks:                The queries are then assigned to a task based on a selected calculation type.
HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2021-03-18      FDRTB-2797     Jaysen Naicker          Split VaR Loadbalancer > Trading vs Banking
2021-03-22      FDRTB-2830     Jaysen Naicker          Optimize Load Balancer code - round robin allocation and query folder creation
ENDDESCRIPTION
--------------------------------------------------------------------"""

import acm
import ael
import FRunScriptGUI
import FLogger
import logging
import collections
import inspect
import os
import csv
import platform

portfolio_exlusion_list = [979, 13]      # 'Swap Flow', 'VOE'

""" ---------------- Global Functions ---------------- """

def __getLoggerKwArgsFromAelParams(ael_params):
    """set logger kwargs"""
    log_file    = ael_params['log_file']
    logger_kwargs = {
        'level': int(ael_params['log_mode']),
        'logToConsole': int(ael_params['log_to_console']) == 1,
        'logToPrime': False,
        'keep': False,
        'logOnce': False,
        'logToFileAtSpecifiedPath' : str(log_file)
    }
    return logger_kwargs
    
def createDefaultLogger(name, ael_params):
    """create default logger"""
    kwargs = __getLoggerKwArgsFromAelParams(ael_params)
    logger = FLogger.FLogger.LOGGERS.get(name)
    if logger:
        logger.Reinitialize(**kwargs)
    else:
        logger = FLogger.FLogger(name=name, **kwargs)

    log_formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')
    for handler in logger.Handlers():
        handler.setFormatter(log_formatter)
        
    return logger

def createOuputDir(output_dir):
    """create output directory"""
    new_dir = output_dir
    if not os.path.exists(new_dir):
        try:
            os.makedirs(new_dir)
        except OSError:
             print ("Creation of the directory %s failed"% new_dir)

def is_standard_calc_type(calc_type):
    return calc_type in ['FRTB SA', 'FRTB IMA']
    
def is_VaR_calc_type(calc_type):
    return calc_type in ['VaR']
    
""" ---------------- Get Valid Positions ---------------- """

context     = acm.GetDefaultContext()
sheet_type  = 'FPortfolioSheet'
column_id   = 'Portfolio Position'

class RowManager( object ):

    def __init__( self ):
        self.top_level = 0

    def is_top_level_node( self, node ):
        """return whether node is a top level node"""
        parent = node.Iterator().Parent()
        if parent.Tree().Item().StringKey() == 'Root':
            return True
        return False

    def get_node_name( self, node ):
        """return unique name for node"""
        node_name = node.Item().StringKey()
        if self.is_top_level_node( node ):
            node_name = ''.join( [ str( self.top_level ), '/', node_name ] )
            self.top_level += 1
            return node_name
        return node_name

    def get_top_level_nodes( self, calc_space ):
        """return list of top level nodes from calc space"""
        nodes = []
        next_sibling = calc_space.RowTreeIterator().FirstChild()
        while next_sibling:
            nodes.append( next_sibling.Tree() )
            next_sibling = next_sibling.NextSibling()
        return nodes

    def get_node_names( self, calc_space, iterator, result=None, node_names=None ):
        """"recurse grid and collect node names"""
        if node_names == None:
            node_names = []
        if result == None:
            result = []
        if calc_space.CalculateValue(iterator.Tree(), column_id):
            node_names.append( self.get_node_name( iterator.Tree() ) )
        if iterator.NextUsingDepthFirst():
            self.get_node_names( calc_space, iterator, result, node_names[:] )
        else:
            result.append( node_names )
        return result

    def get_node_names_from_calc_space( self, calc_space ):
        """return list of node names from calc space"""
        child_node_names = []
        top_level_nodes = self.get_top_level_nodes( calc_space )
        for node in top_level_nodes:
            node_names = self.get_node_names(calc_space, node.Iterator() )
            child_node_names.append( node_names )
        return child_node_names


def getValidPorfoliosList(calc_type):
    """get all valid portfolios for calculation type"""
    if is_standard_calc_type(calc_type):
        criteria = 'AdditionalInfo.FRTB_SA_Eligible'
    elif is_VaR_calc_type(calc_type):
        criteria = 'AdditionalInfo.VaR_Eligible'
    else:
        return []
        
    asql_query = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND')
    #asql_query.AddAttrNode('AdditionalInfo.Portfolio_Status','EQUAL','Active')
    asql_query.AddAttrNode(criteria, 'EQUAL', 1)
    return [port.Name() for port in asql_query.Select()]
    
    
def getOpenPosFromPortfolio(portfolio_name):
    """get all open positions for a portfolio"""
    portfolio   = acm.FPhysicalPortfolio[ portfolio_name ]
    calc_space  = acm.Calculations().CreateCalculationSpace( context, sheet_type )
    top_node    = calc_space.InsertItem( portfolio )
    calc_space.Refresh()
    row_manager = RowManager()
    return [portfolio_name, row_manager.get_node_names_from_calc_space( calc_space )[0][0]]


def getValidPositionsFromPortfolios(calc_type, portfolio_exceptions, pos_file_directory, pos_file_directory_full_name):
    """loop through valid portfolios and get all open positions"""
    prf_list      = []
    prf_exception = []
    val_port_list = getValidPorfoliosList(calc_type)
    
    createOuputDir(pos_file_directory)
    
    for port in portfolio_exceptions:
        prf_exception.append(port.Name())
        if port.Name() in val_port_list:
            val_port_list.remove(port.Name())
            logger.info('==> Removing exception portfolio from list: %s '%(port.Name()))
    
    #Get Valid positions for valid portfolios not in exclusions list
    with open(pos_file_directory_full_name, 'wb') as outFile:
        w = csv.writer(outFile)
        for prf in val_port_list:
            try:
                logger.info('==> Identifying Valid/Open Positions for Porfolio: %s'%(prf))
                x = getOpenPosFromPortfolio(prf)
                w.writerow(x)
            except Exception, e:
                logger.error('Exception in identifying Valid/Open Positions for Porfolio: %s'%(prf))
                w.writerow([prf, e])
                logger.error(e)
                continue
                
    #Add exclusions list to rank file
    with open(pos_file_directory_full_name, 'ab') as outFile:
        w = csv.writer(outFile)
        for prf in prf_exception:
            logger.info('==> Adding Portfolio - %s in exception list to positions file.'%(prf))
            x = [prf, 'Exception']
            w.writerow(x)

""" ---------------- Rank Porfolios ---------------- """

def rankPortfolios(position_file_directory):
    """loop through instruments in valid portfolios file and create a dictionary with cost of calculation weights per portfolio"""
    rank_dict    = {}
    weight_dict  = {'Swap':50, 'Curr':2, 'Stock':1, 'CurrSwap':50, 'Bond':20, 'Bill':2, 'FRA':2, 'Option':10, 
                    'CreditDefaultSwap':50, 'Deposit':2, 'IndexLinkedSwap':50,'CFD':2}
    
    with open(position_file_directory, 'rb') as f:
        rFile = csv.reader(f)
        for row in rFile:
            prf = row[0]
            ins_list = row[1]
            if ins_list == '[]':
                rank_dict[prf] = 0
            elif ins_list == 'Exception':
                rank_dict[prf] = -10
            else:
                ins_list = ins_list.replace("[", "")
                ins_list = ins_list.replace("]", "")
                ins_list = ins_list.replace(" ", "")
                ins_list = ins_list.replace("'", "")
                ins_list = ins_list.split(",")
                rank_dict[prf] = 0
                for ins in ins_list:
                    ins_obj        = acm.FInstrument[ins]
                    curr_pair_obj  = acm.FCurrencyPair[ins]
                    if ins_obj:
                        ins_type = ins_obj.InsType()
                        if ins_type in rank_dict.keys():
                            rank_dict[prf] += weight_dict[ins_type]
                        else:
                            rank_dict[prf] += 1
                    elif curr_pair_obj:
                        rank_dict[prf] += weight_dict['Curr']
                    else:
                        logger.info('==> Ranking Portfolio: %s.'%(prf))
    return rank_dict


def qfManipulation(filter_name, new_criteria, _field, qf_dict):
    """update a exsting query folder's node with new criteria"""
    query = qf_dict[filter_name]
    nodes = query.AsqlNodes()
    if _field == 'Portfolio': ins_node = nodes[1]
    if _field == 'Regulatory Classification': ins_node = nodes[2]
    
    ins_nodes_array = ins_node.AsqlNodes()    
    if ins_node.AsqlNodes()[0].AsqlValue() == None:
        ins_node.AsqlNodes()[0].AsqlValue(new_criteria)
    else:
        if _field == 'Regulatory Classification':
            ins_node.AsqlNodes()[0].AsqlValue(new_criteria)
        else:
            new_node = ins_nodes_array[0].Clone()
            new_node.AsqlValue(new_criteria)
            new_node.Commit()
            ins_nodes_array.Add(new_node)
    logger.info('==> Sucessfully Added Portfolio: %s to %s.'%(new_criteria, filter_name))


def createQfs(master_Qf, qf_dict):
    """create child query folders based on a saved master query folder"""
    for qf_name in qf_dict.keys():
        qf = master_Qf.Clone()
        qf.Name(qf_name)
        qf.Query(qf_dict[qf_name])
        qf.AutoUser(False)
        qf.Commit()
        logger.info('==> Commited Query Folder: %s.'%(qf_name))


def removeQf(qf_prefix):
    """remove all existing queries folders"""
    sql = """select name
        from TextObject
        where type = 'FASQL Query'
        and name like '%s'"""%(qf_prefix + '%')

    for (qf,) in ael.asql(sql, 1)[1][0]:
        qFolder = acm.FStoredASQLQuery[qf]
        try:
            qFolder.Delete()
            logger.info('==> Removed Query Folder: %s.'%(qf))
        except:
            logger.error('==> Failed to remove Query Folder: %s.'%(qf))
            continue


def generatePrefix(calc_type):
    """return a prefix to be used for queries"""
    var_query_prefix  = 'VaR_Historical'
    frtb_query_prefix = 'FRTB_Main'
    
    if is_standard_calc_type(calc_type):
        return frtb_query_prefix
    elif is_VaR_calc_type(calc_type):
        return var_query_prefix
    else:
        return ''


def removeAllQFBasedOnCalcType(calc_type):
    if is_standard_calc_type(calc_type):
        qf_prefix = generatePrefix(calc_type)
        removeQf(qf_prefix)


def loopPortsAndCreateQueries(ord_rank_dict, num_partitions, master_query, qf_prefix):
    """ Perform round robin allocation with even distribution of portfolios to query folders"""
    qf_dict = {}
    num_prf       = len(ord_rank_dict)
    prf_list      = ord_rank_dict.keys()
    i = 0
    direction = 1
    
    logger.info('Ranking Valid Portfolios')
    for j in range(num_prf):
        prf_name = prf_list[j]
        i = i + 1*direction
        
        qf_name = qf_prefix + '_Partition_' + str(i)
        if qf_name not in qf_dict:
            qf_dict[qf_name] = master_query.Query()
            
        qfManipulation(qf_name, prf_name, 'Portfolio', qf_dict)
        
        if qf_prefix.__contains__('Banking'):
            qfManipulation(qf_name, 'Banking', 'Regulatory Classification', qf_dict)
        elif qf_prefix.__contains__('Trading'):
            qfManipulation(qf_name, 'Trading', 'Regulatory Classification', qf_dict)
            
        if direction == 1 and i == num_partitions and j < num_prf + 1:
            direction = -1
            i = i + 1
            continue
 
        if direction == -1 and i > 0 and j < num_prf + 1 :
            if i == 1: 
                i = 0
                direction = 1
        j += 1
        
    createQfs(master_query, qf_dict)


def assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, master_query, position_file_directory, sub_type = None):
    """round robin queries folders and assign them to a query folder"""
    rank_dict     = rankPortfolios(position_file_directory)
    qf_prefix     = generatePrefix(calc_type)
    
    #Loop through FRTB portofolios, split them by Trading and Banking and strip out exclusions per Book Type.
    banking_rank_dict = {}
    trading_rank_dict = {}

    for prf_key in rank_dict:
        prf         = acm.FPhysicalPortfolio[prf_key]
        if prf :
            if not(is_VaR_calc_type(calc_type) and prf.Oid() in portfolio_exlusion_list):
                # Exclude portfolios
                reg_class   = prf.AdditionalInfo().Reg_Classification()
                
                if reg_class and reg_class == 'Banking':
                    banking_rank_dict[prf_key] = rank_dict[prf_key]
                elif reg_class and reg_class == 'Trading':
                    trading_rank_dict[prf_key] = rank_dict[prf_key]
                else:
                    logger.error('==> Porfolio does not have a valid regulatory classification and will not be assigned to a query folder. Portoflio name: %s.'%(prf_key))
            
    ord_rank_banking_dict = collections.OrderedDict(sorted(banking_rank_dict.items(), key=lambda t:-t[1]))
    ord_rank_trading_dict = collections.OrderedDict(sorted(trading_rank_dict.items(), key=lambda t:-t[1]))
    ord_rank_trading_static_dict = collections.OrderedDict(sorted(trading_rank_dict.items(), key=lambda t:-t[1]))
    banking_exp_dict      = {}
    trading_exp_dict      = {}
    
    #Strip out banking portfolio exceptions
    for prf_key in ord_rank_banking_dict:
        if ord_rank_banking_dict[prf_key] == -10:
            banking_exp_dict[prf_key] = ord_rank_banking_dict[prf_key]
            del ord_rank_banking_dict[prf_key]
            
    #Strip out trading portfolio exceptions
    for prf_key in ord_rank_trading_dict:
        if ord_rank_trading_dict[prf_key] == -10:
            trading_exp_dict[prf_key] = ord_rank_trading_dict[prf_key]
            del ord_rank_trading_dict[prf_key]
    
    #Combine all the non exception portfolios
    combined_non_exp_dict = ord_rank_banking_dict.copy()
    combined_non_exp_dict.update(ord_rank_trading_dict)
    
    #Combine all exception portfolios
    combined_exp_dict = banking_exp_dict.copy()
    combined_exp_dict.update(trading_exp_dict)
        
    if is_VaR_calc_type(calc_type):
        #Loop through order valid VAR Banking portfolios and add them to queries.
        prefix = '%s_%s' %(qf_prefix, 'Banking')
        removeQf(prefix)
        loopPortsAndCreateQueries(ord_rank_banking_dict, num_tasks, master_query, prefix)
        
        #Loop through order valid VAR Banking Exception portfolios and add them to queries.
        prefix = '%s_%s_%s' %(qf_prefix, 'Banking', 'Exception')
        removeQf(prefix)
        loopPortsAndCreateQueries(banking_exp_dict, num_cores, master_query, prefix)
        
        #Loop through order valid VAR Trading portfolios and add them to queries.
        prefix = '%s_%s' %(qf_prefix, 'Trading')
        removeQf(prefix)
        loopPortsAndCreateQueries(ord_rank_trading_dict, num_tasks, master_query, prefix)
        
        #Loop through order valid VAR Trading Exception portfolios and add them to queries.
        prefix = '%s_%s_%s' %(qf_prefix, 'Trading', 'Exception')
        removeQf(prefix)
        loopPortsAndCreateQueries(trading_exp_dict, num_cores, master_query, prefix)
    elif is_standard_calc_type(calc_type):
        if sub_type == 'Combined':
            #Loop through order valid FRTB SA non exception portfolios and add them to queries.
            prefix = '%s_%s' %(qf_prefix, sub_type)
            loopPortsAndCreateQueries(combined_non_exp_dict, num_tasks, master_query, prefix)
            
            #Loop through order valid FRTB SA exception portfolios and add them to queries.
            prefix = '%s_%s_%s' %(qf_prefix, sub_type, 'Exception')
            loopPortsAndCreateQueries(combined_exp_dict, num_tasks, master_query, prefix)
        elif sub_type in ('FX', 'Other'):
            #Loop through order valid FRTB SA Banking portfolios and add them to queries.
            riskClass_prefix = '%s_%s_%s' %(qf_prefix, sub_type, 'Banking')
            loopPortsAndCreateQueries(ord_rank_banking_dict, num_tasks, master_query, riskClass_prefix)
            
            #Loop through order valid FRTB SA Banking Exception portfolios and add them to queries.
            riskClass_prefix = '%s_%s_%s_%s' %(qf_prefix, sub_type, 'Banking', 'Exception')
            loopPortsAndCreateQueries(banking_exp_dict, num_tasks, master_query, riskClass_prefix)
            
            #Loop through order valid FRTB SA Trading portfolios and add them to queries.
            riskClass_prefix = '%s_%s_%s' %(qf_prefix, sub_type, 'Trading')
            loopPortsAndCreateQueries(ord_rank_trading_dict, num_tasks, master_query, riskClass_prefix)
            
            #Loop through order valid FRTB SA Trading Exception portfolios and add them to queries.
            riskClass_prefix = '%s_%s_%s_%s' %(qf_prefix, sub_type, 'Trading', 'Exception')
            loopPortsAndCreateQueries(trading_exp_dict, num_tasks, master_query, riskClass_prefix)
        elif sub_type in ('DRC', 'RRAO'):
            #Loop through order valid FRTB SA Trading portfolios and add them to queries.
            prefix = '%s_%s' %(qf_prefix, sub_type)
            loopPortsAndCreateQueries(ord_rank_trading_static_dict, num_tasks, master_query, prefix)
            
""" ---------------- Check Queries ---------------- """

def comparePortLists(valid_ports, query_ports):
    """compare valid portfolios list to portfolios in created queries folders"""
    missing = 0
    missing_list = []
    for port in valid_ports:
        if port not in query_ports:
            missing +=1
            missing_list.append(port)
            logger.info("==> Port Missing from Queries: %s" %(port))
    logger.info("There are %s valid portfolios missing from newly created queries" %(missing))
    return missing_list


def getQueryFolders(qf_prefix):
    """get all query folders based on calculation type"""
    queries = []
    sql = """select name
        from TextObject
        where type = 'FASQL Query'
        and name like '%s'"""%(qf_prefix + '%')

    for (qf,) in ael.asql(sql, 1)[1][0]:
        qFolder = acm.FStoredASQLQuery[qf]
        queries.append(qFolder)
    
    return queries


def getAllPortsInQueryList(queries_list):
    """extract portfolios from query nodes"""
    query_port_list= []
    
    for query in queries_list:
        asql_query = query.Query()
        nodes      = asql_query.AsqlNodes()
        
        for node in nodes:
            
            if node.StringKey() == 'Grouped filter...':
                c_nodes = node.AsqlNodes()
                
                for c_node in c_nodes:
                    if c_node.StringKey() == 'FASQLAttrNode':
                        query_port_list.append(str(c_node.AsqlValue()))

    return query_port_list


def checkQueries(calc_type, sub_type = None):
    """check that all valid portfolios have been allocated to a query folder"""
    ports           = getValidPorfoliosList(calc_type)
    prefix          = generatePrefix(calc_type)
    
    if sub_type != None:
        prefix = '%s_%s' %(prefix, sub_type)
    
    queries         = getQueryFolders(prefix)
    prfs_in_queries = getAllPortsInQueryList(queries)
    comparePortLists(ports, prfs_in_queries)
        

""" ---------------- Create Tasks ---------------- """

def createTasks(calc_type, pos_spec, hierarchy_name, rf_setup_name, var_name, var_period_type, var_type, horizon, output_dir, log_file_dir):
    """create task based on calculation type"""
    task_prefix      = generatePrefix(calc_type)
    frtb_sa_params   = {"CalcType":"Main","DRCEnable":"1","DateDir":"1","Extension":".csv","LogToConsole":"1","LogToFile":"0","Logfile":" ","Logmode":"2","OutputDir":"C:\FRTB\Front Arena Outbound","Overwrite":"1","PLActEnable":"1","PLActoneDayScenarioEndDate":"Today","PLActscenarioCalendar":"ZAR Johannesburg","Prefix":"FRTB_BANKING_SET1","RRAOEnable":"1","SBAEnable":"1","hierarchy":"FRTB SA Static Data","riskClassNames":"FX,Commodity,CSR (NS),CSR (S-C),Equity,GIRR","riskFactorSetup":"FRTB SA Risk Factors"}
    frtb_ima_params  = ''
    var_task_params  = {"Create directory with date":"True","ExportBenchmarkPrice":1,"LogToConsole":0,"LogToFile":0,"Logmode":"2", "VaR File Name":"VaR","batchSize":2000,
                        "clean_pl_source":"Hypothetical","column_name_Bucket Shift Sensitivity":"Interest Rate Yield Delta Bucket","column_name_Parallel Shift Sensitivity":"Portfolio Delta Yield",
                        "column_name_Risk Factor":"Position Delta Per Equity Price Risk Factor","column_name_Stress":"Portfolio Theoretical Total Profit and Loss", "column_name_Stress Grid":"Portfolio Theoretical Total Profit and Loss",
                        "column_name_Twist Sensitivity":"Portfolio Delta Yield", "column_name_Value at Risk":"Portfolio Theoretical Total Profit and Loss", "output_dir":"/services/frontnt/Task/VAR/PeriodType",
                        "positionSpec":"VaR","positionSpecForBookTags":"Desk/PrfName/InsName/Cpty/TradeCurr",
                        "rateFileOutputName":"Rate","riskFactors":"InterestRate","runVaRReports":1,
                        "scenario_count_file_name":"scenario_count.dat", "scenario_dates_file_name":"scenario_dates.dat", 
                        "total_pl_source": "Total", "vaRHistory":"520d", "var_riskFactorSetup":"VaR Risk Factors", \
                        "var_Scenarios":"PeriodType_Equity_All,PeriodType_FX_All,PeriodType_IR_All,PeriodType_CMD_All,PeriodType_INF_All,PeriodType_CR_All,PeriodType_Total",
                        "yield_curves_parallel":"ZAR-BOND-Curve","yield_curves_timebucket":"ZAR-BOND-Curve","yield_curves_twist":"ZAR-BOND-Curve", "time_buckets":"-1","twist_scenarios":"1d shift",
                        "stored_Scenarios":"PeriodType_Equity_All,PeriodType_FX_All,PeriodType_IR_All,PeriodType_CMD_All,PeriodType_INF_All,PeriodType_CR_All,PeriodType_Total",
                        "var_type":"", "stress_Scenarios":"-30 to+30 market price", "stress_grid_file":"StressGrid", "stress_grid_scenarios":"-30 to+30 market price",
                        "stress_name":"Spot and Volatility Grid",  "stress_name_parallel":"Parallel Shift",  "stress_name_timebucket":"Time Bucket Shift",  "stress_type":"Test"}
    mrval_task_params = {'BookTagsFile':'Book Tags.csv','Create directory with date':'TRUE','ExportBenchmarkPrice':'1','Instruments_MarketData':'','LogToConsole':'1','LogToFile':'0','Logfile':'C:\FRTB\Front Arena Outbound\FRTB_MarketValue_Banking_Partition_1.log','Logmode':'2','MailList':'','Output File Prefix':'FRTB_MarketValue_Banking_Partition_1','Overwrite if file exists':'TRUE','PL File Name':'ProfitAndLoss','ReportMessageType':'Full Log','Risk Factor File Name':'RiskFactorEquityPriceDelta','SendReportByMail':'0','Stress File Name':'Stress','TradeTagsFile':'Trade Tags.aap','VaR File Name':'VaR','batchSize':'200','bucket_shift_file':'IRDeltaBuckets','clean_pl_source':'Hypothetical','column_name_Bucket Shift Sensitivity':'Interest Rate Yield Delta Bucket','column_name_Custom':'Portfolio Delta Yield Full Per Currency','column_name_Greeks':'Portfolio Theoretical Total Profit and Loss','column_name_Parallel Shift Sensitivity':'Portfolio Delta Yield','column_name_Risk Factor':'Position Delta Per Equity Price Risk Factor','column_name_Stress':'Portfolio Theoretical Total Profit and Loss','column_name_Stress Grid':'Portfolio Theoretical Total Profit and Loss','column_name_Twist Sensitivity':'Portfolio Delta Yield','column_name_Value at Risk':'Portfolio Theoretical Total Profit and Loss','creditDayCount':'','creditFrequency':'','creditOutputFile':'CreditDelta','creditRateType':'','curve_twist_file':'IRDeltaTwists','customFileName':'Custom','customWriter':'VectorWriter','daily_pl_source':'DailyTotal','decay_factor':'','decay_factor_file_name':'decay_factor.dat','distributedCalculations':'0','exportName':'ALL-SWAP,100bp Per Currency','greeks_file':'Market_Value','horizon':'1d','maxCalcTime':'10','measurement_parallel_shift':'Delta','measurement_timebucket':'Delta','measurement_twist':'Delta','measures_Greeks':'Market Value','output_dir':'C:\FRTB\Front Arena Outbound','parallel_shift_file':'IRDeltaParallel','plExplainOutputFile':'Sens','portfolios':'','positionSpec':'MarketValue-FRTB Desk/MinorDesk/ Ins/InsType/Port/Curr/Cpty','positionSpecForBookTags':'','rateFileOutputName':'Rate','riskFactors':'InterestRate','runBookAndTrdTagReports':'0','runBucketShiftReports':'0','runCreditReport':'0','runCustomReports':'0','runGreekReports':'1','runMarketDataReport':'0','runPLExplainReport':'0','runParallelShiftReports':'0','runPnLReports':'0','runRiskFactorReports':'0','runStressGridReports':'0','runStressReports':'0','runTwistReports':'0','runVaRReports':'0','scenario_count_file_name':'scenario_count.dat','scenario_dates_file_name':'scenario_dates.dat','storedASQLQueries':'FRTB_Main_Banking_Partition_1','stress_Scenarios':'','stress_grid_file':'StressGrid','stress_grid_scenarios':'','stress_name':'Spot and Volatility Grid','stress_name_parallel':'Parallel Shift','stress_name_timebucket':'Time Bucket Shift','stress_type':'','timebucket_name_MarketData':'','timebucket_name_PLExplain':'','time_buckets':'','total_pl_source':'Total','tradeFilters':'','twist_scenarios':'','vaRHistory':'','var_Scenarios':'','var_type':'','volatility_MarketData':'','yieldCurve_MarketData':'','yieldCurve_PLExplain':'','yield_curves_parallel':'','yield_curves_timebucket':'','yield_curves_twist':''}
    check_task_params = {'DateDir':'1','esfcScenarioFile':'','esrsScenarioFile':'','Extension':'.csv','hierarchy':'FRTB SA Static Data','imaRFSetup':'FRTB SA Risk Factors','Logmode':'2','LogToConsole':'0','LogToFile':'0','nmrfScenarioFile':'','OutputDir':'/services/frontnt/Task','performCompletenessCheck':'1','performMappingCheck':'0','performScenarioCheck':'0','plScenarioFile':'','rFSetup':'FRTB SA Risk Factors','rfSetupComp':'FRTB SA Risk Factors','tradeQueries':'FRTB_Main_Banking_Exception_Partition_1','outputPrefix':'FRTB_Main_Banking_Exception_Partition_1'}
  
  
    sql = """select name
        from TextObject
        where type = 'FASQL Query'
        and name like '%s'"""%(task_prefix + '%')

    query_names=[]
    for (qf,) in ael.asql(sql, 1)[1][0]:
        if qf != task_prefix:
            query_names.append(qf)
        
    query_names.sort(key = lambda x: int(x.split("_")[-1]))
    
    if calc_type == 'FRTB SA':
        for qf in query_names:
            if qf.__contains__('Combined'):
                #Create MV Export tasks
                mv_task = acm.FAelTask[qf + "_MV_SERVER"]
                if mv_task:
                    mv_task.Delete()
                    logger.info("Removed task: %s_MV_SERVER" %(qf))
                
                task = acm.FAelTask()
                task.Name(qf + "_MV_SERVER")
                task.ModuleName("FArtiQMarketRiskExport")
                task.ContextName("Standard")
                task_params = task.Parameters()
                for key, val in mrval_task_params.iteritems():
                    task_params.AtPutStrings(key, val)
                    
                task_params.AtPutStrings("storedASQLQueries", qf)
                log_file      = log_file_dir + "/%s.log" % (qf + "_MV_SERVER")

                task_params.AtPutStrings("positionSpec", pos_spec)
                task_params.AtPutStrings("Output File Prefix", qf)
                task_params.AtPutStrings("Logfile", log_file)
                task_params.AtPutStrings("output_dir", output_dir)
                task.Parameters(task_params)
                task.Commit()
                logger.info("Commited task: %s" %(task.Name()))
                
                #Create Risk Factor Check Tasks
                task = acm.FAelTask[qf + "_Check_SERVER"]
                if task:
                    task.Delete()
                    logger.info("Removed task: %s_Check_SERVER" %(qf))
                
                check_task = acm.FAelTask[qf + "_Check_SERVER"]
                if check_task:
                    check_task.Delete()
                    logger.info("Removed task: %s_Check_SERVER" %(qf))
                
                task = acm.FAelTask()
                task.Name(qf + "_Check_SERVER")
                task.ModuleName("FRTBConfigValidation")
                task.ContextName("Standard")
                task_params = task.Parameters()
                for key, val in check_task_params.iteritems():
                    task_params.AtPutStrings(key, val)
                    
                task_params.AtPutStrings("tradeQueries", qf)
                log_file      = log_file_dir + "/%s.log" % (qf + "_Check_SERVER")

                task_params.AtPutStrings("hierarchy", pos_spec)
                task_params.AtPutStrings("rFSetup", pos_spec)
                task_params.AtPutStrings("outputPrefix", qf)
                task_params.AtPutStrings("OutputDir", output_dir)
                task.Parameters(task_params)
                task.Commit()
                logger.info("Commited task: %s" %(task.Name()))
            else:
                #Create SA Export tasks
                task = acm.FAelTask[qf + "_SERVER"]
                if task:
                    task.Delete()
                    logger.info("Removed task: %s_SERVER" %(qf))
                
                task = acm.FAelTask()
                task.Name(qf + "_SERVER")
                task.ModuleName("FRTBSAExport")
                task.ContextName("Standard")
                task_params = task.Parameters()
                for key, val in frtb_sa_params.iteritems():
                    task_params.AtPutStrings(key, val)
                    
                task_params.AtPutStrings("Trade Queries", qf)
                log_file      = log_file_dir + "/%s.log" % (qf + "_SERVER")
                
                if qf.__contains__('DRC'):
                    logger.info('Creating Tasks for DRC Calculation.')
                    task_params.AtPutStrings("riskClassNames", "FX,Commodity,CSR (NS),CSR (S-C),Equity,GIRR")
                    task_params.AtPutStrings("SBAEnable", "False")
                    task_params.AtPutStrings("DRCEnable", "True")
                    task_params.AtPutStrings("RRAOEnable", "False")                
                elif qf.__contains__('RRAO'):
                    logger.info('Creating Tasks for RRAO Calculation.')
                    task_params.AtPutStrings("riskClassNames", "FX,Commodity,CSR (NS),CSR (S-C),Equity,GIRR")
                    task_params.AtPutStrings("SBAEnable", "False")
                    task_params.AtPutStrings("DRCEnable", "False")
                    task_params.AtPutStrings("RRAOEnable", "True")
                elif qf.__contains__('Banking'):
                    if qf.__contains__('FX'):
                        logger.info('Creating Tasks for RiskClass FX for the Banking Book.')
                        task_params.AtPutStrings("riskClassNames", "FX")
                        task_params.AtPutStrings("SBAEnable", "True")
                        task_params.AtPutStrings("DRCEnable", "False")
                        task_params.AtPutStrings("RRAOEnable", "False")
                    elif qf.__contains__('Other'):
                        logger.info('Creating Tasks for all Risk Callses other than FX in the Banking Book.')
                        task_params.AtPutStrings("riskClassNames", "Commodity")
                        task_params.AtPutStrings("SBAEnable", "True")
                        task_params.AtPutStrings("DRCEnable", "False")
                        task_params.AtPutStrings("RRAOEnable", "False")
                    else:
                        continue
                elif qf.__contains__('Trading'):
                    if qf.__contains__('FX'):
                        logger.info('Creating Tasks for RiskClass FX and Equity in the Trading Book.')
                        task_params.AtPutStrings("riskClassNames", "FX,Equity")
                        task_params.AtPutStrings("SBAEnable", "True")
                        task_params.AtPutStrings("DRCEnable", "False")
                        task_params.AtPutStrings("RRAOEnable", "False")
                    elif qf.__contains__('Other'):
                        logger.info('Creating Tasks for all Risk Classes other than FX and Equity in the Trading Book.')
                        task_params.AtPutStrings("riskClassNames", "Commodity,CSR (NS),CSR (S-C),GIRR")
                        task_params.AtPutStrings("SBAEnable", "True")
                        task_params.AtPutStrings("DRCEnable", "False")
                        task_params.AtPutStrings("RRAOEnable", "False")
                    else:
                        continue

                task_params.AtPutStrings("PLActEnable", "False")
                task_params.AtPutStrings("Overwrite", "True")
                task_params.AtPutStrings("hierarchy", hierarchy_name)
                task_params.AtPutStrings("riskFactorSetup", rf_setup_name)
                task_params.AtPutStrings("Position Specification", pos_spec)
                task_params.AtPutStrings("Logfile", log_file)
                task_params.AtPutStrings("OutputDir", output_dir)
                task_params.AtPutStrings("Prefix", qf)
                task.Parameters(task_params)
                task.Commit()
                logger.info("Commited task: %s" %(task.Name()))
            
    elif calc_type == 'FRTB IMA':
        #Add Logic for IMA Tasks
        pass
        
    elif is_VaR_calc_type(calc_type):
        partition_counter = 0
        for qf in query_names:
            task_name = qf.replace("VaR_Historical", "VaR_Historical_%s" % var_period_type)#add switch for DVaR and DVaR
            task = acm.FAelTask[task_name]
            if task:
                task.Delete()
                logger.info("Removed task: %s" %(task_name))

            task = acm.FAelTask()
            task.Name(qf)
            task.ModuleName("FArtiQMarketRiskExport")
            task.ContextName("Standard")
            task_params = task.Parameters()
            for key, val in var_task_params.iteritems():
                if key in ("var_Scenarios", "stored_Scenarios", "output_dir"):
                    period_lookup = {"Daily":"DVaR","Stressed":"SVaR","10Day":"10Day","PeriodTest":"PeriodTest"}
                    val = val.replace("PeriodType", period_lookup[var_period_type])
                task_params.AtPutStrings(key, val)
                
            task_params.AtPutStrings("storedASQLQueries", qf)
            log_file        = log_file_dir + "/%s_%s.log" % (qf, partition_counter)
            output_prefix   = qf + "Partition_%s_" % (partition_counter)
            task_params.AtPutStrings("scenario_count_file_name", "scenario_count.csv")
            task_params.AtPutStrings("scenario_dates_file_name", "scenario_dates.csv")

            task_params.AtPutStrings("VaR File Name", var_name)
            task_params.AtPutStrings("positionSpec", pos_spec)
            task_params.AtPutStrings("positionSpecForBookTags", pos_spec)
            task_params.AtPutStrings("vaRHistory", horizon)
            task_params.AtPutStrings("var_riskFactorSetup", rf_setup_name)
            task_params.AtPutStrings("var_type", var_type)
            task_params.AtPutStrings("var_period_type", var_period_type)
            task_params.AtPutStrings("OutputDir", output_dir)
            task_params.AtPutStrings("Output File Prefix", task_name)
            task_params.AtPutStrings("Overwrite if file exists", "True")
            log_file        = log_file_dir + "/%s.log" % qf.replace("VaR_Historical", "VaR_Historical_%s" % var_period_type)
            task_params.AtPutStrings("Logfile", log_file)
            task.Name(task_name)            
            task.Parameters(task_params)
            task.Commit()
            logger.info("Commited task: %s" %(task.Name()))
            partition_counter = partition_counter + 1

""" ---------------- AEL Task ---------------- """

def getCaller():
    """returns the caller of the caller of this method (hence 3rd element in stack)"""
    frame = inspect.stack()[2]
    return inspect.getmodule(frame[0])
    
def getLoggingAelVariables(caller, log_filename):
    """define ael logging variables"""
    def logfile_cb(index, fieldValues):
        caller.ael_variables.log_file.enable(
            fieldValues[index],
            'You have to check Log To File to be able to select a Logfile.'
        )
        return fieldValues

    logFileSelection = FRunScriptGUI.OutputFileSelection('All Files (*.*)|*.*||')
    logFileSelection.SelectedFile = os.path.join('C:\\', 'temp', log_filename)
    tt_log_mode   = 'Defines the amount of logging produced.'
    tt_log_to_con = (
        'Whether logging should be done in the Log Console or not.'
    )
    tt_log_to_file = 'Defines whether logging should be done to file.'
    tt_log_file = (
        'Name of the logfile. Could include the whole path, c:\temp\...'
    )
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['log_mode',
            'Logmode_Logging',
            'int', [1, 2, 3, 4], 1,
            1, 0, tt_log_mode],
        ['log_to_console',
            'Log to console_Logging',
            'int', [0, 1], 1,
            1, 0, tt_log_to_con],
        ['log_to_file',
            'Log to file_Logging',
            'int', [0, 1], 0,
            1, 0, tt_log_file, logfile_cb],
        ['log_file',
            'Logfile_Logging',
            logFileSelection, None, logFileSelection,
            0, 1, tt_log_file, None, None],
    ]
    return ael_variables

def getOutputAelVariables(caller):
    """define ael output variables"""
    '''
    def setPositionRankFileDirectory(index, fieldValues):
        if "Windows" in platform.platform():
            directory_operator = "\\"
        elif "Linux" in platform.platform():
            directory_operator = "/"
        
        file_path = '%s' %str(fieldValues[index])
        
        if caller.ael_variables.date_dir[4] == 1:
            file_path = '%s%s%s' %(file_path, directory_operator, str(acm.DateToday()))
        
        file_path = '%s%s%s%s' %(file_path, directory_operator, str(caller.ael_variables.position_file_name[4]), str(caller.ael_variables.extension[4]))
        
        fieldValues[6] = file_path
        
        return fieldValues
    '''
    tt_output_dir = (
        'Path to the directory where the reports should be '
        'created. Environment variables can be used for '
        'Windows (%VAR%) or Unix ($VAR).'
    )
    tt_extension = 'Extension used for output file names.'
    tt_date_dir  = (
        'Create a directory with the todays date as the directory name'
    )
    tt_positionl_file_name = (
        'Name of the valid position file that gets created by the Get Valid ' \
        'Position functionality and used by the Create Queries functionality.'
    )
    
    directorySelection = FRunScriptGUI.DirectorySelection()
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['output_dir',
            'Directory path_Output settings',
            directorySelection, None, directorySelection,
            1, 1, tt_output_dir, None, 1],
        ['position_file_name',
            'Position File Name_Output settings',
            'string', ['FRTB_Valid_Positions', 'VaR_Valid_Positions'], 
            None, 1, 0, tt_positionl_file_name],
        ['extension',
            'Output file extension_Output settings',
            'string', None, '.csv',
            1, 0, tt_extension],
        ['date_dir',
            'Create directory with todays date_Output settings',
            'int', [0, 1], 1,
            1, 0, tt_date_dir]
    ]
    return ael_variables

def getTaskAelVariables(caller):
    """define ael task variables"""
    def enableQueryFields(index, fieldValues):
        caller.ael_variables.num_tasks.enable(
        fieldValues[index],
        'Select "Create Queries" to enable relavant fields.'
        )
        caller.ael_variables.num_cores.enable(
        fieldValues[index],
        'Select "Create Queries" to enable relavant fields.'
        )
        caller.ael_variables.master_query.enable(
        fieldValues[index],
        'Select "Create Queries" to enable relavant fields.'
        )
        if fieldValues[0] in ['FRTB SA', 'FRTB IMA']:
            caller.ael_variables.sa_master_query_riskclass_fx.enable(
            fieldValues[index],
            'Select "Create Queries" to enable relavant fields.'
            )
            caller.ael_variables.sa_master_query_riskclass_other.enable(
            fieldValues[index],
            'Select "Create Queries" to enable relavant fields.'
            )
            caller.ael_variables.sa_master_query_drc.enable(
            fieldValues[index],
            'Select "Create Queries" to enable relavant fields.'
            )
            caller.ael_variables.sa_master_query_rrao.enable(
            fieldValues[index],
            'Select "Create Queries" to enable relavant fields.'
            )
            
        return fieldValues
        
    def enablePosFields(index, fieldValues):
        caller.ael_variables.portfolio_exceptions.enable(
        fieldValues[index],
        'Select "Create Queries" to enable relavant fields.'
        )
        
        return fieldValues
        
    def enableTaskFields(index, fieldValues):
        if fieldValues[0] in ['FRTB SA', 'FRTB IMA']:
            caller.ael_variables.position_spec.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.rf_setup.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.hierarchy.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.task_output_dir.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.task_log_dir.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            
        elif fieldValues[0] in ['VaR']:
            caller.ael_variables.position_spec.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.rf_setup.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.hierarchy.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.var_name.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.var_type.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.horizon.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.var_period_type.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.task_output_dir.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
            caller.ael_variables.task_log_dir.enable(
            fieldValues[index],
            'Select "Create Tasks" to enable relavant fields.'
            )
        return fieldValues
    
    def setPositionFileName(index, fieldValues):
        if fieldValues[index] == 'FRTB SA':
            fieldValues[22] = 'FRTB_Valid_Positions'
        elif fieldValues[index] == 'VaR':
            fieldValues[22] = 'VaR_Valid_Positions'
        else:
            fieldValues[22] = 'FRTB_Valid_Positions'
        
        return fieldValues
        
    input_file                = FRunScriptGUI.InputFileSelection(('CSV Files (*.csv)|*.csv'))
    tt_calc_type              = 'Select calculation base.'
    tt_get_val_pos            = 'Get all valid positions for valid porfolios (i.e. Portfolios where the add_info MR_Eligilble = True).'
    tt_create_queries         = 'Create Queries folders based on ranked portfolios.'
    tt_create_tasks           = 'Create tasks based on newly created queries.'
    tt_num_tasks              = 'Number of tasks and queries that will be created.'
    tt_num_cores              = 'Number of exception tasks will be based on the number of server cores.'
    tt_master_query           = 'Name of the Master Query Folder (containing selection criteria). For FRTB SA this represents the Combined Master Query Folder.'
    tt_sa_master_query_riskclass_fx    = 'Name of the Master Query Folder for FRTB SA RiskClass FX and Equity.'
    tt_sa_master_query_riskclass_other    = 'Name of the Master Query Folder for FRTB SA RiskClasses other than FX and Equity.'
    tt_sa_master_query_drc    = 'Name of the Master Query Folder for FRTB SA DRC calculation.'
    tt_sa_master_query_rrao   = 'Name of the Master Query Folder for FRTB SA RRAO calculation.'
    tt_port_exceptions        = 'List all portfolios that should be treated seperate for other ranked portflios.'
    tt_pos_spec               = 'Select a position spesification.'
    tt_rf_setup               = 'Select a risk factor spesification.'
    tt_hierarchy              = 'Select a risk factor hierarchy.'
    tt_var_name               = 'Provide a new to be used when created the VaR file.'
    tt_var_period_type        = 'Select a VaR Period type tag.'
    tt_var_type               = 'Select a VaR type tag.'
    tt_horizon                = 'Select a VaR horizon.'
    tt_task_output_dir        = 'Select a output directory used when creating tasks.'
    tt_task_log_dir           = 'Select a log directory used when creating tasks.'
    directorySelection        = FRunScriptGUI.DirectorySelection()
    
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['calc_type',
            'Calculation Type_Load Balancing',
            'string', ['FRTB SA', 'FRTB IMA', 'VaR'], None,
            1, 0, tt_calc_type, setPositionFileName, None],
        ['get_valid_postitions',
            'Get Valid Positions_Load Balancing',
            'int', [0, 1], 0,
            1, 0, tt_get_val_pos, enablePosFields],
        ['portfolio_exceptions',
            'List of Portfolio Exceptions_Load Balancing',
            acm.FPhysicalPortfolio, None, None,
            0, 1, tt_port_exceptions, None, None],
            
        ['create_queries',
            'Create Queries_Load Balancing',
            'int', [0, 1], 0,
            1, 0, tt_create_queries, enableQueryFields],
        ['num_cores',
            'Number of Server Cores_Load Balancing',
            'int', None, 16,
            0, 0, tt_num_cores, None, None],
        ['num_tasks',
            'Number of Queries/Tasks_Load Balancing',
            'int', None, 64,
            0, 0, tt_num_tasks, None, None],
        ['master_query',
            'Master Query Name_Load Balancing',
            acm.FStoredASQLQuery, None, None,
            0, 0, tt_master_query, None, None],
        ['sa_master_query_riskclass_fx',
            'SA Master Query Risk Class FX and Equity_Load Balancing',
            acm.FStoredASQLQuery, None, None,
            0, 0, tt_sa_master_query_riskclass_fx, None, False],
        ['sa_master_query_riskclass_other',
            'SA Master Query Risk Class Other_Load Balancing',
            acm.FStoredASQLQuery, None, None,
            0, 0, tt_sa_master_query_riskclass_other, None, False],
        ['sa_master_query_drc',
            'SA Master Query DRC Calc_Load Balancing',
            acm.FStoredASQLQuery, None, None,
            0, 0, tt_sa_master_query_drc, None, False],
        ['sa_master_query_rrao',
            'SA Master Query Name RRAO Calc_Load Balancing',
            acm.FStoredASQLQuery, None, None,
            0, 0, tt_sa_master_query_rrao, None, False],
        ['create_tasks',
            'Create Tasks_Load Balancing',
            'int', [0, 1], 0,
            1, 0, tt_create_tasks, enableTaskFields],
        ['position_spec',
            'Positions Spesification_Load Balancing',
            acm.FPositionSpecification, None, None,
            0, 0, tt_pos_spec, None, False],
        ['rf_setup',
            'Risk Factor Setup_Load Balancing',
            acm.FRiskFactorSetup, None, None,
            0, 0, tt_rf_setup, None, False],
        ['hierarchy',
            'Hierarchy_Load Balancing',
            acm.FHierarchy, None, None,
            0, 0, tt_hierarchy, None, False],
        ['var_name',
            'VaR File Name_Load Balancing',
            'string', None, 'VaR',
            0, 0, tt_var_name, None, False],
        ['var_period_type',
            'VaR Period Type_Load Balancing',
            'string', ["Daily", "Stressed", "10Day", "PeriodTest"], None,
            0, 0, tt_var_type, None, False],
        ['var_type',
            'VaR Type_Load Balancing',
            'string', ["Historic"], None,
            0, 0, tt_var_type, None, False],
        ['horizon',
            'VaR Horizon_Load Balancing',
            'string', ["1d", "250d", "520d"], None,
            0, 0, tt_horizon, None, False],
        ['task_output_dir',
            'Task Directory path_Load Balancing',
            directorySelection, None, directorySelection,
            0, 1, tt_task_output_dir, None, False],
        ['task_log_dir',
            'Task Log Directory path_Load Balancing',
            directorySelection, None, directorySelection,
            0, 1, tt_task_log_dir, None, False],
    ]
    return ael_variables
    
    
def createAelVariables(ael_vars_list, log_filename):
    """get all ael variables"""
    caller = getCaller()
    
    ael_vars_list.extend(getTaskAelVariables(
        caller=caller
    ))
    ael_vars_list.extend(getOutputAelVariables(
        caller=caller
    ))
    ael_vars_list.extend(getLoggingAelVariables(
        caller=caller, log_filename=log_filename
    ))
    ael_vars = FRunScriptGUI.AelVariablesHandler(
        ael_vars_list, caller.__name__
    )

    return ael_vars

def constructFileDirectory(directory, date_today_flag, file_name, extension):
    if "Windows" in platform.platform():
        directory_operator = "\\"
    elif "Linux" in platform.platform():
        directory_operator = "/"
    else:
        directory_operator = "/"
    
    file_directory = '%s' %str(directory)
    
    if date_today_flag:
        file_directory = '%s%s%s' %(file_directory, directory_operator, str(acm.DateToday()))
    
    file_name = '%s%s' %(file_name, extension)
    file_directory_fulll_name = '%s%s%s' %(file_directory, directory_operator, file_name)
    
    return file_name, file_directory, file_directory_fulll_name

log_name      = 'Load_Balancer'
ael_variables = createAelVariables([], log_name)
logger        = None

def ael_main(ael_output):
    get_valid_pos         = ael_output['get_valid_postitions']
    create_queries        = ael_output['create_queries']
    create_tasks          = ael_output['create_tasks']
    calc_type             = ael_output['calc_type']
    portfolio_exceptions  = ael_output['portfolio_exceptions']
    num_cores             = ael_output['num_cores']
    num_tasks             = ael_output['num_tasks']
    master_query          = ael_output['master_query']
    sa_master_query_riskclass_fx   = ael_output['sa_master_query_riskclass_fx']
    sa_master_query_riskclass_other   = ael_output['sa_master_query_riskclass_other']
    sa_master_query_drc   = ael_output['sa_master_query_drc']
    sa_master_query_rrao  = ael_output['sa_master_query_rrao']
    position_spec         = ael_output['position_spec']
    rf_setup              = ael_output['rf_setup']
    hierarchy             = ael_output['hierarchy']
    var_name              = ael_output['var_name']
    var_type              = ael_output['var_type']
    var_period_type       = ael_output['var_period_type']
    horizon               = ael_output['horizon']
    task_output_dir       = ael_output['task_output_dir']
    task_log_dir          = ael_output['task_output_dir']
    output_dir            = ael_output['output_dir']
    position_file_name    = ael_output['position_file_name']
    extension             = ael_output['extension']
    date_dir              = ael_output['date_dir']
    global logger   
    logger                = createDefaultLogger(log_name, ael_output)
    
    logger.info('Load Balancing Started\n' + '-'*75)
    
    pos_file_name, pos_file_directory, pos_file_directory_full_name = constructFileDirectory(str(output_dir), date_dir, position_file_name, extension)
    
    #Step 1: Get Valid Positions
    if get_valid_pos == 1:
        logger.info('Getting Valid Positions for calculation type: %s...'%(calc_type))
        logger.info('Writing Valid Portfolios and Position to: %s \n'%(str(output_dir)))
        getValidPositionsFromPortfolios(calc_type, portfolio_exceptions, pos_file_directory, pos_file_directory_full_name)
        logger.info('Finised Valid Position Extraction.\n' + '-'*75)

    #Step 2: Rank Portfolios and Create Queries
    if create_queries == 1:
        if is_standard_calc_type(calc_type):
            removeAllQFBasedOnCalcType(calc_type)
            logger.info('Starting Query Creation for calculation type: %s...'%(calc_type))
            logger.info('Starting Query Creation for Live Trades ...')
            assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, master_query, pos_file_directory_full_name, 'Combined')
            logger.info('Finished Query Creation.\n' + '-'*75)

            logger.info('Starting Query Folder Creation for Risk Class FX ...')
            assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, sa_master_query_riskclass_fx, pos_file_directory_full_name, 'FX')
            logger.info('Finished Query Creation.\n' + '-'*75)
            
            logger.info('Starting Query Folder Creation for Risk Class other than FX ...')
            assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, sa_master_query_riskclass_other, pos_file_directory_full_name, 'Other')
            logger.info('Finished Query Creation.\n' + '-'*75)
            
            logger.info('Starting Query Folder Creation for DRC Calc ...')
            assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, sa_master_query_drc, pos_file_directory_full_name, 'DRC')
            logger.info('Finished Query Creation.\n' + '-'*75)
            
            logger.info('Starting Query Folder Creation for RRAO Calc ...')
            assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, sa_master_query_rrao, pos_file_directory_full_name, 'RRAO')
            logger.info('Finished Query Creation.\n' + '-'*75)
        else:
            logger.info('Starting Query Creation for calculation type: %s...'%(calc_type))
            assignRankedPortfolioToQuery(calc_type, num_tasks, num_cores, master_query, pos_file_directory_full_name)
            logger.info('Finished Query Creation.\n' + '-'*75)

    #Step 3: Check that all portfolios where assigned to a query folder
        logger.info('Starting Query Check.')
        if is_standard_calc_type(calc_type):
            checkQueries(calc_type, 'Combined')
            checkQueries(calc_type, 'FX')
            checkQueries(calc_type, 'Other')
            checkQueries(calc_type, 'DRC')
            checkQueries(calc_type, 'RRAO')
        else:
            checkQueries(calc_type)
        logger.info('Finished Query Check.\n' + '-'*75)

    #Step 4: Create tasks
    if create_tasks == 1:
        logger.info('Starting Task Creation for calculation type: %s...'%(calc_type))
        createTasks(calc_type, position_spec.Name(), hierarchy.Name(), rf_setup.Name(), var_name, var_period_type, var_type, horizon, str(task_output_dir), str(task_log_dir))
        logger.info('Finished Task Creation.\n' + '-'*75)
