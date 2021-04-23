import acm
# Callback hook that will be called from the Risk Factor Setup Applications 
# context menu (Custom Value) in the Risk Factors list
fa_alias = {"Zero Coupon":"Zero","Volatility":"Vol","Commodity":"Commodity","Par CDS Rate":"CDS","Stored Instrument Spread":"CS","Equity":"Equity","FX":"FX","Inflation Rate":"Inflation"}

def CustomValue(riskFactorInstance, addInfoSpec) :
    value = ""
    if str(addInfoSpec.Name()) == 'External Id' :
        value = riskFactorInstance.StringKey()         
        if 'MDT_AA_Format' in riskFactorInstance.RiskFactorCollection().RiskFactorSetup().RiskFactorPropertySpecifications().AsString():
      
            cords = riskFactorInstance.RiskFactorCoordinates()            

            if value.split(".")[0] == "Par CDS Rate":
                yc_currency = None
                for coordinate in cords:
                    coord_value = str(coordinate.CoordinateValue())  
                    riskFactorDim_ID = coordinate.RiskFactorDimensionUniqueId()
                    riskFactorDimension = acm.FRiskFactorDimension[riskFactorDim_ID]
                    '''
                    if riskFactorDimension.DisplayName() == 'Issuer':
                        partyId = acm.FParty[coord_value].Oid()
                        value = value.replace(value.split(".")[2],str(partyId)) 
                    '''
                    if riskFactorDimension.DisplayName() == 'Yield Curve':
                        yc_currency = acm.FYieldCurve[coord_value].Currency().Name() 
                if yc_currency:
                    value = value.replace(value.split(".")[1], yc_currency)

                    
            if value.split(".")[0] in ("Zero Coupon", "Inflation Rate", "Par CDS Rate"):
                last_element = value.split(".")[-1]
                minus_1 = value.split(".")[:-1]
                formatet_rest = ".".join(minus_1)
                value = formatet_rest + "|" + last_element 
                   
            if value.split(".")[0] == "Volatility":
                value_list = value.split(".")
                vol_surface_name = value_list[1]
                vol_surface_obj = acm.FVolatilityStructure[vol_surface_name]
                vol_type = vol_surface_obj.RiskType()          
                temp = []
                time = ''
                strike = ''
                underlying_maturity = ''
                for coordinate in cords:
                    coord_value = str(coordinate.CoordinateValue())
                    riskFactorDim_ID = coordinate.RiskFactorDimensionUniqueId()
                    riskFactorDimension = acm.FRiskFactorDimension[riskFactorDim_ID]
                    
                    if riskFactorDimension.DisplayName() == 'Time':
                        time = coord_value
                    
                    if riskFactorDimension.DisplayName() == 'Strike':  
                        strike = coord_value
                    
                    if riskFactorDimension.DisplayName() == 'Underlying Maturity':
                        underlying_maturity = coord_value               
                        
                    
                volname_surfacename = value_list[0] + "." + vol_surface_name

                if value.split(".")[0] == "Volatility" :  
                    extID_components = [volname_surfacename, strike, time]
                    if underlying_maturity: 
                        extID_components.append(underlying_maturity)
                    value = "|".join(extID_components)
 
            #Do it for all outside other loops
            value = value.replace(value.split(".")[0], fa_alias[value.split(".")[0]])
                    


    return value



