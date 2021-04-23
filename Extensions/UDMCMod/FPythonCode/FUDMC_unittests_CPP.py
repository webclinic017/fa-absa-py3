

from __future__ import print_function
import acm
import FUDMCParser_CPP
import FUDMCSemanticAnalyzer_CPP
from FUDMCCommon_CPP import MCError

import string

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
            if abs(otherf-self.val) < self.bound:
                return 0
        except Exception as e:
            print ("EE", e)
            pass
        return cmp(self.val, other)
    def __repr__(self):
        return "(fuzzy) %d +/- %d"%(self.val, self.bound)

        
def expect_err(locals, codestr, errclass):
    try:
        eval(codestr, globals(), locals)
        raise Exception("Code string should have thrown an exception")
        print ("Expected exception caught:", msg)
    except errclass as msg:
        pass

def expect_TypeError(locals, codestr):
    expect_err(locals, codestr, TypeError)

def expect_RuntimeError(locals, codestr):
    expect_err(locals, codestr, RuntimeError)
    
def basic_test():
    """Test some basic functionality of UDMC"""
    mclib = acm.FUDMCLibrary()
    func = acm.FUDMCValuationFunction("")
    
    # test vm
    func.vm_mkCVarNode(1, "double", "a", True, False, 1)
    #test duplicate var decl 
    expect_RuntimeError(locals(), """func.vm_mkCVarNode(1,"double","a",True,False,1)""")
    expect_RuntimeError(locals(), """func.vm_mkCVarNode(2,"badtype","a",True,False,1)""")
    expect_RuntimeError(locals(), """func.vm_mkCVarNode(4,"int","a",True,True,1)""")
    
    func.vm_mkCNode(2, "double", 1.2, "double", acm.FArray(), "")
    expect_RuntimeError(locals(), """func.vm_mkCNode(2,"double",1.2,"double",acm.FArray(),"")""")
    func.vm_mkCNode(3, "double", 0.0, "double", acm.FArray(), "")   #Port: What was previously expected with opval None?
    return 0

