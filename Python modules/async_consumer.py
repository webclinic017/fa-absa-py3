'''
Created on 8 Jul 2016

@author: conicova
'''
import logging
import sys
import pika
from at_log_config import FAMQConfig

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
CONFIG = FAMQConfig.get_config("Playground")

class RbbitMQConsumer(object):
    """This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    """
    EXCHANGE_TYPE = 'fanout'

    def __init__(self, amqp_url, config, on_message_handler=None):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        :param str amqp_url: The AMQP url to connect with

        """
        self.config = config
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self.on_message_handler = on_message_handler

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """
        LOGGER.info("Connecting to: '%s'", self._url)
        return pika.SelectConnection(pika.URLParameters(self._url),
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        LOGGER.info('Connection opened')
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        LOGGER.info('Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:

            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

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
        LOGGER.info("Setting up the exchange: '%s'", self.config.exchange)
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

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        LOGGER.warning('Channel %i was closed: (%s) %s',
                       channel, reply_code, reply_text)
        self._connection.close()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        LOGGER.info("Declaring exchange '%s'", exchange_name)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self.EXCHANGE_TYPE,
                                       durable=self.config.durable_exchange)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        LOGGER.info("Exchange declared. Setting up the queue: '%s'", self.config.queue_dashboard)
        self.setup_queue(self.config.queue_dashboard)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        LOGGER.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(self.on_queue_declareok, queue_name)

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        LOGGER.info('Binding %s to %s with %s',
                    self.config.exchange, self.config.queue_dashboard, self.config.routing_key)
        self._channel.queue_bind(self.on_bindok, self.config.queue_dashboard,
                                 self.config.exchange, self.config.routing_key)

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        LOGGER.info('Queue bound')
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.config.queue_dashboard)
        #self._channel.basic_recover(self.on_message,self.config.queue_dashboard)

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, '')
        ack = False
        if self.on_message_handler:
            ack = self.on_message_handler(body)
        else:
            ack = True
        if ack:
            self.acknowledge_message(basic_deliver.delivery_tag)
        else:
            self.reject_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)
    
    def reject_message(self, delivery_tag):
        LOGGER.warning('Rejecting message %s', delivery_tag)
        self._channel.basic_reject(delivery_tag)
    
    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        LOGGER.info('RabbitMQ acknowledged the cancellation of the consumer')
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        LOGGER.info('Closing the channel')
        self._channel.close()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        LOGGER.info('Stopping')
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()
        LOGGER.info('Stopped')

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        LOGGER.info('Closing connection')
        self._connection.close()


