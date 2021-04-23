import acm
from at_ael_variables import AelVariableHandler

ALLOCTEXT = "Allocation Process"

class Instr:
    
    def __init__(self, name, trade):
        self.name = name
        self.trades = [trade]
    
    def add_trade(self, trade):
        self.trades.append(trade)
        
    def get_positive_trades(self):
        list_pos = []
        sum = 0
        for t in self.trades:
            if t.Quantity() > 0:
                list_pos.append(t)
                sum += t.Quantity()
        return (list_pos, sum)
    
    def get_negative_trades(self):
        list_neg = []
        sum = 0
        for t in self.trades:
            if t.Quantity() < 0:
                list_neg.append(t)
                sum += t.Quantity()
        return (list_neg, sum)
    

def get_dmas(date, status, portfolio_list):    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', status))
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)
    query.AddAttrNode('CreateUser.Name', 'EQUAL', 'AMBA')
    orNode = query.AddOpNode('OR')
    for portf in portfolio_list:
        orNode.AddAttrNode('Portfolio.Name', 'EQUAL', portf.Name())
    trades = query.Select()
    return trades


def get_allocs(date, portfolio_list):
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'VOID'))
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)
    query.AddAttrNode('CreateUser.Name', 'NOT_EQUAL', 'AMBA')
    query.AddAttrNode('Text1', 'EQUAL', 'Allocation Process')
    orNode = query.AddOpNode('OR')
    for portf in portfolio_list:
        orNode.AddAttrNode('Portfolio.Name', 'EQUAL', portf.Name())
    trades = query.Select()
    return trades


def create_instrument_objs(trades):
    dic_trades = {}
    for t in trades:
        insname = t.Instrument().Name()
        ins = dic_trades.get(insname)
        if not ins:
            dic_trades[insname] = Instr(insname, t)
        else:
            insname1 = ins.name
            ins.add_trade(t)
    return dic_trades
            

def apply_changes(sum_dma, sum_alloc, trades_allocs, trades_dmas):
    allocnbr = trades_allocs[0].Oid()
    if sum_dma == sum_alloc:
        for tr in trades_dmas:
            if tr.Status() == 'Void':
                # Change trade status so that it can be modified
                tr.Status('Simulated')
            else:            
                # Modify trade and change the status back
                tr.Text1(ALLOCTEXT)
                tr.Contract(allocnbr)
                tr.Status('Void')
                tr.Commit()

        print("Trades {0} have contract to {1}".format([trd.Oid() for trd in trades_dmas], allocnbr))
    else:
        raise RuntimeError("Overall quantities do not match for dma trades {0} and "\
                           "allocation trade {1}".format([trd.Oid() for trd in trades_dmas], allocnbr))
             

def modify_trades(date, current_dma_status, portfolio_list, dry_run=True):
    dma_trades = get_dmas(date, current_dma_status, portfolio_list)  # 1172
    allocs_trades = get_allocs(date, portfolio_list)  # 20
    
    dic_dmas = create_instrument_objs(dma_trades)
    dic_allocs = create_instrument_objs(allocs_trades)
    
    acm.BeginTransaction()
    print('Starting amending {0} trades...'.format(len(dma_trades)))
    try:
        for t in dic_dmas.values():
            pos_plus_trades, sum_plus = t.get_positive_trades()
            pos_minus_trades, sum_minus = t.get_negative_trades()
            
            alloc_ins = dic_allocs.get(t.name)
            if not alloc_ins:
                raise RuntimeError('Nonexistent allocation trade for instrument "%s"' %t.name)
            pos_plus_allocs, sum_plus_alloc = alloc_ins.get_positive_trades()
            pos_minus_allocs, sum_minus_alloc = alloc_ins.get_negative_trades()
            if len(pos_plus_allocs) > 1 or len(pos_minus_allocs) > 1:
                raise RuntimeError('More than 1 allocation trade found for instrument "{0}" : {1}'.format(
                                    t.name,
                                   [trd.Oid() for trd in pos_plus_allocs + pos_minus_allocs]))
            
            if sum_plus > 0:
                apply_changes(sum_plus, sum_plus_alloc, pos_plus_allocs, pos_plus_trades)
            if sum_minus < 0:
                apply_changes(sum_minus, sum_minus_alloc, pos_minus_allocs, pos_minus_trades)
        if not dry_run:
            acm.CommitTransaction()
        else:
            acm.AbortTransaction()
    except Exception as exc:
        acm.AbortTransaction()
        print("ERROR: {0}".format(str(exc)))
        print("No trade was changed. Please, contact Ondrej Bahounek with log details.")


ael_variables = AelVariableHandler()
ael_variables.add('start_date',
                  label='Start date',
                  default='2014-11-14')

ael_variables.add('end_date',
                  label='End date',
                  default='2014-11-17')
                  
ael_variables.add('allocation_portfolio',
                  label='Allocation portfolio',
                  cls=acm.FPhysicalPortfolio,
                  multiple=True)

ael_variables.add_bool('dry_run',
                       label='Dry run',
                       default=True)
                       
                       
def ael_main(config):
    print('Dry run: {0}'.format(config['dry_run']))
    calendar = acm.FCalendar['ZAR Johannesburg']
    date = config['start_date']
    if calendar.IsNonBankingDay(None, None, date):
        date = calendar.AdjustBankingDays(date, 1)
    end_date = config['end_date']
    
    while date <= end_date:
        # Change status of trades we need to modify (current status is 'Void')
        modify_trades(date,
                      'Void',
                      config['allocation_portfolio'],
                      config['dry_run'])

        # Connect DMA trades to aggregated trades (current status is 'Simulated')
        modify_trades(date,
                      'Simulated',
                      config['allocation_portfolio'],
                      config['dry_run'])

        date = calendar.AdjustBankingDays(date, 1)

