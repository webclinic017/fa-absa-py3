"""-------------------------------------------------------------------------------------------------------
MODULE
    Transporters

    (c) Copyright 2009-2018 by FIS Front Arena. All rights reserved.

VERSION
    1.0.1(0.1.55)
DESCRIPTION
    An Export/Import Module for ACM Objects

MAJOR REVISIONS

    2008-04-21  RL  Initial implementation
    2011-02-19  RL  Fix dates and remove unused Oid in exported files
    2011-03-18  RL  Use urllib to transform filename
    2011-04-18  RL  Add setting saveCRLF (default=True), Added WorkspaceTransporter
    2011-09-12  RL  Added tag support replacing env variable FCSTransporterTag into all $TIT: $ tags and
                    %TransporterImportTag% against env variable "TransporterImportTag"
    2013-06-26  RL  Split/Merge Extension Modules Parts. Configured using FParameter TransporterSetup.
    2014-01-31  MM  Shared workbooks are now still shared when imported again (SPR 358728)
    2014-09-29  RL  Keep extension group in splitted extension modules.
    2014-12-08  RL  Allow saving files in separate paths, controlled in FParameters->Transporter->filePaths
    2015-04-01  MM  When importing a Workbook that already exists in the ADS, the imported version now
                    successfully overwrites the already existing version
    2015-05-13  MM  When importing a private Workbook that already exists in the ADS, the workbook remains
                    with original owner
    2015-09     RL  Removed references to remotesheets for later releases
    2015-11-26  RL  Unicode updates
    2018-01-12  RL  Add Workbook content support
-------------------------------------------------------------------------------------------------------"""

import acm, ael

import os
import time
import fnmatch
import traceback
import urllib
import zlib
import base64
import re

import xml.etree.cElementTree as ET

from string import maketrans

from Transporter import Transporter, transporterSetup, IN_PRIME, ACM_INTERNAL_VERSION

import FLogger
logger = FLogger.FLogger(name = 'Transporter')

if ACM_INTERNAL_VERSION >= 4.0:
    from XmlSerializer import XmlSerializer


class UpdateException(Exception):
    def __str__(self):
        return repr(self.args[0])


def SelectObjects(object, owner=None, name='*'):
    """Extract object names"""
    
    handler = getHandler(object)
    objects = [str(robject) for robject in handler.Select(owner)]

    return fnmatch.filter(objects, name)


INVALID_CHARS = maketrans(r''' ():?!"#$%&'*+,./@;<>=[]\^{}~''', '''_LRkqeshdpnsspkpsasLReLRbcLRt''')

def getHandler(object):
    """Extract objects"""
    
    for obj, handler in Transporter.all_handlers.iteritems():
        if obj == object or obj.translate(INVALID_CHARS) == object:
            if not isinstance(handler, XMLTransporter):
                raise Exception("This does not work on %s objects"%object)
            return handler
    raise Exception("Object type %s is not found"%object)

def getDate(fromdate):
    #Support for date format shotrtcuts 
    #like -1D, -1d, -1M, -1m, -y, Y SPR-389915
    days_factor = 0
    days_factor_present = False
    months_factor = 0
    months_factor_present = False
    years_factor = 0
    years_factor_present = False

    if not fromdate:
        return None

    for fmt in ('%Y-%b-%d', '%b-%Y-%d', '%d-%b-%Y', '%Y-%d-%b', '%d-%Y-%b', '%b-%d-%Y'):
        try:
            fromdate=datetime.strptime(fromdate, fmt).strftime('%y-%m-%d')
            break
        except Exception, e:
            pass

    if fromdate in ["Y", "y", "yesterday", "Yesterday", "YESTERDAY"]:
        days_factor = -1
        days_factor_present = True

    if fromdate in ["today", "Today", "TODAY"]:
        days_factor = 0
        days_factor_present = True

    if re.search(r'-?\d+[D|d]', fromdate):
        result = re.match(r'(-?\d+)[D|d]', fromdate)
        try :
            days_factor = int(result.group(1))
            days_factor_present = True
        except Exception, e:
            pass
    if re.search(r'-?\d+[M|m]', fromdate):
        result = re.match(r'(-?\d+)[M|m]', fromdate)
        try :
            months_factor = int(result.group(1))
            months_factor_present = True
        except Exception, e:
            pass
    if re.search(r'-?\d+[Y|y]', fromdate):
        result = re.match(r'(-?\d+)[Y|y]', fromdate)
        try :
            years_factor = int(result.group(1))    
            years_factor_present = True
        except Exception, e:
            pass

    if days_factor_present:
        ael_d = ael.date_today().add_days(days_factor)
        return ael_d
        #fromdate = ael_d.to_string(ael.DATE_ISO)
    if months_factor_present:
        ael_d = ael.date_today().add_months(months_factor)
        return ael_d
        #fromdate = ael_d.to_string(ael.DATE_ISO)
    if years_factor_present:
        ael_d = ael.date_today().add_years(years_factor)
        return ael_d
        #fromdate = ael_d.to_string(ael.DATE_ISO)
    return ael.date_from_string(fromdate)

