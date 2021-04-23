"""-------------------------------------------------------------------------------------------------------
MODULE
    Transporter

    (c) Copyright 2009-2018 by FIS Front Arena. All rights reserved.

VERSION
    1.0.1(0.1.55)
DESCRIPTION
    The base class & common routines

MAJOR REVISIONS

    2009-03-13  RL  Initial implementation
-------------------------------------------------------------------------------------------------------"""

import os
import string
import itertools
import acm
import FLogger
import codecs

logger = FLogger.FLogger(name = 'Transporter')

IN_PRIME = 1 if acm.GetClass("FTmServer") != None else 0
ACM_SHORT_VERSION=float(".".join(acm.ShortVersion().strip(string.ascii_letters).split(".")[0:2]))
ACM_INTERNAL_VERSION=float(".".join(num.zfill(2) for num in acm.InternalVersion().strip(string.ascii_letters).split(".")[0:2]))

def checkProfileComponent(profileName, ctype='Operation'):

    """CheckProfileComponent = transporterSetup.get('checkProfileComponent','False')

    if CheckProfileComponent == 'False' or (CheckProfileComponent == 'Prime' and not IN_PRIME):
        return 1
    """

    prof = acm.FComponent.Select01("""name='%s' and type='%s'"""%(profileName, ctype),'')
    if prof:
        for link in itertools.chain( acm.User().Links(), acm.FGroupProfileLink.Select('userGroup=%d'%acm.UserGroup().Oid()) ):
            for profComp in link.UserProfile().ProfileComponents():
                if profComp.Component() is prof:
                    return 1  # Found match!

        raise Exception("%s not in profile"%profileName)

    return 0


def parseEnv(inputstring):
    """ Expand Environment variables on textstrings, allowing also upper case characters"""
    class TemplateEnv(string.Template):
        idpattern="[_A-Za-z][\._A-Za-z0-9]*"
        
    return TemplateEnv(inputstring).safe_substitute(os.environ)


def getParameterSetup(extensionName='TransporterSetup'):
    transporterSetup = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', extensionName)
    if transporterSetup:
        transporterSetup = transporterSetup.Value()
        return dict(list(zip( (str(key) for key in transporterSetup.Keys()), (str(val) for val in transporterSetup.Values()) )))
    return {}


def detect_unicode(file_path,default = 'cp1252'):
    with open(file_path, 'rb') as f:
        raw = f.read(4)    #will read less if the file is smaller
    for enc,boms, size in \
            ('utf-8-sig',(codecs.BOM_UTF8,),3),\
            ('utf-16',(codecs.BOM_UTF16_LE,codecs.BOM_UTF16_BE), 2),\
            ('utf-32',(codecs.BOM_UTF32_LE,codecs.BOM_UTF32_BE), 4):
        if any(raw.startswith(bom) for bom in boms): return enc, size
    return default, 0


class OpenUnicode(object):
    def __init__(self, filename, *args, **kwds):
        self.encoding, self.bom_len = detect_unicode(filename)
        self.file_obj = open(filename, *args, **kwds) 
        
        if self.bom_len > 0:
            self.file_obj.read(self.bom_len)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, *args):
        self.file_obj.close()


transporterSetup = getParameterSetup()
checkProfileComponent("Start "+__name__)


class Transporter(object):
    all_handlers = {}
    CODEC = 'cp1252'
    # jdba 20090706: provide summary at end of # of objects succeeeded or failed (or expired)
    export_success_count = 0
    export_fail_count = 0
    export_expiry_count = 0
    export_failures = {}
    export_expiries = []

    import_add_count = 0
    import_update_count = 0
    import_fail_count = 0
    import_failures = {}
    
    def __init__(self, owner = None, use_def_prot = True):
        self.select = self.Select()
        self.use_def_prot = use_def_prot
        self.owner = owner
    def add_handler(handler):
        """
        if handler.Name() not in [a[0] for a in Transporter.all_handlers]:
            tmptuple = (handler.Name(),handler)
            Transporter.all_handlers.append(tmptuple)
        """
        Transporter.all_handlers[handler.Name()] = handler
    add_handler = staticmethod(add_handler)
#-------
    def get_handler(handlername):
        for name,handler in Transporter.all_handlers.iteritems():
            if name == handlername:
                return handler    
        return None
    get_handler = staticmethod(get_handler)
#-------
    def all_handler_names():
        return Transporter.all_handlers.keys()
    all_handler_names = staticmethod(all_handler_names)
#-------
    def ExtraParameter(self):
        return None
    def ExtraImportParameter(self):
        return None
    def ExtraExportParameter(self):
        return None

    def Export(self,name):
        raise NotImplemented()
    def Import(self,text,name):
        raise NotImplemented()
    #def Delete should only be defined if it exists at all
    def Name(self):
        raise NotImplemented()
    def ClassName(self):
        return self.Name()
    def Select(self):
        raise NotImplemented()
    def Extension(self):
        raise NotImplemented()

    def SetOwner(self, owner):
        self.owner = owner

    def SetDefProt(self, use_def_prot):
        self.use_def_prot = use_def_prot

    def stringdecode(self, soru):
        if type(soru) == type(u""):
            return soru.encode(Transporter.CODEC)
        else:
            return soru

    def get_tag_text(self, xml_tree, tag_name):
        tag_text = None
        tag = xml_tree.find(tag_name)
        if tag <> None: tag_text = tag.text
        return tag_text
        
    def uniqueNames(self, NameOwner):
        count = {}
        for (name, owner) in NameOwner:
            count[name] = count.get(name,0) +1
        unique = []
        for (name, owner) in NameOwner:
            if count.get(name,0) > 1 and owner:
                unique.append("%s: %s"%(str(name),str(owner.Name())))
            else:
                unique.append(name)
        return unique

    def fileToString(self,path,filename):
        file_path = os.path.join(path, filename)
        if not path.strip():
            raise IOError("Path can not be empty")

        fh = open(file_path,'r')
        input = fh.read()
        fh.close()        
        
        return input.replace("\r\n","\n")
