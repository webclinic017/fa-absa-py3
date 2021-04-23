""" SEQ_VERSION_NR = PRIME 2.8.1 """



"""----------------------------------------------------------------------------
MODULE
    FUpgradeCliquetAndRainbow
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Since the definitions of cliquet and rainbow options have changed, these 
    functions searches through the database and updates the already defined 
    cliquet and rainbow options.
    
    CLIQUET OPTIONS
        ValGroup
            EqCliquetGo  => EqCliquet
            EqCliquetEnd => EqCliquet
        Category
            CliquetGo  => Cliquet
            CliquetEnd => Cliquet
        AddInfo
            FCliquetType => Either 'Cliquet End' or 'Cliquet Go'
    
    RAINBOW OPTIONS
        ValGroup      
            EqRainbowBOT => EqRainbow
            EqRainbowWOT => EqRainbow
            EqRainbowMax => EqRainbow
            EqRainbowMin => EqRainbow
        Category
            RainbowBOT => Rainbow
            RainbowWOT => Rainbow
            RainbowMax => Rainbow
            RainbowMin => Rainbow
        AddInfo
            FRainbowType => Either 'Best of Two', 'Worst of Two', 
                                   'Max of Two' or 'Min of Two'
                                   
    The script only has to be run once. 
----------------------------------------------------------------------------"""
import ael

def contexts():
    contexts = ael.Context.select()
    context_vec = []
    for context in contexts: context_vec.append(context.name)
    context_vec.sort()
    return context_vec
    
ael_variables = [('context', 'Select_Context', 'string', contexts(), None, 1, 0)]

def ael_main(dict):
    CONTEXT = dict["context"]
    update_cliquet_definition()
    update_rainbow_definition(CONTEXT)


"""----------------------------------------------------------------------------
Update the cliquet option instrument definition.
----------------------------------------------------------------------------"""
def update_cliq_perf_add_info(i):
    # Updating the old AddInfo field, 'FCliquetPerformance'.
    new_value = ""
    add_info_entities = []
    ic = i.clone()
    for a in ic.additional_infos(): add_info_entities.append(a)

    for a in add_info_entities:
        if a.addinf_specnbr.field_name == 'FCliquetPerformance':
            if a.value == "Yes": new_value = 'Fwd Start Perf'
            else: new_value = 'Fwd Start'       
            a.delete()
            if i.add_info("FFwdStart") == "":
                ai = ael.AdditionalInfo.new(ic)
                ais  = ael.AdditionalInfoSpec['FFwdStart']
                ai.addinf_specnbr = ais.specnbr
                ai.value = new_value
                new_value = ""
            ic.commit()
            ael.poll()
    if new_value != "":
        for a in i.additional_infos():
            if a.addinf_specnbr.field_name == 'FFwdStart':
                ac = a.clone()
                ac.value = new_value
                ac.commit()


