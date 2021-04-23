'''
Purpose                       :  [Listens to and stores changes for valuation data],[Removed the listener on VolPoints]
Department and Desk           :  [PCG MO],[PCG MO]
Requester                     :  [Dirk Strauss],[Dirk Strauss]
Developer                     :  [Zaakirah Kajee],[Willie van der Bank]
CR Number                     :  [433267 2010-09-16],[450116 2010-10-01],[483599 2010-11-04],[488208 2010-11-09],[520263 2010-12-09],[238001 2012-06-07]
'''

import acm, ael, csv, time
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

excl = ['creat_time', 'updat_time', 'creat_usrnbr', 'updat_usrnbr', 'version_id', 'record_type', 'seqnbr', 'volatility', 'value', 'reference_day']

port_excl = ['ias_class_chlnbr', 'owner_ptynbr', 'curr', 'ias_class_chlnbr', 'owner_ptynbr', 'prfnbr', 'type_chlnbr',
 'weekend_days', 'mtm_ptynbr', 'owner_usrnbr', 'authorizer_usrnbr', 'product_chlnbr', 'instrument', 'yield_curve_seqnbr',
'pay_calnbr', 'price_finding_chlnbr', 'category_chlnbr', 'reset_calnbr', 'insaddr', 'group_chlnbr', 'context_seqnbr', 'issuer_ptynbr',
'country_chlnbr', 'rating3_chlnbr', 'rating2_chlnbr', 'rating1_chlnbr', 'underlying_yield_curve_seqnbr', 'seniority_chlnbr', 'calnbr',
'currency_pair', 'curr_pair_seqnbr', 'ref_insaddr', 'ptynbr', 'fx_base_currency', 'accounting_currency', 'acquirer_ptynbr', 'curr1', 'curr2',
'frw_calendar_calnbr', 'frw_prfnbr', 'frw_split_curr', 'spot_calendar_calnbr', 'spot_prfnbr', 'spot_split_curr', 'sweep_curr']

object_id = {'Calendar':'calnbr', 'CalendarDate':'seqnbr', 'Context':'seqnbr','ContextLink':'seqnbr', 'AccountingParameters':'seqnbr',
'ValuationParameters':'seqnbr', 'Instrument': 'insaddr', 'Portfolio': 'prfnbr', 'PortfolioLink':'lnknbr', 'Leg':'legnbr',
'YieldCurve':'seqnbr', 'YieldCurvePoint':'seqnbr', 'YCAttribute':'seqnbr', 'Volatility': 'seqnbr', 'VolPoint':'seqnbr',
'Benchmark':'seqnbr', 'YCSpread':'seqnbr', 'CurrencyPair':'seqnbr'}

object_name = {'Calendar':'calid', 'CalendarDate':'calnbr.calid', 'Context':'name', 'ContextLink':'context_seqnbr.name',
'AccountingParameters':'name' ,'ValuationParameters':'name', 'Instrument': 'insid','Portfolio': 'prfid', 'PortfolioLink':'member_prfnbr.prfid',
'YieldCurve':'yield_curve_name','Leg':'insaddr.insid', 'YieldCurvePoint':'yield_curve_seqnbr.yield_curve_name',
'YCAttribute':'yield_curve_seqnbr.yield_curve_name','Volatility': 'vol_name',  'VolPoint':'vol_seqnbr.vol_name' ,
 'Benchmark':'yield_curve_seqnbr.yield_curve_name', 'YCSpread':'point_seqnbr.yield_curve_seqnbr.yield_curve_name', 'CurrencyPair':'name'}

