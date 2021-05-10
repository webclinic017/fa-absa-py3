import acm


def remove_confirmation_instruction_references():
    for confirmation_instruction in acm.FConfInstruction.Select("updateTime >= '2018-07-27'"):
        if confirmation_instruction.EventChlItem() is None:
            continue
        if confirmation_instruction.EventChlItem().Name() in ['Term Interest Statement']:
            confirmation_instruction.Delete()
    for rule in acm.FConfInstructionRule.Select("updateTime >= '2018-07-27'"):
        if rule.TemplateChoiceList().Name() in ['Term Interest Statement']:
            rule.Delete()


def remove_contact_rule_references():
    for contact_rule in acm.FContactRule.Select("updateTime >= '2018-07-27'"):
        if contact_rule.EventChlItem() is None:
            continue
        if contact_rule.EventChlItem().Name() in ['Term Interest Statement']:
            contact_rule.Delete()
        
    
def remove_additional_info_references():
    for party in acm.FParty.Select("updateTime >= '2018-07-27'"):
        party = party.StorageImage()
        party.AddInfoValue('Comm Freq Term', None)
        party.Commit()


remove_confirmation_instruction_references()       
remove_contact_rule_references()
remove_additional_info_references()
