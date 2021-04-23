'''
Date                    : 2014-07-09
Purpose                 : This script will be used to delete Portfolios that are in the GraveYard Portfolio.
Department and Desk     : TCU
Requester               : Alex Boshoff/Merisa Fraser
Developer               : Fancy Dire
CR Number               : 

Change Log:
Date            Developer               Change
'''

import acm, string

ael_variables = [('infile', 'Input File:', 'string', '', 'Portfolios_To_Delete.csv'),
                ('path', 'Input File Path:', 'string', '', '/apps/services/front/QUERIES/GEN/AEL/temp/'),
                ('outfile', 'Output File:', 'string', '', 'Portfolios_To_Delete_Confirm.csv')]
				
def ael_main(ael_dict):
    path = ael_dict['path']
    infile = ael_dict['infile']
    outfile = ael_dict['outfile']
    
    with open(path + infile) as infile:
        with open(path + outfile, 'w') as outfile:
            # Writing the Columns Headings in the file
            outline = 'Portfolio, Result \n' 
            outfile.writelines(outline)  
            for line in infile:
                l = string.split(line, ',')
                port = l[0].strip()
                print 'Portfolio :', port

                pp = acm.FPhysicalPortfolio[port]
                if not pp:
                    print "Portfolio not found: ", port
                    outline = port + ', Portfolio not Found' + '\n' 
                else:
                    print "Portfolio found"
                    
                    if pp.MemberLinks():
                        for m in pp.MemberLinks():      #Iterate through the portfolio links
                            print "Portfolio falls under:", m.OwnerPortfolio().Name()
                            try:
                                m.Delete()      #Delete the portfolio link
                                print pp.Name(), " Links Deleted!!"
                                outline = port + ', Portfolio links Deleted successfully' + '\n' 
                                
                                try:
                                    pp.Delete() #Delete the Portfolio
                                    print pp.Name(), " Deleted!!"
                                    outline = port + ', Portfolio and links Deleted successfully' + '\n' 
                                    
                                except RuntimeError, e:
                                    print pp.Name(), ":Could not be deleted", e
                                    outline = port + ', Portfolio could not be deleted' + '\n'
                                    
                            except RuntimeError, e:
                                print pp.Name(), ":Links Could not be deleted", e
                                outline = port + ', Portfolio links could not be deleted' + '\n'
                    else:
                        try:
                            pp.Delete()         #Delete portfolio if there are no links
                            print port, " Deleted!!"
                            outline = port + ', Portfolio Deleted successfully' + '\n' 
                        except RuntimeError, e:
                            print port, "Portfolio Could not be deleted", e
                            outline = port + ', Portfolio could not be deleted' + '\n'
                            
                outfile.writelines(outline)     #Write the result to the results file
                
    print 'Wrote secondary output to: ', path
    print 'Completed Successfully'
        
        
