""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/portfoliosPerLevelInPortfolioTree.py"
import acm
import FUxCore
import FUxUtils


class PortfoliosPerLevelInPortfolioTree(FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_initialData = None
        self.m_portfolio = None

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        self.m_portfolio.BuildLayoutPart(b, 'Portfolio Tree')
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def CreateToolTip(self):
        self.m_portfolio.ToolTip('Select the portfolio tree')

    def DisplayErrorMessage(self, information):
        acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error',
                information, 'Ok', None, None, 'Button1', 'Button1')

    def HandleApply(self):
        if not self.m_bindings.Validate(True):
            return None
        if not self.m_portfolio.GetValue():
            return None
        dictResult = self.m_bindings.GetValuesByName()
        return dictResult

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Portfolio Tree')
        self.m_bindings.AddLayout(layout)
        if self.m_initialData:
            self.m_bindings.SetValuesByName(self.m_initialData)
        self.CreateToolTip()
        self.UpdateControls()

    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.m_portfolio = \
            self.m_bindings.AddBinder('portfolio',
                acm.GetDomain('FCompoundPortfolio'))

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.UpdateControls()

    def UpdateControls(self):
        pass


def ael_custom_dialog_show(shell, parameters):
    dialog = PortfoliosPerLevelInPortfolioTree()
    initData = FUxUtils.UnpackInitialData(parameters)
    dialogData = None
    if initData:
        dialogData = initData.At('dialogData')
    dialog.InitControls()
    dialog.m_initialData = dialogData
    dialogData = acm.UX().Dialogs().ShowCustomDialogModal(shell,
        dialog.CreateLayout(), dialog)
    if dialogData:
        resultDict = acm.FDictionary()
        resultDict.AtPut('dialogData', dialogData)
        return resultDict
    return None


def ael_custom_label(parameters, dictExtra, *extra):
    dialogData = parameters.At('dialogData')
    if dialogData:
        portfolio = dialogData.At('portfolio')
        if portfolio:
            return portfolio.Name()
    return None


def get_portfolios_per_level(portfolio_list, portfolios_per_level):
    portfolios_per_level.Add(portfolio_list)
    next_level = acm.FArray()
    for portfolio in portfolio_list:
        if portfolio.Class().IncludesBehavior(acm.FCompoundPortfolio):
            next_level.AddAll(portfolio.SubPortfolios())
        else:
            pass
    if next_level.Size():
        get_portfolios_per_level(next_level, portfolios_per_level)


def ael_custom_dialog_main(parameters, dictExtra):
    result_list = []
    dialogData = parameters.At('dialogData')
    portfolio = dialogData.At('portfolio')
    portfolios_per_level = acm.FArray()
    top_level = acm.FArray()
    top_level.Add(portfolio)
    get_portfolios_per_level(top_level, portfolios_per_level)
    i = 1
    for level in portfolios_per_level:
        np = acm.FNamedParameters()
        np.Name("Level%s" % i)
        np.AddParameter('portfolios', level)
        result_list.append(np)
        i += 1
    return result_list
