def csize(temp,base, *rest):
    if base == 'ZAR/WMAZ' or base =='ZAR/YMAZ':
        return 100
    elif base == 'ZAR/WEAT' or base =='ZAR/SUNS' or base =='ZAR/SUNF' :
        return 50
    else:
        return 25
