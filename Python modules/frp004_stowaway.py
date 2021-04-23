'''frp004_stowaway: last updated on Tue May 27 12:39:10 2003. Extracted by Stowaway on 2003-12-08.'''
'''frp004_Stowaway - Stow away AEL, ACMext and ASQL scripts to a directory
Or Stow away any table entry, or set of entries updated after a certain time.
Run and choose HELP for more help.
020430 FCS/MiHa Created V1.2
020725 FCS/MiHa Better default date handling V1.3
021007 FCS/MiHa Possible to extract ASQL queries too V1.4
021007 FCS/MiHa Possible to extract Instruments to message broker files too V1.5
021018 FCS/MiHa Possible to extract any one, or many, entities to AMB files V1.6
021024 FCS/MiHa Creates a .def file with AEL and ASQL exports, for easy loading
    	    	Adds comment about name, last update, and when Stowed away into AEL and ASQL.
021108 FCS/MiHa	Allows for dumping of tables on AMB format. v1.7
021120 FCS/MiHa Dump instruments per instype. Allow Trade and Ins dump per TradeFilter v1.8
021209 FCS/MiHa 
030228 FCS/MiHa v2.0beta Use AMBA to export entities. 
030304 FCS/MiHa v2.0 Key field works for single scripts too
030312 FCS/MiHa v2.1 Check for numerical key correctly. Check for AMBA requirements
030410 FCS/MiHa v2.2 Check for user and passwd when selecting Table Objects.
030522 FCS/MiHa v2.3 PRIME 3.0 uses acm library. Also handles strange module names

TODO:
    Instruments per Category
    Instruments per ValGroup
    Instruments per Curr
    Allow for lower case names in .def file, also for Python 1.5.2 libs
    Allow for date as date period, e.g. -3d etc
    List important tables first, like Instrument, Trade, Party etc
    Catch warning around os.tempname
    Ask for temporary dir instead of assuming c:/temp
    Allow for inclusion of primary key in table dumps
'''

import ael, os, re, time
#import frp004_mbf_tools
global verbose
verbose=0

#The std width of an AEL console is 41->!
def print_help():
    '''Help for users'''
    print '''
-----------------------------------------
This module is an aid to extracting and
stowing away existing scripts or other
records to a directory. Scripts are
stored as text files to be read back,
possibly with the aid of the created 
.def file.
Records are created on an MBF message
format to be loaded back with e.g. the
AMBA or the ExcelUploadTool, see
explanation below.
When saving scripts, the module will stow
away your Scripts, i.e. AEL, ACM exten-
sions and ASQL modules to a specified
directory. It will store all modules that
were changed after the specified date.
The names will be the module names with
extension .py, .acmext and .asql
A suggestion for the "specified date" is
probably, if you have a demo environment
to go look at c:/DEMO/db/demo_master.bak
That is what this script looks at for
default.
---------
N.B. ACMext works one way for PRIME 2.5,
2.6 and another for 2.4.x where it will
only give you the extension in zipped
format (which is OK to reload) if you
have older PRIME or if your run from 
ATLAS.
To export ASQLs it is required to fill in 
Server, User and Password, and to specify
a path to an ATLAS_EXT.exe. The AEL and
ADFL extractions do not need this 
information.
---------
When exporting records one can choose to
export all records of a certain table,
or tables. Just fill in the field
Table(s). If a single record is wanted
then choose a table and a primary or
unique key of that record.
If instruments are exported, the instype
can be chosen.
If instruments and/or trades are
chosen, it is possible to fill in a
TradeFilter name in the Key field and if
that is not an existing instrument or 
trade key, then the instruments and/or
trades of that tradefilter are exported.
The Table chosen should be Instrument and
/or Trade.
-----------------------------------------
'''
# Name of extensions for the different types
extension_dict = {'AEL':'py','Extension Module':'acmext','ExtMod zipped':'zip',
    'ASQL':'sql','Entity':'txt'}
    
def mkdir(ddir):
    '''Create directory if it does not exist'''
    if not os.path.exists(ddir):
    	print 'Creating', ddir
	os.mkdir(ddir)
    else:
    	if not os.path.isdir(ddir):
	    raise 'The suggested directory is already a file (%s)' %ddir

