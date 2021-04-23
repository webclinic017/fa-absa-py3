""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FFileTransporter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFileTransporter - File transporter methods for Asset Management integrations

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import collections
import os
import time

import FAssetManagementUtils
import FBusinessProcessUtils

logger = FAssetManagementUtils.GetLogger()


class FFileExporter(object):
    """An engine for the transfer of export files to remote parties.

    Given an export process and pre-generated files containing exportable elements, this
    engine is responsible for delivering the files to the remote parties and updating the
    export-based business processes to reflect the success state of the transfer.

    """
    def __init__(self, exportProcess):
        self._exportProcess = exportProcess

    def Execute(self, retries=0, retryDelay=1):
        """Export all files in the export process.

        The method of transfer used is determined by a callback for each export file
        defined by the export processes' integration. This callback may optionally provide
        a collection of FFileTransfer instances to send the file to multiple recipients.

        Files defined by the export process must have been generated prior to performing
        this export process. If a number of retries is provided, each file transfer will be
        re-attempted on failure after retryDelay seconds.

        """
        if not self._exportProcess.TestMode().IsFileTransferEnabled():
            if not self._exportProcess.TestMode().IsEnabled():
                for singleExport in self._exportProcess.SingleExportsAsList():
                    if singleExport.IsExportable() and not self._exportProcess.GenerateEmptyFile():
                        self._SetBusinessProcessesExported(singleExport.ExportableBusinessProcesses())
            logger.info('Skipping transferring of file(s).')
            return
        for singleExport in self._exportProcess.SingleExportsAsList():
            sheetTemplateId = singleExport.SheetTemplateId()
            if not singleExport.IsExportable() and not self._exportProcess.GenerateEmptyFile():
                continue
            try:
                fileTransfers = self._exportProcess.Integration().FileTransferFinderFunction()(singleExport.SingleExportIdentifier())
                if not isinstance(fileTransfers, collections.Iterable):
                    fileTransfers = [fileTransfers, ]
            except Exception as e:
                msg = 'Failed to get a file transporter for export ''%s'': %s' % (sheetTemplateId, e)
                logger.error(msg)
                singleExport.Failed(msg)
            else:
                sourceFile = os.path.join(singleExport.FilePath(), singleExport.Filename())

                try:
                    for ft in fileTransfers:
                        self._ExportFile(ft, sourceFile, retries, retryDelay)
                    self._SetBusinessProcessesExported(singleExport.ExportableBusinessProcesses())
                except (FFileTransfer.TransferError, ImportError, ValueError) as e:
                    msg = 'Failed to transfer export file ''%s'': %s' % (sourceFile, str(e))
                    logger.error(msg)
                    singleExport.Failed(msg)

    def ExportProcess(self):
        return self._exportProcess

    @staticmethod
    def _ExportFile(fileTransfer, sourceFileName, retries, retryDelay):
        fileTransfer.SendWithRetries(sourceFileName, retries, retryDelay)
        logger.info('Successfully exported file ''%s''.', sourceFileName)

    def _SetBusinessProcessesExported(self, businessProcesses):
        count = len(businessProcesses)
        exportEvent = self._exportProcess.Integration().ExportEventId()
        if self._exportProcess.TestMode().IsEnabled():
            logger.info('[TEST MODE] Business processes would have transitioned with event "%s".', exportEvent)
            return
        for bp in businessProcesses:
            try:
                # Revalidate that the business process is still in the required state for an export
                if FBusinessProcessUtils.IsValidEvent(bp, exportEvent):
                    bp.HandleEvent(exportEvent)
                    bp.Commit()
                else:
                    logger.error('Business process %d does not support export event "%s" (current state="%s").',
                            bp.Oid(), exportEvent, bp.CurrentStep().State().Name())
                    count -= 1
            except RuntimeError as e:
                logger.error('Business process %d failed to handle event "%s": %s', bp.Oid(), exportEvent, e)
                count -= 1
        if count > 0:
            logger.info('Updated %d business process%s as having successfully exported.',
                    count, 'es' if count > 1 else '')


