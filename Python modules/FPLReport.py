"""----------------------------------------------------------------------------
MODULE
        FPLReport- Common constants and utility classes used by PLPrimeRun.py
         
----------------------------------------------------------------------------"""

import ael, acm, time, sys, os, re, string


n_errors=0
###################################################
# Globals
###################################################

""" ---------  Interval Constants  ---------"""
YEAR="Year"
MONTH="Month"
WEEK="Week"
DAY="Day"
PERIOD="Period" 

"""---------  Report Type  ---------"""
PORTFOLIO="Portfolio"
POSITION="Position"
TRADE="Trade"

"""---------  Report File Type  ---------"""
RFT="Default"
RFT_TAB="Tab"  # Tab separated report for be used for exmaple import to excel.

"""--------- Banking date entity, used when adjusting to banking days -----"""
used_calendar=None
try:
    used_calendar=ael.Instrument['EUR']
except: pass # Will be set later

""" --------- defined_columns ---------
A ColumnHandler holding the set of columns that values can be calculated for.
Will be init after class definition of ColumnHandler.
"""
defined_columns=None

""" --------- ACM Extension Settings ---------"""
context='Standard'
# Calculation context. Could be overriden by [report]PLContext

""" --------- Settings ---------
Note: Possible names are reportAcmSettings keys with the prefix "report" 
removed
"""
settings={}                     # Will be initialized to default values in ()

""" -------- root --------
The root SheetDescr that holds a tree descripion of the different 
FCompoundPortfolio,FPortfolio or FTradeSelection and there children.
"""
root=None
""" -------- main_simulation_handler --------
SimulationDescr defined in the mainSimulation list will be simulated once!
"""
main_simulation_handler=[] # init in init_simulation()
""" ------- logged_calc_errors -------
A dictionary with found errors when calculating. Reported at the end."""
logged_calc_errors={}


""" ------- now_str -------
Need the today string """
now_str=None

""" ------- server -------"""
server=acm.getServerObject()


""" -------- use_diff_filtering --------
Special when report is used as test tool.
The special diff columns (faked acmExt called 'diff')
must be <> 0.0 for the values to be printed."""
use_diff_filtering=0

# ---------------------------------------------------------------------------
################################################
# Helper operations
####################################################

def sub(a,b):
    return a-b

def prc(a,b):
    return b/a

def zero(a,b=0.0):
    if abs(a-b) < 0.0000001:
        return 1
    return 0

# Transform FObject to Python Object if FObject is matrix, array or 'nil'
def asPyObject(obj):
    if (str(type(obj)) == "<type 'FVariantArray'>") \
    or (str(type(obj)) == "<type 'FArray'>"):
        resObj = []
        for i in range(obj.Size()):
            resObj.append(asPyObject(obj.At(i)))
        return resObj
        
    if (str(type(obj)) == "<type 'FUndefinedObject'>"):
        return None
    
    return obj
 
def exTostr():
    import traceback
    t,v,tb=sys.exc_info()
    return traceback.format_exception_only(t,v)[0][:-1]    
    

####################################################
# Helper Classes
####################################################
""" Class: PerioidGenerator """

class PeriodGenerator:
    """ Helper class for generating list of periods (start date,end date)
    For example by specifying a start date and then define a interval WEEK you
    can
    generate start and end date on weekly bases.
    All dates are banking days
    You can also switch by first using default values per period, for example
    year
    and then generate it weekly"""
    
    def __init__(self, settings):
        start_day       = settings.get('PLStartDate')
        self.eday       = settings.get('PLEndDate')  
        self.use_entity = settings['PLCalendar']
        self.interval   = settings['PLInterval']
        if not start_day:
            d=ael.date_today()
            if self.interval in (YEAR, MONTH, WEEK):
                first = 'd.first_day_of_' + self.interval.lower() + '()'
                self.sday = eval(first).add_banking_day(self.use_entity,-1)
            elif self.interval == DAY:
                self.sday=d.add_banking_day(self.use_entity,-1)
            elif self.interval == PERIOD:
                raise RuntimeError, "StartDate must be defined for interval"\
                                    " PERIOD"
            else:
                raise RuntimeError, "Invalid interval speicfication!"
        else:
            self.sday=start_day
            self.interval=PERIOD # Default if startdate is set.
        self.period_list=[(self.sday,self.eday)]
        self.day_list=[]

    def Generate(self,n=1,interval=None):
        """ Generates periods [(start date,end date),(start date,end date)..]
        using the interval specification.
        n indicates number of intervals and interval parameter let you switch
        how
        the dates are generated.
        n == 0 generates from start date until end date """
        if not interval: interval=self.interval
        tmp=[]  # Holding the interval 
        tmp2={} # Holding the days
        times=0
        d=self.sday
        if interval == PERIOD:
            self.period_list=[(self.sday,self.eday)]
            self.day_list=[self.sday,self.eday]
            return self
        else:
            tmp2[str(self.sday)]=self.sday
        while (n==0 or times < n) and d < self.eday:
            times=times+1
            if interval == YEAR:
                d2=d.add_years(1)
            elif interval == MONTH:
                d2=d.add_months(1)
            elif interval == WEEK:
                d2=d.add_weeks(1)
            elif interval == DAY:
                d2=d.add_days(1)
            else:
                raise RuntimeError, ("Invalid period %s to use when"\
                                     " generating" % str(interval))
            d2.adjust_to_banking_day(self.use_entity)
            if d2 > self.eday:
                d2=self.eday
            tmp.append((d,d2))
            tmp2[str(d2)]=d2
            d=d2
        self.period_list=tmp
        self.period_list.sort()
        self.day_list=tmp2.values()
        self.day_list.sort()
        return self

    def Periods(self):
        return self.period_list

    def Days(self):
        return self.day_list


        