identify ={'context_seqnbr': 'context_seqnbr.name','underlying_yield_curve_seqnbr':'underlying_yield_curve_seqnbr.yield_curve_name',
'curr':'curr.insid',  'insaddr':'insaddr.insid','currency_pair':'currency_pair.name',
'instrument': 'instrument.insid','yield_curve_seqnbr':'yield_curve_seqnbr.yield_curve_name','curr_pair_seqnbr':'curr_pair_seqnbr.name',
'ref_insaddr':'ref_insaddr.insid', 'und_vol_seqnbr':'und_vol_seqnbr.vol_name', 'vol_seqnbr':'vol_seqnbr.vol_name', 
'accounting_currency':'accounting_currency.insid','fx_base_currency': 'fx_base_currency.insid', 'point_seqnbr': 'point_seqnbr.seqnbr',
'attribute_seqnbr':'attribute_seqnbr.seqnbr' }

id_excp = ['curr', 'instrument', 'yield_curve_seqnbr', 'context_seqnbr', 'underlying_yield_curve_seqnbr', 'curr_pair_seqnbr',
'und_vol_seqnbr', 'currency_pair', 'vol_seqnbr', 'fx_base_currency', 'accounting_currency', 'point_seqnbr', 'attribute_seqnbr']

days = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
#path = 'F:\\Test\\'
path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/' 
dateS = ael.date_today().to_string('%Y-%m-%d')
global_file = path + 'AUDIT_LISTENER_' + dateS + '.xml'
t1=t0 = time.time()
AUDIT = Element("VALUATION_STATIC_AUDIT", date = dateS)
DETAIL = SubElement(AUDIT, "DETAIL")
uflag =0

#       ================================================================================================================
#                                               TASK MANAGER
#       ================================================================================================================


def start():
    ael.log('Starting Update handler ......')
    
    ael.Calendar.subscribe(ServerUpdate)
    ael.CalendarDate.subscribe(ServerUpdate)
    ael.Context.subscribe(ServerUpdate)
    ael.ContextLink.subscribe(ServerUpdate)
    ael.AccountingParameters.subscribe(ServerUpdate)
    ael.ValuationParameters.subscribe(ServerUpdate)
    ael.Portfolio.subscribe(ServerUpdate)
    ael.PortfolioLink.subscribe(ServerUpdate)
    ael.Instrument.select('instype = "Curr"').subscribe(ServerUpdate)
    ael.Instrument.select('instype = "RateIndex"').subscribe(ServerUpdate)
    ael.Leg.subscribe(ServerUpdate)
    ael.YieldCurve.subscribe(ServerUpdate)
    ael.YieldCurvePoint.subscribe(ServerUpdate)
    ael.YCAttribute.subscribe(ServerUpdate)
    ael.Volatility.subscribe(ServerUpdate)
    #Removing the listener on VolPoints
    #ael.VolPoint.subscribe(ServerUpdate)
    ael.Benchmark.subscribe(ServerUpdate)
    ael.CurrencyPair.subscribe(ServerUpdate)


def stop():
    ael.log('Update Handler stopped..')
    try:
        ael.Calendar.unsubscribe(ServerUpdate)
        ael.CalendarDate.unsubscribe(ServerUpdate)
        ael.Context.unsubscribe(ServerUpdate)
        ael.ContextLink.unsubscribe(ServerUpdate)
        ael.AccountingParameters.unsubscribe(ServerUpdate)
        ael.ValuationParameters.unsubscribe(ServerUpdate)
        ael.Portfolio.unsubscribe(ServerUpdate)
        ael.PortfolioLink.unsubscribe(ServerUpdate)
        ael.Instrument.select('instype = "Curr"').unsubscribe(ServerUpdate)
        ael.Instrument.select('instype = "RateIndex"').unsubscribe(ServerUpdate)
        ael.Leg.unsubscribe(ServerUpdate)
        ael.YieldCurve.unsubscribe(ServerUpdate)
        ael.YieldCurvePoint.unsubscribe(ServerUpdate)
        ael.YCAttribute.unsubscribe(ServerUpdate)
        ael.Volatility.unsubscribe(ServerUpdate)
        #Removing the listener on VolPoints
        #ael.VolPoint.unsubscribe(ServerUpdate)
        ael.Benchmark.unsubscribe(ServerUpdate)
        ael.CurrencyPair.unsubscribe(ServerUpdate)
    except:
        ael.log('FAILED TO UNSUBSCRIBE TO DATA') 
        
    try: 
        xmloutFile=open(global_file, 'w')
        ElementTree(AUDIT).write(xmloutFile, encoding='utf-8')
        xmloutFile.close()
    except: 
        ael.log('ERROR WRITING XML FILE')
    
    
