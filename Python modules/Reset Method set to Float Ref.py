import acm


ael_variables = []

def ael_main(dict):
    all_vps = acm.FValuationParameters.Select('')
    for vp in all_vps:
        print('before', vp.Name(), vp.ResetGenerateMethod())
        vp.ResetGenerateMethod('Float Ref')
        vp.Commit()
        print('after', vp.Name(), vp.ResetGenerateMethod())
        
        
        
        
        

    
        
