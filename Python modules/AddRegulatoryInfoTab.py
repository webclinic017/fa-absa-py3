import acm
import FIntegrationUtils
import FRegulatoryInfoSpecs
FRegulatoryInfoSpecs.upgrade_for_changes()
FRegulatoryInfoSpecs.upgrade_for_additions()
integration_utils = FIntegrationUtils.FIntegrationUtils()
version = integration_utils.get_acm_version_override()

print (20*'*', "Started installing RegulatoryInfo tab", 20*'*')


EXTENSION_TO_MODIFY = [
'CInsDef_AVERAGE_FORWARD',
'CInsDef_BASKET_CLN',
'CInsDef_BASKET_CREDIT_DEFAULT_SWAP',
'CInsDef_BASKET_REPO',
'CInsDef_BASKET_SEC_LOAN',
'CInsDef_BILL',
'CInsDef_BOND',
'CInsDef_BUY_SELLBACK',
'CInsDef_CALL_DEPOSIT',
'CInsDef_CAP',
'CInsDef_CASH_PAYMENT',
'CInsDef_CD',
'CInsDef_CERTIFICATE',
'CInsDef_CFD',
'CInsDef_CLN',
'CInsDef_COLLATERAL',
'CInsDef_COMBINATION',
'CInsDef_COMMODITY',
'CInsDef_COMMODITY_INDEX',
'CInsDef_COMMODITY_VARIANT',
'CInsDef_CONVERTIBLE',
'CInsDef_CREDIT_BALANCE',
'CInsDef_CREDIT_DEFAULT_SWAP',
'CInsDef_CREDIT_INDEX',
'CInsDef_CURR_SWAP',
'CInsDef_DEPOSIT',
'CInsDef_DEPOSITARY_RECEIPT',
'CInsDef_DIVIDEND_POINT_INDEX',
'CInsDef_DUAL_CURR_BOND',
'CInsDef_EQUITY_INDEX',
'CInsDef_EQUITY_SWAP',
'CInsDef_ETF',
'CInsDef_FLEXI_BOND',
'CInsDef_FLOOR',
'CInsDef_FRA',
'CInsDef_FREEDEF_CASHFLOW',
'CInsDef_FRN',
'CInsDef_FUND',
'CInsDef_FUTURE',
'CInsDef_FX_NDF',
'CInsDef_INDEX_LINKED_BOND',
'CInsDef_INDEX_LINKED_SWAP',
'CInsDef_MBS_ABS',
'CInsDef_OPTION',
'CInsDef_PRECIOUS_METAL_CASH',
'CInsDef_PRECIOUS_METAL_OPTION',
'CInsDef_PRICE_INDEX',
'CInsDef_PRICE_SWAP',
'CInsDef_PROMIS_LOAN',
'CInsDef_RATE_INDEX',
'CInsDef_REPO',
'CInsDef_ROLLING_SCHEDULE',
'CInsDef_SECURITY_LOAN',
'CInsDef_SECURITY_TRANSFER',
'CInsDef_STOCK',
'CInsDef_SWAP',
'CInsDef_TOTAL_RETURN_SWAP',
'CInsDef_VARIANCE_SWAP',
'CInsDef_VOLATILITY_SWAP',
'CInsDef_WARRANT',
'CInsDef_ZERO',
'CInsDef_FX_CASH',
'CInsDef_FX_OPTION']

module = 'RegulatorySupport'

context = acm.GetDefaultContext()
editModule = ''
if module in context.ModuleNames():
    editModule = acm.FExtensionModule[module]
    if editModule:
        print ('Installing RegulatorySupport tab in module %s'%(editModule.Name()))

