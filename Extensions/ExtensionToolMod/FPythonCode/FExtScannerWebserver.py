from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FExtScannerWebserver - Starts a webserver that will display all reports
    with the possiblity to update changed extensions

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""


import os
import re
import sets
from threading import Thread
import webbrowser

import acm

import web

import FExtensionAttributeRemoved
import FExtensionUtils
from FHTML import *


updated_extensions = {}

class WebserverThread(Thread):
    def __init__(self, path):
        self.urls = ('/LocalFiles/(.*)', 'write_report',
                     '/ExcludeDefinition/(.*)','exclude_definition',
                    '/UpdateExtensionAttribute/(.*)', 'update_extension',
                    '/UpdateExtensionModule/(.*)', 'update_module',
                    '/UndoUpdateExtension/(.*)', 'undo_update_extension',
                    '/UndoUpdateExtensionModule/(.*)', 'undo_update_module',
                    '/UpdateExtensionInModule/(.*)', 'update_extension_in_module',
                    '/(.*)', 'show_address')
        globals()['FExtWebserverRunning'] = True
        globals()['path'] = path
        Thread.__init__(self)
    def run(self):
        web.run(self.urls)

class write_report:
    def get_position_and_tag(self, line):
        tagpos = []
        for type in ["ExtensionAttribute", "ExtensionModule", "OneExtensionFromList"]:
            tag1, tag2 = get_update_tag(type)
            link_pos = line.find(tag1)
            tagpos.append((link_pos, tag1, tag2, type))    
        tagpos.sort()
        for tag in tagpos:
            if tag[0] >= 0: 
                return tag
        return -1, None, None, None
        
    def excludeDefinition(self, definition):
        """ Get list of definitions which should be excluded from scan.
            The database might for example contain hundreds of extension attributes
            with the definition "true". These could be excluded from the scan.
        """
        path = globals()['path'] + '\\excludedDefinitions.txt'

        if os.path.exists(path):
            file = open(path,'r')
        else:
            return False
        lines = file.readlines()
        file.close()
        for line in lines:
            if definition == line.replace('\n',''):
                return True
        return False
        
    def nbrOfAttrWithExcludedDefs(self, eqExt):
        path = globals()['path'] + '\\excludedDefinitions.txt'        
        if os.path.exists(path):
            file = open(path,'r')
            lines = [line.replace('\n','') for line in file.readlines()]
        else:
            return 0
        count = 0
        for ext in eqExt:
            if ext in lines:
                count += 1
        return count
        
    def writeEqDefReport(self, name):
        #name is a path to a html file OR a path + msg.
        start = name.find("MSG")
        if start == -1:
            msg = ''
            fileName = name
        else:
            msg = name[start+3:]
            fileName = name[:start]

        file = open(fileName, 'r')
        line = file.readline()

        exclude = False
        while(line):
            #Find placeholder in html for 'exclusion message'
            if line.find('<!--msg-->') != -1 and msg != '':
                print (msg)
                
            #Get the definitions list inside html comment.
            if line.find('<!--definitionsList:') != -1:
                definitionList = line.replace('<!--definitionList:','').replace('-->','').replace('\n','').split('\xa4')
                nbrOfExcludedUpdated = self.nbrOfAttrWithExcludedDefs(definitionList)
                web.output(h2("(Excluded attributes updated = %s)"% str(nbrOfExcludedUpdated)))

            #Get the definition inside html comment.
            #Check if extension attributes with this definition should be excluded.
            if line.find('<!--definition:') != -1:
                exclude = False
                definition = line.replace('<!--definition:','').replace('-->','').replace('\n','')
                exclude = self.excludeDefinition(definition)
                
            #Always print module header e.g "[Default]"
            if exclude and line.find('<!--moduleHeader:-->') != -1:
                print (line)

            if not exclude:
                #button placeholder are comments in html file
                if line.find('<!--button-->') != -1:
                    print ('<br>')
                    web.output(html_link_button("Exclude from next scan", "/ExcludeDefinition/" + definition + "/" + fileName))
                else:
                    print (line)
            line = file.readline()

        file.close()

    def GET(self, name):
        web.header("Content-Type","text/html; charset=utf-8")
        web.header("pragma", "no-cache")
        web.header("Expires", "-1")  
        
        folder = 'ExtensionScanReport_files'
        isSlash = name[name.find(folder)+len(folder)]
        if isSlash != '/':
            name = name.replace(folder, folder+'/')
        
        if name.find('EqDef') != -1:
            #Write report for equal extension attribute definitions.
            self.writeEqDefReport(name)
            return
      
        file = open(name, 'r')
        # "<!-- Add update link for " + str(ext[0]) + "-->"
        line = file.readline()        
        while(line):
            linkPos, tag1, tag2, type = self.get_position_and_tag(line)
            while(linkPos != -1):
                linkEnd = line[linkPos + len(tag1):].find(tag2) + linkPos + len(tag1)
                update_object = line[linkPos + len(tag1):linkEnd]
                update_attribute = update_object[:update_object.find('{')]
                update_dictionary = FExtensionUtils.dictionary_from_string(update_object[update_object.find('{'):-1])
                web.output(line[:linkEnd + len(tag2)])
                if type == "ExtensionAttribute":
                    if update_attribute in updated_extensions:
                        if not updated_extensions[update_attribute].extensions_to_update:
                            updated_extensions[update_attribute].extensions_to_update = \
                                FExtensionUtils.dictionary_from_string(update_object[update_object.find('{'):])
                        if updated_extensions[update_attribute].extensions_to_update == updated_extensions[update_attribute].updated_extensions:
                            web.output(html_link_button("Already updated, UNDO", "/UndoUpdateExtension/" + update_attribute + '/' + name))
                        else:
                            web.output(html_link_button("Partially updated, UPDATE ALL", "/UpdateExtensionAttribute/" + update_object + '/' + name))
                    else:                        
                        web.output(html_link_button("Update Extension", "/UpdateExtensionAttribute/" + update_object + '/' + name))
                elif type == "ExtensionModule":
                    if not FExtensionAttributeRemoved.get_extensions_with_removed_attributes(update_attribute, update_dictionary, {})[0]:
                        web.output(html_link_button("All extensions updated, UNDO", "/UndoUpdateExtensionModule/" + update_attribute + '/' + name))
                    else:
                        updated_in_module = False
                        for ext in updated_extensions:
                            if ext[1:ext.find(']')] == update_attribute:
                                updated_in_module = True
                                break
                        if updated_in_module:
                            web.output(html_link_button(update_attribute + " partially updated, UPDATE ALL", "/UpdateExtensionModule/" + update_object + '/' + name))
                        else:
                            web.output(html_link_button("Update all extensions in " + update_attribute, "/UpdateExtensionModule/" + update_object + '/' + name))
                elif type == "OneExtensionFromList":
                    module_name = update_attribute
                    menu_list = [(name, "Choose extension...")]
                    ext_string = update_object[update_object.find('{') + 1:-1]
                    extpos = ext_string.find(',')
                    while(extpos != -1):
                        menu_list.append(("/UpdateExtensionInModule/" + module_name + '{' + ext_string[:extpos] + '}/' + name, ext_string[:ext_string.find(':')]))
                        ext_string = ext_string[extpos + 2:]
                        extpos = ext_string.find(',')
                    menu_list.append(("/UpdateExtensionInModule/" + module_name + '{' + ext_string + '}/' + name, ext_string[:ext_string.find(':')]))
                    web.output(html_drop_down_menu(menu_list, "ExtensionsIn" + module_name.replace(".", "_").replace(" ", "_"), "Replace extension in module"))
                    
                    
                line = line[linkEnd + len(tag2):]
                linkPos, tag1, tag2, type = self.get_position_and_tag(line)
                
            
            web.output(line)    
            line = file.readline()
        file.close()
 

