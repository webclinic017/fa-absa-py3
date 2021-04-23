""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLAmbaHook.py"

from FACLObjectGateway import FACLObjectGateway

def sender_modify(mbfObject, subject):
    gateway = FACLObjectGateway()
    try:
        mbfObjectToReturn = gateway.Process(mbfObject)
        if mbfObjectToReturn:
            return (mbfObjectToReturn, subject)
        else:
            return None
    except Exception as e:
        import traceback
        print('Failed to process message:\n%s\n%s' % (mbfObject.mbf_object_to_string(), traceback.format_exc()))            
        return None
