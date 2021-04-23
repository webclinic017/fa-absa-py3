"""--------------------------------------------------------------------
MODULE:         FRTB_Update_FRTB_SA_Eligible_Tag
    
DESCRIPTION:    Strategic solution to update FRTB SA Take on data:

                NOTE - 
                
                File format as follows:
                
                Key	,Front Arena Instance	,Front Arena Portfolio Nbr	,Front Arena Portfolio Name	,FRTB_SA_Eligible

--------------------------------------------------------------------"""

import acm
import FRunScriptGUI

def getInputFileSelector():
    types = ('CSV Files (*.csv)|*.csv')
    return FRunScriptGUI.InputFileSelection(types)
    
    
def removeAllIncludedPortfolios(instance):
    ports = acm.FPhysicalPortfolio.Select('')
    print('Removing the following additionall infos from portfolios: \
    FRTB_SA_Eligible, VaR_Eligible, PL_Explain_Eligible, FRTB_IMA_Eligible, \
    SubProduct, Reg_Classification, Masterbook, MinorDesk, Desk, MajorDesk,Valuation_System')
    
    #addInfoNameList = ['FRTB_SA_Eligible', 'VaR_Eligible', 'PL_Explain_Eligible', 'FRTB_IMA_Eligible', 'SubProduct', 'Reg_Classification', 'Masterbook', 'MinorDesk', 'Desk', 'MajorDesk','Valuation_System']
    for port in ports:
        portClone = port.Clone()
        portClone.AdditionalInfo().FRTB_SA_Eligible(None)
        portClone.AdditionalInfo().VaR_Eligible(None)
        portClone.AdditionalInfo().PL_Explain_Eligible(None)
        portClone.AdditionalInfo().Reg_Classification(None)
        portClone.AdditionalInfo().Masterbook(None)
        portClone.AdditionalInfo().MinorDesk(None)
        portClone.AdditionalInfo().Desk(None)
        portClone.AdditionalInfo().MajorDesk(None)
        portClone.AdditionalInfo().Valuation_System(None)
        portClone.AdditionalInfo().FRTB_IMA_Eligible(None)
        if instance == 'SA':
            portClone.AdditionalInfo().SubProduct(None)
        elif instance == 'ARO':
            portClone.AdditionalInfo().AccountingTreatment(None)
            
        port.Apply(portClone)
        try:
            port.Commit()
            print('Successfully removed add infos from portfolio %s' %port.Name())
        except exception, e:
            print('ERROR deleting add infos from portfolio %s: %s' %(port.Name(), str(e)))


def removeAllContextDefinitionLinks():
    context = acm.FContext['FC Accrual Books']
    if context:
        contextList = []
        for contextLink in context.ContextLinks():
            contextList.append(contextLink)
        
        for contextLink in contextList:
            try:
                contextLink.Delete()
                print('Removing Context Link %s from context definition %s' %(contextLink.Portfolio().Name(), context.Name()))
            except Exception as e:
                print('Unable to remove Context Link %s from context definition %s' %(contextLink.Portfolio().Name(), context.Name()))
                print('Exception Raised: %s' %str(e))


