"""
-------------------------------------------------------------------------------------------------------
MODULE
    ImportPackage

    (c) Copyright 2010-2018 by FIS Front Arena. All rights reserved.

VERSION
    1.0.1(0.1.55)

DESCRIPTION
    Import *.def files on the commandline using RunScriptCMD

USAGE
    RunScriptCMD.py ImportPackage --filename=importPackage.def
    
    <?xml version="1.0" encoding="ISO-8859-1" ?> 
    <RunScriptCMD>
     <!-- Read ImportPackage -->
     <Command module="ImportPackage">
       <filename>importPackage.def</filename>
       <setOwner>SYSTEM</setOwner>
       <defaultProtection>7776</defaultProtection>
     </Command>
    </RunScriptCMD>

MAJOR REVISIONS
    2011-03-10  RL  Initial implementation
    2011-03-24  RL  Added protection support
    2011-03-25  RL  Added owner support
-------------------------------------------------------------------------------------------------------"""

import os
import acm
import FRunScriptGUI

import FLogger

logger = FLogger.FLogger('Transporter')

from Transporter import IN_PRIME
import Transporter
Transporter.checkProfileComponent("Start "+__name__)


class ImportPackage(FRunScriptGUI.AelVariablesHandler):
    """Read *.def files and import into ADS"""
    def __init__(self):
        vars = self.ael_variables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)

    def ael_variables( self ):
        fileSelection=FRunScriptGUI.InputFileSelection("def Files (*.def)|*.def|All Files (*.*)|*.*||")
        return [['filename', 'File name_Package', fileSelection, None, fileSelection, 0, 1, 'The *.def file'+'\nRunScriptCMD:filename'[:None if IN_PRIME else 0], None, 1],
                ['setOwner', 'Set Owner_Package', "FUser", acm.FUser.Select(''), None, 0, 0, 'Set owner of object'+'\nRunScriptCMD:setOwner'[:None if IN_PRIME else 0], None, 1],
                ['defaultProtection', 'Protection (OwnGrpOrgWld)_Package', 'string', ['Default', '7776'], 'Default', 0, 0, 'Choose protection Default or octal notation eg. 7776=RWDRWDRWDRW- (OwnGrpOrgWld)'+'\nRunScriptCMD:defaultProtection'[:None if IN_PRIME else 0]],
                ]

ael_gui_parameters = {
        'runButtonLabel': 'Import',
        'runButtonTooltip': 'Import package',
        'hideExtraControls': 1,
        'closeWhenFinished': 0,
        'windowCaption' : __name__+ ' ' + chr(0xA9) + '2018 FIS Front Arena',
        'version' : '1.0.1(0.1.55)'}

def importFileAs( filename, name, protection, owner):
    """ Import one file """
    
    try:
        with open(filename) as fh:
            text = fh.read()
    except Exception, msg:
        logger.ELOG("Failed to open file %s:" %(filename, msg))
        return 1

    if filename.endswith('.sql') or filename.endswith('.asql'):
        module = acm.FSQL[name]
    elif filename.endswith('.py'):
        module = acm.FAel[name]
    else:
        logger.ELOG("Filetype %s not supported" %filename)
        return 1

    try:
        if module:
            module.Text(text)
            if type(protection) == type(0):
                module.Protection(protection)
            if owner:
                module.Owner(owner)
            module.Commit()
            logger.LOG("Updated %s as %s" %(filename, name))
        else:
            if filename.endswith('.py'):
                module = acm.FAel()
            else:
                module = acm.FSQL()
            module.Name(name)
            module.Text(text)
            if type(protection) == type(0):
                module.Protection(protection)
            if owner:
                module.Owner(owner)
            module.Commit()
            logger.LOG("Added %s as %s" %(filename, name))
    except Exception, msg:
        logger.ELOG("Could not import %s as %s: %s" %(filename, name, msg))
        return 1
    
    return 0
        
def getDefProt(protection):
    """ Convert 4 character string octal protection to internal integer describing
        OwnGrpOrgWld protection

        > getDefProt("7776"):
        1
    """
    def int2prot(intt):
        ret = ''
        if int(intt) & 4 > 0:
            ret+='R'
        if int(intt) & 2 > 0:
            ret+='W'
        if int(intt) & 1 > 0:
            ret+='D'
        return ret

    protection=protection.strip()

    if len(protection) == 4 and protection.isdigit():
        use_def_prot = (4095 - (int("".join( [ str( (int(chr) & 2) | (int(chr) & 4) >> 2 | (int(chr) & 1) << 2) for chr in reversed(protection)] ), 8)))
        protStr = "W:%s,O:%s,G:%s,U:%s"%( int2prot(protection[3]), int2prot(protection[2]), int2prot(protection[1]), int2prot(protection[0]))
        logger.LOG('Protection: %s = %s' %(protection, protStr))
    elif protection.upper() in ('YES', '1', 'TRUE', 'DEFAULT'):
        use_def_prot = True
    else:
        use_def_prot = False
    return use_def_prot

def importDefFile(deffile, protection, owner):
    error = 0
    dir = os.path.dirname(deffile)
    cwd = os.getcwd()
    try:
        logger.LOG("Parsing %s" %deffile)
        localfile = os.path.basename(deffile)

        if dir:
            os.chdir(dir)
        use_def_prot = getDefProt(protection)
        if owner:
            logger.LOG('Set owner: %s' %(owner.Name()))

        with open(localfile, 'r') as fh:
            for line in fh:
                filename, name = line.split()
                error += importFileAs(filename, name.strip('"'), use_def_prot, owner)

        logger.LOG("Finished %s"%deffile)
    except Exception, msg:
        logger.ELOG("Error: %s"%msg)
        error += 1
    finally:
        if dir:
            os.chdir(cwd)

    return error > 0
    
def ael_main( params ):
    logger.LOG("%s %s"%(__name__, '1.0.1(0.1.55)') )
    #logger.LOG('ADS: %s'%acm.ADSAddress())

    filename = params.get('filename').AsString().strip()
    if not filename:
        logger.ELOG("File %s missing"%filename)
        return 1
        
    if not ((len(params['defaultProtection']) == 4 and params['defaultProtection'].isdigit()) or params['defaultProtection'].upper() == 'DEFAULT'):
        logger.ELOG("Protection has to be 4 numeric characters or 'Default'")
        return 1

    if importDefFile(filename, params['defaultProtection'], params['setOwner']):
        return 1

    return 0

ael_variables=ImportPackage()
ael_variables.LoadDefaultValues(__name__)
