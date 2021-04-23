
import acm

def updateAddInfoColPostInput(row, col, calcval, val, operation):
    """
    Function can be used as postinput hook for additional info column
    It will save the add info values entered in the column, or delete
    it if 'delete' is pressed.
    
    The idea is to keep the hook generic, so the 'Name' of your column
    should match the Additional Info Name.
    
    Below an example of the column def and extension attr.
    It could be tricky to get it to update correctly and not to appear
    simulated etc.
    
    FColumnDefinition:
    [RAUTENCH]FTradingSheet:CallFloatSpreadAddInfo =
      Class=Instrument
      Description=callFloatSpreadAddInfo...
      ExtensionAttribute=callFloatSpreadAddInfo
      GroupLabel=aaa
      LabelList=callFloatSpreadAddInfo
      Name=CallFloatSpread
      OnPostInputHook=AbsaUtilities.updateAddInfoColPostInput
      ShowSimulItalic=Disabled
      ShowSimulState=Disabled
      SoftSimulDefault=Enabled

    FExtensionAttribute:
    [RAUTENCH]FInstrument:callFloatSpreadAddInfo = object.AdditionalInfo.CallFloatSpread;
    """

    ins = row.Instrument()
    addInfoName = col.StringKey()
    
    if str(operation) == 'insert':
        if ins.AdditionalInfo().GetProperty(addInfoName) == None:
            addInfo = acm.FAdditionalInfo()
            addInfo.Recaddr(ins.Oid())
            addInfo.AddInf(acm.FAdditionalInfoSpec[addInfoName])
            addInfo.FieldValue(str(val))
            try:
                addInfo.Commit()
            except Exception, e:
                print 'Commit failed', e

        else:
            addInfo = acm.FAdditionalInfo.Select('recaddr = %i' %ins.Oid())
            for i in addInfo:
                if i.AddInf().Name() == addInfoName:
                    i.FieldValue(val)
                    try:
                        i.Commit()
                    except Exception, e:
                        print 'Commit failed', e
                    break
      
    elif str(operation) == 'remove':
        addInfo = acm.FAdditionalInfo.Select('recaddr = %i' %ins.Oid())
        for i in addInfo:
            if i.AddInf().Name() == addInfoName:
                i.Delete()

    calcval.Unsimulate()

