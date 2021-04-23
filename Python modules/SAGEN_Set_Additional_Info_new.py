import ael


def getAddInfoEntity( e, ais ):
    """
    def getAdditionalInfo( settlement, ais ):
        returns the the additional info given an entity
        and the additional info spec
    """
    '''
    query = """
        Select
            ai.valnbr
        From 
            AdditionalInfo ai,
            AdditionalInfoSpec ais
        Where
            %i = ai.recaddr
        and ai.addinf_specnbr = %s
        and ais.rec_type = 'Settlement'    
    """ % ( settlement.seqnbr, ais.specnbr)
    ai_list = ael.asql(query,1)
    if len(ai_list[1]) > 1:
        #print ai_list
        return ai_list[1][0][0][0]
    else:
        return None
    '''
    try:
        return e.add_info(ais)
    except:
        return None



def setAddInfoEntity(entity, addInfoName, addInfoValue):
    """
    def setAddInfoEntity(entity, addInfoName, addInfoValue):
        Sets the Additional Info filed addInfoName to addInfoValue for an entity
    """

    ais = ael.AdditionalInfoSpec[addInfoName]
    if not ais:
        msg = "WARNING: The Additional Info Specification %s is not defined." % addInfoName
        print(msg)
        ael.log( msg )
        return
        
    the_ai = None
    # Does not work in Prime 3.2.x for Settlement table
    #for ai in entity.additional_infos():
    #    if ai.addinf_specnbr == ais:
    #        the_ai = ai
    #        break
    the_ai = getAddInfoEntity( entity, addInfoName )
    #the_ai = entity.add_info(addInfoName)
    if the_ai and the_ai.value != addInfoValue:
        try:
            clone = entity.clone()
            aic = the_ai.clone()
            aic.value = addInfoValue
            aic.commit()
            clone.commit()
            ael.poll()
            msg = "INFO: Changed the additional info %s to %s for entity %s" % (addInfoName, addInfoValue, entity)
            print(msg)
            ael.log(msg)
        except Exception, e:
            msg = "WARNING: Could not change the additional info %s to %s for entity %s" % (addInfoName, addInfoValue, entity)
            print(msg)
            ael.log(msg)
    elif not the_ai:
        try:
            clone = entity.clone()
            ai = ael.AdditionalInfo.new( clone )
            ai.addinf_specnbr = ais
            ai.value = addInfoValue
            ai.commit()
            clone.commit()
            msg = "INFO: Set the additional info %s to %s for entity %s" % (addInfoName, addInfoValue, entity)
            print(msg)
            ael.log(msg)
        except Exception, e:
            msg = "WARNING: Could not set the additional info %s to %s for entity %s" % (addInfoName, addInfoValue, entity)
            print(msg)
            ael.log(msg)
'''
def main(temp,sid,addInfoName,addInfoValue,*rest):
    sids = sid.split(';')
    for s in sids:
        if ael.Settlement[(int)(s)]:
            settlement = ael.Settlement[(int)(s)]
            setAddInfoEntity(settlement, addInfoName, addInfoValue)
            return 'Done'
        else:
            return 'Settle seqnbr invalid'
'''
