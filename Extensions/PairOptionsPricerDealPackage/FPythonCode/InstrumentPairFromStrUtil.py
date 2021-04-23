
import acm

import traceback

def GetInstrumentPair(instrument1, instrument2):
    if not instrument1 or not instrument2:
        return
    if hasattr(instrument1, 'Name'):
        instrument1 = instrument1.Name()
    if hasattr(instrument2, 'Name'):
        instrument2 = instrument2.Name()
    currs = [instrument1, instrument2]
    return acm.FInstrumentPair['/'.join(currs)] or acm.FInstrumentPair['/'.join(reversed(currs))]

def BaseCurrency():
    valParams = acm.UsedValuationParameters()
    return valParams.FxBaseCurrency() or valParams.AccountingCurrency() or acm.FCurrency['USD']

def FindMatchingCcy(instrName, set_currency = None, excluded = [], findMatchingCurrency = True):
    if instrName == 'ACC':
        return BaseCurrency()
    if findMatchingCurrency:
        instrument = acm.FCurrency[instrName]
    else:
        instrument = acm.FCommodityVariant[instrName]
    if instrument:
        return instrument
    else:
        if findMatchingCurrency:
            alphaMatch = acm.FCurrency.Select("name >'%s'" % (instrName)).SortByProperty("Name")
            if alphaMatch:
                for match in alphaMatch:
                    # Note, uggly with a loop rather than just taking first element,
                    # but "Cent > CH = True", but cent still come before
                    # CHF in the result list...
                    if match.Name()[:len(instrName)] == instrName and not (match.Name() in excluded):
                        if set_currency:
                            if not GetInstrumentPair(match, set_currency):
                                continue
                        return match
        else:
            pmPairs = acm.FPreciousMetalPair.Instances()
            pmSet = acm.FIdentitySet()
            pmSet.AddAll(pmPairs.Transform('CommodityVariant', acm.FArray, None))

            for pm in pmSet:
                if instrName.lower() == pm.Name().lower():
                    return pm

    if set_currency:
        raise Exception('No instrument pair involving %s matching %s' % (set_currency.Name(), instrName))
    else:
        raise Exception('No instrument matching %s' % (instrName))

def GetInstrumentPairFromInput(input, findMatchingCurrencyPair = True):
    instrName1 = None
    instrName2 = None
    instrPair = None
    instruments = input.split('/')
    if len(instruments) > 2:
        raise Exception('maximum one "/" allowed in an instrument pair')
    if len(instruments) == 2:
        instrName1 = instruments[0]
        instrName2 = instruments[1]
        instrument1 = None
        instrument2 = None
        if findMatchingCurrencyPair:
            if len(instrName1) > 3 or len(instrName2) > 3:
                raise Exception("%s represents too many letters to define a currency" % (instrName1 if len(instrName1) > 3 else instrName2))
            if len(instrName1) == 3:
                instrument1 = FindMatchingCcy(instrName1.upper(), findMatchingCurrency=findMatchingCurrencyPair)
        else:
            matchCurr = True if instrName1 and acm.FCurrency[instrName1] else False
            instrument1 = FindMatchingCcy(instrName1.upper() if matchCurr else instrName1, findMatchingCurrency = matchCurr)
            instrument2 = FindMatchingCcy(instrName2.upper() if not matchCurr else instrName2, findMatchingCurrency = not matchCurr)
        if len(instrName2) == 3:
            instrument2 = FindMatchingCcy(instrName2.upper())
        if instrument1 and instrument2:
            # Both instruments have been entered with 3 characters
            instrPair = GetInstrumentPair(instrument1, instrument2)
        elif instrument1 or instrument2:
            # One of the two instruments has been entered with 3 characters
            alreadyFoundCurr = instrument1 if instrument1 else instrument2
            otherCurr = FindMatchingCcy(instrName1.upper() if instrument2 else instrName2.upper(), alreadyFoundCurr, findMatchingCurrency=findMatchingCurrencyPair)
            instrPair = GetInstrumentPair(alreadyFoundCurr, otherCurr)
        else:
            # Both instruments have been entered with less than 3 characters
            match1 = FindMatchingCcy(instrName1.upper(), findMatchingCurrency=findMatchingCurrencyPair)
            no_match = []
            while match1:
                try:
                    match2 = FindMatchingCcy(instrName2.upper(), match1)
                    instrPair = GetInstrumentPair(match1, match2)
                    break
                except:
                    no_match.append(match1.Name())
                    try:
                        match1 = FindMatchingCcy(instrName1.upper(), excluded=no_match, findMatchingCurrency=findMatchingCurrencyPair)
                    except:
                        raise Exception('No instrument pair matching %s found' % input)
            instrPair = GetInstrumentPair(match1, match2)

    else:
        if findMatchingCurrencyPair:
            if len(instruments[0]) > 3 and len(instruments[0]) != 6:
                # 4, 5 or more than 6 characters
                raise Exception("invalid number of characters to define a instrument pair")
            elif len(instruments[0]) == 6:
                instrName1 = instruments[0][:3]
                instrName2 = instruments[0][3:]

                instrument1 = FindMatchingCcy(instrName1.upper(), findMatchingCurrency=findMatchingCurrencyPair)
                instrument2 = FindMatchingCcy(instrName2.upper())

            else:
                instrument1 = FindMatchingCcy('ACC')
                instrument2 = FindMatchingCcy(instruments[0].upper(), instrument1, findMatchingCurrency=findMatchingCurrencyPair)
        else:
            instrument1 = FindMatchingCcy('ACC')
            instrument2 = FindMatchingCcy(instruments[0], instrument1, findMatchingCurrency=False)

        instrPair = GetInstrumentPair(instrument1, instrument2)

    if not instrPair:
        raise Exception('Currency pair %s/%s does not exist' % (instrument1.Name(), instrument2.Name()))

    return instrPair
    
def GetCallPutFromInstrPairInput(instrPair, input):
    split_currs = input.upper().split('/')
    if len(split_currs) == 2:
        input1, input2 = split_currs
    elif len(split_currs) == 1 and len(input) == 6:
        input1, input2 = [split_currs[0][:3], split_currs[0][3:]]
    else:
        return None
    instrName1, instrName2  = instrPair.split('/')
    if input1 == instrName1[:len(input1)] and input1 != instrName2[:len(input1)]: 
        return False
    elif input1 == instrName2[:len(input1)] and input1 != instrName1[:len(input1)]:
        return True
        
def InstrumentPairFromStr(inputStr, defaultInstrumentPairName, isFxOption = True):
    try:
        instrumentPair = GetInstrumentPairFromInput(inputStr, isFxOption).Name()
    except Exception as e:
        print ("Failed to get instrument pair from '%s' -" % inputStr, e)
        instrumentPair = defaultInstrumentPairName
    return instrumentPair

def InstrumentFromStr(inputStr, isFxOption):
    instr = inputStr
    try:
        instr = FindMatchingCcy(inputStr.upper() if isFxOption else inputStr, findMatchingCurrency = isFxOption)
    except Exception as e:
        instr = None
    return instr.Name() if instr else None
    
def CallPutFromInstrumentPairFromStr(currPairName, newCurrPairName, inputStr):
    isPut = None
    try:
        if inputStr != currPairName:
            isPut = GetCallPutFromInstrPairInput(newCurrPairName, inputStr)
    except Exception as e:
        print ('Failed to get call put', e)
    return isPut
