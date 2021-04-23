"""-----------------------------------------------------------------------------
PURPOSE              :  ATS utility functions
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-05-26  CHG0102232     Libor Svoboda       Initial implementation
2021-02-03  CHG0149970     Libor Svoboda       Add delayed queue
"""
import os
import time
import xml.etree.ElementTree as ET
from collections import deque
from queue import Queue

import acm
import amb
from at_logging import getLogger


LOGGER = getLogger()


def get_param_value(ext_name, param_name):
    ext_obj = acm.GetDefaultContext().GetExtension(acm.FParameters, 
                                                   acm.FObject, ext_name)
    if not ext_obj:
        raise RuntimeError('FParameters extension "%s" not found.' % ext_name)
    params = ext_obj.Value()
    value = params.At(param_name)
    if value is None:
        raise RuntimeError('Parameter "%s" not found in FParameters "%s".'
                           % (param_name, ext_name))
    return str(value)


def get_amb_config(ext_name, params=None, ignore_instance_name=False):
    if params:
        return {
            'amb_server': params['amb_server'].strip(),
            'mb_name': params['mb_name'].strip(),
            'subjects': [item.strip() for item in params['subjects'].split(',') if item],
        }
    if ignore_instance_name:
        return {
            'amb_server': get_param_value(ext_name, 'AMBServer').strip(),
            'mb_name': get_param_value(ext_name, 'BrokerName').strip(),
            'subjects': [item.strip() for item in 
                         get_param_value(ext_name, 'Subjects').split(',') if item],
        }
    instance = acm.FDhDatabase['ADM'].InstanceName()
    try:
        amb_server = get_param_value(ext_name, instance + '.AMBServer')
    except:
        amb_server = get_param_value(ext_name, '.AMBServer')
    try:
        mb_name = get_param_value(ext_name, instance + '.BrokerName')
    except:
        mb_name = get_param_value(ext_name, '.BrokerName')
    try:
        subjects = get_param_value(ext_name, instance + '.Subjects')
    except:
        subjects = get_param_value(ext_name, '.Subjects')
    return {
        'amb_server': amb_server.strip(),
        'mb_name': mb_name.strip(),
        'subjects': [item.strip() for item in subjects.split(',') if item],
    }


def get_api_config(ext_name):
    return {
        'address': get_param_value(ext_name, 'APIAddress').strip(),
        'principal': get_param_value(ext_name, 'APIPrincipal').strip(),
    }


def event_cb(channel, event, instance, *args):
    event_string = amb.mb_event_type_to_string(event.event_type)
    LOGGER.info('Event callback: %s.' % event_string)
    if event_string == "Message":
        instance.message_number += 1
        instance.queue.put((amb.mb_copy_message(event.message), channel, instance.message_number))
    elif event_string == 'Status':
        try:
            instance.message_number = int(event.status.status)
        except ValueError:
            instance.message_number = 0
    elif event_string == 'Disconnect':
        instance.disconnected = True
        msg = 'Disconnected from AMB.'
        LOGGER.error(msg)
        raise RuntimeError(msg)
    LOGGER.info('Callback message number: %s' % instance.message_number)


class DelayedQueue(object):
    
    def __init__(self, delay_in_seconds):
        self._delay = delay_in_seconds
        self._queue = deque()
    
    def put(self, item):
        self._queue.append((time.time(), item))
    
    def empty(self):
        if not self._queue:
            return True
        if self._queue[0][0] + self._delay > time.time():
            return True
        return False
    
    def get(self):
        if self.empty():
            raise IndexError
        _, item = self._queue.popleft()
        return item


class AmbConnection(object):
    
    def __init__(self, fparam_name='', ignore_instance_name=False):
        self._ignore_instance_name = ignore_instance_name
        self.fparam_name = fparam_name
        self.queue = Queue()
        self.message_number = 0
        self.disconnected = False
    
    def init_delayed_queue(self, delay):
        self.queue = DelayedQueue(delay)
    
    def connect(self):
        params = acm.TaskParameters()['taskParameters']
        LOGGER.info('ATS task parameters: %s.' % params)
        try:
            config = get_amb_config(self.fparam_name, params, self._ignore_instance_name)
        except:
            instance = acm.FDhDatabase['ADM'].InstanceName()
            LOGGER.exception('Failed to get AMB config for "%s".' % instance)
            raise
        LOGGER.info('Connecting to AMB using %s.' % config)
        try:
            amb.mb_init(config['amb_server'])
            reader = amb.mb_queue_init_reader(config['mb_name'], event_cb, self)
            for subject in config['subjects']:
                amb.mb_queue_enable(reader, subject)
        except:
            self.disconnected = True
            LOGGER.exception('Failed to connect to AMB.')
            raise
        else:
            self.disconnected = False
            LOGGER.info('Successfully connected to AMB.')
        amb.mb_poll()


class XmlOutput(object):
    
    open_tag = '<TODAY>\n'
    close_tag = '</TODAY>\n'
    encoding = '<?xml version="1.0" encoding="ISO-8859-1" ?>\n'
    
    def __init__(self):
        self._path = ''
        self._init = False
        self._closed = False
    
    @classmethod
    def mandatory_lines(cls):
        return [cls.open_tag, cls.close_tag, cls.encoding]
    
    def _create_new(self):
        with open(self._path, 'w') as xml_file:
            xml_file.write(self.encoding)
            xml_file.write(self.open_tag)
    
    def _check_existing(self):
        with open(self._path, 'r') as xml_file:
            lines = xml_file.readlines()
        if not lines:
            self._create_new()
            return
        if not lines[-1] == self.close_tag:
            return
        filtered_lines = filter(lambda x: x not in self.mandatory_lines(), lines)
        with open(self._path, 'w') as xml_file:
            xml_file.write(self.encoding)
            xml_file.write(self.open_tag)
            xml_file.writelines(filtered_lines)
    
    def init_file(self, file_path):
        self._path = file_path
        if self._init and not self._closed:
            return
        if os.path.exists(self._path):
            self._check_existing()
        else:
            self._create_new()
        self._init = True
        self._closed = False
    
    def close_file(self):
        if not self._init or self._closed:
            return
        with open(self._path, 'a') as xml_file:
            xml_file.write(self.close_tag)
        self._closed = True
    
    def write(self, text):
        with open(self._path, 'a') as xml_file:
            xml_file.write(text)
    
    def get_path(self):
        return self._path


class XmlOutputConverter(object):
    
    def __init__(self, source):
        self._source = source
        self._root = ET.Element('Entity')
    
    def create_output(self):
        raise NotImplementedError
    
    def get_string(self, init_indent=1, indent='\t'):
        if not len(self._root):
            return ''
        elements = ET.tostring(self._root).replace('><', '>\n<').split('\n')
        output = ''
        current_indent = init_indent
        for element in elements:
            if element.startswith('</'):
                current_indent -= 1
            output += current_indent * indent + element + '\n'
            if not ('/>' in element or '</' in element):
                current_indent += 1
        return output