def insert_into_context(extension, searchLayout, actualSearchLayout, referenceLayout, insert_location):
    custom_pane = 'CustomPanes_' + insert_location
    ext = context.GetExtension(acm.FExtensionValue, extension, custom_pane)
    extVal = ext.Value().strip()
    searchPos = -1
    searchPos = extVal.find(referenceLayout)
    regPos = extVal.find(searchLayout)
    if regPos != -1 and regPos > searchPos:#it means it needs to be removed from here and placed before the Accounts tab
        extVal = extVal.replace(searchLayout, '')
    regPos = extVal.find(actualSearchLayout)
    if regPos != -1:
        extVal = extVal.replace(actualSearchLayout, '')
    if not extVal.count(searchLayout):
        if searchPos == -1:#it means this is not found at all
            var_msg = ' '
            if insert_location == 'Trade':
                var_msg = ' on instruments of type '
            print ("Regulatory GUI to be inserted after tab <%s> is not found in layout. Hence, inserting Regulatory as the last tab for %s%s<%s>."%(referenceLayout, insert_location, var_msg, e))
            extVal = extVal + searchLayout
        else:
            extVal = extVal[0 : searchPos + len(referenceLayout)] + searchLayout + extVal[searchPos + len(referenceLayout): ]
    text = '[%s]%s:%s\n%s' %(editModule.Name(), e, custom_pane, extVal)
    context.EditImport('FExtensionValue', text, False, editModule)
    return context


if editModule:
    try:
        for e in EXTENSION_TO_MODIFY:
            searchLayout = None
            try:
                actualSearchLayout = 'CustomLayout_InstrumentRegulatoryInfo,Regulatory;'
                if e in ['CInsDef_AVERAGE_FORWARD', 'CInsDef_COMBINATION', 'CInsDef_COMMODITY', 'CInsDef_COMMODITY_INDEX', 'CInsDef_COMMODITY_VARIANT',\
                        'CInsDef_FUTURE', 'CInsDef_PRECIOUS_METAL_CASH', 'CInsDef_PRICE_SWAP', 'CInsDef_OPTION', 'CInsDef_ROLLING_SCHEDULE',]:
                    searchLayout = 'CustomLayout_InsCommodityRegulatoryInfo,Regulatory;'
                else:
                    searchLayout = 'CustomLayout_InstrumentRegulatoryInfo,Regulatory;'
                referenceLayout = 'CustomLayout_InsIDPane,Identifiers;'
                context = insert_into_context(e, searchLayout, actualSearchLayout, referenceLayout, 'Instrument')
            except Exception as e:
                pass
            try:
                actualSearchLayout = 'CustomLayout_TradeRegulatoryInfo,Regulatory;'
                if e in ['CInsDef_AVERAGE_FORWARD', 'CInsDef_COMBINATION', 'CInsDef_COMMODITY_INDEX', 'CInsDef_COMMODITY_VARIANT',\
                        'CInsDef_FUTURE', 'CInsDef_PRECIOUS_METAL_CASH', 'CInsDef_PRICE_SWAP', 'CInsDef_OPTION', 'CInsDef_ROLLING_SCHEDULE',]:
                    searchLayout = 'CustomLayout_TradeCommodityRegulatoryInfo,Regulatory;'
                elif e == 'CInsDef_FX_CASH':
                    searchLayout = 'CustomLayout_TradeFXCashRegulatoryInfo,Regulatory;'
                elif e in ['CInsDef_STOCK', 'CInsDef_ZERO', 'CInsDef_PROMIS_LOAN', 'CInsDef_MBS_ABS', \
                           'CInsDef_INDEX_LINKED_BOND', 'CInsDef_FRN', 'CInsDef_FLEXI_BOND', \
                           'CInsDef_DUAL_CURR_BOND', 'CInsDef_CONVERTIBLE', 'CInsDef_COMMODITY', \
                           'CInsDef_CLN', 'CInsDef_BOND', 'CInsDef_BILL'] and version < 2017.2:
                    searchLayout = 'CustomLayout_TradeShortSellRegulatoryInfo,Regulatory;'
                elif e in ['CInsDef_COMMODITY']:
                    if version < 2017.2:
                        searchLayout = 'CustomLayout_TradeCommodityShortSellRegulatoryInfo,Regulatory;'
                    else:
                        searchLayout = 'CustomLayout_TradeCommodityRegulatoryInfo,Regulatory;'
                else:
                    searchLayout = 'CustomLayout_TradeRegulatoryInfo,Regulatory;'
                referenceLayout = 'CustomLayout_TradeAccountsPane,Accounts;'
                context = insert_into_context(e, searchLayout, actualSearchLayout, referenceLayout, 'Trade')
            except Exception as e:
                pass
        editModule.Commit()
        print ("Done installing RegulatorySupport tab")
    except Exception as e:
        print ("Exception occurred: %s"%(str(e)))
else:
    print ("Import 'RegulatorySupport' module into extension manager before running this script.")
