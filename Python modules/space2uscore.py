'''space2uscore: last updated on Thu Dec 11 16:54:42 2003. Extracted by Stowaway on 2003-12-11.'''
'''space2uscore - export queries with space in the name
Do like this:
1. In var below, set "aext" to the path where you have an atlas_ext, or arena_ext
2. Set servusrpwd to the server name, user and password.
3. Set the temporary file in "file()" to whereever you want to work, e.g. c:/queries/expq.bat
4. Run this script - it will create the named .bat file
5. Start a command line prompt and cd to the chosen directory, e.g. c:/queries
6. Run the .bat file, e.g. expq.bat
This will create all the query extract which have a space in them to 
files where the not allowed characters have been removed.

If you want all queries, not just the ones with spaces in them, 
replace the
    if name.find(' ') > 0:
with 
    if 1:

031211 FCS/MiHa Created

Customized by Anton van Staden (x7262) for Front Arena Production.
Create a folder c:/Stowaway/ and copy the arena_ext and amba files in there.
Create a SCRIPTS folder and ASQL in c:/Stowaway/ e.g. C:/Stowaway/SCRIPTS/ASQL 
Add the username and password to this script at servusrpwd
Execute script
Execute C:/Stowaway/SCRIPTS/ASQL/expq.bat

'''

import ael
print 40*'-'
aext='"c:/Stowaway/arena_ext"'
servusrpwd='-serv 10.3.15.65:9100 -user EXTRACT -passw ??????'
f=file('C:/Stowaway/SCRIPTS/ASQL/expq.bat', 'w')

def filename_adapt(inname):
    'Replace non-filename characters with underscore'
    replace_characters=''' \xbd\xa7"#\xa4%&/()=?+\\`\xb4^\xa8~*'.:,;<>|\xa3$@{}[]'''
    outname=''
    for c in str(inname): # str if inname was an integer key
    	if c in replace_characters: outname=outname+'_'
    	else: outname=outname+c
    return outname
 

for p in ael.Parameter.select('type=SQL_QUESTION'):
    #print p.pp()
    name = p.name
#    if name.find(' ') > 0:
    if 1:
    	#nname=name.replace(' ','_')
    	nname=filename_adapt(name)
	nname=nname+'.sql'
	print name, nname
    	line = '%s %s -transfer par2file -sqlq "%s" -sqlf "%s"\n' %\
	    (aext, servusrpwd, name, nname)
	print line
	f.write(line)
	#break
f.close()


