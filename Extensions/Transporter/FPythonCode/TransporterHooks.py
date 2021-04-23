#grouping: aef/public

"""-------------------------------------------------------------------------------------------
MODULE
    TransporterHooks

    (c) Copyright 2010-2016 by SunGard Front Arena. All rights reserved.

VERSION
    3.3.0
DESCRIPTION
    Used to dynamically fill the RunScriptCMD parameters
    
    uses the fnmatch module for the name and excludename parameter, this allows for neat pattern matching:

    Pattern     Meaning 
    *           matches everything 
    ?           matches any single character 
    [seq]       matches any character in seq 
    [!seq]      matches any character not in seq 

USAGE
    <?xml version='1.0' encoding='iso-8859-1'?>
    <RunScriptCMD>
        <Command module="TransporterExport" hook="TransporterHooks.ExtensionModules(context='Standard',empty=True)">
            <basepath>.</basepath>
        </Command>
        
        <Command module="TransporterExport" hook="TransporterHooks.UserNames(tag='Extension_Module', group='ADMIN')" >
            <basepath>.</basepath>
        </Command>

        <Command module="TransporterExport" hook="TransporterHooks.Objects(tag='Trade_Filter', owner='${USERNAME}', name='*')" >
            <basepath>.</basepath>
        </Command>
        
        <Command module="TransporterImport" hook="TransporterHooks.FileNames(tag='Extension_Module', name='*.txt')" >
            <basepath>.</basepath>
        </Command>

	<Command module="ContextEditor" hook="TransporterHooks.FileExtensionNames(tag='add_module', basepath='.', name='*.txt')">
		<context>Standard</context>
		<add_before>%org</add_before> <!-- add_after has precedence -->
	</Command>
	
	<!-- Update python code within extension, read from file.
             Does NOT support ALL different kind of inputfiles and file sizes! -->
             
        <Command callback="False" exitOnError="False" module="TransporterUpdate"
                    hook="TransporterHooks.ReadTextFile(tag='extensioncontent', name='TestPython.py')">
            <moduleupdate>TestModule</moduleupdate>
            <extensiontype>FPythonCode</extensiontype>
            <extensionclass>FObject</extensionclass>
            <extensionname>testPython</extensionname>
	</Command>
        
    </RunScriptCMD>

MAJOR REVISIONS

    2010-12-17  RL  Initial implementation
    2011-02-01  RL  Added more options
    2011-08-22  RL  Support for ',' in names
    2013-01-16  RL  Add parameter excludename to exclude ExtensionModules names
    2014-05-27  RL  Extract extension names from files    
-------------------------------------------------------------------------------------------"""

from __future__ import with_statement # This isn't required in Python 2.6
import acm
import ael

import re
import os
import fnmatch
from string import Template

from Transporters import SelectObjects

import FLogger
logger = FLogger.FLogger('Transporter.'+__name__)

def _users(name='*', group=None, hasProfile=None, inactive=False, active=False):
    """Extract User names"""
    if group:
        users=[str(user.Name()) for user in acm.FUser.Select('userGroup="%s"'%group)
            if (not inactive or (inactive and user.Inactive())) and
               (not active or (active and not user.Inactive())) ]
    else:
        users=[str(user.Name()) for user in acm.FUser.Select('')
            if (not inactive or (inactive and user.Inactive())) and
               (not active or (active and not user.Inactive())) ]

    if hasProfile:
        inprofile=[str(prof.User().Name()) for prof in acm.FUserProfileLink.Select('userProfile="%s"'%hasProfile)]
        users=[user for user in users if user in inprofile]
    
    users = fnmatch.filter(users, name)
    return users
    
def _groups(name='*', hasProfile=None):
    """Extract Group names"""
    groups=[str(group.Name()) for group in acm.FUserGroup.Select('')]

    if hasProfile:
        inprofile=[str(prof.UserGroup().Name()) for prof in acm.FGroupProfileLink.Select('''userProfile=%r'''%hasProfile)]
        groups=[group for group in groups if group in inprofile]
    
    groups = fnmatch.filter(groups, name)
    return groups


def _JoinCommaSpace(lst):
    return [ '"%s"'%name if (',' in name or ' ' in name) else name for name in lst ]