class FALogStoretDb(object):
    
    TABLE_PREFIX = ''
    TABLE_LOG_PROCESS = "{0}LogProcess".format(TABLE_PREFIX)
    TABLE_LOG_PROCESS_RUN = "{0}LogProcessRun".format(TABLE_PREFIX)
    TABLE_LOG_SessionInfo = "{0}LogSessionInfo".format(TABLE_PREFIX)
    TABLE_LOG_Row = "{0}LogRow".format(TABLE_PREFIX)
    TABLE_LOG_Exception = "{0}LogException".format(TABLE_PREFIX)
    TABLE_LOG_Row_Txt = "{0}LogRowText".format(TABLE_PREFIX)
    
    STATUS_FINISHED = 3
    STATUS_RUNNING = 0
    
    def __init__(self, connection_string):
        import pyodbc
        super(FALogStoretDb, self).__init__()
        self.connection_string = connection_string
        self.cnxn = pyodbc.connect(self.connection_string)
        self.cursor = self.cnxn.cursor()
        self.processes_cache = {}
        self.process_run_cache = {}
        self.session_info_cache = {}
    
    def write(self, msg):
        process_id = self.get_process_id(msg.process_name)
        process_run_id = self._get_process_run_id(process_id, msg.process_run_name)
        if msg.log_record and msg.log_record.created:
            self.write_log_record_to_db(msg, process_run_id) 
        if len(msg.log_record.msg) > 350:
            self.write_log_record_txt_to_db(msg, process_run_id)
        
        if msg.session_info:
            session_info_id = self._get_session_info_id(process_run_id)
            if session_info_id == 0:
                self.write_log_session_info_to_db(msg, process_run_id)  
        
        if msg.log_exception and (msg.log_exception.exc_type or msg.log_exception.exc_value or msg.log_exception.exc_traceback):
            self._add_exception(msg, process_run_id)
        
        if msg.log_record and msg.log_record.msg == "Finished:{0}".format(msg.process_run_name):
            self._update_process_status(process_run_id, 3)
    
    def write_log_record_to_db(self, msg, process_run_id):
        sql_cmd = """INSERT INTO {0}
        ([ProcessRunId],[Created],[FileName],[FuncName],[LevelNumber],[LineNumber],[Module],[Msg],[Name],[MsgId]) 
        OUTPUT INSERTED.Id VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(FALogStoretDb.TABLE_LOG_Row)
        log_record = msg.log_record
        self.cursor.execute(sql_cmd,
                        (process_run_id, log_record.created, log_record.filename, log_record.funcName,
                         log_record.levelno, log_record.lineno, log_record.module, str(log_record.msg[0:350]), log_record.name,
                         log_record.msg_id))
        self.cnxn.commit()
        
    def write_log_record_txt_to_db(self, msg, process_run_id):
        sql_cmd = """INSERT INTO {0}
        ([ProcessRunId],[Msg],[MsgId]) 
        OUTPUT INSERTED.Id VALUES (?, ?, ?)""".format(FALogStoretDb.TABLE_LOG_Row_Txt)
        log_record = msg.log_record
        self.cursor.execute(sql_cmd,
                        (process_run_id, log_record.msg, log_record.msg_id))
        self.cnxn.commit()
    
    def write_log_session_info_to_db(self, msg, process_run_id):
        sql_cmd = """INSERT INTO {0}
        ([ProcessRunId],[ADSAddress],[User],[ACMClass],[Data],[Hostname],[PcUser],[DateToday],[InstanceName]) 
        OUTPUT INSERTED.Id VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(FALogStoretDb.TABLE_LOG_SessionInfo)
        session_info = msg.session_info
        self.cursor.execute(sql_cmd,
                        (process_run_id, session_info.ads_address, session_info.user, session_info.acm_class,
                         session_info.data, session_info.hostname, session_info.pc_user, session_info.date_today,
                         session_info.instance_name))
        self.cnxn.commit()
    
    def get_process_id(self, process_name, add_if_doesnt_exist=True):
        if self.processes_cache.has_key(process_name):
            return self.processes_cache[process_name]
        sql_cmd = "SELECT Id, ParentId from {0} WHERE Name=?".format(FALogStoretDb.TABLE_LOG_PROCESS)
        curr = self.cursor.execute(sql_cmd, (process_name))
        row = curr.fetchone()
        process_id = 0
        parent_id = 0
        if row:
            process_id = row[0]
            parent_id = row[1]
        else:
            if add_if_doesnt_exist:
                self._add_process(process_name)
                process_id = self.get_process_id(process_name, False)
        
        # TODO remove this from prod, this is just to fix existing processes
        if not parent_id and "." in process_name:
            parent_process = process_name.split(".")[:-1]
            parent_id = self.get_process_id(".".join(parent_process), True)
            self._update_process(process_name, process_id, parent_id)
        
        if process_id == 0:
            raise Exception("FALogStoretDb: Could not find the process id.")
        
        self.processes_cache[process_name] = process_id
        
        return process_id
    
    def _get_process_run_id(self, process_id, process_run_name, add_if_doesnt_exist=True):
        run_key = "{0}->{1}".format(process_id, process_run_name)
        if self.process_run_cache.has_key(run_key):
            return self.process_run_cache[run_key]
        sql_cmd = "SELECT Id from {0} WHERE RunName=? AND ProcessId=?".format(FALogStoretDb.TABLE_LOG_PROCESS_RUN)
        curr = self.cursor.execute(sql_cmd, (process_run_name, process_id))
        row = curr.fetchone()
        process_run_id = 0
        if row:
            process_run_id = row[0]
        else:
            if add_if_doesnt_exist:
                self._add_process_run_id(process_id, process_run_name)
                process_run_id = self._get_process_run_id(process_id, process_run_name, False)
        
        if process_run_id == 0:
            raise Exception("FALogStoretDb: Could not find the process run id.")
        
        self.process_run_cache[run_key] = process_run_id
        
        return process_run_id
    
    def _get_session_info_id(self, process_run_id):
        if self.session_info_cache.has_key(process_run_id):
            return self.session_info_cache[process_run_id]
        sql_cmd = "SELECT Id from {0} WHERE ProcessRunId=?".format(FALogStoretDb.TABLE_LOG_SessionInfo)
        curr = self.cursor.execute(sql_cmd, (process_run_id))
        row = curr.fetchone()
        session_info_id = 0
        if row:
            session_info_id = row[0]
            self.session_info_cache[process_run_id] = session_info_id
        
        return session_info_id
    
    def _add_process_run_id(self, process_id, process_run_name): 
        sql_cmd = "INSERT INTO {0}(ProcessId, RunName, Status) OUTPUT INSERTED.Id VALUES (?, ?, ?)".format(FALogStoretDb.TABLE_LOG_PROCESS_RUN)
        self.cursor.execute(sql_cmd, (process_id, process_run_name, FALogStoretDb.STATUS_RUNNING))
        self.cnxn.commit()
    
    def _add_process(self, process_name):
        process_tree = process_name.split(".")
        parent_id = 0
        if len(process_tree) > 1:
            parent_name = ""
            for item in process_tree[:-1]:
                if parent_name:
                    parent_name = "{0}.{1}".format(parent_name, item)
                else:
                    parent_name = item
                parent_id = self.get_process_id(parent_name, True)
        
        sql_cmd = "INSERT INTO {0}(Name, OutputDir, FileNameRegex, ParentId) VALUES (?,'','',?)".format(FALogStoretDb.TABLE_LOG_PROCESS)
        self.cursor.execute(sql_cmd, (process_name, parent_id))
        self.cnxn.commit()
    
    def _update_process_status(self, process_run_id, status):
        sql_cmd = "UPDATE {0} SET Status=? WHERE Id=?".format(FALogStoretDb.TABLE_LOG_PROCESS_RUN)
        self.cursor.execute(sql_cmd, (status, process_run_id))
        self.cnxn.commit()
    
    def _update_process(self, process_name, process_id, parent_id):
        sql_cmd = "UPDATE {0} SET Name=?, ParentId=? WHERE Id=?".format(FALogStoretDb.TABLE_LOG_PROCESS)
        self.cursor.execute(sql_cmd, (process_name, parent_id, process_id))
        self.cnxn.commit()
        
    def _add_exception(self, msg, process_run_id):
        sql_cmd = """INSERT INTO {0}
        ([ProcessRunId],[MsgId],[ExcType],[ExcValue],[ExcTraceback]) 
        OUTPUT INSERTED.Id VALUES 
        (?, ?, ?, ?, ?)""".format(FALogStoretDb.TABLE_LOG_Exception)
        log_record = msg.log_record
        log_exc = msg.log_exception
        self.cursor.execute(sql_cmd,
                        (process_run_id, log_record.msg_id, log_exc.exc_type, log_exc.exc_value, log_exc.exc_traceback))
        self.cnxn.commit()
    
    def close(self):
        for msg in self.data:
            self.write_to_db(msg)   
        
