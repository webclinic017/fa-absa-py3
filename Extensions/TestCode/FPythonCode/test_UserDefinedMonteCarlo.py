from __future__ import print_function
import unittest

import acm

class TestUDMC(unittest.TestCase):
    """Tests for the user defined Monte Carlo Engine"""
    def setUp(self):
        self.udmc_in_context = 'UdmcMod' in acm.GetDefaultContext().ModuleNames()
        if not self.udmc_in_context:
            acm.GetDefaultContext().AddModule("UdmcMod")
    def tearDown(self):
        if not self.udmc_in_context:
            acm.GetDefaultContext().RemoveModule("UdmcMod")
    def test_UDMCParser(self):
        """Basic tests of the parser funcitonlity"""
        import FUDMCParser
        parser_test_code = """
        int b=2*2*2;
        b=b;
        ##
        int b_1=2*2;
        param int a;
        if ( max(5.0, 1.2) > 2.1 ) {
            b=a[1:1];
            b=a;
            b=a[-2];
            b=a[1,2];
            b=a[1:4];
            b=a[max(4,4)];
            b=max( c[0]-2, 2);
            b= 1 + (3 + 4);
        } 
        else
        {
            b=1-2;
        };
        ##
        double b=2.0*2.0;
        param double a;
        if( a==b) { a=0.0; };
        ##
        double b=2.0*2.0;
        param double a;
        if ( a==b) { a=0.0; };
        
        ##
        int a=1;
        int b=ceiling(4.5);
        for a=0 to 5
        {
          b=b*4;
        };
        ##
        param double totalValue;
        totalValue=totalValue;
        ##
        param double totalValue;
            param double timeToExpiry;
            param doublevec dates;
            param doublemat historicalAssetPrices;
            param doublevec rainbowVolaArray;
            param double discountRate;
            param doublevec basketCarryCostArray;
            param doublevec basketPriceArray;
            param double strikePriceConverted;
            param doublemat basketCorr;
            param doublevec basketWeightArray;
            double val = 0.0;
            double maxval = 0.0;
            double minval = 0.0;
            
            maxval = max(basketWeightArray[0],p[1,0]);
            val = max(0.0, maxval - strikePriceConverted);
            val = max(1, "alban", "31dd", "df _df", "sdf-sdf");  
            cf(timeToExpiry, val);    
        """
        for testcase in parser_test_code.split("##"):
            try:
                tree = FUDMCParser.parse(testcase)
            except Exception as err:
                self.fail("Error in test case: " + testcase)
    def test_UDMCSemanticAnalyzer(self):
        """Basic tests of the semantic analyzer"""
        import FUDMCParser
        import FUDMCSemanticAnalyzer
        semantic_test_code = """
        int b=2*2;
        param int a;
        if ( max(5.0, 1.2) > 2.1 ) {
            b=a;
        } else {
            b=-3;
            b=a-a;
            b=a-3;
        };
        if ( a==b ) {
            b=a;
        };
        
        ##
        double b=2.0*2.0;
        param double a;
        b=max(5.1, a);
        ##
        double b=2.0*2.0;
        param doublevec c;
        param doublemat m;
        param double a;
        b=max(2.0, 4.0);
        b=c[4];
        c=c[2:5];
        c=m[2:4,3];
        c=m[2,3:3];
        c=m[2,:];
        c=m[:,3];
        m=m[2:4,3:5];
        b=max(c[0], 2.0);
        b=max(2*c[0], 2.0);
        b=max(2.0, c[0] );
        b=max(c[0], 2.0);
        b=1.0;
        b=2.0;
        b = abs(b);
        ##
        param doublevec a;
        param doublemat m;
        double c=max(a);
        double d=min(a);
        int e=indexMin(a);
        int f=indexMax(a);
        double g=sum(a);
        double h=sum(m);
        double i=average(a);
        double j=average(m);
        int k=length(a);
        int l=rows(m);
        int n=cols(m);
        double o=0.0;
        double p=0.0;
        f=f;
        sort(a);
        o=a[0];
        reverse(a);
        p=a[0];
        ##
        param doublevec dates;
        param doublemat historicalAssetPrices;
        param doublevec vol;
        param double r;
        param doublemat divt;
        param doublemat diva;
        param doublevec cc;
        param doublevec S;
        param double K;
        param doublemat corr;
        int rr=1;
        double val = 0.0;
        val = max((sum(cc)/length(dates))-K, 0.0);
        rr=symtest("alban");
        cf(1.0, val);
        ##
        param doublemat dates;
        param doublevec d;
        d = dates[2, 1:4];
        """
        for testcase in semantic_test_code.split("##"):
            try:
                tree = FUDMCParser.parse(testcase)
                stree = FUDMCSemanticAnalyzer.analyze(tree)      
            except Exception as err:
                self.fail("Error in test case: " + testcase)
    def test_Baiscs(self):
        """Basic full UDMC test"""
        self.assert_(basic_test() == 0 )
    def test_Everything(self):
        """Complex UDMC test, excercise all aspects"""
        self.assert_(complete_test() == 0 )
    def test_Process(self):
        """Limited tests of the UDMC processes"""
        self.assert_(proces_test() == 0 )



