import ael, BondIndex

BondIndex.update_bond_index_price(ael.Instrument['BondIndex/ZAR/ALBI'])
BondIndex.update_bond_index_price(ael.Instrument['BondIndex/ZAR/GOVI'])
BondIndex.rebase_instruments(ael.Instrument['ZAR/ALBI_TEST'])
BondIndex.rebase_instruments(ael.Instrument['ZAR/GOVI_TEST'])