""" Class: MonikerFactory """
class Moniker:
    """ Class for adding functionality using a moniker string """
    def __init__(self,mstr):
        self.moniker_string=mstr
        self.sim_ext={} # acm_ext:(unqiueVal,extObject)
        self.itr=None
        self.setItr(mstr)

    def setItr(self,s):
        try:
            self.itr = server.Get(s)
        except:
            detail="Failed to get [%s] from server:" % s
            raise RuntimeError,detail
        self.moniker_str=s

    def getItr(self): return self.itr
        
    def Calc(self,acm_ext,cxt):
        """ Calculates an ACM Extension. Also removes zero values """
        global n_errors
        v=server.GetCalculatedValue(self.itr, cxt, acm_ext)

        try:
            v = v.Value()
        except:
            v = 0.0
        try:
            if zero(v):
                return 0.0
        except:
            n_errors=n_errors+1
            detail="-bad value[%s], recived when calculating %s in context %s"\
                   % (str(v),acm_ext,context)
            raise RuntimeError,detail
        return v
        

""" Columns and Aggregate Calculation classes """
class ColumnDescr:
    """ Helper class for describing a column """
    global context
    args={}
    args['scale_factor']=(1.0,'sf')
    args['precision']=(3,'prec')
    args['diff_fn']=(sub,'fn')
    args['header']=(None,'header')
    args['is_agg_col']=(0,'is_agg_col')
    args['sim_descr']=(None,'sim_descr')
    args['context']=(context,'context')
    args['is_diff']=(0,'is_diff')
    
    def __init__(self,colname,acm_ext,**argv):
        self.n=colname
        self.acm=acm_ext
        for (k,(val,attr)) in ColumnDescr.args.items():
            if argv.get(k):
                val=argv.get(k)
            exec("self.%s=%s" % (attr,"val"))
        if not self.header:
            self.header=colname
        
    def Copy(self):
        """ Create a new Copy """
        c=ColumnDescr(self.Name(),self.AcmExt())
        for (k,(val,attr)) in ColumnDescr.args.items():
            if attr == 'fn': c.fn=self.fn
            else: exec('c.%s=self.%s' % (attr,attr))
        return c
        

    def Set(self,**argv):
         for (k,v) in argv.items():
            if not ColumnDescr.args.get(k): 
                raise 'Invalid parameter: %s' % k
            (val,attr)=ColumnDescr.args.get(k)
            self.SetGet(attr,v)
                
    def SetGet(self,attr,*args):
        if len(args[0]) > 0:
            b=args[0][0]
            exec("self.%s=%s" % (attr,"b"))
        else:
            a=eval("self.%s" % attr)
            return a
    def        Name(self, *args): return self.SetGet('n',         args)
    def      AcmExt(self, *args): return self.SetGet('acm',       args)
    def    IsAggCol(self, *args): return self.SetGet('is_agg_col',args)
    def ScaleFactor(self, *args): return self.SetGet('sf',        args)
    def   Precision(self, *args): return self.SetGet('prec',      args)
    def      DiffFn(self, *args): return self.SetGet('fn',        args)
    def      Header(self, *args): return self.SetGet('header',    args)
    def     Context(self, *args): return self.SetGet('context',   args)
    def    SimDescr(self, *args): return self.SetGet('sim_descr', args)
    def      IsDiff(self, *args): return self.SetGet('is_diff',   args)
    def PP(self):
        s=''
        s=s+"%s => %s\n" % ('self.n',self.n)
        s=s+"%s => %s\n" % ('self.acm',self.acm)
        for (k,(val,attr)) in ColumnDescr.args.items():
            exec("v=str(self.%s)" % attr)
            s=s+"self.%s => %s\n" % (attr,v)
        return s
            
class ColumnHandler:
    """ Helper class for handling the different columns.
    Note: The order of calls to Add defines the order """
    def __init__(self):
        self.columns=[]
        self.port_columns=[]
        self.lookup={} # Faster lookup using a dictionary
        
    def Add(self,cd):
        """ Adds a ColumnDescr """
        is_added=0
        if cd.IsAggCol(): # Make sure portfolio columns comes first
            for i in range(len(self.columns)):
                if not self.columns[i].IsAggCol():
                    self.columns.insert(i,cd)
                    is_added=1
                    break
        if not is_added: self.columns.append(cd)
        self.lookup={} # Rebuild lookup, 
                       # will make sure portfolio columns comes first
        for i in range(len(self.columns)): 
            self.lookup[self.columns[i].Name()]=i
        if cd.IsAggCol(): self.port_columns.append(cd)
        
    def Get(self,colname):
        return self.columns[self.lookup[colname]]
        
    def Columns(self): return self.columns

    def Exists(self,colname):
        if self.lookup.has_key(colname):
            return 1
        else:
            return 0
    def PortColumns(self): return self.port_columns
    
    def Len(self):
        """ Return the number of columns """
        return len(self.columns)
        
    def LenPort(self):
        """ Return the length of portfolio columns """
        return len(self.port_columns)
        


