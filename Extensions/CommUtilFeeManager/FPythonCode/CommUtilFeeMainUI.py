'''
MODULE
    CommUtilFeeManager - This module prvoides a maintenance screen for Commitment fees, 
                         Utilisations fees and Rates used to calculate these fees. 
                         This module replaces the CommFeeUploader.
   
HISTORY
    Date        Developer               Notes
    2017-10-09  Ntuthuko Matthews       created
    2017-11-09  Ntuthuko Matthews       add the rates maintenace tab
    2018-03-27  Ntuthuko Matthews	changed the tab name of the rates maintainance tab
					validate the rates to add up to 100%
'''


import acm
import FUxCore
import operator
import logging
from at_logging import getLogger
from CommUtilFeeUploader import CommUtilFeeModel
from RatesUtilFeeUploader import RatesUtilFeeModel
from DataClass import CommUtilFee, RatesUtilFee
from HelperFunctions import HelperFunctions
import CommUtilFeeUI
import RatesUtilUI


def StartDialog(eii, *rest):
    trade = None 
    if eii.ExtensionObject().IsKindOf(acm.FArray):
        trade = eii.ExtensionObject().At(0)
    builder = CreateLayout()
    customDlg = CommUtilFeeUploaderDialog()
    customDlg.InitControls(trade)
    shell = acm.UX().SessionManager().Shell()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg)

