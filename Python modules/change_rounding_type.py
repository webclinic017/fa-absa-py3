import acm

def change_rounding_type(instruments, rounding_spec, type, attribute, decimals=None):
    rounding_spec_copy = acm.FRoundingSpec['%s_ETF_QuickFix' % rounding_spec.Name()]
    if not rounding_spec_copy:
        rounding_spec_copy = rounding_spec.Clone()
        rounding_spec_copy.Name('%s_ETF_QuickFix' % rounding_spec.Name())
        rounding_spec_copy.Commit()
        
        rounding_rules = acm.FRounding.Select('roundingSpec=%s' % rounding_spec.Oid())
        
        for rounding_rule in rounding_rules:
            rounding_rule_copy = rounding_rule.Clone()
            rounding_rule_copy.RoundingSpec(rounding_spec_copy)
            rounding_rule_copy.Commit()
    else:
        rounding_rules = acm.FRounding.Select('roundingSpec=%s' % rounding_spec_copy.Oid()).AsList()
        idx = 0
        while idx < rounding_rules.Size():
            obj = rounding_rules.At(idx)
            rounding_rules.AtPut(None, idx)
            obj.Delete()
            idx += 1
            
        rounding_rules = acm.FRounding.Select('roundingSpec=%s' % rounding_spec_copy.Oid())
        
        rounding_rules = acm.FRounding.Select('roundingSpec=%s' % rounding_spec.Oid())
        for rounding_rule in rounding_rules:
            rounding_rule_copy = acm.FRounding()
            rounding_rule_copy.Type(rounding_rule.Type())
            rounding_rule_copy.Attribute(rounding_rule.Attribute())
            rounding_rule_copy.Decimals(rounding_rule.Decimals())
            rounding_rule_copy.RoundingSpec(rounding_spec_copy)
            rounding_rule_copy.Commit()
    
        
    
    query_str = 'roundingSpec=%s attribute="%s"' % (rounding_spec_copy.Oid(), attribute)
    rounding = acm.FRounding.Select01(query_str, '')
    if rounding:
        rounding.Type(type)
        if decimals and isinstance(decimals, 'int'):
            rounding.Decimals(decimals)
        rounding.Commit()
    
    for instrument in instruments:
        instrument.RoundingSpecification(rounding_spec_copy)
        instrument.Commit()
            
ael_variables = [
    ['instrument', 'Instrument', 'FInstrument', None, '', 1, 1, 'Instruments to be updated.', None, 1],
    ['rounding_spec', 'Rounding Specification', 'FRoundingSpec', None, '', 1, 0, 'Rounding Specification to be cloned', None, 1],
    ['type', 'Type', 'string', None, '', 1, 0, 'Rounding Type', None, 1],
    ['attribute', 'Rounding Attribute', 'string', None, '', 1, 0, 'Rounding Specification to be updated', None, 1],
    ['decimals', 'Decimals', 'string', None, '', 0, 0, 'Rounding Specification to be updated', None, 1],
]

def ael_main(parameters):
    change_rounding_type(
        parameters['instrument'],
        parameters['rounding_spec'],
        parameters['type'],
        parameters['attribute'],
        parameters['decimals']
    )

