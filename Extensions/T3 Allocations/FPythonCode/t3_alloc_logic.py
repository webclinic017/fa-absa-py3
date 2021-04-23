import acm
from collections import defaultdict
from at_portfolio import create_tree


TREES = {
    'ACS Cash Equities Agency': create_tree(
        acm.FPhysicalPortfolio['ACS Cash Equities Agency']),
    # PB allocation functionality disabled
    #'PB_CR_ALLOCATIONS': create_tree(
    #    acm.FPhysicalPortfolio['PB_CR_ALLOCATIONS']),
}
COMPOUND_PORTFOLIOS = TREES.keys()
ACS_DMA_PORTFOLIO = 'DMA'
STATE_CHART_NAME = 'T3 Allocations'
INVALID_STATES = (
    'Void', 
    'Confirmed Void', 
    'Reserved', 
    'Simulated', 
    'Terminated',
)


def log(message, tabs=0):
    print '%s %s%s' % (acm.Time.TimeNow(), tabs*'\t', message)


class MatchingProcessBase(object):
    opening_types = ('XTP_MARKET_HIT', 'XTP_BROKER_FILL',)
    closing_types = ('XTP_ADMIN_TRADE', 'XTP_OD_MOVE',)
    block_types = ('OBP_BLOCK_TRADE', 'FA_BLOCK_TRADE', 'XTP_BLOCK_TRADE',)
    broker_note_types = ('OBP_BROKER_NOTE', 'OBP_ADMIN_ODTRADE',)
    state_chart = acm.FStateChart[STATE_CHART_NAME]
    
    def __init__(self, portfolio_name, start_date):
        self._portfolio_name = portfolio_name
        self._start_date = start_date
        self._query = 'portfolio="%s" and tradeTime>="%s"' % (portfolio_name, start_date)
        self._trades = self.select_trades(self._query)
        self._trade_bps = []
        self._settle_bps = []
        self._trade_container = None
        self._settle_container = None
        self._keys_incomplete = {}
        self._keys_matched = {}
    
    def get_trades(self):
        return self._trades
    
    def get_ins_names(self):
        return set([trade.Instrument().Name() for trade in self.get_trades()])
    
    @classmethod
    def select_trades(cls, query):
        return acm.FTrade.Select(query)
    
    @classmethod
    def get_alloc_container(cls, trades):
        alloc_container = defaultdict(AllocationContainer)
        for trade in trades:
            if not cls.is_trade_valid(trade):
                continue
            if cls.is_closing(trade):
                alloc_container['closing'][cls.get_key(trade)] = trade
            else:
                alloc_container['opening'][cls.get_key(trade)] = trade
        return alloc_container
    
    @classmethod
    def log_state_update(cls, business_process, previous_state, new_state):
        trade = business_process.Subject()
        instrument = trade.Instrument().Name()
        portfolio = trade.Portfolio().Name()
        msg = ('State updated: %s -> %s, trade: %s, instrument: %s,'
               ' portfolio: %s, key: %s.'
               ) % (previous_state, new_state, trade.Oid(), 
                    instrument, portfolio, cls.get_key(trade))
        log(msg, 1)
    
    def process_trades(self, ins_name=''):
        if not ins_name or not acm.FInstrument[ins_name]:
            ins_names = self.get_ins_names()
        else:
            ins_names = [ins_name]
        
        for ins_name in ins_names:
            self._init_data(ins_name)
            self._process_states(ins_name)
    
    def _init_data(self, ins_name):
        trade_items = self.get_trade_items(ins_name)
        settle_items = self.get_settle_items(ins_name)
        log('%s, trade items:' % ins_name, 1)
        log([trade.Oid() for trade in trade_items], 2)
        log('%s, settle items:' % ins_name, 1)
        log([trade.Oid() for trade in settle_items], 2)
        self._trade_container = self.get_alloc_container(trade_items)
        self._settle_container = self.get_alloc_container(settle_items)
        self._trade_bps = self.get_business_processes(trade_items)
        self._settle_bps = self.get_business_processes(settle_items)
    
    def _process_states(self, ins_name):
        log('Processing states...', 1)
        self._set_states(self._trade_bps, 'Allocation Failed', 'Ready')
        self._set_states(self._settle_bps, 'Allocation Failed', 'Ready')
        self._set_states(self._trade_bps, 'Match Failed', 'Ready')
        self._set_states(self._settle_bps, 'Match Failed', 'Ready')
        self._set_states(self._trade_bps, 'Ready', 'To be Matched')
        self._set_states(self._settle_bps, 'Ready', 'To be Matched')
        
        self._process_state_to_be_matched(self._trade_bps, self._trade_container)
        self._process_state_to_be_matched(self._settle_bps, self._settle_container)
        
        self._process_state_match_incomplete(self._trade_bps, self._trade_container)
        self._process_state_match_incomplete(self._settle_bps, self._settle_container)
        
        self._process_state_matched(self._trade_bps, self._trade_container)
        self._process_state_matched(self._settle_bps, self._settle_container,
                                    self._trade_container)
        
        self._process_state_alloc_incomplete(self._trade_bps, self._trade_container)
        self._process_state_alloc_incomplete(self._settle_bps, self._settle_container)
        self._process_state_allocated(ins_name)
        log('Processing done.', 1)

    def _set_states(self, bps, current_state, new_state):
        bps_in_state = self.filter_bps_in_state(bps, current_state)
        for bp in bps_in_state:
            self.force_bp_to_state(bp, new_state)
    
    def _match_incomplete_condition(self, bp, alloc_container):
        trade_key = self.get_key(bp.Subject())
        if (trade_key in alloc_container['opening'] and 
                trade_key in alloc_container['closing']):
            return True
        return False
    
    def _process_state_to_be_matched(self, bps, alloc_container):
        bps_in_state = self.filter_bps_in_state(bps, 'To be Matched')
        for bp in bps_in_state:
            if self._match_incomplete_condition(bp, alloc_container):
                self.force_bp_to_state(bp, 'Match Incomplete')
    
    def _matched_conditon(self, bp, alloc_container):
        trade_key = self.get_key(bp.Subject())
        if trade_key in self._keys_matched:
            return self._keys_matched[trade_key]
        if (alloc_container['opening'][trade_key].equals(
                alloc_container['closing'][trade_key])):
            self._keys_matched[trade_key] = True
            return True
        self._keys_matched[trade_key] = False
        return False
    
    def _process_state_match_incomplete(self, bps, alloc_container):
        bps_in_state = self.filter_bps_in_state(bps, 'Match Incomplete')
        self._keys_matched = {}
        for bp in bps_in_state:
            if not self._match_incomplete_condition(bp, alloc_container):
                self.force_bp_to_state(bp, 'Match Failed')
            elif self._matched_conditon(bp, alloc_container):
                self.force_bp_to_state(bp, 'Matched')
    
    def _extend_trades(self, trades, alloc_container):
        for trade in trades[:]:
            closing_block = self.get_closing_block(trade)
            if not closing_block:
                log('WARNING: Closing block for %s not found.' % trade.Oid(), 1)
                continue
            closing_key = self.get_key(closing_block)
            if closing_key in alloc_container['opening']:
                trades.extend(alloc_container['opening'][closing_key].get_trades())
        return trades
    
    def _alloc_incomplete_condition(self, bp, alloc_container, sec_container=None):
        condition = lambda x: x in ['Matched', 'Allocation Incomplete', 'Allocated']
        trade_key = self.get_key(bp.Subject())
        if trade_key in self._keys_incomplete:
            return self._keys_incomplete[trade_key]
        opening_trades = alloc_container['opening'][trade_key].get_trades()
        closing_trades = alloc_container['closing'][trade_key].get_trades()
        if sec_container:
            opening_trades = self._extend_trades(opening_trades, sec_container)
        
        opening_bps = self.get_related_bps(opening_trades)
        closing_bps = self.get_related_bps(closing_trades)
        if not (all(opening_bps) and all(closing_bps)):
            self._keys_incomplete[trade_key] = False
            return False
        opening_states = self.get_states(opening_bps)
        closing_states = self.get_states(closing_bps)
        if (all(map(condition, opening_states)) 
                and all(map(condition, closing_states))):
            self._keys_incomplete[trade_key] = True
            return True
        self._keys_incomplete[trade_key] = False
        return False
    
    def _process_state_matched(self, bps, alloc_container, sec_container=None):
        bps_in_state = self.filter_bps_in_state(bps, 'Matched')
        self._keys_incomplete = {}
        self._keys_matched = {}
        for bp in bps_in_state:
            if not self._matched_conditon(bp, alloc_container):
                self.force_bp_to_state(bp, 'Match Failed')
            if self._alloc_incomplete_condition(bp, alloc_container,
                    sec_container):
                self.force_bp_to_state(bp, 'Allocation Incomplete')
    
    def _allocated_condition(self, bp, alloc_container):
        closing_condition = lambda x: x in ['Allocation Incomplete', 'Allocated']
        opening_condition = lambda x: x in ['Allocated']
        
        trade = bp.Subject()
        trade_key = self.get_key(trade)
        if self.is_closing(trade):
            opening_trades = alloc_container['opening'][trade_key].get_trades()
            opening_bps = self.get_related_bps(opening_trades)
            if not all(opening_bps):
                return False
            opening_states = self.get_states(opening_bps)
            if all(map(closing_condition, opening_states)):
                return True
        else:
            closing_trades = alloc_container['closing'][trade_key].get_trades()
            closing_bps = self.get_related_bps(closing_trades)
            if not all(closing_bps):
                return False
            closing_states = self.get_states(closing_bps)
            if all(map(opening_condition, closing_states)):
                return True
        return False
    
    def _process_state_alloc_incomplete(self, bps, alloc_container):
        bps_in_state = self.filter_bps_in_state(bps, 'Allocation Incomplete')
        self._keys_incomplete = {}
        for bp in bps_in_state:
            if not self._alloc_incomplete_condition(bp, alloc_container):
                self.force_bp_to_state(bp, 'Allocation Failed')
            elif self._allocated_condition(bp, alloc_container):
                self.force_bp_to_state(bp, 'Allocated')
    
    def _process_state_allocated(self, ins_name):
        acceptable_states = ['Allocated', 'Allocation Incomplete']
        trade_items = self.filter_trades(self.get_trade_items(ins_name),
                                         acceptable_states)
        settle_items = self.filter_trades(self.get_settle_items(ins_name),
                                          acceptable_states)
        trade_container = self.get_alloc_container(trade_items)
        settle_container = self.get_alloc_container(settle_items)
        trade_bps = self.get_business_processes(trade_items)
        settle_bps = self.get_business_processes(settle_items)
        
        trade_bps = self.filter_bps_in_state(trade_bps, 'Allocated')
        self._keys_matched = {}
        reset_settle = False
        for bp in trade_bps:
            if not (self._match_incomplete_condition(bp, trade_container)
                    and self._matched_conditon(bp, trade_container)):
                self.force_bp_to_state(bp, 'Allocation Failed')
                reset_settle = True

        settle_bps = self.filter_bps_in_state(settle_bps, 'Allocated')
        self._keys_matched = {}
        for bp in settle_bps:
            if not (self._match_incomplete_condition(bp, settle_container)
                    and self._matched_conditon(bp, settle_container)) or reset_settle:
                self.force_bp_to_state(bp, 'Allocation Failed')
    
    @classmethod
    def filter_trades(cls, trades, states):
        result = []
        for trade in trades:
            bp = cls.get_related_bp(trade)
            if bp and bp.CurrentStep().State().Name() in states:
                result.append(trade)
        return result
    
    @classmethod
    def get_business_processes(cls, trades):
        bps = []
        for trade in trades:
            if not cls.is_trade_valid(trade):
                continue
            current_process = acm.BusinessProcess.FindBySubjectAndStateChart(
                trade, cls.state_chart)
            if current_process:
                bps.append(current_process.First())
        return bps
    
    @classmethod
    def get_related_bps(cls, trades):
        bps = []
        for trade in trades:
            bp = cls.get_related_bp(trade)
            if bp:
                bps.append(bp)
        return bps
    
    @classmethod
    def get_related_bp(cls, trade):
        bp_trade = cls.get_bp_trade(trade)
        if not bp_trade:
            return None
        current_process = acm.BusinessProcess.FindBySubjectAndStateChart(
            bp_trade, cls.state_chart)
        if current_process:
            return current_process.First()
        return None
    
    @classmethod
    def force_bp_to_state(cls, bp, state, reason=''):
        current_state = bp.CurrentStep().State().Name()
        try:
            bp.ForceToState(state, reason)
            bp.Commit()
        except Exception as exc:
            log('ERROR: Failed to force %s to "%s": %s' % (bp.Oid(), state, str(exc)), 1)
        else:
            cls.log_state_update(bp, current_state, state)
    
    @classmethod
    def filter_bps_in_state(cls, bps, state):
        return [bp for bp in bps if bp.CurrentStep().State().Name() == state]
    
    @classmethod
    def get_states(cls, bps):
        return [bp.CurrentStep().State().Name() for bp in bps]
    
    def get_trade_items(self, ins_name):
        return []
    
    def get_settle_items(self, ins_name):
        return []
    
    @classmethod
    def is_trade_valid(cls, trade):
        if (cls.xtp_type(trade) in cls.broker_note_types and 
                trade.Status() not in INVALID_STATES):
            return True
        return False
    
    @classmethod    
    def xtp_type(cls, trade):
        return trade.AdditionalInfo().XtpTradeType()
    
    @classmethod
    def is_mirror(cls, trade):
        return (trade.MirrorTrade() and trade.MirrorTrade() == trade)
    
    @classmethod
    def get_bp_trade(cls, trade):
        if cls.xtp_type(trade) in cls.broker_note_types and trade.TrxTrade():
            return trade.TrxTrade()
        return trade
    
    @classmethod
    def is_closing(cls, trade):
        if not cls.xtp_type(trade) and not trade.MirrorTrade():
            return False
        return (cls.xtp_type(trade) in cls.broker_note_types or 
                cls.is_mirror(trade))
    
    @classmethod
    def get_closing_block(cls, trade):
        return trade.GetMirrorTrade()
    
    @classmethod
    def get_key(cls, trade):
        items = [
            trade.Portfolio().Name(),
            trade.Instrument().Name(),
            cls.get_position_string(trade),
            trade.Currency().Name(),
            cls.get_match_id(trade),
            trade.TradeTime()[:10].replace('-', ''),
        ]
        return '_'.join([item for item in items if item])
    
    @classmethod
    def get_position_string(cls, trade):
        if cls.is_closing(trade):
            return 'Long' if trade.Quantity() < 0 else 'Short'
        else:
            return 'Long' if trade.Quantity() > 0 else 'Short'
    
    @classmethod
    def get_match_id(cls, trade):
        #if (cls.xtp_type(trade) in cls.block_types and not cls.is_mirror(trade)):
        #    return str(trade.Oid())
        #elif cls.xtp_type(trade) in cls.broker_note_types and trade.TrxTrade():
        #    return str(trade.TrxTrade().Oid())
        return ''

