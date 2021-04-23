import acm
import at
import at_time
from at_ael_variables import AelVariableHandler
from auto_confirm import AutoConfirmation

class CurrAutoconfirm(AutoConfirmation):
    state = at.TS_BO_CONFIRMED
    
    @staticmethod
    def is_owner_pf(pf, owner_name):
        if not pf:
            return False        
        acm_pf = pf
        if isinstance(pf, str):
            if pf == owner_name:
                return True
            acm_pf = acm.FPhysicalPortfolio[pf]
        if acm_pf.Name() == owner_name:
            return True
        for ml in acm_pf.MemberLinks():
            return CurrAutoconfirm.is_owner_pf(ml.OwnerPortfolio(), owner_name)
        return False
    
    def __strict_rule_1(self, trade):
        #Check attributes which should match between trade and mirror trade
        mirror_trade = trade.GetMirrorTrade()
        
        if not mirror_trade:
            #checking if trade contains |FAR|
            if "|FAR|" in trade.OptionalKey():
                self.is_fa_trade.add(trade.Oid())
                return True
            raise UserWarning("Mirror trade not available")
        
        tr_ins_override = trade.AdditionalInfo().InsOverride()
        mtr_ins_override = mirror_trade.AdditionalInfo().InsOverride()
        if (trade.Name() != mirror_trade.GetMirrorTrade().Name()
           or trade.ValueDay() != mirror_trade.ValueDay()
           or trade.Instrument().Name() != mirror_trade.Instrument().Name()
           or trade.Quantity() != -1.0 * mirror_trade.Quantity()):
            raise UserWarning("Attribute mismatch between trade and mirror")
        if tr_ins_override is None and mtr_ins_override is None:
            return True
        if tr_ins_override != mtr_ins_override:
            raise UserWarning("InsOverride doesn't match")
        return True
    
    def __strict_rule_2(self, trade):
        #Check portfolios
        if trade.CounterPortfolio() and trade.Portfolio().Name() == trade.CounterPortfolio().Name():
            raise UserWarning("Portfolio and counter-portfolio are the same")
        return True
        
    def __strict_rule_3(self, trade):
        #check Instrument Override field
        if trade.Instrument().InsType() == 'Future/Forward' or trade.Instrument().InsType() == 'Option':
            if not trade.AdditionalInfo().InsOverride() == None: 
                raise UserWarning("Instrument Override not empty")
        return True
         
    def confirm(self, dry_run = False):
        if len(self.candidates) == 0:
            print("No trades to automatically {0}".format(self.state))
            return

        # validate each trade from candidate list
        for trade in self.candidates:
            self.verify(trade)
            
        #FX Swaps: find all 4 trades
        for trade in self.passed:
            is_swap = False
            if trade.Status() != self.state:
                #Check if it is a spot/forward
                if trade.ConnectedTrdnbr() == trade.Oid():
                    for trade2 in self.passed:
                        if trade2.Oid() != trade.Oid() and trade2.ConnectedTrdnbr() == trade.Oid():
                            is_swap = True
                            side2 = trade2.Oid()
                if trade.ConnectedTrdnbr() != trade.Oid():
                    is_swap = True
                    side2 = trade.ConnectedTrdnbr()
                to_confirm = set()
                to_confirm.add(trade.Oid())
                    
                if is_swap:
                    to_confirm.add(side2)
                
                for mirror in self.passed:
                    if mirror.GetMirrorTrade() and mirror.GetMirrorTrade().Oid() in to_confirm:
                        to_confirm.add(mirror.Oid())
                        
                self.commit_transaction(to_confirm, dry_run, trade.Oid() in self.is_fa_trade)
    
    def commit_transaction(self, to_confirm, dry_run = False, is_fa_trade = False):
        if not to_confirm:
            return
        try:
            print("Confirming trades: {}".format(to_confirm))
            if not dry_run:
                acm.BeginTransaction()
                #If the trade is Front Arena booked skip if statement
                if not is_fa_trade and len(to_confirm) != 4 and len(to_confirm) != 2:
                    raise UserWarning("Needs exactly 2 or 4 trades" \
                                      " but {} found".format(len(to_confirm)))
                for trdnbr in to_confirm:
                    t = acm.FTrade[trdnbr]
                    t.Status(self.state)
                    t.Commit()
                acm.CommitTransaction()
        except Exception as e:
            if not dry_run:
                acm.AbortTransaction()
            bo_error = "Unable to autoconfirm trades {}".format(to_confirm)
            bo_error += " to status {}".format(self.state)
            bo_error += "\nReason: {}".format(e)
            self.errors[acm.FTrade[to_confirm.pop()]] = bo_error

ael_variables = AelVariableHandler()
ael_variables.add("dry_run",
                  label = "Dry run",
                  alt = "Check this to avoid committing changes",
                  cls = "int",
                  default = 0,
                  collection = [0, 1],
                  mandatory = False)
ael_variables.add("date_from",
                  label = "Date from",
                  alt = "Trades since this date (YYYY-MM-DD)",
                  cls = "string",
                  default = "",
                  mandatory = True)
ael_variables.add("date_to",
                  label = "Date to",
                  alt = "Trades until this date (YYYY-MM-DD)",
                  cls = "string",
                  default = "",
                  mandatory = True)

def ael_main(ael_params):
    try:
        date_from = str(at_time.date_from_symbolic_date(ael_params["date_from"]))
    except KeyError:
        date_from = ael_params["date_from"]
    try:
        date_to = str(at_time.date_from_symbolic_date(ael_params["date_to"]))
    except KeyError:
        date_to = ael_params["date_to"]
    print("Running autoconfirm for dates between {} and {}".format(date_from, date_to))

    query_trades = acm.FStoredASQLQuery["PCG_Curr_AutoConfirm"].Query().Clone()
    and_node = query_trades.AddOpNode("AND")
    and_node.AddAttrNodeString("ExecutionTime", date_from, "GREATER_EQUAL")
    and_node = query_trades.AddOpNode("AND")
    and_node.AddAttrNodeString("ExecutionTime", date_to, "LESS_EQUAL")
    trades = query_trades.Select()
    
    candidates = []
    for t in trades:
        if t.add_info("Approx. load"):
            if t.add_info("Approx. load") == "Yes":
                continue
        candidates.append(t)
    print("Number of trade candidates {}".format(len(candidates)))

    curr_engine = CurrAutoconfirm(candidates)
    curr_engine.is_fa_trade = set([])
    curr_engine.confirm(dry_run = ael_params["dry_run"])
    
    #print errors
    curr_engine.print_errors()
    
    
    print("PCG_CURR_AUTOCONFIRM completed.")
