import ael, acm

import at_logging
LOGGER = at_logging.getLogger()

def setAddInfoEntity(entity, AddInfoName, AddInfoValue):
    aisp = ael.AdditionalInfoSpec[AddInfoName]
    if aisp:
        aiList = ael.AdditionalInfo.select('addinf_specnbr = %i' % aisp.specnbr)
        recaddrList = []
        for ai in aiList:
            recaddrList.append(ai.recaddr)
        if recaddrList.__contains__(entity.seqnbr):
            LOGGER.info('Amend')
            # Amend
            if entity.add_info(AddInfoName) != AddInfoValue:
                entity_clone = entity.clone()
                ais = entity_clone.additional_infos()
                for ai in ais:
                    if ai.addinf_specnbr.specnbr == aisp.specnbr:
                        ai.value = AddInfoValue
                try:
                    entity_clone.commit()
                    LOGGER.info("%s %s :Additional info %s updated to %s",
                                entity.record_type, entity.seqnbr, AddInfoName, AddInfoValue)
                except Exception:
                    LOGGER.exception('ERROR: %s %s :Additional info %s was not updated to %s.',
                                     entity.record_type, entity.seqnbr, AddInfoName, AddInfoValue)
            else:
                LOGGER.info("%s %s :Additional info %s was already set to %s",
                            entity.record_type, entity.seqnbr, AddInfoName, AddInfoValue)
        else:
            # New
            entity_clone = entity.clone()
            ai = ael.AdditionalInfo.new(entity_clone)
            ai.addinf_specnbr = aisp
            ai.value = AddInfoValue
            try:
                entity_clone.commit()
                LOGGER.info("%s %s :Additional info %s created with value %s",
                            entity.record_type, entity.seqnbr, AddInfoName, AddInfoValue)
            except Exception:
                LOGGER.exception('ERROR: %s %s :Additional info %s was not created with value %s.',
                                 entity.record_type, entity.seqnbr, AddInfoName, AddInfoValue)
    else:
        LOGGER.error("ERROR: Additional Info Spec %s does not exist.", AddInfoName)
        
        
# Generic function to add and amend Additional Info fields on any entity through ACM
def set_AdditionalInfoValue_ACM(entity, addInfoName, value):
    LOGGER.info("%s %s", addInfoName, value)
    if entity.AdditionalInfo().GetProperty(addInfoName) == None:
        addInfo = acm.FAdditionalInfo()
        addInfo.Recaddr(entity.Oid())
        addInfo.AddInf(acm.FAdditionalInfoSpec[addInfoName])
        addInfo.FieldValue(value)
        try:
            addInfo.Commit()
        except Exception:
            LOGGER.exception('Commit failed')
    else:
        addInfo = acm.FAdditionalInfo.Select('recaddr = %i' % entity.Oid())
        for i in addInfo:
            if i.AddInf().Name() == addInfoName:
                i.FieldValue(value)
                try:
                    i.Commit()
                except Exception:
                    LOGGER.exception('Commit failed.')
                break

def main(temp, sid, addInfoName, addInfoValue, *rest):
    sids = sid.split(';')
    for s in sids:
        if ael.Settlement[(int)(s)]:
            # settlement = ael.Settlement[(int)(s)]
            settlement = acm.FSettlement[(int)(s)]
            # setAddInfoEntity(settlement, addInfoName, addInfoValue)
            set_AdditionalInfoValue_ACM(settlement, addInfoName, addInfoValue)
            return 'Done'
        else:
            return 'Settle seqnbr invalid'
