'''----------------------------------------------------------------------------------------------------------
MODULE                  :       AMB_Reader_Writer
PROJECT                 :       PACE MM
PURPOSE                 :       Reader and Write AMBA messages to specified AMB.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This generic module contains three classes:
    
    AMB_BaseClass       :       Used to Open and Close an AMB connection.
    AMB_Writer          :       Used to Write messages to a specified AMB.
                                Input needed:   AMB Address, MB Name, Event Callback function, Source, Subject.
    AMB_Reader          :       Used to Read messages from a specified AMB.
                                Input needed:   AMB Address, MB Name, Event Callback function, Source List.
'''

import amb
import FOperationsUtils as Utils
CONST_IsAMBConnected = False
CONST_IsAMBConnectedKerberos = False
class AMB_BaseClass():
    def __init__(self, ambaddress, mbName, event_cb):
        self._ambaddress = ambaddress
        self._channel = ''
        self._event_cb = event_cb
        self._mbName = mbName
        
    def open_AMB_Connection(self, isConnected=True):
        global CONST_IsAMBConnected
        if CONST_IsAMBConnected is True and isConnected is True:
            return CONST_IsAMBConnected
        CONST_IsAMBConnected = False
        amb.mb_init(self._ambaddress)
        CONST_IsAMBConnected = True
        return CONST_IsAMBConnected

    
    def open_AMB_Connection_Kerberos(self, kerbPrincipal, ambUserName, password, applicationName, singleSignOn,
                                     isConnected=True):
        global CONST_IsAMBConnectedKerberos
        if CONST_IsAMBConnectedKerberos is True and isConnected is True:
            return CONST_IsAMBConnectedKerberos
        CONST_IsAMBConnectedKerberos = False
        amb.mb_init_kerb2(self._ambaddress, kerbPrincipal, ambUserName, password, applicationName, singleSignOn)
        CONST_IsAMBConnectedKerberos = True
        return CONST_IsAMBConnectedKerberos

    
    def close_AMB_Connection(self):
        global CONST_IsAMBConnectedKerberos
        global CONST_IsAMBConnected
        CONST_IsAMBConnectedKerberos = False
        CONST_IsAMBConnected = False
        return amb.mb_close() == None


class AMB_Writer(AMB_BaseClass):
    def __init__(self, ambaddress, mbName, event_cb, source, subject):
        AMB_BaseClass.__init__(self, ambaddress, mbName, event_cb)
        self.__source = source
        self.__subject = subject

    def __open_Writer_Channel(self):
        try:
            self._channel = amb.mb_queue_init_writer(self._mbName, self._event_cb, self.__source)
            Utils.Log(True, 'Connection to AMB %s successful with Sender MB Name %s and Source %s.' %(self._ambaddress, self._mbName, self.__source))
            return True
        except:
            Utils.Log(True, 'ERROR: Could not open the writer channel with Sender MB Name %s and Source %s.' %(self._mbName, self.__source))
            return False

    def open_AMB_Sender_Connection(self, isConnected=True):
        if not (self._ambaddress and self._mbName and self._event_cb and self.__source):
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. Please check veriables AMB Address, Sender MB Name and Source.')
            return False

        if self.open_AMB_Connection(isConnected):
            return self.__open_Writer_Channel()
        else:
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. mb_init error in internal function.')
            return False

    def open_AMB_Sender_Connection_Kerberos(self, kerbPrincipal, ambUserName, password, applicationName, singleSignOn,
                                            isConnected=True):
        if not (self._ambaddress and self._mbName and self._event_cb and self.__source):
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. Please check veriables AMB Address, Sender MB Name and Source.')
            return False

        if self.open_AMB_Connection_Kerberos(kerbPrincipal, ambUserName, password, applicationName, singleSignOn, isConnected):
            return self.__open_Writer_Channel()
        else:
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. mb_init error in internal function.')
            return False

    def post_Message_To_AMB(self, message):
        mbuf_p = amb.mbf_create_buffer()
        message.mbf_generate(mbuf_p)
        queue_write_error = amb.mb_queue_write(self._channel,
                                            self.__subject,
                                            mbuf_p.mbf_get_buffer_data(),
                                            mbuf_p.mbf_get_buffer_data_size(),
                                            'status_buf')
        Utils.Log(True, 'The AMB Poster posted the following message to the AMB: \n%s\n' % message.mbf_object_to_string())
        return (queue_write_error == None)

    def post_Message_To_AMB_With_Subject(self, message, subject):
        mbuf_p = amb.mbf_create_buffer()
        message.mbf_generate(mbuf_p)
        queue_write_error = amb.mb_queue_write(self._channel,
                                            subject,
                                            mbuf_p.mbf_get_buffer_data(),
                                            mbuf_p.mbf_get_buffer_data_size(),
                                            'status_buf')
        Utils.Log(True, 'The AMB Poster posted the following message to the AMB: \n%s\n' % message.mbf_object_to_string())
        return (queue_write_error == None)

class AMB_Reader(AMB_BaseClass):
    def __init__(self, ambaddress, mbName, event_cb, subscriptionSourceList):
        AMB_BaseClass.__init__(self, ambaddress, mbName, event_cb)
        self.__subscriptionList = subscriptionSourceList

    def __open_Receiver_Channel(self):
        try:
            self._channel = amb.mb_queue_init_reader(self._mbName, self._event_cb, None)
            return True
        except:
            Utils.Log(True, 'ERROR: Could not open the receiver channel with Receiver MB Name %s.' % self._mbName)
            return False

    def __enable_Subscription(self):
        for subscription in self.__subscriptionList:
            try:
                amb.mb_queue_enable(self._channel, subscription)
            except:
                Utils.Log(True, 'ERROR: Could not subscribe to %s.' % subscription)
                return False
        Utils.Log(True, 'Connection to AMB %s successful with Receiver MB Name %s.' %(self._ambaddress, self._mbName))
        return True

    def open_AMB_Receiver_Connection(self, isConnected=True):
        if not (self._ambaddress and self._mbName and self._event_cb and self.__subscriptionList):
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. Please check veriables AMB Address, Sender MB Name and Subscription List.')
            return False

        if self.open_AMB_Connection(isConnected):
            if self.__open_Receiver_Channel():
                return self.__enable_Subscription()
            else:
                return False
        else:
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. mb_init error in internal function.')
            return False

    def open_AMB_Receiver_Connection_Kerberos(self, kerbPrincipal, ambUserName, password, applicationName, singleSignOn,
                                              isConnected=True):
        if not (self._ambaddress and self._mbName and self._event_cb and self.__subscriptionList):
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. Please check veriables AMB Address, Sender MB Name and Subscription List.')
            return False

        if self.open_AMB_Connection_Kerberos(kerbPrincipal, ambUserName, password, applicationName, singleSignOn, isConnected):
            if self.__open_Receiver_Channel():
                return self.__enable_Subscription()
            else:
                return False
        else:
            Utils.Log(True, 'ERROR: Could not open a connection to the AMB. mb_init error in internal function.')
            return False