def status():
    pass


#       ================================================================================================================
#                                               GENERIC FUNCTIONS
#       ================================================================================================================

def format_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
     
def compare_objects(old, new):
    oldL= old.to_string().split('|')
    newL= new.to_string().split('|')
    col = new.columns()
    return [ [col[a], oldL[a], newL[a]] for a in range(0, len(oldL)) if oldL[a] != newL[a] and col[a] not in excl ]

def gen_cldict(obj):
    dict = {'Instrument' : '', 'Group': '', 'Curr':'', 'Attr1':obj.attribute0,'Attr2':obj.attribute1,'Attr3':obj.attribute2, 
    'MappingType': obj.mapping_type, 'ParameterName': obj.name , 'ParameterType': obj.type} 
    if obj.insaddr: dict['Instrument'] = obj.insaddr.insid
    if obj.prfnbr:  dict['Instrument'] = obj.prfnbr.prfid
    if obj.group_chlnbr: dict['Group'] = obj.group_chlnbr.entry
    if obj.curr: dict['Curr'] = obj.curr.insid
    return dict
    
def generate_header(obj, op):
    ENTITY = Element("ENTITY")
    SubElement(ENTITY, "OBJECT").text = obj.record_type
    SubElement(ENTITY, "OBJECT_NAME").text = eval("obj." + object_name[obj.record_type])
    SubElement(ENTITY, "OBJECT_ID").text = str(eval("obj." + object_id[obj.record_type]))
    if op == 'Insert':
        SubElement(ENTITY, "CREATE_TIME").text = format_time(obj.creat_time)
        SubElement(ENTITY, "CREATE_USER").text = obj.creat_usrnbr.name
        SubElement(ENTITY, "CREATE_USERGROUP").text = obj.creat_usrnbr.grpnbr.grpid
    else:
        SubElement(ENTITY, "UPDATE_TIME").text = format_time(obj.updat_time)
        SubElement(ENTITY, "UPDATE_USER").text = obj.updat_usrnbr.name
        SubElement(ENTITY, "UPDATE_USERGROUP").text = obj.updat_usrnbr.grpnbr.grpid
    SubElement(ENTITY, "OPERATION").text = op
    return ENTITY
    
def identify_col(obj, col, val =1):
    if val in ['0', 'None', '']:
        return 'None'
    
    if col not in id_excp:
        if col.find('ptynbr')  >= 0:
            return eval('obj.' + col + '.ptyid')
        elif col.find('chlnbr') >= 0:
            return eval('obj.' + col + '.entry')
        elif col.find('usrnbr') >= 0:
            return eval('obj.' + col + '.name')
        elif col.find('calnbr') >= 0:
            return eval('obj.' + col + '.calid')
        elif col.find('prfnbr') >= 0:
            return eval('obj.' + col + '.prfid')
        elif col.find('insaddr') >= 0:
            return eval('obj.' + col + '.insid') 
        elif col.find('curr') >= 0:
            return eval('obj.' + col + '.insid')
        else:
            return 'ERROR'
    else:
        try:
            return eval("obj." + identify[col])
        except:
            return 'ERROR'
            
def get_we(num):
    bin = []
    if num == 0:
        return 'None'
     
    while num:
        bin.append(num%2)
        num /= 2
    if len(bin) == 7:
        bin.append(0)
    
    bin.remove(0)
    bin= bin[::-1]
    final = ''
    for i in range(len(bin)):
        if bin[i] ==1:
            final += days[i] + ' '
    return final
    
    
