from __future__ import print_function
""" 
    Script for downloading ECBFIX FX rates. 
    This module contains code for connecting to a webpage through a 
    proxy and both read and receive the xml file at a given address.
    It is possible to use any proxy except NTLM proxies.
                                                                        """
import urllib, socket, base64, time, httplib, ssl
from xml.dom import minidom
import acm

def GetProxyConnection(SSL, proxy, proxy_cred = None):
    """ A function that tries to connect to the specified 
        SSL webpage through the specified proxy. The proxy
        cannot be NTLM, since it is not possible to enter 
        authorization credentials in python with a NTLM proxy. """
    try:    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print (e)
        return None
        
    try:
        s.connect(proxy)#('10.254.67.4', 8080))
        print ('Socket established.')
    except socket.error as e:
        print ('Socket could not be established', e)
        return None
    
    proxy_authorization = "\r\n"
    if proxy_cred:
        user_pass = base64.encodestring(proxy_cred[0] + ':' + proxy_cred[1])
        proxy_authorization = 'Proxy-authorization: Basic ' + user_pass + '\r\n'
    connectMessage = "CONNECT %s:%s HTTP/1.0\r\n" % ( SSL[0], SSL[1]) + proxy_authorization 
    
    try:                 
        s.send(connectMessage)
        print ('Sent CONNECT message to proxy server connecting to SSL URL.')
    except socket.error as e:
        print ("Error sending CONNECT message to %s:%s %s"%( SSL[0], SSL[1], str(e)))
        return None

    try:
        buf = ''
        count  = 0
        start = time.time()
        while not buf.endswith('\r\n\r\n'):
            buf += s.recv(1)
            count += 1
            buf = buf[-1024:]
            if count > 10**7:
                raise RuntimeError("Recieved garbage from proxy.") 
            if time.time() - start > 60*5:
                raise RuntimeError("Timeout while recieving proxy response.")
        print ("Proxy response: ", (buf))
    except socket.error as e:
        print ("Error receiving data from URL:", str(e))
        return None
    except RuntimeError as e:
        print ("Error receiving data from URL:", str(e))
        return None

    try:
        sock = ssl.wrap_socket(s)
        print ('Proxy Connection installed')
    except Exception as e:
        print ("Error initiating SSL connection:", str(e))
        return None
        
    h = httplib.HTTPSConnection( SSL[0])#, SSL[1])
    h.sock = sock
    
    return h
    
def GetXMLFile( SSL, webAddress, proxy, proxy_cred=None ):
    """ Function that gets the proxy connection to the given
        SSL URL and then sends a request to get the xml file
        specified as webAddress. The function returns the 
        response from the SSL URL, and if the request was
        successful return value is the xml file as a string. """
    h = GetProxyConnection( SSL, proxy, proxy_cred)
    if not h:
        return None
        
    params = urllib.urlencode({'1':1})
    h.putrequest( "POST", webAddress)
    h.putheader( "Content-Type", "application/x-www-form-urlencoded" )
    h.putheader( "Content-Length", str( len(params)))
    h.endheaders()
    
    h.send(params)
    
    res = h.getresponse()
    return res.read()

def ReadXMLFile(xmlStr):
    """ Function that reads the given xml string and returns
        a tuple. The tuple contains the date for the fx rates
        and an array with tuples where the first object is the
        currency name and the second is the fx rate. """
    fxDict = acm.FDictionary()
    doc = minidom.parseString(xmlStr)
    
    for node in doc.getElementsByTagName('Cube'):
        if node.hasAttribute('time'):
            fxArray = acm.FArray()
            day = node.getAttribute('time')
            for fxNode in node.childNodes:
                if fxNode.nodeName == 'Cube': #Fx node
                    fxArray.Add(((str(fxNode.getAttribute('currency')), float(fxNode.getAttribute('rate')))))
            fxDict.AtPut(day, fxArray)
    return fxDict

def StartDownload(SSL, webAddr, proxy_addr, proxy_cred = None):
    """ Function that connects to the SSL address given through
        the given proxy and then returns the xml file at the 
        given web address as a string. """
    return GetXMLFile( SSL, webAddr, proxy_addr, proxy_cred )

def LoadFromFile(address):
    try:
        doc = minidom.parse(address).toxml()
    except Exception as e:
        print (e)
        doc = None
    return doc

