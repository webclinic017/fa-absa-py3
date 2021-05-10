
import acm

name = 'CutOff-Time'

scenario = acm.FExplicitScenario()
scenario.Name(name)

shiftVector1 = acm.CreateReplaceShiftVector('trade inclusion datetime', None)
shiftVector1.AddReplaceShiftItem(acm.Time.NotADateTime(), 'NotADateTime')

shiftVector2 = acm.CreateReplaceShiftVector('use mark to market price today', None)
shiftVector2.AddReplaceShiftItem(acm.FEnumeration['EnumMtMTodayChoice'].Enumeration('No'), 'No')

scenario.AddShiftVector(shiftVector1)
scenario.AddShiftVector(shiftVector2)

storedScen = acm.FStoredScenario.Select01("name='%s'" %name, None)
if not storedScen:
    storedScen = acm.FStoredScenario()

storedScen.Scenario(scenario)
storedScen.Commit()


