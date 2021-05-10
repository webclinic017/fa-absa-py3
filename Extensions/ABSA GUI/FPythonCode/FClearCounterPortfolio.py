
def ContentsChanged(eii):
    insDefApp = eii.ExtensionObject()
    if not insDefApp.OriginalTrade():
        #This will clear counter portfolio if Ctrl+N
        insDefApp.EditTrade().MirrorPortfolio(None)
