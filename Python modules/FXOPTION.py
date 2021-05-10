import ael

def fxOption(i,*rest):
    if i.instype == 'Option' and i.und_instype == 'Curr':
        return 'Yes'
    return 'No'

def fxOptionCurr(i,*rest):
    if i.und_instype == 'Curr':
        return 'Yes'
    return 'No'