class TestCase:
    epsilon = 1e-12
    def __init__(self, params, code, results):
        """Construct a test case
        
        Arguments:
        params     -- Dict {paramname:paramval}
        code       -- String PEL code
        results    -- Dict {paramname:finalvalue}
        """
        self.params     = params
        self.code       = code
        self.results    = results
        self.mcexpr     = None
        self.exception  = None
        self.failed     = False
    
    def test(self):
        #run it through parser and semantic analyzer first to get good tracebacks for simple errros
        try:
            ast_tree = FUDMCParser_CPP.parse(self.code)
            FUDMCSemanticAnalyzer_CPP.analyze(ast_tree)

            # now run it through entire loop
            createFunc = acm.GetFunction("CreateCValuationFunction", 1)
            valfunc = createFunc(self.code)

            r = self.params.get("r", 0.05)
            yc = acm.FYieldCurve['DEFAULT']
            ycinfo = yc.IrCurveInformation()
            payDates = [ acm.Time.DateToday() ]
            res = valfunc.PerformCValuation(self.params, ycinfo, None, None, payDates, 1)

            for key, val in self.results.items():
                resval = res[key]
                if not resval:
                    resval = res[acm.FSymbol(key)]
                if not self.CompareResult( resval, val ):
                    print ("Unexpected result in case:\n", self)
                    raise Exception("Unexpected result var %s expected %s got %s" % \
                            (key, str(val), str(resval) ) )
                print ("OK ", resval, "==", str(val))
            return res
        except Exception as e:
            self.exception = e
            self.failed = True
        except:
            self.failed = True
        
    def __str__(self):
        return "Testcase:\n\t"+str(self.params) +"\n--\n"+self.code + "\n--\n"+ str(self.results)
    def shouldfail(self):
        """Return true if this case is expected to generate an error"""
        return 'fail' in self.results
        
    def CompareResult( self, calculatedResult, expectedResult ):
        if 'Class' in dir( expectedResult ):
            if expectedResult.Class() == acm.FRealMatrix:
                return self.CompareRealMatrices( calculatedResult, expectedResult )
            elif expectedResult.Class() == acm.FRealArray:
                return self.CompareRealArrays(  calculatedResult, expectedResult )
            elif expectedResult.Class() == acm.FReal:
                try:
                    if abs( calculatedResult - expectedResult ) > TestCase.epsilon:
                        return False
                    else:
                        return True
                except:
                    return False
            else:
                return calculatedResult == expectedResult
        else:
            return calculatedResult == expectedResult
    
    def CompareRealArrays( self, calculatedArray, expectedArray ):
        try:
            for pos in range(expectedArray.Size()):
                if abs( expectedArray.At( pos ) - calculatedArray.At( pos ) ) > TestCase.epsilon:
                        return False
            return True
        except:
            return False
    
    def CompareRealMatrices( self, calculatedMatrix, expectedMatrix ):
        try:
            for row in range(expectedMatrix.Rows()):
                for col in range(expectedMatrix.Columns()):
                    if abs( expectedMatrix.At( row, col ) - calculatedMatrix.At( row, col ) ) > TestCase.epsilon:
                        return False
            return True
        except:
            return False

    
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
cashFlow(0 , a);
---------------------------------
result=fuzzyfloat(3.29617, 10)
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
param matrix(double) a;
double c=7.0;
double d=8.0;
c=a[0];
d=a[1];
---------------------------------
c=3
d=4
##################################### Test vector and matrix functions
a=[3,4,1,7,2]
m=[[1,4,5],[3,4,-3]]
---------------------------------
param matrix(double) a;
param matrix(double) m;
matrix(double) zeromat = zeros(2,4);
double c=max(a);
double d=min(a);
double g=sum(a);
double f=prod(a);
double i=average(a);
double j=average(m);
int k=length(a);
int l=rows(m);
int n=cols(m);
n=n;
---------------------------------
c=7
d=1
g=17
f=168
i=3.4
j=14/6.0
k=5
l=2
n=3
##################################### Test vector and matrix row functions
m=[[1,4,5],[3,4,-3]]
---------------------------------
param matrix(double) m;
matrix(double) a = rowAverage(m);
matrix(double) b = rowProd(m);
matrix(double) c = rowSum(m);
c=c;
---------------------------------
a=[[10/3.0],[4/3.0]]
b=[[20],[-36]]
c=[[10],[4]]
##################################### Test vector and matrix col functions
m=[[1,4,5],[3,4,-3]]
---------------------------------
param matrix(double) m;
matrix(double) a = colAverage(m);
matrix(double) b = colProd(m);
matrix(double) c = colSum(m);
c=c;
---------------------------------
a=[[2,4,1]]
b=[[3,16,-15]]
c=[[4,8,2]]
##################################### Test bad vectors
a=[3,4]
---------------------------------
param matrix(double) a;
double c=7.0;
c=a[300];
---------------------------------
c=3
d=4
fail=1
exception = "Matrix index out of range"
##################################### Test matrix
a=[[1,2,3], [4,5,6]]
---------------------------------
param matrix(double) a;
matrix(double) b=a;
b=transpose(a);
---------------------------------
b=[[1,4],[2,5],[3,6]]
##################################### Test matrix access
a=[[1,2,3], [4,5,6]]
---------------------------------
param matrix(double) a;
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
param matrix(double) a;
double e=0.0;
e=a[3000,0];
---------------------------------
fail=1
exception = "Matrix index out of range"
##################################### Test matrix mul 
a=[[1,2,3], [4,5,6]]
b=[ [3,4],[5,6],[3,4] ]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) c=a*b;
c=c;
---------------------------------
c=[[22, 28],[55, 70]]
##################################### Test matrix sub
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) c=a-b;
c=c;
---------------------------------
c=[[0,1,2],[6,5,4]]
##################################### Test matrix add
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) c=a+b;
c=c;
---------------------------------
c=[[2,3,4],[2,5,8]]
##################################### Test matrix elementwise mul
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) c=a.*b;
c=c;
---------------------------------
c=[[1,2,3],[-8,0,12]]
##################################### Test matrix elementwise div
a=[[1,2,3], [4,5,6]]
b=[[1,1,1], [-2,0,2]]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) c=a./b;
c=c;
---------------------------------
c=[[1,2,3],[-8,0,12]]
fail=1
##################################### Test matrix scalar
a=[[2,4,8], [4,-2,6]]
b=2
---------------------------------
param matrix(double) a;
param double b;
matrix(double) c=a*b;
matrix(double) d=a/b;
matrix(double) e=a+b;
matrix(double) f=a-b;
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
param matrix(double) a;
param double b;
matrix(double) c=a/b;
c=c;
---------------------------------
c=[[4,8,16],[8,-4,12]]
fail=1
##################################### Test matrix min/max 
a=[[2,4,8], [0,-2,6]]
---------------------------------
param matrix(double) a;
matrix(double) c=max(a,1.0);
matrix(double) d=min(2.0,a);
double e=max(a);
double f=min(a);
c=c;
---------------------------------
c=[[2,4,8], [1,1,6]]
d=[[2,2,2], [0,-2,2]]
e=8
f=-2
##################################### Test vanilla
strikePrice=3
vol=4
---------------------------------
param double strikePrice;
param double vol;
cashFlow(0, strikePrice * vol );
---------------------------------
##################################### vector access
a=[0,1,2,3,4,5,6,7,8]
---------------------------------
param matrix(double) a;
matrix(double) b = a[0:3];
matrix(double) c = a[0:-1];
matrix(double) d = a[0:0];
matrix(double) f = a[8:8];
matrix(double) g = a[7:8];
matrix(double) h = a[0:9];
matrix(double) i = a[-1:-1];
b=b;
---------------------------------
b=[[0,1,2]]
c=[[0,1,2,3,4,5,6,7,8]]
d=[[0]]
f=[[8]]
g=[[7]]
h=[[0,1,2,3,4,5,6,7,8]]
i=[[8]]
##################################### matrix access
a=[[1,2,3], [4,5,6], [7,8,9], [0,1,0]]
---------------------------------
param matrix(double) a;
double b=a[0,1];
matrix(double) c=a[1,:];
matrix(double) d=a[:,1];
matrix(double) e=a[1:3,1];
matrix(double) f=a[1,0:2];
matrix(double) g=a[1,1:-1];
matrix(double) h=a[0:2,0:3];
matrix(double) j=a[:,:];
b=b;
---------------------------------
b=2
c=[[4,5,6]]
d=[[2],[5],[8],[1]]
e=[[5], [8]]
f=[[4,5]]
g=[[5,6]]
h=[[1,2,3],[4,5,6]]
j=[[1,2,3], [4,5,6], [7,8,9], [0,1,0]]
##################################### test of abs, SPR 270036
---------------------------------
double b=2.0;
b = b -10.0;
b=abs(b);
---------------------------------
b=8
##################################### test of multiple mulop, SPR 270144
---------------------------------
double b=2.0;
b = b *3.0 *2.0;
---------------------------------
b=12
##################################### multiplication of double and int, SPR 270040
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
if ( a >= b ) { res = res + 1; };    # Test a comment
# Another comment
if ( a >= c ) { res = res + 2; };
if ( a >= d ) { res = res; } else { res = res + 4; };
---------------------------------
res=7
##################################### point operators on vectors, SPR 270042
a = [25,9,48]
b = [5,3,8]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) res = a;
res = a./b;
---------------------------------
res=[[5,3,6]]
##################################### point operators on vectors, SPR 270042
a = [7,9,11]
b = [5,3,8]
---------------------------------
param matrix(double) a;
param matrix(double) b;
matrix(double) res = a;
res = a.*b;
---------------------------------
res=[[35,27,88]]
##################################### SPR 274105: Erroneous function calls should generate better messages.
a = 10
---------------------------------
param int a;
int b = 5;
b = unknownFunc(a); # Unknown method.
---------------------------------
fail = 1
exception = "No overloaded function matches call"
##################################### SPR 274105: Parameter declarations in main loop generates bad messages.
a = [0.7, 3.9, 8.7]
b = [1.2, 3.4, -0.8]
---------------------------------
param matrix(double) a;
param matrix(double) b;

