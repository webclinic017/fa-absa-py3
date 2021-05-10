""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/FClipboard.py"
import sys
import ctypes.wintypes as wintypes
from contextlib import contextmanager
from ctypes import (string_at, 
                    windll, 
                    c_char_p, 
                    c_int, 
                    c_size_t, 
                    c_void_p, 
                    c_char_p, 
                    create_string_buffer, 
                    sizeof, 
                    cast, 
                    addressof)


GHND = 66

# FUNCTION HEADERS
OpenClipboard = windll.user32.OpenClipboard
OpenClipboard.argtypes = [wintypes.HWND]
OpenClipboard.restype = wintypes.BOOL

EmptyClipboard = windll.user32.EmptyClipboard

GetClipboardData = windll.user32.GetClipboardData
GetClipboardData.argtypes = [wintypes.UINT]
GetClipboardData.restype = wintypes.HANDLE

SetClipboardData = windll.user32.SetClipboardData
SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
SetClipboardData.restype = wintypes.HANDLE

CloseClipboard = windll.user32.CloseClipboard
CloseClipboard.argtypes = []

RegisterClipboardFormat = windll.user32.RegisterClipboardFormatA
RegisterClipboardFormat.argtypes = [wintypes.LPCSTR]
RegisterClipboardFormat.restype = wintypes.UINT

GlobalAlloc = windll.kernel32.GlobalAlloc
GlobalAlloc.argtypes = [wintypes.UINT, c_size_t]
GlobalAlloc.restype = wintypes.HGLOBAL

GlobalLock = windll.kernel32.GlobalLock
GlobalLock.argtypes = [wintypes.HGLOBAL]
GlobalLock.restype = c_void_p

GlobalUnlock = windll.kernel32.GlobalUnlock
GlobalUnlock.argtypes = [c_int]

_strncpy = windll.kernel32.lstrcpyn
_strncpy.restype = c_char_p
_strncpy.argtypes = [c_char_p, c_char_p, c_size_t]

# CLIPBOARD FORMATS
CF_TEXT = 1
CF_HTML = RegisterClipboardFormat('HTML Format')



def Paste(clipFormat=CF_TEXT):
    text = ""
    if OpenClipboard(0):
        hClipMem = GetClipboardData(clipFormat)
        if hClipMem:        
            text = string_at(GlobalLock(hClipMem))
            GlobalUnlock(hClipMem)
        CloseClipboard()
    return text

def Copy(text, clipFormat=CF_TEXT):
    buffer = create_string_buffer(text)
    bufferSize = sizeof(buffer)
    hGlobalMem = GlobalAlloc(GHND, c_size_t(bufferSize))
    lpGlobalMem = GlobalLock(hGlobalMem)
    _strncpy(cast(lpGlobalMem, c_char_p),
             cast(addressof(buffer), c_char_p),
             c_size_t(bufferSize))
    GlobalUnlock(c_int(hGlobalMem))
    if OpenClipboard(0):
        EmptyClipboard()
        SetClipboardData(clipFormat, hGlobalMem)
        CloseClipboard()
        
def ToClipboardData(text):
    buffer = create_string_buffer(text)
    bufferSize = sizeof(buffer)
    hGlobalMem = GlobalAlloc(GHND, c_size_t(bufferSize))
    lpGlobalMem = GlobalLock(hGlobalMem)
    _strncpy(cast(lpGlobalMem, c_char_p),
             cast(addressof(buffer), c_char_p),
             c_size_t(bufferSize))
    GlobalUnlock(c_int(hGlobalMem))
    return hGlobalMem
    
@contextmanager
def ClipboardHandler():
    if OpenClipboard(0):
        EmptyClipboard()
        yield
        CloseClipboard()