""" simulation Descr """
class SimulationDescr:
    """ Helper class for a simulation object """
    def __init__(self,name,acm_ext,value=None):
        self.name=name
        self.acm_ext=acm_ext
        self.value=value
        self.ext_obj=None
        
    def Convert(self,value):
        """ Converts values to correct type if needed """
        global now_str
        if self.AcmExt() == 'endDate' and type(value) == type(""):
            value=ael.date(value)
        if type(value) == ael.ael_date:
            if value == ael.date_today(): value=now_str
            else: value=str(value) + ' 23:59:59'
        if type(value) == ael.ael_entity:
            if value.record_type == 'Instrument': value=value.insid
            elif value.record_type == 'Portfolio': value=value.prfid
        return str(value)

    
    def Set(self,value): self.value=value
    def Get(self): return self.value
    def Name(self): return self.name
    def AcmExt(self): return self.acm_ext
   
    
    def Simulate(self,handler,context,value=None):
        if not value: value=self.value
        self.ext_obj=server.GetCalculatedValue(handler,context,self.acm_ext)
        old_value=self.ext_obj.Value() # ! make sure non-calculated values get
                                       # the right type
        value=self.Convert(value)
        if str(value) == str(old_value):
            self.ext_obj=None # To avoid remove simulation.
            return
        try: self.ext_obj.RemoveSimulation()
        except: pass
        
        self.ext_obj.Simulate(value,0)
        self.ext_obj.Value() # Force convert of types.
        
    def RemoveSimulation(self):
        if self.ext_obj:
            self.ext_obj.RemoveSimulation()
            self.ext_obj=None
        
        
class CalcDescr:
    def __init__(self,key,column_handler,moniker):
        self.moniker=moniker
        self.key=key
        self.columnHandler=column_handler
        self.values={}
        self.strValues={}
    def Diff(self,a,b):
        values=map(lambda x,y: x-y,a,b)
        return self.Format(values)
    
    def Format(self,values):
        tmp=[]
        for i in range(len(values)):
            if values[i] == None:
                tmp.append('')
            else:
                fmt="%%.%dlf" % self.columnHandler.Columns()[i].Precision()
                tmp.append(fmt % values[i])
        return tmp
        #return map(str,values) # fix later, use formater perhaps
    def Key(self): return self.key
    def MaxLen(self):
        max_len=[0]*self.columnHandler.Len()
        for (k,v) in self.StrValues().items():
            tmp=map(len,v)
            max_len=map(max,max_len,tmp)
        return max_len
    def Moniker(self): return self.moniker
    def Values(self,key=None,values=None):
        if key:
            key=str(key)
            if values:
                self.values[key]=values
                self.strValues[key]=self.Format(values)
            else:
                return self.values[key]
        else:
            return self.values
    def StrValues(self,key=None):
        if key: return self.strValues[key]
        else: return self.strValues
    def Sort(self):
        """ Sorts the string values and returns them """
        tmp=[]
        keys=self.values.keys()
        keys.sort()
        for k in keys: tmp.append((k,self.strValues[k]))
        return tmp
    def Calc(self,main_simulation_handler,pg):
        global logged_calc_errors
        for d in pg.Days():
            values=[]         
            for cd in self.columnHandler.Columns():
                if cd.IsDiff():
                    values.append(values[-1]-values[-2]) #special for testing
                    continue
                for sd in main_simulation_handler:
                    if sd.AcmExt() == 'endDate':
                        if d != ael.date_today():
                            sd.Simulate(self.Moniker().getItr(), cd.context,d)
                    else:
                        sd.Simulate(self.Moniker().getItr(),cd.Context())
                    
                    if cd.SimDescr():
                        cd.SimDescr().Simulate(self.Moniker().getItr(),
                                               cd.Context())
                v=None
                try:
                    v=self.Moniker().Calc(cd.AcmExt(), cd.context)
                except RuntimeError,detail:
                    key=str(self.Key())+cd.AcmExt()
                    if not logged_calc_errors.has_key(key):
                        logged_calc_errors[key]="%s: %s" % (self.Key(),detail)
                        v=None
                values.append(v)
                if cd.SimDescr(): cd.SimDescr().RemoveSimulation()
                for sd in main_simulation_handler: sd.RemoveSimulation()
            self.Values(d,values)
                 
class SheetDescr:
    def __init__(self,key,column_descr,moniker=None,cname=None):
        self.key=key
        self.cname=cname
        self.columnDescr=column_descr
        self.children=[]
        self.lookup={}
        if moniker:
            self.calcDescr=CalcDescr(key,column_descr,moniker)
        else:
            self.calcDescr=None

    def Add(self,key,moniker,cname):
        """ Adds a child but adds no values """
        sd=SheetDescr(key,self.columnDescr,moniker,cname)
        self.children.append(sd)
        self.lookup[key]=sd
        return sd

    def Calc(self,main_simulation_handler,perioid_generator):
        """ Note: showCurr should have been simulated per context
        before call (optimization)"""      
        if not self.IsRoot():
            self.calcDescr.Calc(main_simulation_handler,perioid_generator)
        for c in self.children:
            c.Calc(main_simulation_handler,perioid_generator)
    def Category(self):
        return self.cname
    def Children(self):
        return self.children

    def Get(self,key=None):
        if key: return self.lookup[k]
        else: return self.children
    
    def IsRoot(self):
        if self.calcDescr:
            return 0
        else:
            return 1

    def Key(self): return self.key
    
    def MaxLen(self):
        """ Returns max needed string len"""        
        if self.IsRoot():
            max_len=[]
            for cd in self.columnDescr.Columns():
                max_len.append(len(cd.Header()))
        else:
            max_len=self.calcDescr.MaxLen()
        for c in self.children:
            max_len=map(max,max_len,c.MaxLen())
        return max_len
        
    def StrValues(self,key=None):
        return self.calcDescr.StrValues(key)
    def Diff(self,a,b):
        return self.calcDescr.Diff(a,b)
    def Values(self,key=None,values=None):
        return self.calcDescr.Values(key,values)
    

    def PP(self,level=0):
        if not self.IsRoot():
            print self.calcDescr.Sort()
        else:
            print ""
        for c in self.children:
            c.PP(level+1)

    def Sort(self):
        self.children.sort(lambda x,y: cmp(x.Key(),y.Key()))
        for c in self.children: c.Sort()
    


