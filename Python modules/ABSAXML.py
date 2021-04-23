"""-----------------------------------------------------------------------
MODULE
    ABSAXML

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Wraps the xml minidom class for xml creation. Is called by the ABSAPortfolioSwapReports module.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import os
import FReportSettings
from xml.dom import minidom
from string import Template
'''================================================================================================
Versioning, this will have to be stored in TimeSeries, if there is more then one...
Do we get the Vlaue's from the XML? Or Set Variables?
================================================================================================'''
class ABSAReportXML:

    XmlDom              = None
    XmlDoc              = None
    RootNode            = None 
    InputParams         = None
    FileName            = None
    ReportName          = None
    ReportDate          = None 
    Client              = None
    ParamDict           = {}     #MKLIMKE Do we really need this
    OutputDirectory     = None
    Path                = None
    Template            = None   #MKLIMKE this is making it very specific?
    
    '''==============================================================
    ==============================================================='''
    def __init__(Self, Type, Client, ReportDate): #maybe pass the dictionary

        Self.ReportName = Type
        Self.Client     = Client
       
        Self.ReportDate = ReportDate

        Self.XmlDom     = minidom.getDOMImplementation()
        Self.XmlDoc     = Self.XmlDom.createDocument(None, Self.clean_tag_name(Self.ReportName), None)
        Self.RootNode   = Self.XmlDoc.documentElement     

        #Self.getExtensionParameters() #MKLIMKE
        Self.FileName()
    '''==============================================================
    ==============================================================='''
    def create_tag(self, node, name): #MKLIMKE could have node type here
        name    = self.clean_tag_name(name) 
        newnode = self.XmlDoc.createElement(name)
        node.appendChild(newnode)
        return newnode
    '''==============================================================
    ==============================================================='''
    def create_full_tag(self, node, name, value):
        name        = self.clean_tag_name(name) 
        elementNode = self.XmlDoc.createElement(name)
        valueNode   = self.XmlDoc.createTextNode(value)
        elementNode.appendChild(valueNode)
        node.appendChild(elementNode)
        return elementNode
    '''==============================================================
    ==============================================================='''
    def to_string(self,Pretty = False):
        if Pretty == False:
            return self.XmlDoc.toxml()
        else:    
            return self.XmlDoc.toprettyxml()
    '''==============================================================
    Certain Values are not allowed in XML so wee need to strip them.
    ==============================================================='''
    def clean_tag_name(self, value):
        NewValue = str(value)
        NewValue  = NewValue.replace(' ', '_') 
        NewValue  = NewValue.replace('&', 'and')
        NewValue  = NewValue.replace('/', '-')
        NewValue  = NewValue.replace('[', '')
        NewValue  = NewValue.replace(']', '')
        NewValue  = NewValue.replace("'", '')
        return NewValue
    '''==============================================================
    ==============================================================='''
    def assemble_chain_grouper(self, list):
        GrouperList = []
        for g in list:
            GrouperList.append(acm.Risk().GetGrouperFromName(g))
        ch_grouper      = acm.FChainedGrouper(GrouperList)
    '''==============================================================
    Do we need to recurse the tree???
    Add the Sheet Type
    ==============================================================='''
    def sheet_to_xml(self,context,node,sheet,date,item,chainedGrouper = None):
        createContext   = acm.FColumnCreatorCreateContext(context)  
        columns         = sheet.ColumnCollection(createContext)
        sheetnode       = self.create_tag(node, 'Sheet')    

        self.create_full_tag(sheetnode, 'SheetName', sheet.Contents().AtString('sname'))    
        self.create_full_tag(sheetnode, 'ColumnCount', str(len(columns)))    
        
        calcSpace = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet') #MKLIMKE get the sheet type from the parameters
        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
        topnode   = calcSpace.InsertItem(item)
        
        if chainedGrouper != None: #MKLIMKE add a grouper later!!
            pass

        calcSpace.Refresh()
        portfolioIter       = calcSpace.RowTreeIterator().FirstChild()  
        childIter           = portfolioIter.FirstChild()
      
        while childIter:

            rownode = self.create_tag(sheetnode, 'Row')
            rownode = self.create_tag(rownode, childIter.Tree().StringKey())
            for c in columns:
                Calc = calcSpace.CalculateValue(childIter.Tree(), c.ColumnId())
                self.create_full_tag(rownode, c.ColumnId(), str(Calc))
            childIter = childIter.NextSibling()

        calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    '''==============================================================
    ==============================================================='''
    def getExtensionParameters(self):
        ParamNode = self.create_tag(self.RootNode, 'Parameters')
        ParamDict = acm.FExtensionContext['Standard'].GetExtension('FParameters', 'FObject', 'Client Statement').Value()
        for Param in ParamDict.Keys():
            pass
            #print ParamDict[Param]
    '''==============================================================
    ==============================================================='''
    def ACMObjectToXML(Self, Node, AcmEntity):
    
        EntityNode = Self.create_tag(Node, AcmEntity.RecordType())
        Index = 0
        for Column in AcmEntity.Table().Columns():
            TagName     = Self.clean_tag_name(Column)
            Value       = Self.clean_tag_name(AcmEntity.ColumnValues()[Index])
            Self.create_full_tag(EntityNode, TagName, Value)
            Index = Index + 1

    '''==============================================================
    ==============================================================='''
    def TranformToFo(Self, StyleSheet):
        context         = acm.GetDefaultContext()
        pt              = context.GetExtension('FXSLTemplate', 'FObject', StyleSheet)       
        xsl             = pt.Value()
        transformer     = acm.CreateWithParameter('FXSLTTransform', xsl)

        xmlfilePath     = str(Self.InputParams['outputPath'].SelectedDirectory()) + "/" +  Self.FileName + '.xml' 
        xmlfile         = open(xmlfilePath, "w")  
        xmlfile.write(Self.to_string(True))
        xmlfile.close()
        acm.Log('File:' + Self.FileName + '.xml')
        
        FOP             = transformer.Transform(Self.to_string())
        file            = str(Self.InputParams['outputPath'].SelectedDirectory()) + "/" +  Self.FileName + '.fo' #MKLIMKE Not so sure I like this 
        outfile         = open(file, "w")  
        outfile.write(FOP)
        outfile.close()
    '''==============================================================
    ""Y:\Jhb\Arena\Prime\FOP\fop.bat" "${filename}.fo" -${extension} "${filename}.${extension}" -c "Y:\Jhb\Arena\Prime\FOP\conf\config.xml""
    ""Y:\Jhb\Arena\Prime\FOP\fop.bat" "TEST.fo" -pdf "TEST.pdf" -c "Y:\Jhb\Arena\Prime\FOP\conf\config.xml""
    ==============================================================='''
    def FopConversion(Self):
        file        = str(Self.InputParams['outputPath'].SelectedDirectory()) + "/" +  Self.FileName
        command     = Template(FReportSettings.FOP_BAT)
        command     = command.substitute({'extension':'pdf', 'filename':file})
        os.system(command)
        acm.Log('File:' + Self.FileName + '.pdf')
        
        
    '''==============================================================
    This really has nothing to do with XML??
    ==============================================================='''
    def PDFToScreen(Self):
        os.system(str(Self.InputParams['outputPath'].SelectedDirectory()) + "/" +  Self.FileName + '.pdf')
    '''==============================================================
    Would be easier to get the client name here ....
    ==============================================================='''
    def FileName(Self):
        Self.FileName = Self.clean_tag_name(Self.ReportName + Self.ReportDate + Self.Client)
    '''==================================================================================================================================
    =================================================================================================================================='''
    def AelVariablesToXml(Self, Node, ParamDict):
        SettingNode = Tag(Dom, Node, 'ReportSettings')
        for Parameter in ParamDict.keys():
            Value = ''
            try:
                Value = ParamDict[Parameter].StringKey()
            except:
                Value = str(ParamDict[Parameter])
                pass
            fullTag(Dom, SettingNode, Parameter, Value)
        return SettingNode
    '''==================================================================================================================================
    ABOUT:
        
    NOTES:
        Do we want to return a list or a single node? Actually should give error if return more then one. (ambigious)
    =================================================================================================================================='''
    def FindNode(Self, Node, Name):
 
        NodeList = Node.getElementsByTagName(Name)
        if len(NodeList) == 0:
            return None
        if len(NodeList) == 1:
            return NodeList[0]
        if len(NodeList) > 1:
            raise Exception('Error then is more then one node returned')
    '''==================================================================================================================================
    ABOUT:
    =================================================================================================================================='''
    def GetNodeValue(Self, Node, Name):
        Node = Self.FindNode(Dom, Dom.documentElement, Name)
        if Node:
            return Node.childNodes[0].nodeValue
        else:
            return ""
    '''================================================================================================
    TODO:
    Notes:
       First check if the node exists, create it if it doesn't.
       What we can do is update
    ABOUT:
        Options 
                Amend   = 0
                Update  = 1
                Average = 3
    ================================================================================================'''
    def UpdateNodeValue(Self,Node,NodeName,Value,Option = 0,Dec = 2):

        SubNode = Self.FindNode(Node, NodeName)
        if SubNode == None:
            SubNode = Self.create_full_tag(Node, NodeName, formnum(Value, Dec))
        else:
        
            #MK FIX for Francois
            NodeValue   = SubNode.childNodes[0].nodeValue.replace(',', '')
            NodeValue   = NodeValue.replace('(', '')
            NodeValue   = NodeValue.replace(')', '')
            
            
            FloatVal    = float(NodeValue)

            if Option == 0:
                NewValue    = FloatVal + Value

            if Option == 1:
                NewValue    = Value
            
            SubNode.removeChild(SubNode.childNodes[0])
            TextNode    = Self.XmlDoc.createTextNode(formnum(NewValue, Dec))
            SubNode.appendChild(TextNode)

    '''================================================================================================
    TODO:
        This won't work beacuse we are looking for element 
    ================================================================================================'''
    def FindNodeWithValue(Self, Node, NodeName, Value):
        NodeList = Node.getElementsByTagName(NodeName) 
        for Node in NodeList:
            if Node.childNodes[0].nodeValue == Value: #Remember that the value inside the node is also a node.
                return Node
        return None    
    '''==============================================================
    Functions still ToDo
    ==============================================================='''
    def CheckSchema(): pass
    def SheetPropertiesToXML(): pass
    def AddAttribute(self, node, name, value): pass
'''================================================================================================
Testing:
================================================================================================'''
#x = ABSAReportXML('TEST')
'''================================================================================================
Notes:
    Thank you Zakirah
================================================================================================'''
def formnum(x,dec = 2):  
    
    Neg = False
    if x < 0:
        Neg = True
        x = x*-1
    
    pl = 2
    if dec != 0:
        pl = dec
    
    evalstr =  "'%." + str(pl) + "f' %x"
    y = eval(evalstr)
    
    sp = y.split('.')
    check = 0
    
    
    if sp[0][0] == '-':
        check = 1
        conv = sp[0][1:]
    else:
        conv =sp[0]
        
        
    l = len(conv)
    ns = ''
    x = (l%3)
    
    if l > 3:
        ind = l -3
        ns = conv[ind:l]
        while ind >= 0:
           
            if x ==0 and ind == 0:
                ns = ns + '.' + sp[1]
            else:
                ns =  conv[ind-3:ind] + ',' + ns
            
            ind -=3
        
        if x != 0:
            
            ns = conv[0:x] + ns + '.' + sp[1]
            
        if check ==1:
            ns = '-' + ns
    else:
        ns = y
   
    
    if dec == 0:
        x = ns.split('.')
        if Neg:
            return '-' + x[0]
        else:
            return x[0]
    else:
        if Neg:
            return '-' + ns
        else:
            return ns
       