class exclude_definition:
    """ Executed when the 'exclude from next scan'-button is clicked. 
        The definition is saved in a text file on disk and 
        in future scans these definitions will be excluded.
    
    """
    
    def addToExcludedDefinitionsList(self, definition):
        path = globals()['path'] + '\\excludedDefinitions.txt'
        if not os.path.exists(path):
            file = open(path, 'w')
            file.close()
        file = open(path,'r')        
        defList = [line.replace('\n','') for line in file.readlines()]
        file.close()
        
        if definition not in defList:
            defList.append(definition)
            defList.sort()

        file = open(path,'w')
        for el in defList:
            file.write(el+'\n')
        file.close()

    def GET(self, name):                
        definition = name[:name.find("c:")-1]
        file =       name[name.find("c:"):]

        self.addToExcludedDefinitionsList(definition)        

        msg = """
              <br><br>
              <font color=red>Extension attributes with definition equal to:
              <br><b>%s</b><br>
              will not be included in following scans.
              <br>Definitions can be removed/added by manually
               editing the file <b>%s</b>. (1 definition / line)</font>
               """ % (definition, globals()['path'] + 'excludedDefinitions.txt')

        web.redirect('/LocalFiles/'+file+'MSG'+msg)
       
class update_extension:
    def GET(self, name):
        extattr = name[:name.find('{')]
        module_name = extattr[1:extattr.find(']')]
        class_name = extattr[extattr.find(']') + 1:extattr.find(':')]
        extension_name = extattr[extattr.find(':') + 1:]
        rename_dictionary = FExtensionUtils.dictionary_from_string(name[name.find('{') + 1: name.find('}')])
        call_address = name[name.find('/') + 1:]
        
        oldDef = FExtensionAttributeRemoved.update_extension_attribute(module_name, class_name, extension_name, rename_dictionary)
        
        updated_extensions[extattr] = FExtensionUtils.UpdatedExtension(oldDef, rename_dictionary, rename_dictionary)
        
        web.redirect('/LocalFiles/' + call_address + '#' + extension_name)
        