def update_cliquet_definition():
    v_list = ael.ChoiceList['ValGroup']
    valgroup_nbr = -1
    for member in v_list.members():
        if member.entry == "EqCliquet":
            valgroup_nbr = member
            break
    c_list = ael.ChoiceList['Category']
    category_nbr = -1
    for member in c_list.members():
        if member.entry == "Cliquet":
            category_nbr = member
            break
    cl_cliq_go = ael.ChoiceList.read('list="Category" and entry="CliquetGo"')
    if cl_cliq_go != None: 
        cliquet_gos = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_cliq_go.seqnbr))  
    else: cliquet_gos = []
    
    cl_cliq_end = ael.ChoiceList.read('list="Category" and entry="CliquetEnd"') 
    if cl_cliq_end != None:
        cliquet_ends = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_cliq_end.seqnbr))
    else: cliquet_ends = []
        
    for i in cliquet_gos:
        change = 0
        if i.product_chlnbr != None:
            if valgroup_nbr != -1 and \
               i.product_chlnbr.entry == "EqCliquetGo" :
                ic = i.clone()
                ic.product_chlnbr = valgroup_nbr
                if i.add_info('FCliquetType') == "":
                    ai = ael.AdditionalInfo.new(ic)
                    ais = ael.AdditionalInfoSpec['FCliquetType']
                    ai.addinf_specnbr = ais.specnbr
                    ai.value = 'Cliquet Go'
                ic.commit()
                change = 1
                ael.poll()
        if i.category_chlnbr != None:
            if category_nbr != -1 and i.category_chlnbr.entry == "CliquetGo":
                ic = i.clone()
                ic.category_chlnbr = category_nbr
                ic.commit()
                change = 1
                ael.poll()
        update_cliq_perf_add_info(i)
        if change: 
            print 'Updated the Cliquet Go option ', i.insid
            print '-----------------------------------------\n'
    for i in cliquet_ends:
        change = 0
        if i.product_chlnbr != None:
            if valgroup_nbr != -1 and i.product_chlnbr.entry == "EqCliquetEnd":
                ic = i.clone()
                ic.product_chlnbr = valgroup_nbr
                if i.add_info('FCliquetType') == "":
                    ai = ael.AdditionalInfo.new(ic)
                    ais = ael.AdditionalInfoSpec['FCliquetType']
                    ai.addinf_specnbr = ais.specnbr
                    ai.value = 'Cliquet End'
                ic.commit()
                change = 1
                ael.poll()
        if i.category_chlnbr != None:
            if category_nbr != -1 and \
               i.category_chlnbr.entry == "CliquetEnd":
                ic = i.clone()
                ic.category_chlnbr = category_nbr
                ic.commit()
                change = 1
                ael.poll()
        update_cliq_perf_add_info(i)
        if change: 
            print 'Updated the Cliquet End option ', i.insid
            print '-----------------------------------------\n'
    print "\nAll Cliquet Options are updated.\n"