# -----------------------------------------------------------------------------
# Report helper classes
# -----------------------------------------------------------------------------
class PrintPLReport:
    """ Base Class for the different reports """
    def __init__(self,columnHandler,sheetDescr,settings,
                 periodGenerator):
        global use_diff_filtering
        self.filename=settings['PLFileName']
        self.columnHandler=columnHandler
        self.settings=settings
        self.periodGenerator=periodGenerator # Should be generated before call
        self.showMask=[1,1,1]
        self.PLReportType=settings.get('PLReportType',PORTFOLIO)
        self.sheetDescr=sheetDescr
        self.columnHeaders=[]
        self.portColumnHeaders=[]
        for cd in self.columnHandler.Columns():
            self.columnHeaders.append(cd.Header())
        for cd in self.columnHandler.PortColumns():
            self.portColumnHeaders.append(cd.Header())
        self.aggKeys=list(range(len(self.periodGenerator.Periods())))
        self.diff_idx=[]
        if use_diff_filtering:
            for i in range(self.columnHandler.Len()):
                if self.ColumnHandler().Columns()[i].IsDiff():
                    self.diff_idx.append(i)
        

    def InitReport(self):
        """ Inits, open file, calc format etc, creates attributes """
        try:
            self.fp=open(self.filename,'w')
            print "Opened file: %s" % self.filename
        except:
            msg="Failed to open file: %s! Aborts." % self.filename
            print msg
            raise RuntimeError,msg
        #
        # Format string help
        #
        max_len=self.sheetDescr.MaxLen()
        self.value_fmt=[]
        self.header_fmt=[]
        self.max_line_len=reduce(lambda x,y:x+y,max_len)+\
                                (2*self.columnHandler.Len()) # + tab
        for i in range(self.columnHandler.Len()):
            self.value_fmt.append("%%+%ds" % (max_len[i]+1))
            self.header_fmt.append("%%+%ds" % (max_len[i]+1))
        self.n_blank=20
        self.name_fmt="%%-%ds" % self.n_blank
        self.period_fmt="%%%ds:" % self.n_blank
        #
        # showMap
        #
        if self.settings.get("PLShowStartDate",'Yes') == 'No': 
            self.showMask[0]=0
        if self.settings.get("PLShowEndDate",'Yes') == 'No': 
            self.showMask[1]=0
        if self.settings.get("PLShowPeriod",'Yes') == 'No': 
            self.showMask[2]=0
        #
        # Other stuff
        #
        self.df=self.settings['PLDateFormat']
        self.portIdx=0
                        
                        
    def ExcludePeriod(self,element,s,e):
        if not self.diff_idx:
            return 0
        has_no_diff=1
        for i in self.diff_idx:
            if element.Values(s)[i] in [None,0.0] \
            or element.Values(e)[i] in [None,0.0]:
                has_no_diff=0
                break
        print "ExcludePeriod", has_no_diff
        return has_no_diff
        
    def PrintPLEnd(self):
        global logged_calc_errors
        if logged_calc_errors:
            keys=logged_calc_errors.keys()
            keys.sort()
            self.fp.write(("\n%s\nThe Following errors/warnings was found:\n"\
                           % (self.max_line_len*'-')))
            for k in keys:
                self.fp.write(str(logged_calc_errors[k])+'\n')
        self.fp.close()
        print "Done!"

    def PrintLine(self,format,values,n_blanks=0,tab='  '):
        fmt=format
        if n_blanks > 0: self.fp.write(n_blanks*' ')
        for i in range(len(values)):
            if type(format) == type([]): # Improve later for performance
                fmt=format[i]
            self.fp.write((fmt % values[i]))
            if i < len(values)-1:
                self.fp.write(tab)
            else:
                self.fp.write('\n')
    
    def PrintReport(self):
        self.InitReport()
        #self.PrintPLHeader()
        self.PrintPLBody()
        self.PrintPLEnd()
        
        
        
    def PrintPLBody(self):
        """ Default for printing """
        for child in self.sheetDescr.Children():
            if child.Category() == 'CompoundPortfolio':
                self.PrintPLHeader(child.Key(),child.Category())
                if self.PLReportType == PORTFOLIO:
                    self.PrintPortHeader(child,self.n_blank+3)
                comp=child
                for child in comp.Children():
                    #self.PrintPLHeader(child.Key(),child.Category())
                    if self.PLReportType in [TRADE,POSITION]:
                        self.PrintPLPosition(child)
                    else:
                        self.PrintPLPort(child)
                self.PrintPLCompAgg(comp)
            else:
                #self.PrintPLHeader(child.Key(),child.Category())
                if self.PLReportType in [TRADE,POSITION]:
                    self.PrintPLPosition(child)
                else:
                    self.PrintPLHeader(child.Key(),child.Category())
                    self.PrintPortHeader(child,self.n_blank+3)
                    self.PrintPLPort(child)
                    
    def PrintPLPort(self,element):
        self.fp.write((self.name_fmt % element.Key())+'\n')
        for i in self.aggKeys:
            (s,e)=self.periodGenerator.Periods()[i]
            s=str(s)
            e=str(e)
            self.PrintPLPeriodValues(element,s,e,None)
            self.PrintPeriodSeparator()
        #self.PrintElementSeparator(element.Key())

        
    def PrintPLPeriodValues(self,element,s,e,parent):
        s_val=element.StrValues(s)
        e_val=element.StrValues(e)
        if not parent:
            name1=element.Key()
            name2=''
        else:
            name1=parent.Key()
            name2=element.Key()
        if self.showMask[0]:
            self.PrintScaledDateLine(s,s_val,self.period_fmt,2,name1,name2)
        if self.showMask[1]:
            self.PrintScaledDateLine(e,e_val,self.period_fmt,2,name1,name2)
        if self.showMask[2]:
            self.PrintScaledPeriodLine(element.Diff(element.Values(s),element.Values(e)),
                                       self.period_fmt,2,name1,name2,s,e)

        
    def PrintPLPosition(self,pos):
        self.PrintPLHeader(pos.Key(),pos.Category())
        self.PrintPortHeader(pos,self.n_blank+3)
        for ins in pos.Children():
            is_printed=0
            for idx in self.aggKeys:
                (s,e)=self.periodGenerator.Periods()[idx]
                s=str(s)
                e=str(e)
                if self.ExcludePeriod(ins,s,e): continue
                if not is_printed:
                    self.PrintElementHeader(ins.Key())
                    is_printed=1
                self.PrintPLPeriodValues(ins,s,e,pos)
                if self.PLReportType == TRADE:
                    for t in ins.Children():
                        for (k,v) in t.calcDescr.Sort():
                            self.PrintScaledTimeLine(t.Key(),v,self.period_fmt,
                                                     2,pos.Key(),ins.Key())
                self.PrintPeriodSeparator()
            self.PrintElementSeparator(ins.Key())
        self.PrintPLPortAgg(pos)
            
            

    def PrintPLAggHeader(self,total_str,prfid):
        self.fp.write(("%s\n\n" % (self.max_line_len*'-')))
        self.fp.write(self.name_fmt % total_str)
        self.PrintLine(self.header_fmt,self.portColumnHeaders,3)
        self.fp.write("\n")
        self.fp.write((self.name_fmt % prfid)+'\n')

    def PrintPLAgg(self,element,total_str):
        """PrintPLAgg(element) """
        self.PrintPLAggHeader(total_str,element.Key())
        for i in self.aggKeys:
            (s,e)=self.periodGenerator.Periods()[i]
            s=str(s)
            e=str(e)
            self.PrintPLPeriodValues(element,s,e,None)
            self.PrintPeriodSeparator()


    #
    # Operations that should or may be implemented by subclasses
    # Note: Operations below are listed in call order in PrintPLBody except 
    # PrintPLHeader()
    def PrintPLHeader(self,prfid,category): pass
    def PrintPortHeader(self,prfid,n_blank): pass
    def PrintElementHeader(self,name): pass
    def PrintScaledDateLine(self,d,val,fmt,n_blank,*args): 
        pass # Args are start and enddate as strings
    def PrintScaledPeriodLine(self,val,fmt,n_blank): pass
    def PrintPeriodSeparator(self): pass
    def PrintElementSeparator(self,name): pass
    def PrintPLPortAgg(self,port): pass
    def PrintPLCompAgg(self,child): pass    

