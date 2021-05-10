'''
A D S   C O M P A R A T O R

Author: Michael Gogins
Copyright (C) 2015 by SunGard Front Arena AB

Generates a list of entities from a package in the host Prime, then diffs the 
entities, comparing AMBA messages for the entities between the host (source) 
ADS and a remote (target) ADS.

Algorithm: 

1)  The inputs are:
    a) A list of FObjects.
    b) The target ADS address, username, and password.
2)  Write the entity keys (ClassName[StringKey]) in lexicographic order to a 
    temporary file.
3)  On the host (source) Prime:
    a)  Run this script.
    b)  Read the entity key file.
    c)  Turn each entity key into an FObject (if possible).
    d)  Turn each FObject into an AMBA message without sequence numbers,
        without create and update times and users, and with string enums 
        and such. Certain messages are skipped, namely those that have 
        only sequence numbers as IDs AND that also occur as sub-messages in 
        other messages.
    e)  Save the AMBA messages in a temporary file.
4)  Use the subprocess module to run this same script in arena_python on the 
    target ADS, repeating steps 3)a) through 3)e).
5)  Use the subprocess module to use an external diff program such as WinMerge
    to compare the source messages file with the target messages file. Any 
    differences will indicate some sort of bug, either in the dependency tree 
    builder and AMBA export code, or in AMBA itself. Most differences can be 
    fixed manually with a little work.
'''

test = True

input_objects = []
input_filename = ''
arena_python = ''
host_ads = ''
host_ads_username = ''
host_ads_password = ''
target_ads = ''
target_ads_username = ''
target_ads_password = ''

import acm

import FLogger
import os
import os.path

import PackageInstallerParametersManager
#reload(PackageInstallerParametersManager)

import subprocess

import tempfile
import time
import traceback

parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
prime_folder = parameters.read('PrimeFolder')
diff_command_template = str(parameters.read('MergeToolCommandTemplate'))
 
logger = FLogger.FLogger(name=__name__, level=verbosity)

generator = acm.FAMBAMessageGenerator()
generator.ShowAllFields(True)
generator.ShowTimeStamps(False)
generator.NiceEnumNames(True)
generator.ShowSeqNbr(False)

input_file = None
input_filename = None
host_file = None
host_filename = None
target_file = None
target_filename = None

fields_to_omit = set()
fields_to_omit.add('CREAT_TIME')
fields_to_omit.add('UPDAT_TIME')
fields_to_omit.add('CREAT_USRNBR')
fields_to_omit.add('UPDAT_USRNBR')
fields_to_omit.add('CREAT_USRNBR.USERID')
fields_to_omit.add('UPDAT_USRNBR.USERID')
fields_to_omit.add('VERSION_ID')
fields_to_omit.add('SOURCE')
fields_to_omit.add('TIME')

# Messages to omit for parts that are NOT removed HERE.
messages_to_skip = set()
messages_to_skip.add('BENCHMARK')
messages_to_skip.add('YIELDCURVEPOINT')
messages_to_skip.add('CALENDARDATE')
messages_to_skip.add('PRICE')

classes_to_omit = set()
classes_to_omit.add('FBenchmark')
classes_to_omit.add('FYieldPoint')
classes_to_omit.add('FVolatilityPoint')
classes_to_omit.add('FCalendarDate')
classes_to_omit.add('FChoiceList')
classes_to_omit.add('FPrice')

parts_to_omit = set()
parts_to_omit.add('INSTRUMENTALIAS')

def subprocess_printlog(command, wait=True, shell=False):
    command = command.replace('\\\\', '/');
    command = command.replace('\\', '/');
    logger.debug('subprocess command: %s' % command)
    sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    if wait == True:
        out, err = sp.communicate()
        if out:
            logger.info("Standard output of subprocess:")
            logger.info(out)
        if err:
            logger.info("Standard error of subprocess:")
            logger.info(err)
        logger.debug("returncode of subprocess: %s" % sp.returncode)        

def remove_fields(message):
    for field in fields_to_omit:
        message.RemoveKeyString(field)
    for child_message in message.Messages():
        remove_fields(child_message)
        
# Using a depth-first search, sort the submessages of each message in the 
# tree of messages.
def sort_parts(message):
    for submessage in message.Messages():
        sort_parts(submessage)
    types = set()
    for submessage in message.Messages():
        tipe = submessage.Type()
        types.add(tipe)
    for tipe in types:
        submessages = message.FindMessages(tipe)
        sort_me = {}
        for submessage in submessages:
            message.RemoveMessage(submessage)
            # This key is completely arbitrary, but at least it will be the 
            # same across ADSs.
            key = str(submessage)
            sort_me[key] = submessage
        sorted_keys = sorted(sort_me.keys())
        for key in sorted_keys:
            part = sort_me[key]
            if part not in parts_to_omit:
                message.AddMessage(part)
        
def message_for_entity(entity):
    message = generator.Generate(entity)
    remove_fields(message)
    sort_parts(message)
    return message
    
def key_for_entity(entity):
    return '%s[%s]' % (entity.ClassName(), entity.StringKey())
    
def entity_for_key(key):
    class_name = key.split('[')[0]
    id = key.split('[')[1].split(']')[0]
    code = 'acm.%s["%s"]' % (class_name, id)
    object = eval(code)
    return object
    