def ExcludeFromList(objectlist, excludename=''):
    if excludename != '':
        for exclude in excludename.split(','):
            objectlist = [n for n in objectlist if not fnmatch.fnmatch(n, exclude)]
    return objectlist


def ExtensionModules(tag='Extension_Module', context=None, name='*', owner=None, empty=False, notempty=False, usermodule=False, group=None, hasProfile=None, inactive=False, active=False, excludename=''):
    """Extract Extension Module names

    excludename can have many strings split by "," e.g.
    
    TransporterHooks.ExtensionModules(name='T*', excludename='Tran*,TRAD*,TAB*')
    
    """
    if context:
        context = list( acm.FExtensionContext[context].ModuleNames() )

    if usermodule:
        users = _users(group=group, hasProfile=hasProfile, inactive=inactive, active=active)
    else:
        users = None

    if owner:
        owner = owner.upper()
    
    em=[str(em.Name()) for em in acm.FExtensionModule.Select('') \
        if  (not context or (context and str(em.Name()) in context)) and \
            (not owner or (owner and str(em.Owner().Name()) == owner)) and \
            (not empty or (empty and len(em.Types()) == 0 )) and \
            (not notempty or (notempty and len(em.Types()) > 0 )) and \
            (not users or (users and (str(em.Name()) in users ))) ]
    em = fnmatch.filter(em, name)
    
    em = ExcludeFromList(em, excludename)

    return {tag:",".join(_JoinCommaSpace(em))}


def ContextExtensionModules(tag='Extension_Module', contextname='Standard', name='*', excludename='' ):
    """Extract Extension Module names from a Context"""
    context = acm.FExtensionContext[contextname]

    if context:
        em = [str(ext) for ext in context.ModuleNames()]
    else:
        em = []

    em = fnmatch.filter(em, name)
    
    em = ExcludeFromList(em, excludename)

    return { tag:",".join(_JoinCommaSpace(em)) }


def BrokenExtensionModules(tag='Extension_Module'):
    """Extract "broken" Extension Module names"""
    col, res=ael.asql("select o.seqnbr from TextObject o where o.type = 'Extension Module' and o.usrnbr > 0")
    
    em = [ str(row[0]) for row in res[0] ]

    return { tag:",".join(_JoinCommaSpace(em)) }


def UserNames( tag='usernames', name='*', group=None, hasProfile=None, inactive=False, active=False, excludename=''):
    """Extract User names"""
    users = _users(name, group, hasProfile, inactive, active)
    
    users = ExcludeFromList(users, excludename)
    return { tag:",".join(_JoinCommaSpace(users)) }

class TemplateEnv(Template):
    idpattern="[_A-Za-z][\._A-Za-z0-9]*"


def ReadTextFile(tag='File', name='file.txt', search=None, replace=None, parseenv=False):
    """Extract File without stripping"""
    with open(name, 'r') as inputfile:
        text = inputfile.read()
        if parseenv:
            text = TemplateEnv(text).safe_substitute(os.environ)
        if search and replace:
            if type(search) != type(replace):
                raise Exception("Expecting search and replace to be of same type")
            
            if type(search) in (str, unicode):
                search = (search,)
                replace = (replace,)
                
            for (search, replace) in zip(search, replace):
                print "Replace %s with %s"%(search, replace)
                text = text.replace(search, replace)

    return { tag:text }

           
def ReadFile(tag='File', name='file.txt', separator=','):
    """Extract File"""
    with open(name, 'r') as inputfile:
        text = separator.join([line.strip() for line in inputfile])

    return { tag:text }

           
def FileNameList(basepath='.', name='*.*', extension=True, excludename=''):
    """Extract File names as list"""
    files = fnmatch.filter(os.listdir(basepath), name)

    if not extension:
        files = [file.split('.')[0] for file in files]

    files = ExcludeFromList(files, excludename)

    return sorted(files)


def FileNames(tag='Files', basepath='.', name='*.*', extension=True, separator=',', excludename='', addfilepath=False):
    """Extract File names"""

    if addfilepath:
        basepath = os.path.join( basepath, tag )

    files = FileNameList(basepath, name, extension, excludename)

    return { tag:separator.join(_JoinCommaSpace(files)), 'basepath':basepath }


