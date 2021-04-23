import acm
import csv


OP_NODE = {0: 'AND', 1: 'OR'}
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}


qf = acm.FStoredASQLQuery["Mandate/BAGL_EMEA_Comm"]
nodes = qf.Query()


def _Spacer(depth):
    return "    " * depth


def PrintNode(nodes, depth, text, criteria):
    if 'AsqlNodes' in dir(nodes):
        for node in nodes.AsqlNodes():
            if type(nodes) is type(acm.FArray()):
                for n in node:
                    PrintNode(n, depth, text)

            elif 'AsqlNodes' in dir(node):
                if len(node.AsqlNodes()) > 1:
                    text.append("%s[%s]" % (_Spacer(depth), OP_NODE[node.AsqlOperator()]))
                    depth += 1
                    criteria.append({'Instrument.InsType': [],
                                     'Instrument.Currency.Name': [],
                                     'Instrument.Underlying.InsType' : []})
                for n in node.AsqlNodes():
                    PrintNode(n, depth, text, criteria)
            else:
                #print '----', '%s' % node.AsqlAttribute().AttributeString()
                #print depth
                #print criteria

                criteria[depth - 1]['%s' % node.AsqlAttribute().AttributeString()].append('%s' % node.AsqlValue())
                text.append("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                                  ATTR_NODE[node.AsqlOperator()],
                                                  node.AsqlValue()))

    else:
        #print '----', '%s' % nodes.AsqlAttribute().AttributeString()
        #criteria['%s' % nodes.AsqlAttribute().AttributeString()].append('%s' % nodes.AsqlValue())

        text.append("%s%s %s %s" % (_Spacer(depth), nodes.AsqlAttribute().AttributeString(),
                                ATTR_NODE[nodes.AsqlOperator()], nodes.AsqlValue()))
        return text, criteria

text = []
criteria = {'Instrument.InsType': [],
            'Instrument.Currency.Name': [],
            'Instrument.Underlying.InsType' : []}
criteria = []

PrintNode(nodes, 0, text, criteria)


with open('C:\Temp\Mandates.csv', 'wb') as csvfile:
    fileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    for line in criteria:
        print('-' *60)
        print(line)

        instruments = line['Instrument.InsType']
        underlyings = line['Instrument.Underlying.InsType']
        currencies = line['Instrument.Currency.Name']

        for instrument in instruments:
            if underlyings:
                for underlying in underlyings:
                    for currency in currencies:
                        print('%s %s %s' % (instrument, underlying, currency))
                        row = ['%s' % instrument, '%s' % underlying, '%s' % currency]
                        fileWriter.writerow(row)
            else:
                for currency in currencies:
                    print('%s %s %s' % (instrument, None, currency))
                    row = ['%s' % instrument, None, '%s' % currency]
                    fileWriter.writerow(row)


print('Done')
