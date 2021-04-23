'''================================================================================================
================================================================================================'''
import acm
import time
import smtplib
CheckedTrades = acm.FDictionary()  #trades that have laready been checked for the day
'''================================================================================================
================================================================================================'''
class Gmail(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'SMTPRELAY.barcapint.com'
        self.port = 587
        self.session = None
        
        try:
            self.session = smtplib.SMTP(self.server) #, self.port)        
            #self.session.ehlo()
            #self.session.starttls()
            #self.session.ehlo
            #self.session.login(self.email, self.password)
        except:
            self.session = None
            print 'Failed to connect to email server'            

    def send_message(self, toemail, subject, body):
    
        if self.session != None:
            headers = [
                "From: PRIME client",
                "Subject: " + subject,
                "To: " + toemail]
                #"MIME-Version: 1.0",
                #"Content-Type: text/html"]
            headers = "\r\n".join(headers)
            self.session.sendmail(self.email, toemail, headers + "\r\n\r\n" + body)    
        else:
            print 'Error sending email , not connected to email server'            
'''================================================================================================
================================================================================================'''
gm = Gmail('SungardDemo123@gmail.com', 'Holistic1')
'''================================================================================================
================================================================================================'''
def send_mail(TO, SUBJECT, MSG):
    try:
        thread = acm.FThread()
        thread.Run(gm.send_message, [TO, SUBJECT, MSG])
    except:
        print 'Failed to send email'
'''================================================================================================
Enhance template
    -what other fields
        *Aquirer
        *Trade Time
        *Date
        *from System
        *Portfolio
================================================================================================'''
def create_message(trade, user):

    CounterPartyName = 'None'
    if trade.Counterparty() != None:
        CounterPartyName = trade.Counterparty().Name()
    
    Template =\
    """
    NOTIFICATION of trade exceeding 5M USD
    --------------------------------------
    Trade Number   = %d
    Currency Pair  = %s 
    %s             = %d 
    %s             = %d
    Price          = %f    
    ValueDay       = %s 
    Counterparty   = %s 
    USD Equivelent = %d
    Trader         = %s
    User           = %s   
    Status         = %s 
    """\
    \
    %(\
    trade.Oid(),\
    trade.CurrencyPair().Name(),\
    trade.Instrument().Name(), trade.Quantity(),\
    trade.Currency().Name(), trade.Premium(),\
    trade.Price(),\
    trade.ValueDay(),\
    CounterPartyName,\
    trade.BaseCostDirty(),\
    trade.Trader().Name(),\
    user.Name(),\
    trade.Status()\
    )                               
    return Template
'''================================================================================================
================================================================================================'''
def trade(trade):

    trade = acm.Ael.AelToFObject(trade)
    if abs(trade.BaseCostDirty() > 5000000):

        msg = create_message(trade, acm.User())
        module = acm.FExtensionModule[acm.User().Name()]
        
        if module != None:
            extension = module.GetExtension('FParameters', 'FObject', 'FXUserParams')
            if extension == None:
                return

            params = extension.Value()
            email_yes = str(params.At('ltn_email'))
            if str(email_yes) == 'yes':
                Principle = acm.FPrincipalUser.Select01("type = 'Custom 1'  and user = '%s'" % acm.User().Name(), '')
                if Principle != None:
                    print 'Sending email notification for trade ' + str(trade.Oid())
                    send_mail(Principle.Principal(), 'LARGE TRADE NOTIFICATION', msg)
                else:
                    print "No Custom 1 Principal found for user %s" %  acm.User().Name()
        else:
            print "No module for user %s" %  acm.User().Name()
'''================================================================================================
================================================================================================'''
def work():

    global CheckedTrades
    #time.sleep(5) #not necesssary for this ATS to do so much work
    User_List = acm.FUserGroup['FO FX Trader'].Users()

    date  = acm.Time.DateToday()
    if not CheckedTrades.HasKey(date):
        CheckedTrades.Clear()
        CheckedTrades[date] = acm.FArray() 

    for trade in acm.FStoredASQLQuery.Select01('name = PACEover5m_today', '').Query().Select():
        if not CheckedTrades[date].Includes(trade.Oid()):
            CheckedTrades[date].Add(trade.Oid())
                       
            for User in User_List:

                acm.PollDbEvents()
                msg = create_message(trade, User)
                module = acm.FExtensionModule[User.Name()]

                if module != None:
                    extension = module.GetExtension('FParameters', 'FObject', 'FXUserParams')
                    if extension == None:
                        return
                    
                    params = extension.Value()
                    email_yes = str(params.At('ltn_email'))
                    
                    if str(email_yes) == 'yes':
                        Principle = acm.FPrincipalUser.Select01("type = 'Custom 1'  and user = '%s'" % User.Name(), '')
                        if Principle != None:
                            print 'Sending email notification for trade ' + str(trade.Oid())
                            send_mail(Principle.Principal(), 'LARGE TRADE NOTIFICATION', msg)
                        else:
                            print "No Custom 1 Principal found for user %s" %  User.Name()
                else:
                    print "No module for user %s" %  User.Name()
                
'''================================================================================================
================================================================================================'''
def start(): 
    print """Starting Large Trade Notification ATS >>""" 
    return
def stop(): return
def status(): return
'''================================================================================================
setup smtp.vbs

Const cdoSendUsingPickup = 1 'Send message using the local SMTP service pickup directory. 
Const cdoSendUsingPort = 2 'Send the message using the network (SMTP over the network). 

Const cdoAnonymous = 0 'Do not authenticate
Const cdoBasic = 1 'basic (clear-text) authentication
Const cdoNTLM = 2 'NTLM

dim objEmail
    Set objEmail = CreateObject("CDO.Message") 
objEmail.Configuration.Fields.Item ("http://schemas.microsoft.com/cdo/configuration/sendusing")= cdoSendUsingPort 
'Name or IP of remote SMTP server
objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserver") ="SMTPRELAY.barcapint.com"
'Server port
objEmail.Configuration.Fields.Item ("http://schemas.microsoft.com/cdo/configuration/smtpserverport") =25 

objEmail.Configuration.Fields.Item ("http://schemas.microsoft.com/cdo/configuration/smtpAuthenticate") = cdoNTLM 
'objEmail.Configuration.Fields.Item ("http://schemas.microsoft.com/cdo/configuration/NNTPAccountName") = "USERNAME"
'objEmail.Configuration.Fields.Item ("http://schemas.microsoft.com/cdo/configuration/SaveSentItems") = TRUE

objEmail.Configuration.Fields.Update
================================================================================================'''

'''================================================================================================
test smtp.vbs

objEmail.From = "test@CZAPBCC1APP002A.com"
    objEmail.To = "eduan.erasmus@absacapital.com;shaun.steyn@absacapital.com"
    objEmail.Subject = "test"
    objEmail.Textbody = "nothing " 
    objEmail.Send
================================================================================================'''
