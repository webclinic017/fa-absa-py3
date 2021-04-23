
import os

import acm

DEPLOY_SCRIPT = r'c:\Program Files\Front\Front Arena\Prime\4.3\build_acmwebservice.cmd' 

msg = """In order to deploy the webservices you need to create a deployment script. 
By default this should be located at:

    "c:\Program Files\Front\Front Arena\Prime\4.3\Build and Deploy ACM WebService.cmd"

A suitable contents for the script is:

    c:
    cd "C:\Program Files\Front\Front Arena\Prime\4.3"
    acm_ws_generator.exe -server sundevil:9043 -user danroo01 -password intas -targettype wcf_selfhost
    pause

"""

def build_and_deploy_ws(*eii):
    if os.path.isfile(DEPLOY_SCRIPT):
        os.system('"' + DEPLOY_SCRIPT + '"')
    else:
        print (msg)
    

def publish_all_ws(eii):
    ext = eii.ExtensionObject().ActiveModule()
    print ("Publishing all custom functions in ", ext.Name(), " to Web Services")
    for func_extensions in ext.GetAllExtensions("FCustomFunction"):
        func_name = func_extensions.Name()
        func = None
        for num_params in range(20):
            tmp = acm.GetFunction(func_name, num_params)
            if tmp and func:
                raise Exception("Webservice funciton published twice with different parameters" + func_name)
            if tmp:
                func = tmp
        if not func:
            raise Exception("Function in extension but unavailable, restart PRIME..")        
        if not func.DocString():        
            doc_str = acm.FDocString(func)
            doc_str.Append("doc")
            ext.Add(func.DocClass(), doc_str)
            ext.AddMember(doc_str, "FDocString", "web services", "web services")
            print ("  ", func, " published")
        else:
            print ("  ", func, " already published")
        ext.Commit()