"""----------------------------------------------------------------------------
Update the rainbow option instrument definition.
----------------------------------------------------------------------------"""
def update_rainbow_definition(context_name):
    v_list = ael.ChoiceList['ValGroup']
    valgroup_nbr = -1
    for member in v_list.members():
        if member.entry == "EqRainbow":
            valgroup_nbr = member
            break
    c_list = ael.ChoiceList['Category']
    category_nbr = -1
    for member in c_list.members():
        if member.entry == "Rainbow":
            category_nbr = member
            break
    
    cl_bot = ael.ChoiceList.read('list="Category" and entry="RainbowBOT"') 
    if cl_bot != None:
        rainbows_bot = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_bot.seqnbr))  
    else: rainbows_bot = []
    
    cl_wot = ael.ChoiceList.read('list="Category" and entry="RainbowWOT"') 
    if cl_wot != None:
        rainbows_wot = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_wot.seqnbr))
    else: rainbows_wot = []     
    
    cl_max = ael.ChoiceList.read('list="Category" and entry="RainbowMax"') 
    if cl_max != None:
        rainbows_max = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_max.seqnbr))
    else: rainbows_max = []     
    
    cl_min = ael.ChoiceList.read('list="Category" and entry="RainbowMin"') 
    if cl_min != None:
        rainbows_min = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_min.seqnbr))
    else: rainbows_min = []
    
    for i in rainbows_bot:
        change = 0
        if i.product_chlnbr != None:
            if valgroup_nbr != -1 and i.product_chlnbr.entry == "EqRainbowBOT" :
                ic = i.clone()
                ic.product_chlnbr = valgroup_nbr
                if i.add_info('FRainbowType') == "":
                    ai = ael.AdditionalInfo.new(ic)
                    ais = ael.AdditionalInfoSpec['FRainbowType']
                    ai.addinf_specnbr = ais.specnbr
                    ai.value = 'Best of Two'
                ic.commit()
                change = 1
                ael.poll()
        if i.category_chlnbr != None:
            if category_nbr != -1 and i.category_chlnbr.entry == "RainbowBOT":
                ic = i.clone()
                ic.category_chlnbr = category_nbr
                ic.commit()
                change = 1
        if change: 
            print 'Updated the Rainbow BOT option ', i.insid
            print '-----------------------------------------\n'
    for i in rainbows_wot:
        change = 0
        if i.product_chlnbr != None:      
            if valgroup_nbr != -1 and i.product_chlnbr.entry == "EqRainbowWOT":
                ic = i.clone()
                ic.product_chlnbr = valgroup_nbr
                if i.add_info('FRainbowType') == "":
                    ai = ael.AdditionalInfo.new(ic)
                    ais = ael.AdditionalInfoSpec['FRainbowType']
                    ai.addinf_specnbr = ais.specnbr
                    ai.value = 'Worst of Two'
                ic.commit()
                change = 1
                ael.poll()
        if i.category_chlnbr != None:
            if category_nbr != -1 and i.category_chlnbr.entry == "RainbowWOT":
                ic = i.clone()
                ic.category_chlnbr = category_nbr
                ic.commit()
                change = 1
        if change: 
            print 'Updated the Rainbow WOT option ', i.insid
            print '-----------------------------------------\n'
    for i in rainbows_max:
        change = 0
        if i.product_chlnbr != None:      
            if valgroup_nbr != -1 and i.product_chlnbr.entry == "EqRainbowMax":
                ic = i.clone()
                ic.product_chlnbr = valgroup_nbr
                if i.add_info('FRainbowType') == "":
                    ai = ael.AdditionalInfo.new(ic)
                    ais = ael.AdditionalInfoSpec['FRainbowType']
                    ai.addinf_specnbr = ais.specnbr
                    ai.value = 'Max of Two'
                ic.commit()
                ael.poll()
                change = 1
        if i.category_chlnbr != None:
            if category_nbr != -1 and i.category_chlnbr.entry == "RainbowMax":
                ic = i.clone()
                ic.category_chlnbr = category_nbr
                ic.commit()
                change = 1
        if change: 
            print 'Updated the Rainbow Max option ', i.insid
            print '-----------------------------------------\n'
    for i in rainbows_min:
        change = 0
        if i.product_chlnbr != None:      
            if valgroup_nbr != -1 and i.product_chlnbr.entry == "EqRainbowMin":
                ic = i.clone()
                ic.product_chlnbr = valgroup_nbr
                if i.add_info('FRainbowType') == "":
                    ai = ael.AdditionalInfo.new(ic)
                    ais = ael.AdditionalInfoSpec['FRainbowType']
                    ai.addinf_specnbr = ais.specnbr
                    ai.value = 'Min of Two'
                ic.commit()
                change = 1
                ael.poll()
        if i.category_chlnbr != None:
            if category_nbr != -1 and i.category_chlnbr.entry == "RainbowMin":
                ic = i.clone()
                ic.category_chlnbr = category_nbr
                ic.commit()
                change = 1
        if change: 
            print 'Updated the Rainbow Min option ', i.insid
            print '-----------------------------------------\n'
    ael.poll()
    context = ael.Context[context_name]
    v_list = ael.ChoiceList['ValGroup']
    valgroup_nbr = -1
    for member in v_list.members():
        if member.entry == "EqRainbow":
            valgroup_nbr = member
            break
    rainbow_found = 0
    context_clone = context.clone()
    clinks = context_clone.links()
    for cl in clinks:
        if cl.type == 'Correlation Matrix':
            if cl.group_chlnbr != None:
                if cl.group_chlnbr.entry == "EqRainbowWOT" or \
                   cl.group_chlnbr.entry == "EqRainbowBOT" or \
                   cl.group_chlnbr.entry == "EqRainbowMax" or \
                   cl.group_chlnbr.entry == "EqRainbowMin":
                    print "Removing Rainbow Context Link ", cl.name, " for Val Group ", cl.group_chlnbr.entry
                    rainbow_found = 1
                    rainbow_matrix = cl.name 
                    cl.delete()
    if rainbow_found:
        context_link = ael.ContextLink.new(context_clone)
        context_link.context_seqnbr = context
        context_link.type = 'Correlation Matrix'
        context_link.mapping_type = 'Val Group'
        context_link.name = rainbow_matrix
        context_link.group_chlnbr = valgroup_nbr
        context_link.commit()
        print "\nAdded the Context Link ", rainbow_matrix, " for Val Group ", valgroup_nbr.entry 
    context_clone.commit()
    print "\nAll Rainbow Options are updated.\n"






