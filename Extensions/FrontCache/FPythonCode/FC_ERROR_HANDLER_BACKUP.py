
import smtplib
from MimeWriter import MimeWriter
try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

FROM_ADDRESS = 'siyao.liu@barclayscapital.com'

TO_ADDRESSES = ['siyao.liu@barclayscapital.com']

SUBJECT = 'FRONT CACHE CRITICAL ERROR'

COMMASPACE = ', '

def handelError(TEXT, exception, traceback):
    tempfile = StringIO()
    mw = MimeWriter(tempfile)
    mw.addheader('to', COMMASPACE.join(TO_ADDRESSES))
    mw.addheader('from', FROM_ADDRESS)
    subj = SUBJECT
    mw.addheader('subject', SUBJECT)
    body = mw.startbody('text/plain')
    body.write('Text Message:\n\n')
    body.write(TEXT)
    body.write('\n\n')
    if exception:
        body.write('Exception:')
        body.write('\n\n')
        body.write(str(exception))
        body.write('\n\n')
    if traceback:
        body.write('Traceback:')
        body.write('\n\n')
        body.write(traceback.format_exc())
        body.write('\n\n')
    
    message = tempfile.getvalue()

    smtp = smtplib.SMTP('smtphost.bzwint.com')
    smtp.sendmail(FROM_ADDRESS, TO_ADDRESSES, message)
    smtp.quit()
    print('Email Sent')
