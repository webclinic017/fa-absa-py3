import acm

'''

Purpose: New column and ACM method that reflects the base exotic option type
Department : P C G - Price Testing
Desk : All
Requester : Nolan, Candiceanne: Absa Capital
Developer : Anil Parbhoo
CR Number : 476565
Book of Work / Jira Reference Number : ABITFA-337 
Previous CR Numbers relating to this deployment : n/a


'''






def GetExoticOptionBaseType(self):
    
    if self.InsType() == 'Option':
        if not self.IsExotic():
            if not self.Digital():
                return 'Vanilla'
        if self.IsBarrier():
            return 'Barrier'
        if self.IsAsian():
            return 'Asian'
        if self.Digital():
            return 'Digital'
        if self.IsLookback():
            return 'Look Back'
        if self.IsCliquet():
            return 'Cliquet'
        if self.ExoticType()=='Other':
            if self.Exotic().PowerExponent()!= 0.00 or self.Exotic().PowerGearing()!= 0.00:
                return 'Power'
        if self.ExoticType()=='Other':
                if self.Exotic().ChooserCallStrike() != 0.00 or self.Exotic().ChooserPutStrike() != 0.00:
                    return 'Chooser'
        if self.IsForwardStart():
            return 'Forward Start'
        if self.IsLadder():
            return 'Ladder'
        if self.IsQuantoOption(): 
            return 'Quanto'
        if self.IsRainbow(): 
            return 'Rainbow'
        if self.IsRangeAccrual(): 
            return 'Range Accrual'
        return 'Other'
    
    else:
        return 'None'    
            
        
        