def text_time(atime):
    import time
    return time.strftime('%Y-%m-%d', time.gmtime(atime))
    
def comment(e, type):
    'Return a comment line to an AEL or ASQL, to be place at top of file'
    comment = str(display_id(e)) + ': last updated on ' +\
	time.ctime(e.updat_time) + '. Extracted by Stowaway on ' + str(ael.date_today()) + '.'
    if type == 'ASQL': 
    	comment = '/* ' + comment + '*/\n'
    elif type == 'AEL':
    	comment = "'''" + comment + "'''\n"
    else: raise 'Cannot comment type %s.' % type
    return comment
        
def filename_adapt(inname):
    'Replace non-filename characters with underscore'
    replace_characters=''' \xbd\xa7"#\xa4%&/()=?+\\`\xb4^\xa8~*'.:,;<>|\xa3$@{}[]'''
    outname=''
    for c in str(inname): # str if inname was an integer key
    	if c in replace_characters: outname=outname+'_'
    	else: outname=outname+c
    return outname
    
def write_to_file(ddir,fname,ext,text,f=None, do_close=0):
    'Write a text to a file. File could already be opened'
    if not f: # Else file is already open, just add to it
        fullname = os.path.join(ddir, fname+'.'+ext)
        f = open(fullname, 'w')
    else: fullname='' #Just to return something
    if not text:
    	print 'No text to write_to_file!!************'
	if not fullname: fullname = 'Help'
    else: f.write(text)
    if do_close:
        f.close()
    return fullname
    
def dump_text_objs(ddir,fromdate,aetype,key='',stype=''):
    '''Store each TextObject newer than fromdate to the directory'''
    if not stype: stype = aetype
    textsfound=[]
    for ae in ael.TextObject.select('type="%s"'%aetype):
    	if key and ae.name != key: continue # Looking for just one record
	if ael.date_from_time(ae.updat_time) >= fromdate or key: # If exist, don't mind date
	    if verbose:print text_time(ae.updat_time), stype
	    lines = ae.get_text()
	    if stype != 'ExtMod zipped': # Can't add comments to zipped format
	    	lines = comment(ae, aetype) + lines
	    fname = write_to_file(ddir, filename_adapt(ae.name), extension_dict[stype], lines)
	    if verbose: print fname
	    textsfound.append(ae.name)
    return textsfound
    
def dump_aels(ddir,fromdate,key=''):
    '''Store each AEL newer than fromdate to the directory'''
    return dump_text_objs(ddir, fromdate, 'AEL', key)

def dump_exts(ddir,fromdate,key=''):
    '''Store each Extension Module newer than fromdate to the directory'''
    import string
    extsfound=[]
    extmod = 'Extension Module'
    try:
    	#Library is acm since PRIME 3.0
    	try:
	    import acm
	    exts = acm.FExtensionModule.Select('')
	    print 'Exts1', exts
    	except:	
	    import ael2  # If this fails, we are in ATLAS
	    try: # PRIME 2.5.x
		exts = ael2.FExtensionModule.Select('')
	    	print 'Exts2', exts
	    except: # PRIME 2.4.x
		print 'Trying the PRIME 2.4.x way of reading extensions'
		exts = ael2.getServerObject().GetClass('FExtensionModule').Select('')
	    	print 'Exts3', exts
	if exts:
	    for i in range(exts.Size()):
		upd = ael.date(string.split(exts.At(i).UpdateTime())[0])
		if upd > fromdate or key:
		    name = exts.At(i).Name()
    	    	    if key and key != name: continue # Read only one specific Ext
    		    fname = write_to_file(ddir, name, extension_dict[extmod],
			exts.At(i).AsString())
		    if verbose: print upd.to_string(), ':', fname
		    extsfound.append(name)
    except:
    	print 'Export of Extension Modules is best done from PRIME'
	print 'You will now only get the zipped data in the file'
    	dump_text_objs(ddir, fromdate, 'Extension Module', key, 'ExtMod zipped')
    return extsfound

