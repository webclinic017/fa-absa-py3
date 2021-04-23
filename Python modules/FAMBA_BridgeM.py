"""
Additional mutators, some of these are optional and should
not be used in the default case.


"""

import amb, time
import FAMBA_Bridge

from FAMBA_Bridge import FAMBA_mutator, pref, fetchPath, \
                                getTranslatedPrimaryKey, hasPath, FAMBAFilter, \
                                getMBFMessageValue, find_mbf_object, getMessageType, \
                                NotBridgeTableFilter, BridgeTableFilter, DefaultFilter, \
                                getSQLVal


class MirrorTranslation(FAMBA_mutator):
    """
    TODO fix and test

    """
    def fixMessage(self, m):
        # pass
        pref.dMsg("Path True "+str(fetchPath(m, ["*TRADE", "MIRROR_TRDNBR"])))
        pref.dMsg("Path 2 True "+str(fetchPath(m, ["*TRADE", "_MIRROR_TRDNBR"])))
        if( fetchPath(m, ["*TRADE", "MIRROR_TRDNBR"])
                or fetchPath(m, ["*TRADE", "_MIRROR_TRDNBR"])):
            # get all legs
            # get python form
            message = self.mbf2py(m)

            trade = [V for (N, V) in message if N == "TRADE" or
                        N == "+TRADE" or N=="!TRADE" ][0]
                        
            pref.dMsg("TRADE"+str(trade))
            pref.dMsg("TRADE MIRROR "+str([V for (N, V) in trade if N == "MIRROR_TRDNBR" 
                        or "_MIRROR_TRDNBR"]))
            #fetch the mirror trade            
            key = int([V for (N, V) in trade if N == "MIRROR_TRDNBR" 
                        or N == "_MIRROR_TRDNBR"][0])

            pref.dMsg("FAMBA_Bridge.addinfoDic->"+str(FAMBA_Bridge.addinfoDic))

            nkey = getTranslatedPrimaryKey("Trade", key)

            pref.dMsg("Found translation key "+str(nkey)+" "+str(type(nkey)))

            #if not nkey:
            #        pref.dMsg("No key skipping!!")
            #        return m

            pref.dMsg("Wrapping message in a transaction")

            #new built message

            #add the relevant message
            nmessage = [(N, V) for (N, V) in message if not (N == "TRADE" or
                        N == "+TRADE" or N=="!TRADE")]
            nmessage.append(("TRANSACTION", [("TRADE", trade)]))

            pref.dMsg("Final return is!")
            pref.dMsg(nmessage)
            
            #changing the message
            self.pyreplace2mbf(m, nmessage)
        return m
    
    def INSERT_TRADE(self, m):
        pref.dMsg("MIRRORFIX INSERT_TRADE V2")
        return self.fixMessage(m)
    
    def UPDATE_TRADE(self, m):
        pref.dMsg("MIRRORFIX UPDATE_TRADE V2")
        return self.fixMessage(m)














class MirrorTranslationSend(FAMBA_mutator):
    """
    Mirror trade insert make AMBA behave in unwanted ways. In order to prevent
    this we strip MIRROR_TRDNBR and replace it with _MIRROR_TRDNBR
    
    TODO fix and test
    """
    
    def fixMessage(self, m):
        # pass
        if( fetchPath(m, ["*TRADE", "MIRROR_TRDNBR"])):
            pref.dMsg("MIRRORSTRIP")
            # get all legs
            # get python form
            message = self.mbf2py(m)

            trade = [V for (N, V) in message if N == "TRADE" or
                        N == "+TRADE" or N=="!TRADE" ][0]
                        
            #fetch the mirror trade            
            vals = [("_"+str(N), V) for (N, V) in trade if N == "MIRROR_TRDNBR" 
                        or N=="TRX_TRDNBR"]

            ntrade = [(N, V) for (N, V) in trade if (not (N=="MIRROR_TRDNBR" or 
                                                        N=="TRX_TRDNBR"))]
            ntrade.extend(vals) 

            #do we need this or could we use the editing list to fix this
            nmessage = [(N, V) for (N, V) in message if not (N == "TRADE" or
                        N == "+TRADE" or N=="!TRADE")]
            nmessage.append(("TRADE", ntrade))

            pref.dMsg("Final return is!")
            pref.dMsg(nmessage)
            
            #changing the message
            self.pyreplace2mbf(m, nmessage)
        return m
    
    def INSERT_TRADE(self, m):
        pref.dMsg("MIRRORFIX SEND INSERT_TRADE V3")
        return self.fixMessage(m)
    
    def UPDATE_TRADE(self, m):
        pref.dMsg("MIRRORFIX SEND UPDATE_TRADE V3")
        return self.fixMessage(m)




