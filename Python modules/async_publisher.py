'''
Created on 8 Jul 2016

@author: conicova
'''
from Queue import Queue  # thread safe
import logging
import threading
import time
from datetime import datetime
from at_log_message import LogMessage, LogRecord, UTC_OFFSET_TIMEDELTA
from uuid import uuid4

import pika
from pika.exceptions import ProbableAuthenticationError

# from collections import deque
LOGGER = logging.getLogger(__name__)

logging.getLogger("pika").setLevel(logging.CRITICAL)

USE_ACM_THREAD = True

class MQNotImplementedError(Exception):
    pass

class MQMessage(object):
    
    def to_json(self):
        raise MQNotImplementedError("Method 'to_json' is not implemented")

class MQConfig(object):
    
    def __init__(self):
        self.instance_name = "Playground"
        
        self.amqp = ""
        self.exchange = 'playground'
        self.routing_key = 'consumer.playground'
        self.queue_dashboard = 'fa_dashboard';
        self.queue_elasticsearch = 'fa_elasticsearch'
        self.delivery_mode = 1 
        ''' set delivery mode to 2 to make messages persistent.
            The queue has to be declared Durable.
        '''
        self.durable_exchange = False
        self.durable_queue = False
        
        self.queue = ""
        self.app_id = "default-app-id"
        self.content_type = "'application/json'"
        self.exchange_type = "fanout"

class FAHeart(object):
    
    def __init__(self, process_name, process_run_name, interval=5):
        self.last_beat_time = None
        self.interval = interval
        self.is_alive = True
        self.id = uuid4().get_hex()[0:10]
        self._log_msg = LogMessage(process_name, process_run_name, self._get_empty_log_record())
    
    def _get_empty_log_record(self):
        log_record = LogRecord()
        log_record.created = ""
        log_record.filename = ""
        log_record.funcName = ""
        log_record.levelno = -1
        log_record.lineno = ""
        log_record.module = ""
        log_record.msg = ""
        log_record.name = ""
        log_record.msg_id = -1
        
        return log_record
    
    def get_beat_msg(self):
        """ Generates a heart beat message and updates the
        last_beat_time.
        """
        LOGGER.debug("Heart beat: %s", self.id)
        created = datetime.today()+UTC_OFFSET_TIMEDELTA 
        self._log_msg.log_record.created = created.strftime(LogRecord.date_time_format)
        self.last_beat_time = datetime.today()
        
        return self._log_msg.to_json()
    
    def need_to_beat(self):
        """ Returns true, if there was no heart beat message
        generated for more than 'interval' seconds.
        """
        if not self.is_alive:
            return False
        if self.last_beat_time == None:
            return True
        timespan = datetime.today() - self.last_beat_time
        timespan = timespan.seconds + timespan.days * 24 * 3600
        if timespan > self.interval:
            return True
        
        return False 
        

class ARabbitMQPublisher(object):
    def __init__(self, config):
        self.config = config
        self._message_number = 0
        self._stopping = False 
        self.is_ready = False  # True if can send messages, else False
        self.name = ""
        self.hearts = {}
    
    def publish_message(self, msg):
        raise Exception("Method not implemented")
        
    def run(self):
        raise Exception("Method not implemented")
    
    def stop(self):
        raise Exception("Method not implemented")
    
    def can_publish(self):
        return True
    
    def register_heart(self, heart):
        self.hearts[heart.id] = heart
        
    def unregister_heart(self, heart):
        if self.hearts.has_key(heart.id):
            self.hearts.pop(heart.id)
    
class SyncRabbitMQPublisher(ARabbitMQPublisher):
    
    def __init__(self, config):
        super(SyncRabbitMQPublisher, self).__init__(config)
        params = pika.URLParameters(self.config.amqp)
        
        self._connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
        self._channel = self._connection.channel()  # start a channel
        self._channel.queue_declare(queue=self.config.queue)  # Declare a queue
        self._properties = pika.BasicProperties(app_id=self.config.app_id,
                                                content_type=self.config.content_type,
                                                headers={},
                                                delivery_mode=self.config.delivery_mode)
    
    def publish_message(self, msg):
        self._publish_message_mq(msg)
    
    def _publish_message_mq(self, msg):
        self._message_number += 1
        self._channel.basic_publish(self.config.exchange, self.config.routing_key,
                                    msg,
                                    self._properties)
        
        LOGGER.debug('Published message # %i', self._message_number)
    
    def run(self):
        LOGGER.info("Publisher running")
    
    def stop(self):
        LOGGER.info('Stopping')
        self._connection.close()
        LOGGER.info('Stopped')
        
    @staticmethod
    def get_instance(config):
        return SyncRabbitMQPublisher(config)

