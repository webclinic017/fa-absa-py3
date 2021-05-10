import ael, BondIndex

ael_variables = [('user_input', 'User Input', 'string', ('Yes', 'No'), None),
                 ('bond_index', 'Bond Index', 'string', ('ZAR/ALBI_TEST', 'ZAR/GOVI_TEST'), None),
             	 ('input_file', 'Input Path', 'string', ('F:\\Albi Yields.csv', 'F:\\Govi Yields.csv'), None)]

def ael_main(ael_dict):
    bond_index = ael.Instrument[ael_dict["bond_index"]]
    BondIndex.calculation_report(bond_index, ael_dict["user_input"], ael_dict["input_file"])
    


