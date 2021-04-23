""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeModuleAdmin.py"
from __future__ import print_function
import acm

class ModuleIndex:
    PARAMETER = 0
    HOOKS = 1
    
class ModuleAdministrator:

    __thisAdministrator = None
    
    def __init__(self):
        if ModuleAdministrator.__thisAdministrator:
            raise ModuleAdministrator.__thisAdministrator

        self.__modules = dict()
        ModuleAdministrator.__thisAdministrator = self
        
    def GetModule(self, moduleIndex):
        module = None
        name = self.ModuleNameFromIndex(moduleIndex)
        if (moduleIndex in self.__modules):
            module = self.__modules[moduleIndex]
        if not module:
            module = acm.FAel[self.ModuleNameFromIndex(moduleIndex)]
        if not module:
            module = acm.FAel()
            module.Name(self.ModuleNameFromIndex(moduleIndex))
            print(name + ' created')
        if (moduleIndex not in self.__modules):
            self.__modules[moduleIndex] = module
        return module
        
    def ModuleNameFromIndex(self, moduleIndex):
        if moduleIndex == 0:
            return 'FSettlementParameters'
        elif moduleIndex == 1:
            return 'FSettlementHooks'
        else:
            return ''

    def AddVariableAndValue(self, moduleIndex, varName, value):
        res = False
        module = GetModuleAdministrator().GetModule(moduleIndex)
        if (module):
            module.Text(module.Text() + '\n' + varName + ' = ' + str(value) + '\n')
            res = True
        return res

    def AddFreeTextString(self, moduleIndex, text):
        res = False
        module = GetModuleAdministrator().GetModule(moduleIndex)
        if (module):
            module.Text(module.Text() + '\n' + str(text) + '\n')
            res = True
        return res

    def SaveModule(self, moduleIndex):
        res = False
        module = GetModuleAdministrator().GetModule(moduleIndex)
        if module:
            try:
                module.Commit()
                self.__modules[moduleIndex] = module
                res = True
                print('Saved module: ' + GetModuleAdministrator().ModuleNameFromIndex(moduleIndex))
            except Exception as e:
                print('Could not save the module with name %s. %s' % (GetModuleAdministrator().ModuleNameFromIndex(moduleIndex), str(e)))
                    
        return res    
        

def GetModuleAdministrator(singletonModuleAdmin = ModuleAdministrator):
    moduleAdmin = None
    try:
        moduleAdmin = singletonModuleAdmin()
    except ModuleAdministrator as anInstance:
        moduleAdmin = anInstance
    return moduleAdmin

