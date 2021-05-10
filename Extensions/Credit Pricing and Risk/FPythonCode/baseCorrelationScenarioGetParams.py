import acm
ael_variables = [
['vertical_shift', 'Vertical Shift (%)', 'double', None, None, 1, 0, '', None, True],
['tilt', 'Tilt (%)', 'double', None, None, 1, 0, '', None, True]
]

def ael_main_ex( parameters, dictExtra ):
    params = acm.FNamedParameters()
    name = str('')
    vertical = parameters['vertical_shift']
    tilt = parameters['tilt']
    if (vertical != 0.0):
        name = name + str(vertical) + '% vertical'
        if (tilt != 0.0):
            name = name + str(' & ') + str(tilt) + '% tilt'
    elif (tilt != 0.0):
        name = name + str(tilt) + '% tilt'
    params.Name(name)
    params.AddParameter( 'vertical_shift', parameters['vertical_shift'] )
    params.AddParameter( 'tilt', parameters['tilt'] )
    vec = acm.FArray()
    vec.Add( params )
    return vec