class FFileTransfer(object):
    """A base class for the transfer of a local file to a (possibly remote) destination."""

    class TransferError(Exception):
        """Exception class for all file transfer errors."""
        pass

    def Send(self, sourceFileName):
        """Attempt to send the source file to the specified destination. The transfer method
        used will depend on the selected base class.

        """
        raise NotImplementedError('Base class does not support file transfer')

    def SendWithRetries(self, sourceFileName, retries=3, retryDelay=5):
        """Send the file over a number of retries. If all retries are exhausted, a
        TransferError exception is raised.

        """
        assert(retries >= 0 and retryDelay >= 0)
        attempt = 1
        while True:
            try:
                self.Send(sourceFileName)
            except FFileTransfer.TransferError as e:
                if attempt >= retries:
                    if retries > 0:
                        logger.error('Transfer failed after %d attempt(s), aborting.', retries)
                    raise
                logger.warn('Failed to transfer file: %s', e)
                logger.info('Waiting %d second(s) before retrying transfer (attempt %d of %d)',
                        retryDelay, attempt, retries)
                time.sleep(retryDelay)
                attempt += 1
            else:
                break

    @staticmethod
    def _ValidateSourceFile(sourceFileName):
        if not os.path.exists(sourceFileName):
            raise ValueError('Source file to transfer "' + sourceFileName + '" does not exist.')
        if os.path.getsize(sourceFileName) == 0:
            raise ValueError('Source file to transfer "' + sourceFileName + '" is empty.')


class FFileSystemTransfer(FFileTransfer):
    """Represents the transfer of a file on the local file system."""

    def __init__(self, destinationPath, overwriteExistingFiles=False, keepSourceFile=True):
        super(FFileSystemTransfer, self).__init__()
        self._destinationPath = destinationPath
        self._overwriteExistingFiles = overwriteExistingFiles
        self._keepSourceFile = keepSourceFile

    def Send(self, sourceFileName):
        import shutil
        self._ValidateSourceFile(sourceFileName)
        try:
            self._ValidateDestinationPath(self._destinationPath)
            destination_file = os.path.join(self._destinationPath, os.path.basename(sourceFileName))
            if not self._overwriteExistingFiles:
                destination_file = self._GetUniqueFilename(destination_file)
            transfer_file_func = shutil.copy2 if self._keepSourceFile else shutil.move

            logger.info('%s file ''%s'' to ''%s''.', 'Copying' if self._keepSourceFile else 'Moving',
                    sourceFileName, destination_file)
            transfer_file_func(sourceFileName, destination_file)
        except IOError as e:
            raise FFileTransfer.TransferError(e)

    @staticmethod
    def _ValidateDestinationPath(path):
        if not os.path.lexists(path):
            os.makedirs(path)

    @staticmethod
    def _GetUniqueFilename(filename):
        count = 1
        base, ext = os.path.splitext(filename)
        while os.path.lexists(filename):
            filename = base + '_' + str(count) + ext
            count += 1
        return filename


class FFTPTransfer(FFileTransfer):
    """Represents the transfer of a file to a remote FTP server."""

    class FTPServer(object):
        """Stores FTP server details."""
        def __init__(self, hostname, port=21, username='anonymous', password='anonymous@', path=''):
            self.hostname = hostname
            self.port = port or 21
            self.username = username
            self.password = password
            self.path = path or ''

        @classmethod
        def createFromPartyOrContact(cls, obj):
            """Given an FParty or FContact object, return an FTPServer instance with party/contact's
            FTP server details.

            This function is dependent on the following AdditionalInfo attributes being defined for
            the party/contact:
                'FTP Hostname', 'FTP Port', 'FTP Username', 'FTP Password' & 'FTP Path'

            """
            ai = obj.AdditionalInfo()
            return cls(hostname=ai.FTP_Hostname(), port=ai.FTP_Port(), username=ai.FTP_Username(),
                    password=ai.FTP_Password(), path=ai.FTP_Path())

    def __init__(self, server):
        super(FFTPTransfer, self).__init__()
        self._ValidateFTPServer(server)
        self._server = server

    def Server(self, server):
        if server is None:
            return self._server
        self._ValidateFTPServer(server)
        self._server = server

    def Send(self, sourceFileName):
        import ftplib
        self._ValidateSourceFile(sourceFileName)
        try:
            logger.info('Sending ''%s'' to %s:%i%s via FTP.', sourceFileName, self._server.hostname,
                    self._server.port, self._server.path)

            ftp = ftplib.FTP()
            ftp.connect(self._server.hostname, self._server.port)
            ftp.login(self._server.username, self._server.password)
            ftp.cwd(self._server.path)
            with open(sourceFileName, 'rb') as f:
                ftp.storbinary('STOR ' + os.path.basename(sourceFileName), f, 1024)
            ftp.close()
        except ftplib.all_errors as e:
            raise FFileTransfer.TransferError(e)

    @staticmethod
    def _ValidateFTPServer(server):
        if (not server or
            server.hostname is None or
            not isinstance(server.port, int) or
            server.path is None):
            raise ValueError('Invalid FTP server: ' + str(vars(server)))


