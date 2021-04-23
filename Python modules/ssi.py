import ael
ssi = ael.SettleInstruction.new()
ssi.counterparty_ptynbr = ael.Party['HardusTest']
ssi.curr = 2
ssi.money_cp_accnbr = ael.Account[562]
ssi.settleid = 'FXZAR3'
list = ['Premium', 'Dividend', 'Payment Premium', 'Assignment Fee', 'Broker Fee', 'Internal Fee',  \
    	'Extension Fee', 'Termination Fee', 'Payment Cash', 'Fixed Amount', 'Fixed Rate', 'Float Rate', \
	'Caplet', 'Floorlet', 'Digital Caplet', 'Digital Floorlet', 'Total Return', 'Credit Default', \
	'Call Fixed Rate', 'Call Float Rate', 'Redemption Amount', 'Zero Coupon Fixed', 'Return',	\
	'Exercise Cash', 'Security Nominal', 'Stand Alone Payment', 'Fee', 'End Cash', 'Initial Margin', \
	'Variation Margin', 'Premium 2']
for t in list:
    ssir = ael.SettleInstructionRule.new()
    ssir.type = (str)(t)
    ssir.settle_seqnbr = ssi	
    #print ssir.pp()

ssi.commit()

print ssi.pp()