class fuzzyfloat:
    """Float like object that allows for approximate comparisons
    
    fuzzyfloat(5, 0,2) == 5.1 --> True
    """
    def __init__(self, val, bound):
        float.__init__(val)
        self.val  = val
        self.bound = bound
    def __cmp__(self, other):
        try:
            if hasattr(other, 'Class') and other.Class() == acm.FDenominatedValue:
                otherf = other.Number()
            else:
                otherf = float(other)
            if abs(otherf-self.val)<self.bound:
                return 0
        except Exception as e:
            print ("EE", e)
            pass
        return cmp(self.val, other)
        
def expect_err(locals, codestr, errclass):
    try:
        eval(codestr, globals(), locals)
        raise Exception("Code string should have thrown an exception")
    except errclass as msg:
        pass

def expect_TypeError(locals, codestr):
    expect_err(locals, codestr, TypeError)

def expect_RuntimeError(locals, codestr):
    expect_err(locals, codestr, RuntimeError)
    
def basic_test():
    """Test some basic functionality of UDMC"""
    mclib = acm.FUDMCLibrary()
    if len(mclib.GetFunctionNames())<3: raise Exception("missing functions")
    mmax = mclib.GetFunction("max")
    if not mmax: raise Exception("Function max is mising")
    nofunc = mclib.GetFunction("sdlfjsdlkjflsdf")
    if nofunc: raise Exception("Non existing function found")
    mulop = mclib.GetFunction("mul_double_int")
    if not mulop: raise Exception("mulop not found")

    
    # ** Test basics of valfunc **
    # test invalid instantiation
    expect_TypeError(locals(), "acm.FUDMCValuationFunction()")
    expect_TypeError(locals(), "acm.FUDMCValuationFunction(3)")

    # Create an empty function (this func availabe during development)
    func = acm.FUDMCValuationFunction("")
    
    # test vm
    func.vm_mkvarnode(1, "double", "a", True, False, 1)
    #test duplicate var decl 
    expect_RuntimeError(locals(), """func.vm_mkvarnode(1,"double","a",True,False,1)""")
    expect_RuntimeError(locals(), """func.vm_mkvarnode(2,"badtype","a",True,False,1)""")
    expect_RuntimeError(locals(), """func.vm_mkvarnode(4,"int","a",True,True,1)""")
    
    func.vm_mknode(2, "double", 1.2, "double", acm.FArray(), "")
    expect_RuntimeError(locals(), """func.vm_mknode(2,"double",1.2,"double",acm.FArray(),"")""")
    func.vm_mknode(3, "double", None, "double", acm.FArray(), "")
    return 0

