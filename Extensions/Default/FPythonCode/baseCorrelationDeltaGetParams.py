import acm
ael_variables = [

['detachments', 'Detachment Points (e.g. 3,6,9,...)', 'string', None, None, 1, 0, '', None, True]

]

def parse_string(str):
    ar = str.split(',')
    return ar

def ael_main_ex( parameters, dictExtra ):
    vec = acm.FArray()
    points = parse_string(parameters['detachments'])
    for point in points:
        params = acm.FNamedParameters()
        name = str(str(point) + '%')
        params.Name(name)
        params.AddParameter( 'detachment', point )
        vec.Add( params )
    
    return vec