class mirrorTranslationStrip(FAMBA_mutator):
        """
        Strip the mirror trade entries from the trade and handle
        the trades as though they are ordinary trades.
        """
        
        def stripMirror(self, message):
                trade = [V for (N, V) in message if N == "TRADE" or
                        N == "+TRADE" or N=="!TRADE" ][0]
                ntrade = [(N, V) for (N, V) in trade if (not (N=="MIRROR_TRDNBR" or 
                                                        N=="TRX_TRDNBR"))]
                nmessage = [(N, V) for (N, V) in message if not (N == "TRADE" or
                        N == "+TRADE" or N=="!TRADE")]
        
                nmessage.append(("TRADE", ntrade))
                return nmessage
        
        def fixMessage(self, m):
                if(fetchPath(m, ["*TRADE", "MIRROR_TRDNBR"])):
                    mess = self.mbf2py(m)
                    nmess = self.stripMirror(mess)
                    self.pyreplace2mbf(m, nmess)
                return m

        def INSERT_TRADE(self, m):
            pref.dMsg("FAMBA_BridgeM mirrorTranslation SEND INSERT_TRADE V3")
            return self.fixMessage(m)

            
        def UPDATE_TRADE(self, m):
                pref.dMsg("FAMBA_BridgeM mirrorTranslation SEND UPDATE_TRADE V3")
                return self.fixMessage(m)

        
        
        
class fixLegnbr(FAMBA_mutator):
        """
        This class control updates and inserts of FX outright and Swap.
        It keeps the sent instrument that is not connected to anything
        on the 4 side in sync with the Front 2 side.
        The point with this is that subsequent updates to trades in Front 2
        are managed correctly.
        
        The handling below of legs should possible be extended to related
        instruments.
        
        """
        
        def makeLeg(self, els, insid):
                import ael
                #insa = ael.Instrument[insid]
                
                nnbr = [(N, V) for (N, V) in els  
                        if not (N == "LEGNBR" or N == "EXTERN_ID")]

                legnbr = [V for (N, V) in els
                          if N == "LEGNBR"][0]
                
                ext    = [V for (N, V) in els
                          if N == "EXTERN_ID"]

                #if insa:
                #        legnbr = insa.legs()[self.cleg].legnbr
                #        self.cleg =self.cleg+1
                #        nnbr.append(("LEGNBR",str(legnbr)))

                if ext == []:
                        nnbr.append(("EXTERN_ID", "L"+str(legnbr)+"J"))
                else:
                        #use the old extern_id if available
                        nnbr.append(("EXTERN_ID", ext[0]))
                return nnbr
        
        def makeUpdt(self, mess):
                """Python formatted message"""
                self.cleg = 0
                omess = [(N, V) for (N, V) in mess 
                                if (not (N == "!INSTRUMENT"
                                         or N=="+INSTRUMENT"
                                         or N=="INSTRUMENT"))] 
                ins   = [V for (N, V) in mess  
                                if (N == "!INSTRUMENT") 
                                        or N =="+INSTRUMENT"
                                        or N =="INSTRUMENT"][0] 
                insid = [V for (N, V) in ins 
                                if N == "INSID"][0]                
                legs  = [(N, self.makeLeg(V, insid)) for (N, V) in ins
                                if N == "LEG" or
                                        N == "!LEG" or N =="+LEG"]
                insnl = [(N, V) for (N, V) in ins                                 
                                if not (N == "LEG" or
                                                N == "!LEG"
                                                or N == "+LEG")]
                nins   = insnl
                nins.extend(legs)
                omess.append(("INSTRUMENT", nins))
                return omess
                
        
        def process(self, m):
                if(hasPath(m, ["*INSTRUMENT", "INSTYPE", "INS_FX_SWAP"])):
                        mess = self.mbf2py(m)
                        nmess = self.makeUpdt(mess)
                        self.pyreplace2mbf(m, nmess)
                        return m
                else:
                        pref.dMsg("Nothing to change!!")
                return m
        