# PB allocation functionality disabled
#class MatchingProcessPB(MatchingProcessBase):
#    pb_closing_types = ('PB_CLOSING_BLOCK',)
#    no_fees_chlist = acm.FChoiceList.Select01(
#        'name="PS No Fees" and list="TradeKey3"', '')
#    
#    @classmethod
#    def is_mirror(cls, trade):
#        if cls.xtp_type(trade) in cls.pb_closing_types:
#            return True 
#        return super(MatchingProcessPB, cls).is_mirror(trade)
#    
#    @classmethod
#    def get_bp_trade(cls, trade):
#        if cls.xtp_type(trade) in cls.pb_closing_types:
#            return trade.TrxTrade()
#        return trade
#
#    @classmethod
#    def get_closing_block(cls, trade):
#        return trade.TrxTrade()
#
#    @classmethod
#    def is_trade_valid(cls, trade):
#        return (trade.Status() not in INVALID_STATES)
#    
#    def get_trade_items(self, ins_name):
#        trades = []
#        query = self._query + ' and instrument="%s"' % ins_name
#        for trade in self.select_trades(query):
#            if (self.xtp_type(trade) not in self.block_types and 
#                    self.xtp_type(trade) not in self.broker_note_types):
#                trades.append(trade)
#        return trades
#    
#    def get_settle_items(self, ins_name):
#        trades = []
#        query = self._query + ' and instrument="%s"' % ins_name
#        for trade in self.select_trades(query):
#            if (self.xtp_type(trade) in self.block_types or
#                    self.xtp_type(trade) in self.broker_note_types):
#                trades.append(trade)
#        return trades
#    
#    @classmethod
#    def get_split_trades(cls, trade):
#        trx_trade = trade.TrxTrade()
#        if not trx_trade:
#            return []
#        split_trades = []
#        trades = acm.FTrade.Select('trxTrade="%s"' % trx_trade.Oid())
#        for trx_trade in trades:
#            if (cls.xtp_type(trx_trade) in cls.broker_note_types and
#                    trx_trade.Price() == trade.Price() and
#                    trx_trade.Quantity() == -trade.Quantity()):
#                split_trades.append(trx_trade)
#        return split_trades
#    
#    @classmethod
#    def link_broker_note(cls, trade):
#        msg = 'Failed to link broker note %s: ' % trade.Oid()
#        if not trade.Portfolio().AdditionalInfo().PS_PortfolioType() == 'CFD Allocation':
#            return
#        split_trades = cls.get_split_trades(trade)
#        if not split_trades:
#            log(msg + 'No split trades identified.', 1)
#            return
#        for split_trade in split_trades:
#            fa_block_trade = split_trade.TrxTrade()
#            if not fa_block_trade:
#                log(msg + 'No FA block trade.', 1)
#                continue
#            if split_trade.ContractTrdnbr() == fa_block_trade.Oid():
#                continue
#            split_trade.ContractTrdnbr(fa_block_trade.Oid())
#            try:
#                split_trade.Commit()
#            except Exception as exc:
#                log(msg + 'Commit failed. %s' % str(exc), 1)
#    
#    @classmethod
#    def update_broker_note(cls, trade):
#        msg = 'Failed to update broker note %s: ' % trade.Oid()
#        split_trades = cls.get_split_trades(trade)
#        if not split_trades:
#            log(msg + 'No split trades identified.', 1)
#            return
#        for split_trade in split_trades:
#            if split_trade.Text1() == 'Allocation Process':
#                continue
#            split_trade.Text1('Allocation Process')
#            try:
#                split_trade.Commit()
#            except Exception as exc:
#                log(msg + 'Commit failed. %s' % str(exc), 1)
#    
#    def _pre_process_trades(self, ins_name=''):
#        if not ins_name or not acm.FInstrument[ins_name]:
#            trades = self.get_trades()
#        else:
#            query = self._query + ' and instrument="%s"' % ins_name
#            trades = self.select_trades(query)
#        
#        for trade in trades:
#            if not self.is_trade_valid(trade):
#                continue
#            if self.xtp_type(trade) in self.broker_note_types:
#                self.link_broker_note(trade)
#                self.update_broker_note(trade)
#            if not trade.Text1() == 'Allocation Process':
#                trade.Text1('Allocation Process')
#            if not trade.OptKey3() == self.no_fees_chlist:
#                trade.OptKey3(self.no_fees_chlist)
#            if not trade.IsModified():
#                continue
#            try:
#                trade.Commit()
#            except Exception as exc:
#                log('Failed to preprocess trade %s. %s' % (trade.Oid(), str(exc)), 1)
#    
#    def process_trades(self, ins_name=''):
#        self._pre_process_trades(ins_name)
#        super(MatchingProcessPB, self).process_trades(ins_name)
        

