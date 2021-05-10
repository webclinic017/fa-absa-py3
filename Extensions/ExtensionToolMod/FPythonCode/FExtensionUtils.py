from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FExtensionUtils - Utility functions when working with extensions 

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import re
import sets
import string

import acm


operators = sets.Set(['+','-','*','/', 'or','and','not','==','<>','<','>','<=','>=',\
                     ',','=',':=',':','\'','?',':*'])
operators.add('->')
constant_identifiers = sets.Set(['true','false','nil','default','object','tag'])

def sorted_list(l):
    """Returns a sorted string, (compares strings caseinsensitivly)"""
    sortlist = l[:]
    sortlist.sort(lambda a, b: cmp(a.upper(),b.upper()))
    return sortlist
       

# ----------------------------------------------------------------------------
# FRONT
# Front specific utility class
class PLoop:
    """ Adapter class to loop over prime collections  as if they were AEL sequences"""
    def __init__(self,collection):
        self.collection = collection.AsArray()
        self.len = self.collection.Size()
    def __getitem__(self,i):
        if self.len > i:
            return self.collection.At(i)
        else:
            raise IndexError


def acmGetAllSubclasses(klass):
    """Get all subclasses inclusive for klass"""
    classes = []
    for sub in PLoop(klass.Subclasses()):
        classes.extend(acmGetAllSubclasses(sub))
    classes.append(klass)
    return classes


class ExtensionDefinition(object):
    """Representation of an ExtensionDefinition in parsed form"""
    def __init__(self, module_name, class_name, extension_name):
        """Initialize extensionDefinition, exttokens shoulf be a Set"""
        self.module_name = module_name
        self.class_name = class_name
        self.extension_name = extension_name    
    def __str__(self):
        return "[%s]%s:%s" % (self.module_name, self.class_name, self.extension_name)
    def __repr__(self):
        return str(self)
    def __cmp__(self, other):
        return cmp((self.extension_name.upper(), self.class_name, self.module_name),\
                (other.extension_name.upper(), other.class_name, other.module_name))
    def __eq__(self, other):
        return self.extension_name == other.extension_name and self.class_name == other.class_name\
                and self.module_name == other.module_name
    def __hash__(self):
        return hash(str(self))

class ColumnDefinition(ExtensionDefinition):
    def __init__(self, module_name, class_name, extension_name, attribute_dictionary):
        ExtensionDefinition.__init__(self, module_name, class_name, extension_name)
        self.attribute_dictionary = attribute_dictionary
        self.type = "ColumnDefinition"
    def create_definition(self):
        """ Creates a definiton

        Returns: <str> "[module_name]class_name:extension_name =
                          attribute_name=attribute_value
                              ...
                            " """
        returnstring = []
        returnstring.append("%s =\n" % (self, ))
        for key in sorted_list(self.attribute_dictionary.keys()):
            returnstring.append("  %s=%s\n" % (key,self.attribute_dictionary[key]))
            
        return "".join(returnstring)
    def create_from_definition(def_str):
        """Basic parsing of referenced from columns
        
        Returns: ExtensionDefinition"""
        
        column_attribute_dictionary = {}
        module_name, class_name, extension_name = None, None, None
        for line in def_str.split("\n"):
            # Match: [contextname]clasname:extensionname= 
            match_column_definition = re.match(r"\[([\w\._\- /]+)\]([\w]+):([\w\.\(\) /%\-&]+) =.*", line)
            if match_column_definition:
                module_name, class_name, extension_name = match_column_definition.groups()
            # Match:   attributename=atribute value
            match_column_attribute = re.match(r"  ([\w]+)=([\w\.\(\) /%\-&]+)", line)
            if match_column_attribute:
                attribute_name, attribute_value = match_column_attribute.groups()
                column_attribute_dictionary[attribute_name]= attribute_value
        if module_name and class_name and extension_name:
            return ColumnDefinition(module_name, class_name, extension_name,\
                column_attribute_dictionary)
        return None
    create_from_definition = staticmethod(create_from_definition)


