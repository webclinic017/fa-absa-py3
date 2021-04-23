"""-------------------------------------------------------------------------------------------------------
MODULE
    Transporters - An Export/Import Module for ACM Objects

DESCRIPTION

MAJOR REVISIONS

    2008-04-21  RL           Initial implementation
    2013-03-01  Jan Sinkora  TF+ASQL import bugfix
-------------------------------------------------------------------------------------------------------"""

import acm, ael
import os
from Transporter import Transporter
from XmlSerializer import XmlSerializer

import time

import xml.etree.cElementTree as ET

class XMLTransporter(Transporter):
    added=None
    def StringToFile(self, params, output, name ):
        path=params['basepath'].AsString()
        filename=name+self.Extension()
        
        if not path.strip():
            raise IOError("Path can not be empty")
            
        notallowed='/\\":*?><|'
        changed=False
        for na in notallowed:
            if na in filename:
                filename=filename.replace(na, '_')
                changed=True
        if changed:
            print "Warning: changed name to %s"%filename,
            
        if os.path.exists(path):
            file_path = os.path.abspath(os.path.join(path, filename))
            fh = open(file_path, 'wb')
            fh.write(output.replace("\r\n", "\n"))
            fh.close()
        else:
            raise IOError("Path <%s> does not exist"%path)

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
        count={}
        for (name, owner) in NameOwner:
            count[name]=count.get(name, 0) +1
        unique=[]
        for (name, owner) in NameOwner:
            if count.get(name, 0) > 1 and owner:
                unique.append("%s:%s"%(str(name), str(owner.Name())))
            else:
                unique.append(name)
        return unique

    def Export(self, params):
        export_items=params[self.Name()]
        for name in export_items:
            print 'Exporting %s %s' %(self.ClassName(), name),
            try:
                output=self.ExportSingle(params, name)
                if output:
                    self.StringToFile(params, output, name)
                    Transporter.export_success_count+=1
            except Exception, msg:
                Transporter.export_fail_count+=1
                print "Failed: %s %s"%(Exception, msg)
                Transporter.export_failures[self.Name()+':\t'+name]=msg
            else:
                print "done"

    def Import(self, params):
        import_items=params[self.Name()]
        path=params['basepath'].AsString()        

        for name in import_items:
            print 'Importing %s %s' %(self.ClassName(), name),
            try:
                text=self.fileToString(path, name)
                name=os.path.splitext(name)[0]
                # for file names with name.xml.qf and name.amba.qf
                if name.find(".xml.") > 0: name = name.split(".xml.")[0]
                if name.find(".amba.") > 0: name = name.split(".amba.")[0]
                self.ImportSingle(params, name, text)
            except Exception, msg:
                Transporter.import_fail_count+=1
                Transporter.import_failures[self.Name()+':\t'+name]=msg
                print "Failed: %s %s"%(Exception, msg)
            else:
                if self.added: Transporter.import_add_count+=1
                else: Transporter.import_update_count+=1
                print "done"

    def vars(self):
        return [[self.Name(), self.Name()+' name(s)', 'string', self.select, None, 0, 1, 'Select %ss'%self.ClassName(), None, True]]

