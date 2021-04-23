""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FParameterLists - Data preparation for Structured Equity Products
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    The parameter-list hook is used for instruments that are valued using the 
    Valuation hook function and which use ad hoc valuation parameters. The 
    returned parameter list tells ATLAS what these parameters are.
    
    The instrument information window then displays the valuation parameters, 
    just as it does for parameter mappings defined in the Context and Parameter 
    Override applications.
    
    The hook function is also called whenever values that depend on yield curves 
    and volatilities need to be calculated, such as when an instrument window is 
    opened or when evaluating ARENA functions, such as rf_scenario().

----------------------------------------------------------------------------"""
import ael 

# Parameters used for the valuation of basket and quanto basket options.
def BasketOption(i):  
    if i.und_insaddr == None: 
        raise "FParameterList", "The option " + str(i.insid) + " does not have an underlying instrument."
    stock_links = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
    params_vec = []
    # Discount rates for the option
    params_vec.append([i.used_yield_curve(i.curr).ir_name, 'Discount', i.strike_curr.insid])
    
    # Check if the basket option is a quanto basket option.
    curr_dict = {}
    curr_dict[i.curr.insid] = 1
    for stock_link in stock_links:
        if len(curr_dict) > 1: break
        else:
            stock_curr = stock_link.member_insaddr.curr.insid
            if not curr_dict.has_key(stock_curr):
                curr_dict[stock_curr] = 1
    if len(curr_dict) > 1: quanto_flag = 1
    else: quanto_flag = 0
    
    for stock_link in stock_links:
        stock_j = stock_link.member_insaddr
        # Volatility surfaces
        vol_surf = stock_j.used_volatility(stock_j.curr).vol_name
        params_vec.append([vol_surf, 'Volatility', stock_j.curr.insid])
        
        if quanto_flag:
            fx_vol_surf = stock_j.curr.used_volatility(i.curr).vol_name
            params_vec.append([fx_vol_surf, 'Volatility', stock_j.curr.insid])
            
        # Discount rates for the stocks
        params_vec.append([stock_j.used_yield_curve(stock_j.curr).ir_name, 'Discount', stock_j.curr.insid])
        
        # Repo rates
        params_vec.append([stock_j.used_repo_curve(stock_j.curr).ir_name, 'Repo', stock_j.curr.insid])
    return params_vec

# Parameters used for the valuation of rainbow options. 
def RainbowOption(i):
    stock_links = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
    params_vec = []
    # Discount rates for the option
    params_vec.append([i.used_yield_curve(i.curr).ir_name, 'Discount', i.strike_curr.insid])
    for stock_link in stock_links:
        stock_j = stock_link.member_insaddr
        # Volatility surfaces
        vol_surf = stock_j.used_volatility(stock_j.curr).vol_name
        params_vec.append([vol_surf, 'Volatility', stock_j.curr.insid])

        # Repo rates
        params_vec.append([stock_j.used_repo_curve(stock_j.curr).ir_name, 'Repo', stock_j.curr.insid])
    return params_vec