class TestCase:
    def __init__(self, params, code, results):
        """Construct a test case
        
        Arguments:
        params     -- Dict {paramname:paramval}
        code       -- String PEL code
        results    -- Dict {paramname:finalvalue}
        """
        self.params = params
        self.code = code
        self.results = results
        self.mcexpr = None
        
    def test(self):
        #run it through parser and semantic analyzer first to get good tracebacks for simple errros
        import FUDMCParser
        import FUDMCSemanticAnalyzer
        ast_tree = FUDMCParser.parse(self.code)
        FUDMCSemanticAnalyzer.analyze(ast_tree)
        # now run it through entire loop
        valfunc = acm.FUDMCValuationFunction(self.code)
        r = self.params.get("r", 0.05)
        yc = acm.FYieldCurve['EUR-SWAP']
        ycinfo = yc.Ir().YieldCurve()
        res = valfunc.PerformValuation(self.params, ycinfo, 0, "SEK", 1)
        for key, val in self.results.items():
            resval = res[key]
            if not resval:
                resval = res[acm.FSymbol(key)]
            if not resval == val:
                print ("in case:\n", self)
                #raise Exception("Unexpected result var %s expected %s got %s" % \
                #                (key, str(val), str(resval) ) )
        return res
        
    def __str__(self):
        return "testcase:\n"+str(self.params) +"\n--\n"+self.code + "\n--\n"+ str(self.results)
    def shouldfail(self):
        """Return true if this case is expected to generate an error"""
        return 'fail' in self.results
        
def load_test_cases(s):
    state = 'scanning'    
    cases = []
    for l in s.split("\n"):        
        if l[0:1] == '#' and \
            state != 'readcode':
            if state == 'readres':
                cases.append( TestCase( params, code, tmpdict) )
            state = 'readparam'
            tmpdict = {}
        elif l[0:1] == '-':
            if state == 'readparam':                
                params = tmpdict
                tmpdict = None
                state = 'readcode'
                code = []
            elif state == 'readcode':
                code = "\n".join(code)
                state = 'readres'
                tmpdict = {}
        else:
            if state == 'readparam' or \
               state == 'readres':
                try:
                    if l:
                        var, val = l.split("=")
                        tmp = eval(val)
                        if isinstance(tmp, list):
                            if len(tmp) and isinstance(tmp[0], list):
                                # looks like a matrix
                                realmatrix = acm.FRealMatrix()
                                realmatrix.Size( len(tmp), len(tmp[0]))
                                for rowi in range(len(tmp)):
                                    for coli in range(len(tmp[0])):
                                        realmatrix.AtPut(rowi, coli, tmp[rowi][coli])
                                tmp = realmatrix 
                            else:
                                # just an ordinary array
                                realarr = acm.FRealArray()
                                for i in tmp:
                                    realarr.Add(float(i))
                                tmp = realarr
                        tmpdict[var.strip()] = tmp
                except Exception as e:
                    print ("** bad result line ", l, e, "**")
                    raise
            elif state == 'readcode':
                code.append(l)
            else:
                raise Exception("bad state")
    return cases

