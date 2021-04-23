""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FSEQDataPrep - Data preparation for Structured Equity Products
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Install choice lists, additional info specifications,
    and context links needed by the different AEL modules 
    used to value structured equity products.

NOTE
    CHOICE LISTS
        Each choicelist should be specified as a tuple:
        (<list to which it belongs>,<name of this entry>,<description>)
    
        If <list to which it belongs> is empty, a new choicelist will be created, 
        and given the name of <name of this entry>.
    
    ADDITIONAL INFO SPEC
        Each additional info field should be specified as a tuple:
        (<Table>, <TypeGroup>, <TypeSpecification>, <FieldName>, <Description>, <Default>, <Mandatory>)
        
        <Table> is the table to which the add info is connected to 
        <TypeGroup> is one of 'Standard', 'Enum' or 'RecordRef'
        <TypeSpecification> specifies the type (within <TypeGroup>) of the add info
        <FieldName> is the name of the add info field
        <Description> describes the add info field
        <Default> is the default value of the add info
        <Mandatory> tells whether the add info field is mandatory or not
    
    TIME SERIES SPEC
        Each context link should be specified as a tuple:
        (<ContextName>, <Type>, <Name>, <InstrumentName>, <ChoiceListName>, <ChoiceListEntryName>)
            
        <ContextName> is the name of the context to which the context link is to be added
        <Type> is one of 'Correlation', 'Price Finding', 'Dividend Stream' or 'Valuation Function'
        <Name> is the name related to the context link (depending on <Type>; e.g. name of 
                   valuation function)
        <InstrumentName> is the name of the instrument the link applies to if applicable, 
                   should have the value '' (the empty string) otherwise
        <ChoiceListName> is the name of the corresponding choice list if applicable,
                   should have the value '' (the empty string) otherwise
        <ChoiceListEntryName> is the name of the corresponding choice list entry if applicable,
                   should have the value '' (the empty string) otherwise   