class update_module:
    def GET(self, name):
        module_name = name[:name.find('{')]
        rename_dictionary = FExtensionUtils.dictionary_from_string(name[name.find('{') + 1: name.find('}')])
        call_address = name[name.find('/') + 1:]
        
        FExtensionAttributeRemoved.update_extension_module(module_name, updated_extensions, rename_dictionary)
        
        web.redirect('/LocalFiles/' + call_address)

        
class update_extension_in_module:
    def GET(self, name):
        module_name = name[:name.find('{')]
        rename_dictionary = FExtensionUtils.dictionary_from_string(name[name.find('{') + 1: name.find('}')])
        call_address = name[name.find('/') + 1:]
        
        FExtensionAttributeRemoved.update_extension_module(module_name, updated_extensions, rename_dictionary)
        
        web.redirect('/LocalFiles/' + call_address)

class undo_update_extension:
    def GET(self, name):
        extattr = name[:name.find('/')]
        module_name = extattr[1:extattr.find(']')]
        class_name = extattr[extattr.find(']') + 1:extattr.find(':')]
        extension_name = extattr[extattr.find(':') + 1:]
        call_address = name[name.find('/') + 1:]
        
        if extattr in updated_extensions:
            dummy_context = acm.FExtensionContext()
            dummy_context.AddModule(module_name)
            dummy_context.EditImport("FExtensionAttribute", extattr + " = " + updated_extensions.pop(extattr).original_code)
            dummy_context.RemoveModule(module_name)
        
        if module_name in updated_extensions:
            del updated_extensions[module_name]
        
        web.redirect('/LocalFiles/' + call_address + '#' + extension_name)

class undo_update_module:
    def GET(self, name):
        module_name = name[:name.find('/')]
        call_address = name[name.find('/') + 1:]
        
        dummy_context = acm.FExtensionContext()
        dummy_context.AddModule(module_name)
        for ext in updated_extensions.keys():
            if ext[1:ext.find(']')] == module_name:
                dummy_context.EditImport("FExtensionAttribute", ext + " = " + updated_extensions.pop(ext).original_code)
        dummy_context.RemoveModule(module_name)

        web.redirect('/LocalFiles/' + call_address)

        

class show_address:
    def GET(self, name):
        web.header("Content-Type","text/html; charset=utf-8")
        web.header("pragma", "no-cache")
        print ("Matched the address")
        print (name)
        print ("<!-- Detta är en kommentar -->")

def start_webserver(address, path):

    if not 'FExtWebserverRunning' in globals() or not globals()['FExtWebserverRunning']:
        web_server = WebserverThread(path)
        web_server.start()

    webbrowser.open(address)
    print ("\nDONE")
