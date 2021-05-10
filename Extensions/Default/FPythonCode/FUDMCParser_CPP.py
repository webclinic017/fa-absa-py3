

import re
import string
import spark
from FUDMCCommon_CPP import McAstNode, stringtodict, MCError

def extract_location_info(text, pos):
    linenbr = text[:pos].count("\n")
    return "Line Number = " + str(linenbr+1)+"\nLine = " + \
           text.split("\n")[linenbr] 

class MCExprScanner_1(spark.GenericScanner):
    """Tokenizer for MC mini language, pretty standard stuff
    
    Expression in MCExprScanner_2 have higher precedence.
    """
    def __init__(self):
        self.addtoken(MCExprScanner_1, "statementsep", r' ; ')        
        self.addtoken(MCExprScanner_1, "comma",        r' , ')
        self.addtoken(MCExprScanner_1, "lbrace",       r' \{ ')
        self.addtoken(MCExprScanner_1, "rbrace",       r' \} ')
        self.addtoken(MCExprScanner_1, "lbracket",     r' \[ ')
        self.addtoken(MCExprScanner_1, "rbracket",     r' \] ')
        self.addtoken(MCExprScanner_1, "lparen",       r' \( ')
        self.addtoken(MCExprScanner_1, "rparen",       r' \) ')
        self.addtoken(MCExprScanner_1, "addop",        r' \+ | \- ')
        self.addtoken(MCExprScanner_1, "mullop",       r' / | \* ')
        self.addtoken(MCExprScanner_1, "relop",        r' < | > ')
        self.addtoken(MCExprScanner_1, "assign",       r' = ')
        self.addtoken(MCExprScanner_1, "colon",        r' \: ')        
        self.addtoken(MCExprScanner_1, "sym",          r'([a-zA-Z_][a-zA-Z_0-9]*(\(double\))?)')
        spark.GenericScanner.__init__(self)
    def tokenize(self, text):
        """Main tokenize method"""
        self._rv = []        
        spark.GenericScanner.tokenize(self, text)
        return self._rv    
    def make(self, typename, attr=''):
        """Create token and add it to result list"""
        newnode = McAstNode(typename=typename, attr=attr, terminal=True)
        newnode.debuginfo = extract_location_info( self.string, self.pos)
        self._rv.append(newnode)    
    def t_whitespace(self, dummy):
        r' [\s^\n]+ '
        pass    

class MCExprScanner_2(MCExprScanner_1):    
    """See notes in MCExprScanner_2"""
    def __init__(self):
        self.addtoken(MCExprScanner_2, "number",    r' \d+ ',          "int")
        self.addtoken(MCExprScanner_2, "double",    r' \d+ \. \d+ ')
        self.addtoken(MCExprScanner_2, "for",       r' for(?=\W) ')
        self.addtoken(MCExprScanner_2, "if",        r' if(?=\W) ')
        self.addtoken(MCExprScanner_2, "or",        r' or(?=\W) ')
        self.addtoken(MCExprScanner_2, "and",       r' and(?=\W) ')
        self.addtoken(MCExprScanner_2, "not",       r' not(?=\W) ')
        self.addtoken(MCExprScanner_2, "to",        r' to(?=\W) ')
        self.addtoken(MCExprScanner_2, "else",      r' else(?=\W) ')
        self.addtoken(MCExprScanner_2, "equals",    r' == ',            "relop")
        self.addtoken(MCExprScanner_2, "relop2",    r' <= | >= ',       "relop")
        self.addtoken(MCExprScanner_2, "relop3",    r' != ',            "relop")
        self.addtoken(MCExprScanner_2, "param",     r' param(?=\W) ')
        self.addtoken(MCExprScanner_2, "process",   r' process(?=\W) ')
        self.addtoken(MCExprScanner_2, "elmulp",    r' \./ | \.\* ',    "mullop")
        MCExprScanner_1.__init__(self)