class XMLTransporter(Transporter):
    SHARED_CHAR = "@"

    added = None
    DEFAULT_EXTENSION='.none'
    customfileextensions=eval(transporterSetup.get('fileExtensions', \
            "{'Trade Filter':'.tf','Extension Module':'.ext','Task':'.task','Query Folder':'.xml.qf','ASQL Query':'.asql','Python':'.py','TradingSheetTemplate':'.xml.tst','Workbook':'.wb','Workspace':'.ws'}" \
            ), {"__builtins__": __builtins__})

    customfilepath=eval(transporterSetup.get('filePaths', \
            "{'Trade Filter':'Trade_Filter','Extension Module':'Extension_Module','Task':'Task','Query Folder':'Query_Folder','ASQL Query':'ASQL_Query','Python':'Python','TradingSheetTemplate':'TradingSheetTemplate','Workbook':'Workbook','Workspace':'Workspace','ASQL Report':'ASQL_Report'}" \
            ), {"__builtins__": __builtins__})


    def StringToFile(self, path, output, name, extension=None ):
        
        if extension == None:
            extension = self.Extension()
            if ',' in extension:
                extension = extension.split(',')[0]

        if not path.strip():
            raise IOError("Path can not be empty")

        na = name
        if transporterSetup.get('specialCharConv', 'True') == 'True':
            na = urllib.quote(name, ' @.()')
        if na != name:
            filename = na + extension
            logger.WLOG("Warning: changed name to %s"%filename)
        else:
            filename = name + extension
            
        if not os.path.exists(path):
            raise IOError("Path <%s> does not exist"%path)

        file_path = os.path.abspath(os.path.join(path, filename))

        if str(transporterSetup.get('saveCRLF', 'True')).strip() == 'True' and "\r\n" not in output:
            output = output.replace("\n", "\r\n")

        with open(file_path, 'wb') as fh:
            fh.write(output)
        
        return file_path

    def checkAllowed(self, allow, added, objectSame=None):
        if (added and "INSERT" not in allow.upper()) or ( not added and "UPDATE" not in allow.upper()):
            raise UpdateException( allow + " allowed" )

        if not added and objectSame == True and "CHANGE" in allow.upper():
            raise UpdateException( allow + " allowed" )

    def get_tag_text(self, xml_tree, tag_name):
        tag_text = None
        tag = xml_tree.find(tag_name)
        if tag <> None: tag_text = self.stringdecode(tag.text)
        return tag_text
        
    def uniqueNames(self, NameOwner):
        unique = []
        for (name, owner) in NameOwner:
            if owner:
                unique.append("%s%s%s"%(str(name), self.SHARED_CHAR, str(owner.Name())))
            else:
                unique.append(str(name))
        return unique

    def SetDefProt(self, use_def_prot):
        """ Convert 4 character string octal protection to internal integer describing
            OwnGrpOrgWld protection

            > SetDefProt("7776"):
            1
        """
        use_def_prot=use_def_prot.strip()

        if len(use_def_prot) == 4 and use_def_prot.isdigit():
            self.use_def_prot = (4095 - (int("".join( [ str( (int(chr) & 2) | (int(chr) & 4) >> 2 | (int(chr) & 1) << 2) for chr in reversed(use_def_prot)] ), 8)))
            logger.DLOG('Protection: %s = %s' %(use_def_prot, self.use_def_prot))
        elif use_def_prot.upper() in ('YES', '1', 'TRUE', 'DEFAULT'):
            self.use_def_prot = True
        else:
            self.use_def_prot = False

    def Export(self, params):
        export_items = params[self.Name()]
        if len(export_items) == 1: # and '*' in export_items[0]:
            """ Expand list and filter on name if entered in the GUI """
            namefilter = export_items[0]
            export_items = [str(object) for object in self.Select()]
            
            export_items = fnmatch.filter(export_items, namefilter)

        basepath = params['basepath'].AsString()
        if not os.path.exists(basepath):
            Transporter.export_fail_count+= len(export_items)
            raise IOError("Path <%s> does not exist"%basepath)

        if str(params.get('addfilepath', 'NO')).upper() in ('YES', '1', 'TRUE'):
            outputpath = os.path.join( basepath, self.FilePath() )
            if not os.path.exists(outputpath):
                logger.LOG("Creating directory '%s' for %s"%( outputpath, self.ClassName() ))
                os.mkdir(outputpath)
        else:
            outputpath = basepath
            
        for name in export_items:
            logger.LOG('Exporting %s %s' %(self.ClassName(), name))
            try:
                output = self.ExportSingle(params, name)
                if output:
                    self.StringToFile(outputpath, output, name)
                    Transporter.export_success_count+= 1
            except Exception, msg:
                Transporter.export_fail_count+= 1
                logger.ELOG("Failed: %s %s"%(Exception, msg))
                logger.DLOG("Traceback: %s"%(traceback.format_exc()))
                Transporter.export_failures[self.Name()+':\t'+name] = msg
            else:
                logger.DLOG("Success")

    def Import(self, params):
        import_items = params[self.Name()]

        basepath = params['basepath'].AsString()

        if str(params.get('addfilepath', 'NO')).upper() in ('YES', '1', 'TRUE'):
            inputpath = os.path.join( basepath, self.FilePath() )
            logger.LOG('Importing from %s' %(inputpath))
        else:
            inputpath = basepath

        if not os.path.exists(inputpath):
            Transporter.import_fail_count += len(import_items)
            raise IOError("Path <%s> does not exist"%inputpath)
        
        for name in import_items:
            logger.LOG('Importing %s %s' %(self.ClassName(), name))
            try:
            
                # Assuming name is object name, if no file present with given name.
                # User able to provide file or object names.
                filepath = os.path.join(inputpath, name)
                if not os.path.exists(filepath):
                    nname = self.GetFilename(name)
                    if name != nname:
                        name = nname
                        logger.WLOG("Warning: changed filename to %s" % name)

                text = self.fileToString(inputpath, name)
                name = os.path.splitext(name)[0]
                # for file names with name.xml.qf and name.amba.qf
                if name.find(".xml.") > 0: name = name.split(".xml.")[0]
                if name.find(".amba.") > 0: name = name.split(".amba.")[0]

                newname = urllib.unquote(name)

                if name != newname:
                    logger.WLOG("Warning: changed name to %s"%newname)
                    name = newname

                replaceText = os.environ.get('FCSTransporterTag', None)
                if replaceText:
                    text = re.sub(r'\$TIT:?.*?\$', r'$TIT: %s$'%replaceText, text)
                    logger.LOG("Replace $TIT : %s$"%replaceText)

                replaceText = os.environ.get('TransporterImportTag', None)                    
                if replaceText:
                    text = text.replace('%TransporterImportTag%', replaceText)
                    logger.LOG("Replace %%TransporterImportTag%%:%s"%replaceText)

                self.ImportSingle(params, name, text)
            except Exception, msg:
                Transporter.import_fail_count+= 1
                Transporter.import_failures[self.Name()+':\t'+name] = msg
                logger.ELOG("Failed: %s %s"%(Exception, msg))
                logger.DLOG("Traceback: %s"%(traceback.format_exc()))
            else:
                if self.added: Transporter.import_add_count+= 1
                else: Transporter.import_update_count+= 1
                logger.DLOG("success")


    def GetFilename(self, objName):
        extension = self.Extension()
        if ',' in extension:
            extension = extension.split(',')[0]

        filename = objName + extension
        if transporterSetup.get('specialCharConv', 'True') == 'True':
            filename = urllib.quote(objName, ' @.()') + extension
        return filename


    def AddAcmTags(self, xmlRoot, acmObj, standardTags=True, **kwargs):
        if standardTags == True:
            ET.SubElement(xmlRoot, "acm_version").text = acm.Version()
            ET.SubElement(xmlRoot, "version").text = "%s $"%(str(acmObj.VersionId()))+"Id"+"$"
            ET.SubElement(xmlRoot, "update_time").text = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(acmObj.UpdateTime()))
            ET.SubElement(xmlRoot, "object_name").text = acmObj.Name().decode(self.CODEC)
        
            xmlOwner = ET.SubElement(xmlRoot, "owner")
            
            owner = acmObj.Owner()
            if owner: 
                xmlOwner.text = owner.Name().decode(self.CODEC)

            ET.SubElement(xmlRoot, "protection").text = str(acmObj.Protection())

        for key, val in kwargs.iteritems():
            elem = ET.SubElement(xmlRoot, key)
            if val is not None:
                elem.text = str(val).decode(self.CODEC)

    def AddPersistentLinks(self, xmlRoot, archiveAsString ):
        etObj = ET.fromstring(archiveAsString)
        persistentLinks = ET.SubElement(xmlRoot, "persistentLinks")

        for obj in etObj.findall('.//FPersistent'):
            cls = obj.find('Class/FDomain/DomainName/string').text
            ptrint = obj.find('StorageId/ptrint')
            if ptrint != None:
                oid = ptrint.text
                inst = acm.GetClass(cls)[oid]
                if inst != None:
                    if inst.Name().endswith(str(inst.Oid())) and inst.Name() != str(inst.Oid()):
                        logger.WLOG("Skipped link %s %s Oid %s"%(cls, inst.Name(), oid))
                    if inst.Name() != str(inst.Oid()) and not inst.Name().endswith(str(inst.Oid())):
                        persistentLink = ET.SubElement(persistentLinks, "persistentLink")
                        ET.SubElement(persistentLink, "class").text = cls
                        ET.SubElement(persistentLink, "oid").text = oid
                        ET.SubElement(persistentLink, "name").text = inst.Name().decode(self.CODEC)
                        
                        tag = ET.SubElement(persistentLink, "user")

                        if hasattr(inst, 'User') and "user" in [str(att.Name()) for att in inst.Class().Attributes()]:
                            if inst.User():
                                tag.text = inst.User().Name().decode(self.CODEC)
                                logger.LOG("Store link %s %s@%s Oid %s"%(cls, inst.Name(), tag.text, oid))
                            else:
                                tag.text = '0'
                        else:
                            tag.text = ''
                            logger.LOG("Store link %s %s Oid %s"%(cls, inst.Name(), oid))
                else:
                    logger.WLOG("Can not store link %s Oid %s" %(cls, oid))

    def PersistentRelink(self, mainObj, archiveData):
        xmlObj = ET.fromstring(archiveData)
        for obj in xmlObj.findall('.//FPersistent'):
            cls = obj.findtext('Class/FDomain/DomainName/string')
            oid = obj.findtext('StorageId/ptrint')
            if cls and oid:
                for link in mainObj.findall('./persistentLinks/persistentLink'):
                    if self.get_tag_text(link, "class") == cls and \
                        self.get_tag_text(link, "oid") == oid:
                        name = self.get_tag_text(link, "name")
                        user = self.get_tag_text(link, "user")

                        if user and "user" in [str(att.Name()) for att in acm.GetClass(cls).Attributes()]:
                            if user == '0':
                                inst = ([ws for ws in acm.GetClass(cls).Select('''name="%s" and user=0'''%(name) )] + [None])[0]
                            else:
                                inst = ([ws for ws in acm.GetClass(cls).Select('''name="%s" and user="%s"'''%(name, user) )] + [None])[0]
                        else:
                            inst = acm.GetClass(cls)[name]
             
                        if inst:
                            if str(inst.Oid()) != oid:
                                if user and user != '0':
                                    logger.LOG("Relink %s %s@%s Oid %s->%s"%(cls, name, user, oid, inst.Oid() ))
                                else:
                                    logger.LOG("Relink %s %s Oid %s->%s"%(cls, name, oid, inst.Oid()))
                                obj.find('StorageId/ptrint').text = str(inst.Oid())
                        else:
                            logger.WLOG("Relink instance %s %s Oid %s not found"%(cls, name, oid))

        return ET.tostring(xmlObj, 'ISO-8859-1')


    def vars(self):
        return [[self.Name(), self.Name()+' name(s)', 'string', [], None, 0, 1, 'Select %ss'%self.ClassName()+('\nRunScriptCMD:%s'%(self.Name().replace(' ', '_')))[:None if IN_PRIME else 0] + '\nAdded File Path: %s'%self.FilePath(), None, True]]


    def Extension(self):
        extension=self.customfileextensions.get(self.Name(), None)
        if not extension:
            return self.DEFAULT_EXTENSION
        return extension


    def FilePath(self):
        filepath=self.customfilepath.get(self.Name(), None)
        if not filepath:
            return self.Name().replace(' ', '_')
        return filepath


    def Delete(self, params):
        error = 0
        delete_items = params[self.Name()]
        for name in delete_items:
            logger.LOG("Delete %s %s"%(self.Name(), name))
            object = self.SelectSingle(name)

            if not object:
                logger.WLOG("%s %s does not exist" % (self.Name(), name))
                error += 1
            else:
                try:
                    object.Delete()
                except Exception, msg:
                    logger.ELOG("%s %s could not be deleted: %s" % (self.Name(), name, msg))
                    error += 1
                else:
                    logger.DLOG("Success")
        return error

    def SelectSingle(self, name):
        return acm.GetClass(self.ClassName())[name]

    def SelectObjects(self,query=''):
        return acm.GetClass(self.ClassName()).Select(query)

    def Select(self, owner=None):
        klass = acm.GetClass(self.ClassName())
        assert klass, self.ClassName()+' not found in the system'

        objects = [ a for a in klass.Select('') \
                        if not owner or (owner and a.Owner() and a.Owner().Name() == owner)]
        return self.Names(objects)

    def Names(self, objects):
        klass = acm.GetClass(self.ClassName())
        assert klass, self.ClassName()+' not found in the system'

        if klass.GetMethod('User', 0):
            return self.uniqueNames( [ (object.Name(), object.User()) for object in objects] )
        else:
            return [ object.Name() for object in objects]


