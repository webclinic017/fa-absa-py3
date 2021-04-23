
import acm
import FAptReport
import FAptReportGenerate
import FAptReportUtils
import FAptUserPreferences
import importlib

class FPortfolioAptReport:

    def __init__(self, extensionObject):
        ui_trd_manager = extensionObject
        active_sheet = ui_trd_manager.ActiveSheet()
        self.selection = active_sheet.Selection().SelectedRowObjects()
        self.ael_variables = FAptReport.FAptReport().ael_variables
        self._init_parameters()
       
    def _init_parameters(self):
        self.parameters = dict((k[0], k[4]) for k in self.ael_variables)
        self.parameters['portfolio'] = acm.FArray()
        self.parameters['trade_filter'] = acm.FArray()
        self.parameters['grouper'] = acm.FArray()

    def _create_asql_query(self, trades):
        asql_query = acm.CreateFASQLQuery("FTrade", 'OR')
        for trd in trades:
            asql_query.AddOpNode('OR')
            asql_query.AddAttrNode('Oid', 'EQUAL', trd.Oid())
        return asql_query

    def _create_asql_query_folder(self, row_object, trades):
        asql_query_folder_name = '#'+row_object.StringKey() if row_object else "SELECTED POSITIONS"
        asql_query_folder = acm.FASQLQueryFolder()
        asql_query_folder.Name(asql_query_folder_name)
        asql_query = self._create_asql_query(trades)
        asql_query_folder.AsqlQuery(asql_query)
        return asql_query_folder

    def _row_object_class(self, row_object):
        return row_object.Class().StringKey()
        
    def _tradesBeforeDate(self, trades, cutOffDate):
        tradesBeforeDate = acm.GetFunction('tradesBeforeDate', 2)
        return tradesBeforeDate(trades, cutOffDate)
        
    def _get_grouper(self, row_object):
        top_row = None
        parent = row_object.Parent()
        while parent:
            top_row = parent
            parent = top_row.Parent()
        top_row = top_row if top_row else row_object
        return top_row.Grouping().Grouper()
        
    def _get_piat_params(self, row_object):
        portfolio = row_object.Portfolio()
        if portfolio.IsKindOf(acm.FPhysicalPortfolio):
            self.parameters['portfolio'].Add(portfolio)
        else:
            self.parameters['trade_filter'].Add(portfolio)
            
    def _get_miat_params(self, row_object, cutOffDate):
        trades = row_object.Trades()
        tradesBeforeDate = self._tradesBeforeDate(trades, cutOffDate).AsArray()
        query_folder = self._create_asql_query_folder(row_object, tradesBeforeDate)
        self.parameters['trade_filter'].Add(query_folder)
        
    def _get_siat_params(self, single_ins_and_trades, cutOffDate):
        if len(single_ins_and_trades) == 1:
            row_object = single_ins_and_trades[0]
            trades = row_object.Trades()
            tradesBeforeDate = self._tradesBeforeDate(trades, cutOffDate).AsArray()
            query_folder = self._create_asql_query_folder(row_object, tradesBeforeDate)
            self.parameters['trade_filter'].Add(query_folder)
        else:
            trades = [trd for row_object in single_ins_and_trades for trd in self._tradesBeforeDate(row_object.Trades(), cutOffDate).AsArray()]
            query_folder = self._create_asql_query_folder(None, trades)
            self.parameters['trade_filter'].Add(query_folder)

    def _get_parameters(self):
        single_ins_and_trades = []
        cutOffDate = acm.Time.DateValueDay()
        for row_object in self.selection:
            grouper = self._get_grouper(row_object)
            self.parameters['grouper'].Add(grouper)
            row_object_class = self._row_object_class(row_object)
            if row_object_class == 'FPortfolioInstrumentAndTrades':
                self._get_piat_params(row_object)
            elif row_object_class == 'FMultiInstrumentAndTrades':
                self._get_miat_params(row_object, cutOffDate)
            else:
                single_ins_and_trades.append(row_object)
        if single_ins_and_trades:
            self._get_siat_params(single_ins_and_trades, cutOffDate)
        return self.parameters
        
    def run(self):
        #user_preferences = FAptUserPreferences.FAptUserPreferences()
        #user_preferences.create()
        parameters = self._get_parameters()
        FAptReport.ael_main(parameters)
        
def apt_reload():
    import FAptReportCommon
    importlib.reload(FAptReportCommon)
    import FAptReportUtils
    importlib.reload(FAptReportUtils)
    import FAptTest
    importlib.reload(FAptTest)
    import FAptIdRecon
    importlib.reload(FAptIdRecon)
    import FAptIdRecon
    importlib.reload(FAptIdRecon)
    import FAptFinancial
    importlib.reload(FAptFinancial)
    import FAptSetup
    importlib.reload(FAptSetup)
    import FPortfolioAptReport
    importlib.reload(FPortfolioAptReport)
    import FReportMapperClasses
    importlib.reload(FReportMapperClasses)
    import FReportParser
    importlib.reload(FReportParser)
    import FAptReportGenerate
    importlib.reload(FAptReportGenerate)
    import FAptReport
    importlib.reload(FAptReport)
    import FAptLauncher
    importlib.reload(FAptLauncher)
    import FAptUserPreferences
    importlib.reload(FAptUserPreferences)
            
def startAptPro(eii):
    apt_reload()
    apt_report = FPortfolioAptReport(eii.ExtensionObject())
    apt_report.run()
    

            