class FAgentParameterTransporter(XMLTransporter):
    """This is the Agent Parameter from FA version before 4.3. It is not compatible with FStoredAgentSetupTransporter"""
    def ExportSingle(self, params, name):
        agent = ([ag for ag in acm.FAgentParameter.Select('cid="Agent Parameter" and name="%s"' % agent_name)] + [None])[0]
        assert agent, self.Name()+':'+name+' not found in the system'
        
        root = Element("FAgentParameter")   
        
        acm_version = SubElement(root, "acm_version")
        acm_version.text = acm.Version()
        
        export_time = SubElement(root, "export_time")
        export_time.text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                
        data_owner = SubElement(root, "owner")
        data_owner.text = agent.Owner().Name()                    
        
        protection = SubElement(root, "protection")
        protection.text = str(agent.Protection())
        
        archive_data = SubElement(root, "data")
        archive_data.text = agent.Archive()
        return ET.tostring(root, 'ISO-8859-1')

    def ImportSingle(self, params, name, text):
        ag_file_xml=ET.fromstring(text)

        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(ag_file_xml, "protection")

        owner=self.owner or self.get_tag_text(ag_file_xml, "owner")
            
        ag_archive_data = get_tag_text(ag_file_xml, "data")

        real_name = self.get_tag_text(ag_file_xml, "object_name")

        agent = ([ag for ag in acm.FAgentParameter.Select('cid="Agent Parameter" and name=%s' % real_name)] + [None])[0]

        if agent:
            print "Updated ", real_name,
        else:  
            agent = acm.FAgentParameter()
            agent.Name(real_name)
            print "Added ", real_name,
   
        agent.Owner(owner)
        if protection: agent.Protection(protection)
        agent.Archive(ag_archive_data)            
        agent.Commit()            
        agent.Archive(ag_archive_data)        
        agent.Commit()          

    def Delete(self, params):
        delete_items=params[self.Name()]

        for name in delete_items:
            print "Delete %s"%(name),
            agent = ([ag for ag in acm.FAgentParameter.Select('cid="Agent Parameter" and name="%s"' % name)] + [None])[0]
            if agent:
                agent.Delete()
                print "done"
            else:
                print "%s %s does not exist" % (self.Name(), name)
    def Name(self):
        return 'Agent'
    def ClassName(self):
        return 'FAgentParameter'
    def Select(self):
        return list(acm.FAgentParameter.Instances())
    def Extension(self):
        return '.agent'

class FStoredAgentSetupTransporter(XMLTransporter):
    """This is the Agent Parameter from FA version 4.3. It is not compatible with earlier FAgentParameterTransporter"""
    def ExportSingle(self, params, name):
        agent = ([ag for ag in acm.FStoredAgentSetup.Select('name="%s"' % name)] + [None])[0]    
            
        assert agent, self.Name()+':'+name+' not found in the system'

        #Create the root element
        root = ET.Element("FStoredAgentSetup")
        
        acm_version = ET.SubElement(root, "acm_version")
        acm_version.text = acm.Version()
        
        export_time = ET.SubElement(root, "export_time")
        export_time.text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        object_name = ET.SubElement(root, "object_name")
        object_name.text = agent.Name()

        data_owner = ET.SubElement(root, "owner")
        data_owner.text = agent.Owner().Name()                    
        
        protection = ET.SubElement(root, "protection")
        protection.text = str(agent.Protection())
        
        context = ET.SubElement(root, "Context")
        context.text = str(agent.Context())

        type = ET.SubElement(root, "Type")
        type.text = str(agent.Type())

        type = ET.SubElement(root, "Class")
        if agent.Setup():        
            type.text = str(agent.Setup().AgentClassName())

        setup = ET.SubElement(root, "Setup")
        if agent.Setup():
            par=agent.Setup().ParameterNamesAndValues()
            for key, val in zip(par.Keys(), par.Values()):
                ET.SubElement(setup, str(key)).text=str(val)

        return ET.tostring(root, 'ISO-8859-1')
    
    def ImportSingle(self, params, name, text):
        ag_file_xml=ET.fromstring(text)

        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(ag_file_xml, "protection")
        
        owner=self.owner or self.get_tag_text(ag_file_xml, "owner")
        real_name = self.get_tag_text(ag_file_xml, "object_name")
            
        agent = ([ag for ag in acm.FStoredAgentSetup.Select('name=%s' % real_name)] + [None])[0]

        if agent:
            print "Updated ", real_name,
            self.added=False
        else:  
            agent = acm.FStoredAgentSetup()
            agent.Name(real_name)
            print "Added ", real_name,
            self.added=True

        agent.Owner(owner)
        if protection: agent.Protection(protection)
        agent.Context(self.get_tag_text(ag_file_xml, "Context"))

        agent.Type(self.get_tag_text(ag_file_xml, "Type"))

        #klass=self.get_tag_text(ag_file_xml, "Class")
        #agent.Setup().AgentClassName(klass)

        setup=ag_file_xml.find("Setup")        
        for tg in setup.getchildren():
            agent.SetParameterValueAt(tg.tag, tg.text)
        agent.Commit()          

    def Delete(self, params):
        delete_items=params[self.Name()]

        for name in delete_items:
            print "Delete %s"%(name),
            agent = ([ag for ag in acm.FStoredAgentSetup.Select('name="%s"' % name)] + [None])[0]
            if agent:
                agent.Delete()
                print "done"
            else:
                print "%s %s does not exist" % (self.Name(), name)
    def Name(self):
        return 'Agent'
    def ClassName(self):
        return 'FStoredAgentSetup'
    def Select(self):
        return list(acm.FStoredAgentSetup.Instances())
    def Extension(self):
        return '.agent'

class FTradeFilterTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
        tf=ael.TradeFilter[name]    

        if not tf:
            raise Exception("Trade Filter %s does not exist" % name)

        if date and str(date).strip() != '':
            if ael.date_from_time(tf.updat_time) < date:
                print '%s %s is too old' %(self.Name(), name)
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None

        tf_root = ET.Element("FTradeFilter")
        
        tf_acm_version=ET.SubElement(tf_root, "acm_version")
        tf_acm_version.text=acm.Version()

        tf_version=ET.SubElement(tf_root, "version")
        tf_version.text="%s $"%(str(tf.version_id))+"Id"+"$"
        
        tf_export_time=ET.SubElement(tf_root, "export_time")
        tf_export_time.text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        object_name = ET.SubElement(tf_root, "object_name")
        object_name.text = tf.fltid
                                
        tf_data_owner = ET.SubElement(tf_root, "owner")
        tf_data_owner.text=tf.owner_usrnbr.userid                    
        
        tf_protection=ET.SubElement(tf_root, "protection")
        tf_protection.text=tf.protection
        
        if tf.query_seqnbr:
            tf_data_queryname =ET.SubElement(tf_root, "asql_query")
            tf_data_queryname.text=tf.query_seqnbr.name            
            print "Warning: Tradefilter '%s' is using ASQL query '%s'"%  (tf.fltid, tf.query_seqnbr.name),
        else:
            tf_data_query = ET.SubElement(tf_root, "query")            
            tf_data_query.text=str(tf.get_query())                        

        return ET.tostring(tf_root, 'ISO-8859-1')

    def ImportSingle(self, params, name, text):
        tf_file_xml=ET.fromstring(text)
        
        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(tf_file_xml, "protection")
        
        owner=self.owner or self.get_tag_text(tf_file_xml, "owner")
        owner_usrnbr = ael.User[owner].usrnbr
        
        tf_asql_query = tf_file_xml.find("asql_query")
        if tf_asql_query <> None: tf_asql_query = tf_asql_query.text
        else: tf_asql_query = None
        
        tf_query = tf_file_xml.find("query")
        if tf_query <> None: tf_query = tf_query.text
        else: tf_query = None
        
        real_name=self.get_tag_text(tf_file_xml, "object_name")
        tf=ael.TradeFilter[real_name]    
        mode = 'add'
        if tf:
            print "Updated ", real_name,
            self.added=False
            tf = tf.clone()
            mode = 'update'
        else:
            print "Added ", real_name,
            tf = ael.TradeFilter.new()
            self.added=True

        tf.fltid = real_name
        tf.owner_usrnbr = owner_usrnbr
        if protection:
            tf.protection = protection                
        if tf_asql_query:
            asql = ael.TextObject.read('type="SQL Query" and name="%s"' % tf_asql_query)
            if asql:                    
                tf.query_seqnbr = asql
                tf.set_query([])                
            else:
                raise Exception("Failed to %s Trade Filter %s because of missing %s" % (mode, tf.fltid, tf_asql_query))
        elif tf_query:
            tf.set_query(eval(tf_query))
        else: 
            raise Exception("Trade Filter File %s has wrong format" % name)
        tf.commit()

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            tf=ael.TradeFilter[name]    

            if not tf:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                tf.delete()
                print " done"

    def Name(self):
        return 'Trade Filter'
    def ClassName(self):
        return 'FTradeFilter'
    def Select(self):
        return [tf.fltid for tf in ael.TradeFilter.select()]
    def Extension(self):
        return '.tf'

class FASQLQueryTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
        asql = ael.TextObject.read('type="SQL Query" and name="%s"' % name)
        assert asql, self.Name()+':'+name+' not found in the system'
        if date and str(date).strip() != '':
            if ael.date_from_time(asql.updat_time) < date:
                print '%s %s is too old' %(self.Name(), name) 
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
        return asql.get_text()

    def ImportSingle(self, params, name, text):
        asql = ael.TextObject.read('type="SQL Query" and name="%s"' % name)
    
        if asql:
            print "Updated ",
            self.added=False
            asql=asql.clone()
            asql.set_text(text)
            asql.commit()
        else:    
            print "Added ",
            self.added=True
            asql = ael.TextObject.new()
            asql.type = "SQL Query"
            asql.name = name
            asql.set_text(text)
            asql.commit()

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            asql = ael.TextObject.read('type="SQL Query" and name="%s"' % name)

            if not asql:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                asql.delete()
                print "done"

    def Name(self):
        return 'ASQL Query'
    def ClassName(self):
        return 'FASQLQuery'
    def Select(self):
        return [asql.name for asql in ael.TextObject.select('type="SQL Query"')]
    def Extension(self):
        return '.asql'

class FStoredASQLQueryTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
        if name.find(":") > 0:
            name, owner=name.split(":")
            ownernum=acm.FUser[owner].Oid()
            qf = (list(acm.FStoredASQLQuery.Select("name='%s' and user=%d" %(name, ownernum)))+[None])[0]
        else:
            qf = (list(acm.FStoredASQLQuery.Select('name=%s' % name))+[None])[0]

        assert qf, self.Name()+':'+name+' not found in the system'

        if date and str(date).strip() != '':
            if ael.date_from_time(qf.UpdateTime()) < date:
                print '%s %s is too old' %(self.Name(), name)
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
            
        qf_root = ET.Element("FStoredASQLQuery")
   
        qf_acm_version=ET.SubElement(qf_root, "acm_version")
        qf_acm_version.text=acm.Version()

        qf_version=ET.SubElement(qf_root, "version")
        qf_version.text="%s $"%(str(qf.VersionId()))+"Id"+"$"

        qf_export_time=ET.SubElement(qf_root, "export_time")
        qf_export_time.text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        object_name = ET.SubElement(qf_root, "object_name")
        object_name.text = qf.Name()

        qf_data_owner = ET.SubElement(qf_root, "owner")
        qf_data_owner.text=qf.Owner().Name()                    
        
        qf_protection=ET.SubElement(qf_root, "protection")
        qf_protection.text=str(qf.Protection())
        
        qf_subtype = ET.SubElement(qf_root, "subtype")
        qf_subtype.text = qf.SubType()

        qf_archive_data = ET.SubElement(qf_root, "data")
        qf_archive_data.text = qf.Archive()
        return ET.tostring(qf_root, 'ISO-8859-1')

    def ImportSingle(self, params, name, input):
        qf_file_xml=ET.fromstring(input)

        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(qf_file_xml, "protection")
        
        owner=self.owner or acm.FUser[self.get_tag_text(qf_file_xml, "owner")]

        qf_subtype = qf_file_xml.find("subtype")
        if qf_subtype <> None: qf_subtype = qf_subtype.text
            
        qf_archive_data = qf_file_xml.find("data")
        if qf_archive_data <> None: qf_archive_data = qf_archive_data.text
                   
        real_name=self.get_tag_text(qf_file_xml, "object_name")

        if qf_archive_data:
            qf = acm.FStoredASQLQuery[real_name]
        
            if qf:      
                qf.Owner(owner)
                if protection: qf.Protection(protection)
                qf.Owner(owner)
                qf.SubType(qf_subtype)        
                qf.Archive(qf_archive_data)        
                qf.Commit()                            
                print "Updated ", real_name,
                self.added=False
            else:
                qf = acm.FStoredASQLQuery()
                qf.Name(real_name)
                qf.Owner(owner)
                qf.SubType(qf_subtype)        
                if protection: qf.Protection(protection)
                qf.Archive(qf_archive_data)
                qf.AutoUser(False)
                qf.Commit()
                print "Added ", real_name,
                self.added=True
        else:
            raise Exception("Query Folder File %s has wrong format" % qf_file)

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            qf = (list(acm.FStoredASQLQuery.Select('name=%s' % name))+[None])[0]
            if not qf:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                qf.Delete()
                print " done"

    def Name(self):
        return 'Query Folder'
    def ClassName(self):
        return 'FStoredASQLQuery'
    def Select(self):
        return self.uniqueNames( [(a.Name(), a.User()) for a in acm.FStoredASQLQuery.Instances()])
    def Extension(self):
        return '.xml.qf'

class FAelTaskTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
        task = acm.FAelTask[name]

        assert task, self.Name()+':'+name+' not found in the system'

        if date and str(date).strip() != '':
            if ael.date_from_time(task.UpdateTime()) < date:
                print '%s %s is too old' %(self.Name(), name) 
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
   
        task_root = ET.Element("FAelTask")
       
        task_acm_version=ET.SubElement(task_root, "acm_version")
        task_acm_version.text=acm.Version()

        task_version=ET.SubElement(task_root, "version")
        task_version.text="%s $"%(str(task.VersionId()))+"Id"+"$"

        task_export_time=ET.SubElement(task_root, "export_time")
        task_export_time.text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        object_name = ET.SubElement(task_root, "object_name")
        object_name.text = task.Name()
                                
        task_data_owner = ET.SubElement(task_root, "owner")
        task_data_owner.text=task.Owner().Name()                    
        
        task_protection=ET.SubElement(task_root, "protection")
        task_protection.text=str(task.Protection())
                
        task_module = ET.SubElement(task_root, "module")
        task_module.text = task.ModuleName() 

        if task.HistoryLength():
            task_module = ET.SubElement(task_root, "historylength")
            task_module.text = task.HistoryLength() 

        if task.Description():
            task_module = ET.SubElement(task_root, "description")
            task_module.text = task.Description() 

        if task.LogFileName():
            task_module = ET.SubElement(task_root, "logfilename")
            task_module.text = task.LogFileName() 
       
        task_parameter = ET.SubElement(task_root, "parameter")
        task_parameter.text = task.ParametersText()

        return ET.tostring(task_root)

    def ImportSingle(self, params, name, input):
        task_file_xml=ET.fromstring(input)

        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(task_file_xml, "protection")
        
        owner=self.owner or acm.FUser[self.get_tag_text(task_file_xml, "owner")]

        real_name = self.get_tag_text(task_file_xml, "object_name")
    
        task_parameter = self.stringdecode(task_file_xml.find("parameter").text)
        task_module = self.stringdecode(task_file_xml.find("module").text)
        historylength=params.get('taskhistorylength', None) or self.get_tag_text(task_file_xml, "historylength")
        description=self.get_tag_text(task_file_xml, "description")
        logfilename=self.get_tag_text(task_file_xml, "logfilename")
        
        task = acm.FAelTask[real_name]
        
        if task:
            print "Updated ", real_name,
            self.added=False
            taskClone=task.Clone()
            taskClone.ModuleName(task_module)
            taskClone.ParametersText(task_parameter)
            taskClone.Owner(owner)
            if protection: taskClone.Protection(protection)
            if historylength: taskClone.HistoryLength(historylength)
            if description: taskClone.Description(description)
            if logfilename:
                taskClone.LogFileName(logfilename)
            task.Apply(taskClone)
            task.Commit()
        else:
            print "Added ", real_name,
            self.added=True
            task = acm.FAelTask()
            task.ModuleName(task_module)
            task.Name(real_name)
            task.ParametersText(task_parameter)
            task.Owner(owner)
            if protection: task.Protection(protection)
            if historylength: task.HistoryLength(historylength)
            if description: task.Description(description)
            if logfilename:
                task.LogFileName(logfilename)
            task.Commit()    

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            task = acm.FAelTask[name]

            if not task:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                task.Delete()
                print " done"

    def Name(self):
        return 'Task'
    def ClassName(self):
        return 'FAelTask'
    def Select(self):
        return list(acm.FAelTask.Instances())
    def Extension(self):
        return '.xml.task'

class FAelTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
        ael_module = acm.FAel[name]
        if ael_module:
            if date and str(date).strip() != '':
                if ael.date_from_time(ael_module.UpdateTime()) < date:
                    print '%s %s is too old' %(self.Name(), name) 
                    Transporter.export_expiry_count+=1
                    Transporter.export_expiries.append(self.Name()+':\t'+name)
                    return None
            return ael_module.Text()
        else:
            raise Exception('%s %s not found' %(self.Name(), name))
            
    def ImportSingle(self, params, name, input):
        ael_module = acm.FAel[name]
    
        if ael_module:
            print "Updated ",
            self.added=False
            ael_module.Text(input)
            ael_module.Commit()
        else:
            print "Added ",
            self.added=True
            ael_module = acm.FAel()    
            ael_module.Name(name)
            ael_module.Text(input)
            ael_module.Commit()

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            ael_module = acm.FAel[name]

            if not ael_module:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                ael_module.Delete()
                print " done"

    def Name(self):
        return 'Python'
    def ClassName(self):
        return 'FAel'
    def Select(self):
        return list(acm.FAel.Select(''))
    def Extension(self):
        return '.py'

class FExtensionModuleTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
        em = acm.FExtensionModule[name]
        assert em, self.Name()+':'+name+' not found in the system'
        if date and str(date).strip() != '':
            if ael.date_from_time(em.UpdateTime()) < date:
                print '%s %s is too old' %(self.Name(), name)
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
        return em.AsString().replace('\ndescription ""', '\ndescription "$'+"Id"+'$"')

    def ImportSingle(self, params, name, input):
        if float(".".join(acm.ShortVersion().split(".")[0:2])) < 2009.2:
            input=input.replace('\n...', '\n\xa4')
        data = acm.ImportExtensionModule(input)
        filename=data.Name()
        if filename != name:
            print "(as '%s')"%(filename),
        em = acm.FExtensionModule[filename]

        if em:
            print "Updated ",
            self.added=False
            em.Apply(data)
            try:
                em.Commit()
            except RuntimeError:
                em.Undo()
                em=acm.FExtensionModule[filename]

                acm.BeginTransaction()
                try:
                    em.Delete()
    
                    em = acm.FExtensionModule()
                    em.Apply(data)
                    em.Commit()
                    acm.CommitTransaction()
                except:
                    acm.AbortTransaction()
                    raise
        else:
            print "Added ",
            self.added=True
            em = acm.FExtensionModule()
            em.Apply(data)
            em.Commit()

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            em = acm.FExtensionModule[name]

            if not em:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                em.Delete()
                print " done"

    def Name(self):
        return 'Extension Module'
    def ClassName(self):
        return 'FExtensionModule'
    def Select(self):
        return [em for em in acm.FExtensionModule.Select('') if not ( str(em.Name()) == str(em.Owner().Name()) )]
    def Extension(self):
        return '.ext'

class FWorkbookTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']
#        if name.find(":") > 0:
#            name,owner=name.split(":")
#            ownernum=acm.FUser[owner].Oid()
#            wb = (list(acm.FWorkbook.Select("name=%s and user=%d" %(name,ownernum)))+[None])[0]
#        else:
        wb = acm.FWorkbook[name]
        if not wb:
            wb=acm.FWorkbook.Select01('name=%s' % name, '')
                
        if not wb:
            raise Exception('%s %s is not found' %(self.Name(), name))

        if date and str(date).strip() != '':
            if ael.date_from_time(wb.UpdateTime()) < date:
                print '%s %s is too old' %(self.Name(), name) 
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None

        wb_root = ET.Element("FWorkbook")
        
        wb_acm_version=ET.SubElement(wb_root, "acm_version")
        wb_acm_version.text=acm.Version()

        wb_version=ET.SubElement(wb_root, "version")
        wb_version.text="%s $"%(str(wb.VersionId()))+"Id"+"$"
        
        wb_export_time=ET.SubElement(wb_root, "export_time")
        wb_export_time.text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        object_name = ET.SubElement(wb_root, "object_name")
        object_name.text = wb.Name()

        wb_data_owner = ET.SubElement(wb_root, "owner")
        
        owner = wb.Owner()
        if owner: wb_data_owner.text=owner.Name()                    
        
        wb_protection=ET.SubElement(wb_root, "protection")
        wb_protection.text=str(wb.Protection())

        xml_ser = XmlSerializer()
                
        #Retrieve the Trading Sheets
        for ts in wb.Sheets():        
            ts_root = ET.SubElement(wb_root, "FTradingSheet")              
            ts_id = ET.SubElement(ts_root, "id")
            ts_id.text = str(ts.Oid())
            ts_type = ET.SubElement(ts_root, "type")      
            ts_type.text = str(ts.Class().Name())
            ts_archive_data = ET.SubElement(ts_root, "data")
            ts_archive_data.text = xml_ser.ExportStream(ts)

        return ET.tostring(wb_root, 'ISO-8859-1')
                
    def ImportSingle(self, params, name, input):
        wb_file_xml=ET.fromstring(input)
            
        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(wb_file_xml, "protection")
        
        owner=self.owner or acm.FUser[self.get_tag_text(wb_file_xml, "owner")]
        real_name=self.get_tag_text(wb_file_xml, "object_name")

        wb = (list(acm.FWorkbook.Select('name=%s and user="%s"' % (real_name, owner))) + [None])[0]
        if wb:
            print "Updated ",
            self.added=False
            #Remove existing sheets
            for ts in wb.Sheets():
                ts.Delete()
        else:
            print "Added ",
            self.added=True                            
            #Create the workbook    
            wb = acm.FWorkbook()
            wb.Name(real_name)

        xml_ser = XmlSerializer()
        sheets = acm.FArray()
        #Add new sheets
        for ts_elem in wb_file_xml.findall("FTradingSheet"):                    
            ts_id = ts_elem.find("id").text
            ts_type = ts_elem.find("type").text
            ts_archive_data = ts_elem.find("data").text
            ts = xml_ser.ImportStream(ts_archive_data)
            ts.Name(ts_type+str(ts.Oid())) # Temporary name
            ts.Commit()        
            ts.Name(ts_type+str(ts.Oid())) # Final Name
            ts.Commit()

            sheets.Add(ts)

        wb.Sheets(sheets)
        wb.Owner(owner)
        wb.User(owner)
        if protection: wb.Protection(protection)
        wb.AutoUser('false')
        wb.Commit()
                
    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            wb = acm.FWorkbook[name]
            if not wb:
                wb=acm.FWorkbook.Select01('name="%s"' % name, '')

            if not wb:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                wb.Delete()
                print " done"

    def Name(self):
        return 'Workbook'
    def ClassName(self):
        return 'FWorkbook'
    def Select(self):
        return self.uniqueNames( [(a.Name(), a.User()) for a in acm.FWorkbook.Select('')])
    def Extension(self):
        return '.wb'
        
