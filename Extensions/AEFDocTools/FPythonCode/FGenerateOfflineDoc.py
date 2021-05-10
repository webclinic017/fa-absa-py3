
import acm


context = acm.GetDefaultContext()
modelDescStr = acm.GetDefaultValueFromName(context, acm.FObject, "AEFBrowser - content")
modelDescLst = modelDescStr.split("\n")
models = acm.FArray()

for a in modelDescLst :
    model = acm.FExplorerNodeModel()
    model.Substitute("context", acm.GetDefaultContext())
    model.Substitute("user", acm.User())
    model.Initialize(a)
    models.Add(model)

writer = acm.FReStructuredTextToHTMLFileWriter()
writer.WriteToFile('c:\\temp\\OfflineDoc', models)