class PrintPLReportDefault(PrintPLReport):
    """ Generates the default report """
    report_header_fmt="""
******************************************************************************
  PRIME PROFIT/LOSS REPORT                                                %s
  Report type  : %-s
  Portfolio    : %-20s              (%s)       
  Period       : %s to %s
  Scale factor : %s
  Valuation    : Default (change later)

  All values are (as default) shown in %s 
  Expired positions are %s
******************************************************************************
"""

    def __init__(self,columnHandler,sheetDescr,settings,
                 periodGenerator):
        PrintPLReport.__init__(self,columnHandler,sheetDescr,
                               settings,periodGenerator)

    def PrintPLHeader(self,prfid,category):
        """ Should be called after InitReport() """
        f=('%s %%H:%%M:%%S'% self.df)
        now=time.strftime(f,time.localtime(time.time()))
        sd=self.periodGenerator.sday.to_string(self.df)
        ed=self.periodGenerator.eday.to_string(self.df)
        if self.settings.get('PLIncludeExpired','Yes') == 'No':inc='excluded'
        else:inc='included'
        c=category
        show_curr=self.settings.get('PLShowCurr','Portfolio')
        if type(show_curr) == ael.ael_entity:
            show_curr="currency %s" % show_curr.insid
        else:
            show_curr="portfolio currency"
        header=PrintPLReportDefault.report_header_fmt % (now,
                                                 self.settings['PLReportType'],
                                                 prfid,c,sd,ed,'1000.0',
                                                 show_curr,inc)
        # Perhaps split using string
        self.fp.write(header+'\n')
        
    def PrintScaledDateLine(self,d,val,fmt,n_blank,*args):
        self.fp.write(fmt % ael.date(d).to_string(self.df))
        self.PrintLine(self.value_fmt,val,n_blank)
    def PrintScaledTimeLine(self,time_str,val,fmt,n_blank,*args):
        time_str=ael.date(time_str[:10]).to_string(self.df) + time_str[10:]
        self.fp.write(fmt % time_str)
        self.PrintLine(self.value_fmt,val,n_blank)
    
        
    def PrintScaledPeriodLine(self,val,fmt,n_blank,*args):
        self.fp.write(fmt % "Period")
        self.PrintLine(self.value_fmt,val,n_blank)
        
    def PrintPLPortAgg(self,child):
        if self.settings['PLReportType'] == POSITION: 
            self.PrintPLAgg(child,"Portfolio Total")

    def PrintPLCompAgg(self,child):
        self.PrintPLAgg(child,"Compound Total")

    def PrintPortHeader(self,prfid,n_blank):
        self.PrintLine(self.header_fmt,self.columnHeaders,n_blank)

    def PrintElementHeader(self,name): 
        self.fp.write((self.name_fmt % name)+'\n')
    def PrintElementSeparator(self,name): self.fp.write('\n')
    def PrintPeriodSeparator(self): self.fp.write('\n')