def get_links(port):
    return ael.PortfolioLink.select('member_prfnbr = %d' %(port.prfnbr))

def get_port_struc(port):
    res = ''
    flag = 1
    ms = ''
    resl = []
    while flag == 1:
        pl = get_links(port)
        
        if len(pl) == 0:
            flag = 0
            if res == '':
                res = port.prfid  
        elif not pl[0].owner_prfnbr:
            res += ms + port.prfid  
            flag = 0
        else:
            res += ms + port.prfid  
            port = pl[0].owner_prfnbr
            if len(pl) > 1:
                for i in range(1, len(pl)):
                    resl.append(res + ' -> ' + get_port_struc(pl[i].owner_prfnbr)[0])
            ms = ' -> '
    resl.append(res)
    return resl

#       ================================================================================================================
#                                               OBJECT SPECIFIC PROCESSING
#       ================================================================================================================

    
def parent_update(obj):
    global DETAIL, uflag
    old = ael.get_old_entity()
    diff = compare_objects(old, obj)
    if len(diff) > 0:
        ENTITY = generate_header(obj, 'Update')
        AMENDS = SubElement(ENTITY, "AMENDMENTS")
        for d in diff:
            CHANGE = SubElement(AMENDS, "CHANGE")
            SubElement(CHANGE, "FIELD").text = d[0]
            if d[0] in port_excl:
                if d[0] == 'weekend_days':
                    SubElement(CHANGE, "ORIGINAL_VALUE").text = get_we(old.weekend_days)
                    SubElement(CHANGE, "NEW_VALUE").text = get_we(obj.weekend_days)
                else:
                    SubElement(CHANGE, "ORIGINAL_VALUE").text = identify_col(old, d[0], d[1])
                    SubElement(CHANGE, "NEW_VALUE").text = identify_col(obj, d[0], d[2])
            else:
                SubElement(CHANGE, "ORIGINAL_VALUE").text = d[1]
                SubElement(CHANGE, "NEW_VALUE").text = d[2]
        if obj.record_type == 'ContextLink':
            SubElement(AMENDS, "CURRENT_LINK", gen_cldict(obj))
            SubElement(AMENDS, "OLD_LINK", gen_cldict(old))          
        DETAIL.append(ENTITY)
        uflag = 1
    
def parent_insert(obj):
    
    global DETAIL
    ENTITY = generate_header(obj, 'Insert')
    AMENDS = SubElement(ENTITY, "AMENDMENTS")
    newL= obj.to_string().split('|')
    col = obj.columns()
    for d in range(0, len(newL)):
        if col[d] not in excl and newL[d] not in ['0', 'None', '']:
            CHANGE = SubElement(AMENDS, "CHANGE")
            SubElement(CHANGE, "FIELD").text = col[d]
            if col[d] not in port_excl or col[d] == object_id[obj.record_type]:
                SubElement(CHANGE, "NEW_VALUE").text = newL[d]
            else:
                if col[d] == 'weekend_days':
                    SubElement(CHANGE, "NEW_VALUE").text = get_we(obj.weekend_days)
                else:
                    SubElement(CHANGE, "NEW_VALUE").text = identify_col(obj, col[d], newL[d])
    if obj.record_type == 'ContextLink':
        SubElement(AMENDS, "CURRENT_LINK", gen_cldict(obj))
    DETAIL.append(ENTITY)
    
    
def object_delete(obj):
   
    global DETAIL
    ENTITY = generate_header(obj, 'Delete')
    AMENDS = SubElement(ENTITY, "AMENDMENTS")
    newL= obj.to_string().split('|')
    col = obj.columns()
    for d in range(0, len(newL)):
        if col[d] not in excl and newL[d] not in ['0', 'None', '']:
            CHANGE = SubElement(AMENDS, "CHANGE")
            SubElement(CHANGE, "FIELD").text = col[d]
            if col[d] not in port_excl or col[d] == object_id[obj.record_type]:
                SubElement(CHANGE, "VALUE").text = newL[d]
            else:
                if col[d] == 'weekend_days':
                    SubElement(CHANGE, "VALUE").text = get_we(obj.weekend_days)
                else:
                    SubElement(CHANGE, "VALUE").text = identify_col(obj, col[d], newL[d])
                    
    if obj.record_type == 'ContextLink':
        SubElement(AMENDS, "CURRENT_LINK", gen_cldict(obj))
    DETAIL.append(ENTITY)
        
 
