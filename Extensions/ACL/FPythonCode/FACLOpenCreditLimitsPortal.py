""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLOpenCreditLimitsPortal.py"

import acm
import webbrowser

def launch_browser_url(eii):
    from FACLParameters import PrimeSettings 
    webbrowser.open_new_tab(PrimeSettings.limitsServerUrl)
    
    
def launch_browser_url_deal(eii):
    extObject = eii.ExtensionObject()
    trade = extObject.OriginalTrade()
    if trade:
        acrRef = trade.AdditionalInfo().ACR_REF()
        if acrRef:
            from FACLParameters import PrimeSettings
            serverString = PrimeSettings.limitsServerUrl
            if not serverString[-1] == "/":
                serverString += "/"
            urlString = '%sdefault.aspx?ClassID=0&ID=%s&HostID=135' % (serverString, acrRef)
            webbrowser.open_new_tab(urlString)
        else:
            print("The trade %s does not have a ACL reference and most likely does not exist in ACL" % (trade.Oid())) 
    else:
        print("The trade is not saved and can not be opened in ACL")