class CommUtilFeeUploaderDialog(FUxCore.LayoutTabbedDialog):
    TOTAL = float(500050)
    FEE_TYPES = ['', 'Utilization', 'Commitment']
    ROLL_PERIOD_INPUT = ['', 'Annually', 'At End', 'Daily', 'Monthly', 'Quarterly', 'SemiAnnually', 'Weekly']
    ROLL_CONV_INPUT = ['', 'Following', 'Preceding', 'Mod. Following', 'Mod. Preceding']
    DAY_COUNT_INPUT = ['', 'Act/360', 'Act/365']

    #Set decimal formatters
    NUM_FORMATTER = acm.Get('formats/FXRate')
    NUM_FORMATTER_8_DIGITS = acm.Get('formats/AllocationBucketWeight')

    # Set a module logger.
    LOGGER = getLogger(__name__)
    LOGGER.setLevel(logging.INFO)

    def __init__(self): 
        self.commFeeLayout = None
        self.ratesLayout = None
        self.dlg = None
        self.commBindings = None
        self.ratesBindings = None
        self.layout = None
        self.trade = None
        self.ratesUtilFee = None
        self.commUtilFee = None
        self.feeType = None
        self.shell = None
        self.bindingValues = []
        self.ratesBindingValues = []
        self.IntCommUtilFeePaneCtrls()
        self.InitRatesPaneCtrls()
        self.chkChanged = False

        self.LOGGER.debug('Setting default values __init__...')

    def IntCommUtilFeePaneCtrls(self):
        self.cboCalcFeeTypeCtrl = None
        self.txtTradeNumberCtrl = None
        self.txtFacilityMaxCtrl = None
        self.txtThresholdCtrl = None
        self.txtCommitFeeRateCtrl = None
        self.txtFacilityExpiryCtrl = None
        self.txtCommitFeeBaseCtrl = None
        self.cboCommitPeriodCtrl = None
        self.cboRollingConventionCtrl = None
        self.cboDayCountCtrl = None
        self.chkCopyCtrl = None
        self.chkLinkedCtrl = None
        self.btnCloseCtrl = None
        
        self.LOGGER.debug('Setting default values IntCommUtilFeePaneCtrls...')

    def InitRatesPaneCtrls(self):
        self.chkShowCtrl = None
        for i in range(1, 11):
            rate_from = 'txtRateUtilizedFrom{0}Ctrl'.format(i)
            rate_to = 'txtRateUtilizedTo{0}Ctrl'.format(i)
            rate = 'txtRate{0}Ctrl'.format(i)
            self.__dict__[rate_from] = None
            self.__dict__[rate_to] = None
            self.__dict__[rate] = None

        self.LOGGER.debug('Setting default values InitRatesPaneCtrls...')

    def UpdateCommFeeControls(self):
        value = None
        value = self.bindingValues == self.commBindings.GetValuesByName()
        self.LOGGER.debug('Updating bindingValues (bindingValues vs. commBindings) = {0}'.format(value))         
        self.bindingValues = self.commBindings.GetValuesByName()
   
    def UpdateRatesControls(self):
        value = self.ratesBindingValues == self.ratesBindings.GetValuesByName()
        self.LOGGER.debug('Updating ratesBindingValues (ratesBindingValues vs. ratesBindings) = {0}'.format(value))        
        self.ratesBindingValues = self.ratesBindings.GetValuesByName()

    def InitControls(self, trade):
        self.commBindings = acm.FUxDataBindings()
        self.commBindings.AddDependent(self)
        self.ratesBindings = acm.FUxDataBindings()
        self.ratesBindings.AddDependent(self)
        self.trade = trade

        #Bind the first Pane to the window
        self.CommUtilFeeBindings()

    def IsRatesUpdateControls(self):
        self.LOGGER.debug('IsRatesUpdateControls {0}'.format(self.ratesBindingValues != self.ratesBindings.GetValuesByName()))
        return self.ratesBindingValues != self.ratesBindings.GetValuesByName()

    def IsCommUtilsUpdateControls(self):
        return self.chkChanged or (self.cboCalcFeeTypeCtrl.GetValue() and 
                    self.bindingValues != self.commBindings.GetValuesByName())

    def IsUpdateControls(self):
        if self.IsRatesUpdateControls() or self.IsCommUtilsUpdateControls():
            return True
        return False

    def GetControlName(self, control):
        controls = {self.txtRateUtilizedFrom1Ctrl:'intRateUtilizedFrom1Ctrl',
                    self.txtRateUtilizedFrom2Ctrl:'intRateUtilizedFrom2Ctrl',
                    self.txtRateUtilizedFrom3Ctrl:'intRateUtilizedFrom3Ctrl',
                    self.txtRateUtilizedFrom4Ctrl:'intRateUtilizedFrom4Ctrl',
                    self.txtRateUtilizedFrom5Ctrl:'intRateUtilizedFrom5Ctrl',
                    self.txtRateUtilizedFrom6Ctrl:'intRateUtilizedFrom6Ctrl',
                    self.txtRateUtilizedFrom7Ctrl:'intRateUtilizedFrom7Ctrl',
                    self.txtRateUtilizedFrom8Ctrl:'intRateUtilizedFrom8Ctrl',
                    self.txtRateUtilizedFrom9Ctrl:'intRateUtilizedFrom9Ctrl',
                    self.txtRateUtilizedFrom10Ctrl:'intRateUtilizedFrom10Ctrl',
                    self.txtRateUtilizedTo1Ctrl:'intRateUtilizedTo1Ctrl',
                    self.txtRateUtilizedTo2Ctrl:'intRateUtilizedTo2Ctrl',
                    self.txtRateUtilizedTo3Ctrl:'intRateUtilizedTo3Ctrl',
                    self.txtRateUtilizedTo4Ctrl:'intRateUtilizedTo4Ctrl',
                    self.txtRateUtilizedTo5Ctrl:'intRateUtilizedTo5Ctrl',
                    self.txtRateUtilizedTo6Ctrl:'intRateUtilizedTo6Ctrl',
                    self.txtRateUtilizedTo7Ctrl:'intRateUtilizedTo7Ctrl',
                    self.txtRateUtilizedTo8Ctrl:'intRateUtilizedTo8Ctrl',
                    self.txtRateUtilizedTo9Ctrl:'intRateUtilizedTo9Ctrl',
                    self.txtRateUtilizedTo10Ctrl:'intRateUtilizedTo10Ctrl'
                    }

        if control in controls.keys():
            return controls[control]
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        
        if parameter == self.cboCalcFeeTypeCtrl:
            value = parameter.GetValue()
            self.chkCalcCommFeeCtrl.Visible(False)
            self.chkCalcUtilFeeCtrl.Visible(False)
            self.txtThresholdCtrl.Visible(True)
            self.chkCopyCtrl.Visible(False)
            self.chkCopyCtrl.Checked(False)
            self.txtCommitFeeRateCtrl.Editable(True)
            self.txtCommitFeeRateCtrl.Label('Comm Fee Rate(%)*')
            self.cboDayCountCtrl.Label('Day Count') 
            if 'Commitment' == value:
                self.feeType = 'Commitment'
                self.CommUtilFeePopulate()
                self.chkCalcCommFeeCtrl.Visible(True)
                self.txtCommitFeeRateCtrl.Visible(True)

                self.LOGGER.debug('Show and populate the commission fee controls...')
                
            elif 'Utilization' == value:
                self.feeType = 'Utilization'
                self.CommUtilFeePopulate()
                self.chkCalcUtilFeeCtrl.Visible(True)
                self.txtThresholdCtrl.Visible(False)
                self.txtCommitFeeRateCtrl.Visible(False)
                self.txtCommitFeeRateCtrl.Editable(False)
                self.txtCommitFeeRateCtrl.Label('Utilization Fee*')
                self.cboDayCountCtrl.Label('Day Count*')
                
                self.LOGGER.debug('Show and populate the utilisation fee controls...')

            else:
                self.feeType = None
                self.CommUtilFeePopulate()
                
                self.LOGGER.debug('Clear comm/util fee controls...')
                
            self.UpdateCommFeeControls()
        
    def HandleDestroy(self):
        """closes the dialog"""
        self.commBindings.RemoveDependent(self)
        self.ratesBindings.RemoveDependent(self)

    def HandleCancel(self):
        try:
            #Check for any unsaved changes before closing the dialog.
            result = None
            if self.IsUpdateControls():
                message = 'You have unsaved changes.\nAre you sure that you want to quit?'
                result = self.MessageBoxYesNo(message)
                if result == 'Button2':
                    return

            self.LOGGER.debug('Closing the Commitment/Utilization Fee Manager.')
            return True
        except Exception, e:
            self.LOGGER.error(str(e))
            return True

    def HandleApply(self):
        #save if a change was made
        validRates = False
        validCommFee = False

        try:
            self.LOGGER.debug('IsUpdateControls {0}'.format(self.IsUpdateControls()))
            self.LOGGER.debug('IsRatesUpdateControls {0}'.format(self.IsRatesUpdateControls()))
            self.LOGGER.debug('IsCommUtilsUpdateControls {0}'.format(self.IsCommUtilsUpdateControls()))
            
            if self.IsUpdateControls():
                if self.IsRatesUpdateControls():
                    model = self.AddRates()
                    if self.ValidateRanges():
                        self.SaveRates(model)
                        validRates = True
                
                if self.IsCommUtilsUpdateControls():
                    model = self.AddCommFee()
                    if self.ValidateCommUtilFee():
                        self.SaveCommUtil(model)
                        validCommFee = True

                #update commBindings when changes have been saved
                if validRates or validCommFee:
                    self.UpdateCommFeeControls()
            else:
                self.LOGGER.info('No changes will be made.')

        except Exception, e:
            self.LOGGER.error('1: {0}'.format(e))

        #don't close the window
        return

    def HandleCreate(self, dlg, layout):
        try:
            self.dlg = dlg
            self.layout = layout
            self.shell = self.dlg.Shell()
            self.dlg.Caption('Commitment/Utilization Fee Manager')
            self.AddPanes() 
            self.LoadControls()
            self.RatePopulate()
            self.UpdateCommFeeControls()
            self.UpdateRatesControls()
            if self.trade:
                self.LOGGER.debug('Opening the Commitment/Utilization Fee Manager - {0}'.format(self.trade.Oid()))

        except Exception, e:
            self.LOGGER.error('2: {0}'.format(e))
        
    def MessageBoxInformation(self, message):
        acm.UX().Dialogs().MessageBoxInformation(self.shell, message)
        return

    def MessageBoxYesNo(self, message, caption='Question'):
        return acm.UX().Dialogs().MessageBoxYesNo(self.shell, caption, message)

    def ValidateCommUtilFee(self):
        #add validation logic

        if not self.commUtilFee.IsEmpty():
            if not self.trade:
                self.MessageBoxInformation('Missing Trade Number.')
                return False
            if not self.commUtilFee.FacilityMax:
                self.MessageBoxInformation('Facility Limit is required.')
                return False
            if self.feeType == 'Commitment':
                if not self.commUtilFee.Limit:
                    self.MessageBoxInformation('Threshold (0<x<1) is required.') 
                    return False
                if self.commUtilFee.Limit:
                    if float(self.commUtilFee.Limit) > 1:
                        self.MessageBoxInformation('Threshold (0<x<1) cannnot be greater than 1.')
                        return False
                    if float(self.commUtilFee.Limit) < 0:
                        self.MessageBoxInformation('Threshold (0<x<1) cannnot be less than 0.')
                        return False
                if not self.commUtilFee.CommitFeeRate:
                        self.MessageBoxInformation('Comm Fee Rate{0} is required.'.format('%'))
                        return False
            if not self.commUtilFee.FacilityExpiry:
                self.MessageBoxInformation('Facility Expiry (dd/mm/yyyy) is required.')
                return False
            if not self.commUtilFee.CommitFeeBase:
                self.MessageBoxInformation('Rolling Base Day (dd/mm/yyyy) is required.')
                return False
            if self.commUtilFee.FacilityExpiry < self.commUtilFee.CommitFeeBase:
                self.MessageBoxInformation('CommFeeBase must be smaller than FacilityExpiry')
                return False
            if not self.commUtilFee.CommitPeriod:
                self.MessageBoxInformation('Rolling Period is required.')
                return False
            if not self.commUtilFee.RollingConvention:
                self.MessageBoxInformation('Rolling Convention is required.')
                return False
            if self.feeType == 'Utilization':
                if self.ratesUtilFee.IsEmpty():
                    self.MessageBoxInformation('Cannot calculate Utilization Fee.\nNo rates found in the Utilisation Fee Rate Table')
                    return False            
                if not self.commUtilFee.DayCount:
                    self.MessageBoxInformation('DayCount is required.')
                    return False
            return True
        else:
            return False

    def OnValidateRangeItem(self, control):
        try:
            if len(self.ratesBindingValues) == 0:
                self.UpdateRatesControls()

            _control = self.GetControlName(control)
            dictResult = self.ratesBindingValues
            value = dictResult.At(_control)
        except Exception, e:
            self.LOGGER.debug('Error:{0}'.format(e))
            
        self.LOGGER.debug('Control find in dictResult = {0}'.format(value))
        if value:
            result = control.GetValue() in dictResult.Values()
            self.LOGGER.debug('Found value in dictResult = {0}'.format(result))
            if result:
                msg = 'Invalid utilized rates. This already exists.'
                self.MessageBoxInformation(msg) 
                return False
            return True
    
    def ValidateRanges(self):
        """
        This function is to valid the correctness of the % utilisation.
        There shouldn't be any overlaps or incomplete % intervals
        When rates are entered correctly they add up to 500050.
        """
        if self.ratesUtilFee.IsEmpty():
            return False
            
        lst = [HelperFunctions().get_rate_list(self.ratesUtilFee, i)
                for i in range(1, self.ratesUtilFee.Size())]

        lst = reduce(operator.add, lst)
        
        #check for duplicates
        if not self.CheckDuplicateRates(lst):
            return False
        
        #check for ordering
        if not self.CheckOrderingRates(lst):
            return False
        
        #check for gaps in the ranges
        if not self.CheckTotalRanges():
            return False        

        return True

    def CheckTotalRanges(self):
        ranges = [HelperFunctions().get_rate_utilised_ranges(self.ratesUtilFee, i)
                  for i in range(1, self.ratesUtilFee.Size())
              ]
        
        lst = reduce(operator.add, ranges)
        
        current = round(sum(lst), 2)
        self.LOGGER.debug('TOTAL = Current >>> {0}, {1}'.format(self.TOTAL, current))
        if self.TOTAL != current:
            msg = 'Invalid utilized rates. Please check if the ranges (0.0 - 100) are set correctly.'
            self.MessageBoxInformation(msg) 
            self.LOGGER.info(msg)
            return False
        return True        

    def CheckRateRanges(self):
        ranges = [getattr(self.ratesUtilFee, 'Rate{0}'.format(i))
                  for i in range(1, self.ratesUtilFee.Size())
        ]
        
        lst = reduce(operator.add, ranges)
        current = round(lst, 2)
        self.LOGGER.debug('TOTAL = Current >>> {0}, {1}'.format(self.TOTAL, current))
        if 1.0 != current:
            msg = 'Invalid rates. Please ensure that all the rates add up to 100%%.'
            self.MessageBoxInformation(msg) 
            self.LOGGER.info(msg)
            return False
        return True  

    def CheckOrderingRates(self, lst):
        if not sorted(lst) == lst:
            msg = 'Invalid utilized rates. Overlapping rates found.'
            self.MessageBoxInformation(msg)
            self.LOGGER.info(msg)
            return False     
        return True        

    def CheckDuplicateRates(self, lst):
        duplicates = [i for i in lst if lst.count(i) > 1]
        
        if duplicates:
            newSet = set(duplicates)
            items = ','.join(str(i) for i in newSet)
            msg = 'Invalid utilized rates. Duplicate rates found: {0}'.format(items)
            self.MessageBoxInformation(msg) 
            self.LOGGER.info(msg)
            return False     
        return True
    
    def SaveRates(self, model):
        if self.ratesUtilFee and not self.ratesUtilFee.IsEmpty():
            try:
                model = RatesUtilFeeModel(self.trade)
                model.Put(self.ratesUtilFee)
                self.UpdateRatesControls()
                self.LOGGER.info('% Utilization Rates were saved successfully.')
            except Exception, e:
                self.LOGGER.error('3: An error occurred while saving rates: {0}'.format(e))

    def SaveCommUtil(self, model):
        if self.commUtilFee and self.feeType:
            try:
                model = CommUtilFeeModel(self.trade)
                model.Put(self.commUtilFee, self.feeType)
                self.LOGGER.info('{0} Fees were saved successfully.'.format(self.commUtilFee.FeeType))
                self.chkChanged = False

                self.CommUtilFeePopulate()

            except Exception, e:
                self.LOGGER.error('4: An error occurred while saving {0}: {1}'.format(self.feeType, e))

    def AddRates(self):
        model = RatesUtilFeeModel(self.trade)
        try:
            self.ratesUtilFee = model.New()
             
            for i in range(1, self.ratesUtilFee.Size()):
                rate_from = 'RateFrom{0}'.format(i)
                rate_to = 'RateTo{0}'.format(i)
                rate = 'Rate{0}'.format(i)

                rate_from_text_field = getattr(self, 'txtRateUtilizedFrom{0}Ctrl'.format(i)).GetValue()
                rate_to_text_field = getattr(self, 'txtRateUtilizedTo{0}Ctrl'.format(i)).GetValue()
                rate_text_field = getattr(self, 'txtRate{0}Ctrl'.format(i)).GetValue()

                setattr(self.ratesUtilFee, rate_from, rate_from_text_field if rate_from_text_field else 0)
                setattr(self.ratesUtilFee, rate_to, rate_to_text_field if rate_to_text_field else 0)
                setattr(self.ratesUtilFee, rate, rate_text_field if rate_text_field else 0)

            self.LOGGER.debug('Mapping the Rates class with UI data: {0}'.format(self.ratesUtilFee.Items()))

        except Exception, e:
            self.LOGGER.error('5: An error occurred while populating the rate controls: {0}'.format(e))
            
        return model

    def RatePopulate(self):
        model = RatesUtilFeeModel(self.trade)
        try:
            self.ratesUtilFee = model.Get()

            for i in range(1, self.ratesUtilFee.Size()):
                rate_from = getattr(self.ratesUtilFee, 'RateFrom{0}'.format(i))
                rate_to = getattr(self.ratesUtilFee, 'RateTo{0}'.format(i))
                rate = getattr(self.ratesUtilFee, 'Rate{0}'.format(i))

                getattr(self, 'txtRateUtilizedFrom{0}Ctrl'.format(i)).SetValue(rate_from)
                getattr(self, 'txtRateUtilizedTo{0}Ctrl'.format(i)).SetValue(rate_to)
                getattr(self, 'txtRate{0}Ctrl'.format(i)).SetValue(rate)

            self.LOGGER.debug('Mapping UI with Rates class with: {0}'.format(self.ratesUtilFee.Items()))

        except Exception, e:
            self.LOGGER.error('6: An error occurred while retrieving data from rate fields: {0}'.format(e))

    def ShowHideFields(self, showHide=False):
        if not self.ratesUtilFee:
            model = RatesUtilFeeModel(self.trade)
            self.ratesUtilFee = model.New()
            
        for i in range(5, self.ratesUtilFee.Size()):
            rate_from = 'RateFrom{0}'.format(i)
            rate_to = 'RateTo{0}'.format(i)
            rate = 'Rate{0}'.format(i)

            getattr(self, 'txtRateUtilizedFrom{0}Ctrl'.format(i)).Visible(showHide)
            getattr(self, 'txtRateUtilizedTo{0}Ctrl'.format(i)).Visible(showHide)
            getattr(self, 'txtRate{0}Ctrl'.format(i)).Visible(showHide)

        self.LOGGER.debug('ShowHideFields is {0} on rate controls'.format(showHide))

    def EditableFields(self, editable=False):
        if not self.ratesUtilFee:
            model = RatesUtilFeeModel(self.trade)
            self.ratesUtilFee = model.New()
            
        for i in range(1, self.ratesUtilFee.Size()):
            rate_from = 'RateFrom{0}'.format(i)
            rate_to = 'RateTo{0}'.format(i)
            rate = 'Rate{0}'.format(i)

            getattr(self, 'txtRateUtilizedFrom{0}Ctrl'.format(i)).Editable(editable)
            getattr(self, 'txtRateUtilizedTo{0}Ctrl'.format(i)).Editable(editable)
            getattr(self, 'txtRate{0}Ctrl'.format(i)).Editable(editable)

        self.LOGGER.debug('EditableFields is {0} on rate controls'.format(editable))

    def AddCommFee(self):
        model = CommUtilFeeModel(self.trade)
        try:
            self.commUtilFee = model.New()
            if self.commUtilFee:
                self.commUtilFee.FeeType = self.cboCalcFeeTypeCtrl.GetValue()
                self.commUtilFee.CalcCommFee = self.chkCalcCommFeeCtrl.Checked()
                self.commUtilFee.CalcUtilFee = self.chkCalcUtilFeeCtrl.Checked()
                self.commUtilFee.Linked = self.chkLinkedCtrl.Checked()
                self.commUtilFee.FacilityMax = self.txtFacilityMaxCtrl.GetValue()
                self.commUtilFee.Limit = self.txtThresholdCtrl.GetValue()
                self.commUtilFee.CommitFeeRate = str(self.txtCommitFeeRateCtrl.GetValue())
                self.commUtilFee.FacilityExpiry = self.txtFacilityExpiryCtrl.GetValue()
                self.commUtilFee.CommitFeeBase = self.txtCommitFeeBaseCtrl.GetValue()
                self.commUtilFee.CommitPeriod = self.cboCommitPeriodCtrl.GetValue()
                self.commUtilFee.RollingConvention = self.cboRollingConventionCtrl.GetValue()
                self.commUtilFee.DayCount = self.cboDayCountCtrl.GetValue()
                self.LOGGER.debug('Mapping the AddCommFee class with UI data: {0}'.format(self.commUtilFee.Items()))
                
        except Exception, e:
            self.LOGGER.error('7: An error occurred while populating the comm/util controls: {0}'.format(e))

        return model

    def CommUtilFeePopulate(self):
        try:
            model = CommUtilFeeModel(self.trade)
            if self.feeType:
                self.commUtilFee = model.Get(self.feeType)
            else:
                self.commUtilFee = model.New()
            
            if self.commUtilFee:
                if str(self.cboCalcFeeTypeCtrl.GetValue()) in ['', None]:
                    self.cboCalcFeeTypeCtrl.SetValue('')

                self.chkCalcCommFeeCtrl.Checked(self.commUtilFee.CalcCommFee)
                self.chkCalcUtilFeeCtrl.Checked(self.commUtilFee.CalcUtilFee)
                self.chkLinkedCtrl.Checked(self.commUtilFee.Linked)
                self.txtFacilityMaxCtrl.SetValue(self.commUtilFee.FacilityMax)
                self.txtThresholdCtrl.SetValue(self.commUtilFee.Limit)
                self.txtCommitFeeRateCtrl.SetValue(self.commUtilFee.CommitFeeRate)
                self.txtFacilityExpiryCtrl.SetValue(self.commUtilFee.FacilityExpiry)
                self.txtCommitFeeBaseCtrl.SetValue(self.commUtilFee.CommitFeeBase)
                self.cboCommitPeriodCtrl.SetValue(self.commUtilFee.CommitPeriod)
                self.cboRollingConventionCtrl.SetValue(self.commUtilFee.RollingConvention)
                self.cboDayCountCtrl.SetValue(self.commUtilFee.DayCount)

            self.LOGGER.debug('Mapping UI with CommUtilFee class with: {0}'.format(self.commUtilFee.Items()))
            
        except Exception, e:
            self.LOGGER.error('8: An error occurred while retrieving data from comm/util fee fields: {0}'.format(e)) 

    def LoadControls(self):
        try:
            self.btnTradeCtrl = self.commFeeLayout.GetControl('btnInsertItems')        
            self.chkCalcCommFeeCtrl = self.commFeeLayout.GetControl('chkCalcCommFeeCtrl')
            self.chkCalcUtilFeeCtrl = self.commFeeLayout.GetControl('chkCalcUtilFeeCtrl')
            self.chkLinkedCtrl = self.commFeeLayout.GetControl('chkLinkedCtrl')
            self.chkCopyCtrl = self.commFeeLayout.GetControl('chkCopyCtrl')
            self.chkShowCtrl = self.ratesLayout.GetControl('chkShowCtrl')

            self.btnTradeCtrl.AddCallback("Activate", self.btnTradeCtrlClicked, self)
            self.chkCalcCommFeeCtrl.AddCallback("Changing", self.chkCalcCommFeeCtrlChanging, self)
            self.chkCalcUtilFeeCtrl.AddCallback("Changing", self.chkCalcUtilFeeCtrlChanging, self)
            self.chkLinkedCtrl.AddCallback("Changing", self.chkLinkedCtrlChanging, self)
            self.chkShowCtrl.AddCallback("Changing", self.chkShowCtrlChanging, self)
            self.chkCopyCtrl.AddCallback("Changing", self.chkCopyCtrlChanging, self)
        
            self.chkCalcCommFeeCtrl.Visible(False)
            self.chkCalcUtilFeeCtrl.Visible(False)
            self.chkCopyCtrl.Visible(False)
            self.txtTradeNumberCtrl.Editable(False)
            self.txtTradeNumberCtrl.SetValue(self.trade)
            self.ShowHideFields()
            #self.EditableFields()

            self.LOGGER.debug('Loading controls...')

        except Exception, e:
            self.LOGGER.error('9: {0}'.format(e))

    def btnTradeCtrlClicked(self, arg1, arg2):
        insertItems = acm.FArray()
        insertItems.Add(acm.FTrade)
        trade = acm.UX().Dialogs().SelectObjectsInsertItems(self.shell, insertItems, True)
        if trade:
            self.trade = trade[0]
            self.txtTradeNumberCtrl.SetValue(self.trade)
            self.CommUtilFeePopulate()

    def chkCalcCommFeeCtrlChanging(self, arg1, arg2):
        self.chkChanged = True

    def chkCalcUtilFeeCtrlChanging(self, arg1, arg2):
        self.chkChanged = True

    def chkLinkedCtrlChanging(self, arg1, arg2):
        self.chkChanged = True
        
    def chkShowCtrlChanging(self, arg1, arg2):
        self.ShowHideFields(self.chkShowCtrl.Checked())

    def chkCopyCtrlChanging(self, arg1, arg2):
        temp_feeType = self.feeType
        if self.chkCopyCtrl.Checked():
            self.feeType = 'Commitment'
            self.CommUtilFeePopulate()
            self.feeType = temp_feeType
        else:
            self.feeType = temp_feeType
            self.CommUtilFeePopulate()

    def AddPanes(self):
        try:
            self.commFeeLayout = self.dlg.AddPane('Comm/Utilisation Fee', self.CommUtilFeePane())
            self.commBindings.AddLayout(self.commFeeLayout)
            
            self.RatePaneBindings()
            self.ratesLayout = self.dlg.AddPane('Utilisation Fee Rate Table', self.RatesPane())
            self.ratesBindings.AddLayout(self.ratesLayout)

            self.commBindings.AddLayout(self.layout)
            self.ratesBindings.AddLayout(self.layout)
            
            self.LOGGER.debug('Adding Panes and commBindings to the main layout')
            
        except Exception, e:
            self.LOGGER.error('10: {0}'.format(e))

    def CommUtilFeePane(self):
        return CommUtilFeeUI.CommUtilFeePane(self)

    def RatesPane(self):
        return RatesUtilUI.RatesPane(self)
        
    def CommUtilFeeBindings(self):
        self.txtTradeNumberCtrl = self.commBindings.AddBinder('txtTradeNumberCtrl', acm.GetDomain('string'), None)
        self.cboCalcFeeTypeCtrl = self.commBindings.AddBinder('cboCalcFeeTypeCtrl', acm.GetDomain('string'), None, self.FEE_TYPES)
        self.txtFacilityMaxCtrl = self.commBindings.AddBinder('txtFacilityMaxCtrl', acm.GetDomain('double'), None)
        self.txtThresholdCtrl = self.commBindings.AddBinder('txtThresholdCtrl', acm.GetDomain('double'), None)
        self.txtCommitFeeRateCtrl = self.commBindings.AddBinder('txtCommitFeeRateCtrl', acm.GetDomain('double'), self.NUM_FORMATTER_8_DIGITS)
        self.txtFacilityExpiryCtrl = self.commBindings.AddBinder('txtFacilityExpiryCtrl', acm.GetDomain('date'), None)
        self.txtCommitFeeBaseCtrl = self.commBindings.AddBinder('txtCommitFeeBaseCtrl', acm.GetDomain('date'), None)
        self.cboCommitPeriodCtrl = self.commBindings.AddBinder('cboCommitPeriodCtrl', acm.GetDomain('string'), None, self.ROLL_PERIOD_INPUT)
        self.cboRollingConventionCtrl = self.commBindings.AddBinder('cboRollingConventionCtrl', acm.GetDomain('string'), None, self.ROLL_CONV_INPUT)
        self.cboDayCountCtrl = self.commBindings.AddBinder('cboDayCountCtrl', acm.GetDomain('string'), None, self.DAY_COUNT_INPUT)

        self.LOGGER.debug('Binding CommUtilFeeBindings controls...')

    def RatePaneBindings(self):
        self.txtRateUtilizedFrom1Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom1Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo1Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo1Ctrl', acm.GetDomain('double'), None)
        self.txtRate1Ctrl = self.ratesBindings.AddBinder('doubleRate1Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom2Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom2Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo2Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo2Ctrl', acm.GetDomain('double'), None)
        self.txtRate2Ctrl = self.ratesBindings.AddBinder('doubleRate2Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom3Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom3Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo3Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo3Ctrl', acm.GetDomain('double'), None)
        self.txtRate3Ctrl = self.ratesBindings.AddBinder('doubleRate3Ctrl', acm.GetDomain('double'), None) 

        self.txtRateUtilizedFrom4Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom4Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo4Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo4Ctrl', acm.GetDomain('double'), None)
        self.txtRate4Ctrl = self.ratesBindings.AddBinder('doubleRate4Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom5Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom5Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo5Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo5Ctrl', acm.GetDomain('double'), None)
        self.txtRate5Ctrl = self.ratesBindings.AddBinder('doubleRate5Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom6Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom6Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo6Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo6Ctrl', acm.GetDomain('double'), None)
        self.txtRate6Ctrl = self.ratesBindings.AddBinder('doubleRate6Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom7Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom7Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo7Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo7Ctrl', acm.GetDomain('double'), None)
        self.txtRate7Ctrl = self.ratesBindings.AddBinder('doubleRate7Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom8Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom8Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo8Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo8Ctrl', acm.GetDomain('double'), None)
        self.txtRate8Ctrl = self.ratesBindings.AddBinder('doubleRate8Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom9Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom9Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo9Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo9Ctrl', acm.GetDomain('double'), None)
        self.txtRate9Ctrl = self.ratesBindings.AddBinder('doubleRate9Ctrl', acm.GetDomain('double'), None)

        self.txtRateUtilizedFrom10Ctrl = self.ratesBindings.AddBinder('intRateUtilizedFrom10Ctrl', acm.GetDomain('double'), None)
        self.txtRateUtilizedTo10Ctrl = self.ratesBindings.AddBinder('intRateUtilizedTo10Ctrl', acm.GetDomain('double'), None)
        self.txtRate10Ctrl = self.ratesBindings.AddBinder('doubleRate10Ctrl', acm.GetDomain('double'), None)

        self.LOGGER.debug('Binding RatePaneBindings controls...')

def CreateLayout():
    b = acm.FUxLayoutBuilder() 
    b. BeginHorzBox()
    b.  AddFill()
    b.  AddButton('ok', 'Save')
    b.  AddButton('cancel', 'Close')
    b. EndBox() 
    return b
