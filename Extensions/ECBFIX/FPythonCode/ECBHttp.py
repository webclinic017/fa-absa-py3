from __future__ import print_function
import ctypes
import ctypes.wintypes
import os

# winhttp flags
WINHTTP_ACCESS_TYPE_NO_PROXY = 1
WINHTTP_NO_PROXY_NAME = 0
WINHTTP_NO_PROXY_BYPASS = 0
INTERNET_DEFAULT_HTTP_PORT = 80
WINHTTP_NO_REFERER = None
WINHTTP_DEFAULT_ACCEPT_TYPES = None
WINHTTP_AUTOPROXY_AUTO_DETECT = 0x00000001
WINHTTP_AUTOPROXY_CONFIG_URL = 0x00000002
WINHTTP_AUTO_DETECT_TYPE_DHCP = 0x00000001
WINHTTP_AUTO_DETECT_TYPE_DNS_A = 0x00000002
WINHTTP_OPTION_PROXY = 38
WINHTTP_NO_ADDITIONAL_HEADERS = None
WINHTTP_NO_REQUEST_DATA = None
WINHTTP_ACCESS_TYPE_NAMED_PROXY = 3


"""
typedef struct {
  DWORD   dwFlags;
  DWORD   dwAutoDetectFlags;
  LPCWSTR lpszAutoConfigUrl;
  LPVOID  lpvReserved;
  DWORD   dwReserved;
  BOOL    fAutoLogonIfChallenged;
} WINHTTP_AUTOPROXY_OPTIONS;
"""
class WINHTTP_AUTOPROXY_OPTIONS(ctypes.Structure):
    _fields_ = [("dwFlags", ctypes.wintypes.DWORD),
                ("dwAutoDetectFlags", ctypes.wintypes.DWORD),
                ("lpszAutoConfigUrl", ctypes.wintypes.LPCWSTR),
                ("lpvReserved", ctypes.c_void_p ),
                ("dwReserved", ctypes.wintypes.DWORD),
                ("fAutoLogonIfChallenged", ctypes.wintypes.BOOL),]

"""
struct WINHTTP_PROXY_INFO {
  DWORD  dwAccessType;
  LPWSTR lpszProxy;
  LPWSTR lpszProxyBypass;
};
"""
class WINHTTP_PROXY_INFO(ctypes.Structure):
    _fields_ = [("dwAccessType", ctypes.wintypes.DWORD),
                ("lpszProxy", ctypes.wintypes.LPCWSTR),
                ("lpszProxyBypass", ctypes.wintypes.LPCWSTR),]

'''
typedef struct {
  BOOL   fAutoDetect;
  LPWSTR lpszAutoConfigUrl;
  LPWSTR lpszProxy;
  LPWSTR lpszProxyBypass;
} WINHTTP_CURRENT_USER_IE_PROXY_CONFIG;
'''
class WINHTTP_CURRENT_USER_IE_PROXY_CONFIG(ctypes.Structure):
    _fields_ = [("fAutoDetect", ctypes.wintypes.BOOL),
                ("lpszAutoConfigUrl", ctypes.wintypes.LPWSTR),
                ("lpszProxy", ctypes.wintypes.LPWSTR),
                ("lpszProxyBypass", ctypes.wintypes.LPWSTR),]



'''
_GetProxyInfoAuto receives the proxy info either through the proxy URL or by
finding the proxy settings file through DHCP or DNS
'''
def _GetProxyInfoAuto(winHttp, url, hHttpSession, proxyUrl=None):
    AutoProxyOptions = WINHTTP_AUTOPROXY_OPTIONS()
    ProxyInfo = WINHTTP_PROXY_INFO()

    if proxyUrl:
        AutoProxyOptions.dwFlags = WINHTTP_AUTOPROXY_CONFIG_URL
        AutoProxyOptions.lpszAutoConfigUrl = proxyUrl
    else:
        AutoProxyOptions.dwFlags = WINHTTP_AUTOPROXY_AUTO_DETECT
        # Use DHCP and DNS-based auto-detection.
        AutoProxyOptions.dwAutoDetectFlags = WINHTTP_AUTO_DETECT_TYPE_DHCP|WINHTTP_AUTO_DETECT_TYPE_DNS_A

    AutoProxyOptions.fAutoLogonIfChallenged = True

    p_AutoProxyOptions = ctypes.pointer(AutoProxyOptions)
    p_ProxyInfo = ctypes.pointer(ProxyInfo)

    if not winHttp.WinHttpGetProxyForUrl(hHttpSession,
        url,
        p_AutoProxyOptions,
        p_ProxyInfo):
            return None
    return ProxyInfo