def dump_asqls(fromdate,cd,key=''):
    '''Store each ASQL newer than fromdate to a file'''
    print 'Dumping of ASQLs:'
    sqlsfound=[]
    for sql in ael.Parameter.select('type=SQL_QUESTION'):
    	if key and key != sql.name: continue # Read only one specific ASQL
	if ael.date_from_time(sql.updat_time) >= fromdate or key:
	    if verbose: print text_time(sql.updat_time), sql.name,
	    outfile=os.path.join(cd.dumpdir, filename_adapt(sql.name)+'.'+extension_dict['ASQL'])
    	    cmd = '"%s" -transfer par2file -server %s -user %s -passw %s -sqlq %s -sqlf %s' % \
	    	(cd.extcmd, cd.server, cd.usern, cd.passwd, sql.name, outfile)
    	    stat = os.system(cmd)
    	    if verbose: print outfile,
	    if not stat: 
	    	if verbose:print
		# This does not work, comment will be at end.
		#f=open(outfile,'a+')
		#f.seek(0) 
		#f.write(comment(sql,'ASQL'))
		#f.close()
    	    	# So instead I read the whole query to a buffer
		f=open(outfile, 'a+')
		f.seek(0) 
		wholequery = f.readlines()
		f.truncate(0)
		f.write(comment(sql, 'ASQL'))
    	    	f.writelines(wholequery)		
		f.close()
	    	sqlsfound.append(sql.name)
	    else:
	    	if verbose: print '- Dump Failed', stat
    return sqlsfound
    
def generate_def_file(namelist, dir, filename, type):
    'Generate a .def file to automatically load the dumped files'
    deffile=''
    import sys
    for name in namelist:
	if not deffile: 
	    deffile=os.path.join(dir, filename)
	    f=open(deffile, 'w')
	if sys.version[:5] == '1.5.2':
	    import string
	    namelow = string.lower(name)
	else:
	    namelow = name.lower()    	
	f.write(namelow+'.'+extension_dict[type]+'\t\t"'+name+'"\n')
    if deffile:
    	f.close()
    return deffile
    
def openfile(ddir, tabname):
    'Open file with a table name'
    datestr=ael.date_today().to_string(ael.DATE_Quick)
    fullname = os.path.join(ddir, tabname+'_'+datestr+'.'+extension_dict['Entity'])
    f = open(fullname, 'w')
    return f, fullname
    	
#---

class ConnectData:
    def __init__(self, server, usern, passwd, ambacmd, extcmd, dumpdir):
    	self.server=server
	self.usern=usern
	self.passwd=passwd
	self.ambacmd=ambacmd
	self.extcmd=extcmd
	self.dumpdir=dumpdir

def dID_name(e,keyname='Best'): #Keyname can be 'Best','unique','primary'
    '''Return name of unique key, or if it doesn't exist, primary key'''
    unique=''
    for k in eval('ael.'+e.record_type+'.keys()'):
	if k[1] == 'unique': 
	    unique=k[0]
	    if len(k[2]) > 1: # Combination key
	    	unique = unique + '+' # '+' means handle it your own way
	elif k[1] == 'primary': primary=k[0]
    if keyname == 'Best':
    	if unique: return unique
	else: return primary #Found no unique, have to take primary
    elif keyname == 'unique': return unique
    else: return primary

def display_id(e):
    '''Prints identifying ID of an entity. Ideally e.display_id() should work
    like this. There is an SPR-221643 on that subject. It is better/easier
    to fix the SPR than to enlarge on this function.'''
    type = e.record_type
    dID = dID_name(e)
    if dID == "type+": # As in ['type', 'usrnbr', 'name'], typically a TextObject or Parameter
    	dID = 'name'
    elif dID[-1:] == '+': 
    	dID = dID_name(e, 'primary')
    return str(getattr(e, dID))

def primary_key(e):
    dID = dID_name(e, 'primary')
    return getattr(e, dID)
   
#--- 

def dump_entity2file(ofilename, ifilename, cd):
    #ifilename is a dump_obj file of format "tablename key" per row
    if not '/' in ofilename and not '\\' in ofilename: # i.e. no path
    	ofilename=os.path.join(cd.dumpdir, ofilename+'.'+extension_dict['Entity'])
    cmd = '"%s" -dump_obj %s -dump_out %s -nice_enum_names 1 -server %s -user %s -passw %s' % \
    	(cd.ambacmd, ifilename, ofilename, cd.server, cd.usern, cd.passwd)
    if verbose==2:print cmd
    stat = os.system(cmd)
    if not stat: 
    	if verbose: print 'Created message file', ofilename
    else:
    	if verbose: print '- AMBA Dump Failed', stat