a = a.*b; 
double c = 0.19; # Variable declaration not allowed here.
---------------------------------
fail = 1
exception = "Declaration not allowed in main loop"
##################################### SPR 274105: Vector-matrix type mismatch generates unintuitive messages.
---------------------------------
double a=3.0;
double b=4.0;
int res = 0;
if(a<b){ res=res+1;};
if(b>a){ res=res+1;};
---------------------------------
res=2
##################################### Bug in type propagation.
aMat = [[1.0, 2.0], [3.0, 4.0]]
---------------------------------
param matrix(double) aMat;
double maxValue = 0.0;

maxValue = (rowMax(aMat,0,2))[0,0]; # The expression in parenthesis must be converted to a matrix (funccall pass) before the index-expression is evaluated.
---------------------------------
maxValue = 2.0
##################################### SPR 274102: Loop from 0 to 0 should not generate error messages.
a=0
---------------------------------
param int a;
int i=3;
int sum=1;
for i=0 to a
{
    sum=sum+i;
};
---------------------------------
sum=1
##################################### Zeros with single parameter
---------------------------------
matrix(double) zeroVec = zeros(10);
double n = zeroVec[5];
n=n;
---------------------------------
n = 0.0
##################################### Operators
a = 1
b = 0
---------------------------------
param int a;
param int b;
int c = 0;
int d = 0;
int e = 0;
int f = 0;
int g = 0;
int h = 0;
int i = 0;
int j = 0;
int k = 0;
c = a and b;
d = a or b;
e = not b;
f = a == b;
g = a != b;
h = a > b;
i = a < b;
j = a >= b;
k = a <= b;
---------------------------------
c = 0
d = 1
e = 1
f = 0
g = 1
h = 1
i = 0
j = 1
k = 0
##################################### Operators with general ints
a = 27
b = -19
c = 0
---------------------------------
param int a;
param int b;
param int c;
int d = 0;
int e = 0;
int f = 0;
d = a or b;
e = a and c;
f = b or c;
---------------------------------
d = 1
e = 0
f = 1
#####################################
anInt = 5
---------------------------------
param int anInt;
cashFlow(0, anInt );
---------------------------------
result=fuzzyfloat(0, 10)
fail = 1
exception = "No overloaded function matches call"
#####################################
anInt = 5
aDouble = 15.0
---------------------------------
param int anInt;
param double aDouble;
double mulRes = aDouble * anInt;
double divRes = aDouble / anInt; 
---------------------------------
mulRes = 75.0
divRes = 3.0 
##################################### If no PEL is submitted, output a readable error message.
---------------------------------
---------------------------------
fail = 1
exception = "UDMC Parser called without input PEL code."
#####################################
mat=[[7, 8, 9], [1, 2, 3], [4, 5, 6]]
rows = 3
cols = 3
---------------------------------
param matrix(double) mat;
param int rows;
param int cols;
matrix(double) rowOne = mat[0, :];
matrix(double) colTwo = mat[:, 1];
matrix(double) lastRow = mat[rows - 1, :];
matrix(double) lastCol = mat[:, cols - 1];
matrix(double) lowerTwo = mat[1:3, :];
matrix(double) leftTwo = mat[:, 0:2];
matrix(double) upperRight = mat[0:2, 1:3];
matrix(double) allMatrix = mat[:, :];
matrix(double) bottomRow = mat[2, 0:3];
matrix(double) centerCol = mat[0:3, 1];
matrix(double) centerRow = mat[1:1,:];
matrix(double) rightCol = mat[:, 2:2];
double centerEl = mat[rows-2, cols-2];
---------------------------------
rowOne = [[7, 8, 9]]
colTwo = [[8], [2], [5]]
lastRow = [[4, 5, 6]]
lastCol = [[9], [3], [6]]
lowerTwo = [[1, 2, 3], [4, 5, 6]]
leftTwo = [[7, 8], [1, 2], [4, 5]]
upperRight = [[8, 9], [2, 3]]
allMatrix = [[7, 8, 9], [1, 2, 3], [4, 5, 6]]
bottomRow = [[4, 5, 6]]
centerCol = [[8], [2], [5]]
centerRow = [[1, 2, 3]]
rightCol = [[9], [3], [6]]
centerEl = 2.0
##################################### SPR 277701: Minus operator does not work ok.
---------------------------------
double a = -7.0;
---------------------------------
a = -7.0
##################################### SPR 274103: 
vec = [[1.0, 2.0, 3.0, 4.0, 5.0]]
mat = [[7.0, 8.0, 9.0],[11.0, 12.0, 13.0]]
---------------------------------
param matrix(double) vec;
param matrix(double) mat;
double a = vec[0, -1];
double b = vec[-1, -1];
double c = mat[0, -1];
double d = mat[-1, 0];
matrix(double) e = mat[:, -1];
matrix(double) f = mat[-1, :];
double g = vec[-1];
double h = mat[-1];
matrix(double) i = mat[-1:-1, 0];
matrix(double) j = mat[0,-1:-1];
matrix(double) k = mat[1, 1:1];
matrix(double) l = mat[0:0, 1];
---------------------------------
a = 5.0
b = 5.0
c = 9.0
d = 11.0
e = [[9.0], [13.0]]
f = [[11.0, 12.0, 13.0]]
g = 5.0
h = 13.0
i = [[11.0]]
j = [[9.0]]
k = [[12.0]]
l = [[8.0]]
##################################### SPR 283914
a = 5
b = 6
---------------------------------
param double a;
param double b;
double s1 = 3.0;
double s2 = 4.0;
double K = 7.0;
double result1 = 0.0;
double result2 = 0.0;
        
