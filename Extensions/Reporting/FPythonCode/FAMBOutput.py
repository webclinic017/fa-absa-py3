from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAMBOutput - Module for sending XML to AMB.
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import ael
import amb
import time

def event_cb(channel, event_p, *arg_p):
    """Callback function"""
    etype=amb.mb_event_type_to_string(event_p.event_type)
    if etype == 'Status':
        ael.log('AMB Last Acknowledge Status = %s' % event_p.status.status)
        print ('AMB Last Acknowledge Status = %s' % event_p.status.status)
    elif etype == 'Message':
        ael.log('AMB Message Id      : %s' % str(event_p.message.id))
        ael.log('AMB Message Subject : %s' % str(event_p.message.subject))
        ael.log('AMB Message Time    : %s' % str(event_p.message.time))
        ael.log('AMB Message Size    : %s' % str(event_p.message.size))
        ael.log('AMB Message Type    : %s' % str(event_p.message.event_type))
        
        print ('AMB Message Id      : %s' % str(event_p.message.id))
        print ('AMB Message Subject : %s' % str(event_p.message.subject))
        print ('AMB Message Time    : %s' % str(event_p.message.time))
        print ('AMB Message Size    : %s' % str(event_p.message.size))
        print ('AMB Message Type    : %s' % str(event_p.message.event_type))
        buffer = amb.mbf_create_buffer_from_data(event_p.message.data_p)
        message = buffer.mbf_read().mbf_object_to_string_xml()
        ael.log('AMB Message Data XML: \n%s' % message)
        print ('AMB Message Data XML: \n%s' % message)
        amb.mb_queue_accept(channel, event_p.message, time.strftime("%Y-%m-%d %H:%M:%S"))
    elif etype == 'Disconnect':
        ael.log("Event Disconnect")
        print ("Event Disconnect")
    elif etype == 'End of Data':
        ael.log('AMB End of Data')
        print ('AMB End of Data')
    else:
        ael.log('AMB Unknown event type =' % etype)
        print ('AMB Unknown event type =' % etype)

def sendXMLToAMB(inputXML, ambAddress, ambSender, ambSubject, ambXmlMessage):
    """ Send xml data file to AMB """
    # connect to AMB
    try:
        amb.mb_init(ambAddress)
    except Exception as err:
        ael.log('ERROR: ' + str(err) + '\nOccured when trying to connect to AMB at %s' % ambAddress)
        print ('ERROR: ', err, '\nOccured when trying to connect to AMB at %s' % ambAddress)
        return
    # create writer channel
    try:
        writer = amb.mb_queue_init_writer(ambSender, event_cb, None)
    except Exception as err:
        ael.log('ERROR: ' + str(err) + '\nOccured when trying to create writer channel for sender %s' % ambSender)
        print ('ERROR: ', err, '\nOccured when trying to create writer channel for sender %s' % ambSender)
        return
        
    try:
        # Create XML Report AMB messages
        message = amb.mbf_start_message( None, "INSERT_XMLREPORT", "1.0", None, ambSender )

        # Start XMLREPORT list
        mb_msg = message.mbf_start_list("XMLREPORT")

        # Insert XML Report as REPORT_DATA
        mb_msg.mbf_add_string("REPORT_DATA", inputXML)

        # End XMLREPORT list
        mb_msg.mbf_end_list()

        # End XML Report AMB message
        message.mbf_end_message()
    except Exception as err:
        ael.log('ERROR: ' + str(err) + '\nOccured when trying to create AMBA message')
        print ('ERROR: ', err, '\nOccured when trying to create AMBA message')
        return

    try:
        # Create AMB Buffer
        buffer = amb.mbf_create_buffer()
    except Exception as err:
        ael.log('ERROR: ' + str(err) + '\nOccured when trying to create buffer for the XML message')
        print ('ERROR: ', err, '\nOccured when trying to create buffer for the XML message')
        return
        
    try:
        # mbf_generate(buffer) will compress the message if it's greater than 64Kb in size        
        type = 'AMB'
        if ambXmlMessage:
            # mbf_generate_xml generates messages on XML format
            message.mbf_generate_xml(buffer) 
            type = 'XML' 
        else:
            # mbf_generate generates messages on FRONT internal AMB format
            message.mbf_generate(buffer)           
    except Exception as err:
        ael.log('ERROR: ' + str(err) + '\nOccured when trying to generate the ' + type + ' message')
        print ('ERROR: ', err, '\nOccured when trying to generate ' + type + ' message')
        return

    # send the XML message to the AMB
    status = amb.mb_queue_write(writer, ambSubject, buffer.mbf_get_buffer_data(), buffer.mbf_get_buffer_data_size(), time.strftime("%Y-%m-%d %H:%M:%S"))
    # check the status
    if status:
        ael.log("ERROR: ould not send the XML message to the AMB")
        print ("ERROR: could not send the XML message to the AMB")
    else:
        ael.log("XML report sent to AMB %s" % ambAddress)
        print ("XML report sent to AMB %s" % ambAddress)