class ExtensionAttribute(ExtensionDefinition):
    """Representation of an ExtensionAttribute in parsed form"""
    def __init__(self, module_name, class_name, extension_name, extcode, exttokens, extparsed):
        """Initialize extensionAttribute, exttokens shoulf be a Set"""
        ExtensionDefinition.__init__(self, module_name, class_name, extension_name)
        self.code = extcode
        self.tokens = exttokens
        self.parsed_code = extparsed
        self.type = "ExtensionAttribute"
    def create_definition(self):
        """ Creates a definiton

        Returns: <str> "[module_name]class_name:extension_name = extcode" """
        return "%s = %s\n" % (self, self.code)            
            
    def create_from_definition(definition):
        """Create from extension code"""
        def parse_adfl(adfl_code):
            adfl_code += ";"
            double_quote = False
            is_method = False
            start_char = -1
            extattr = {}
            methods = {}
            functions = {}
            const_ident = {}
            ops = {}
            consts_strings = {}
            for i, char in enumerate(adfl_code):
                if start_char >= i: continue
                if char in string.whitespace + "()[]{}":
                    continue
                if char == '"':
                    if not (double_quote and adfl_code[i-1] == "\\"):
                        if double_quote:
                            consts_strings.setdefault(adfl_code[start_char:i+1],[]).append(start_char)
                        double_quote = not double_quote
                        start_char = i
                elif double_quote:
                    continue
                elif char == ".":
                    is_method = True
                else:
                    word = re.split('[^a-zA-Z0-9_"]+', adfl_code[i:], 1)[0]
                    if not word:
                        for next_word in re.split('\W+', adfl_code[i:]):
                            if next_word:
                                word = next_word
                                break
                    offset = adfl_code[i:].find(word)
                    start_char = i + offset
                    for chars in re.split('\s', adfl_code[i:start_char]):
                        if chars in operators:
                            ops.setdefault(chars,[]).append(i + adfl_code[i:].find(chars))
                        if '"' in chars:
                            quote_pos = i + adfl_code[i:].find('"')
                            if not (double_quote and adfl_code[quote_pos - 1] == "\\"):
                                if double_quote:
                                    consts_strings.setdefault(adfl_code[start_char:quote_pos + 1],[]).append(start_char)
                                double_quote = not double_quote
                                start_char = quote_pos
                            word = ""
                            break
                    if not word: continue
                    if word in constant_identifiers:
                        const_ident.setdefault(word,[]).append(start_char)
                    elif word in operators:
                        ops.setdefault(word,[]).append(start_char)
                    elif word[0] in string.digits:
                        consts_strings.setdefault(word,[]).append(start_char)
                    elif is_method:
                        methods.setdefault(word,[]).append(start_char)
                    elif adfl_code[start_char + len(word)] == "(" or\
                        adfl_code[start_char + len(word)] == " " and\
                        adfl_code[start_char + len(word) + 1] in string.letters + string.digits + "_" and\
                        not re.split('\W+', adfl_code[start_char + len(word) + 1:], 1)[0] in operators:
                            functions.setdefault(word,[]).append(start_char)
                    else: extattr.setdefault(word,[]).append(start_char)
                    is_method = False
                    start_char += len(word) - 1
            return {"extattr":extattr, "methods":methods, "functions":functions,\
                    "const_ident":const_ident, "ops":ops, "consts_strings":consts_strings}       

        definition = definition.strip().replace("\n", " ")
        match = re.match(r"\[([\w\._\- /]+)\]([\w]+):([\w]+) = (.*)", definition)
        if match:
            module_name, class_name, extension_name, extcode = match.groups()
            #Seperate the adfl expression into tokens
            exttokens = sets.ImmutableSet( re.split(r'\W+', extcode) )
            parsed_code = parse_adfl(extcode)
            return ExtensionAttribute(module_name, class_name, extension_name,\
                extcode, exttokens, parsed_code)
        elif definition:
            print ("Failed to match : -'" +  definition +"'-")
    create_from_definition = staticmethod(create_from_definition)