result1 = max(K + a*s1 + b*s2, 0.0);
result2 = max(a*s1 + b*s2 + K, 0.0);
---------------------------------
result1 = 46
result2 = 46
##################################### Unary Operators
anInt = 7
aDouble = 15.0
aMat = [[3, 4], [23, -5], [54, -34]]
---------------------------------
param int anInt;
param double aDouble;
param matrix(double) aMat;
int negAnInt = - anInt;
double negADouble = - aDouble;
matrix(double) negAMat = - aMat;
matrix(double) negAnExpression = - (aMat * aDouble);
int posAnInt = + anInt;
double posADouble = + aDouble;
matrix(double) posAMat = + aMat;
matrix(double) posAnExpression = + ( - aMat * aDouble);
---------------------------------
negAnInt = -7
negADouble = -15.0
negAMat = [[-3, -4], [-23, 5], [-54, 34]]
negAnExpression = [[-45, -60], [-345, 75], [-810, 510]]
posAnInt = 7
posADouble = 15
posAMat = [[3, 4], [23, -5], [54, -34]]
posAnExpression = [[-45.0, -60.0], [-345.0, 75.0], [-810.0, 510.0]]
#####################################
a = 5.0
b = 3.0
c = 7
d = 8
---------------------------------
param double a;
param double b;
param int c;
param int d;

