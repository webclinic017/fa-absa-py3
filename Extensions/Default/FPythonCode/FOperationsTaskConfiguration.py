""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTaskConfiguration.py"

#-------------------------------------------------------------------------
class Configuration(object):
    
    #-------------------------------------------------------------------------
    def __init__(self, paramDict):
        super(Configuration, self).__init__()
        
        for key, value in paramDict.items():
            setattr(self, key, value)