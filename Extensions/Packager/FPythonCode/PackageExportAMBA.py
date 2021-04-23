"""
    PackageExportAMBA
    
    (C)2012-2018 FIS Front Arena
    
    Handles the AMBA file export
    
    20120514 Richard Ludwig


    Extension Manager extension type FAMBADefinition it is possible to have AMBA settings per Object type.
    
    An example for FInstrument:
    
    [PackageTagger]FInstrument:Configurator =
      add_fields={{instrument,strike_price},{instrument,free_text}}
      add_referring={leg,insaddr}
      add_ref_fields={{trade,insaddr,instrument,instype}}
      nice_enum_names=1
      remove_fields={{instrument,free_text}}
      remove_ref_fields={{instrument,settle_calnbr,calendar,calid}}
      show_all_fields=0
      show_protection=1
      show_seqnbr=0
      use_regional_settings=0
      utc_timestamps=1
    
"""
import acm
import FRunScriptGUI
import urllib
import PackageDependents
reload(PackageDependents)

try:
    import PackageFilter
except:
    PackageFilter = None

def ExportCommonObjectAsXMLCB(eii):
    commonobj = eii.ExtensionObject()        
    shell = eii.Parameter('shell')
    follow = str(eii.MenuExtension().At( "Follow")) == "True"
    ExportCommonObject(shell, commonobj, follow = follow)


def ExportCommonObjectAsXMLCBFromAppMenu(eii):
    commonobj = eii.ExtensionObject().CurrentObject()
    shell = eii.Parameter('shell')
    ExportCommonObject(shell, commonobj)

def getAMBADefinition(commonobject):
    context = acm.GetDefaultContext()
    configName = context.GetExtension('FParameters', 'FObject', 'Configurator').Value().At('FAMBADefinitionName')

    par = context.GetExtension('FAMBADefinition', commonobject.Class(), configName )
    if par:
        return par
    else:
        emptyPar = acm.FAMBADefinition()
        emptyPar.Name('Empty')

        return emptyPar


def generateFilename( objectList, package):
    # Create a nice filename
    filename = "mixedobjects"
    if package != None:
        filename = package
        
    elif len(objectList) == 1: # and hasattr(objectList[0],'Name'):
        cls = objectList[0].Class()
        try:
            if cls.UniqueNameAttribute():
                method = cls.UniqueNameAttribute().GetMethod().Name()
            else:
                method = cls.UniqueAttribute().GetMethod().Name()
        except:
            method = 'StringKey'
            
        metCall = getattr(objectList[0], str(method))
        if metCall == None:
            metCall = getattr(objectList[0], 'Oid')
        uniqueName = metCall()
        
        filename = urllib.quote( ("%s_%s"%(objectList[0].ClassName(), uniqueName)).replace(' ', '_'), ' @.')

    elif objectList[0].ClassName() == objectList[-1].ClassName():
        filename = objectList[0].ClassName()
    
    return filename


def WriteToFile(commonobjects, formatterclass, filename, typeUpdate=False):

    gen = acm.FAMBAMessageGenerator()
    taggedmessformatter = formatterclass()
    if str(filename).endswith('.xml'):
        try:
            output = acm.FCharacterOutputFileStream(filename)

            ambamessages = acm.FAMBAMessage()
            ambamessages.Type("MESSAGES")
            for commonobject in commonobjects:
                # Set FAMBADefinition
                par = getAMBADefinition(commonobject)
                gen.Parameters(par.Value())
                
                objMessage = gen.Generate(commonobject)
                messageType = objMessage.At('TYPE')
                objMessage.RemoveKeyString('TYPE')
                if typeUpdate:
                    objMessage.AtPut('TYPE', 'UPDATE_%s'%messageType)
                else:
                    objMessage.AtPut('TYPE', 'INSERT_%s'%messageType)
                
                ambamessages.AddMessage(objMessage)
                
            taggedmessformatter.FormatStream(output, ambamessages)
        finally:
            if output != None:
                output.Close()
    else:        
        try:
            output = acm.FCharacterOutputFileStream(filename)
            
            for commonobject in commonobjects:
                # Set FAMBADefinition
                par = getAMBADefinition(commonobject)
                gen.Parameters(par.Value())

                objMessage = gen.Generate(commonobject)
                messageType = objMessage.At('TYPE')
                objMessage.RemoveKeyString('TYPE')

                if typeUpdate:
                    objMessage.AtPut('TYPE', 'UPDATE_%s'%messageType)
                else:
                    objMessage.AtPut('TYPE', 'INSERT_%s'%messageType)

                taggedmessformatter.FormatStream(output, objMessage)
        finally:
            if output != None:
                output.Close()
    
        
def __UpdateReferenceSet(object, visited, dependencies):
    
    if object not in visited and object != None:
        # Marking object type as visited.
        visited.add(object)

        # Adding references defined in this package.
        for reference in PackageDependents.Dependents(object):
            __UpdateReferenceSet(reference, visited, dependencies)

        # Adding references out of object to list, if not already present.
        for reference in object.ReferencesOut():
            __UpdateReferenceSet(reference, visited, dependencies)
      
        # Adding object to list (after its dependencies).  
        dependencies.append(object)

        # Adding objects which depend on object.
        for reference in PackageDependents.Depends(object):
            __UpdateReferenceSet(reference, visited, dependencies)


def followDependents(objects):
    visited = set()
    dependencies = list()
    
    for object in objects:
        __UpdateReferenceSet(object, visited, dependencies)

    return dependencies

    
def ExportCommonObject(shell, commonobj, package = None, follow=False):
    if not commonobj:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'No FCommonObject Selected!')
        return

    fileSelection = FRunScriptGUI.OutputFileSelection("AMBA text files (*.txt)|*.txt|XML Files (*.xml)|*.xml|All files (*.*)|*.*||")
    
    objectList = [obj for obj in commonobj if hasattr(obj, 'ClassName')] # Strip header string objects
    if follow:
        objectList = followDependents(objectList)
    # Create a nice filename
    if package != None:
        fileSelection.SelectedFile(package)
    elif len(objectList) == 1: # and hasattr(objectList[0],'Name'):
        cls = objectList[0].Class()
        try:
            if cls.UniqueNameAttribute():
                method = cls.UniqueNameAttribute().GetMethod().Name()
            else:
                method = cls.UniqueAttribute().GetMethod().Name()
        except:
            method = 'StringKey'
            
        metCall = getattr(objectList[0], str(method))
        if metCall == None:
            metCall = getattr(objectList[0], 'Oid')
        uniqueName = metCall()
        
        filename = urllib.quote( ("%s_%s"%(objectList[0].ClassName(), uniqueName)).replace(' ', '_'), ' @.')

        fileSelection.SelectedFile(filename)
    elif objectList[0].ClassName() == objectList[-1].ClassName():
        fileSelection.SelectedFile(objectList[0].ClassName())

    if PackageFilter:
        reload(PackageFilter)
        objectList = PackageFilter.Filter(objectList)

    # Open file requester
    if acm.UX().Dialogs().BrowseForFile(shell, fileSelection ):
        if str(fileSelection.SelectedFile()).endswith('.xml'):
            WriteToFile(objectList, acm.FTaggedMessageXMLFormatter, fileSelection.SelectedFile(), typeUpdate=False)
        else:
            WriteToFile(objectList, acm.FTaggedMessageMBFormatter, fileSelection.SelectedFile(), typeUpdate=False)