class AsyncRabbitMQPublisher(ARabbitMQPublisher):
    """This is an example publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    It uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.
    """
    
    def __init__(self, config):
        """Setup the publisher publisher object, passing in the URL we will use
        to connect to RabbitMQ.

        :param str amqp_url: The URL for connecting to RabbitMQ

        """
        self._connection = None
        self._channel = None
        self._deliveries = {}
        self._acked = 0
        self._nacked = 0
        self._queue = Queue()
        self.lock = threading.RLock()
        # Set to true only once, when connected and can start to send messages. 
        # If it reconnects the looper should try and send until not stopping. 
        self.msg_looper_started = False;
        self._prev_ack_msg = 0
        self.require_confirmation = False
        super(AsyncRabbitMQPublisher, self).__init__(config)
    
    def can_publish(self):
        """Return true if can publish messages else false.
        
        is_ready - is true if delivery confirmation has been started,
        otherwise there might be some messages that will not be confirmed
        but consumed.
        """
        # This can still fail if another thread will close the connection when evaluating the second clause
        self.lock.acquire()
        try:
            if self._channel is None or not self._channel.is_open or not self.is_ready:
                return False
            else:
                return True
        except Exception:
            LOGGER.exception("Something went wrong")
        finally:
            self.lock.release()
        return False
    
    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika. If you want the reconnection to work, make
        sure you set stop_ioloop_on_close to False, which is not the default
        behavior of this adapter.

        :rtype: pika.SelectConnection

        """
        LOGGER.info('Connecting to %s', self.config.amqp)
        return pika.SelectConnection(pika.URLParameters(self.config.amqp),
                                     on_open_callback=self.on_connection_open,
                                     on_close_callback=self.on_connection_closed,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        LOGGER.info('Connection opened.')
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self.is_ready = False  # cannot send messages if no connection
        self.msg_looper_started = False
        self._channel = None
        if self._stopping:
            # https://github.com/pika/pika/issues/670
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self._connection.ioloop.stop)

    def open_channel(self):
        """This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.

        """
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.config.exchange)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self.is_ready = False
        self._channel = None
        if not self._stopping:
            LOGGER.warning('Channel was closed: (%s) %s', reply_code, reply_text)
            self._connection.close()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        LOGGER.info('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self.config.exchange_type,
                                       durable=self.config.durable_exchange)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        LOGGER.info('Exchange declared')
        self.setup_queue(self.config.queue)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        LOGGER.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(self.on_queue_declareok, queue_name,
                                    durable=self.config.durable_queue)

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        LOGGER.info('Binding %s to %s with %s',
                    self.config.exchange, self.config.queue, self.config.routing_key)
        self._channel.queue_bind(self.on_bindok, self.config.queue,
                                 self.config.exchange, self.config.routing_key)

    def on_bindok(self, unused_frame):
        """This method is invoked by pika when it receives the Queue.BindOk
        response from RabbitMQ. Since we know we're now setup and bound, it's
        time to start publishing."""
        LOGGER.info('Queue bound')
        self.start_publishing()        

    def start_publishing(self):
        """This method will enable delivery confirmations and schedule the
        first message to be sent to RabbitMQ

        """
        LOGGER.info('Issuing consumer related RPC commands')
        self.enable_delivery_confirmations()

        # this might be a restart, so it is not necessary to start the msg_looper
        if not self.msg_looper_started:
            self.msg_looper_started = True
            LOGGER.info("Entering the msg looper")
            self._msg_looper()

    def enable_delivery_confirmations(self):
        """Send the Confirm.Select RPC method to RabbitMQ to enable delivery
        confirmations on the channel. The only way to turn this off is to close
        the channel and create a new one.

        When the message is confirmed from RabbitMQ, the
        on_delivery_confirmation method will be invoked passing in a Basic.Ack
        or Basic.Nack method from RabbitMQ that will indicate which messages it
        is confirming or rejecting.

        """
        if self.require_confirmation:
            LOGGER.info('Issuing Confirm.Select RPC command')
            self._channel.confirm_delivery(self.on_delivery_confirmation)
        self.is_ready = True
    
    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        LOGGER.info('Received %s for delivery tag: %i, multiple: %s',
                    confirmation_type,
                    method_frame.method.delivery_tag,
                    method_frame.method.multiple)
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        if method_frame.method.multiple:
            for i in range(self._prev_ack_msg + 1, method_frame.method.delivery_tag):
                LOGGER.info('Deduced %s for delivery tag: %i',
                    confirmation_type, i)
                if self._deliveries.has_key(i):
                    self._deliveries.pop(i)
                else:
                    LOGGER.warning("Missing the key %s.", i)
                    
        if self._deliveries.has_key(method_frame.method.delivery_tag):
            self._deliveries.pop(method_frame.method.delivery_tag)
        else:
            LOGGER.warning("Missing the key %s, Multiple %s.",
                           method_frame.method.delivery_tag, method_frame.method.multiple)
        self._prev_ack_msg = method_frame.method.delivery_tag
        LOGGER.info('Published %i messages, %i have yet to be confirmed, '
                    '%i were acked and %i were nacked',
                    self._message_number, len(self._deliveries),
                    self._acked, self._nacked)

    def _publish_message_mq(self, msg):
        """If the class is not stopping, publish a message to RabbitMQ,
        appending a list of deliveries with the message number that was sent.
        This list will be used to check for delivery confirmations in the
        on_delivery_confirmations method.
        """
        # If the connection closes there will be an exception
        properties = pika.BasicProperties(app_id=self.config.app_id,
                                          content_type=self.config.content_type,
                                          headers={})
        
        # add the message to the dic before it gets sent
        # in case if the que is faster than the adding to the dict
        self._message_number += 1
        if self.require_confirmation:
            self._deliveries[self._message_number] = msg
        # print msg
        try:
            self._channel.basic_publish(self.config.exchange, self.config.routing_key,
                                        msg,
                                        properties)
            LOGGER.debug('Published message # %i', self._message_number)
        except Exception:
            if self.require_confirmation and self._deliveries.has_key(self._message_number):
                self._deliveries.pop(self._message_number)
            raise
    
    def publish_message(self, msg):
        LOGGER.debug("Adding msg to the queue: (%s)", self.name)
        self._queue.put(msg)
    
    def run(self):
        """Run the publisher code by connecting and then starting the IOLoop.
        """
        self.name = "Publisher Thread {0} {1}".format(threading.current_thread().name, threading.current_thread().ident)
        while not self._stopping:
            self._connection = None
            self._deliveries = {}
            self._acked = 0
            self._nacked = 0
            self._message_number = 0
            LOGGER.info("Publisher running")
            # This call might fail, and we have to retry to reconnect
            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
                LOGGER.info("Publisher finished")
            except ProbableAuthenticationError:
                LOGGER.warning("Probable authentication issues. Retrying in 2 second...")
            except IOError:
                LOGGER.warning("IOError occurred. Retrying in 2 second...")
            except Exception as ex:
                # Don't want to print the full stack trace
                LOGGER.error("Something went wrong '%s'. Retrying in 2 second...", ex)
            
            time.sleep(2)
            
        LOGGER.info('Stopped')
    
    def _msg_looper(self):
        while self.can_publish() and not self._queue.empty():
            msg = self._queue.get()
            try:
                self._publish_message_mq(msg)
            except Exception:
                self._queue.put(msg)
                # the publisher might get disconnected, and we don't want to display the exception.
                if self.can_publish():
                    LOGGER.exception("Failed to publish the msg.")
                else:
                    LOGGER.warning("Failed to publish the msg, probably disconnected. Will retry after reconnect.")
                # The exception might be the cause of a disconnect.
                # If not go to sleep, this can block the thread
                break
        if self.can_publish():
            for heart in self.hearts.values():
                LOGGER.debug("Checking heart beat for %s", heart.id)
                if heart.need_to_beat():
                    try:
                        self._publish_message_mq(heart.get_beat_msg())
                    except Exception:
                        LOGGER.debug("Failed to send heart beat.", exc_info=1)
                                
        # sleep only if no message in the queue or is not ready to process them
        if not self._stopping:
            self._connection.add_timeout(2, self._msg_looper)
        else:
            LOGGER.info("Msg looper has finished")
    
    def stop(self):
        """Stop the publisher by closing the channel and connection. We
        set a flag here so that we stop scheduling new messages to be
        published. The IOLoop is started because this method is
        invoked by the Try/Catch below when KeyboardInterrupt is caught.
        Starting the IOLoop again will allow the publisher to cleanly
        disconnect from RabbitMQ.

        """
        print "Stopping the publisher"  # just for user to see why it is still working
        LOGGER.info('Stopping.')
        max_wait_time = 20
        # give some time for the messages to be sent.
        while not self._queue.empty() and max_wait_time > 0:
            if max_wait_time < 10:
                LOGGER.warning("%s messages not sent.", self._queue.qsize())
            time.sleep(5)
            max_wait_time -= 5
        
        if not self._queue.empty():
            LOGGER.critical("%s messages not sent.", self._queue.qsize())
            
        max_wait_time = 20
        # give some time for the messages to be acked.
        while len(self._deliveries) > 0 and max_wait_time > 0:
            if max_wait_time < 10:
                LOGGER.warning("%s messages waiting to be acknowledged.", len(self._deliveries))
                for key, value in self._deliveries.iteritems():
                    LOGGER.warning("Not acked: %s: {%s}", key, value)
            time.sleep(5)
            max_wait_time -= 5
        
        # display the messages that were not acked. 
        if len(self._deliveries) > 0:
            LOGGER.critical("%s messages waiting to be acknowledged.", len(self._deliveries))
            for key, value in self._deliveries.iteritems():
                LOGGER.critical("Not acked: %s: {%s}", key, value)
            
        self._stopping = True
        LOGGER.info('Closing channel')
        self.close_channel()
        LOGGER.info('Closing connection')
        self.close_connection()
        LOGGER.info('Stopped')

    def close_channel(self):
        """Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.

        """
        if self._channel is not None and self._channel.is_open:
            LOGGER.info('Closing the channel')
            self._channel.close()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        if self._connection is not None and self._connection.is_open:
            LOGGER.info('Closing the connection')
            self._connection.close()

    @staticmethod
    def get_instance(config):
        return AsyncRabbitMQPublisher(config)

class RabbitMQPublisher(object):
    """This class provides the required methods to interact with the MQ publisher.
    It is responsible for the correct initialisation based on the provided parameters.
    There are two available publishers: async and sync.
    The Async publisher creates two additional threads: the RabbitMQ_Publisher and the RabbitMQ_Timeout.
    The RabbitMQ_Publisher thread hosts the comunication with the RabbitMQ.
    The RabbitMQ_Timeout thread makes sure that the publisher is stopped if no messages are published for a specified 
    time period (timeout). If the timeout is set to 0, the RabbitMQ_Timeout is not started. 
    """
    def __init__(self, config, is_async=True):
        self.was_started = False
        self.is_async = is_async
        if is_async:
            self.publisher = AsyncRabbitMQPublisher.get_instance(config)
            thr_publihser_name = "RabbitMQ_Publisher_{0}".format(time.time())
            self.thr = CustomThread(target=self._start_publisher, args=(), kwargs={}, name=thr_publihser_name, use_acm=USE_ACM_THREAD)
            thr_timeout_name = "RabbitMQ_Timeout{0}".format(time.time())
            self.thr_timeout = CustomThread(target=self._start_timeout, args=(), kwargs={}, name=thr_timeout_name, use_acm=USE_ACM_THREAD)
        else:
            self.publisher = SyncRabbitMQPublisher.get_instance(config)
            
        self.timeout = None
        self._current_timeout = 0
        self.stopping = False
            
    def _start_timeout(self):
        """Stops the publisher if no messages published 
        in the specified time interval (timeout).
        """
        if self.stopping:
            return
        
        if self._current_timeout > 0:
            time_to_sleep = self._current_timeout
            self._current_timeout = 0
            while time_to_sleep > 0 and not self.stopping:
                time.sleep(5)
                time_to_sleep -= 5
            self._start_timeout()
        else:
            LOGGER.info("Publisher timeout")
            self.stop()
            LOGGER.info("RabbitMQ timeout stopped")
        
    def _start_publisher(self):
        try:
            self.publisher.run()
        except Exception:
            LOGGER.exception("An exception occurred while starting the publisher.")
            
    def start(self):
        """Starts the publisher"""
        if self.is_async:
            if self.was_started:
                raise Exception("Trying to start the same publisher a second time.")
            self.was_started = True
            LOGGER.info("Starting publisher thread")
            self.thr.start()
            if self.timeout:
                self._current_timeout = self.timeout
                self.thr_timeout.start()
    
    def stop(self):
        """Stops the publisher."""
        self.stopping = True
        self.publisher.stop()
        LOGGER.info("Stopping publisher thread")
        if self.is_async:
            self.thr.join()
            LOGGER.info("RabbitMQ publisher stopped")
    
    def publish(self, msg):
        """Publish the specified message (MQMessage).
        Raises exception if the publisher is stopping.
        """
        self._current_timeout = self.timeout
        if self.stopping:
            raise Exception('Publisher already stopping.')
        try:
            self.publisher.publish_message(msg.to_json())
        except:
            LOGGER.exception("Failed to convert the message.")
        
            
class CustomThread(object):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, use_acm=False):
        self.use_acm = use_acm
        self.target = target
        self.is_started = False
        self.thr = None
        self.thr_acm = None
        if not self.use_acm:
            self.thr = threading.Thread(target=target, args=args, kwargs=kwargs, name=name)
        else:
            import acm
            self.thr_acm = acm.FThread()
            if name:
                self.thr_acm.Name(name)
        
    def start(self):
        if self.is_started:
            LOGGER.warning("Trying to start a thread that is already running.")
            return
        self.is_started = True
        if self.thr:
            self.thr.start()
        if self.thr_acm:
            self.thr_acm.Run(self.target, [])
    
    def join(self):
        if self.thr and self.thr.is_alive():
            self.thr.join()
        if self.thr_acm:
            while not self.thr_acm.IsTerminated():
                time.sleep(2)