def PortLink_insert(obj): 
    
    global DETAIL
    ENTITY = generate_header(obj, 'Insert')
    AMENDS = SubElement(ENTITY, "AMENDMENTS")
    links = get_port_struc(obj.member_prfnbr)
    CHANGE = SubElement(AMENDS, "CHANGE")
    for l in links:
        SubElement(CHANGE, "PORT_LINK").text = l
    DETAIL.append(ENTITY)
        
def PortLink_delete(obj):
    
    global DETAIL
    ENTITY = generate_header(obj, 'Delete')
    AMENDS = SubElement(ENTITY, "AMENDMENTS")
    links = get_port_struc(obj.owner_prfnbr)
    CHANGE = SubElement(AMENDS, "CHANGE")
    for l in links:
        SubElement(CHANGE, "PORT_LINK").text = obj.member_prfnbr.prfid + ' -> ' + l
    DETAIL.append(ENTITY)    
    
            
#       ================================================================================================================
#                                               LISTENER 
#       ================================================================================================================
    
def ServerUpdate(sender,obj,param, op, *rest):

    global t1, t0, uflag
    
    if obj.creat_usrnbr:
        if (obj.record_type == 'Leg' and obj.insaddr.instype not in ('Curr', 'RateIndex')):  
            return
        elif (obj.record_type == 'Volatility' and obj.add_info('Prod_Vol') in ('False', 'No')):
            return
        elif ( obj.record_type == 'YieldCurve' and obj.add_info('Prod_YC') in ('False', 'No')):
            return
        elif (obj.record_type == 'YieldCurvePoint' and obj.yield_curve_seqnbr.add_info('Prod_YC') in ('False', 'No')):
            return
        elif (obj.record_type == 'YCAttribute' and obj.yield_curve_seqnbr.add_info('Prod_YC') in ('False', 'No')):
            return
        #Removing the listener on VolPoints
        #elif (obj.record_type == 'VolPoint' and obj.vol_seqnbr.add_info('Prod_Vol') in ('False', 'No')):
        #    return
        elif obj.record_type == 'ContextLink' and obj.context_seqnbr.name != 'ACMB Global':
            return
        elif obj.record_type == 'Context' and obj.name != 'ACMB Global':
            return
        elif obj.record_type == 'Benchmark' and obj.yield_curve_seqnbr.add_info('Prod_YC') in ('False', 'No'):
            return
        else:
            t1= time.time()
            if obj.record_type != 'PortfolioLink':
                    if op == 'update':
                        parent_update(obj)
                    elif op == 'insert':
                        parent_insert(obj)
                    else:
                        object_delete(obj)                 
          
            elif obj.record_type == 'PortfolioLink':
                if op == 'insert':
                    PortLink_insert(obj)
                    
                if op == 'delete':
                    try:
                        PortLink_delete(obj)                      
                    except:
                        ael.log('Error obtaining portfolio Link info')
                        
            if t1 - t0 > 5 and (uflag == 1 or op != 'update'):
                uflag = 0
                try:
                    xmloutFile=open(global_file, 'w')
                    xmloutFile.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
                    xmloutFile.write('<?xml-stylesheet type="text/xsl" href="Y:\Jhb\FAReports\AtlasEndOfDay\TradeAmendment\ValStatic.xsl"?>\n')
                    ElementTree(AUDIT).write(xmloutFile)
                    xmloutFile.close()
                    
                except:
                    ael.log('Error writing to file')
                t0 = t1

#start()
#stop()