#        def processOld(self,m):
#                self.delete(m,["*INSTRUMENT","*LEG","LEGNBR"])
#                self.delete(m, ["*INSTRUMENT","*LEG","*CASHFLOW","CFWNBR"])
#                return m
        
        def INSERT_INSTRUMENT(self, m):
                return self.process(m)
                #return m
                
        def UPDATE_INSTRUMENT(self, m):
                return self.process(m)
        
        
        

        
        
class fixYieldCurves(FAMBA_mutator):
        """
        Yield curves are not working as expected with additional infos.
        This is a patch for SPR 235651
        
        """
        def makeCurve(self, name, ai):
                import ael
                ycn = ael.YieldCurve[name]
                if(not ycn):
                        ycn = ael.YieldCurve.new()
                        pref.dMsg("curve_name "+str(name))
                        ycn.yield_curve_name = name
                        ycn.yield_curve_type = "Benchmark"
                        #ael.enum_from_string("IrType","Spread")
                        ycn.commit()
                # add aditional infos
                #we will assume that all ais have a proper spec
                pref.dMsg("Available recs and values "+str(ai))
                for spec, val in ai:
                        pref.dMsg("FAMBA_BridgeM makeCurve spec="+str(spec) + " val="+val)
                        v = ael.AdditionalInfoSpec[spec]
                        if v:
                                #first find the addinfo and if any
                                #change the value !!!
                                q = "recaddr=%s and addinf_specnbr =%s" % (ycn.seqnbr, v.specnbr)
                                x = ael.AdditionalInfo.read(q)
                                if x:
                                        oa = x.clone()
                                else:                                
                                        oa = ael.AdditionalInfo.new(ycn)
                                oa.addinf_specnbr = v
                                oa.value = val
                                oa.commit()
                                pref.dMsg("Setting "+str(spec)+"="+str(val))
                
        
        def change(self, m):
                header = [(N, V) for (N, V) in m
                                if not (N=="YIELDCURVE"
                                        or N=="!YIELDCURVE"
                                        or N=="+YIELDCURVE")]
                #the type of the header
                header[0] = ("TYPE", "UDPATE_YIELDCURVE")
                yc =  [V for (N, V) in m
                                if (N=="YIELDCURVE"
                                        or N=="!YIELDCURVE"
                                        or N=="+YIELDCURVE")][0]
                ycname = [V for (N, V) in yc 
                                if N == "YIELD_CURVE_NAME"][0]
                #get all add infos processed
                ais      = [V for (N, V) in yc
                          if (N=="ADDITIONALINFO" or
                              N=="+ADDITIONALINFO" or
                              N=="!ADDITIONALINFO")]
                ai = []
                pref.dMsg("FAMBA_BridgeM ais "+str(ais))
                for i in ais:
                    spec = "none"
                    val = "none"
                    for (N, V) in i:    
                            if N=="VALUE":
                                    val = V 
                            elif N == "ADDINF_SPECNBR.FIELD_NAME":
                                    spec = V 
                    ai.append((spec, val))
                
                #go on and build a curve and add all add info
                self.makeCurve(ycname, ai)

                #use this to commit as addInfo do not work
                ycu    = [(N, V) for (N, V) in yc
                          if not (N=="ADDITIONALINFO" or
                              N=="+ADDITIONALINFO" or
                              N=="!ADDITIONALINFO")]
        
                #yield curve stripped of add info
                header.append(("YIELDCURVE", ycu))
                return header
        
        
        def process(self, m):
                path = ["*YIELDCURVE", "*ADDITIONALINFO"]
                #check if there is an additional info on curve
                if(fetchPath(m, path)):
                        pref.dMsg("Found Yield curve!!!")
                        #process the curve like this
                        mess = self.mbf2py(m)
                        nmess = self.change(mess)
                        self.pyreplace2mbf(m, nmess)
                
                #raise "Not an error, stopping anyway!!"
                return m
        
        
        def INSERT_YIELDCURVE(self, m):
                return self.process(m)
        
        
        def UPDATE_YIELDCURVE(self, m):
                return self.process(m)
        
        
                