class PythonCode(ExtensionDefinition):
    def __init__(self, module_name, class_name, extension_name, python_code):
        ExtensionDefinition.__init__(self, module_name, class_name, extension_name)
        self.code = python_code
        self.methods = self.get_python_methods(python_code)
        self.tokens = sets.ImmutableSet( re.split(r'\W+', python_code) )
        self.type = "PythonCode"
    def get_python_methods(python_code):
        methods = {}
        for line in python_code.split('\n'):
            if line[:4] == "def " and line[-1:] == ":":
                method = line[4:line.find('(')]
                args = line[line.find('(')+1:line.rfind(')')].split(", ")
                methods[method] = args
        return methods
    def create_definition(self):
        return "%s\n%s¤\n" % (self, self.code)
    def create_from_definition(def_str):
        module_name, class_name, extension_name = None, None, None
        # Match: [contextname]clasname:extensionname 
        match_column_definition = re.match(r"\[([\w\._\- /]+)\]([\w]+):([\w\.\(\) /%\-&]+)\n(.*\n)", def_str)
        if match_column_definition:
            module_name, class_name, extension_name, python_code = match_column_definition.groups()
            pytmod = "[%s]%s:%s\n" % (module_name, class_name, extension_name)
            python_code = def_str[def_str.find(pytmod)+len(pytmod):]
            return PythonCode(module_name, class_name, extension_name, python_code)
        else:
            print ("Failed to match :\n" +  def_str)
    
    create_from_definition = staticmethod(create_from_definition)
    get_python_methods = staticmethod(get_python_methods)
        
        
        
def get_extensions(context, exttype, name=None):
    """Get specified extension as string"""
    res = []
    for extname in context.ExtensionNames(exttype, None, 0, 0):
        if not name or extname.AsString() == name:
            res.append(context.EditExport(exttype, None, extname))
    if res:
        return "\n".join(res)
    return ""

def get_one_parsed_extension(exttype, module_name, class_name, extension_name): 
    dummy_context = acm.FExtensionContext()
    dummy_context.AddModule(module_name)
    
    if exttype == "FExtensionAttribute": split_on = ";\n"
    elif exttype == "FPythonCode": split_on = "¤\n\n"
    else: split_on ="\n\n"

    extensions = dummy_context.EditExport(exttype, None, extension_name).split(split_on)
    for ext in extensions:
        ext = ext.strip().replace("\n", " ")
        match = re.match(r"\[([\w\._\- /]+)\]([\w]+):([\w]+) = (.*)", ext)
        if match:
            ext_module, ext_class, ext_name, extcode = match.groups()
            if ext_class == class_name:
                dummy_context.RemoveModule(module_name)
                return ExtensionAttribute.create_from_definition(ext)
    
    dummy_context.RemoveModule(module_name)
    return None

def create_composit_index(seq, attributenames):
    res = {}   
    for obj in seq:
        key = []
        for attribute in attributenames.split(" "):
            key.append(getattr(obj, attribute))            
        res.setdefault(len(key) == 1 and key[0] or tuple(key),[]).append(obj)
    return res

def flatten(array):
    returnarray=[]
    for arr in array:
        if isinstance(arr, list):
            returnarray.extend(flatten(arr))
        else:
            returnarray.append(arr)
    return returnarray

def get_extensiontype_in_module(module, exttype, includeBuiltInModules):
    if isinstance(module, list):
        eA = sets.Set()
        for mod in sets.Set(flatten(module)):
            eA |= sets.Set(get_extensiontype_in_module(mod, exttype, includeBuiltInModules))
    elif isinstance(module, dict):
        eA = sets.Set()
        for mod in sets.Set(module.keys()) - sets.Set(["%user", "%group", "%org"]):
            eA |= sets.Set(get_extensiontype_in_module(mod, exttype, includeBuiltInModules))
    else:
        if exttype == "FExtensionAttribute":
            split_on = ";\n"
            extclass = ExtensionAttribute
        elif exttype == "FPythonCode":
            split_on = "¤\n\n"
            extclass = PythonCode
        else:
            split_on ="\n\n"
            extclass = ColumnDefinition
            
        dummy_context=acm.FExtensionContext()
        dummy_context.AddModule(module)
        if includeBuiltInModules or not dummy_context.Modules()[-1].IsBuiltIn():
            eA = sets.Set([extclass.create_from_definition(item) \
                for item in get_extensions(dummy_context,exttype).split(split_on) \
                if item and extclass.create_from_definition(item)])
        else : eA = sets.Set()
        dummy_context.RemoveModule(module)
    return list(eA)

def get_python_in_module(module, includeBuiltInModules = True):
    return get_extensiontype_in_module(module, "FPythonCode", includeBuiltInModules)

def get_extension_in_module(module, includeBuiltInModules = True):
    return get_extensiontype_in_module(module, "FExtensionAttribute", includeBuiltInModules)
    
def get_column_in_module(module, includeBuiltInModules = True):
    return get_extensiontype_in_module(module, "FColumnDefinition", includeBuiltInModules)
    
def get_menuextension_in_module(module, includeBuiltInModules = True):
    return get_extensiontype_in_module(module, "FMenuExtension", includeBuiltInModules)

