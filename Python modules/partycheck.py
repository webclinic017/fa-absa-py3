import ael
p = ael.Party['001 - ALL ALL PRIVATE INDIVIDUALS']
alias = p.aliases()
for i in alias:
    if i.type:
    	if (i.type.alias_type_name == 'Dart_Number'):
    	    print(i.alias)
	    print(dir(i.alias))
	    st = i.alias.rstrip()
	    print(st)
	    