----------------------------------------------------------------------------"""
import ael

choicelists_to_install   = []
addinfospecs_to_install  = []
timeseries_to_create     = []
context_links_to_install = []

def instypes():
    types = ['ALL', 'Average', 'Barrier', 'DoubleBarrier', 'ForwardStart',
             'Basket', 'Rainbow', 'Cliquet', 'Ladder']
    return types

def contexts():
    contexts = ael.Context.select()
    context_vec = []
    for context in contexts: context_vec.append(context.name)
    context_vec.sort()
    return context_vec
    
ael_variables = [('instype', 'InstrumentType', 'string', instypes(), None, 1, 1),
                 ('context', 'Context', 'string', contexts(), 'EQ_DEMO', 1, 0)]


def ael_main(dict):
    
    # FPrintInfo is used by addinfo field FPrintInfo
    choicelists_to_install.append(('', 'FPrintInfo', 'Used by addinfo field FPrintInfo'))
    choicelists_to_install.append(('FPrintInfo', 'Yes', 'Print valuation parameters'))
    choicelists_to_install.append(('FPrintInfo', 'No', 'Print valuation parameters'))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FPrintInfo', 'FPrintInfo', '', 0))
    
    CONTEXT = dict["context"]
    
    for t in dict["instype"]:
        if t == 'ALL':
            add_average_parameters(CONTEXT)
            add_barrier_parameters(CONTEXT, 'Barrier')
            add_barrier_parameters(CONTEXT, 'DoubleBarrier')
            add_fwd_start_parameters(CONTEXT)
            add_basket_parameters(CONTEXT)
            add_rainbow_parameters(CONTEXT)
            add_cliquet_parameters(CONTEXT)
            add_ladder_parameters(CONTEXT)
            break
            
        if   t == 'Average':      add_average_parameters(CONTEXT)
        elif t == 'Barrier' or t == 'DoubleBarrier': add_barrier_parameters(CONTEXT, t)
        elif t == 'ForwardStart': add_fwd_start_parameters(CONTEXT)
        elif t == 'Basket':       add_basket_parameters(CONTEXT)
        elif t == 'Rainbow':      add_rainbow_parameters(CONTEXT)
        elif t == 'Cliquet':      add_cliquet_parameters(CONTEXT)
        elif t == 'Ladder':       add_ladder_parameters(CONTEXT)
            
    install_choicelist(choicelists_to_install)
    install_context_links(context_links_to_install)
    install_addinfo(addinfospecs_to_install)
    create_timeseries(timeseries_to_create)
    print 'SEQ DATA PREPARATION COMPLETED.'



def add_average_parameters(context):
    
    # 1. ADD CHOICE LISTS #
    choicelists_to_install.append(('ValGroup', 'EqAverage', 'Average Options'))
    choicelists_to_install.append(('Valuation Function', 'FEqAverage.pv', 'Average Option valuation'))
    choicelists_to_install.append(('Valuation Extension', 'theorAverage', 'Average Option valuation'))
    choicelists_to_install.append(('Category', 'Average', 'Equity Average Options'))
    
    # FAverageType is used by addinfo field FAverageType
    choicelists_to_install.append(('', 'FAverageType', 'Used by addinfo field FAverageType'))
    choicelists_to_install.append(('FAverageType', 'ArithmeticFix', 'Arithmetic Fix Strike'))
    choicelists_to_install.append(('FAverageType', 'ArithmeticFloating', 'Arithmetic Floating Strike'))
    choicelists_to_install.append(('FAverageType', 'GeometricFix', 'Geometric Fix Strike'))
    
    # FFwdStart is used by addinfo field FFwdStart
    choicelists_to_install.append(('', 'FFwdStart', 'Used by addinfo field FFwdStart'))
    choicelists_to_install.append(('FFwdStart', 'Fwd Start', 'Forward start option'))
    choicelists_to_install.append(('FFwdStart', 'Fwd Start Perf', 'Forward start performance option'))
    
    # FAverageIn is used by addinfo field FAverageIn
    choicelists_to_install.append(('', 'FAverageIn', 'Used by addinfo field FAverageIn'))
    choicelists_to_install.append(('FAverageIn', 'Yes', 'An asian with average in'))
    
    # 2. ADD ADD_INFO_SPECS #
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FAverageType', 'FAverageType', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FFwdStart', 'FFwdStart', '', 0))
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Double', 'FFwdStartAlpha', 'Strike=FFwdStartAlpha*S(FFwdStartDay)', '1.0', 0))
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Date', 'FFwdStartDay', 'Start day for forward start options', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FAverageIn', 'FAverageIn', '', 0))
     
    # 3. ADD TIME_SERIES_SPECS #
    timeseries_to_create.append(('Instrument', 'FAveragePrices', 'Average prices'))
    timeseries_to_create.append(('Instrument', 'FAverageStrike', 'Average strike prices'))
    
    # 4. ADD CONTEXT LINKS #
    context_links_to_install.append((context, 'Valuation Function', 'FEqAverage.pv', '', 'ValGroup', 'EqAverage'))
    context_links_to_install.append((context, 'Valuation Extension', 'theorAverage', '', 'ValGroup', 'EqAverage'))
    

def add_barrier_parameters(context, ins_type):
    
    # 1. ADD CHOICE LISTS #
    if ins_type == 'Barrier':
        choicelists_to_install.append(('ValGroup', 'EqBarrier', 'Barrier Options'))
        choicelists_to_install.append(('Valuation Function', 'FEqBarrier.pv', 'Barrier Option valuation'))
        choicelists_to_install.append(('Valuation Extension', 'theorBarrier', 'Barrier Option valuation'))
        choicelists_to_install.append(('Category', 'Barrier', 'Equity Barrier Options'))
    else: 
        choicelists_to_install.append(('ValGroup', 'EqDoubleBarrier', 'Double Barrier Options'))
        choicelists_to_install.append(('Valuation Function', 'FEqDblBarrier.pv', 'Double Barrier Option valuation'))
        choicelists_to_install.append(('Valuation Extension', 'theorDblBarrier', 'Double Barrier Option valuation'))
        choicelists_to_install.append(('Category', 'DoubleBarrier', 'Equity Barrier options'))

    # FBarrierMonitorFrq is used by addinfo field FBarrierMonitorFrq
    choicelists_to_install.append(('', 'FBarrierMonitorFrq', 'Used by addinfo field FBarrierMonitorFrq'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Daily', 'Monitoring barrier daily'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Monthly', 'Monitoring barrier monthly'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Weekly', 'Monitoring barrier weekly'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Arbitrary', 'Monitoring barrier on arbitrary dates'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Continuous', 'Monitoring barrier continuously'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'DailyLastTwoWeeks', 'Monitoring barrier daily last two weeks'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'DailyLastMonth', 'Monitoring barrier daily last month'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'WeeklyLastMonth', 'Monitoring barrier weekly last month'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Yearly', 'Monitoring barrier yearly'))

    # FBarrier Crossed is used by addinfo field FBarrierCrossed
    choicelists_to_install.append(('', 'FBarrier Crossed', 'Used by addinfo field FBarrier Crossed'))
    choicelists_to_install.append(('FBarrier Crossed', 'Yes', 'The price has crossed the barrier'))
    choicelists_to_install.append(('FBarrier Crossed', 'Yes TEMP?', 'The price has crossed the barrier?'))
    
    # FBarrierModel is used by addinfo field FBarrierModel
    choicelists_to_install.append(('', 'FBarrierModel', 'Used by addinfo field FBarrierModel'))
    choicelists_to_install.append(('FBarrierModel', 'Analytical', 'Selects an analytical valuation model'))
    choicelists_to_install.append(('FBarrierModel', 'Trinomial', 'Selects a trinomial valuation model'))
    choicelists_to_install.append(('FBarrierModel', 'Monte Carlo', 'Selects a Monte Carlo valuation model'))
    
    # FBarrierModel is used by addinfo field FBarrierRebateDate
    choicelists_to_install.append(('', 'FBarrierPayRebate', 'Used by addinfo field FBarrierPayRebate'))
    choicelists_to_install.append(('FBarrierPayRebate', 'Expiry', 'The rebate is payed on expiry'))
    
    # 2. ADD ADD_INFO_SPECS #
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Double', 'FBarrier2', 'Second barrier for double barrier options', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FBarrier Crossed', 'FBarrier Crossed', '', 0))
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Date', 'FBarrier Cross Date', 'Barrier getting knocked at this date.', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FBarrierMonitorFrq', 'FBarrierMonitorFrq', '', 0))
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Double', 'FBarrier RiskMan', 'A second barrier for risk management.', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FBarrierModel', 'FBarrierModel', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FBarrierPayRebate', 'FBarrierPayRebate', '', 0))
    
    # 3. ADD TIME_SERIES_SPECS #
    timeseries_to_create.append(('Instrument', 'FBarrierMonitorDays', 'Monitor days.'))
    
    # 4. ADD CONTEXT LINKS #
    if ins_type == "Barrier": 
        context_links_to_install.append((context, 'Valuation Function', 'FEqBarrier.pv', '', 'ValGroup', 'EqBarrier'))
        context_links_to_install.append((context, 'Valuation Extension', 'theorBarrier', '', 'ValGroup', 'EqBarrier'))
    else: 
        context_links_to_install.append((context, 'Valuation Function', 'FEqDblBarrier.pv', '', 'ValGroup', 'EqDoubleBarrier'))
        context_links_to_install.append((context, 'Valuation Extension', 'theorDblBarrier', '', 'ValGroup', 'EqDoubleBarrier'))
    
def add_fwd_start_parameters(context):
    
    # 1. ADD CHOICE LISTS #
    choicelists_to_install.append(('ValGroup', 'EqFwdStart', 'Forward Start Options'))
    choicelists_to_install.append(('Valuation Function', 'FEqFwdStart.pv', 'Forward Start Option valuation'))
    choicelists_to_install.append(('Valuation Extension', 'theorFwdStart', 'Forward Start Option valuation'))
    choicelists_to_install.append(('Category', 'FwdStart', 'Forward Start Options'))

    # FFwdStart is used by addinfo field FFwdStart
    choicelists_to_install.append(('', 'FFwdStart', 'Used by addinfo field FFwdStart'))
    choicelists_to_install.append(('FFwdStart', 'Fwd Start', 'Forward start option'))
    choicelists_to_install.append(('FFwdStart', 'Fwd Start Perf', 'Forward start performance option'))
    
    # 2. ADD ADD_INFO_SPECS #
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Double', 'FFwdStartAlpha', 'Strike=FFwdStartAlpha*S(FFwdStartDay)', '1.0', 0))
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Date', 'FFwdStartDay', 'Start day for forward start options', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FFwdStart', 'FFwdStart', '', 0))
    
    # 4. ADD CONTEXT LINKS #
    context_links_to_install.append((context, 'Valuation Function', 'FEqFwdStart.pv', '', 'ValGroup', 'EqFwdStart'))
    context_links_to_install.append((context, 'Valuation Extension', 'theorFwdStart', '', 'ValGroup', 'EqFwdStart'))
    
    
def add_basket_parameters(context):
    
    # 1. ADD CHOICE LISTS #
    choicelists_to_install.append(('ValGroup', 'EqBasket', 'Basket Options'))
    choicelists_to_install.append(('Valuation Function', 'FEqBasket.pv', 'Basket Option valuation'))
    choicelists_to_install.append(('Valuation Extension', 'theorBasket', 'Basket Option valuation'))
    choicelists_to_install.append(('Category', 'Basket', 'Basket Options'))
    choicelists_to_install.append(('', 'Parameter List', 'Used to display AEL valuation params.'))
    choicelists_to_install.append(('Parameter List', 'BasketOption', 'Params for basket options.'))
    
    # 4. ADD CONTEXT LINKS #
    context_links_to_install.append((context, 'Valuation Function', 'FEqBasket.pv', '', 'ValGroup', 'EqBasket'))
    context_links_to_install.append((context, 'Valuation Extension', 'theorBasket', '', 'ValGroup', 'EqBasket'))
    context_links_to_install.append((context, 'Parameter List', 'BasketOption', '', 'ValGroup', 'EqBasket'))
    
    
def add_rainbow_parameters(context):
    
    # 1. ADD CHOICE LISTS #
    choicelists_to_install.append(('ValGroup', 'EqRainbow', 'Rainbow Options'))
    choicelists_to_install.append(('Valuation Function', 'FEqRainbow.pv', 'Rainbow Option valuation'))
    choicelists_to_install.append(('Valuation Extension', 'theorRainbow', 'Rainbow Option valuation'))
    choicelists_to_install.append(('Category', 'Rainbow', 'Rainbow Options'))
    choicelists_to_install.append(('', 'Parameter List', 'Used to display AEL valuation params.'))
    choicelists_to_install.append(('Parameter List', 'RainbowOption', 'Params for rainbow options.'))
    
    # FRainbowType is used by addinfo field FRainbowType
    choicelists_to_install.append(('', 'FRainbowType', 'Used by addinfo field FRainbowType'))
    choicelists_to_install.append(('FRainbowType', 'Best of Two', 'BOT Rainbow option'))
    choicelists_to_install.append(('FRainbowType', 'Worst of Two', 'WOT Rainbow option'))
    choicelists_to_install.append(('FRainbowType', 'Max of Two', 'Max Rainbow option'))
    choicelists_to_install.append(('FRainbowType', 'Min of Two', 'Min Rainbow option'))

    
    # 2. ADD ADD_INFO_SPECS #
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FRainbowType', 'FRainbowType', '', 0))

    
    # 4. ADD CONTEXT LINKS #
    context_links_to_install.append((context, 'Valuation Function', 'FEqRainbow.pv', '', 'ValGroup', 'EqRainbow'))
    context_links_to_install.append((context, 'Valuation Extension', 'theorRainbow', '', 'ValGroup', 'EqRainbow'))
    context_links_to_install.append((context, 'Parameter List', 'RainbowOption', '', 'ValGroup', 'EqRainbow'))


def add_cliquet_parameters(context):
    
    # 1. ADD CHOICE LISTS #
    choicelists_to_install.append(('ValGroup', 'EqCliquet', 'Cliquet options.'))
    choicelists_to_install.append(('Valuation Function', 'FEqCliquet.pv', 'Cliquet Option valuation'))
    choicelists_to_install.append(('Valuation Extension', 'theorCliquet', 'Cliquet Option valuation'))
    choicelists_to_install.append(('Category', 'Cliquet', 'Cliquet Options'))

    # FFwdStart is used by addinfo field FFwdStart
    choicelists_to_install.append(('', 'FFwdStart', 'Used by addinfo field FFwdStart'))
    choicelists_to_install.append(('FFwdStart', 'Fwd Start', 'Forward start option'))
    choicelists_to_install.append(('FFwdStart', 'Fwd Start Perf', 'Forward start performance option'))
    
    # FCliquetType is used by addinfo field FCliquetType
    choicelists_to_install.append(('', 'FCliquetType', 'Used by addinfo field FCliquetType'))
    choicelists_to_install.append(('FCliquetType', 'Cliquet End', 'Cliquet pay in the end'))
    choicelists_to_install.append(('FCliquetType', 'Cliquet Go', 'Cliquet pay as you go'))
    
    # 2. ADD ADD_INFO_SPECS #
    addinfospecs_to_install.append(('Instrument', 'Standard', 'Double', 'FFwdStartAlpha', 'Strike = FFwdStartAlpha*S(FFwdStartDay)', '1.0', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FFwdStart', 'FFwdStart', '', 0))
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FCliquetType', 'FCliquetType', '', 0))
    
    # 3. ADD TIME_SERIES_SPECS #
    timeseries_to_create.append(('Instrument', 'FCliquetResetDays', 'Reset days for a Cliquet option.'))
    
    # 4. ADD CONTEXT LINKS #
    context_links_to_install.append((context, 'Valuation Function', 'FEqCliquet.pv', '', 'ValGroup', 'EqCliquet'))
    context_links_to_install.append((context, 'Valuation Extension', 'theorCliquet', '', 'ValGroup', 'EqCliquet'))
    
def add_ladder_parameters(context):
    
    # 1. ADD CHOICE LISTS #
    choicelists_to_install.append(('ValGroup', 'EqLadder', 'Ladder options.'))
    choicelists_to_install.append(('Valuation Function', 'FEqLadder.pv', 'Ladder Option valuation'))
    choicelists_to_install.append(('Valuation Extension', 'theorLadder', 'Ladder Option valuation'))
    choicelists_to_install.append(('Category', 'Ladder', 'Ladder Options'))

    # FBarrierMonitorFrq is used by addinfo field FBarrierMonitorFrq
    choicelists_to_install.append(('', 'FBarrierMonitorFrq', 'Used by addinfo field FBarrierMonitorFrq'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Daily', 'Monitoring barrier daily'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Monthly', 'Monitoring barrier monthly'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Weekly', 'Monitoring barrier weekly'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Arbitrary', 'Monitoring barrier on arbitrary dates'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Continuous', 'Monitoring barrier continuously'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'DailyLastTwoWeeks', 'Monitoring barrier daily last two weeks'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'DailyLastMonth', 'Monitoring barrier daily last month'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'WeeklyLastMonth', 'Monitoring barrier weekly last month'))
    choicelists_to_install.append(('FBarrierMonitorFrq', 'Yearly', 'Monitoring barrier yearly'))
    
    # 2. ADD ADD_INFO_SPECS #
    addinfospecs_to_install.append(('Instrument', 'RecordRef', 'ChoiceList', 'FBarrierMonitorFrq', 'FBarrierMonitorFrq', '', 0))
    
    # 3. ADD TIME_SERIES_SPECS # 
    timeseries_to_create.append(('Instrument', 'FLadderRungs', 'The rungs of a ladder option.'))
    
    # 4. ADD CONTEXT LINKS #
    context_links_to_install.append((context, 'Valuation Function', 'FEqLadder.pv', '', 'ValGroup', 'EqLadder'))
    context_links_to_install.append((context, 'Valuation Extension', 'theorLadder', '', 'ValGroup', 'EqLadder'))


b92_type_dict = {
    # Standard data types
    'None'    : 0, 
    'Integer' : 1,
    'Char'    : 2,
    'String'  : 3,
    'Double'  : 4,
    'Boolean' : 5,
    'Date'    : 6,
    'Time'    : 7, 
    'DateTime': 8,
    # RecordRef types
 
    # A choice list reference seems to be 32?!   
    'ChoiceList' : 32 
    }
    

def install_choicelist(list_to_install):
    ''' 
    Install new choice lists and choice list items.
    The list is required to be a list of tuples on 
    the following format:
        
    (<list to which it belongs>,<name of this entry>,<description>)             
    
    '''
    for cl_tuple in list_to_install:
        if cl_tuple[0] == '':
            # Empty name means create new list
            group = 'MASTER'
        else: group = cl_tuple[0]
        c_list = ael.ChoiceList[group]
        has_entry = 0
        if c_list != None:
            try:
                for member in c_list.members():
                    if member.entry == cl_tuple[1]:
                        has_entry = 1
                        break
            except: pass

        if not has_entry:
            cl = ael.ChoiceList.new()
            if cl_tuple[0] == '':
                # Empty name means create new list
                cl.list = 'MASTER'
            else:
                cl.list = cl_tuple[0]
            cl.entry = cl_tuple[1]

            # A description can only be 39 characters
            cl.description = cl_tuple[2][:39]

            try:
                cl.commit()
                print "Installed ChoiceList entry: ", cl_tuple[1], " in list ", cl_tuple[0]
                ael.poll()
            except Exception, msg:
                if str(msg) == 'Commit failed (Duplicate)':
                    # The entry did already exist
                    #print 'List:',cl.list,',Entry:',cl.entry,'did already exist'
                    pass
                else:
                    print 'ERROR: Could not create List:', cl.list, ',Entry:', cl.entry, '.'
                    print "!!#", str(msg), "#!!"
                    print



def install_addinfo(list_to_install):
    ''' 
    Install new additional info specifications.
    The list is required to be a list of tuples on 
    the following format:
        
    (<Table>, <TypeGroup>, <TypeSpecification>, <FieldName>, <Description>, <Default>, <Mandatory>)
    
    '''
    for ai_tuple in list_to_install:
        if ael.AdditionalInfoSpec[ai_tuple[3]] == None:
            ais = ael.AdditionalInfoSpec.new()
            setattr(ais, 'rec_type', ai_tuple[0])
            setattr(ais, 'data_type.grp', ai_tuple[1])

            try:
                value = b92_type_dict[ai_tuple[2]]
            except:
                # ai_tuple][2] not found in dictionary
                print 'ERROR: Type', ai_tuple[2], 'unknown. Inserting \
                    addinfospec', ai_tuple[3], 'failed.'
                continue

            setattr(ais, 'data_type.type', value)
            ais.field_name = ai_tuple[3]
            ais.description = ai_tuple[4][:39]
            ais.default_value = ai_tuple[5]
            ais.mandatory = ai_tuple[6]

            try:
                ais.commit()
                print "Installed AdditionalInfoSpec: ", ai_tuple[3]
            except Exception, msg:
                if str(msg) == 'Commit failed (Duplicate)':
                    # The entry did already exist
                    #print 'Addinfospec',ais.field_name,'did already exist.'
                    pass
                else:
                    print 'ERROR: Could not create addinfospec', ais.field_name
                    print "!!#", str(msg), "#!!"
                    print
                    


def get_choice_list_item(group, entry):
    '''
    Return the choice list with name entry 
    in the choice list group, or None if not 
    found
    
    '''
    ret_value = None
    group = ael.ChoiceList[group]
    if not (group == None):
        for cl in group.members():
            if cl.entry == entry:
                ret_value = cl
                break
    return ret_value


def install_context_links(list_to_install):
    '''
    Install new context links.
    The list is required to be a list of tuples on 
    the following format:

    (<ContextName>, <Type>, <Name>, <InstrumentName>, <ChoiceListName>, <ChoiceListEntryName>)

    '''
    ael.poll()
    context = None
    rebind = 0

    for context_tuple in list_to_install:
        if context == None: rebind = 1
        else:
            if not (context.name == context_tuple[0]):
                # This link belongs to a different context
                # than the one currently being used, rebind.
                rebind = 1
                
        if rebind == 1:
            context = ael.Context[context_tuple[0]]

            if context == None:
                # The context did not exist, create a new
                try:
                    context = ael.Context.new()
                    context.name = context_tuple[0]
                    context.commit()
                except:
                    print 'ERROR creating new context'
            rebind = 0
        
        has_link = 0
        for link in context.links():
            if link.group_chlnbr != None:
                if context_tuple[1] == link.type and \
                   context_tuple[2] == link.name and \
                   context_tuple[4] == link.group_chlnbr.list and \
                   context_tuple[5] == link.group_chlnbr.entry:
                    has_link = 1
                    break
            
        if not has_link:
            context_clone = context.clone()
            try:
                context_link = ael.ContextLink.new(context_clone)
            except: 
                context_link = ael.ContextLink.new()
            
            try:context_link.type = context_tuple[1]
            except Exception, msg:
                if context_tuple[1] == 'Parameter List': 
                    print "The Context type Parameter List does not exist in ATLAS 3.1.x"
                    break
                else:
                    print "!!# EXCEPTION #!!"
                    print "Error: The Context Link Type ", context_tuple[1], " is not handled by this client. Use an older version of this script.\n"
                    raise
                    
            if hasattr(context_link, 'mapping_type'):
                try:
                    # Works for ATLAS 3.2.0 - 3.2.2
                    context_link.mapping_type = context_tuple[1]
                except: 
                    # Works for ATLAS 3.2.3 - 3.3.x
                    context_link.mapping_type = "Val Group"

            context_link.name = context_tuple[2]
            if not (context_tuple[3] == ''):
                i = ael.Instrument[context_tuple[3]]
                if not (i == None):
                    context_link.insaddr = i
                else:
                    print 'ERROR: Instrument', context_tuple[3], 'not found' \
                        ' when creating a context link to', context_tuple[2]

            cl = get_choice_list_item(context_tuple[4], context_tuple[5])
            if not (cl == None):
                context_link.group_chlnbr = cl

            try:
                context_link.commit()
                print "Installed Context Link: ", str(context_tuple)
            except Exception, msg:
                print 'ERROR: Could not create context link', context_link.name
                print "!!#", str(msg), "#!!"
                print

            try:
                context_clone.commit()
            except Exception, msg:
                print 'ERROR: Could not create context', context.name
                print "!!#", str(msg), "#!!"
                print

def create_timeseries(series_to_create):    
    '''
    Each tuple is on the form: 'record type','name','description'
    '''
    for time_tuple in series_to_create:
        if ael.TimeSeriesSpec[time_tuple[1]] == None:
            time = ael.TimeSeriesSpec.new()
            time.rec_type = time_tuple[0]
            time.field_name = time_tuple[1]
            time.description = time_tuple[2]
            try:
                time.commit()
                print "Installed the TimeSeriesSpec: ", str(time_tuple[1])
            except Exception, msg:
                print 'ERROR: Could not create time seriesspecification', time_tuple[1]
                print "!!#", str(msg), "#!!"
                print
        #else: print "The timeserie " , time_tuple[1] , " did already exist." 



"""----------------------------------------------------------------------------
Verify that the ValGroup, Valuation Function, Valuation Extension, Category and 
Parameter List entries exist.
----------------------------------------------------------------------------"""
group = ael.ChoiceList['MASTER']
has_valgroup = 0; has_valfunction = 0; has_param_list = 0
has_category = 0; has_valextension = 0
for cl in group.members():
    if has_valgroup and has_valfunction and has_param_list and \
    has_category and has_valextension: break
    if   cl.entry == 'ValGroup':           has_valgroup    = 1
    elif cl.entry == 'Valuation Function': has_valfunction = 1
    elif cl.entry == 'Parameter List':     has_param_list  = 1
    elif cl.entry == 'Category':           has_category    = 1
    elif cl.entry == 'Valuation Extension':has_valextension= 1
    
choicelists_to_install = []
if not has_valgroup: 
    choicelists_to_install.append(('', 'ValGroup', 'Valuation groups'))
if not has_valfunction: 
    choicelists_to_install.append(('', 'Valuation Function', 'Valuation functions'))
if not has_param_list:
    choicelists_to_install.append(('', 'Parameter List', 'List of valuation params.'))
if not has_category:    
    choicelists_to_install.append(('', 'Category', 'Instrument categories.'))
if not has_valextension:    
    choicelists_to_install.append(('', 'Valuation Extension', 'ADFL valuation functions.'))
if len(choicelists_to_install) != 0:
    install_choicelist(choicelists_to_install)


"""----------------------------------------------------------------------------
Create the page "NonSplitIndexes" under the PageList "FPages".
----------------------------------------------------------------------------"""
def get_parent_ids():
    page_dict = {}
    pages = ael.ListNode.select()
    for page in pages: 
        if page.father_nodnbr == None:
            page_dict[page.id] = 1
    return page_dict
    
def get_pages(parent_id):
    page_dict = {}
    pages = ael.ListNode.select()
    for page in pages: 
        if page.father_nodnbr != None:
            parent_page = ael.ListNode[page.father_nodnbr.nodnbr].id
            if parent_page == parent_id and page.terminal:
                page_dict[page.id] = 1
    return page_dict

def get_parent_nodnbr(parent_id):
    pages = ael.ListNode.select()
    for page in pages: 
        if page.id == parent_id:
            if page.father_nodnbr == None:
                return page.nodnbr
    return -1

def create_page(parent_id, page_id):
    parents_dict = get_parent_ids()
    parent_exists = 0
    # Check if the parent page exists
    if parents_dict.has_key(parent_id): parent_exists = 1
    if not parent_exists:
        # Create the pagelist parent_id
        page = ael.ListNode.new()
        page.id = parent_id
        page.commit()
        ael.poll()
        print "Created the ListNode " + parent_id + " in the PageDefinition application."
    # Find all the pages under the list parent_id 
    pages_under_parent = get_pages(parent_id)
    page_exists = 0
    if pages_under_parent.has_key(page_id):
        page_exists = 1
    if not page_exists:
        # Create the page page_id
        page = ael.ListNode.new()
        page.id = page_id
        page.terminal = 1
        parent_nodnbr = get_parent_nodnbr(parent_id)
        if parent_nodnbr != -1:
            page.father_nodnbr = parent_nodnbr
        else:
            raise "ERROR ", "No father node number."
        page.commit()
        ael.poll()
        print "Created the ListNode " + page_id + " in the PageDefinition application."

    return 1

create_page("FPages", "NonSplitIndexes")