class PrintPLReportTab(PrintPLReport):
    """ Generates the tab separated report """
    
    def __init__(self,columnHandler,sheetDescr,settings,
                 periodGenerator):
        PrintPLReport.__init__(self,columnHandler,sheetDescr,settings,
                               periodGenerator)

    def PrintScaledDateLine(self,d,val,fmt,n_blank,*args):
        self.fp.write("%s\t%s\tDate\t%s\t" % (args[0],args[1],
                                              ael.date(d).to_string(self.df)))
        self.PrintLine(self.value_fmt,val,0,"\t") 
        # PrintLine adds newline at end
    def PrintScaledTimeLine(self,time_str,val,fmt,n_blank,*args):
        time_str=ael.date(time_str[:10]).to_string(self.df) + time_str[10:]
        self.fp.write("%s\t%s\tTradeTime\t%s\t" % (args[0],args[1],time_str))
        self.PrintLine(self.value_fmt,val,0,"\t") 
        # PrintLine adds newline at end

    def PrintScaledPeriodLine(self,val,fmt,n_blank,*args):
        self.fp.write(("%s\t%s\tPeriod\t%s-%s\t"  % (args[0],args[1],args[2],
                                                     args[3])))
        self.PrintLine(self.value_fmt,val,0,"\t")

    def PrintPLAggHeader(self,total_str,key): pass 
        
    
# ---------------------------------------------------------------------
# Local Operations
# ---------------------------------------------------------------------
    
    
def create_column_handler(column_names):
    global defined_columns
    columns=ColumnHandler()
    for cn in column_names:
        try:
            pc=defined_columns.Get(cn)
            columns.Add(pc.Copy())
        except:
            print "Invalid column name %s. Could not be found in possible"\
                  " columns. Ignores it." % cn
    return columns

def init_column_handler_from(workbook):
    print 70*'-'
    ch=ColumnHandler()
    s=''
    print "Init:", workbook
    for t in ael.TextObject.select('type=Workbook'):
        if t.name == workbook:
            m=re.search('(@@pobj\s+FPortfolioSheet\s+oid=\d+)',t.get_text(),
                        re.M)
            s=m.group(1)
    if not s:
        raise RuntimeError,workbook
    ps=server.Get(s)
    parts=ps.Contents()
    columns=parts.At('columns')
    column_defs={}
    column_names=[]
    try:
        for i in columns.split('@@column ')[1:]:
            column_names.append(i.split('|')[2])
    except AttributeError:
        for i in range(columns.Size()):
            n=str(columns.At(i))
            n=n[1:-1]
            column_names.append(n)
        
    tmp=server.GetAllStandardExtensions('FColumnDefinition','FTradingSheet',
                                        1,1,
                                        'sheet columns',
                                        'portfoliosheet')

    tmp2=server.GetAllStandardExtensions(
                            'FNumFormatter',
                            'FObject',
                            1,1,'','')
    for i in range(tmp.Size()):
        if str(tmp.At(i).StringKey()) in column_names:
            if tmp.At(i).At('ExtensionAttribute'):
                # pick num decimals
                dec=0
                format=tmp.At(i).At('Format')
                for f in range(tmp2.Size()):
                    if str(tmp2.At(f).StringKey()) == str(format):
                        dec=tmp2.At(f).NumDecimals()
                        break
                column_defs[tmp.At(i)] = dec
    for k in column_defs.keys(): 
        labels = string.split(str(k.At('LabelList')),';')
        ch.Add(ColumnDescr(str(k), str(k.At('ExtensionAttribute')),
                           header = labels[0], precision = column_defs[k]))
    print "Initialized %d columns from workbook %s" % (len(column_defs),
                                                       workbook)
    return ch


def init_sheet_descr_aux(child,phys,PLReportType,inc_exp):
    if PLReportType == TRADE:
        trades={}
        for t in range(phys.Trades().Size()):
            key=phys.Trades().At(t).Instrument().Oid()
            tmp=trades.get(key,[])
            tmp.append(phys.Trades().At(t))
            trades[key]=tmp
    if PLReportType in [TRADE,POSITION]:
        ins=phys.Instruments().AsArray()
        for k in range(ins.Size()):
            i=ins.At(k)
            ii=ael.Instrument[ins.At(k).Oid()]
            if inc_exp or ii.exp_day and ii.exp_day >= ael.date_today():
                s = '@@sitr @@pobj %s oid = %d\xa4@@pobj %s oid = %d' \
                    % (phys.ClassName(),phys.Oid(),i.ClassName(),i.Oid())
                cc=child.Add(i.Name(),Moniker(s),'Instrument')
                if PLReportType == TRADE:
                        for t in trades.get(i.Oid(),[]):
                                cc.Add(t.TradeTime(),
                                       Moniker(t.MonikerString()),'Trade')  
    

def init_sheet_descr(obj,ch,PLReportType=PORTFOLIO,inc_exp=1):
    root=SheetDescr('root',ch)
    if str(obj.Portfolio().ClassName()) == 'FCompoundPortfolio':
        comp=root.Add(obj.Portfolio().Name(),
                      Moniker(obj.MonikerString()),
                      str(obj.Portfolio().Category()))
        children=obj.Portfolio().SubPortfolios()
        for j in range(children.Size()):
            phys=children.At(j)
            child=comp.Add(phys.Name(),
                           Moniker("@@pitr "+phys.MonikerString()),
                           str(phys.Category()))
            init_sheet_descr_aux(child,phys,PLReportType,inc_exp)
    elif str(obj.Portfolio().ClassName()) == 'FPhysicalPortfolio':
        child=root.Add(obj.Portfolio().Name(),
                       Moniker("@@pitr "+obj.MonikerString()),
                       str(obj.Portfolio().Category()))
        init_sheet_descr_aux(child,obj.Portfolio(),PLReportType,inc_exp)
    elif str(obj.Portfolio().ClassName()) == 'FTradeSelection':
        child=root.Add(obj.Portfolio().Name(),
                       Moniker(obj.MonikerString()),
                       str(obj.Portfolio().Category()))
        init_sheet_descr_aux(child,obj.Portfolio(),PLReportType,inc_exp)
    else:
        raise 'Unsupported obj type = %s' % obj.Portfolio().ClassName()
    return root

