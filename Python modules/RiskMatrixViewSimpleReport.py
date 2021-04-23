'''
Created on 18 Jul 2013

@author: conicova
'''

import acm
import WBXMLReport
from zak_funcs import formnum

class RiskMatrixContainer(object):
    """ 
    This is a container for a Risk Matrix. 
    Offers the methods necessary to convert the Risk Matrix
    into a CSV or XML Representation. 
    """ 
    def __init__(self, column_id, item):
        self.column_id = column_id
        self.item = item
        self.h_header = []
        self.v_header = []
        self.data = [[]]
    
    def fill(self, rm_container):
        self.column_id = rm_container.column_id
        self.item = rm_container.item
        self.set_h_header(rm_container.h_header_title, rm_container.h_header)
        self.set_v_header(rm_container.v_header_title, rm_container.v_header)
        self.set_data(rm_container.data)
    
    def set_h_header(self, title, items):
        """ 
        Set the title and the values of the horizontal vector 
        """ 
        self.h_header = items
        self.h_header_title = title

    def set_v_header(self, title, items):
        """ 
        Set the title and the values of the vertical vector 
        """ 
        self.v_header = items
        self.v_header_title = title

    def set_data(self, items):
        """ 
        Set the values of the risk matrix. The items has to be a 
        two dimensional list
        """ 
        self.data = items

    def print_csv(self, output):
        """  
        Prints the csv representation of the Risk Matrix.
        The output parameter is a function that takes one parameter.
        """ 
        output('Item:{0}'.format(self.item))
        output('Column Id:{0}'.format(self.column_id))
        output('{0};{1}'.format(self.h_header_title, ';'.join(self.h_header)))
        for i, row in enumerate(self.data):
            temp = [self.v_header[i]]
            temp.extend(row)
            output(';'.join(temp))
    
    def get_fprimetable(self):
        """ 
        Returns a PrimeTable instance filled with data from this 
        container.
        """ 
        columns = []
        for i, label in enumerate(self.h_header):
            column_id = "c_id_{0}".format(i)
            column_unique_id = "c_id_{0}_u".format(i)
            context = "Standard"
            prime_column = WBXMLReport.PrimeColumn(
                label, self.h_header_title, column_id,
                column_unique_id, context)
            columns.append(prime_column)
        
        rows = []
        for i, row in enumerate(self.data):
            cells = []
            for cell in row:
                cells.append(WBXMLReport.PrimeCell(cell, cell, formnum(float(cell))))
            row_label = self.v_header[i]
            row_id = "r_id_{0}".format(i)
            rows.append(WBXMLReport.PrimeRow(row_label, row_id=row_id, cells=cells))
        
        name = "{0}, {1}".format(self.column_id, self.item)
        
        return WBXMLReport.PrimeTable(name, "MatrixView", columns, rows)
    
class FScenarioUtil(object):
    """ 
    Contains methods that are related to FStoredScenario.
    """ 
    def __init__(self, title):
        """ 
        Sets the scenario attribute to the front arena instance 
        of the FStoredScenario type with the corresponding title
        """ 
        ss = acm.FStoredScenario.Select("name='{0}'".format(title))
        if len(ss) != 1:
            raise ValueError("Could not find the specified scenario.")
        self.scenario = ss[0].Scenario()
    
    def get_scenario_vector_as_list(self, vector_nr):
        """  
        Returns the tuple (title, values) with the vector title
        and the vector items values
        """ 
        scen_dim = self.scenario.ExplicitDimensions()[vector_nr]
        sel_value = lambda x: str(x.Parameter('rs'))
        vec = scen_dim.ShiftVectors()[0]
        values = map(sel_value, vec.AsList())
        # could not fine a better way to extract the vector title
        vec_val_str = vec.AsString()[1:-1]
        title = (vec.StringKey()[0:len(vec.StringKey()) - len(vec_val_str) - 2]).strip()
        return (title, values)