class fixRemoveResets(FAMBA_mutator):
                
        def filt(self,X,n=0):
                if type(X) == type([]):
                        l = [self.filt(Y, n) for Y in X]
                        f = [X for X in l if not X == None]
                        return f                      
                if type(X) == type(""):
                        return X
                else:
                        (N, A) = X 
                        
                        if N == "RESET" or N == "!RESET" or N == "+RESET":
                                return None
                        elif type(A) == type(""):
                                return (N, A)
                        else:
                                return (N, self.filt(A, n+1))
                                
                
        def process(self, m):
                #check for resets and if any process
                #possibly we should simple parse everything
                if(fetchPath(m, ["*INSTRUMENT", "*LEG", "*CASHFLOW", "*RESET"])):
                        mess = self.mbf2py(m)
                        nmess = self.filt(mess)
                        self.pyreplace2mbf(m, nmess)
                else:
                        pref.dMsg("Didn't find anything!!")
                return m
        
        
        def UPDATE_INSTRUMENT(self, m):
                pref.dMsg("-------------- fixRemoveResets -------------")
                return self.process(m)
        
        def INSERT_INSTRUMENT(self, m):
                pref.dMsg("-------------- fixRemoveInstrument -------------")
                return self.process(m)



# -----------------------------------------------------------
# Fields requiring replace in quote_parameter
# -----------------------------------------------------------
#
#only oderbook_id needs replacing
#
#
#None is using this at the moment, candidate for permanent removal
#Removed from default mutators
#   
class FAMBA_localOrderBooks(FAMBA_mutator):
    "to fix quoteParameter"
    
    #
    #Minor bug, using q.* doesnt work here
    #
    def findQuoteParameterByKeys(self, insid, curr, ptyid, exttype):
        import ael
        """This function finds one quote parameter that matches specified order book.
        Since the relationship between quote parameter and orderbook is one-to-one
        this will work. It will not crash simply because of multiple quote parameters.
        """
        val = ael.asql( \
                "select q.seqnbr from quoteparameter q,orderbook o, instrument i, instrument c, party p "  \
                "    where o.insaddr = i.insaddr and i.insid = '" + str(insid) + "'"      \
                "        and o.curr = c.insaddr and c.insid ='" + str(curr) + "'"         \
                "        and p.ptynbr = o.market_ptynbr and p.ptyid = '" + str(ptyid)+"'"  \
                "        and o.external_type = '" + str(exttype) + "'" \
                "        and q.orderbook_id = o.oid " \
            )
        pref.dMsg(str(self)+"="*5 + ">\n" + str(val))
        # only getting seqnbr number
        return val[1][0][0][0]
    
    def findPrimaryMessageKeys(self, msg):
        
        #getMBFMessageValue
        insid   = getMBFMessageValue(msg, 'QUOTEPARAMETER', 'ORDERBOOK_ID.INSADDR.INSID')
        curr    = getMBFMessageValue(msg, 'QUOTEPARAMETER', 'ORDERBOOK_ID.CURR.INSID')
        ptyid   = getMBFMessageValue(msg, 'QUOTEPARAMETER', 'ORDERBOOK_ID.MARKET_PTYNBR.PTYID')
        exttype = getMBFMessageValue(msg, 'QUOTEPARAMETER', 'ORDERBOOK_ID.EXTERNAL_TYPE')
        #return ('DAIM 7.0 21/03/11','EUR','AIMS',0)
        #return (1,2,3,4)
        return (insid, curr, ptyid, exttype) 
    
    def findQuoteParameter(self, msg):
        """
        Go through the message and create a primary key linking to the correct quote param
        """
        keys = self.findPrimaryMessageKeys(msg)
        pref.dMsg("Keys were " + str(keys))
        quoteParam = self.findQuoteParameterByKeys(keys[0], keys[1], keys[2], keys[3])
        pref.dMsg("Quote oid is " + str(quoteParam))
        return quoteParam
    
    def alterMessage(self, msg, val):
        """
        add seqnbr to object
        """
        pref.dMsg("Adding string")
        #---# must ignore +-! signs 
        #obj = msg.mbf_find_object('QUOTEPARAMETER')
        obj = find_mbf_object(msg, 'QUOTEPARAMETER')
        obj.mbf_add_int("SEQNBR", val)
        return msg
    
    def mutate(self, msg):
        """ Replacing seqnb of msg if appropriate """
        type = getMessageType(msg)
        pref.dMsg("QUOTEPARAMETER FAMBA_mutator type is "+ str(type) \
                      +    " localOrderBooks " + str(pref.hasLocalOrderBooks()) )
                
        if type == 'UPDATE_QUOTEPARAMETER' and pref.hasLocalOrderBooks():
            pref.dMsg("QUOTEPARAMETER Creating seqnbr in message!!")
            qpm = self.findQuoteParameter(msg)
            msg = self.alterMessage(msg, qpm)
            return msg
        
        elif type == 'DELETE_QUOTEPARAMETER' and pref.hasLocalOrderBooks():
            pref.dMsg("QUOTEPARAMETER Creating seqnbr in delete message!!")
            qpm = self.findQuoteParameter(msg)
            msg = self.alterMessage(msg, qpm)
            return msg
        
        else:
            pref.dMsg("QUOTEPARAMETER mutate Ignoring")
            return msg
        
        