class AELTransporter(XMLTransporter):
    def SetDefProt(self, use_def_prot):
        """ Convert 4 character string octal protection to ael protection string
            OwnGrpOrgWld protection <-> W,O,G,U

            > SetDefProt("7776"):
            'W:R,O:R,G:RWD,U:RWD'
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

        use_def_prot=use_def_prot.strip()
        if len(use_def_prot) == 4 and use_def_prot.isdigit():
            self.use_def_prot = "W:%s,O:%s,G:%s,U:%s"%( int2prot(use_def_prot[3]), int2prot(use_def_prot[2]), int2prot(use_def_prot[1]), int2prot(use_def_prot[0]))
            logger.DLOG('Protection: %s = %s' %(use_def_prot, use_def_prot))
        elif use_def_prot.upper() in ('YES', '1', 'TRUE', 'DEFAULT'):
            self.use_def_prot = True
        else:
            self.use_def_prot = False


class FTradeFilterTransporter(AELTransporter):
    DEFAULT_EXTENSION=".tf"

    def GetQuery(self, tf):
        """ Convert locale date serialised dates to ISO """
        query = []
        
        checkDate = re.compile('\d{1,4}[/.-]\d{1,4}[/.-]\d{1,4}$')
        for en in tf.get_query():
            qline = []
            for tok in en:
                if checkDate.match(tok) is not None:
                    try:
                        tok = ael.date_from_string(tok).to_string(ael.DATE_ISO)
                    except:
                        logger.DLOG(traceback.format_exc())
                qline.append(tok)
            query.append( tuple( qline ))
        return query
        
        
    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])
        tf = ael.TradeFilter[name]


        if not tf:
            raise Exception("Trade Filter %s does not exist" % name)

        if date and str(date).strip() != '':
            if ael.date_from_time(tf.updat_time) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None

        tf_root = ET.Element("FTradeFilter")
        
        tf_acm_version = ET.SubElement(tf_root, "acm_version")
        tf_acm_version.text = acm.Version()

        tf_version = ET.SubElement(tf_root, "version")
        tf_version.text = "%s $"%(str(tf.version_id))+"Id"+"$"
        
        tf_export_time = ET.SubElement(tf_root, "update_time")
        tf_export_time.text = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(tf.updat_time))

        object_name = ET.SubElement(tf_root, "object_name")
        object_name.text = tf.fltid.decode(self.CODEC)
                                
        tf_data_owner = ET.SubElement(tf_root, "owner")
        tf_data_owner.text = tf.owner_usrnbr.userid.decode(self.CODEC)
        
        tf_protection = ET.SubElement(tf_root, "protection")
        tf_protection.text = tf.protection
        
        if tf.query_seqnbr:
            tf_data_queryname = ET.SubElement(tf_root, "asql_query")
            tf_data_queryname.text = tf.query_seqnbr.name.decode(self.CODEC)
            logger.WLOG("Warning: Tradefilter '%s' is using ASQL query '%s'"%  (tf.fltid, tf.query_seqnbr.name))
        else:
            tf_data_query = ET.SubElement(tf_root, "query")            
            tf_data_query.text = str(self.GetQuery(tf)).decode(self.CODEC)

        return ET.tostring(tf_root, 'ISO-8859-1')

    def ImportSingle(self, params, name, text):
        tf_file_xml = ET.fromstring(text)
                
        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(tf_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()
        owner_usrnbr = ael.User[owner].usrnbr
        
        tf_asql_query = tf_file_xml.find("asql_query")
        if tf_asql_query <> None: tf_asql_query = self.stringdecode( tf_asql_query.text )
        else: tf_asql_query = None
        
        tf_query = tf_file_xml.find("query")
        if tf_query <> None: tf_query = self.stringdecode( tf_query.text )
        else: tf_query = None
        
        real_name = self.get_tag_text(tf_file_xml, "object_name")
        if not real_name:
            real_name = name
        tf = ael.TradeFilter[real_name]

        if tf:
            if (tf.query_seqnbr and tf.query_seqnbr.name == tf_asql_query) or \
                ((not tf.query_seqnbr) and (str(self.GetQuery(tf)) == tf_query) ):
                objectSame = True
            else:
                objectSame = False
        else:
            objectSame = None

        self.checkAllowed(params.get("allow", "Insert & Update"), tf == None, objectSame) # Exception if not allowed

        if tf:
            self.added = False
            tf = tf.clone()
        else:
            tf = ael.TradeFilter.new()
            self.added = True
        
        tf.fltid = real_name
        tf.owner_usrnbr = owner_usrnbr
        
        if type(self.use_def_prot) == type(''):
            tf.protection = self.use_def_prot
        elif self.use_def_prot == True:
            pass #tf.protection = None
        else:             
            tf.protection = self.get_tag_text(tf_file_xml, "protection")

        if tf_asql_query:
            tf.set_query([])
            asql = ael.TextObject.read('type = "SQL Query" and name = "%s"' % tf_asql_query)
            if asql:                    
                tf.query_seqnbr = asql
            else:
                raise Exception("Failed to Import Trade Filter %s because of missing ASQL Query '%s'" % (tf.fltid, tf_asql_query))
        elif tf_query:
            tf.set_query(eval(tf_query, {"__builtins__": __builtins__}))
        else: 
            raise Exception("Trade Filter File %s has wrong format" % name)
        tf.commit()

        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return tf
        
    def Name(self):
        return 'Trade Filter'
    def ClassName(self):
        return 'FTradeSelection'


class FASQLQueryTransporter(AELTransporter):
    DEFAULT_EXTENSION=".asql"

    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])
        asql = ael.TextObject.read('type = "SQL Query" and name = "%s"' % name)
        assert asql, self.Name()+':'+name+' not found in the system'
        if date and str(date).strip() != '':
            if ael.date_from_time(asql.updat_time) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
        return asql.get_text()

    def ImportSingle(self, params, name, text):
        asql = ael.TextObject.read('type = "SQL Query" and name = "%s"' % name)

        if asql:
            objectSame = asql.get_text() == text
        else:
            objectSame = None
            
        self.checkAllowed(params.get("allow", "Insert & Update"), asql == None, objectSame) # Exception if not allowed
    
        if asql:
            self.added = False
            asql = asql.clone()
            asql.set_text(text)
            if self.owner:
                asql.owner_usrnbr = self.owner.Name()

        else:
            self.added = True
            asql = ael.TextObject.new()
            asql.type = "SQL Query"
            asql.name = name
            asql.set_text(text)
            if self.owner:
                asql.owner_usrnbr = self.owner.Name()

        if type(self.use_def_prot) == type(''):
            asql.protection = self.use_def_prot
        #elif self.use_def_prot == True:
        #    asql.protection = None

        asql.commit()
        if self.added:
            logger.LOG("Added %s" %name)
        else:
            logger.LOG("Updated %s" %name)

        return asql
        
    def Name(self):
        return 'ASQL Query'
    def ClassName(self):
        return 'FSQL'


class FStoredASQLQueryTransporter(XMLTransporter):
    DEFAULT_EXTENSION=".xml.qf"
    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])

        qf = self.SelectSingle(name)

        assert qf, self.Name()+':'+name+' not found in the system'

        if date and str(date).strip() != '':
            if ael.date_from_time(qf.UpdateTime()) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
            
        qf_root = ET.Element("FStoredASQLQuery")

        try:
            self.AddAcmTags(qf_root, qf, shared=str(qf.User() == None), subtype=qf.SubType(), data=qf.Archive())
        except AttributeError:
            self.AddAcmTags(qf_root, qf, shared=str(qf.User() == None), subtype=qf.SubType(), data=qf.Text())

        return ET.tostring(qf_root, 'ISO-8859-1')

    def ImportSingle(self, params, name, inputText):
        qf_file_xml = ET.fromstring(inputText)

        if type(self.use_def_prot) == type(0):
            protection = self.use_def_prot
        elif self.use_def_prot == True:
            protection = None
        else:             
            protection = int(self.get_tag_text(qf_file_xml, "protection"))
        
        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(qf_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()

        qf_subtype = qf_file_xml.find("subtype")
        if qf_subtype <> None: qf_subtype = qf_subtype.text
            
        qf_archive_data = qf_file_xml.find("data")
        
        qf_shared = qf_file_xml.findtext("shared", 'True') in ('True', '1', 'Yes')

        if qf_archive_data <> None: qf_archive_data = self.stringdecode( qf_archive_data.text )
                   
        real_name = self.get_tag_text(qf_file_xml, "object_name")

        if not real_name:
            real_name = name

        if not qf_archive_data:
            raise Exception("Query Folder File %s has wrong format" % name)

        if not qf_shared:
            ownernum = acm.FUser[owner].Oid()
        else:
            ownernum = 0

        logger.DLOG( "acm.FStoredASQLQuery.Select(name='%s' and user=%d)" %(real_name, ownernum))
        qf = (list(acm.FStoredASQLQuery.Select('''name="%s" and user=%d''' %(real_name, ownernum)))+[None])[0]

        if qf:
            if qf.SubType() == qf_subtype and qf_archive_data == qf.Text():
                objectSame = True
            else:
                objectSame = False
        else:
            objectSame = None

        self.checkAllowed(params.get("allow", "Insert & Update"), qf == None, objectSame) # Exception if not allowed
    
        if qf:
            self.added = False
        else:
            qf = acm.FStoredASQLQuery()
            qf.Name(real_name)
            self.added = True

        qf.Owner(owner)
        qf.SubType(qf_subtype)        
        if type(protection) == type(0): qf.Protection(protection)
        
        try:
            qf.Archive(qf_archive_data)
        except AttributeError:
            qf.Text(qf_archive_data)

        qf.AutoUser(False)
        if not qf_shared:
            qf.User(owner)
        qf.Commit()                            

        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return qf
            

    def Name(self):
        return 'Query Folder'
    def ClassName(self):
        return 'FStoredASQLQuery'
    def SelectSingle(self, name):
        qf=None
        try:
            if name.isdigit():
                qf = acm.FStoredASQLQuery[name]
            else:
                if name.find(self.SHARED_CHAR) > 0:
                    name, owner = name.split(self.SHARED_CHAR)
                    ownernum = acm.FUser[owner].Oid()
                else:
                    ownernum = 0
                
                logger.DLOG( '''acm.FStoredASQLQuery.Select(name="%s" and user=%d)''' %(name, ownernum))
                qf = (list(acm.FStoredASQLQuery.Select('''name="%s" and user=%d''' %(name, ownernum)))+[None])[0]

        except Exception, msg:
            logger.DLOG( "Select %s failed: %s/%s" %(name, str(Exception), msg))
        return qf


class FAelTaskTransporter(XMLTransporter):
    DEFAULT_EXTENSION=".xml.task"
    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])
        task = acm.FAelTask[name]

        assert task, self.Name()+':'+name+' not found in the system'

        if date and str(date).strip() != '':
            if ael.date_from_time(task.UpdateTime()) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
   
        task_root = ET.Element("FAelTask")

        self.AddAcmTags(task_root, task,\
                        module=task.ModuleName(), context=task.Context().Name(),\
                        parameter=task.ParametersText(), historylength=task.HistoryLength(),\
                        description=task.Description(), logfilename=task.LogFileName())
        """
        if task.Schedules():
            scheds_root = ET.SubElement(task_root, "Schedules")
            for schedule in task.Schedules():
                sched_root = ET.SubElement(scheds_root, "Schedule")
                self.AddAcmTags(sched_root, schedule, standardTags=False,\
                        DailyRepeat=schedule.DailyRepeat(),
                        DailyRepeatInterval = schedule.DailyRepeatInterval(),
                        DailyRepeatUntil = schedule.DailyRepeatUntil(),
                        DailyRunTime = schedule.DailyRunTime(),
                        Enabled = schedule.Enabled(),
                        Executor = schedule.Executor(),
                        MonthOptionDayNumber = schedule.MonthOptionDayNumber(),
                        Period = schedule.Period(),
                        PeriodInterval = schedule.PeriodInterval(),
                        Rib = schedule.Rib(),
                        Schedule = schedule.Schedule(),
                        StartDate = schedule.StartDate())
        """
        return ET.tostring(task_root, 'ISO-8859-1')

    def ImportSingle(self, params, name, inputText):
        task_file_xml = ET.fromstring(inputText)

        if type(self.use_def_prot) == type(0):
            protection = self.use_def_prot
        elif self.use_def_prot == True:
            protection = None
        else:             
            protection = int(self.get_tag_text(task_file_xml, "protection"))

        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(task_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()

        real_name = self.get_tag_text(task_file_xml, "object_name")
    
        task_parameter = self.stringdecode(task_file_xml.find("parameter").text )
        task_module = self.stringdecode(task_file_xml.find("module").text)
        historylength = params.get('taskhistorylength', None) or self.get_tag_text(task_file_xml, "historylength")
        description = self.get_tag_text(task_file_xml, "description")
        logfilename = self.get_tag_text(task_file_xml, "logfilename")
        context = self.get_tag_text(task_file_xml, "context")
        
        task = acm.FAelTask[real_name]

        self.checkAllowed(params.get("allow", "Insert & Update"), task == None)# Exception if not allowed        
        if task:
            self.added = False
        else:
            self.added = True
            task = acm.FAelTask()
            task.Name(real_name)

        task.ModuleName(task_module)
        task.ParametersText(task_parameter)
        task.Owner(owner)
        if type(protection) == type(0): task.Protection(protection)
        if historylength: task.HistoryLength(historylength)
        if description: task.Description(description)
        if logfilename:
            task.LogFileName(logfilename)
        if context: task.Context(context)

        task.Commit()    
        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return task

    def Name(self):
        return 'Task'
    def ClassName(self):
        return 'FAelTask'


class FAelTransporter(XMLTransporter):
    DEFAULT_EXTENSION=".py"
    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])
        ael_module = acm.FAel[name]
        if ael_module:
            if date and str(date).strip() != '':
                if ael.date_from_time(ael_module.UpdateTime()) < date:
                    logger.WLOG('%s %s is too old' %(self.Name(), name))
                    Transporter.export_expiry_count+= 1
                    Transporter.export_expiries.append(self.Name()+':\t'+name)
                    return None
            return ael_module.Text()
        else:
            raise Exception('%s %s not found' %(self.Name(), name))
            
    def ImportSingle(self, params, name, inputText):
        ael_module = acm.FAel[name]

        if ael_module:
            objectSame = ael_module.Text() == inputText
        else:
            objectSame = None
    
        self.checkAllowed(params.get("allow", "Insert & Update"), ael_module == None, objectSame) # Exception if not allowed
        if ael_module:
            self.added = False
            ael_module.Text(inputText)
            if self.owner:
                ael_module.Owner(self.owner)
        else:
            self.added = True
            ael_module = acm.FAel()    
            ael_module.Name(name)
            ael_module.Text(inputText)
            if self.owner:
                ael_module.Owner(self.owner)

        if type(self.use_def_prot) == type(0):
            ael_module.Protection(self.use_def_prot)

        ael_module.Commit()
        if self.added:
            logger.LOG("Added %s" %name)
        else:
            logger.LOG("Updated %s" %name)
            
        return ael_module

    def Name(self):
        return 'Python'
    def ClassName(self):
        return 'FAel'


class FExtensionModuleTransporter(XMLTransporter):
    DEFAULT_EXTENSION = ".txt"
    onlyUserModules=False
    splitModule=False
    splitModuleExtensions=eval( transporterSetup.get('splitExtensionModule',
                """{'FPythonCode':'.py','FPythonCode':'.xsl'}"""), {"__builtins__": __builtins__} )

    def Extension(self):
        if self.splitModule:
            extension=self.splitModuleExtensions.get('FExtensionModule', '.split.txt')
        else:
            extension=self.customfileextensions.get(self.Name(), None)
            if not extension:
                return self.DEFAULT_EXTENSION
        return extension


    def SplitModule(self, extname, em, basepath):
        """ Split Extension Module in parts defined in FParameters 
            Save the parts in an folder with the same name as the extension module"""

        outputpath = os.path.join(basepath, extname)

        logger.LOG("Split %s module parts into %s"%(extname, outputpath))
        context = acm.Create('FExtensionContext')
        context.AddModule(em)

        for (extType, fileExt) in self.splitModuleExtensions.iteritems():
            if extType == 'FExtensionModule':
                continue

            counter = 0

            for counter, ext in enumerate( em.GetAllExtensions(extType), 1):
                name = ext.Name().AsString()
                className = ext.ClassExtension().ExtendedClass().Name().AsString()
                if className == "FObject":
                    filename = name
                else:
                    filename = "%s@%s"%(name, className)
                    
                logger.DLOG(" extract %s %s"%(extType, name))
                output = str(ext.Value())[:-1]
                if not os.path.exists(outputpath):
                    os.mkdir(outputpath)

                self.StringToFile( outputpath, output, filename, extension = fileExt)

                self.EditImport(context, name, extType, className, content = "") # Instead of removing extension completely, it's set to empty otherwise the groups are removed

            logger.LOG("Split %d %s objects"%(counter, extType))


    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])

        basepath = params['basepath'].AsString()
        
        if str(params.get('addfilepath', 'NO')).upper() in ('YES', '1', 'TRUE'):
            outputpath = os.path.join( basepath, self.FilePath() )
        else:
            outputpath = basepath

        self.splitModule = params['SplitModules'] in ('true', 1, True)
        
        em = self.SelectSingle(name)
        assert em, self.Name()+':'+name+' not found in the system'
        
        if date and str(date).strip() != '':
            if ael.date_from_time(em.UpdateTime()) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None

        try:
            if self.splitModule:
                emClone = em.Clone()

                self.SplitModule(name, em, outputpath)
                em = self.SelectSingle(name) # Catch changed extension module, this is on purpose!
                
            output = em.AsString()

        finally:
            if self.splitModule:
                em.Apply(emClone)        

        # Set the timestamp to update time instead of export time # timestamp (utc) "2011-02-18 23:50:35"
        if '# timestamp (utc)' in output.splitlines()[3] :
            output = output.replace(output.splitlines()[3], \
                                    '# timestamp (utc) "%s"'%time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(em.UpdateTime())))
        # Replace empty description to CVS id tag
        return output.replace('\ndescription ""', '\ndescription "$'+"Id"+'$"')


    def EditImport(self, context, name, extType, className, content):
        """ Store extension in module """
        equal = ' =' if extType not in ('FPythonCode', 'FXSLTemplate', 'FUserDefinedPayoff', 'FStringResource', 'FSource', 'FExtensionAttribute', 'FExtensionValue', 'FDocString', 'FAgentTemplate') else ''
        
        updateString="[]%s:%s%s\n%s\n"%(className, name, equal, content)

        context.EditImport(extType, updateString)


    def MergeModule(self, extname, em, basepath):
        """ Merge parts into Extension Module"""
        
        filepath = os.path.join(basepath, extname )
        logger.LOG("Merge %s module parts from %s"%(extname, filepath))
        
        try:
            files = os.listdir(filepath) 
        except:
            logger.WLOG("The system cannot find the path specified: %s"%(filepath))
            files = []

        context = acm.Create('FExtensionContext')
        context.AddModule(em)

        for (extType, fileExt) in self.splitModuleExtensions.iteritems():
            if extType == 'FExtensionModule':
                continue

            counter = 0
            for counter, filename in enumerate( fnmatch.filter(files, "*" + fileExt), 1 ):
                logger.DLOG("Merge %s file into %s"%(filename, extname))
                
                inputText = self.fileToString(filepath, filename)
                name = filename.replace(fileExt, '')
                if '@' in filename:
                    (name, className) = name.split('@')
                else:
                    className = "FObject"
                
                self.EditImport(context, name, extType, className, inputText)

            logger.LOG("Merged %d %s objects"%(counter, extType))
        em.Commit()


    def ImportSingle(self, params, name, inputText):
    
        self.splitModule = params['SplitModules'] in ('true', 1, True)
        
        if ACM_INTERNAL_VERSION < 4.04:
            inputText = inputText.replace('\n...\n\n', '\n\xa4\n')
        data = acm.ImportExtensionModule(inputText)
        assert data, self.Name()+':'+name+' not could not be loaded'
        
        real_name = data.Name()
        if real_name != name:
            logger.LOG("(as '%s')"%(real_name))
        em = self.SelectSingle(real_name)
        
        if em:
            output = em.AsString()
            objectSame = inputText.replace(inputText.splitlines()[3], "") == output.replace(output.splitlines()[3], "")
        else:
            objectSame = None

        self.checkAllowed(params.get("allow", "Insert & Update"), em == None, objectSame) # Exception if not allowed

        if (params.get('UserModules', False) in ('true', 1, True) or self.onlyUserModules) and not self.owner:
            setOwner = acm.FUser[real_name]
            if not setOwner:
                logger.WLOG('User "%s" does not exist' %(real_name))
        else:
            setOwner = self.owner

        if em:
            self.added = False
            em.Apply(data)

            if type(self.use_def_prot) == type(0):
                em.Protection(self.use_def_prot)

            if setOwner:
                em.Owner(setOwner)
 
            try:
                em.Commit()
            except RuntimeError:
                em.Undo()
                em = self.SelectSingle(real_name)
                acm.BeginTransaction()
                try:
                    em.Delete()
    
                    em = acm.FExtensionModule()
                    em.Apply(data)
                    if type(self.use_def_prot) == type(0):
                        em.Protection(self.use_def_prot)
                    if setOwner:
                        em.Owner(setOwner)
                    em.Commit()
                    acm.CommitTransaction()
                except:
                    acm.AbortTransaction()
                    raise
        else:
            self.added = True
            em = acm.FExtensionModule()

            if type(self.use_def_prot) == type(0):
                em.Protection(self.use_def_prot)

            if setOwner:
                em.Owner(setOwner)
            em.Apply(data)
            em.Commit()

        if self.splitModule:
            basepath = params['basepath'].AsString()
            if str(params.get('addfilepath', 'NO')).upper() in ('YES', '1', 'TRUE'):
                inputPath = os.path.join(basepath, self.FilePath() )
            else:
                inputPath = basepath
                
            self.MergeModule(real_name, em, inputPath )

        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return em

    def SetSplitModuleCB(self, index, fieldvalues):
        self.splitModule = fieldvalues[index] in ('true', 1, True)
        return fieldvalues

    def SetUserModuleCB(self, index, fieldvalues):
        self.onlyUserModules = fieldvalues[index] in ('true', 1, True)
        return fieldvalues

    def SetUserModuleUpdateCB(self, index, fieldvalues):
        self.SetUserModuleCB(index, fieldvalues)
        objects = self.ael_variables[index+1][3]
        if type(objects) == type([]):
            del objects[:] # List
        else:
            objects.Clear() # FArray

        for name in self.Select():
            if type(objects) == type([]):
                objects.append(name)  
            else:
                objects.Add(name)

        return fieldvalues
        
    def ExtraExportParameter(self):
        vars=[['SplitModules', 'Split Modules', 'bool', [False, True], False, 0, 0, 'Split modules into parts'+'\nRunScriptCMD:SplitModules'[:None if IN_PRIME else 0], self.SetSplitModuleCB, True],
              ['UserModules', 'User Modules', 'bool', [False, True], False, 0, 0, 'Show only user modules'+'\nRunScriptCMD:UserModules'[:None if IN_PRIME else 0], self.SetUserModuleUpdateCB, True],]
        return vars    

    def ExtraImportParameter(self):
        vars=[['SplitModules', 'Split Modules', 'bool', [False, True], False, 0, 0, 'Join module parts into module'+'\nRunScriptCMD:SplitModules'[:None if IN_PRIME else 0], self.SetSplitModuleCB, True],
              ['UserModules', 'User Modules', 'bool', [False, True], False, 0, 0, 'Import user modules, set owner on module to user'+'\nRunScriptCMD:UserModules'[:None if IN_PRIME else 0], self.SetUserModuleCB, True]]
        return vars

    def Name(self):
        return 'Extension Module'
        
    def ClassName(self):
        return 'FExtensionModule'
        
    def Select(self, owner=None):
        if self.onlyUserModules:
            return [em.Name() for em in acm.FExtensionModule.Select('') \
                    if ( em.Owner() and str(em.Name()) == str(em.Owner().Name()) )\
                        and (not owner or (owner and em.Owner() and em.Owner().Name() == owner))]
        else:
            return [em.Name() for em in acm.FExtensionModule.Select('') \
                    if not ( em.Owner() and str(em.Name()) == str(em.Owner().Name()) )\
                        and (not owner or (owner and em.Owner() and em.Owner().Name() == owner))] + ['Default']


    def SelectSingle(self, name):
        em = acm.FExtensionModule[name]
    
        if not em:
            for module in acm.GetDefaultContext().Modules():
                if str(module.Name()) == name:
                    em=module
        return em


class FTradingSheetTemplateTransporter(XMLTransporter):
    DEFAULT_EXTENSION=".xml.tst"
    xmlSerializer = XmlSerializer()

    def ExportSheet(self, sheet, xmlRoot):
        tsRoot = ET.SubElement(xmlRoot, "FTradingSheet")
 
        ET.SubElement(tsRoot, "type").text = str(sheet.Class().Name())
        
        ts_archive_data = ET.SubElement(tsRoot, "data")

        xmlText = self.xmlSerializer.ExportStream(sheet, transporterSetup.get('compressStream', 'True')=='True')

        ts_archive_data.text = xmlText
        #self.AddPersistentLinks(tsRoot, xmlText)
                
        assert xmlText, "%s Could not export %s %s" %(self.Name(), sheet.Class().Name(), sheet.SheetName())


    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])

        wb = self.SelectSingle(name)

        assert wb, self.Name()+':'+name+' not found in the system'

        if date and str(date).strip() != '':
            if ael.date_from_time(wb.UpdateTime()) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
            
        wbRoot = ET.Element("FTradingSheetTemplate")

        self.AddAcmTags(wbRoot, wb, shared=str(wb.User() == None) )


        #Retrieve the Trading Sheet
        ts = wb.TradingSheet()
        
        self.ExportSheet(ts, wbRoot)

        return ET.tostring(wbRoot, 'ISO-8859-1')


    def ImportSheet(self, ts_elem):
        ts_type = ts_elem.find("type").text
        ts_archive_data = self.stringdecode( ts_elem.find("data").text )

        ts = self.xmlSerializer.ImportStream(ts_archive_data)
        
        ts.Name(ts_type+str(ts.Oid())) # Temporary name
        ts.Commit()        
        ts.Name(ts_type+str(ts.Oid())) # Final Name
        ts.Commit()
        
        return ts_type, ts


    def ImportSingle(self, params, name, inputText):
        wb_file_xml = ET.fromstring(inputText)
        
        if type(self.use_def_prot) == type(0):
            protection = self.use_def_prot
        elif self.use_def_prot == True:
            protection = None
        else:             
            protection = int(self.get_tag_text(wb_file_xml, "protection"))

        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(wb_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()

        real_name = self.get_tag_text(wb_file_xml, "object_name")
        if not real_name:
            real_name = name

        ts_shared = wb_file_xml.findtext("shared", 'True') in ('True', '1', 'Yes')

        if ts_shared:
            tst = (list(acm.FTradingSheetTemplate.Select('''name="%s" and user=0''' % (real_name))) + [None])[0]
        else:
            tst = ([tst for tst in acm.FTradingSheetTemplate.Select('''name="%s"''' % (real_name)) if tst.User() and tst.User().Name() == owner ] + [None])[0]

        self.checkAllowed(params.get("allow", "Insert & Update"), tst == None) # Exception if not allowed
        if not tst:
            self.added = True
            tst = acm.FTradingSheetTemplate()
            tst.Name(real_name)
        else:
            self.added = False

            if str(tst.Name()) != real_name:
                raise UpdateException( 'Update conflict "%s" != "%s"'%(str(tst.Name()), real_name) )

            ts = tst.TradingSheet()
            ts.Delete()

        ts_elem = wb_file_xml.find("FTradingSheet")

        ts_type, ts = self.ImportSheet(ts_elem)
        
        tst.SubType(ts_type)
        tst.ToArchive('TradingSheet', ts )

        tst.Owner(owner)
        if type(protection) == type(0): tst.Protection(protection)
        tst.AutoUser(False)
        if not ts_shared:
            tst.User(owner)
        tst.Commit()

        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return tst

    def Name(self):
        return 'TradingSheetTemplate'

    def ClassName(self):
        return 'FTradingSheetTemplate'

    def SelectSingle(self, name):
        wb = None
        try:
            if name.isdigit():
                wb = acm.FTradingSheetTemplate[name]
            else:
                if name.find(self.SHARED_CHAR) > 0:
                    name, owner = name.split(self.SHARED_CHAR)
                    ownernum = acm.FUser[owner].Oid()
                else:
                    ownernum = 0

                wb = (list(acm.FTradingSheetTemplate.Select('''name="%s" and user=%d''' %(name, ownernum)))+[None])[0]

        except Exception, msg:
            logger.DLOG( "Select %s failed: %s/%s" %(name, str(Exception), msg))

        return wb

class FWorkbookTransporter(FTradingSheetTemplateTransporter):
    DEFAULT_EXTENSION=".wb"
    operationsWB=' (Operations)'
    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])

        wb = self.SelectSingle(name)

        if not wb:
            raise Exception('%s %s is not found' %(self.Name(), name))

        if date and str(date).strip() != '':
            if ael.date_from_time(wb.UpdateTime()) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None

        wb_root = ET.Element('FWorkbook')

        self.AddAcmTags(wb_root, wb, type=str(wb.ClassName()), shared=str(wb.User() == None) )

        wb_archive_data = ET.SubElement(wb_root, "data")

        if transporterSetup.get('compressStream', 'True')=='True':
            wb_archive_data.text = base64.b64encode(zlib.compress(wb.FromArchiveAsString()))
        else:
            wb_archive_data.text = wb.FromArchiveAsString()

        self.AddPersistentLinks(wb_root, wb.FromArchiveAsString())

        #Retrieve the Trading Sheets
        for ts in wb.Sheets():
            self.ExportSheet(ts, wb_root)

        return ET.tostring(wb_root, 'ISO-8859-1')
                
    def ImportSingle(self, params, name, inputText):
        wb_file_xml = ET.fromstring(inputText)
            
        if type(self.use_def_prot) == type(0):
            protection = self.use_def_prot
        elif self.use_def_prot == True:
            protection = None
        else:             
            protection = int(self.get_tag_text(wb_file_xml, "protection"))

        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(wb_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()
        
        real_name = self.get_tag_text(wb_file_xml, "object_name")
        if not real_name:
            real_name = name

        wbtype = self.get_tag_text(wb_file_xml, "type")
        if not wbtype:
            wbtype = 'FWorkbook'
        
        wb_shared = wb_file_xml.findtext("shared", 'False') in ('True', '1', 'Yes')

        if wbtype == 'FWorkbook':
            if wb_shared:
                original_wb = (list(acm.FWorkbook.Select('''name="%s" and user=0''' % (real_name))) + [None])[0]
            else:
                original_wb = (list(acm.FWorkbook.Select('''name="%s" and user="%s"''' % (real_name, owner))) + [None])[0]
        elif wbtype == 'FBackOfficeManagerWorkbook':
            if wb_shared:
                original_wb = (list(acm.FBackOfficeManagerWorkbook.Select('''name="%s" and user=0''' %(real_name))) + [None])[0]
            else:
                original_wb = (list(acm.FBackOfficeManagerWorkbook.Select('''name="%s" and user="%s"''' %(real_name, owner))) + [None])[0]

        self.checkAllowed(params.get("allow", "Insert & Update"), original_wb == None) # Exception if not allowed

        if original_wb:
            if str(original_wb.Name()) != real_name:
                raise UpdateException( 'Update conflict "%s" != "%s"'%( str(original_wb.Name()), real_name) )

        #Create the workbook
        if wbtype == 'FWorkbook':
            wb = acm.FWorkbook()
        else:
            wb = acm.FBackOfficeManagerWorkbook()

        wbdata = self.stringdecode(wb_file_xml.findtext("data"))
        if wbdata:
            try:
                wbdata = zlib.decompress(base64.b64decode(wbdata))
            except:
                pass
            wbdata = self.PersistentRelink( wb_file_xml, wbdata )
            try:
                wb.Archive( wbdata )
            except AttributeError:
                wb.Text( wbdata )

        wb.Name(real_name)
        
        #Add new sheets
        sheets = acm.FArray()
        for ts_elem in wb_file_xml.findall("FTradingSheet"):
            ts_type, ts = self.ImportSheet(ts_elem)

            if ts:
                sheets.Add(ts)
            else:
                logger.ELOG('%s Could not import %s' %(self.Name(), ts_type))

        wb.Sheets(sheets)
        wb.Owner(owner)
        if not wb_shared:
            wb.User(owner)
        if type(protection) == type(0): wb.Protection(protection)
        wb.AutoUser(False)
        
        if original_wb:
            original_wb.AutoUser(False)
            original_wb.Apply(wb)
            original_wb.Commit()
            logger.LOG("Updated %s" %real_name)
            self.added = False
        else:
            wb.Commit()
            logger.LOG("Added %s" %real_name)
            self.added = True
        
        return wb

    def Name(self):
        return 'Workbook'

    def ClassName(self):
        return 'FWorkbook'

    def SelectSingle(self, name):
        wb = None
        nname = name.replace(self.operationsWB, '')
        try:
            if name.isdigit():
                wb = acm.FWorkbook[nname]
            else:
                if name.find(self.SHARED_CHAR) > 0:
                    nname, owner = nname.split(self.SHARED_CHAR)
                    ownernum = acm.FUser[owner].Oid()
                else:
                    ownernum = 0
                
                if name.endswith(self.operationsWB):
                    wb = (list(acm.FBackOfficeManagerWorkbook.Select('''name="%s" and user=%d''' %(nname, ownernum)))+[None])[0]
                else:
                    wb = (list(acm.FWorkbook.Select('''name="%s" and user=%d''' %(nname, ownernum)))+[None])[0]
        except Exception, msg:
            logger.DLOG( "Select %s failed: %s/%s" %(name, str(Exception), msg))

        return wb

    def SelectObjects(self,query=''):
        allwbs = list(acm.GetClass(self.ClassName()).Select(query))
        if ACM_INTERNAL_VERSION >= 4.06:
            allwbs.extend(list( acm.FBackOfficeManagerWorkbook.Select(query) ))
        return allwbs        

    def Select(self, owner=None):
        allwbs = self.uniqueNames( [(a.Name(), a.User()) for a in acm.FWorkbook.Select('')\
                                    if not owner or (owner and a.User() and a.User().Name() == owner)] )
        if ACM_INTERNAL_VERSION >= 4.06:
            allwbsO= self.uniqueNames( [(a.Name(), a.User()) for a in acm.FBackOfficeManagerWorkbook.Select('')\
                                    if not owner or (owner and a.User() and a.User().Name() == owner)] )
            allwbs.extend( [ "%s%s"%(name, self.operationsWB) for name in allwbsO ] )

        return allwbs

    def Names(self, objects):
        names = []
        if ACM_INTERNAL_VERSION >= 4.06:
            Wb = [ a for a in objects if a.IsKindOf(acm.FBackOfficeManagerWorkbook) ]
            objects = [ a for a in objects if not a.IsKindOf(acm.FBackOfficeManagerWorkbook) ]
            Wb= self.uniqueNames( [(a.Name(), a.User()) for a in Wb ] )
            names.extend( [ "%s%s"%(name, self.operationsWB) for name in Wb ] )

        Wb= self.uniqueNames( [(a.Name(), a.User()) for a in objects ] )
        names.extend(Wb)
            
        return names


class FWorkspaceTransporter(XMLTransporter):
    DEFAULT_EXTENSION=".ws"

    def ExportSingle(self, params, name):
        ws = self.SelectSingle(name)

        assert ws, self.Name()+':'+name+' not found in the system'
            
        wsRoot = ET.Element("FWorkspace")
        
        self.AddAcmTags(wsRoot, ws)

        ts_archive_data = ET.SubElement(wsRoot, "data")
        if transporterSetup.get('compressStream', 'True')=='True':
            ts_archive_data.text = base64.b64encode(zlib.compress(ws.FromArchiveAsString()))
        else:
            ts_archive_data.text = ws.FromArchiveAsString()

        self.AddPersistentLinks(wsRoot, ws.FromArchiveAsString())

        assert ts_archive_data.text, "%s Could not export workspace %s" %(self.Name(), ws.Name())
        return ET.tostring(wsRoot, 'ISO-8859-1')


    def ImportSingle(self, params, name, inputText):
        wb_file_xml = ET.fromstring(inputText)
        
        if type(self.use_def_prot) == type(0):
            protection = self.use_def_prot
        elif self.use_def_prot == True:
            protection = None
        else:             
            protection = int(self.get_tag_text(wb_file_xml, "protection"))

        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(wb_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()

        real_name = self.get_tag_text(wb_file_xml, "object_name")
        if not real_name:
            real_name = name

        tst = ([tst for tst in acm.FWorkspace.Select('''name="%s"''' % (real_name)) if tst.User() and tst.User().Name() == owner ] + [None])[0]

        self.checkAllowed(params.get("allow", "Insert & Update"), tst == None) # Exception if not allowed
        if not tst:
            self.added = True
            tst = acm.FWorkspace()
            tst.Name(real_name)
        else:
            self.added = False
            if str(tst.Name()) != real_name:
                raise UpdateException( 'Update conflict "%s" != "%s"'%(str(tst.Name()), real_name) )

        stream = self.stringdecode( wb_file_xml.find("data").text )
        try:
            stream = zlib.decompress(base64.b64decode(stream))
        except:
            pass
        
        ts_archive_data = self.PersistentRelink( wb_file_xml, stream )
        try:
            tst.Archive( ts_archive_data )
        except AttributeError:
            tst.Text( ts_archive_data )

        tst.Owner(owner)
        if type(protection) == type(0): tst.Protection(protection)
        tst.AutoUser(False)
        tst.User(owner)
        tst.Commit()

        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return tst

    def Name(self):
        return 'Workspace'

    def ClassName(self):
        return 'FWorkspace'

    def SelectSingle(self, name):
        wb = None
        try:
            if name.isdigit():
                wb = acm.FWorkspace[name]
            else:
                if name.find(self.SHARED_CHAR) > 0:
                    name, owner = name.split(self.SHARED_CHAR)
                    ownernum = acm.FUser[owner].Oid()
                else:
                    ownernum = 0

                wb = (list(acm.FWorkspace.Select('''name="%s" and user=%d''' %(name, ownernum)))+[None])[0]

        except Exception, msg:
            logger.DLOG( "Select %s failed: %s/%s" %(name, str(Exception), msg))

        return wb


Transporter.add_handler(FExtensionModuleTransporter())
Transporter.add_handler(FTradeFilterTransporter())
Transporter.add_handler(FStoredASQLQueryTransporter())
Transporter.add_handler(FASQLQueryTransporter())
Transporter.add_handler(FAelTaskTransporter())
Transporter.add_handler(FAelTransporter())
Transporter.add_handler(FWorkbookTransporter())
Transporter.add_handler(FTradingSheetTemplateTransporter())
Transporter.add_handler(FWorkspaceTransporter())

class FRemoteSheetDefinitionTransporter(XMLTransporter):
    DEFAULT_EXTENSION=".rsdef"
    def ExportSingle(self, params, name):
        ws = self.SelectSingle(name)

        assert ws, self.Name()+':'+name+' not found in the system'
            
        wsRoot = ET.Element("FRemoteSheetDefinition")
        
        self.AddAcmTags(wsRoot, ws, RSCollection=ws.SubType(), Weight=str(ws.Weight()), UpdateFrequency=str(ws.UpdateFrequency()))

        ts_archive_data = ET.SubElement(wsRoot, "data")
        if transporterSetup.get('compressStream', 'True')=='True' and False:
            ts_archive_data.text = base64.b64encode(zlib.compress(ws.FromArchiveAsString()))
        else:
            ts_archive_data.text = ws.FromArchiveAsString()

        self.AddPersistentLinks(wsRoot, ws.FromArchiveAsString())
        
        assert ts_archive_data.text, "%s Could not export RS definition %s" %(self.Name(), ws.Name())

        xmlSerializer = XmlSerializer()

        #Retrieve the Trading Sheet
        ts = ws.TradingSheet()

        tsRoot = ET.SubElement(wsRoot, "FTradingSheet")
 
        ET.SubElement(tsRoot, "type").text = str(ts.Class().Name())
        
        ts_archive_data = ET.SubElement(tsRoot, "data")
        xmlText = xmlSerializer.ExportStream(ts, transporterSetup.get('compressStream', 'True')=='True')

        ts_archive_data.text = xmlText

        assert ts_archive_data.text, "%s Could not export RS definition %s" %(self.Name(), ws.Name())
        return ET.tostring(wsRoot, 'ISO-8859-1')

    def ImportSingle(self, params, name, inputText):
        wb_file_xml = ET.fromstring(inputText)
        
        if type(self.use_def_prot) == type(0):
            protection = self.use_def_prot
        elif self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(wb_file_xml, "protection")

        if self.owner:
            owner = self.owner.Name()
        else:
            owner = self.get_tag_text(wb_file_xml, "owner")

        if (not owner) or (not acm.FUser[owner]):
            owner = acm.FACMServer().User().Name()

        real_name = self.get_tag_text(wb_file_xml, "object_name")
        if not real_name:
            real_name = name

        ws = self.SelectSingle(real_name)

        self.checkAllowed(params.get("allow", "Insert & Update"), ws == None) # Exception if not allowed
        if not ws:
            self.added = True
            ws = acm.FRemoteSheetDefinition()
            ws.Name(real_name)
        else:
            self.added = False
            #if str(ws.Name()) != real_name:
            #    raise UpdateException( 'Update conflict "%s" != "%s"'%(str(tst.Name()),real_name) )

        ws.SubType( self.get_tag_text(wb_file_xml, "RSCollection") )
        #ws.Weight( self.get_tag_text(wb_file_xml, "Weight") )
        #ws.UpdateFrequency( self.get_tag_text(wb_file_xml, "UpdateFrequency") )

        stream = self.stringdecode( wb_file_xml.find("data").text )
        try:
            stream = zlib.decompress(base64.b64decode(stream))
        except:
            pass
        
        xmlSerializer = XmlSerializer()

        #Add new sheet
        ts_elem = wb_file_xml.find("FTradingSheet")
    
        ts_type = ts_elem.find("type").text
        ts_archive_data = self.stringdecode( ts_elem.find("data").text )
        ts = xmlSerializer.ImportStream(ts_archive_data)
        
        ts.Name(ts_type+str(ts.Oid())) # Temporary name
        ts.Commit()        
        ts.Name(ts_type+str(ts.Oid())) # Final Name
        ts.Commit()

        ts_archive_data = self.PersistentRelink( wb_file_xml, stream )

        etObj = ET.fromstring(ts_archive_data)

        for obj in etObj.findall('.//FPersistent'):
            cls = obj.find('Class/FDomain/DomainName/string').text
            if cls.endswith('Sheet'):
                ptrint = obj.find('StorageId/ptrint')
                if ptrint != None:
                    ptrint.text = str(ts.Oid())
                    break

        try:
            ws.Archive( ET.tostring(etObj, 'ISO-8859-1') )
        except AttributeError:
            ws.Text( ET.tostring(etObj, 'ISO-8859-1') )

        ws.Owner(owner)
        if type(protection) == type(0): ws.Protection(protection)
        ws.AutoUser(False)

        ws.Commit()

        if self.added:
            logger.LOG("Added %s" %real_name)
        else:
            logger.LOG("Updated %s" %real_name)
        
        return ws

    def Name(self):
        return 'RS Definition'
    def ClassName(self):
        return 'FRemoteSheetDefinition'


if ACM_INTERNAL_VERSION > 4.07 and ACM_INTERNAL_VERSION < 4.22:
    Transporter.add_handler(FRemoteSheetDefinitionTransporter())

class FASQLReportTransporter(FASQLQueryTransporter):
    DEFAULT_EXTENSION=".report"
    def ExportSingle(self, params, name):
        date = getDate(params['fromdate'])
        asql = ael.TextObject.read('type = "SQL Report" and name = "%s"' % name)
        assert asql, self.Name()+':'+name+' not found in the system'
        if date and str(date).strip() != '':
            if ael.date_from_time(asql.updat_time) < date:
                logger.WLOG('%s %s is too old' %(self.Name(), name))
                Transporter.export_expiry_count+= 1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
        return asql.get_text()

    def ImportSingle(self, params, name, text):
        asql = ael.TextObject.read('type = "SQL Report" and name = "%s"' % name)

        if asql:
            objectSame = asql.get_text() == text
        else:
            objectSame = None

        self.checkAllowed(params.get("allow", "Insert & Update"), asql == None, objectSame) # Exception if not allowed
    
        if asql:
            self.added = False
            asql = asql.clone()
            asql.set_text(text)
            if self.owner:
                asql.owner_usrnbr = self.owner.Name()

        else:
            self.added = True
            asql = ael.TextObject.new()
            asql.type = "SQL Report"
            asql.name = name
            asql.set_text(text)
            if self.owner:
                asql.owner_usrnbr = self.owner.Name()

        if type(self.use_def_prot) == type(''):
            asql.protection = self.use_def_prot

        asql.commit()
        if self.added:
            logger.LOG("Added %s" %name)
        else:
            logger.LOG("Updated %s" %name)
        
        return asql

    def Delete(self, params):
        error = 0
        delete_items = params[self.Name()]
        for name in delete_items:
            logger.LOG("Delete %s %s"%(self.Name(), name))
            object = ael.TextObject.read('type = "SQL Report" and name = "%s"' % name)
            
            if not object:
                logger.WLOG("%s %s does not exist" % (self.Name(), name))
                error += 1
            else:
                try:
                    object.delete()
                except Exception, msg:
                    logger.ELOG("%s %s could not be deleted: %s" % (self.Name(), name, msg))
                    error += 1
                else:
                    logger.DLOG("Success")
        return error
        
    def SelectObjects(self,query=''):
        if query:
            query = ' and %s'%query
        return ael.TextObject.select('type="SQL Report"%s'%query)

    def Names(self, objects):
        return [ object.name for object in self.SelectObjects()]

    def Name(self):
        return 'ASQL Report'

    def ClassName(self):
        return 'AsqlReport'

    def Select(self, owner=None):
        return [asql.name for asql in ael.TextObject.select('type="SQL Report"') if (not owner or (owner and asql.owner_usrnbr and asql.owner_usrnbr.userid == owner))]
        
    def SelectSingle(self, name):
        return ael.TextObject.read('type = "SQL Report" and name = "%s"' % name)


Transporter.add_handler(FASQLReportTransporter())