class MatchingProcessACS(MatchingProcessBase):

    @classmethod
    def is_trade_valid(cls, trade):
        return (trade.Status() not in INVALID_STATES)

    @classmethod
    def get_bp_trade(cls, trade):
        if (cls.is_trade_item(trade) and trade.MirrorTrade() and 
                cls.is_settle_item(trade.GetMirrorTrade())):
            return trade.GetMirrorTrade()
        return trade
    
    @classmethod
    def is_closing(cls, trade):
        if cls.is_trade_item(trade): 
            if cls.xtp_type(trade) in cls.block_types or (
                    not cls.xtp_type(trade) and trade.MirrorTrade() 
                    and cls.is_settle_item(trade.GetMirrorTrade())):
                return True
        elif cls.is_settle_item(trade):
            if cls.xtp_type(trade) in cls.broker_note_types:
                return True
        if cls.xtp_type(trade) in cls.closing_types:
            return True
        return False
    
    def get_trade_items(self, ins_name):
        query = self._query + ' and instrument="%s"' % ins_name
        if self._portfolio_name.endswith('-STL'):
            query = query.replace('-STL', '-TRD')
        return self.select_trades(query)
    
    def get_settle_items(self, ins_name):
        query = self._query + ' and instrument="%s"' % ins_name
        if self._portfolio_name.endswith('-TRD'):
            query = query.replace('-TRD', '-STL')
        return self.select_trades(query)
    
    @classmethod
    def is_trade_item(cls, trade):
        return str(trade.Portfolio().Name()).endswith('-TRD')
    
    @classmethod
    def is_settle_item(cls, trade):
        return str(trade.Portfolio().Name()).endswith('-STL')


