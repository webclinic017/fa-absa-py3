'''
Created on 8 Jul 2013

@author: conicova
Creates the xls formated report as required by Andrey Chechin.
The report contains the FA risk matrixes and additional
matrixes computed based on the FA risk matrixes.
'''
from __future__ import print_function
import acm

from RiskMatrixViewSimpleReport import RiskMatrixContainer 
import xml.etree.ElementTree as ElementTree
import StringIO

class ColDefinition(object):
    """
    Container for the column definition
    """
    def __init__(self, title, position):
        self.title = title
        self.position = position  # defines the column position in the xls file  
        
    def __str__(self):
        return ("{0}-{1}".format(self.position, self.title))
        
    def __repr__(self):
        return self.__str__()

# list of objects containing the columns definitions 

class Point(object):
    """
    Represent a point in a two dimensional space.
    Contains the necessary methods to calculate
    the xls coordinates.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_xls(self):
        """
        Returns the relative xls coordinates of the point
        """
        return 'R{0}C{1}'.format(self.y, self.x)
    
    @staticmethod
    def add(point, x, y):
        """
        Moves the provided point by the provided x and y values.
        Returns the moved point 
        """
        return Point(point.x + x, point.y + y)
    
    @staticmethod
    def get_area_xls(point, x, y):
        """
        Returns the xls representation of the area between the provided
        point and the one resulted from moving it by x and y values.
        """
        point_a = point.get_xls()
        point_b = Point.add(point, x, y).get_xls()
        return "{0}:{1}".format(point_a, point_b)
    
class XLSCell(object):
    """
    Represents a container for the specification of an xls cell.
    """
    # The supported types, similar with those from xls
    t_number = 'Number'
    t_string = 'String'
    
    # Special type, in xls is a number
    t_percent = 'Percent'
    
    def __init__(self, value, x, y, x_length, y_length, is_formula, style, value_type):
        self.value = value
        self.x = x  # horizontal
        self.y = y  # vertical
        self.x_length = x_length  # the number of vertical cells occupied by the cell
        self.y_length = y_length  # the number of horizontal cells occupied by the cell
        self.is_formula = is_formula  # set to true if contains a xls formula
        self.style = style  # the xls style of the cell
        self.value_type = value_type  # the xls type of the data

class RiskMatrixXLS(RiskMatrixContainer):
    """
    Represents an extension of the RiskMatrixContainer class
    that offers additional attributes and functions, required
    for the creation of the formated report.
    """
   
    def __init__(self, x, y, rm):
        """
        Creates a new instance and fills it using the
        provided parameters:
        x, y -  the position of the risk matrix inside the xls file
        rm - RiskMatrixContainer
        """
        self.fill(rm)
        self.point = Point(x, y)
        self.display_underlying = False
        self.display_column_title = False
        self.has_formulas = False
        self.value_type = XLSCell.t_number
        
    def get_xls_data_area(self):
        """
        Returns the xls representation of the are occupied by the
        risk matrix (without headers).
        """
        return Point.get_area_xls(self.point, len(self.data[0]) - 1, len(self.data) - 1)
        
    def print_csv(self, output):
        """
        Uses the one parameter function output, 
        to output the RiskMatrixXLS. 
        """
        output(self.point.get_xls())
        super(RiskMatrixXLS, self).print_csv(output)
        
    def get_xls_cells(self):
        """
        Return the xls cells information, which have to
        be inserted to an xls file in order to output the
        risk matrix.
        """
        result = []
        result.extend(self._get_xls_cells_v_header())
        result.extend(self._get_xml_cells_h_header())
        result.extend(self._get_xml_cells_data())
        
        return result
   
    def create_xls_cell(self, value, offset_x, offset_y
                  , x_length=1, y_length=1, is_formula=False
                  , style=None, value_type=XLSCell.t_number):
        """
        Creates a new instance of the XLSCell and fills it
        with the provided parameters.
        Sets the cell location relative to the risk matrix
        position.
        """
        p = Point.add(self.point, offset_x, offset_y)
        return XLSCell(value, p.x, p.y, x_length, y_length, is_formula, style, value_type)
        
    def _get_xls_cells_v_header(self):
        """
        Creates all the required xls cells items required for
        the representation of the risk matrix rows header.
        """
        result = []
        
        if self.display_underlying:
            # will display the row header only for the first matrix 
            e = self.create_xls_cell(self.v_header_title, -2, 0
                               , y_length=len(self.v_header) - 1, value_type=XLSCell.t_string
                               , style='titleRowHeader')  
            result.append(e)
        
        for y, item in enumerate(self.v_header):
            e = self.create_xls_cell(item, -1, y)
            result.append(e)
        return result
    
    def _get_xml_cells_h_header(self):
        """
        Creates all the required xls cells items required for
        the representation of the risk matrix columns header.
        """
        result = []
        if self.display_column_title:
            e = self.create_xls_cell(self.column_id, 3, -3, value_type=XLSCell.t_string , style='columnHeader')
            result.append(e)
        
        if self.display_underlying:
            e = self.create_xls_cell(self.item, 0, -3, value_type=XLSCell.t_string, style='titleHeader')
            result.append(e)
            
        e = self.create_xls_cell(self.h_header_title, 0, -2
                           , x_length=len(self.h_header) - 1, value_type=XLSCell.t_string
                           , style='groupHeader')  
        result.append(e)
          
        for x, item in enumerate(self.h_header):
            e = self.create_xls_cell(item, x, -1)
            result.append(e)
        return result
    
    def _get_xml_cells_data(self):
        """
        Creates all the required xls cells items required
        for the representation of the risk matrix data.
        """
        result = []
        style = 'signNumber'
        if self.value_type == XLSCell.t_percent:
            style = 'signPercent'
        for y, row in enumerate(self.data):
            for x, item in enumerate(row):
                e = self.create_xls_cell(item, x, y
                                   , is_formula=self.has_formulas
                                   , style=style
                                   , value_type=XLSCell.t_number)
                result.append(e)
        return result    
    
class RiskMatrixFormattedReport(object):
    """
    Responsible for the creation of the formated xls report.
    Contains all the necessary functions and constants.
    """
    _SPACE_X = 1  # horizontal space between matrixes, added after each matrix
    _SPACE_Y = 4  # vertical space between matrixes, added after each matrix
    
    _TOP_X = 2  # the top horizontal cell for data
    _TOP_Y = 2  # the top vertical cell for the data
    
    _HEADER_X_SIZE = 1  # row header size
    _HEADER_Y_SIZE = 2  # column header size
    
    # the titles of the special columns
    _GAMMA = 'Portfolio Gamma Implicit Cash Equity'
    _THETA = 'Theta From Gamma'
    
    # computed column
    _BREAKEVEN_VOL = 'BREAKEVEN VOL'
    # computed matrixes
    _COMBINED = 'Combined'
    _CHANGES = 'Changes'
    _EQUITY_INDEX = 'EquityIndex'
    
    def __init__(self):
        self.col_defs = []
    
    def _fill_col_defs(self, columns):
        """
        Fills the column definitions using the provided
        columns list.
        Takes into account the need to add later the computed
        matrixes, by setting the correct position.
        """
    
        start_position = 3  # it is necessary to display the BREAKEVEN VOL as the third matrix
        for col in columns:
            if col == self._GAMMA:
                position = 1
            elif col == self._THETA:
                position = 2
            else:
                start_position += 1
                position = start_position
            self.col_defs.append(ColDefinition(col, position))
    
    @classmethod
    def _cmp_ins_type(cls, x, y):
        x_type = acm.FInstrument[x].InsType()
        y_type = acm.FInstrument[y].InsType()
        if cls._EQUITY_INDEX not in (x_type, y_type) or x_type == y_type:
             return cmp(x, y)
         
        if x_type == cls._EQUITY_INDEX:
            return -1
        if y_type == cls._EQUITY_INDEX:
            return 1
    
    @staticmethod
    def _get_matrix(und_t=None, col_t=None, risk_matrixes=None):
        """
        Returns the risk matrix with the specified 
        underlying title and column title.
        """
        if und_t and col_t:
            filter_func = lambda x: x.item == und_t and x.column_id == col_t
        else:
            if und_t:
                filter_func = lambda x: x.item == und_t
            if col_t:
                filter_func = lambda x: x.column_id == col_t
            if not (und_t or col_t):
                print('{0}-{1}'.format(und_t, col_t)) 
                raise Exception('Have to specify at least the underlying or the column title')
        return filter(filter_func, risk_matrixes)[0]
    
    # matrix title that have a special position (begin or end)
    _ordering = {
            'ZAR/ALSI': 5,
            'ZAR/SWIX': 4,
            _COMBINED: 2,
            _CHANGES: 1
        }
    @classmethod
    def _cmp_zar(cls, x, y):
        """
        A special comparer in order to have the ZAR/ALSI and ZAR/SWIX
        as the first two matrixes.
        The _COMBINED and _CHANGES matrixes have to be the last two matrixes.
        """
        order_x = cls._ordering.get(x, 3)
        order_y = cls._ordering.get(y, 3)
        if order_x == order_y:
            return -1 * cls._cmp_ins_type(x, y)
        return cmp(order_x, order_y)
    
    @classmethod
    def _set_xy_matrix(self, underlying, column, x, y
                       , len_x, _header_x_size, _space_x
                       , risk_matrixes
                       , indexed_rm
                       , display_column_title
                       ):
        """
        Adds a new RiskMatrixXLS to the indexed_rm list.
        Returns the next x coordinate and the new risk matrix.
        """
        base_rm = self._get_matrix(underlying, column, risk_matrixes) 
        new_rm = RiskMatrixXLS(x + _header_x_size, y, base_rm)
        new_rm.display_column_title = display_column_title
        
        indexed_rm.append(new_rm)
        x += _header_x_size + len_x + _space_x
        
        return (x, new_rm)
    
    @staticmethod
    def _set_matrix_attr(new_rm
                         , display_u_title
                         , has_formulas
                         , value_type):
        """
        Initialises the attributes of provided 
        risk matrix with the provided parameters.
        """
        new_rm.display_underlying = display_u_title
        new_rm.has_formulas = has_formulas
        new_rm.value_type = value_type
        
        return new_rm
    
    def _set_xy_matrixes(self, risk_matrixes):
        """
        Creates a new list of RiskMatrixXLS objects.
        Adds the computed matrixes and sets the location of
        the top left corner of data (without headers) 
        for each matrix. 
        """
        
        underlyings = list(set([rm.item for rm in risk_matrixes]))
        
        underlyings.sort(self._cmp_zar, None, True)  # want the ZAR to be at the beginning
        indexed_rm = []
        matrix_len_x = len(risk_matrixes[0].data[0])
        matrix_len_y = len(risk_matrixes[0].data)
        
        self.col_defs.sort(key=lambda x: x.position)
       
        y_special_space = 0
        for yj, u in enumerate(underlyings):
            display_column_title = False
            has_formulas = False
            if u == self._CHANGES or u == self._COMBINED:
                has_formulas = True
            if yj == 0:
                display_column_title = True
            if u == self._CHANGES:
                y_special_space += 2  # will add two additional rows for combobox 
            y = yj * (matrix_len_y + self._SPACE_Y) + self._TOP_Y + self._HEADER_Y_SIZE + y_special_space
            x = self._TOP_X
            # have to move the x index after each matrix
            # have to move y index after each underlying
            set_xy_matrix = lambda column: self._set_xy_matrix(
                                                            u, column, x, y,
                                                            matrix_len_x,
                                                            self._HEADER_X_SIZE,
                                                            self._SPACE_X,
                                                            risk_matrixes,
                                                            indexed_rm,
                                                            display_column_title)
            for xj, col_def in enumerate(self.col_defs):
                display_u_title = False
                if xj == 0:
                    display_u_title = True
                (x, new_rm) = set_xy_matrix(col_def.title)
                self._set_matrix_attr(new_rm, display_u_title, has_formulas, value_type=XLSCell.t_number)
                # have to insert the BREAKEVEN VOL after the _THETA,
                # which is not in the list of columns
                if col_def.title == self._THETA:
                    (x, new_rm) = set_xy_matrix(self._BREAKEVEN_VOL)
                    self._set_matrix_attr(new_rm, display_u_title=False, has_formulas=True, value_type=XLSCell.t_percent)
                    
            # iterate to next matrix with a different underlying 
            x = 0
        
        return indexed_rm
    
    @staticmethod
    def _gen_template_matrix(col_title, template_title, matrix):
        """
        Generates a new RiskMatrixContainer with the specified
        column_id and title. Fills the v_header and h_header
        based on the specified matrix.
        Returns the new generated object.
        """
        t_matrix = RiskMatrixContainer(col_title, template_title)
        t_matrix.set_h_header(matrix.h_header_title, matrix.h_header)
        t_matrix.set_v_header(matrix.v_header_title, matrix.v_header)
        
        return t_matrix
    
    def _gen_template_matrixes(self, risk_matrixes):
        """
        Adds the computed matrixes to the list 
        of existing matrixes.
        """
        rm = risk_matrixes[0]
        append_f = lambda col_title, template_title: risk_matrixes.append(
                        self._gen_template_matrix(col_title, template_title, rm))
                   
        # insert _COMBINED as an underlying
        for col in self.col_defs:
            append_f(col.title, self._COMBINED)
        # insert _CHANGES as an underlying
        for col in self.col_defs:
            append_f(col.title, self._CHANGES)
        
        # have to create an empty matrix for the BREAKEVEN VOL
        underlyings = set([rm.item for rm in risk_matrixes])
        for u in underlyings:
            # have to create an empty matrix for the BREAKEVEN VOL
            append_f(self._BREAKEVEN_VOL, u)
        
        return risk_matrixes
    
    @staticmethod        
    def _calc_breakeven_vol(point_gamma, point_theta, x, y):
        """
        Computes the formula that has to be used in the
        BREAKEVEN VOL matrix cell. This is computed based 
        on the location of the _GAMMA and _THETA matrixes
        and the relative position of the cell.
        """
        
        xls_gamma = Point.add(point_gamma, x, y).get_xls()
        xls_theta = Point.add(point_theta, x, y).get_xls()
        
        result = ('=IF(AND({0}>0,{1}>0),'
                  '"FREE",'
                  '(({1}*365/252)/(-100*0.5*{0}))^0.5'
                  '*IF({0}<0,-1,1)*(252^0.5))').format(xls_gamma, xls_theta)
        return result
    
    @classmethod
    def _fill_breakeven_vol(self, underlying, rm_row):  
        """
        Fills the BREAKEVEN VOL matrix with data (formulas)
        """
                
        # have to select the Gamma and Theta risk matrixes, and calculate
        # the breakeven vol
        gamma_matrix = self._get_matrix(None, self._GAMMA, rm_row)
        theta_matrix = self._get_matrix(None, self._THETA, rm_row) 
        b_vol_matrix = self._get_matrix(None, self._BREAKEVEN_VOL, rm_row) 
       
        # for the Changes there is no BREAKEVEN VOL
        if underlying == self._CHANGES:
            return b_vol_matrix
        
        b_vol_calc_f = lambda x, y: self._calc_breakeven_vol(gamma_matrix.point,
                                               theta_matrix.point, x, y)
        data = []
        for y, row_d in enumerate(gamma_matrix.data):
            row = []
            for x in range(len(row_d)):
                row.append(b_vol_calc_f(x, y))
            data.append(row)
        b_vol_matrix.set_data(data)
        
        return b_vol_matrix
    
    @staticmethod
    def _sum(x, y, rm_list):
        """
        Computes the formula that will sum the cells from
        each matrix that a relative to the location of each 
        matrix.
        """
        result = '='  # =B5+B29+B53+B77+B102
        
        for rm in rm_list:
            xls_rm = Point.add(rm.point, x, y).get_xls()
            result = '{0}{1}+'.format(result, xls_rm)
        result = result[0:-1]
        return result
    
    @classmethod
    def _fill_combined_matrix(cls, rm_col):
        """
        Fills the COMBINED matrix with data.
        The rm_col contains all the formated risk matrixes
        in a xls 'column'. 
        """
        rm_col_u = filter(lambda x: x.item not in (cls._COMBINED, cls._CHANGES), rm_col)
        
        first_matrix = rm_col_u[0]
        data = []
        for y, row_d in enumerate(first_matrix.data):
            row = []
            for x in range(len(row_d)):
                row.append(cls._sum(x, y, rm_col_u)) 
            data.append(row)
        rm_combined = filter(lambda x: x.item == cls._COMBINED, rm_col)[0]
        rm_combined.set_data(data)
        
        return rm_combined
    
    @classmethod
    def _fill_changes_matrix(cls, rm_col, point_x1, point_x2):
        """
        Fills the CHNAGES matrix with data.
        The rm_col contains all the formated risk matrixes
        in a xls 'column'.
        """
        result = '={0}-INDEX({1},{2},{3})'
        underlying = cls._COMBINED
        rm_u = cls._get_matrix(underlying, None, rm_col)
        
        data = []
        for y, row_d in enumerate(rm_u.data):
            row = []
            for x in range(len(row_d)):
                cell = Point.add(rm_u.point, x, y).get_xls()
                row.append(result.format(cell
                                         , rm_u.get_xls_data_area()
                                         , point_x1.get_xls()
                                         , point_x2.get_xls()
                                         )) 
            data.append(row)
        
        rm_changes = cls._get_matrix(cls._CHANGES, None, rm_col)
        rm_changes.set_data(data)
        
        return rm_changes
    
    def get_formated_risk_matrixes(self, risk_matrixes, columns):
        """
        Returns a list of formated risk matrixes and 
        additional computed matrixes.
        The matrixes contain the information required to
        correctly position them inside a xls file.
        The matrixes that contain formulas are computed
        relative to the position of the other matrixes.
        (relative only at the moment of computation)
        """
        self._fill_col_defs(columns)
        
        rm = self._gen_template_matrixes(risk_matrixes)
        formated_rm = self._set_xy_matrixes(rm)
       
        # have to fill the COMBINED and CHANGES
        # will group by column
        risk_matrixes_col = {}
        
        for risk_matrix in formated_rm:
            if not risk_matrixes_col.has_key(risk_matrix.column_id):
                risk_matrixes_col[risk_matrix.column_id] = []
            risk_matrixes_col[risk_matrix.column_id].append(risk_matrix)
        
        rm_changes_gamma = self._get_matrix(self._CHANGES, self._GAMMA, formated_rm)
        point_x1 = Point.add(rm_changes_gamma.point, 1, -4) 
        point_x2 = Point.add(rm_changes_gamma.point, 3, -4)
        
        for col in risk_matrixes_col.keys():
            rm_col = risk_matrixes_col[col]
            self._fill_combined_matrix(rm_col)
            self._fill_changes_matrix(rm_col, point_x1, point_x2)
        # finished COMBINED and CAHANGES
        
        
        # have to fill the BREAKEVEN VOL
        risk_matrixes_rows = {}
        # will group by underlying
        for risk_matrix in formated_rm:
            if not risk_matrixes_rows.has_key(risk_matrix.item):
                risk_matrixes_rows[risk_matrix.item] = []
            risk_matrixes_rows[risk_matrix.item].append(risk_matrix)
        
        for underlying in risk_matrixes_rows.keys():
            rm_under = risk_matrixes_rows[underlying]
            self._fill_breakeven_vol(underlying, rm_under)
        # finished BREAKEVEN VOL
        
        return formated_rm
   
    @classmethod
    def _get_xml_cells_other(cls, formated_risk_matrixes):
        """
        Creates all the required xls cells items required
        for the representation of the report additional information.
        """
        result = [] 
        
        rm = cls._get_matrix(cls._CHANGES, cls._GAMMA, formated_risk_matrixes)
         
        e = rm.create_xls_cell("REF", -1, -4, value_type=XLSCell.t_string, style="styleRef")
        result.append(e)
        
        e = rm.create_xls_cell("Vertical", 0, -5, value_type=XLSCell.t_string)
        result.append(e)
        e = rm.create_xls_cell(0, 0, -4, value_type=XLSCell.t_number, style="styleYellow")
        result.append(e)
        
        point_vertical = Point.add(rm.point, 0, -4).get_xls()
        area_vertical = Point.get_area_xls(
                                           Point.add(rm.point, -1, 0),
                                           0, len(rm.v_header) - 1)
        
        value = '=MATCH({0},{1},1)'.format(point_vertical, area_vertical)
        e = rm.create_xls_cell(value, 1, -4, value_type=XLSCell.t_number, is_formula=True, style="styleGray")
        result.append(e)
        
        e = rm.create_xls_cell("Horizontal", 2, -5, value_type=XLSCell.t_string)
        result.append(e)
        e = rm.create_xls_cell(0, 2, -4, value_type=XLSCell.t_number, style="styleYellow")
        result.append(e)
        
        point_horizontal = Point.add(rm.point, 2, -4).get_xls()
        area_horizontal = Point.get_area_xls(
                                           Point.add(rm.point, 0, -1),
                                           len(rm.h_header) - 1, 0)
        value = '=MATCH({0},{1},1)'.format(point_horizontal, area_horizontal)
        e = rm.create_xls_cell(value, 3, -4, value_type=XLSCell.t_number, is_formula=True, style="styleGray")
        result.append(e)
        
        return result 
    
    @classmethod
    def get_xml_formated_risk_matrixes(cls, formated_risk_matrixes):
        """
        Returns the string representation of the xml that contains
        the information about the cells of the formated report.
        Uses the provided list of formated risk matrixes, to create
        the xml.
        """
        parent = ElementTree.Element("Report")
        
        cells_items = []
        for rm in formated_risk_matrixes:
            if rm.item != cls._CHANGES or rm.column_id != cls._BREAKEVEN_VOL:
                elements = rm.get_xls_cells()
                for e in elements:
                    cells_items.append(e)
        
        # have to add some additional xls content
        cells_items.extend(cls._get_xml_cells_other(formated_risk_matrixes))
        
        cells_items.sort(key=lambda x: x.y)
        
        y_values = list(set([item.y for item in cells_items]))
        y_values.sort()
        
        for y in y_values:
            cells_by_y = filter(lambda item: item.y == y, cells_items)
            cells_by_y.sort(key=lambda item: item.x)
            row_e = ElementTree.SubElement(parent, "row")
            row_e.set("index", str(y))
            for item in cells_by_y:
                cell_e = ElementTree.SubElement(row_e, "cell")
                cell_e.set("index", str(item.x))
                cell_e.set("isFormula", str(item.is_formula))
                cell_e.set("yLength", str(item.y_length))
                cell_e.set("xLength", str(item.x_length))
                cell_e.set("style", str(item.style))
                cell_e.set("valueType", str(item.value_type))
                cell_e.text = item.value
                
        xml_tree = ElementTree.ElementTree(parent)
        encoding = 'ISO-8859-1'
        strio = StringIO.StringIO()
        xml_tree.write(strio, encoding=encoding)
        result = strio.getvalue()
        strio.close()
        
        return result

# uses a specific xslt template