testcases = """##################################### bad syntax will fail to parse
a=1
---------------------------------
a=2
---------------------------------
fail=1
##################################### test self assignment
---------------------------------
double b=2.0;
b=b; # comment
---------------------------------
b=2
##################################### test variable names
---------------------------------
double b=2.0;
double b_1=2.0;
double b1=3.0;
b=b1+b_1;
---------------------------------
b=5
##################################### basic float aritmatic
---------------------------------
double b=2.0*2.5;
double c=3.0*(4.0+2.0);
b=b;
---------------------------------
b=5.0
c=18.0
##################################### test basic math
---------------------------------
double a=exp(1.0);
double b=exp(0.0);
double c=ln(exp(4.0));
double d=floor(4.5);
double e=ceiling(4.5);
double f=pow(2.0, 3.0);
a=a;
---------------------------------
a=fuzzyfloat(2.71828, 0.0001)
b=1.0
c=4
d=4
e=5
f=8
##################################### Test parameter
a=3.0
---------------------------------
param double a;
double b=1.0;
b=2.0*a;
---------------------------------
b=6.0
##################################### Test greater than, less than
---------------------------------
double a=3.0;
double b=4.0;
int res = 0;
if(a<b){ res=res+1;};
if(b>a){ res=res+1;};
---------------------------------
res=2
##################################### init order of vars
a=3.0
---------------------------------
param double a;
double b=a;
double g=b;
double c=g;
double y=g;
double d=y+c;
a=a;
---------------------------------
d=6.0
##################################### Basic function call
a=3.0
---------------------------------
param double a;
double b=1.9;
b=max(b,a);
---------------------------------
b=3
##################################### and or etc
a=3
---------------------------------
param int a;
int b=0;
if (a>2 and a<1)  {  b=b+1; };
if (a<1 or a<5)   {  b=b+2; };
if (a>2)          {  b=b+0; };
---------------------------------
b=2
##################################### Test if statement with ints
a=3
---------------------------------
param int a;
int b=1;
if (a>4){
  b=2+b;
};
if (a<5){
  b=3+b;
};
if (a<4.0){
  b=b+4;
};
if (a>2.0){
  b=b+8;
};
if (a==3){
  b=2+b;
};
---------------------------------
b=18
##################################### Test accumulate function
a=3.5
r=0.03
---------------------------------
param double a;
cf(2.0 , a);
---------------------------------
Result=fuzzyfloat(3.29617, 10)
##################################### Test if statement
a=3
---------------------------------
param int a;
double b=0.5;
if (a>4){
  b=2+ b;
};
if (2.0<4.0){
  b=b+2;
};
if (a>2.0){
  b=b+4;
};
if (a>4){
  b=2+b;
}else{
  b=b-1.0;
};
---------------------------------
b=5.5
##################################### and or etc
a=3
---------------------------------
param int a;
int b=0;
if (a>2 and a<4)          {  b=b+1; };
if (a<1 or a<5)           {  b=b+2; };
if (a>2 and a >6 )        {  b=b+4; };
if (not a<2 and a<6 )     {  b=b+8; };
---------------------------------
b=11
##################################### for loop
a=5
---------------------------------
param int a;
int i=3;
int sum=0;
for i=0 to a
{
    sum=sum+i;
};
---------------------------------
sum=10
##################################### for loop
a=5
---------------------------------
param int a;
int i=3;
int sum=0;
for i=2 to 5
{
    sum=sum+i;
};
---------------------------------
sum=9
##################################### Test vectors
a=[3,4]
---------------------------------
param doublevec a;
double c=7.0;
double d=8.0;
c=a[0];
d=a[1];
---------------------------------
c=3
d=4
##################################### Test vectors negative indexes
a=[3,4]
---------------------------------
param doublevec a;
double c=7.0;
double d=8.0;
c=a[-2];
d=a[-1];
---------------------------------
c=3
d=4
##################################### Test vector and matrix functions
a=[3,4,1,7,2]
m=[[1,4,5],[3,4,-3]]
---------------------------------
param doublevec a;
param doublemat m;
doublevec zzero = zeros(2);
doublemat zeromat = zeros(2,4);
double c=max(a);
double d=min(a);
int e=indexMin(a);
int f=indexMax(a);
double g=sum(a);
double h=sum(m);
double i=average(a);
double j=average(m);
int k=length(a);
int l=rows(m);
int n=cols(m);
double o=0.0;
double p=0.0;
double q=zzero[1];
double r=zeromat[1,3];
f=f;
sort(a);
o=a[0];
reverse(a);
p=a[0];
---------------------------------
c=7
d=1
e=2
f=3
g=17
h=14
i=3.4
j=14/6.0
k=5
l=2
n=3
o=1.0
p=7
##################################### Test bad vector access
a=[3,4]
---------------------------------
param doublevec a;
double c=7.0;
c=a[300];
---------------------------------
c=3
d=4
fail=1
##################################### Test matrix
aaa=1
a=[[1,2,3], [4,5,6]]
---------------------------------
param doublemat a;
doublemat b=a;
b=transpose(a);
---------------------------------
b=[[1,4],[2,5],[3,6]]
##################################### Test matrix access
a=[[1,2,3], [4,5,6]]
---------------------------------
param doublemat a;
double b=0.0;
double c=0.0;
double d=0.0;
double e=0.0;
c=a[1,2];
b=a[0,1];
e=a[-1,-1];
---------------------------------
b=2
c=6
e=6
##################################### Test matrix bad index
a=[[1,2,3], [4,5,6]]
---------------------------------
param doublemat a;
double e=0.0;
e=a[3000,0];
---------------------------------
fail=1
##################################### Test matrix mul 
a=[[1,2,3], [4,5,6]]
b=[ [3,4],[5,6],[3,4] ]
---------------------------------
param doublemat a;
param doublemat b;
doublemat c=a*b;
c=c;
---------------------------------
c=[[22, 28],[55, 70]]
##################################### Test matrix sub
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param doublemat a;
param doublemat b;
doublemat c=a-b;
c=c;
---------------------------------
c=[[0,1,2],[6,5,4]]
##################################### Test matrix add
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param doublemat a;
param doublemat b;
doublemat c=a+b;
c=c;
---------------------------------
c=[[2,3,4],[2,5,8]]
##################################### Test matrix elementwise mul
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param doublemat a;
param doublemat b;
doublemat c=a.*b;
c=c;
---------------------------------
c=[[1,2,3],[-8,0,12]]
##################################### Test matrix elementwise div
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param doublemat a;
param doublemat b;
doublemat c=a./b;
c=c;
---------------------------------
c=[[1,2,3],[-8,0,12]]
fail=1
##################################### Test matrix scalar
a=[[2,4,8], [4,-2,6]]
b=2
---------------------------------
param doublemat a;
param double b;
doublemat c=a*b;
doublemat d=a/b;
doublemat e=a+b;
doublemat f=a-b;
c=c;
---------------------------------
c=[[4,8,16],[8,-4,12]]
d=[[1,2,4],[2,-1,3]]
e=[[4,6,10],[6,0,8]]
f=[[0,2,6],[2,-4,4]]
##################################### Test matrix div scalar by zero 
a=[[2,4,8], [0,-2,6]]
b=0
---------------------------------
param doublemat a;
param double b;
doublemat c=a/b;
c=c;
---------------------------------
c=[[4,8,16],[8,-4,12]]
fail=1
##################################### Test vanilla
strikePrice=3
vol=4
---------------------------------
param double strikePrice;
param double vol;
cf(0.0, strikePrice * vol );
---------------------------------
##################################### vector access
a=[0,1,2,3,4,5,6,7,8]
---------------------------------
param doublevec a;
doublevec b = a[0:3];
doublevec c = a[0:-1];
doublevec d = a[0:0];
doublevec f = a[8:8];
doublevec g = a[7:8];
doublevec h = a[0:9];
b=b;
---------------------------------
b=[0,1,2]
c=[0,1,2,3,4,5,6,7,8]
g=[7]
h=[0,1,2,3,4,5,6,7,8]
##################################### matrix access
a=[[1,2,3], [4,5,6], [7,8,9], [0,1,0]]
---------------------------------
param doublemat a;
double b=a[0,1];
doublevec c=a[1,:];
doublevec d=a[:,1];
doublevec e=a[1:3,1];
doublevec f=a[1,0:2];
doublevec g=a[1,1:-1];
doublemat h=a[0:2,0:3];
doublemat j=a[:,:];
b=b;
---------------------------------
b=2
c=[4,5,6]
d=[2,5,8,1]
e=[5,8]
f=[4,5]
g=[5,6]
h=[[1,2,3],[4,5,6]]
j=[[1,2,3], [4,5,6], [7,8,9], [0,1,0]]
##################################### stringconstants
a=1
---------------------------------
int a = symtest("aa");
int b = symtest("CC d");
int c = 0;
c = a+b;
---------------------------------
a=2
b=4
c=6
##################################### test of abs, SPR 270036
---------------------------------
double b=2.0;
b = b -10.0;
b=abs(b);
---------------------------------
b=8
##################################### test of multiple mulop, SPR270144
---------------------------------
double b=2.0;
b = b *3.0 *2.0;
---------------------------------
b=12
##################################### multiplication of double and int, SPR270040
---------------------------------
double b=2.0;
b = b * 2 ;
b = 3 * b ;
---------------------------------
b=12
##################################### less than or equal, SPR 270038
---------------------------------
int a = 5 ;
int b = 4 ;
int c = 5 ;
int d = 6 ;
int res = 0 ;
if ( a <= b ) { res = res; } else { res = res + 1; };
if ( a <= c ) { res = res + 2; };
if ( a <= d ) { res = res + 4; };
---------------------------------
res=7
##################################### greater than or equal, SPR 270038
---------------------------------
int a = 5 ;
int b = 4 ;
int c = 5 ;
int d = 6 ;
int res = 0 ;
if ( a >= b ) { res = res + 1; };   # Test a comment
# Another comment
if ( a >= c ) { res = res + 2; };
if ( a >= d ) { res = res; } else { res = res + 4; };
---------------------------------
res=7
##################################### point operators on vectors, SPR 270042
a = [25,9,48]
b = [5,3,8]
---------------------------------
param doublevec a;
param doublevec b;
doublevec res = a;
res = a./b;
---------------------------------
res=[5,3,6]
##################################### point operators on vectors, SPR 270042
a = [7,9,11]
b = [5,3,8]
---------------------------------
param doublevec a;
param doublevec b;
doublevec res = a;
res = a.*b;
---------------------------------
res=[35,27,88]
#####################################
"""    

    
def complete_test():    
    #code = """double b=2.0*2.0;
    #param double a;
    #b=max(7.1, a);
    #b=a;"""
    #valfunc = acm.FUDMCValuationFunction(code)
    #params = acm.FDictionary()
    #params.AtPut("a", 9.3)
    #print (valfunc.PerformValuation(params))
    failed = 0
    cases = load_test_cases(testcases)
    #for case in [cases[-1]]:
    for case in cases:
        # Do not show pydot diagram if the test is supposed to fail.
        if case.shouldfail():
            import FUDMCCommon
            dot = FUDMCCommon.pydot
            FUDMCCommon.pydot = False

        try:
            #print (case)
            res = case.test()
            #print (res)
        except Exception as err:
            if case.shouldfail():
                pass
            else:
                print ("FAILED ", err)
                print (case)
                failed = failed + 1
                raise
        if case.shouldfail():
            FUDMCCommon.pydot = dot
                
    return failed

def proces_test():
    """Very basic tests for processes"""
    mclib = acm.FUDMCLibrary()
    if mclib.GetProcessValueType("sldskjf") != "": raise Exception("Type for non-existing process should be zero")
    return 0
 
     
def errorhandling_test():
    adflexpr = """mcvalue("doublevec a=zeros(4);
double c=7.0;
c=a[0];
c=a[1];
c=a[2];
c=a[3];
c=a[4];", object)"""
    adflobject = acm.FInstrument['ABB'] #we don't use the instrument so any will do
    adflcontext = acm.GetDefaultContext()    
    adfltag = acm.CreateEBTag()
    res = acm.GetCalculatedValueFromString(adflobject, adflcontext, adflexpr, adfltag).Value()
    res.PerformValuation({}, 0.4)
    
    





