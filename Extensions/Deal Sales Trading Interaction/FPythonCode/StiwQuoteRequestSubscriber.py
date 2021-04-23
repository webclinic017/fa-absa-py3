
import acm
import clr
Media = clr.System.Media
SystemSounds = Media.SystemSounds

SOUND_ON_NEW_QUOTE = True
SOUND_ON_QUOTE_UPDATE = True
UPDATE_QUOTE_REQUEST_SOUND = "C:\Windows\Media\Windows Notify.wav"
NEW_QUOTE_REQUEST_SOUND = "C:\Windows\Media\Windows Notify.wav"

FLASH_WINDOW_ON_NEW_QUOTE = True
FLASH_WINDOW_ON_QUOTE_UPDATE = True

class ProxyFilter(object):
    def IsSatisfiedBy(self, *args):
        return True

class NotifyUserHelper(object):
    def __init__(self, owner):
        self._owner = owner
        
    def __NotifyWithSound(self, sound):
        try:
            Media.SoundPlayer(sound).Play()
        except:
            SystemSounds.Exclamation.Play()        
            
    def __NotifyWithFlashingWindow(self):
        try:
            self._owner.Flash('EnableAndAutoDisableOnActivate')
        except Exception as e:
            print(('__NotifyWithFlashingWindow failed', e)) 

    def Destroyed(self):
        destroyed = False
        try:
            self._owner.CurrentObject()
        except:
            destroyed = True
        return destroyed

    def NewEvent(self):
        if not self.Destroyed():
            if SOUND_ON_NEW_QUOTE:
                self.__NotifyWithSound(NEW_QUOTE_REQUEST_SOUND)        
            if FLASH_WINDOW_ON_NEW_QUOTE:
                self.__NotifyWithFlashingWindow()
            
    def UpdateEvent(self):
        if not self.Destroyed():
            if SOUND_ON_QUOTE_UPDATE:
                self.__NotifyWithSound(UPDATE_QUOTE_REQUEST_SOUND)        
            if FLASH_WINDOW_ON_QUOTE_UPDATE:
                self.__NotifyWithFlashingWindow()

class QuoteRequestSubscriber(object):
    def __init__(self, owner, filterQueryCB=None, filterStatusCB=None):
        self._quoteRequests = None
        self._filterQueryCB = filterQueryCB if filterQueryCB else ProxyFilter()
        self._filterStatusCB = filterStatusCB
        self._notify = NotifyUserHelper(owner)
        self._enabled = False
        self.__GetQuoteRequests()
        
    def __del__(self):
        self.__Unsubscribe()
        
    def __GetQuoteRequests(self):
        self._quoteRequests = acm.Trading().GetQuoteRequests()
    
    def __Notify(self):
        return self._notify
        
    def __Subscribe(self):
        self._quoteRequests.AddDependent(self)    

    def __Unsubscribe(self):
        self._quoteRequests.RemoveDependent(self)
      
    def __NotifyOnNewQuoteRequest(self, quoteRequest):
        return self._filterStatusCB(quoteRequest, 'insert') if self._filterStatusCB else quoteRequest

    def __NotifyOnQuoteRequestUpdate(self, quoteRequest):
        return self._filterStatusCB(quoteRequest, 'update') if self._filterStatusCB else quoteRequest
        
    def __NewQuoteRequest(self, quoteRequest):
        if self.__NotifyOnNewQuoteRequest(quoteRequest):
            self.__Notify().NewEvent()
            
    def __QuoteRequestUpdate(self, quoteRequest):
        if self.__NotifyOnQuoteRequestUpdate(quoteRequest):
            self.__Notify().UpdateEvent()
        
    def Enable(self):
        self._enabled = True
        self.__Subscribe()
            
    def Disable(self):
        self._enabled = False
        self.__Unsubscribe()
        
    def ToggleEnabled(self):
        self.Enable() if not self._enabled else self.Disable()
        
    def Enabled(self):
        return self._enabled 
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if parameter and self._filterQueryCB().IsSatisfiedBy(parameter):
            if self.__Notify().Destroyed():
                self.Disable()
            elif str(aspectSymbol) == 'insert':
                self.__NewQuoteRequest(parameter)
            elif str(aspectSymbol) == 'update':
                self.__QuoteRequestUpdate(parameter)
            else:
                print(('UNHANDLED', aspectSymbol))