class RiskMatrixGen(object):
    """ 
    This class contains the required methods to generate
    a Risk Matrixes.
    The Risk Matrix is generated for one cell that may be defined
    by an underlying and a column title. 
    In order to generate the Risk Matrix it is necessary to specify
    a scenario. It is expected that the scenario will be two dimensional.
    """ 
    @staticmethod
    def _get_col_conf_scenario(scenario):
        column_config = acm.Sheet.Column().ConfigurationFromScenario(scenario)
        return column_config
    
    @staticmethod
    def _get_chained_grouper(GROUPER_NAMES):
        groupers = map(acm.Risk().GetGrouperFromName, GROUPER_NAMES)
        chained_grouper = acm.FChainedGrouper(groupers)
        return chained_grouper
    
    @classmethod
    def _get_tree_nodes(cls, top_node, level):
        """ 
        Returns all the tree nodes located 
        at the specified level (depth) from the top_node 
        """
        result = []
        child = top_node.Iterator().FirstChild()
        while child:
            if level == 0:
                result.append(child.Tree())
                sibling = child.NextSibling()
                while sibling:
                    result.append(child.Tree())
                    sibling = child.NextSibling()
            else:
                result.extend(cls._get_tree_nodes(child.Tree(), level - 1))
            child = child.NextSibling()
        return result
    
    @staticmethod
    def _get_tree_node_key(tree_node):
        return tree_node.Item().StringKey()
    
    @staticmethod
    def _get_number(x):
        if hasattr(x, "Number"):
            result = str(x.Number())
            if result == "nan":
                result = "0"
                print(("Error, the obj {0} of type {1} has a nan value. Returning zero".format(x, type(x)))) 
            return result
        else:
            print(("Error, the obj {0} of type {1} has no attribute named Number. Returning zero".format(x, type(x))))
            return "0"
    
    @staticmethod
    def _calculate(calc_space, underlying_node, column_config, column_id):
        risk_matrix = RiskMatrixContainer(column_id, RiskMatrixGen._get_tree_node_key(underlying_node))
            
        calculation = calc_space.CreateCalculation(underlying_node, column_id, column_config)
        
        result = map(lambda x: map(RiskMatrixGen._get_number, x), calculation.Value())
        risk_matrix.set_data(result)
        
        return risk_matrix

    def gen_risk_matrixes(self, sc_title, tf_title, col_ids, gr_names):
        """
        Initialises the calc_risk_matrixes list which contains items 
        of the RiskMatrixContainer type. 
        """
        context = acm.GetDefaultContext()
        sheet_type = 'FPortfolioSheet'
        tf = acm.FTradeSelection[tf_title]
        calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
        top_node = calc_space.InsertItem(tf)
        top_node.ApplyGrouper(self._get_chained_grouper(gr_names))
        calc_space.Refresh()
        scenario_u = FScenarioUtil(sc_title)
        column_config = self._get_col_conf_scenario(scenario_u.scenario)
            
        tree_nodes = self._get_tree_nodes(top_node, len(gr_names) - 1)
        # filter_instruemnts = lambda ins: True if self._get_tree_node_key(ins) == "GBP/FTSE" else False
        # tree_nodes = filter(filter_instruemnts, tree_nodes)
        print(('Number of items:{0}'.format(len(tree_nodes))))
        self.calc_risk_matrixes = []
        
        h_title, h_values = scenario_u.get_scenario_vector_as_list(0)
        v_title, v_values = scenario_u.get_scenario_vector_as_list(1)
      
        for tree_node in tree_nodes:
            for column_id in col_ids:
                print(("Computing RiskMatrix for: {0}-{1}".
                       format(self._get_tree_node_key(tree_node), column_id)))
                risk_matrix = self._calculate(calc_space, tree_node,
                    column_config, column_id)
                risk_matrix.set_h_header(h_title, h_values)
                risk_matrix.set_v_header(v_title, v_values)
                self.calc_risk_matrixes.append(risk_matrix)