#         sql_cmd = "UPDATE {0} SET Status = ?, HashTagStatus = 0 WHERE Id = ?".format(FALogStoretDb.TABLE_LOG_PROCESS_RUN)
#         self.cursor.execute(sql_cmd, (FALogStoretDb.STATUS_FINISHED, self.process_run_id))
#         self.cnxn.commit() 
        
class MyConsumer(object):
    def __init__(self, config):
        self.db_log = FALogStoretDb(config.connection_string)
        self.consumer = RbbitMQConsumer(config.amqp, config, lambda body: self.on_message(body))
        
    def start(self):
        self.consumer.run()
        
    def stop(self):
        self.consumer.stop()
    
    def on_message(self, body):
        from at_log_message import LogMessage
        msg = LogMessage.from_json(body)
        try:
            self.db_log.write(msg)
        except Exception as ex:
            print(ex)
            # raise ex
            return False
        return True

def main():
    global CONFIG
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    environment = "Playground"
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == '--env':
            i += 1
            if i < len(sys.argv):
                environment = sys.argv[i]
        else:
            i += 1
    
    LOGGER.info("Environment: '%s'", environment)
    CONFIG = FAMQConfig.get_config(environment)
    consumer = MyConsumer(CONFIG)
    try:
        consumer.start()
    except KeyboardInterrupt:
        consumer.stop()


if __name__ == '__main__':
    main()
