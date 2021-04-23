import acm
import ael


stored_scenario_inputs = [
{'ScenarioName':'10Day_CMD_All','Risk Class':'Commodity','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_CMD_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'10Day_CR_All','Risk Class':'Credit','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_CR_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'10Day_EQ_All','Risk Class':'Equity','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_EQ_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'10Day_FX_All','Risk Class':'FX','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_FX_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'10Day_INF_All','Risk Class':'Inflation','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_INF_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'10Day_IR_All','Risk Class':'Interest Rate','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_IR_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'10Day_Total','Risk Class':'Total','ScenarioFile':'/apps/services/VaR_Scenarios/10Day/DVaR_Total_10d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_CMD_All','Risk Class':'Commodity','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_CMD_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_CR_All','Risk Class':'Credit','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_CR_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_EQ_All','Risk Class':'Equity','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_EQ_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_FX_All','Risk Class':'FX','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_FX_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_INF_All','Risk Class':'Inflation','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_INF_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_IR_All','Risk Class':'Interest Rate','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_IR_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'DVaR_Total','Risk Class':'Total','ScenarioFile':'/apps/services/VaR_Scenarios/DVaR/DVaR_Total_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_CMD_All','Risk Class':'Commodity','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_CMD_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_CR_All','Risk Class':'Credit','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_CR_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_EQ_All','Risk Class':'Equity','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_EQ_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_FX_All','Risk Class':'FX','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_FX_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_INF_All','Risk Class':'Inflation','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_INF_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_IR_All','Risk Class':'Interest Rate','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_IR_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_Total','Risk Class':'Total','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR/SVaR_Total_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_CMD_All','Risk Class':'Commodity','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_CMD_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_CR_All','Risk Class':'Credit','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_CR_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_EQ_All','Risk Class':'Equity','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_EQ_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_FX_All','Risk Class':'FX','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_FX_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_INF_All','Risk Class':'Inflation','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_INF_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_IR_All','Risk Class':'Interest Rate','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_IR_1d_Shifts_FormattedData.txt'},\
{'ScenarioName':'SVaR_PeriodTest_Total','Risk Class':'Total','ScenarioFile':'/apps/services/VaR_Scenarios/SVaR_PeriodTest/PeriodTest_Total_1d_Shifts_FormattedData.txt'}]


#scenario = acm.Risk().CreateDynamicScenario(context, templateName, params)
templateName="RiskScenarioFromFile"
context = acm.GetDefaultContext()
def do_run():
    for stored_scenario in stored_scenario_inputs:
        scenario_params = {}
        if stored_scenario["Risk Class"] != "Total":
            scenario_params = {
                acm.FSymbol('ShiftDisplayType'): "Absolute",
                acm.FSymbol('riskFactorSetup'): acm.FRiskFactorSetup["VaR Risk Factors"],
                acm.FSymbol('Attribute'): "VaR Risk Class",
                acm.FSymbol('Value'): stored_scenario["Risk Class"],
                acm.FSymbol('file'): stored_scenario["ScenarioFile"],
                acm.FSymbol('startIndex'):0,
                acm.FSymbol('endIndex'):0,
                acm.FSymbol('delimiterChar'):","    
            }
        else:
            scenario_params = {
            acm.FSymbol('ShiftDisplayType'): "Absolute",
            acm.FSymbol('riskFactorSetup'): acm.FRiskFactorSetup["VaR Risk Factors"],
            acm.FSymbol('Attribute'): "VaR Risk Total",
            acm.FSymbol('Value'): stored_scenario["Risk Class"],
            acm.FSymbol('file'): stored_scenario["ScenarioFile"],
            acm.FSymbol('startIndex'):0,
            acm.FSymbol('endIndex'):0,
            acm.FSymbol('delimiterChar'):","    
            }


        scenario = acm.Risk().CreateDynamicScenario(context, templateName, scenario_params)
        
        storedScenario = acm.FStoredScenario[stored_scenario["ScenarioName"]]
        if storedScenario:
            storedScenario.Delete()
            print("Deleted FStoredScenario: " + stored_scenario["ScenarioName"])
            print()
            
        storedScenario = acm.FStoredScenario()
        storedScenario.Scenario(scenario)
        storedScenario.Name(stored_scenario["ScenarioName"])
        storedScenario.AutoUser(False)
        storedScenario.Commit()
        print("Created FStoredScenario: "+storedScenario.Name())
    
ael_variables = []

def ael_main(ael_dict):
    do_run()



    

    
    