class FSFTPTransfer(FFTPTransfer):
    """Represents the transfer of a file to a remote SFTP server.

    NOTE: This class has a dependency on the 3rd Party Python module 'paramiko'
          for SFTP functionality (see http://www.lag.net/paramiko/).

    """
    def __init__(self, server):
        super(FSFTPTransfer, self).__init__(server)

    def Send(self, sourceFileName):
        import paramiko
        self._ValidateSourceFile(sourceFileName)
        try:
            logger.info('Sending ''%s'' to %s:%i%s via SFTP.', sourceFileName, self._server.hostname,
                    self._server.port, self._server.path)

            transport = paramiko.Transport((self._server.hostname, self._server.port))
            transport.connect(username = self._server.username, password = self._server.password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            destinationFileName = os.path.basename(sourceFileName)
            if self._server.path != "":
                sftp.chdir(self._server.path)
            self._TransferFile(sftp, sourceFileName, destinationFileName)
            sftp.close()
            transport.close()
        except (paramiko.SSHException, paramiko.SFTPError, IOError) as e:
            raise FFileTransfer.TransferError(e)

    @staticmethod
    def _TransferFile(sftp, sourceFileName, remoteFileName):
        # This is a reimplementation of the built-in 'put' method in paramiko, without the subsequent
        # local-remote file size check after transfer. This check has been seen to have failed on some
        # SFTP servers, despite the transfer being successful.
        with file(sourceFileName, 'rb') as local:
            remote = sftp.file(remoteFileName, 'wb')
            try:
                remote.set_pipelined(True)
                while True:
                    data = local.read(32768)
                    if len(data) == 0:
                        break
                    remote.write(data)
            finally:
                remote.close()


class FEmailTransfer(FFileTransfer):
    """Represents the transfer of a file as an attachment in an email message."""

    class SMTPServer(object):
        """Stores SMTP server details."""
        def __init__(self, hostname, port=25, username=None, password=None, tls_mode=False):
            self.hostname = hostname
            self.port = port
            self.username = username
            self.password = password
            self.tls_mode = tls_mode

    class Message(object):
        """Stores common email message details."""
        def __init__(self, recipients, subject, sender = 'Front Arena', body = ''):
            self.recipients = recipients
            self.subject = subject
            self.sender = sender
            self.body = body

    def __init__(self, server, message):
        super(FEmailTransfer, self).__init__()
        self._ValidateSMTPServer(server)
        self._server = server
        self._ValidateMessage(message)
        self._message = message
        if not isinstance(self._message.recipients, collections.Iterable):
            self._message.recipients = [self._message.recipients, ]

    def Send(self, sourceFileName):
        import smtplib
        self._ValidateSourceFile(sourceFileName)
        try:
            logger.info('Emailing ''%s'' to %s via SMTP server %s.', sourceFileName,
                    self._message.recipients, self._server.hostname)

            server = smtplib.SMTP()
            server.connect(self._server.hostname, self._server.port)
            if self._server.tls_mode:
                server.starttls()
            if self._server.username:
                server.login(self._server.username, self._server.password)
            server.verify(self._message.recipients)
            msg = self._GetEmailMessage(self._message.recipients, self._message, sourceFileName)
            server.sendmail(self._message.sender, self._message.recipients, msg.as_string())
            server.quit()
        except (smtplib.SMTPException, smtplib.socket.error, IOError) as e:
            raise FFileTransfer.TransferError(e)

    @staticmethod
    def _ValidateSMTPServer(server):
        if (not server or
            server.hostname is None or
            not isinstance(server.port, int)):
            raise ValueError('Invalid SMTP server: ' + str(vars(server)))

    @staticmethod
    def _ValidateMessage(message):
        if (not message or
            message.recipients is None or
            message.sender is None):
            raise ValueError('Invalid email message: ' + str(vars(message)))

    @classmethod
    def _GetEmailMessage(cls, recipients, message, filename=None):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart()
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = message.subject
        msg['From'] = message.sender
        msg.attach(MIMEText(message.body, 'plain'))
        if filename:
            msg.attach(cls._GetEmailAttachment(filename))
        return msg

    @classmethod
    def _GetEmailAttachment(cls, filename):
        import mimetypes
        ctype, encoding = mimetypes.guess_type(filename)
        if not ctype or not encoding:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            from email.mime.text import MIMEText
            with open(filename) as f:
                attachment = MIMEText(f.read(), _subtype = subtype)
        else:
            from email.mime.base import MIMEBase
            from email import encoders
            attachment = MIMEBase(maintype, subtype)
            with open(filename, 'rb') as f:
                attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment',
                filename=os.path.basename(filename))
        return attachment