class MCExprASTBuilder(spark.GenericASTBuilder):
    """Build an AST for an expression in MC mini language,takes a token list"""
    def __init__(self, Ast, start, source):
        spark.GenericASTBuilder.__init__(self, Ast, start)
        self.source = source
    def p_expr(self, dummy):
        """ program ::= declarationlist statementlist
            program ::= declarationlist
            program ::= statementlist


            declarationlist ::= declaration statementsep declarationlist
            declarationlist ::= declaration statementsep 
            
            declaration ::= paramdeclaration 
            declaration ::= vardeclaration
            declaration ::= processdeclaration
            
            statementlist ::= statement statementsep statementlist
            statementlist ::= statement statementsep
            statementlist ::= statement 
                        
            vardeclaration ::= typedeclaration assignment
            paramdeclaration ::= param typedeclaration variable
            processdeclaration ::= process typedeclaration variable
            typedeclaration ::= sym
            
            statement ::= expression
            statement ::= assignment
            statement ::= ifstatement
            statement ::= funccall
            statement ::= forloop
            
            block ::= lbrace statementlist rbrace            
            
            assignment ::= variable assignmentop expression
            assignmentop ::= assign
            variable   ::= sym
            
            ifstatement ::= if lparen expression rparen block else block
            ifstatement ::= if lparen expression rparen block
                                 
            forloop ::= for assignment to expression block
            
            funccall ::= sym lparen expressionlist rparen
            funccall ::= sym lparen rparen
            
            expressionlist ::= expression comma expressionlist
            expressionlist ::= expression
            
            expression ::= orstatement
            
            orstatement ::= orstatement or andstatement
            orstatement ::= andstatement
            
            andstatement ::= andstatement and notstatement
            andstatement ::= notstatement
            
            notstatement ::= not condition
            notstatement ::= condition
            
            condition ::= condition relop compound
            condition ::= compound

            compound ::= compound addop multerm
            compound ::= multerm
            
            multerm ::= multerm mullop term
            multerm ::= term
            multerm ::= addop term
            
            term ::= indexexpr
            term ::= matindexexpr
            term ::= sliceexpr
         
            indexexpr ::= factor lbracket compound rbracket
            indexexpr ::= factor lbracket compound rbracket
            indexexpr ::= factor lbracket slice rbracket
            indexexpr ::= factor lbracket emptyslice rbracket
            indexexpr ::= factor
            
            matindexexpr ::= factor lbracket compound comma compound rbracket            
            matindexexpr ::= factor lbracket compound comma slice rbracket
            matindexexpr ::= factor lbracket compound comma emptyslice rbracket

            matindexexpr ::= factor lbracket slice comma compound rbracket
            matindexexpr ::= factor lbracket slice comma slice rbracket
            matindexexpr ::= factor lbracket slice comma emptyslice rbracket
            
            matindexexpr ::= factor lbracket emptyslice comma compound rbracket
            matindexexpr ::= factor lbracket emptyslice comma emptyslice rbracket
            matindexexpr ::= factor lbracket emptyslice comma slice rbracket
            
            matindexexpr ::= factor
            
            sliceexpr ::= factor lbracket slice rbracket
            
            slice ::= compound colon compound 
            emptyslice ::= colon
            
            factor ::= funccall
            factor ::= lparen expression rparen
            factor ::= atom
            
            atom ::= int
            atom ::= double
            atom ::= variable
            
        """
    def error(self, token):
        """Error handler during tokenization process"""
        debuginfo = None
        if token!=None:
            if token.debuginfo != "":
                debuginfo = token.debuginfo
            else:
                debuginfo = extract_location_info(self.source, token.pos)
        raise MCError("Syntax error at or near ", token=token, debug_info=debuginfo)
    
class MCExprStrippedASTBuilder(MCExprASTBuilder):
    """Build a cleaned up AST for a MC payoff expression
    
    Unneccessary nodes are removed and some rearrangements are made
    """
    stripable_nodes = stringtodict("""comma, statementsep, lparen, rparen,
      param, assignmentop, lbrace, rbrace, if, lbracket, rbracket, colon, else,
      for, to, or, and""")
    preserve_nodes = stringtodict("""program, declarationlist, statementlist, expressionlist,
      variable, typedeclaration, relop, paramdeclaration, vardeclaration""")
    convert_nodes = { 'condition' : 'operator', 'term' : 'operator', 'multerm' : 'operator', 'compound' : 'operator' }
    fold_nodes = stringtodict( 'expressionlist, declarationlist, statementlist' )  
    def buildASTNode(self, nodes, nodetype):
        """Construction callback function, builds one node"""

        # strip uninteresting nodes
        children = [node for node in nodes if not node.typename in 
                    MCExprStrippedASTBuilder.stripable_nodes]
        # colapse nodes with just one child unless they will be stripped 
        # later or are interesting
        if len(children) == 1 and \
            not nodetype in MCExprStrippedASTBuilder.preserve_nodes and \
            not nodetype in MCExprStrippedASTBuilder.stripable_nodes:
            return children[0]
        # convert some nodes to a common type
        result = self.AST(MCExprStrippedASTBuilder.convert_nodes.get(
                          nodetype, nodetype))
        # fold nodes - ie make a straight list of a tree structure
        if nodetype in MCExprStrippedASTBuilder.fold_nodes:
            tmpresult = []
            for child in children:
                if child.typename == nodetype:
                    tmpresult.extend(child)
                else:
                    tmpresult.append(child)
            result = self.AST(nodetype)
            result[:len(children)] = tmpresult
        else:          
            # strip not token last to avoid notstatement being removed by one child step
            children = [node for node in children if node.typename != 'not']
            result[:len(children)] = children
        if len(nodes):
            result.debuginfo = nodes[0].debuginfo        
        return result        