def entitykey2tmpfile(e, tmpfile=None,tmpdir='c:/temp'):
    if not tmpfile:
        tmpfile=os.tempnam(tmpdir, 'dump')
    f=file(tmpfile, 'a+')
    if verbose==2: print 'Tab,id', e.record_type, primary_key(e)
    if verbose==2: print 'tmpfile', tmpfile
    f.write('%s %d\n' % (e.record_type, primary_key(e)))
    f.close()
    return tmpfile

def dump_entity(e,cd,ofilename='',tmpkeyfile=None,tmpdir='c:/temp'):
    if not tmpkeyfile:
    	tmpkeyfile = entitykey2tmpfile(e, None, tmpdir)
    if not ofilename:
    	ofilename='%s_%s' % (e.record_type, filename_adapt(display_id(e)))
    dump_entity2file(ofilename, tmpkeyfile, cd)
    return tmpkeyfile, ofilename

def dump_selection(sel, fdtime, cd, join):
    '''Not yet used!!!'''
    keyfile=''
    for e in sel:
	if e.updat_time > fdtime:
	    if not join:
		dump_entity(e, cd)
	    else:
		keyfile=entitykey2tmpfile(e, keyfile)
    if keyfile: # have found entities to save
	dump_entity2file(outfilename, keyfile, cd)
    
def uniqueFileName(dir, tabnam):
    prefix=filename_adapt(tabnam + '_' + ael.date_today().to_string(ael.DATE_Quick) + '_')
    ext = extension_dict['Entity']
    for n in range(0, 1000): # Can't use os.tempnam because we need an extension
	outfilename=os.path.join(dir, "%s%d.%s" % (prefix, n, ext))
	if not os.path.isfile(outfilename): break
    return outfilename # Will raise exception if none of the 1000 was unique

def dump_entities(fromdate,tables,cd,join=1):
    if type(fromdate) == type('str'): fromdate=ael.date(fromdate)
    fromdatetime=fromdate.to_time()
    for tnam in tables:
    	outfilename = uniqueFileName(cd.dumpdir, tnam)
	keyfile=''
	for e in eval('ael.'+tnam):
	    if e.updat_time > fromdatetime:
	    	if not join:
		    dump_entity(e, cd)
		else:
		    keyfile=entitykey2tmpfile(e, keyfile)
	if keyfile: # have found entities to save
	    dump_entity2file(outfilename, keyfile, cd)

def dump_instruments(fromdate,cd,instypes=None, joinfiles=0):
    '''Store each Instrument newer than fromdate to the directory as an AMB file. If
    instypes is given, only those types are dumped.'''
    if type(fromdate) == type('str'): fromdate=ael.date(fromdate)
    fromdatetime=fromdate.to_time()
    if not instypes:
    	isel = ael.Instrument.select().members()
    else:
    	isel=[]
    	for it in instypes:
    	    isel = isel + ael.Instrument.select('instype="%s"'%it).members()
    keyfile=''
    for e in isel:
	if e.updat_time > fromdatetime:
	    if not joinfiles:
		dump_entity(e, cd)
	    else:
		keyfile=entitykey2tmpfile(e, keyfile)
    if keyfile: # have found entities to save
    	if len(instypes) == 1: prefix=instypes[0]
	else: prefix='Instrument'
    	outfilename = uniqueFileName(cd.dumpdir, prefix)
	dump_entity2file(outfilename, keyfile, cd)

	