'''
    HTTPAutoProxyGetRequest makes a HTTP GET request with the proxy settings
    it gets from using the WPAD protocol. Function use the C library WinHttp.
    Supports NTLM which standard Python libraries does not provide.
'''
def HTTPAutoProxyGetRequest(userAgent, httpVersion, serverAddress, documentPath):
    if os.name != 'nt':
        print ("HTTPAutoProxyGetRequest is only supported on Windows")
        return None

    userAgent = userAgent.decode('utf-8')
    httpVersion = httpVersion.decode('utf-8')
    serverAddress = serverAddress.decode('utf-8')
    documentPath = documentPath.decode('utf-8')
    hRequest = None
    hConnect = None
    hHttpSession = None

    winHttp = ctypes.windll.LoadLibrary("Winhttp.dll")

    hHttpSession = winHttp.WinHttpOpen(userAgent,
        WINHTTP_ACCESS_TYPE_NO_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0)

    if hHttpSession == 0:
        _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
        print ('ERROR: Could not create an HTTP session')
        return None

    hConnect = winHttp.WinHttpConnect(hHttpSession, serverAddress, INTERNET_DEFAULT_HTTP_PORT, 0)

    if hConnect == 0:
        _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
        print ('ERROR: Could not create the connection handler')
        return None

    hRequest = winHttp.WinHttpOpenRequest(hConnect,
        u"GET",
        documentPath,
        httpVersion,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        0);

    if hRequest == 0:
        _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
        print ('ERROR: Could not create the HTTP request handler')
        return None

    url = u"http://" + serverAddress + u"/" + documentPath

    ProxyInfo = None
    autoProxy = False
    autoProxyUrl = None

    ieProxyConfig = WINHTTP_CURRENT_USER_IE_PROXY_CONFIG()
    if winHttp.WinHttpGetIEProxyConfigForCurrentUser(ctypes.pointer(ieProxyConfig)):
        if ieProxyConfig.fAutoDetect:
            autoProxy = True
        if ieProxyConfig.lpszAutoConfigUrl != None and ieProxyConfig.lpszAutoConfigUrl != "":
            autoProxy = True
            autoProxyUrl = ieProxyConfig.lpszAutoConfigUrl
    else:
        autoProxy = True

    # Get proxy info through auto proxy
    if autoProxy:
        ProxyInfo = _GetProxyInfoAuto(winHttp, url, hHttpSession, autoProxyUrl)
    else:
        if ieProxyConfig.lpszProxy != None and ieProxyConfig.lpszProxy != "":
            ProxyInfo = WINHTTP_PROXY_INFO()
            ProxyInfo.lpszProxy = ieProxyConfig.lpszProxy
            ProxyInfo.lpszProxyBypass = ieProxyConfig.lpszProxyBypass
            ProxyInfo.dwAccessType = WINHTTP_ACCESS_TYPE_NAMED_PROXY

    if ProxyInfo:
        p_ProxyInfo = ctypes.pointer(ProxyInfo)
        if not winHttp.WinHttpSetOption(hRequest, WINHTTP_OPTION_PROXY, p_ProxyInfo, ctypes.sizeof(ProxyInfo)):
            _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
            print ('ERROR: Could not setup the proxy settings')
            return None

    if not winHttp.WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, None):
        _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
        if ProxyInfo:
            print ('ERROR: Could not setup the request. The proxy settings gathered may be incorrect')
        else:
            print ('ERROR: Could not setup the request. No proxy could be found. Consider manual setup in case of existing proxy server')
        return None

    if not winHttp.WinHttpReceiveResponse(hRequest, None):
        _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
        print ('ERROR: Could not receive any response to the HTTP GET request')
        return None

    datasize = ctypes.wintypes.DWORD(0)
    downloaded = ctypes.wintypes.DWORD(0)
    p_datasize = ctypes.pointer(datasize)
    p_downloaded = ctypes.pointer(downloaded)

    data = ""

    while True:
        if not winHttp.WinHttpQueryDataAvailable(hRequest, p_datasize):
            _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
            print ('ERROR: Could not gather the data from the HTTP response')
            return None

        if datasize.value == 0:
            break

        readBuffer = ctypes.create_string_buffer(datasize.value+1)

        if not winHttp.WinHttpReadData(hRequest, readBuffer, datasize, p_downloaded):
            _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)
            print ('ERROR: Could not read the data from the HTTP response')
            return None

        data += readBuffer.value

    _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession)

    return data

def _HttpCleanUp(winHttp, hRequest, hConnect, hHttpSession):
    if hRequest != 0 or hRequest == None:
        winHttp.WinHttpCloseHandle(hRequest)
    if hConnect != 0 or hConnect == None:
        winHttp.WinHttpCloseHandle(hConnect)
    if hHttpSession != 0 or hHttpSession == None:
        winHttp.WinHttpCloseHandle(hHttpSession)