class MatchingProcessDMA(MatchingProcessBase):
    
    @classmethod
    def is_trade_valid(cls, trade):
        return (trade.Status() not in INVALID_STATES)
    
    @classmethod
    def is_closing(cls, trade):
        return False
    
    def get_trade_items(self, ins_name):
        query = self._query + ' and instrument="%s"' % ins_name
        return self.select_trades(query)

    def _process_states(self, ins_name):
        for bp in self._trade_bps:
            if (self.xtp_type(bp.Subject()) in self.broker_note_types
                    and not bp.CurrentStep().State().Name() == 'Allocated'):
                self.force_bp_to_state(bp, 'Allocated')


class AllocationContainer(object):
    
    def __init__(self):
        self._agg_dict = {}
    
    def add(self, key, trade):
        if key in self._agg_dict:
            self._agg_dict[key].append(trade)
        else:
            self._agg_dict[key] = TradeAggregator(trade)
    
    def get_trades(self):
        result = []
        for aggergator in self._agg_dict.values():
            result.extend(aggregator.get_trades())
        return result
    
    def __getitem__(self, key):
        return self._agg_dict[key]
    
    def __setitem__(self, key, value):
        self.add(key, value)
    
    def __contains__(self, item):
        return (item in self._agg_dict)
    
    def __iter__(self):
        for key in self._agg_dict:
            yield key