class FUDMCPreProcessor:
    declarationStarts = ('param', 'int', 'double', 'matrix(double)', 'process')
    lineNbr = 0
    def __init__(self, text):
        self.unprocessedText = text
        self.processedText = str()
        self.regExp = re.compile(r'#.*');

    def __getattr__(self, attrname):
        if attrname == 'processedText':
            return self.processedText
        else:
            raise AttributeError(attrname)

    def PreProcess(self):
        lines = self.removeComments(self.unprocessedText)
        lines = self.preparseLines(lines)
        self.processedText = string.join(lines, '\n')
    
    def removeComments(self, text):
        lines = []
        for line in text.split('\n'):
            line = string.strip(line)
        
            match = self.regExp.search(line)
            if match:
                lines.append(line.replace(str(match.group()), ''))
            else:
                lines.append(line)
        return lines
    
    def preparseLines(self, lines):
        self.pelCodeState = self.PelCodeInitialState()
        
        FUDMCPreProcessor.lineNbr = 0
        for line in lines:
            FUDMCPreProcessor.lineNbr = FUDMCPreProcessor.lineNbr + 1
            if line.strip() == '':
                continue
            self.pelCodeState = self.pelCodeState.checkState(line)
            self.pelCodeState.checkLine(line)
        return lines
    
    class PelCodeParserState:
        def getFirstWordOnLine(self, line):
            result = re.search('[a-zA-Z_()]*', line)
            return (result and result.group(0)) or ''
        def getLastWordOnLine(self, line):
            result = re.search('[a-zA-Z_()]*$', line)
            return (result and result.group(0)) or ''
        def getFirstNonWhiteOnLine(self, line):
            return (len(line.strip()) and line.strip()[0]) or ''
        def getLastNonWhiteOnLine(self, line):
            return (len(line.strip()) and line.strip()[len(line.strip())-1]) or ''    
            
    class PelCodeInitialState(PelCodeParserState):
        def checkState(self, line):
            if self.getFirstWordOnLine(line) in FUDMCPreProcessor.declarationStarts:
                return FUDMCPreProcessor.PelCodeDeclarationState()
            else:
                return FUDMCPreProcessor.PelCodeStatementState()
        def checkLine(self, line):
            pass
                
    class PelCodeDeclarationState(PelCodeParserState):
        def checkState(self, line):
            if not self.getFirstWordOnLine(line) in FUDMCPreProcessor.declarationStarts:
                return FUDMCPreProcessor.PelCodeStatementState()
            return self
        def checkLine(self, line):
            pass
        
    class PelCodeStatementState(PelCodeParserState):
        def checkState(self, line):
            return self
        def checkLine(self, line):
            if self.getFirstWordOnLine(line) in FUDMCPreProcessor.declarationStarts:
                raise MCError(str("Declaration not allowed in main loop. Syntax error on line: %i"%FUDMCPreProcessor.lineNbr))

def parse(text):
    """Parse text and return parse tree. Will throw exceptions on bad input
    
    Arguments:
      text     -- string, a PEL expression

    Returns: An AST built up of McAstNode objects
    """
    
    """If no code is submitted, don't try to parse."""
    if text in ('', ';'):
        raise MCError("UDMC Parser called without input PEL code.")
    
    preProcessor = FUDMCPreProcessor(text)
    preProcessor.PreProcess()
    
    tokens  = MCExprScanner_2().tokenize(preProcessor.processedText)
    return  MCExprStrippedASTBuilder(McAstNode, 'program', text).parse(tokens)