def dump_ins_trade_with_filter(fromdate, cd, tfilt, isins, istrd, joinfiles=0,tmpdir='c:/temp'):
    'Dump trades and/or instruments according to a TradeFilter'
    fromdatetime=fromdate.to_time()
    inslis=[]
    ikey, tkey, lastt=None, None, None
    foundNow, tfound=0, 0
    for t in tfilt.trades():
	foundNow=0
	if istrd: 
	    if t.updat_time > fromdatetime:
	    	tfound=tfound+1
		foundNow=1
		lastt = t
		if joinfiles: tkey = entitykey2tmpfile(t, tkey, tmpdir)
		else: dump_entity(t, cd)
    	if isins and t.insaddr not in inslis: # This avoid duplicating ins dumps
	    if t.insaddr.updat_time > fromdatetime or foundNow: # If trade was chosen, ref should always be included
	    	inslis.append(t.insaddr)
	    	ikey = entitykey2tmpfile(t.insaddr, ikey, tmpdir)
    if joinfiles:
    	if tfound == 1:
    	    dump_entity(lastt, cd)
    	else:
    	    dump_entity2file(uniqueFileName(cd.dumpdir, 'Trade'), tkey, cd)	    
    if len(inslis) == 1:
    	dump_entity(inslis[0], cd)
    else:
    	if joinfiles:
	    dump_entity2file(uniqueFileName(cd.dumpdir, 'Instrument'), ikey, cd)
    	else:
	    for i in inslis:
	    	dump_entity(i, cd)
		
def test(n):
    print 40*'-'
    cd=ConnectData('10.3.15.65:9100', 'indira', 'intas', 'C:/DEMO/FRONT ARENA/AMBA/amba.exe', '', 'c:/tmp/de')
    if n==1: dump_entity2file('trade_030228', 'c:/tmp/dump.in', cd)
    elif n==2: print entitykey2tmpfile(ael.Trade[3436])
    elif n==3: 
    	tmpf= entitykey2tmpfile(ael.Trade[3436])
    	print entitykey2tmpfile(ael.Trade[3036], tmpf)
    elif n==4: dump_entity(ael.Trade[3436], cd)
    elif n==5: dump_entities('030201', ['Trade'], cd)
    elif n==6: dump_entities('030201', ['Trade'], cd, 0)
    elif n==7: dump_entities('030201', ['Instrument', 'Trade'], cd, 0)

def backup_file_date(bcpfile='c:/demo/db/demo_master.bak'):
    '''Find the date from the last backup database of demoMaster, which should be
    the last time one took a full backup, or installed a new demoMaster.'''
    import stat
    try:
	mtime = os.stat(bcpfile)[stat.ST_MTIME]
	return text_time(mtime)
    except:
	return ael.date_today().to_string()

def all_usernames():
    'Return all User names'
    retvec=[]
    for u in ael.User.select():
    	retvec.append(u.userid)
    return retvec
    
def all_tables():
    'Return all ael_tables'
    retvec=[]
    for x in dir(ael):
	try: 
    	    if type(eval('ael.'+x)) == ael.ael_table:
    		retvec.append(x)
	except: pass
    return retvec

def all_instypes():
    non_instruments=['StockRight', 'LEPO', 'CP', 'EquityIndex', 'BondIndex',
    'MultiOption', 'MultiAsset', 'Unknown', '?']
    retvec=[]
    for n in range(1, 50):
	itype=ael.enum_to_string('Instype', n)
	if itype not in non_instruments:
    	    retvec.append(itype)
    return retvec
        
whatvect = ['HELP', '1.AllScripts', '2.AEL', '3.ACMext', '4.ASQL', '5.Table Objects', '6.Test']
#default_date = ael.date('2002-01-01').to_string() # Beginning of year
default_date = backup_file_date() # Get the change date of server_data

ael_variables = [('a_what', 'What', 'string', whatvect, 'HELP', 1),
		('b_fromdate', 'FromDate', 'date', [], default_date, 1),
		('c_dumpdir', 'DumpDir', 'string', [], 'C:/Stowaway/SCRIPTS/AEL', 1),
		('d_table', 'Table(s)', 'string', all_tables(), None, 0, 1),
		('e_key', 'Key', 'string', None, None, 0),
		('f_instypes', 'Instypes', 'string', all_instypes(), None, 0, 1),
		('g_joinfiles', 'JoinFiles', 'string', ['Yes', 'No'], 'No', 0),
    		('h_user', 'User', 'string', all_usernames(), None, 0),
		('i_passwd', 'Password', 'string', None, None, 0),
		('j_server', 'Server', 'string', None, '10.3.15.65:9100', 0),
		('k_extpath', 'AtlasExtCmd', 'string', None, 'c:/Stowaway/arena_ext', 0),
		('l_ambapath', 'AMBACmd', 'string', None, 'c:/Stowaway/amba', 0),
		('verbosity', 'Verbosity', 'string', ['Silent', 'Info', 'Debug'], 'Debug', 0)]
	

