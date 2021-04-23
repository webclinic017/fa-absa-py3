'''----------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Phumzile Mgcima
CR Number: 883716 (Initial Deployment)
----------------------------------------------------------------------'''


import copy
import PS_XMLReportingTools

from xml.etree import ElementTree as ET
from decimal import Decimal
from zak_funcs import formnum

'''
This module splits rows entries that are arrays into multiple lines in the resulting xml.
_indices represents the index of each column that contains an array,
'''

# preprocessing hook
def PreProcessXML(reportObj, param, xml,_indices):
    
    xmltree = ET.fromstring(xml)
    rowselement = xmltree.find('.//Table/Rows/Row/Rows')
    
    # here is the magic
    expand_rows(rowselement, _indices)        
    
    xml = ET.tostring(xmltree)
    #xml = PS_XMLReportingTools.PreProcessXML(reportObj, param, xml) # call the original preprocessing
    xml = PS_XMLReportingTools.PreProcessXML(reportObj, param, xml)
    return xml


def expand_rows(rowselement, cell_indices):
    """Expand all rows under rowselement by values specified by column indices."""
    rows = rowselement.findall('Row')
    for row in rows:
        # keep original order -- will add the row later again. etree does not support insertafter/before :P
        # so we basically recreate all rows

        formatted_replacements = get_replvals(row, cell_indices, 'FormattedData')
        raw_replacements = get_replvals(row, cell_indices, 'RawData')
        assert len(formatted_replacements) == len(
                raw_replacements), "Inconsistency between Raw and Formatted Data"

        #  [[r0c0, r0c1, r0c2], [r1c0, r1c1, c1c2], ...]
        if formatted_replacements:
            for formatted_replacement, raw_replacement in zip(
                    formatted_replacements, raw_replacements):
                # we make a deep copy of the subtree and replace the values
                newrow = copy.deepcopy(row)
                newcells = newrow.findall('Cells/Cell')
                for (arrindex, cellindex) in enumerate(cell_indices):
                    #ensure we dont pass ('',) which leads to index exception
                    if formatted_replacement[0]!='':
                        try:
                            #NumberFormat exception might be thrown.
                            formatted_val = formnum(Decimal(formatted_replacement[arrindex]))
                        except:
                            formatted_val = formatted_replacement[arrindex]
                        try:
                            #NumberFormat exception might be thrown.
                            raw_val = formnum(Decimal(raw_replacement[arrindex]))
                        except:
                            raw_val = raw_replacement[arrindex]
                        newcells[cellindex].find('FormattedData').text = formatted_val
                        newcells[cellindex].find('RawData').text = raw_val
                        
                rowselement.append(newrow)
        else:
            rowselement.append(row)

        #recursion going through the grouping levels.
        expand_rows(rowselement.find('./Row/Rows'), cell_indices)
        rowselement.remove(row)

            
def get_replvals(row, indices, data_format):
    """Return an array (rows) of arrays (cell values) of replacement values for the specified row."""
    cells = row.findall('Cells/Cell')
           
    fdVals = [ cells[index].find(data_format).text[1:-1].split(', ') for index in indices
    
        if cells[index].find(data_format).text and cells[index].find(data_format).text.startswith('[') ]
    
    return list(zip(*fdVals))