class AggregationFix(FAMBAFilter, FAMBA_mutator):
    """
    Aggregation appears quite broken, enable this when needed
    
    """
    
    def copyAndRename(self, wc, targ):
        """ Copy a trade """
        tt = targ.mbf_start_list("+Trade")
        self.copy(wc, tt)
    

        
    
    def getSrcTrdnbr(self, m):
        """
        Assumes that the value exists
        
        Can probably be removed as this has been fixed in ADS?
        """
        v = m.mbf_find_object("-TRADE")
        a = v.mbf_find_object("ADDITIONALINFO")
        pref.dMsg( ("V", v, "a", a))
        while a != None:
            pref.dMsg(a.mbf_object_to_string())
            if hasPath(a, ["ADDINF_SPECNBR.FIELD_NAME", "zzAB_Trade"]):
                rVal = a.mbf_find_object("Value").mbf_get_value()
                return rVal
            a = v.mbf_find_object("ADDITIONALINFO", "current")       
        raise Exception("GetSrcTrdnbr could not find source trdnbr")
        
    
    
    """
    Improvments
    """
    def filter(self, m):
        # aggregation
        ans = hasPath(m, ["TYPE", "DELETE_TRADE"])  \
            and hasPath(m, ["-TRADE", "AGGREGATE", "2"]) \
            and hasPath(m, ["-TRADE", "ADDITIONALINFO",
                            "ADDINF_SPECNBR.FIELD_NAME", "zzAB_Trade"])

        if ans:
            srcTrdnbr = self.getSrcTrdnbr(m)
            s = """    
            select trdnbr from trade t, additionalInfo a, additionalInfoSpec s
                where t.trdnbr = a.recaddr  and a.value = %s
                    and a.addinf_specnbr = s.specnbr and s.field_name = 'zzAB_Trade'
            """ % (srcTrdnbr)
            val = getSQLVal(s)
                        
            if val == None:
                #Then this value should be passed on if trades are sent over
                # the bridge
                pref.dMsg("Should change and pass on a value")
                # check that trades should be sent over the bridge
                V = self.getAgentResults(m, [NotBridgeTableFilter(),
                                            BridgeTableFilter(),
                                            DefaultFilter()])
                pref.dMsg("V is now "+str(V))
                if V:
                    return (True, 10101, '')
                else:
                    return (True, 0, '')

            else:
                pref.dMsg("Value is a True Delete statement")
                return (True, 0, '')
        return (True, 0, '')

    def DELETE_TRADE(self, m):
        (V, P, M) = self.filter(m)
        if V and P!=0:
            pref.dMsg("CALLING AGGREGATION")
            o = m.mbf_find_object("-Trade")
            self.copyAndRename(o, m)
            self.replace(m, ["TYPE"], ("DELETE_TRADE", "INSERT_TRADE"))
            self.delete(m, ["-TRADE"])
        return m        