def get_expressiontransform_in_module(module, includeBuiltInModules = True):
    return get_extensiontype_in_module(module, "FExpressionTransform", includeBuiltInModules)

def get_columnappearance_in_module(module, includeBuiltInModules = True):
    return get_extensiontype_in_module(module, "FColumnAppearance", includeBuiltInModules)

class moduleInfo:
    def __init__(self, moduleLevel, modulesInContext, isBuiltIn):
        self.moduleLevel = moduleLevel
        self.modulesInContext = modulesInContext
        self.isBuiltIn = isBuiltIn
    def IsBuiltIn(self):
        return self.isBuiltIn
    def ModulesInContext(self):
        return self.modulesInContext
    def ModuleLevel(self):
        return self.moduleLevel

class moduleDict(dict):
    def __str__(self):
        return str(self.moduleNames())
    def modules(self): return self.keys()
    def moduleNames(self):
        names = sets.Set(self.keys()) - sets.Set(["%user", "%group", "%org"])
        names = list(names)
        names.sort(lambda a,b: cmp((self[a].moduleLevel, a), (self[b].moduleLevel, b)))
        return names
    def builtInModules(self):
        returnDict = moduleDict()
        for mod in self.modules():
            if self[mod].isBuiltIn:
                returnDict[mod] = self[mod]
        return returnDict
    def nonBuiltInModules(self):
        returnDict = moduleDict()
        for mod in self.modules():
            if not self[mod].isBuiltIn:
                returnDict[mod] = self[mod]
        return returnDict
    def get_modules_at_level(self, level):
        returnDict = moduleDict()
        for mod in self.moduleName():
            if self[mod].moduleLevel <= level:
                if self[mod].moduleLevel == level:
                    returnDict[mod] = self[mod]
            else: break
        return returnDict
    def user_modules(self):
        if not self.has_key("%user"):
            return None
        return get_modules_at_level(self["%user"].moduleLevel)
    def gruop_modules(self):
        if not self.has_key("%group"):
            return None
        return get_modules_at_level(self["%group"].moduleLevel)
    def organisation_modules(self):
        if not self.has_key("%org"):
            return None
        return get_modules_at_level(self["%org"].moduleLevel)
    def get_context(self):
        context = acm.FExtensionContext()
        for mod in self.moduleNames(): context.AddModule(mod)
        return context
    def StringKey(self):
        if not self.modules(): return "[]"
        res = ["["]
        for i, mod in enumerate(self.moduleNames()):
            res.append(mod)
            res.append(", ")
            if i == 4 and len(self.modules()) > 6: 
                res[-1] = "..."
                res.append("...")
                break
        res[-1] = "]"
        return "".join(res)
        
def get_moduleDict(modules):
    moduleLevelDict = moduleDict()
    dummy_context = acm.FExtensionContext()
    for i, mod in enumerate(modules):
        dummy_context.AddModule(mod)
        moduleLevelDict[mod.StringKey()] = moduleInfo\
            (i, sets.Set([module.StringKey() for module in modules]), dummy_context.Modules()[-1].IsBuiltIn())
        dummy_context.RemoveModule(mod)
    return moduleLevelDict
    