def write_entity_messages(objects, filename):
    keys = []
    for object in objects:
        keys.append(key_for_entity(object))
    keys.sort()
    input_file = open(filename, 'w')
    for key in keys:
        input_file.write('OBJECT KEY: %s\n' % key)
        try:
            entity = entity_for_key(key)
            message = message_for_entity(entity)
            message_type = str(message.Messages()[0].Type())
            if message_type not in messages_to_skip:
                logger.info('Writing:  %s' % key)
                input_file.write(str(message))
            else:
                logger.info('Skipping: %s' % key)
        except:
            error_text = traceback.format_exc()
            input_file.write(error_text)
    input_file.close()
    return input_filename
    
def write_entity_keys(objects, filename):
    input_file = open(filename, 'w')
    input_file.write('ADS: %s\n\n' % acm.ADSAddress())
    keys = []
    for object in objects:
        if str(object.ClassName()) not in classes_to_omit:
            keys.append(key_for_entity(object))
    keys.sort()
    input_file = open(filename, 'w')
    for key in keys:
        input_file.write('%s\n' % key)
    input_file.close()
    return input_filename

def create_entity_keys_file_from_objects(objects, filename):
    filename = write_entity_keys(objects, filename)
    
def create_entity_messages_file_from_entity_keys_file(entity_keys_filename, messages_filename):
    input_file = open(entity_keys_filename, 'r')
    output_file = open(messages_filename, 'w')
    output_file.write('ADS: %s\n\n' % acm.ADSAddress())
    for key in input_file:
        key = key.rstrip()
        logger.info('Read object key: %s' % key)
        output_file.write('OBJECT KEY: %s\n\n' % key)
        try:
            entity = entity_for_key(key)
            message = message_for_entity(entity)
            message_type = str(message.Messages()[0].Type())
            if message_type not in messages_to_skip:
                logger.info('Writing message for object:  %s' % key)
                output_file.write(str(message))
            else:
                logger.info('Skipping: %s' % key)
        except:
            error_text = traceback.format_exc()
            output_file.write(error_text)
        output_file.write('\n')
    input_file.close()
    output_file.close()
    
def diff_messages_files(host_messages_filename, target_messages_filename):
    diff_command = diff_command_template % (host_messages_filename, target_messages_filename)
    subprocess_printlog(diff_command, wait=False)
    
def create_remote_messages_file(ads, user, password, entity_keys_filename, target_entity_messages_filename):
    # Save this module as an external Python script, and run it in arena_python.
    extensionModule = acm.FExtensionModule['PackageInstaller']
    pythonModule = extensionModule.GetExtension(acm.FPythonCode, acm.FObject, 'AdsComparator')
    this_script = pythonModule.Value()
    script_filename = os.path.join(tempfile.tempdir, 'AdsComparator.py')
    script_file = open(script_filename, 'w')
    lines = this_script.split('\n')
    for line in lines:
        script_file.write(line + '\n')
    script_file.flush()
    script_file.close()    
    command = '"%s\\arena_python.exe" -server %s -username %s -password %s -filename "%s"' % (prime_folder, ads, user, password, script_filename)
    os.putenv('entity_keys_filename', entity_keys_filename)
    os.putenv('target_entity_messages_filename', target_entity_messages_filename)
    subprocess_printlog(command)    
    
def compare_ads_entities(objects, target_ads, target_ads_username, target_ads_password):
    began_compare_ads_entities = time.clock()
    logger.info('Began compare_ads_entities(<%s, %s>, %s, %s, %s)...' %(type(objects), len(objects), target_ads, target_ads_username, target_ads_password))
    entity_keys_file_handle, entity_keys_filename = tempfile.mkstemp(text=True, prefix='entity_keys_')
    create_entity_keys_file_from_objects(objects, entity_keys_filename)
    logger.info('Created file of host entity keys from %s for comparison at: %s' % (acm.ADSAddress(), entity_keys_filename))
    entity_messages_file_handle, entity_messages_filename = tempfile.mkstemp(text=True, prefix='entity_messages_')
    target_entity_messages_file_handle, target_entity_messages_filename = tempfile.mkstemp(text=True, prefix='target_entity_messages_')
    create_entity_messages_file_from_entity_keys_file(entity_keys_filename, entity_messages_filename)
    logger.info('Created file of host entity messages from %s for comparison at: %s' % (acm.ADSAddress(), entity_messages_filename))
    create_remote_messages_file(target_ads, target_ads_username, target_ads_password, entity_keys_filename, target_entity_messages_filename)
    logger.info('Created file of target entity messages from %s for comparison at: %s' % (target_ads, target_entity_messages_filename))
    diff_messages_files(entity_messages_filename, target_entity_messages_filename)
    ended_compare_ads_entities = time.clock()
    elapsed_compare_ads_entities = ended_compare_ads_entities - began_compare_ads_entities
    logger.info('Ended compare_ads_entities (%12.4f seconds).' % elapsed_compare_ads_entities)

try:
    entity_keys_filename = os.environ.get('entity_keys_filename')
    target_entity_messages_filename = os.environ.get('target_entity_messages_filename')
    if os.environ.get('entity_keys_filename') != None:
        create_entity_messages_file_from_entity_keys_file(entity_keys_filename, target_entity_messages_filename)
except:
    logger.error(traceback.format_exc())