double result1 = - a - b;
double result2 = - (a - b);
double result3 = - (a + b);
int result4 = - c - d;
int result5 = - (c - d);
int result6 = - (c + d);
---------------------------------
result1 = -8.0
result2 = -2.0
result3 = -8.0
result4 = -15
result5 = 1
result6 = -15
##################################### SPR 284156
mat = [[3,4,1],[23,5,3],[54,34,89]]
---------------------------------
param matrix(double) mat;
matrix(double) resultSort = sort(mat);
---------------------------------
resultSort = [[1.0, 3.0, 3.0], [4.0, 5.0, 23.0], [34.0, 54.0, 89.0]]
##################################### SPR 284156
mat = [[3, 4, 89], [23, 5, 3], [54, 34, 6]]
---------------------------------
param matrix(double) mat;
matrix(double) resultSort = colSort(mat);
---------------------------------
resultSort = [[3.0, 4.0, 3.0], [23.0, 5.0, 6.0], [54.0, 34.0, 89.0]]
##################################### SPR 284156
mat = [[3, 4, 89], [23, 5, 3], [54, 34, 6]]
---------------------------------
param matrix(double) mat;
matrix(double) resultSort = rowSort(mat);
---------------------------------
resultSort = [[3.0, 4.0, 89.0], [3.0, 5.0, 23.0], [6.0, 34.0, 54.0]]
##################################### SPR 284156
mat = [[3, 4, 89], [23, 5, 3], [54, 34, 6]]
---------------------------------
param matrix(double) mat;
matrix(double) resultSort = reverse(mat);
---------------------------------
resultSort = [[6.0, 34.0, 54.0], [3.0, 5.0, 23.0], [89.0, 4.0, 3.0]]
##################################### SPR 284156
mat = [[3, 4, 89], [23, 5, 3], [54, 34, 6]]
---------------------------------
param matrix(double) mat;
matrix(double) resultSort = colReverse(mat);
---------------------------------
resultSort = [[54.0, 34.0, 6.0], [23.0, 5.0, 3.0], [3.0, 4.0, 89.0]]
##################################### SPR 284156
mat = [[3, 4, 89], [23, 5, 3], [54, 34, 6]]
---------------------------------
param matrix(double) mat;
matrix(double) resultSort = rowReverse(mat);
---------------------------------
resultSort = [[89.0, 4.0, 3.0], [3.0, 5.0, 23.0], [6.0, 34.0, 54.0]]
##################################### Unary Operators
anInt = 7
aDouble = 15.0
aMat = [[3, 4], [23, -5], [54, -34]]
---------------------------------
param int anInt;
param double aDouble;
param matrix(double) aMat;
int negAnInt = - anInt;
double negADouble = - aDouble;
matrix(double) negAMat = - aMat;
matrix(double) negAnExpression = - (aMat * aDouble);
int posAnInt = + anInt;
double posADouble = + aDouble;
matrix(double) posAMat = + aMat;
matrix(double) posAnExpression = + ( - aMat * aDouble);
---------------------------------
negAnInt = -7
negADouble = -15.0
negAMat = [[-3, -4], [-23, 5], [-54, 34]]
negAnExpression = [[-45, -60], [-345, 75], [-810, 510]]
posAnInt = 7
posADouble = 15
posAMat = [[3, 4], [23, -5], [54, -34]]
posAnExpression = [[-45.0, -60.0], [-345.0, 75.0], [-810.0, 510.0]]
#####################################
a = 5.0
b = 3.0
c = -9.0
d = 8
e = 12
f = -11
g = [ [ 7.0, 2.0, -3.0 ], [ 6.0, -4.0, 11.0 ] ]
h = [ [ 4.0, 6.0, 1.0 ], [ -12.0, -3.0, 2.0 ] ]
i = [ [ 5.0, 3.0, 9.0 ], [ -1.0, 6.0, 8.0 ] ]
j = [ [ 2.2, 7.5, -12.4 ], [ 39.2, 22.8, -119.6 ] ]
---------------------------------
param double a;
param double b;
param double c;
param int d;
param int e;
param int f;
param matrix(double) g;
param matrix(double) h;
param matrix(double) i;
param matrix(double) j;