def get_modules(users, context):
    moduleLevelDict = moduleDict()
    if not users:
        for i, module in enumerate(context.Modules()):
            moduleLevelDict[module.StringKey()] = moduleInfo\
                (i, sets.Set([mod.StringKey() for mod in context.Modules()]), module.IsBuiltIn())
        return moduleLevelDict
    
    usermod, groupmod, orgmod = sets.Set(), sets.Set(), sets.Set()
    modInAllContext = sets.Set(context.ModuleNames()) - sets.Set(["%user", "%group", "%org"])
    hasUserMod, hasGroupMod, hasOrgMod = False, False, False
    
    for mod in context.ModuleNames():
        if mod == "%user": hasUserMod = True
        elif mod == "%group": hasGroupMod = True
        elif mod == "%org": hasOrgMod = True
        
    for user in users:
        if hasUserMod and acm.FExtensionModule[user.Name()]:
            usermod.add(user)
        if user.UserGroup():
            if hasGroupMod and not user.UserGroup() in groupmod\
                        and acm.FExtensionModule[user.UserGroup().Name()]:
                groupmod.add(user.UserGroup())
            if hasOrgMod and user.UserGroup().Organisation() and \
                not user.UserGroup().Organisation() in orgmod \
                and acm.FExtensionModule[user.UserGroup().Organisation().Name()]:
                orgmod.add(user.UserGroup().Organisation())
    
    dummy_context = acm.FExtensionContext()
    for i, mod in enumerate(context.ModuleNames()):
        moduleLevelDict[mod] = moduleInfo(i, sets.Set(), False)
        if mod == "%user":
            for user in usermod:
                modsInCont = sets.Set(modInAllContext)
                if hasGroupMod and user.UserGroup() and user.UserGroup() in groupmod:
                    modsInCont.add(user.UserGroup().Name())
                if hasOrgMod and user.UserGroup() and user.UserGroup().Organisation()\
                    and user.UserGroup().Organisation() in orgmod:
                    modsInCont.add(user.UserGroup().Organisation().Name())
                dummy_context.AddModule(user.Name())
                moduleLevelDict[user.Name()] = moduleInfo(i, modsInCont, dummy_context.Modules()[-1].IsBuiltIn())
                dummy_context
        elif mod == "%group":
            for group in groupmod:
                modsInCont = sets.Set(modInAllContext)
                if hasUserMod:
                    modsInCont |= sets.Set([user.Name() for user in (sets.Set(group.Users()) & usermod)])
                if hasOrgMod and group.Organisation()\
                    and group.Organisation() in orgmod:
                    modsInCont.add(group.Organisation().Name())
                dummy_context.AddModule(group.Name())
                moduleLevelDict[group.Name()] = moduleInfo(i, modsInCont, dummy_context.Modules()[-1].IsBuiltIn())
                dummy_context.RemoveModule(group.Name())
        elif mod == "%org":
            for org in orgmod:
                modsInCont = sets.Set(modInAllContext)
                groups = sets.Set(org.UserGroups()) & groupmod
                groupnames = sets.Set()
                usernames = sets.Set()
                for group in groups:
                    groupnames.add(group.Name())
                    usernames |= sets.Set([user.Name() for user in (sets.Set(group.Users()) & usermod)])
                if hasUserMod:
                    modsInCont |= usernames
                if hasGroupMod:
                    modsInCont |= groupnames
                dummy_context.AddModule(org.Name())
                moduleLevelDict[org.Name()] = moduleInfo(i, modsInCont, dummy_context.Modules()[-1].IsBuiltIn())
                dummy_context.RemoveModule(org.Name())
        else:
            if acm.FExtensionModule[mod]:
                modsInCont = sets.Set(modInAllContext)
                if hasUserMod:
                    modsInCont |= sets.Set([user.Name() for user in usermod])
                if hasGroupMod:
                    modsInCont |= sets.Set([group.Name() for group in groupmod])
                if hasOrgMod:
                    modsInCont |= sets.Set([org.Name() for org in orgmod])
                dummy_context.AddModule(mod)
                moduleLevelDict[mod] = moduleInfo(i, modsInCont, dummy_context.Modules()[-1].IsBuiltIn())
                dummy_context.RemoveModule(mod)
                
    return moduleLevelDict

class UpdatedExtension:
    def __init__(self, original_code = "", extensions_to_update = {}, updated_extensions = {}):
        self.original_code = original_code
        self.updated_extensions = updated_extensions
        self.extensions_to_update = extensions_to_update
    def __str__(self):
        return str("%s %s %s " % (self.original_code, str(self.extensions_to_update), str(self.updated_extensions)))
    def __repr__(self):
        return str(self)
        
        
def dictionary_from_string(dictionary_string):
    if not dictionary_string:
        return {}
    dictionary = {}
    if dictionary_string[0] == "{":
        dictionary_string = dictionary_string[1:]
    if dictionary_string[-1] == "}":
        dictionary_string = dictionary_string[:-1]    
    dictionary_string = dictionary_string.replace("'", "").replace(" ", "")
    extpos = dictionary_string.find(',')
    while(extpos != -1):
        key = dictionary_string[:dictionary_string.find(':')]
        value = dictionary_string[dictionary_string.find(':') + 1: extpos]
        dictionary[key] = value
        dictionary_string = dictionary_string[extpos + 1:]
        extpos = dictionary_string.find(',')
    extpos = dictionary_string.find(':')
    if extpos != -1:
        key = dictionary_string[:extpos]
        value = dictionary_string[extpos + 1:]
        dictionary[key] = value
        
    return dictionary