class fixRemoveBarrierStatus(FAMBA_mutator):
        """
        Remove barrier cross status
        
        """
                
        def filt(self, mess):
                """
                 
                """
                omess  = [(N, V) for (N, V) in mess 
                                if (not (N == "!INSTRUMENT"
                                         or N=="+INSTRUMENT"
                                         or N=="INSTRUMENT"))] 
                ins    = [V for (N, V) in mess  
                                if (N == "!INSTRUMENT") 
                                        or N =="+INSTRUMENT"
                                        or N =="INSTRUMENT"][0]
                ext    = [V for (N, V) in ins  
                                if (N == "!EXOTIC") 
                                        or N =="+EXOTIC"
                                        or N =="EXOTIC"][0]
                
                
                ext2   = [(N, V) for (N, V) in ext
                                if not (N=="BARRIER_CROSSED_STATUS"
                                        or N=="BARRIER_CROSS_DATE")]
                
                inso   = [(N, V) for (N, V) in ins
                                if not (N == "!EXOTIC"
                                        or N == "+EXOTIC"
                                        or N == "EXOTIC")]

                inso.append(("EXOTIC", ext2))
                omess.append(("INSTRUMENT", inso))
                return omess
                
                
        def process(self, m):
                #check for resets and if any process
                #possibly we should simple parse everything
                if(fetchPath(m, ["*INSTRUMENT", "*EXOTIC", "BARRIER_CROSSED_STATUS"])):
                        pref.dMsg("Found barrier crossed status!")
                        mess = self.mbf2py(m)
                        nmess = self.filt(mess)
                        self.pyreplace2mbf(m, nmess)
                else:
                        pref.dMsg("Didn't find barrier status")
                        
                return m
        
        
        def UPDATE_INSTRUMENT(self, m):
                pref.dMsg("-------------- fixRemoveBarrierStatus -------------")
                return self.process(m)


class addFieldObject(FAMBA_mutator):
        """
Add fields to a message. The point is to skip the need of a lot definies in the AMBA.
Managing settings on the AMBAs is limited and is cumbersome to maintain.
        """

        def __init__(self):
                #COMPLETE LIST similar to old format

                """
                Field Add
                {{leg,payleg},{leg,nominal_at_start},{trade,price},{trade,premium},{orderBook,external_type},{YieldCurve,updat_usrnbr},{Volatility,updat_usrnbr},{Instrument,updat_usrnbr}}
                
                """
                
                self.reffieldsT = [["QuoteParameter", "orderbook_id", "OrderBook", "external_type"],
                                  ["QuoteParameter", "orderbook_id", "OrderBook", "insaddr"],
                                  ["QuoteParameter", "orderbook_id", "OrderBook,curr"],
                                  ["QuoteParameter", "orderbook_id", "OrderBook", "market_ptynbr"],
                                  ["trade", "insaddr", "instrument", "instype"],
                                  ["trade", "insaddr", "instrument", "exotic_type"]]
        
                self.reffields = {"INSADDR.INSID":[("Instrument", "instype", "INSADDR.INSTYPE"),
                                                   ("Instrument", "exotic_type",
                                                        "INSADDR.EXOTIC_TYPE")],
                                  "!INSADDR.INSID":[("Instrument", "instype", "INSADDR.INSTYPE"),
                                                    ("Instrument", "exotic_type",
                                                        "INSADDR.EXOTIC_TYPE")],
                                  "+INSADDR.INSID":[("Instrument", "instype", "INSADDR.INSTYPE"),
                                                    ("Instrument", "exotic_type",
                                                        "INSADDR.EXOTIC_TYPE")]}
                #needs more logic and an example to fix
                #self.addfields = {"LEG":      
        
        def flatten(self, L):
                l =[]
                for i in L:
                        if(type(i) == type([])):
                                 i = self.flatten(i)
                                 l.extend(i)
                        else:
                                 l.append(i) 
                return l      
        
        def parseFields(self,X,n=0):
                if type(X) == type([]):
                        l = [self.parseFields(Y, n) for Y in X]
                        l = self.flatten(l)
                        f = [X for X in l if not X == None]
                        return f                      
                if type(X) == type(""):
                        return X
                else:
                        (N, A) = X 
                        
                        if N in self.reffields:
                                RL = [(N, A)]
                                import ael
                                for T, AT, R in self.reffields[N]:
                                        #append anything                                
                                        RL.append((R, getattr(getattr(ael, T)[A], AT)))  
                                return RL                                       
                        elif type(A) == type(""):
                                return (N, A)
                        else:
                                return (N, self.parseFields(A, n+1))

        def advals(self, mess):
                return self.parseFields(mess)


        def process(self, m):
                pref.dMsg("adding values to transaction")
                mess = self.mbf2py(m)
                nmess = self.advals(mess)
                self.pyreplace2mbf(m, nmess)
                return m
                
                