def ReContext(tag='reContext', basepath='.', reContext='', nameContext="+%s"):
    """   reContext is a regular expression to extract a Context Name from the current directory r"\w+\\([A-Za-z]+)$" """
    if reContext:
        currentDir = os.path.abspath(basepath) 
        logger.LOG("ReContext: %r basepath: %s" %( reContext, currentDir))
        found = re.search(reContext, currentDir)
        
        if found:
            context = nameContext%found.group(1)
            logger.LOG("ReContext CONTEXT: %s" %( context))
        else:
            logger.ELOG("FileExtensionNames could not extract context")
            raise Exception("FileExtensionNames could not extract context")

    return {tag:context}


def FileExtensionNames(tag='add_module', basepath='.', name='*.*', separator=',', excludename='', tagContext='destination', reContext='', nameContext="+%s"):
    """Extract Extension module names from files. """
    
    if reContext:
        context = ReContext(tag='reContext', basepath=basepath, reContext=reContext, nameContext=nameContext)['reContext']
    else:
        context = ''
        
    files = FileNameList(basepath, name)
    
    modules = []
    for filename in files:
        with open( os.path.join(basepath, filename), 'rU') as file:
            for lineno, line in enumerate(file):
                if line.startswith("name "):
                    modules.append( line[13:-2] )
                    break
                elif lineno > 6:
                    break

    modules = ExcludeFromList(modules, excludename)
    
    returnDict = { tag:separator.join(_JoinCommaSpace(modules)), 'basepath':basepath}
    if tagContext and context:
        returnDict[tagContext]=context

    return returnDict


def ObjectList(objectname, owner=None, name='*', group=None, hasProfile=None, excludename=''):
    # ObjectNames
    if owner:
        owner = owner.upper()
    
    if group or hasProfile:
        objects = set()
        users = _users(group=group, hasProfile=hasProfile)
        for owner in users:
            objects.update( SelectObjects(objectname, owner, name) )
    else:
        objects = SelectObjects(objectname, owner, name)
    objects = ExcludeFromList(objects, excludename)

    return objects


def Objects(tag='Objects', objectname=None, owner=None, name='*', group=None, hasProfile=None, excludename=''):
    """ The Objects function extracts object names based on different criterias, 
        to be used with Transporter:Export, Transporter:Delete"""

    if not objectname:
        objectname = tag

    objects = ObjectList(objectname, owner, name, group, hasProfile, excludename)

    return { tag:",".join(_JoinCommaSpace(objects)) }


def CompareObjectsToFiles(tag='Objects', objectname=None, owner=None, name='*', group=None, hasProfile=None, excludename='', basepath='.', filename='*.*', separator=',', excludefile=''):
    """ The CompareObjectsToFiles function extracts object names based on different criterias,
        as well as filenames and generates an list of objectnames only existing in the database.
        To Archive call with Transporter:Export and then Transporter:Delete"""

    if not objectname:
        objectname = tag

    # Object names
    objects = ObjectList(objectname, owner, name, group, hasProfile, excludename)
    # File names
    #if objectname == 'ExtensionModule':
    #    files = FileExtensionNames(tag='ExtensionModule', basepath=basepath, name=filename, separator=separator,
    #            excludename='')['ExtensionModule']
    files = FileNameList(basepath, filename, extension = False, excludename = excludefile)
    
    return { tag:separator.join(_JoinCommaSpace( set( objects ) - set(files) )) }


def UserProfiles(tag='UserProfiles',name='*',user=None, group=None, excludename=''):
    """ Extract UserProfiles for either group, user or just name """
    userProfiles = []
    if user:
        userProfiles = [ pl.UserProfile().Name() for pl in acm.FUserProfileLink.Select('''user=%r'''%user) ]
    elif group:
        userProfiles = [ pl.UserProfile().Name() for pl in acm.FGroupProfileLink.Select('''userGroup=%r'''%group) ]
    else:
        userProfiles = [profile.Name() for profile in acm.FUserProfile.Select('') ]
    
    userProfiles = fnmatch.filter(userProfiles, name)
    
    userProfiles = ExcludeFromList(userProfiles, excludename)
    
    return {tag:",".join(_JoinCommaSpace(userProfiles))} 
