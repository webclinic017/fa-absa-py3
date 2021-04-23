import acm

print(20*'*', "Started installing clearing tab", 20*'*')

MODULE_NAMES = ['AMWIDealTaker', 'AMWIDealInitiator', 'FManualClearing']

EXTENSION_NAME = 'CustomPanes_Trade'

EXTENSION_TO_MODIFY = [
'CInsDef_BASKET_CREDIT_DEFAULT_SWAP',
'CInsDef_CAP',
'CInsDef_CREDIT_DEFAULT_SWAP',
'CInsDef_CURR_SWAP',
'CInsDef_DIVIDEND_POINT_INDEX',
'CInsDef_EQUITY_INDEX',
'CInsDef_EQUITY_SWAP',
'CInsDef_FLOOR',
'CInsDef_FRA',
'CInsDef_INDEX_LINKED_SWAP',
'CInsDef_OPTION',
'CInsDef_SWAP',
'CInsDef_TOTAL_RETURN_SWAP',
'CInsDef_VARIANCE_SWAP',
'CInsDef_FUTURE'
]

context = acm.GetDefaultContext()
editModule = ''
for module in MODULE_NAMES:
    if module in context.ModuleNames():
        editModule = acm.FExtensionModule[module]
        if editModule:
            print('Installing clearing tab in module %s'%(editModule.Name()))
            break
if editModule:
    try:
        for e in EXTENSION_TO_MODIFY:
            try:
                ext = context.GetExtension(acm.FExtensionValue, e, EXTENSION_NAME)
                extVal = ext.Value().strip()
                if not extVal.count('CustomLayout_Clearing,Clearing'):
                    extVal = extVal + 'CustomLayout_Clearing,Clearing;'
                    text = '[%s]%s:%s\n%s' %(editModule.Name(), e, EXTENSION_NAME, extVal)
                    context.EditImport('FExtensionValue', text, False, editModule)
            except Exception, e:
                pass
        editModule.Commit()
        print("Done installing clearing tab")
    except Exception, e:
        print("Exception occurred: %s"%(str(e)))
else:
    print("Import 'AMWI' module into extension manager before running this script.")


