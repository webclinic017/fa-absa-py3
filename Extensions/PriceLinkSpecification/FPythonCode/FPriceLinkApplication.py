""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkApplication.py"
import acm
import FUxCore

import FPriceLinkSpecificationUtils as Utils

class PriceLinkApplication(FUxCore.LayoutApplication):
    ''' Abstract class. Should not be instantiated directly '''

    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)

        self.tableName = ''
        self.owner = acm.User()
        self.protection = 0

        self.force_reset    = ''
        self.bid            = ''
        self.ask            = ''
        self.bid_size       = ''
        self.ask_size       = ''
        self.last           = ''
        self.high           = ''
        self.low            = ''
        self.open           = ''
        self.settle         = ''
        self.diff           = ''
        self.time_last      = ''
        self.volume_last    = ''
        self.volume_number  = ''
        self.available      = ''
        self.select_all     = ''

    def ShowTableModifiedDialog(self):
        """pops up question message box"""
        message = '%s table has been changed.\nDo you really want to discard the changes?' % self.tableName
        return self.ShowQuestion(message)

    def ShowQuestion(self, message):
        choice = acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Question', message)
        return choice

    def ShowWarning(self, message):
        self.MessageBox('Warning', message)

    def ShowError(self, message):
        self.MessageBox('Error', message)

    def MessageBox(self, boxType, message):
        """pops up an error message box"""
        acm.UX().Dialogs().MessageBox(self.Shell(), boxType, message, 'OK', None, None, 'Button1', 'Button2')

    def GetResetFieldsAsTuple(self):
        return (self.force_reset, self.available, self.volume_number, self.volume_last,
        self.time_last, self.diff, self.settle, self.open, self.low, self.high,
        self.last, self.ask_size, self.bid_size, self.ask, self.bid)

    def EnableAllResetFields(self):
        fieldList = self.GetResetFieldsAsTuple()
        for field in fieldList:
            field.Enabled(True)
        self.select_all.Enabled(True)

    def DisableAllResetFields(self):
        fieldList = self.GetResetFieldsAsTuple()
        for field in fieldList:
            field.Enabled(False)
        self.select_all.Enabled(False)

    def CheckAllResetFields(self):
        fieldList = self.GetResetFieldsAsTuple()
        for field in fieldList:
            field.Checked(True)
        self.select_all.Checked(True)

    def UnCheckAllResetFields(self):
        fieldList = self.GetResetFieldsAsTuple()
        for field in fieldList:
            field.Checked(False)
        self.select_all.Checked(False)

    def SetResetFields(self, number):
        """sets reset fields"""
        bits = 15
        valueList = Utils.DecimalToBinary(number, bits)
        fieldList = self.GetResetFieldsAsTuple()
        for field, value in zip(fieldList, valueList):
            field.Checked(value)
        if all(valueList):
            self.select_all.Checked(1)

    def GetResetFields(self):
        """returns decimal value for reset fields"""
        binaryStr = ''
        fieldList = self.GetResetFieldsAsTuple()
        for field in fieldList:
            if field.Checked():
                binaryStr += '1'
            else:
                binaryStr += '0'
        return Utils.BinaryToDecimal(binaryStr)

    def GetPriceSemantics(self):
        semantics = ['']
        semantics.extend(acm.FChoiceList.Select("list='PriceSemantics'"))
        return semantics

    def GetPriceServices(self):
        services = ['']
        services.extend(acm.FChoiceList.Select("list='PriceServices'"))
        return services

    def GetContextHelpID(self):
        return 1141

class PriceServicesChangeHandler:
    def __init__(self, parent):
        self.parent = parent

    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) in ('update', 'insert'):
            selectedService = self.parent.service.GetData()
            self.parent.service.Populate(self.parent.GetPriceServices())
            self.parent.service.SetData(selectedService)
        elif str(aspect) == 'remove':
            if self.parent.service.ItemExists(param):
                self.parent.service.RemoveItem(param)


def OnCheckBoxSelected(Dlg, arg):
    """Action when any check box is checked"""
    fieldList = Dlg.GetResetFieldsAsTuple()
    valueList = [field.Checked() for field in fieldList]
    Dlg.select_all.Checked(all(valueList))