class TradeAggregator(object):
    rel_premium_tolerance = 0.1
    vwap_tolerance = 0.01
    quantity_tolerance = 0.0001
    
    def __init__(self, trade):
        self._trades = [trade]
    
    def append(self, trade):
        if not trade in self._trades:
            self._trades.append(trade)
    
    def extend(self, trades):
        for trade in trades:
            self.append(trade)
    
    def get_trades(self):
        return self._trades
    
    def get_agg_quantity(self):
        if not self._trades:
            return 0.0
        return sum([trade.Quantity() for trade in self._trades])
    
    def get_agg_premium(self):
        if not self._trades:
            return 0.0
        return sum([trade.Premium() for trade in self._trades])
    
    def get_vwap(self):
        agg_quantity = self.get_agg_quantity()
        if not agg_quantity:
            return 0.0
        return sum([trade.Quantity() * trade.Price() 
                    for trade in self._trades]) / agg_quantity
    
    def count(self):
        return len(self.get_trades())
    
    def equals(self, aggregator):        
        total_quantity = self.get_agg_quantity() + aggregator.get_agg_quantity()
        total_premium = self.get_agg_premium() + aggregator.get_agg_premium()
        total_vwap = self.get_vwap() - aggregator.get_vwap()
        premium_tolerance = abs(self.rel_premium_tolerance * 
                                self.get_agg_premium() / self.get_agg_quantity())
        if abs(total_quantity) > self.quantity_tolerance:
            return False
        if abs(total_premium) > premium_tolerance:
            return False
        if abs(total_vwap) > self.vwap_tolerance:
            return False
        return True


def get_process_class(portfolio_name):
    if (TREES['ACS Cash Equities Agency'].has(portfolio_name) and 
            portfolio_name == ACS_DMA_PORTFOLIO):
        return MatchingProcessDMA 
    elif TREES['ACS Cash Equities Agency'].has(portfolio_name):
        return MatchingProcessACS
    # PB allocation functionality disabled
    #elif TREES['PB_CR_ALLOCATIONS'].has(portfolio_name):
    #    return MatchingProcessPB
    return MatchingProcessBase


def get_process_object(portfolio_name, start_date):
    MatchingProcess = get_process_class(portfolio_name)
    return MatchingProcess(portfolio_name, start_date)