double result1 = a - b + c - ( c + c - b ) + ( - a + b - c );
double result2 = - a - b - c + a + b + c;
double result3 = - d + a + f - a + d - c;
int result4 = d - e - f - ( d + d - f ) + ( - d + e - f );
int result5 = - d - e - f + d + e + f;
int result6 = - f + d + f - ( d - e + d );
matrix(double) result7 = g + ( i - h ) + g - ( h + i );
matrix(double) result8 = - g - h - i + g + h + i;
matrix(double) result9 = i + g - ( h + i - g ) + ( -g + h + -i );
matrix(double) result10 = g - h - j + ( -g - j - i - h ) + g - h + h + g + ( -j - g );
---------------------------------
result1 = 21.0
result2 = 0.0
result3 = -2.0
result4 = -5.0
result5 = 0
result6 = 4
result7 = [ [ 6.0, -8.0, -8.0 ], [ 36.0, -2.0, 18.0 ] ]
result8 = [ [ 0.0, 0.0, 0.0 ], [ 0.0, 0.0, 0.0 ] ]
result9 = [ [ 2.0, -1.0, -12.0 ], [ 7.0, -10.0, 3.0 ] ]
result10 = [ [ -12.6, -35.5, 23.2 ], [ -86.6, -72.4, 357.8 ] ]
#####################################
"""

def complete_test():    
    failed = 0
    cases = load_test_cases(testcases)
    #for case in [cases[-1]]:
    for case in cases:
        # Do not show pydot diagram if the test is supposed to fail.
        if case.shouldfail():
            import FUDMCCommon_CPP
            dot = FUDMCCommon_CPP.pydot
            FUDMCCommon_CPP.pydot = False

        print ("------------------ Case Begin ------------------------")
        print (case)
        res = case.test()
        
        try:
            if case.failed:
                handle_failed(case)
            else:
                print (res)
                print ("pass")
        except:
            print ("FAILED")
            failed = failed + 1
        FUDMCCommon_CPP.pydot = dot

    return failed

def handle_failed(_testCase):
    if _testCase.shouldfail():
        """ Check that error messages are as expected (McError)"""
        if _testCase.results.get('exception', None):
            expectedError = _testCase.results.get('exception')
            if not _testCase.exception:
                print ("FAILED - Error expected but not thrown")
                failed = failed + 1
            elif string.find(str(_testCase.exception), str(expectedError)) < 0:
                print ("FAILED - Error message: \n\tExpected:\t%s\n\tGot:\t%s"%(str(expectedError), str(_testCase.exception)))
                failed = failed +1
            else:
                print ("pass(e) - Exception thrown: %s"%str(_testCase.exception))
        else:
            print ("pass(e) - Exception thrown: %s"%((_testCase.exception and str(_testCase.exception)) or 'No error message.'))
    else:
        print ("FAILED - Error thrown: %s"%((_testCase.exception and str(_testCase.exception)) or 'No error message.'))
        raise

     
def errorhandling_test():
    adflexpr = """mcvalue("matrix(double) a=zeros(4);
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
    res.PerformCValuation({}, 0.4, None, None, None, 1)
    
    
def test():
    failed = 0
    #errorhandling_test()
    #return 
    failed = failed + basic_test()
    failed = failed + complete_test()
    if failed > 0:
        print (failed, "---- Tests Failed ----")
    else:
        print (" ---- All tests completed Ok ----")
    return failed