def ael_main(chdict):
    global verbose
    if chdict['verbosity'] == 'Silent': verbose=0
    elif chdict['verbosity'] == 'Info': verbose=1
    else: verbose = 2
    #frp004_mbf_tools.verbosity(verbose) # Set or reset printouts
    what2do = []	
    if 'HELP' == chdict['a_what']: print_help()
    elif '1.AllScripts' == chdict['a_what']: what2do = whatvect[2:5] #2, 3 and 4 are scripts
    else: what2do = [chdict['a_what']]
    fromd = chdict['b_fromdate']
    ddir = chdict['c_dumpdir']
    server=chdict['j_server']
    usern=chdict['h_user']
    passwd=chdict['i_passwd']
    tables=chdict['d_table']
    key=chdict['e_key']
    instypes=chdict['f_instypes']
    if chdict['g_joinfiles'] == 'Yes': joinfiles=1
    else: joinfiles=0
    extpath=chdict['k_extpath']
    ambapath=chdict['l_ambapath']
    conDat =ConnectData(server, usern, passwd, ambapath, extpath, ddir)
    
    if '4.ASQL' in what2do:
    	if not server or not usern or not passwd or not extpath:
	    print 'When extracting ASQL you must supply User, Password, Server'\
	    	' and path to the ATLAS_EXT command'
	    what2do=[]
    if '5.Table Objects' in what2do:
    	if key and len(tables) != 1 and not ael.TradeFilter[key]:
	    print 'When extracting one entity, key must be set and just one'\
	    	' table can be chosen.'
	    what2do=[]
	if not server or not usern or not passwd or not ambapath:
	    print 'When extracting Table info you must supply User, Password, Server'\
	    	' and path to the AMBA command'
    	    what2do=[]

    if '6.Test' in what2do:
    	print 40*'-'
    	test(key)
    elif what2do: mkdir(ddir)

    for what in what2do:
    	if what == '2.AEL': 
	    texts = dump_aels(ddir, fromd, key)
	    if texts:
	    	deffile=generate_def_file(texts, ddir, 'Stowaway_AEL'+\
		    ael.date_today().to_string(ael.DATE_Quick)+'.def', 'AEL')
		if deffile: print 'New AELs in .def file:', deffile
	elif what == '3.ACMext': dump_exts(ddir, fromd, key)
	elif what == '4.ASQL': 
	    asqls = dump_asqls(fromd, conDat, key)
	    if asqls:
	    	deffile=generate_def_file(asqls, ddir, 'Stowaway_ASQL'+\
		    ael.date_today().to_string(ael.DATE_Quick)+'.def', 'ASQL')
		if deffile: print 'New ASQLs in .def file:', deffile
	elif what == '5.Table Objects':
    	    isins='Instrument' in tables
	    istrd='Trade' in tables
	    if key:
	    	isnum=1
	    	for k in key: # TODO This can probably be made nicer with regexp
		    if k not in ['0123456789']:
		    	isnum=0
			break
		#if re.search('\d',key):  # If only numbers
		if isnum:
		    key=int(key)
		    entity = eval("ael.%s[%d]" % (tables[0], key))
		else:
		    try: entity = eval("ael."+tables[0]+"['"+key+"']")
		    except: entity = None # Above will fail it table does not have unique key
		if entity: dump_entity(entity, conDat)
		else: 
		    # Special case. If tables is Instrument or Trades, look for TradeFilter
		    tf = ael.TradeFilter[key]
    	    	    if (isins or istrd) and tf:
		    	dump_ins_trade_with_filter(fromd, conDat, tf, isins, istrd, joinfiles)
		    else:
    			print 'Table object', tables[0], key, 'NOT FOUND!'
	    else:
	    	'Special case. If instrument and instype is set, search by that, only.'
	    	if isins and instypes:
		    dumpeddic = dump_instruments(fromd, conDat, instypes, joinfiles)
		else:    
		    dumpeddic = dump_entities(fromd, tables, conDat, joinfiles)
		#for d in dumpeddic.keys():
		#    print 'Dumped',dumpeddic[d],d		    
    	else: print 'What:', what
    if verbose: print 'Done.'