#        def INSERT_TRADE(self,m):
#                return self.process(m)
                
#        def UPDATE_TRADE(self,m):
#                return self.process(m)

        def mutate(self, m):
                return self.process(m)




class removeOldieLinks(FAMBA_mutator):
        """
        When updating an old entity such as a trade we should not add an additional info.
        Therefore we remove it on this side. We could do this on the target side.

        Now also doubles to remove any _* links
        A completely fully featured working complete version will have to wait
        
        Also removing name CFWNBR as this is junk and never handled properly
        (this should perpahs be removed in the future)
        """
        
        
        def addInfoTrdLink(self, mess):
                if(not (type(mess) == type([]))):
                        return False
                l = [(N, V) for (N, V) in mess if (N=="ADDINF_SPECNBR.FIELD_NAME" 
                                                 and (V=="zzAB_Trade"
                                                      or V=="zzBR_Trade"))]
                return l!=[]
                
        
        def filt(self, mess):
                """
                 
                """
                omess  = [(N, V) for (N, V) in mess 
                                if (not (N == "!TRADE"
                                         or N=="+TRADE"
                                         or N=="TRADE"))] 
                ins    = [V for (N, V) in mess  
                                if (N == "!TRADE") 
                                        or N =="+TRADE"
                                        or N =="TRADE"]
                #TODO check correctness
                #the trade is a converted fxSwap if there is not trade
                #this is safe to ignore
                if(ins==[]):
                        return mess
                else:
                        ins = ins[0]
                
                inso   = [(N, V) for (N, V) in ins
                                if not (N == "!ADDITIONALINFO"
                                        or N == "+ADDITIONALINFO"
                                        or N == "ADDITIONALINFO") and not self.addInfoTrdLink(V)
                                   and not N[0:1]=="_" ]


                omess.append(("TRADE", inso))
                
                
                return omess
                
                
        def UPDATE_TRADE(self, m):
                pref.dMsg("checking if addinfo should be removed")
                return self.process(m)
        
        
        def escapeAddVals(self,X,LN=None):
                """Recursive in order to deal with it
                   Could potentially touch additional infos
                """
                if(type(X)==type("")):
                        return X
                else:
                        if(LN=="ADDITIONALINFO"
                                or LN=="!ADDITIONALINFO"
                                or LN=="+ADDITIONALINFO"):
                                #additional info ignore 
                                return X
                        else:
                                eleml = [(N, self.escapeAddVals(V, N)) for (N, V) in X
                                           if not (N[0:1]=="_")
                                              and not (N=="AMBA_BRIDGE_REF_RES")
                                              and not (N=="CFWNBR")                                   
                                           ]
                                return eleml

        
        
        def isUpdTrade(self, msg):
                type = getMessageType(msg)
                
                #
                #This may be a security hazard
                #as the type itself is used in the call
                # 
                # security reasons
                type.upper() 
                if(type=="UPDATE_TRADE"):
                        return True

        
        def mutate(self, msg):
                
                isUpdTrade = self.isUpdTrade(msg)
                
                mess = self.mbf2py(msg)
                #first rebuild skipping anything denoted as _ values
                mess = self.escapeAddVals(mess)
                if(isUpdTrade):
                        mess =  self.filt(mess)
                
                self.pyreplace2mbf(msg, mess)
                return msg
                
                        
                        
