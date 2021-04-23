
from __future__ import print_function
import acm
import FUxCore
from FAFOUtils import get_currPair_price

calc_space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

def get_fwd_points(curve_obj, curr_pair, price_market):
    
    fwd_points_res = []
    points = curve_obj.Points()
    from_curr = curr_pair.Currency1()
    to_curr = curr_pair.Currency2()
    current_spot =  get_currPair_price(curr_pair, price_market)
    tenors = [p.Name() for p in points]
    for period in tenors:
        if period == '1d':
            fwd_date = curr_pair.ForwardDate(acm.Time.DateToday(), '-1d')
        else:
            fwd_date = curr_pair.ForwardDate(acm.Time.DateToday(), period)
        forward_rate = from_curr.Calculation().FXRate(calc_space, to_curr, fwd_date).Number()
        if forward_rate <> None:
            fwd_points = (forward_rate - current_spot)*10000
            fwd_points_res.append([period, fwd_date, round(fwd_points, 2)])
    return fwd_points_res

def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddOption('curr_pair', 'Currency Pair' )
    b.AddOption('curve', 'Curve')
    b.AddButton('ok', 'OK')
    b.AddGrid('grid', 300, 350)
    b.EndBox()
    return b
        
def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    customDlg = myCustomDialog()
    builder = CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, customDlg )
    
class myCustomDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okBtn = 0
        self.m_curr_pairs = 0
        
    def HandleApply( self ):
        return None

    def PopulateData(self):
        curr_pairs = acm.FCurrencyPair.Select('')
        self.m_curr_pair.Populate(curr_pairs)
        curves = acm.FYieldCurve.Select('')
        self.m_curve.Populate(curves)
        
        self.tenor_column = self.m_grid.AddColumn("Tenor", 80)
        self.date_column = self.m_grid.AddColumn("Date", 80)
        self.point_column = self.m_grid.AddColumn("Point", 100)
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Forward Points')
        self.m_okBtn = layout.GetControl("ok")
        self.m_curr_pair = layout.GetControl("curr_pair")
        self.m_curve = layout.GetControl("curve")
        self.m_grid = layout.GetControl('grid')
        
        self.m_grid.ShowRowHeaders(False)
        self.m_grid.ShowColumnHeaders(True)
        self.m_grid.SetEnterKeyMove(True, 'Right')
        self.m_grid.SetCellBorderStyle('Horizontal')
        self.m_grid.TabDirection(True)
        
        self.m_ok = layout.GetControl('ok')
        self.m_ok.AddCallback('Activate', self.OnOk, self.m_grid)
        self.PopulateData()
        
    def OnOk(self, grid, cd):
        grid.RemoveAllItems()
        curr_pair = self.m_curr_pair.GetData()
        curve = self.m_curve.GetData()
        price_market = 'SPOT'
        if curr_pair == None and curve == None:
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 'Question', 'Choose currency pair and curve!')
            return
        elif curr_pair == None:
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 'Question', 'Choose currency pair!')
            return
        elif curve == None:
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 'Question', 'Choose curve!')
            return
        table_info = get_fwd_points(curve, curr_pair, price_market)
        table_info.sort(key=lambda x: x[1])
        self.DrawTable(table_info)
        
    def DrawTable(self, table_info):
        for data in table_info:
            self.CreateRow(self.m_grid, self.m_grid.GetRootItem(), data)
        
    def CreateRow(self, grid, parent, data):
        row = parent.AddChild()
        colIter = grid.GridColumnIterator()
        i = 0
        while colIter.Next():
            cell = row.GetCell(colIter.GridColumn())
            cell.SetData(data[i])
            i += 1
        return row
        
