""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAPFE_Dialog.py"
from __future__ import print_function
import acm
import FUxCore
import FUxNet
#need to import the clr module in order to use .Net stuff
import clr
import FBDPCommon
import FBDPChartDisplay
import FBDPChartData


clr.AddReference("System.Windows.Forms.DataVisualization")

def ReallyStartDialog(shell, count):
    customDlg = AAPFEDialog()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )

def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartDialog(shell, 0);

    
class AAPFEDialog (FUxCore.LayoutDialog):
    def __init__(self, pfeResults, afterPFEResults):
        self.m_chart = 0
        self.m_pfeResults = pfeResults
        self.m_afterPFEResults = afterPFEResults
        self.m_ResultUnit = pfeResults[0].Unit() if pfeResults else None
        
    def Display( self ):
        try:
        
            pfeDateList = [pfe.DateTime().replace("00:00:00", "") for pfe in self.m_pfeResults]
            pfeList = [pfe.Number() for pfe in self.m_pfeResults]
            
            afterPFEDateList = [pfe.DateTime().replace("00:00:00", "") for pfe in self.m_afterPFEResults]
            afterPFEList = [pfe.Number() for pfe in self.m_afterPFEResults]
            
            s1 = FBDPChartData.seriesData(name='PFE', color=FBDPChartData._FCOLOR_BLACK, xList=pfeDateList, yList=pfeList)
            s2 = FBDPChartData.seriesData(name='After PFE', color=FBDPChartData._FCOLOR_RED, xList=afterPFEDateList, yList=afterPFEList)
            self.m_currentResults = [s1, s2]
            self.Draw()

        except Exception as err:
            print('Exception: ', err)
            
        return None

    def Draw(self):

        XAxisLabel = 'Valuation Date'
        YAxisLabel = 'PFE (' + self.m_ResultUnit + ')'  
        subTitle =  '' 
        viewLabel = 'PFE Projections'
        chartType = FBDPChartData.CHART_TYPE_STEPLINE
        uiData = FBDPChartData.UIData(seriesList=self.m_currentResults,
                XAxisLabel=XAxisLabel,
                YAxisLabel=YAxisLabel,
                subTitle=subTitle, chartType=FBDPChartData.CHART_TYPE_STEPLINE, 
                viewLabel=viewLabel)
        self.m_chart.display(uiData)
        
    def __CalculatePFEs(self, trade):
    
        self.m_currentCBInst = trade.CreditBalance()
        if not self.m_currentCBInst:
            return [], []
            
        cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext (), 'FPortfolioSheet')
        topnode = cs.InsertItem(self.m_currentCBInst)
        calc = cs.CreateCalculation(topnode, 'PFE Results')
        pfeResults = calc.Value()
        
        topnode = cs.InsertItem(trade)
        calc = cs.CreateCalculation(topnode, 'PFE Results With Incremental Trade')
        pfeAfterResults = calc.Value()
        
        return pfeResults,  pfeAfterResults

        
    def HandleCreate( self, dlg, layout):
        
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('PFE projection')
        self.m_chart = FBDPChartDisplay.Display2DChart(layout.GetControl('chart2d'))
        self.m_chart.setup()
        self.Display()
    
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.  BeginVertBox('None')
        b.Add2DChart('chart2d', 900, 800)
        b.  EndBox()
        return b