def updatePortfolios(FA_Instance, fileSelection):
    portDict = {}
    try:
        with open(str(fileSelection), 'r') as file:
            for line in file:
                split                = line.split(',')
                instance             = split[0].rstrip().split('_')[0]
                oid                  = split[1].rstrip()
                frtb_sa_eligible     = split[4].rstrip()
                var_eligible         = split[5].rstrip()
                pl_explain_eligible  = split[6].rstrip()
                frtb_ima_eligible    = split[7].rstrip()
                sub_product          = split[8].rstrip()
                reg_classification   = split[9].rstrip()
                accounting_treatment = split[10].rstrip()
                master_book          = split[11].rstrip()
                minor_desk           = split[12].rstrip()
                desk                 = split[13].rstrip()
                major_desk           = split[14].rstrip()
                valuation_system     = split[15].rstrip()
                if instance == FA_Instance:
                    if not oid in portDict:        
                        portDict[oid] = {'Instance': instance, 'FRTB_SA_Eligible': frtb_sa_eligible, 'VaR_Eligible' : var_eligible,
                                        'PLExplain_Eligible' : pl_explain_eligible, 'FRTB_IMA_Eligible' : frtb_ima_eligible,
                                        'SubProduct' : sub_product, 'Reg_Classification' : reg_classification,
                                        'Accounting_Treatment' : accounting_treatment, 'Masterbook' : master_book,
                                        'Minor_Desk' : minor_desk, 'Desk' : desk, 'Major_Desk' : major_desk,
                                        'Valuation_System': valuation_system}
        print("Portfolios successfully extracted from .csv")
        print(portDict)
    except Exception as e:
        print("Unable to extract portfolio info from file.")
        print('Exception Raised: %s'%(e))
    
    for oid in portDict:
        if portDict[oid]['Instance'] == FA_Instance:
            portSelection = acm.FPhysicalPortfolio.Select('oid = %i'  %int(oid))
            if len(portSelection) == 1:
                port = portSelection[0]
                try:
                    print("Updating: %s" %port.Name())
                    clone       = port.Clone()
                    
                    if portDict[oid]['FRTB_SA_Eligible'] != '#N/A':
                        clone.AdditionalInfo().FRTB_SA_Eligible(portDict[oid]['FRTB_SA_Eligible'])
                    if portDict[oid]['VaR_Eligible'] != '#N/A':
                            clone.AdditionalInfo().VaR_Eligible(portDict[oid]['VaR_Eligible'])
                    if portDict[oid]['PLExplain_Eligible'] != '#N/A':
                        clone.AdditionalInfo().PL_Explain_Eligible(portDict[oid]['PLExplain_Eligible'])
                    if portDict[oid]['Reg_Classification'] != '':
                        clone.AdditionalInfo().Reg_Classification(portDict[oid]['Reg_Classification'])
                    if portDict[oid]['Masterbook'] != '':
                            clone.AdditionalInfo().Masterbook(portDict[oid]['Masterbook'])
                    if portDict[oid]['Minor_Desk'] != '':
                        clone.AdditionalInfo().MinorDesk(portDict[oid]['Minor_Desk'])
                    if portDict[oid]['Desk'] != '':
                        clone.AdditionalInfo().Desk(portDict[oid]['Desk'])
                    if portDict[oid]['Major_Desk'] != '':
                        clone.AdditionalInfo().MajorDesk(portDict[oid]['Major_Desk'])
                    if portDict[oid]['Valuation_System'] != '':
                        clone.AdditionalInfo().Valuation_System(portDict[oid]['Valuation_System'])
		    
		    if FA_Instance == 'SA':
                        if portDict[oid]['SubProduct'] != '':
                            clone.AdditionalInfo().SubProduct(portDict[oid]['SubProduct'])
                        if portDict[oid]['Accounting_Treatment'] != '':
                            clone.TypeChlItem(portDict[oid]['Accounting_Treatment'])
                    elif FA_Instance == 'ARO':
                        if portDict[oid]['Accounting_Treatment'] != '':
                            clone.AdditionalInfo().AccountingTreatment(portDict[oid]['Accounting_Treatment'])
                            
                    port.Apply(clone)
                    port.Commit()
                    print("Portfolio %s updated succesfully" %port.Name())
                except Exception as e:
                    print("Portfolio %s updated was unsuccesful" %port.Name())
                    print(str(e))
                
		'''
                if FA_Instance == 'SA':
                    if portDict[oid]['Accounting_Treatment'] == 'Accrual':
                        contextLink = acm.FContextLink()
                        contextLink.Context('FC Accrual Books')
                        contextLink.MappingType('Portfolio')
                        contextLink.Name('AP_MM')
                        contextLink.Portfolio(port.Name())
                        contextLink.Type('Accounting Parameter')
                        try:
                            contextLink.Commit()
                            print('Adding portfolio %s to Context Definition %s' %(port.Name(), 'FC Accrual Books'))
                        except Exception as e:
                            print('Unable to add portfolio %s to the Context Definition %s' %(port.Name(), 'FC Accrual Books'))
		'''

fileSelection    = getInputFileSelector()       
ael_variables = [['FA_instance', 'FA Instance', 'string', ['SA', 'ARO'], None, 1, 0, 'Select FA Instance you are updating.', None, None],
                ['fileSelection', 'Input Portfolios .csv file', fileSelection, None, fileSelection, 0, 1, 'Select file containing all portfolios in scope. (Take on Data)', None, True]]

def ael_main(ael_output):
    fileSelection = ael_output['fileSelection']
    instance = ael_output['FA_instance']
    #removeAllIncludedPortfolios(instance)
    #removeAllContextDefinitionLinks()
    updatePortfolios(instance, fileSelection)
