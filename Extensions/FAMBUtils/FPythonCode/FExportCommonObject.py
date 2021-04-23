
import acm

def CreateFileSelection(filter):
    fs = acm.FFileSelection()
    fs.PickExistingFile(False)
    fs.FileFilter = filter
    return fs
    

def WriteToFile(commonobjects, formatterclass, fileSelection):
    gen = acm.FAMBAMessageGenerator()
    ambamessages = acm.FAMBAMessage()
    ambamessages.Type("MESSAGES")
    for commonobject in commonobjects:
        ambamessages.AddMessage(gen.Generate(commonobject))
    output = acm.FCharacterOutputFileStream(fileSelection.SelectedFile())
    taggedmessformatter = formatterclass()
    taggedmessformatter.FormatStream(output, ambamessages)
    output.Close()
    
    
    
def ExportCommonObjectAsXMLCB(eii):
    commonobj = eii.ExtensionObject()        
    fs = CreateFileSelection("XML Files (*.xml)|*.xml|All files (*.*)|*.*||")
    shell = eii.Parameter('shell')
    if acm.UX().Dialogs().BrowseForFile(shell, fs ):
        WriteToFile(commonobj, acm.FTaggedMessageXMLFormatter, fs)
    
    
    
def ExportCommonObjectAsXMLCBFromAppMenu(eii):
    commonobj = eii.ExtensionObject().CurrentObject()      
    fs = CreateFileSelection("XML Files (*.xml)|*.xml|All files (*.*)|*.*||")
    shell = eii.Parameter('shell')
    if not commonobj:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'No FCommonObject Selected!')
    elif acm.UX().Dialogs().BrowseForFile(shell, fs ):
        WriteToFile([commonobj], acm.FTaggedMessageXMLFormatter, fs)        
        


