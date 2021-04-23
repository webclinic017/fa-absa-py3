"""FUxNet - Helper methods for inserting CLR controls into a FUxLayoutBuilder
(c) Copyright 2013 by Sungard FRONT ARENA. All rights reserved.
   
"""
import acm
import clr
def BuildFullCLRName(prefix, fullClassName, assemblyName):
    
    fullCLRName = prefix + fullClassName + ',' + assemblyName
    return fullCLRName
    
def AddWinFormsReferences():
    #Add references to WinForms in order to simplify the adding of controls
    clr.AddReference('System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089')
    
"""
Helper method for adding a WinForms control to a FUxLayoutBuilder.

@params:
layoutBuilder is a FUxLayoutBuilder to which you want to add the control. The layout builder should be prepared with desired horizontal or vertical boxes before calling this method.
name is a string that contains the name of the control in the layout
fullClassName is a string that identifies the control that should be added. It should be in the format: "FullNamespacePath.ClassName", e.g "System.Windows.Forms.Button".
assemblyName is a string that identifies the assembly in which the control resides. It should be in the format:
"AssemblyName[,Version=x.x.x.x, Culture=culture, PublicKeyToken=xxxxxxxxxxxxxxxx]. The optional information(inside brackets) is used to specify a specific version of a control. Version 4.0.0.0 is default.
As an example the assemblyName could look like this: "System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089".
width is the width of the control.
height is the height of the control.
maxWidth is the maximum allowed width of the control.
maxHeight is the maximum allowed height of the control.
"""

def AddWinFormsControlToBuilder(layoutBuilder,name,fullClassName,assemblyName,width=-1,height=-1,maxWidth=-1,maxHeight=-1):
    AddWinFormsReferences()
    fullCLRName = BuildFullCLRName("winForms.", fullClassName, assemblyName)
    layoutBuilder.AddCustom(name, fullCLRName, width, height, maxWidth, maxHeight)
    
