
import ael

def get_fixing_source():
    smarkets = [x.ptyid for x in ael.Party.select("type = 'MtM Market'")]
    return smarkets