class filteredMessageLogger(FAMBA_mutator, FAMBAFilter):
        """
        Used to patch for update error in AMBA
        """
        
        def __init__(self, outfile):
                self.outfile = outfile
                #lets assume we never crash and if we do try to get back
                self.filePos = 0
                try:
                        self.theFile = open(self.outfile, "a")
                except Exception, e:
                        raise Exception("Could not open out file for cache misses file "+ \
                                        str(self.outfile)+ \
                                        " reason: "+ str(e))

        def writeOut(self, body):
                
                #we do not want to 
                F = self.theFile #open(self.outfile,"a")
                F.write(body)
                #F.flush()
                #F.close()
                
        def __del__(self):
                """Flush file nad close it, be nice to windows"""
                if(hasattr(self, "theFile") and self.theFile):
                        self.theFile.flush()
                        self.theFile.close()
                
        def logmessage(self, msg, reason):
                
                vals = None
                try:
                        vals = msg.mbf_object_to_string()
                except Exception, e:
                        #should never happen
                        pref.dMsg("Could not get message text "+str(e))
                        return
        
                #timing needs to be consistent only within itself
                hbody = "#-!"*40+"\n"+"HEADER\nLENGTH="+str(len(vals))+ \
                        "\nTIME="+time.strftime("%Y-%m-%d %H:%M:%S")+ \
                        "\nSENT=N"+ \
                        "\nREASON=%s" % reason + \
                        "\nDATA\n"+vals
                pref.dMsg("Write to file " + self.outfile)
                self.writeOut(hbody)
                
                
        def filterMessage(self, msg, points, reason):
                if(reason[:4] == "E404"):
                        pref.dMsg("Logging missed message")
                        self.logmessage(msg, reason)
                
        
        def specialTrade(self, m):
                pref.dMsg("PATH IS "+str(fetchPath(m, ["TRADE", "INSADDR.INSID", "HEARTBEAT_INSTRUMENT_THAT_IS_NOT"])))
                if(fetchPath(m, ["TRADE", "INSADDR.INSID", "HEARTBEAT_INSTRUMENT_THAT_IS_NOT"])):
                        return True
                else:
                        return False
        
        def getCV(self, val):                
                return (val.split("=")[1]).strip()

        def getLatestPayload(self):
                R = open(self.outfile)
                R.seek(self.filePos)
                #get the data inbetween
                R.readline() #header
                length = int(self.getCV(R.readline())) # actual length
                timet  = self.getCV(R.readline())
                sent   = R.readline()
                R.readline()    
                data = R.read(length)            
                # then resend
                filePos = R.tell()
                R.close()                
                return (filePos, data)
                        
        def buildNew(self, mess):
                #we actually don't care about the message, try to get it from the file
                pref.dMsg("File position is "+ str(self.filePos))
                #self.filePos = self.FilePos +1
                nFilePos, payload = self.getLatestPayload()
                print "New File pos", nFilePos
                print "payload", payload
                #convert the text to actual mbf_message (using mbf ??)               
                return mess
        
        def rebuildMessage(self, m):
                pref.dMsg(self.filePos)
                mess = self.mbf2py(m)
                nmess = self.buildNew(mess)
                self.pyreplace2mbf(m, nmess)
                return m
                
        def INSERT_TRADE(self, m):
                pref.dMsg("specialTrade checking val")
                if(self.specialTrade(m)):
                        return self.rebuildMessage(m)
                else:
                        return m
                
                
xfilter = False
        
class filteredMessageLoggerInstance(FAMBA_mutator):
        
        
        def INSERT_TRADE(self, m):
                global xfilter
                if(xfilter):
                        pref.dMsg("Using filter logger to add lost updates")
                        return xfilter.INSERT_TRADE(m)
                else:
                        pref.dMsg("No filter logger available to use!")
                        return m
        
