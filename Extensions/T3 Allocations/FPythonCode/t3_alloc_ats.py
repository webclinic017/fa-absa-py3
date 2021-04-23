import acm
from t3_alloc_logic import COMPOUND_PORTFOLIOS, STATE_CHART_NAME, get_process_object, log


DATE_TODAY = acm.Time().DateToday()
CALENDAR = acm.FCalendar['ZAR Johannesburg']
START_DATE = CALENDAR.AdjustBankingDays(DATE_TODAY, -2)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AllocationsAts(object, metaclass=Singleton):
    def __init__(self):
        self._state_chart = acm.FStateChart[STATE_CHART_NAME]
        self._bp_queue = []
        self._trade_sets = self.get_trade_sets(COMPOUND_PORTFOLIOS, START_DATE)
        self._business_processes = self._get_business_processes()
        self._processing_queue = [(key, None) for key in self._trade_sets.keys()]
        self._subscribe()
        log('ATS init finished.')

    def ServerUpdate(self, sender, aspect, entity):
        if entity.IsKindOf(acm.FTrade):
            prf_name = entity.Portfolio().Name()
            if prf_name in self._trade_sets:
                self._processing_queue.append((prf_name,
                                               entity.Instrument().Name()))
                bp_trade = self._trade_sets[prf_name].get_bp_trade(entity)
                is_valid = self._trade_sets[prf_name].is_trade_valid(entity)
                if (bp_trade and is_valid and not 
                        acm.BusinessProcess.FindBySubjectAndStateChart(
                        bp_trade, self._state_chart)):
                    self._bp_queue.append(bp_trade)
        elif entity.IsKindOf(acm.FBusinessProcess):
            trade = entity.Subject()
            prf_name = trade.Portfolio().Name()
            ins_name = trade.Instrument().Name()
            if (prf_name in self._trade_sets and 
                    (prf_name, ins_name) not in self._processing_queue):
                self._processing_queue.append((prf_name, ins_name))
    
    def process_trades(self):
        while self._processing_queue:
            portfolio_name, ins_name = self._processing_queue.pop(0)
            log('Processing portfolio: %s.' % portfolio_name)
            if portfolio_name in self._trade_sets:
                self._trade_sets[portfolio_name].process_trades(ins_name)
    
    def create_bps(self):
        while self._bp_queue:
            trade = self._bp_queue.pop(0)
            log('Checking BP of trade: %s.' % trade.Oid())
            bp = self._get_business_process(trade)
            if bp not in self._business_processes:
                self._business_processes.append(bp)
                bp.AddDependent(self)
            prf_name = trade.Portfolio().Name()
            if prf_name in self._trade_sets:
                self._processing_queue.append((prf_name, 
                                               trade.Instrument().Name()))
    
    def remove_all_subscriptions(self):
        for trade_process in self._trade_sets.values():
            trade_process.get_trades().RemoveDependent(self)
        
        for bp in self._business_processes:
            bp.RemoveDependent(self)
    
    def status(self):
        log('ATS running.')
    
    def _get_business_processes(self):
        business_processes = []
        for trade_process in self._trade_sets.values():
            for trade in trade_process.get_trades():
                bp_trade = trade_process.get_bp_trade(trade)
                is_valid = trade_process.is_trade_valid(trade)
                if not bp_trade or not is_valid:
                    continue
                bp = self._get_business_process(bp_trade)
                if not bp:
                    continue
                business_processes.append(bp)
        return business_processes
    
    def _get_business_process(self, trade):
        current_process = acm.BusinessProcess.FindBySubjectAndStateChart(
            trade, self._state_chart)
        if current_process:
            return current_process.First()
        return self._create_business_process(trade)
    
    def _create_business_process(self, trade):
        business_process = acm.BusinessProcess().InitializeProcess(
            trade, self._state_chart)
        try:
            business_process.Commit()
        except RuntimeError as err:
            log('ERROR: Failed to create business process: %s' % str(err))
            return None
        return business_process
    
    def _subscribe(self):
        for trade_process in self._trade_sets.values():
            trade_process.get_trades().AddDependent(self)
        
        for bp in self._business_processes:
            bp.AddDependent(self)
    
    @classmethod
    def get_trade_sets(cls, compound_names, start_date):
        trade_sets = {}
        for comp_name in compound_names:
            compound = acm.FCompoundPortfolio[comp_name]
            if not compound:
                continue
            for physical in compound.AllPhysicalPortfolios():
                portfolio_name = physical.Name()
                trade_process = get_process_object(portfolio_name, start_date)
                trade_sets[portfolio_name] = trade_process
                log('Init portfolio: %s' % portfolio_name)
        return trade_sets


def start():
    ats = AllocationsAts()
    log('ATS Started')


def stop():
    ats = AllocationsAts()
    ats.remove_all_subscriptions()
    log('ATS Finished')


def status():
    ats = AllocationsAts()
    ats.status()


def work():
    ats = AllocationsAts()
    ats.create_bps()
    ats.process_trades()
