import acm

def durationInDays( duration, tradingHours):

    d = (duration // 1) 
    h = (duration % 1) * (24 / tradingHours)

    # (24 / tradingHours) is one full trading day    
    if h > 1.0:
        h = 1
   
    return d + h