class FTradingSheetTemplateTransporter(XMLTransporter):
    def ExportSingle(self, params, name):
        date=params['fromdate']

        if name.find(":") > 0:
            name, owner=name.split(":")
            ownernum=acm.FUser[owner].Oid()
            wb = (list(acm.FTradingSheetTemplate.Select("name='%s' and user=%d" %(name, ownernum)))+[None])[0]
        else:
            wb = acm.FTradingSheetTemplate[name]
            if not wb:
                wb = (list(acm.FTradingSheetTemplate.Select('name="%s"' % (name))) + [None])[0]

        assert wb, self.Name()+':'+name+' not found in the system'

        if date and str(date).strip() != '':
            if ael.date_from_time(wb.UpdateTime()) < date:
                print '%s %s is too old' %(self.Name(), name)
                Transporter.export_expiry_count+=1
                Transporter.export_expiries.append(self.Name()+':\t'+name)
                return None
            
        wb_root = ET.Element("FTradingSheetTemplate")
        
        wb_acm_version=ET.SubElement(wb_root, "acm_version")
        wb_acm_version.text=acm.Version()

        wb_version=ET.SubElement(wb_root, "version")
        wb_version.text="%s $"%(str(wb.VersionId()))+"Id"+"$"
        
        wb_export_time=ET.SubElement(wb_root, "export_time")
        wb_export_time.text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        object_name = ET.SubElement(wb_root, "object_name")
        object_name.text = wb.Name()

        wb_data_owner = ET.SubElement(wb_root, "owner")
        
        owner = wb.Owner()
        if owner: wb_data_owner.text=owner.Name()                    
        
        wb_protection=ET.SubElement(wb_root, "protection")
        wb_protection.text=str(wb.Protection())

        xml_ser = XmlSerializer()

        #Retrieve the Trading Sheets
        ts = wb.TradingSheet()
        ts_root = ET.SubElement(wb_root, "FTradingSheet")
        
        ts_id = ET.SubElement(ts_root, "id")
        ts_id.text = str(ts.Oid())
        
        ts_type = ET.SubElement(ts_root, "type")
        ts_type.text = str(ts.Class().Name())
        
        ts_archive_data = ET.SubElement(ts_root, "data")
        ts_archive_data.text = xml_ser.ExportStream(ts)
        
        return ET.tostring(wb_root, 'ISO-8859-1')

    def ImportSingle(self, params, name, input):
        wb_file_xml=ET.fromstring(input)
        
        if self.use_def_prot:
            protection = None
        else:             
            protection = self.get_tag_text(wb_file_xml, "protection")
        
        owner=self.owner or acm.FUser[self.get_tag_text(wb_file_xml, "owner")]

        real_name=self.get_tag_text(wb_file_xml, "object_name")

        tst = (list(acm.FTradingSheetTemplate.Select('name=%s and user="%s"' % (real_name, owner))) + [None])[0]
        if not tst:
            print "Added ", real_name,
            self.added=True
            tst = acm.FTradingSheetTemplate()
            tst.Name(real_name)
        else:
            print "Updated ", real_name,
            self.added=False

        xml_ser = XmlSerializer()

        #Add new sheets
        ts_elem = wb_file_xml.find("FTradingSheet")
    
        ts_id = ts_elem.find("id").text
        ts_type = ts_elem.find("type").text
        ts_archive_data = ts_elem.find("data").text
        ts = xml_ser.ImportStream(ts_archive_data)
        
        ts.Name(ts_type+str(ts.Oid())) # Temporary name
        ts.Commit()        
        ts.Name(ts_type+str(ts.Oid())) # Final Name
        ts.Commit()

        tst.SubType(ts_type)
        tst.ToArchive('TradingSheet', ts )

        tst.Owner(owner)
        tst.User(owner)
        if protection: tst.Protection(protection)
        tst.AutoUser('false')
        tst.Commit()

    def Delete(self, params):
        delete_items=params[self.Name()]
        for name in delete_items:
            print "Delete %s"%(name),
            tst = acm.FTradingSheetTemplate[name]
            if not tst:
                tst = (list(acm.FTradingSheetTemplate.Select('name="%s"' % (name))) + [None])[0]

            if not tst:
                print "%s %s does not exist" % (self.Name(), name)
            else:
                tst.Delete()
                print " done"

    def Name(self):
        return 'TradingSheetTemplate'
    def ClassName(self):
        return 'FTradingSheetTemplate'
    def Select(self):
        return self.uniqueNames( [(a.Name(), a.User()) for a in acm.FTradingSheetTemplate.Select('')])
    def Extension(self):
        return '.xml.tst'
        
if float(".".join(acm.ShortVersion().split(".")[0:2])) >= 4.3:
    Transporter.add_handler(FStoredAgentSetupTransporter())
else:
    Transporter.add_handler(FAgentParameterTransporter())

Transporter.add_handler(FExtensionModuleTransporter())
Transporter.add_handler(FTradeFilterTransporter())
Transporter.add_handler(FStoredASQLQueryTransporter())
Transporter.add_handler(FASQLQueryTransporter())
Transporter.add_handler(FAelTaskTransporter())
Transporter.add_handler(FAelTransporter())
Transporter.add_handler(FWorkbookTransporter())
Transporter.add_handler(FTradingSheetTemplateTransporter())
