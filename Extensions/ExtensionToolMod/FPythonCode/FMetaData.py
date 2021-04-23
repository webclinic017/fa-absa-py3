from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FMetaData - Functions to generate and get data about available ACM methods 
    and extension attributes in Default

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import sets

import acm

import FExtensionUtils

def removeParamsFromMethod(methodString):
    #In >= 4.0 StringKey returns e.g. 'SetProperty(property, value)' while in < 4.0 it returns 'SetProperty'.
    #Remove (...) from the method string.
    import re
    if methodString.find('(') != -1:                            
        p = re.compile('\(.*\)')
        parameterList = p.findall(methodString)[0]
        methodString = methodString.replace(parameterList, '')        
        return methodString
    else:
        return methodString

def generate_meta_data(path):
    defaultModule = acm.FExtensionModule['Default']
    if not defaultModule:
        for em in acm.GetDefaultContext().Modules():
            if em.Name() == "Default":
                defaultModule=em
    print (defaultModule)
    extensionAttributes=FExtensionUtils.get_extension_in_module(defaultModule)
    print ("#", len(extensionAttributes), "ExtensionAttributes")
    extensionAttributes.sort()

    res=[]
    for ext in extensionAttributes:
        res.append(ext.create_definition())

    res.append('*'*30 + "  ACM Methods  " + '*'*30 +'\n')

    classes = [c for c in FExtensionUtils.acmGetAllSubclasses(acm.GetClass("FObject"))]
    classes.sort(lambda a, b:cmp(a.StringKey().upper(), b.StringKey().upper()))
    classNames = sets.Set([c.StringKey() for c in classes])
    
    print ("#", len(acm.AllMethodNames()), "ACM Methods")
    
    isDefFAdditionalInfoProxy = "FAdditionalInfoProxy" in classNames
    print ("Scanning ACM classes", end=" ")
    allMethods=sets.Set()
    d=0
    for klass in classes:
        if not d % int(len(classes)/20): print ('.', end=" ")
        d+=1
        for methods in klass.Methods().AsArray():
            for method in methods:
                if method and not (isDefFAdditionalInfoProxy and 
                            method.ReceiverClass().IncludesBehavior("FAdditionalInfoProxy")):
                    isOptional = 0
                    receiverOp = 0
                    if method.Operands():
                        if str(method.Operands()[0].Name()) == "receiver":
                            receiverOp = 1
                    for op in method.Operands():
                        if op.IsOptional():
                            isOptional += 1
                    for i in range(isOptional+1):
                        methodString = removeParamsFromMethod(method.StringKey())                                                
                        allMethods.add((methodString, len(method.Operands())-receiverOp-i))                        

    print ('.')
    methods=list(allMethods)
    methods.sort(lambda a, b:cmp((a[0].upper(), a[1]), (b[0].upper(), b[1])))

    for method in methods:
        res.append(method[0] + '\t' + str(method[1]) +  '\n')


    print ("#", len(classes), "Classes")
    print ("#", len(allMethods), "Methods") #methods


    print ("ACM Version", acm.Version())
    print ("Output file:", path + "Definitions_" + acm.Version())
    
    open(path + "Definitions_" + acm.Version(), 'w').write("".join(res))

class ACMMetaData:
    def __init__(self, fromVer, toVer, path="c:\\"):
        def get_extensions_and_methods(path, ver):
            defaultExtensionAttributes = sets.Set()
            file = open(path + "Definitions_" + ver, 'r')
            line = file.readline()
            while(line != str('*'*30 + "  ACM Methods  " + '*'*30 +'\n')):
                defaultExtensionAttributes.add(FExtensionUtils.ExtensionAttribute.create_from_definition(line))
                line = file.readline()
            acmMethods = {}
            line = file.readline()
            while(line):
                method, parameters = line.strip('\n').split('\t')
                acmMethods.setdefault(method, []).append(parameters)
                line = file.readline()
            file.close()
            return defaultExtensionAttributes, acmMethods
        
        self.fromVer = fromVer
        self.toVer = toVer
        
        defaultExtensionAttributes1, acmMethods1 = \
            get_extensions_and_methods(path, fromVer)
        defaultExtensionAttributes2, acmMethods2 = \
            get_extensions_and_methods(path, toVer)
        
        self.availableAttributes = defaultExtensionAttributes2
        self.removedAttributes = defaultExtensionAttributes1 - defaultExtensionAttributes2
        self.removedAcmMethods = sets.Set(acmMethods1.keys()) - sets.Set(acmMethods2.keys())
        
        self.changedAcmMethodOperands = {}
        for key in sets.Set(acmMethods1.keys()) & sets.Set(acmMethods2.keys()):
            operands1 = sets.Set(acmMethods1[key])
            operands2 = sets.Set(acmMethods2[key])
            removedOperands = list(operands1-operands2)
            if removedOperands:
                removedOperands.sort()
                commonOperands = list(operands1 & operands2)
                commonOperands.sort()
                newOperands = list(operands2)
                newOperands.sort()
                self.changedAcmMethodOperands[key]=(removedOperands, commonOperands, newOperands)
                
    def __nonzero__(self):
        return bool(self.fromVer and self.toVer and self.fromVer != self.toVer)





