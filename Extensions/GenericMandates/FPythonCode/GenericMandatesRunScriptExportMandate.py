"""
RunScript

Export mandate definition to a CSV file.

NOTE: The query folder needs to have the following structure:
    
    <AND>
        <OR>
            <AND>
                Attribute1 = Value
                Attribute2 = Value
                ...
            <AND>
                Attribute3 = Value
                Attribute4 = Value
                ...
            <AND>
                ...

"""

import acm
import csv

from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import Mandate, GetAllMandateLimitOids


OP_NODE = {0: 'AND', 1: 'OR'}
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}
ENABLE_DEBUGGING = False
SANDBOX = False


def StartRunScript(eii):
    del eii
    acm.RunModuleWithParameters("GenericMandatesRunScriptExportMandate", acm.GetDefaultContext())


def __GetAllMandateLimitNames():
    """
    Function to retrieve the names of all the mandates stored in the database.
    :return: FArray
    """
    mandateNames = acm.FArray()
    limitOids = GetAllMandateLimitOids()
    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]
        if limit:
            mandateNames.Add(limit.Name())
    return mandateNames


def __Spacer(depth):
    return "    " * depth


ael_variables = [
    ['Mandates', 'Select Mandate', 'string', __GetAllMandateLimitNames(), None, 1, 0, 'Choose Query Folder', None, 1],
    ["ExportPath", "Export File Location", "string", None, "Y:\\Jhb\\Supervision\\Trader Mandates\\Trader Mandate Exceptions 2018\\Mandate\\", 1, 0, "If true, a violation/will be created for a breach"]]


def ael_main(ael_variables):
    mandateName = ael_variables['Mandates']
    
    limit = acm.FLimit[mandateName]
    mandate = Mandate(limit)

    path = ael_variables['ExportPath']
    path = "%s%s.csv" % (path, mandate.Entity().replace(' ', '_'))
    
    
    getLogger().info('Mandates Export script starting')

    with open(path, 'wb') as csvfile:
        fileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        row = ['Mandate Name', mandate.Name()]
        fileWriter.writerow(row)
        row = ['Mandated Entity', mandate.Entity()]
        fileWriter.writerow(row)
        row = ['Export Date', '%s' % acm.DateToday()]
        fileWriter.writerow(row)
        fileWriter.writerow([])
        row = ['Product Supervisors']
        fileWriter.writerow(row)
        row = [] + mandate.GetProductSupervisor()
        fileWriter.writerow(row)
        fileWriter.writerow([])
        row = ['Mandated Users / Traders']
        fileWriter.writerow(row)
        row = ["%s (%s)" % (user.FullName(), user.Name()) for user in mandate.GetMandatedUsers()]
        fileWriter.writerow(row)
        fileWriter.writerow([])

        entity = mandate.Entity()

        # Write column headings to CSV file
        row = ['Mandate Name', 'Mandated Entity', 'Instrument', 'Underlying Instrument', 'Currency']
        fileWriter.writerow(row)

        folders = mandate.QueryFoldersObj()

        # Loop through all the Query Folders linked to the mandate
        for folder in folders:
            text = []
            criteria = []
            groupNo = 0
            counter = 0
            insType = []
            undInsType = []
            curr = []
            
            ruleGroups = {}

            # Create data structure containing query folder parameters
            nodes = folder.Query()
            for node in folder.Query().AsqlNodes():
                AddNode(node, criteria, groupNo)
                groupNo += 1

            # Print data structure to CSV file
            for line in criteria:
                getLogger().info(line)
                
                groupNo = line[0]
                if groupNo not in ruleGroups.keys():
                    ruleGroups[groupNo] = {'insType': [], 'undInsType': [], 'curr': []}
            
                if line[1] == "Instrument.InsType":
                    ruleGroups[groupNo]['insType'].append("%s" % line[3])
                elif line[1] == "Instrument.Underlying.InsType":
                    ruleGroups[groupNo]['undInsType'].append("%s" % line[3])
                elif line[1] == "Instrument.Currency.Name":
                    ruleGroups[groupNo]['curr'].append("%s" % line[3])

                
            for key in ruleGroups.keys():
                ruleGroup = ruleGroups[key]
                getLogger().info(ruleGroup)
                if ruleGroup['undInsType']:
                    for ins in ruleGroup['insType']:
                        for underlying in ruleGroup['undInsType']:
                            for currency in ruleGroup['curr']:
                                row = ['%s' % mandateName, '%s' % entity, '%s' % ins, '%s' % underlying, '%s' % currency]
                                fileWriter.writerow(row)
                else:
                    for ins in ruleGroup['insType']:
                        for currency in ruleGroup['curr']:
                            row = ['%s' % mandateName, '%s' % entity, '%s' % ins, None, '%s' % currency]
                            fileWriter.writerow(row)
                            
            getLogger().info(ruleGroups)
    getLogger().info('Mandates EOD script completed.')
    
    # Required for RTB 
    acm.Log("Wrote secondary output to {0}".format(path))
    acm.Log("Completed successfully")



def AddNode(nodes, content, groupNo):
    """
    Add a node to the tree view.
    :param nodes: FASQLAttr / FASQLOperator
    :param tree:
    :param trade: FTrade
    """
    if 'AsqlNodes' in dir(nodes):
        for node in nodes.AsqlNodes():
            if type(nodes) is type(acm.FArray()):
                # FArray of asqlNodes
                for n in node:
                    AddNode(n, content, groupNo)

            elif 'AsqlNodes' in dir(node):
                groupNo += 1
                for n in node.AsqlNodes():
                    AddNode(n, content, groupNo)
            else:
                content.append([groupNo, 
                                "%s" % node.AsqlAttribute().AttributeString(), 
                                "%s" % ATTR_NODE[node.AsqlOperator()], 
                                "%s" % node.AsqlValue()])
    else:
        node = nodes
        groupNo += 1
        
        # Attribute Nodes
        content.append([groupNo, 
                        "%s" % node.AsqlAttribute().AttributeString(), 
                        "%s" % ATTR_NODE[node.AsqlOperator()], 
                        "%s" % node.AsqlValue()])