def init_acm_settings(settings):
    """ get acm settings and set settings.
    NOTE: Perhaps change from were we take settings !!! """
    global reportACMSettings, context
    for k in reportACMSettings.keys():
        try:
            value=asPyObject(server.GetCalculatedValue(0,context, k).Value())
            if value:
                settings[k[6:]]=value
                print "Got setting %s(%s) from context %s" % (k,str(value),
                                                                   context)
        except: pass
    return settings


def init_simulation():
    global main_simulation_handler
    main_simulation_handler.append(SimulationDescr('EndDate','endDate'))

def eval_settings(name_str = '', **settings):
    """ Operation that evaluates and take care of some settings.
    Objects could be assigned!
    Should be called after init_settings and init_acm_settings """
    # filename
    s=settings["PLFileName"]
    (path,filename)=os.path.split(s)
    if path[0] in ['"',"'"]: path=path[1:]
    path=os.path.normpath(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print "Created directory:", path
        except:
            detail="-error [%s], failed to create directory: %s" % (exTostr(),
                                                                    path)
            raise RuntimeError, detail
    filename=''
    m=re.search("(.*)(%N)(.*)",s,re.I)
    if m:
        is_ok=0
        n_str=''
        for i in range(100):
            try:
                filename=eval(m.group(1)+n_str+m.group(3))
                filename=os.path.normpath(filename)
            except:
                detail="Error [%s] when evaluating filename.Please correct"\
                       " syntax" % exTostr()
                print "-error, %s" % detail
                raise RuntimeError,detail
            if os.path.exists(filename):
                n_str="_"+str(i+1)
            else:
                is_ok=1
                break
        if not is_ok:
            detail="-error, more than 100 files exists, please delete some to"\
                   " be able to continue!"
            print detail
            raise RuntimeError,detail
    else:
        filename=eval(s)
    settings['PLFileName']=os.path.normpath(filename)
    #calendar
    s=settings['PLCalendar']
    if s == 'Accounting':
        settings['PLCalendar']=ael.Instrument[ael.used_acc_curr()]
    elif s.index(':'):
        [table,id]=s.split(':')
        settings['PLCalendar']=eval("ael.%s['%s']" % (table,id))
    else:
        detail="-error, envalid specification of [report]PLCalendar!. Please"\
               " correct it"
        raise RuntimeError, detail

    # Dates
    for s in ['PLStartDate','PLEndDate']:
        v=settings.get(s)
        if not v: continue
        try:
            if v == 'TODAY':
                settings[s]=ael.date_today()
            elif s[0] == '-':
                n=int(s)
                settings[s]=ael.date_today().add_banking_days(n,
                                                        settings['PLCalendar'])
            else:
                settings[s]=ael.date(v)
        except:
            detail="-error, invalid format [%s] in setting [report]%s. Please"\
                   " correct it." % (v,s)
            raise RuntimeError, detail

    # showCurr
    s=settings['PLShowCurr']
    if s == 'Accounting':
        settings['PLShowCurr']=ael.Instrument[ael.used_acc_curr()]
    elif s and not s in ['Portfolio']:
        settings['PLShowCurr']=ael.Instrument[s]
    return settings

        
        
        
# -----------------------------------------------------------------------
# Main entry
# -----------------------------------------------------------------------

""" acm settings and other default definitions """
""" --------- reportACMSettings ---------
A dictionary of settings that can be defined by ACM Extensions affecting
how report should be generated.
Default values will be set in init() (must be called after connect).
Note: string values are case sensitive.
      reportPLFileName will be evaluated i.e could be a python expresion e.g.
    default is "'c:/temp/PlPrime_'+top.prfid+'_'+ael.date_today()+'%N.txt'" 
   were
    %N is a special tag making sure filename get a unique number 
i.e. "" or "_1" or "_2"...
"""

reportACMSettings={
    'reportPLReportType' : None, # The string i.e Position or Portfolio
    'reportPLReportFileType' : None, 
    # The string Default or Tab. Undefined means Default.
    'reportPLInterval' : None,   # The string Week, Month, Year, Day or Period.
    'reportPLShowStartDate' : None, 
    # string 'Yes' or 'No', everything except 'No' means 'Yes'
    'reportPLShowPeriod' : None,    # string 'Yes' or 'No', dito
    'reportPLShowEndDate' : None,   # string 'Yes' or 'No', dito
    'reportPLPeriodInterval' : None, 
    # Should report be genrated weekly,montly etc from start-enddate.
    'reportPLStartDate' : None, 
    # If defined, reportPLInterval is PERIOID. Format 2002-05-27, -N (TODAY-N)
    'reportPLEndDate' : None,   
    # If defined,  reportPLInterval is PERIOID, format as StartDate + TODAY
    'reportPLCalendar' : None,   # Calendar or Instrument of type Curr. 
                            # Format: ['Accounting'|Curr:INSID|Calendar:Calid],
    'reportPLIncludeExpired' : None,
    'reportPLDateFormat'     : None,
    'reportPLColumns' : None, #  [col1 col2 col3 ....]
    'reportPLFileName' : None, # string, filename with path included
    'reportPLContext' : None,
    'reportPLShowCurr': None, # Accounting,[Portfolio] or any curr
    'reportPLContext': None, # Accounting,[Portfolio] or any curr
    'reportPLWorkbookTemplate': None, # Accounting,[Portfolio] or any curr
    
    }


defined_columns=ColumnHandler()
defined_columns.Add(ColumnDescr('RPL','rPL',is_agg_col=1))
defined_columns.Add(ColumnDescr('UPL','uPL',is_agg_col=1))
defined_columns.Add(ColumnDescr('TPL','tPL',is_agg_col=1))
defined_columns.Add(ColumnDescr('MaUPL','maUPL',is_agg_col=1))
defined_columns.Add(ColumnDescr('MaTPL','maTPL',is_agg_col=1))
defined_columns.Add(ColumnDescr('Cash','cash',is_agg_col=1))
defined_columns.Add(ColumnDescr('ActualCash','actualCash',is_agg_col=1))
defined_columns.Add(ColumnDescr('MarketValue','marketVal',is_agg_col=1))
defined_columns.Add(ColumnDescr('Fees','fees',is_agg_col=1))
defined_columns.Add(ColumnDescr('Div','accDividends',is_agg_col=1))

defined_columns.Add(ColumnDescr('nRPL','rPL',is_agg_col=1,context='Standard'))
defined_columns.Add(ColumnDescr('nUPL','uPL',is_agg_col=1,context='Standard'))
defined_columns.Add(ColumnDescr('nTPL','tPL',is_agg_col=1,context='Standard'))
defined_columns.Add(ColumnDescr('nMaUPL','maUPL',is_agg_col=1,
                                context='Standard'))
defined_columns.Add(ColumnDescr('nMaTPL','maTPL',is_agg_col=1,
                                context='Standard'))
defined_columns.Add(ColumnDescr('nCash','cash',is_agg_col=1,
                                context='Standard'))
defined_columns.Add(ColumnDescr('nActualCash','actualCash',is_agg_col=1,
                                context='Standard'))
defined_columns.Add(ColumnDescr('nMarketValue','marketVal',is_agg_col=1,
                                context='Standard'))
defined_columns.Add(ColumnDescr('nFees','fees',is_agg_col=1,
                                context='Standard'))
defined_columns.Add(ColumnDescr('nDiv','accDividends',is_agg_col=1,
                                context='Standard'))

defined_columns.Add(ColumnDescr('dRPL','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dUPL','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dTPL','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dMaUPL','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dMaTPL','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dCash','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dActualCash','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dMarketValue','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dFees','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('dDiv','diff',is_agg_col=1))
defined_columns.Add(ColumnDescr('Premium','premium',is_agg_col=1))
defined_columns.Add(ColumnDescr('Position','portPLPositionDisplay'))
defined_columns.Add(ColumnDescr('Avg','avgPrice'))
defined_columns.Add(ColumnDescr('Mean','meanPrice'))
defined_columns.Add(ColumnDescr('PUsedPr','priceInPortCurr'))
#defined_columns.Add(ColumnDescr('RPL-NewPL','rPL',is_agg_col=1,
#context='Standard'))
defined_columns.Add(ColumnDescr('Diff-Rpl','diff',is_agg_col=1))
#defined_columns.Add(ColumnDescr('Diff-Test','diff',is_agg_col=1))

""" --------- Main Entry ----------- """
def run_report(fobject, **settings):
    """ Global execute and init operation. Must be called after connect.
    top is an ael.Portfolio (compound or phys) and children is a possible
    list of physical portfolios. 
    Also adds some own objects to the settings structure """
    global used_calendar,root,context,now_str
    settings['PLDateFormat'] = eval(settings['PLDateFormat'])
    # Set now_str
    now_str=str(server.Get('@@ dt now'))
    print "Starting PLReport for %s %s with now as %s" \
    % (fobject.Portfolio().Category(),fobject.Portfolio().Name(),now_str)
    context=settings.get('PLContext')
    settings = init_acm_settings(settings)
    settings = apply(eval_settings, (fobject.Portfolio().Name(),), settings)
    if settings.has_key('PLWorkbookTemplate'):
        try:
            ch=init_column_handler_from(settings['PLWorkbookTemplate'])
        except RuntimeError,message:
            msg="Please define a PortfolioSheet with name: %s. This execution is aborted!" % message
            raise RuntimeError,msg     
    else:
        ch=create_column_handler(settings['PLColumns'])
    pg = PeriodGenerator(settings)
    if settings.has_key('PLPeriodInterval'):
        pg.Generate(0,settings['PLPeriodInterval'])
    else:
        pg.Generate(1)
    rt=settings['PLReportType']
    print "ReportType=%s" % rt
    inc_exp=1
    if settings.get('PLIncludeExpired','Yes') == 'No': inc_exp=0

    init_simulation()
    #
    # Where the work is done
    #
    root=init_sheet_descr(fobject,ch,rt,inc_exp)
    root.Sort()
    root.Calc(main_simulation_handler,pg)
    if settings.get('PLReportFileType',RFT) == RFT:
        report=PrintPLReportDefault(ch,root,settings,pg)
    else:
        report=PrintPLReportTab(ch,root,settings,pg)   
    report.PrintReport()

    #
    # And we are done.
    #
    return 
   
#Test
"""
s1="@@pitr @@pobj FCompoundPortfolio oid=686"
s2="@@pitr @@pobj FPhysicalPortfolio oid=474"
s3="@@pitr @@pobj FTradeSelection oid=1001215"
inc_exp=1

for s in [s1,s2,s3]:
    global root
    o=server.Get(s)
    init_settings()
    pg=PeriodGenerator(settings['PLInterval'],
                       settings.get('PLStartDate'),
                       settings.get('PLEndDate'))
    pg.Generate(1)
    print "Testing", o.Portfolio().Name()
    eval_settings(o.Portfolio())
    ch=create_column_handler(settings['PLColumns'])
    root=None
    PLReportType=settings['PLReportType']
    init_sheet_descr(o,ch,PLReportType)
    root.Sort()
    root.Calc(main_simulation_handler,pg)
    report=PrintPLReportDefault(ch,root,settings,pg,s1)
    report.PrintReport()

    report=PrintPLReportTab(ch,root,settings,pg,s1)

    #report=PrintPLReportDefault(repor,ch,root,settings,pg,s1)
    report.PrintReport()
    break

"""





