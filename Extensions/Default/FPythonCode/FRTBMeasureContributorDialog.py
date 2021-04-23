
import acm
import FUxCore

from ContributorDialog import ContributorDialog

class CheckBox( object ):
    
    def __init__(self, id, label):
        self.m_id = id
        self.m_label = label
        self.m_ctrl = None

    def HandleCreate( self, layout ):
        self.m_ctrl = layout.GetControl( self.m_id )
        self.m_ctrl.Checked( True )

    def BuildLayoutPart( self, builder ):
        builder.AddCheckbox( self.m_id, self.m_label )
        
    def SetChecked( self, checked ):
        self.m_ctrl.Checked( checked )
        
    def GetValue( self ):
        return self.m_ctrl.Checked()
        
riskClasses = \
[
["commodity", "Commodity"],
["csr_ns",  "CSR (NS)"],
["equity", "Equity"],
["fx", "FX"],
["girr", "GIRR"]
]
measureTypes = \
[
["delta", "Delta"],
["vega", "Vega"],
["curvature", "Curvature"]
]
additionals = \
[
["drc", "DRC"],
["rrao", "RRAO"]
]
    
class FRTBMeasureContributorDialog( ContributorDialog ):

    def __init__(self, params):
        ContributorDialog.__init__( self, params )
        self.m_rfSetupCtrl = None
        self.m_hierarchyCtrl = None
        
        self.m_rcCheckBoxes = []
        for rc in riskClasses:
            self.m_rcCheckBoxes.append( CheckBox( rc[0], rc[1] ) )
        
        self.m_measureCheckBoxes = []
        for measure in measureTypes:
            self.m_measureCheckBoxes.append(  CheckBox( measure[0], measure[1] ) )
        
        self.m_additionalCheckBoxes = []
        for apa in additionals:
            self.m_additionalCheckBoxes.append( CheckBox( apa[0], apa[1] ) )
        
    def HandleParams( self, params ):
        ContributorDialog.HandleParams( self, params )
        self.m_rfSetupCtrl.SetData( params["rfSetup"] )
        self.m_hierarchyCtrl.SetData( params["hierarchy"] )

        checkedRiskClasses = params.At("riskClasses", None)
        for rc in self.m_rcCheckBoxes:
            if checkedRiskClasses:
                rc.SetChecked( rc.m_label in checkedRiskClasses )
        
        checkedMeasures = params.At("measures", None)
        for measure in self.m_measureCheckBoxes:
            if checkedMeasures:
                measure.SetChecked( measure.m_label in checkedMeasures )
        
        checkedAdditionals = params.At("additionals", None)
        for apa in self.m_additionalCheckBoxes:
            if checkedAdditionals:
                apa.SetChecked( apa.m_label in checkedAdditionals )

    def HandleCreate(self, dlg, layout):
        ContributorDialog.HandleCreate( self, dlg, layout )
        self.m_rfSetupCtrl = layout.GetControl( 'rfSetup' )
        self.m_rfSetupCtrl.Populate( acm.FRiskFactorSetup.Select("") )
        self.m_hierarchyCtrl = layout.GetControl( 'hierarchy' )
        self.m_hierarchyCtrl.Populate( acm.FHierarchy.Select("") )
        for rc in self.m_rcCheckBoxes:
            rc.HandleCreate( layout )
        for measure in self.m_measureCheckBoxes:
            measure.HandleCreate( layout )
        for apa in self.m_additionalCheckBoxes:
            apa.HandleCreate( layout )
        self.HandleParams( self.m_params )

    def CreateLayout_Override( self, builder ):
        builder.BeginVertBox('EtchedIn', 'Input' )
        builder.AddComboBox( 'rfSetup', "Risk Factor Setup" )
        builder.AddComboBox( 'hierarchy', "SA Data" )
        
        builder.  BeginVertBox('EtchedIn', 'Risk Classes' )
        for rc in self.m_rcCheckBoxes:
            rc.     BuildLayoutPart( builder )
        builder.  EndBox()
        builder.  BeginVertBox('EtchedIn', 'Measures' )
        for measure in self.m_measureCheckBoxes:
            measure.BuildLayoutPart( builder )
        builder.  EndBox()
        for apa in self.m_additionalCheckBoxes:
            apa.    BuildLayoutPart( builder )
        builder.EndBox()
        
    def HandleApply( self ):
        ContributorDialog.HandleApply( self )
        self.m_params["columnName"] = self.m_params["name"]
        self.m_params["rfSetup"] = self.m_rfSetupCtrl.GetData()
        self.m_params["hierarchy"] = self.m_hierarchyCtrl.GetData()
        self.m_params["riskClasses"] = acm.FArray()
        for rc in self.m_rcCheckBoxes:
            if rc.GetValue():
                self.m_params["riskClasses"].Add( rc.m_label )
     
        self.m_params["measures"] = acm.FArray()
        for measureBox in self.m_measureCheckBoxes:
            if measureBox.GetValue():
                self.m_params["measures"].Add( measureBox.m_label )
  
        self.m_params["additionals"] = acm.FArray()
        for apa in self.m_additionalCheckBoxes:
            if apa.GetValue():
                self.m_params["additionals"].Add( apa.m_label )
                
        return self.m_params

def Create(params):
    return FRTBMeasureContributorDialog( params )
