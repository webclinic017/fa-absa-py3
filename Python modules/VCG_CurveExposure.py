'''
Purpose: Output to txt file the curves on a given trade for price testing, Updated to allow for multiple trade filters
Department: VCG
Requester: Candice Nolan,Mkhabele, Palesa, Khaya
Developer: Palesa Mkhabele/Anwar Banoo, Ickin Vural, Aaeda
CR Number: C433285, C453230,C000000489250,C000000496595, C701717
'''
import ael, acm, sets, csv

def write_file(name, data, access):
    f = file(name, access)
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close()

def TrdFilter():
    TrdFilter=[]
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    return TrdFilter

ael_variables = [('TrdFilter', 'Trade Filter', 'string', TrdFilter(), '', 1),
                 ('fname', 'File Name', 'string', None, 'Y:\Jhb\PCG Valuation Control\Curve Coverage.csv', 1)]   

 

def getCurves(ins, e1, tfname):
    try:
        l1 = ins.MappedDiscountLink().Link()
        name = str(l1.AsString().rsplit(',')[0]).lstrip("'").rstrip("'")
        yc = ael.YieldCurve[name]
        e1.add((tfname, yc.yield_curve_type, yc.curr.insid, name))
    except:
        pass

    try:
        l2 = ins.MappedForwardLink().Link()
        name = str(l2.AsString().rsplit(',')[0]).lstrip("'").rstrip("'")
        yc = ael.YieldCurve[name]
        e1.add((tfname, yc.yield_curve_type, yc.curr.insid, name))
    except:
        pass

    try:
        l3 = ins.MappedRepoLink().Link()
        name = str(l3.AsString().rsplit(',')[0]).lstrip("'").rstrip("'")
        yc = ael.YieldCurve[name]
        e1.add((tfname, yc.yield_curve_type, yc.curr.insid, name))
    except:
        pass
    return e1

    
def ael_main(dict):                    
    
    filename =    dict['fname'] 
    
    for tfname in dict['TrdFilter'].split(','): 
        tf = ael.TradeFilter[tfname] 
    
        insl = []
        insl_fx = []
        data = [['TRADE FILTER', 'CURVE TYPE', 'CURR', 'CURVE NAME']]
        e1 = sets.Set()
        for t in tf.trades():
            i   = t.insaddr
            if i.instype == 'Curr':
                cur = t.curr.insaddr
                curname = t.curr.insid

                if (i.insid, curname) not in insl_fx:
                    insl_fx.append((i.insid, curname))
                    ins = acm.FInstrument[i.insid]
                    e1 = getCurves(ins, e1, tfname)
                    ins = acm.FInstrument[curname]
                    e1 = getCurves(ins, e1, tfname)
                    
            elif i.insid not in insl:
                insl.append(i.insid)
                ins = acm.FInstrument[i.insid]
                e1 = getCurves(ins, e1, tfname)
                
                try:
                    legs = ins.Legs()
                except:
                    pass
                if legs:
                    for leg in legs:
                        e1 = getCurves(leg, e1, tfname)

                i = i.und_insaddr
                
                if i:
                    ins = acm.FInstrument[i.insid]
                    e1 = getCurves(ins, e1, tfname)
                    
               
                
        if len(e1) > 0:
            write_file(dict['fname'], data, 'a')
            write_file(dict['fname'], e1, 'ab')

            print 'SUCCESS'
    print 'Wrote secondary output to:::' + filename
