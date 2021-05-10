import acm
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add("trades", label = "Trades to change", cls = "FTrade", mandatory = True, multiple = True)

def ael_main(ael_params):
    for t in ael_params["trades"]:
        t_copy = t.Clone()
        t_copy.Counterparty("CORONATION AM PTY LTD")
        t.Apply(t_copy)
        t.Commit()
