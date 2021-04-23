from __future__ import print_function


"""----------------------------------------------------------------------------

MODULE

    FOrderFlowSimulator: Methods for pricing, arrival, volume and direction
    
    (C) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module generates different user-defined order flows
    to selected order books.

NOTES:
    
    -This module can only be used in PRIME versions from 4.0 
     
    
------------------------------------------------------------------------------"""

import acm
import ael
import time
import thread
import random
import sys
import copy
from math import *
from array import array


# Variables -------------

glActive = True



# Constants ---------------------------------

BID = 0
ASK = 1



# Global functions --------------------------    

# flag to stop all processes 
# if user presses "stop all"
def stopAll(mei):
    global glActive
    print ("stop all....")
    glActive = False
  
  
 
# check if number is empty 
# (not a number)
def isEmpty(number):
    flag = '1.#QNAN'
    if str(number) == flag:
        return True
    elif number == None:
        return True
    else:
        return False


# create an order, set price
# and quantity and send it
# to the market
def createAndSendOrder(tradingSession, ob, isSellOrder, price, quantity):
    order = tradingSession.CreateOrder(ob)
    order.Price = price
    order.Quantity = quantity
    if isSellOrder:
        order.BuyOrSell = "Sell"
    else:
        order.BuyOrSell = "Buy"
    order.Send()
    return order

# Functions for param GUI -------------------

def cbThrottle(idx, fieldValues):
    if( fieldValues[idx] == '1' ):
        ael_variables[4][9] = 1
        ael_variables[5][9] = 1
    else:
        ael_variables[4][9] = 0
        ael_variables[5][9] = 0
    return fieldValues



def cbStaticSeed(idx, fieldValues):
    if( fieldValues[idx] == '1' ):
        ael_variables[7][9] = 1
    else:
        ael_variables[7][9] = 0        
    return fieldValues



def cbOverShoot(idx, fieldValues):
    if( fieldValues[idx] == '1' ):
        ael_variables[49][9] = 1
        ael_variables[50][9] = 1
        ael_variables[51][9] = 1
        ael_variables[52][9] = 1
    else:
        ael_variables[49][9] = 0
        ael_variables[50][9] = 0
        ael_variables[51][9] = 0
        ael_variables[52][9] = 0
    return fieldValues



def lmVolumeMethod(idx, fieldValues):
    if( fieldValues[idx] == 'rectangular' ):
        ael_variables[11][9] = 0
        ael_variables[12][9] = 0
        ael_variables[13][9] = 1
        ael_variables[14][9] = 1
    elif( fieldValues[idx] == 'gaussian' ):
        ael_variables[11][9] = 1
        ael_variables[12][9] = 1
        ael_variables[13][9] = 0
        ael_variables[14][9] = 0
    else:
        ael_variables[11][9] = 0
        ael_variables[12][9] = 0
        ael_variables[13][9] = 0
        ael_variables[14][9] = 0
    return fieldValues



def lmPriceMethod(idx, fieldValues):
    if( fieldValues[idx] == 'rectangular' ):
        ael_variables[16][9] = 1
        ael_variables[17][9] = 1
        ael_variables[18][9] = 1
        ael_variables[19][9] = 0
        ael_variables[20][9] = 1
    elif( fieldValues[idx] == 'gaussian' ):
        ael_variables[16][9] = 1
        ael_variables[17][9] = 1
        ael_variables[18][9] = 0
        ael_variables[19][9] = 1
        ael_variables[20][9] = 1
    else:
        ael_variables[16][9] = 0
        ael_variables[17][9] = 0
        ael_variables[18][9] = 0
        ael_variables[19][9] = 0
        ael_variables[20][9] = 0
    return fieldValues



def lmDirectionMethod(idx, fieldValues):
    if( fieldValues[idx] == 'toggle' ):
        ael_variables[23][9] = 0
        ael_variables[24][9] = 0
    elif( fieldValues[idx] == 'random' ):
        ael_variables[23][9] = 1
        ael_variables[24][9] = 0
    elif( fieldValues[idx] == 'bias' ):
        ael_variables[23][9] = 1
        ael_variables[24][9] = 1
    else:
        ael_variables[23][9] = 0
        ael_variables[24][9] = 0
    return fieldValues



def lmImballance(idx, fieldValues):
    if( fieldValues[idx] == 'disable' ):
        ael_variables[26][9] = 0
        ael_variables[27][9] = 0
        ael_variables[28][9] = 0
        ael_variables[29][9] = 0
        ael_variables[30][9] = 0
        ael_variables[31][9] = 0
        ael_variables[32][9] = 0
        ael_variables[33][9] = 0
        ael_variables[34][9] = 0
    elif( fieldValues[idx] == 'spread_level (fast)' ):
        ael_variables[26][9] = 1
        ael_variables[27][9] = 1
        ael_variables[28][9] = 1
        ael_variables[29][9] = 1
        ael_variables[30][9] = 1
        ael_variables[31][9] = 1
        ael_variables[32][9] = 1
        ael_variables[33][9] = 0
        ael_variables[34][9] = 0
    elif( fieldValues[idx] == 'transaction_level (slow)' ):
        ael_variables[26][9] = 0
        ael_variables[27][9] = 0
        ael_variables[28][9] = 0
        ael_variables[29][9] = 0
        ael_variables[30][9] = 0
        ael_variables[31][9] = 0
        ael_variables[32][9] = 0
        ael_variables[33][9] = 1
        ael_variables[34][9] = 1
    else:
        ael_variables[26][9] = 0
        ael_variables[27][9] = 0
        ael_variables[28][9] = 0
        ael_variables[29][9] = 0
        ael_variables[30][9] = 0
        ael_variables[31][9] = 0
        ael_variables[32][9] = 0
        ael_variables[33][9] = 0
        ael_variables[34][9] = 0
    return fieldValues



def cbSendAndCancel(idx, fieldValues):
    if( fieldValues[idx] == '1' ):
        ael_variables[37][9] = 1
        ael_variables[38][9] = 1
        ael_variables[39][9] = 1
        ael_variables[40][9] = 1
        ael_variables[41][9] = 1
    else:
        ael_variables[37][9] = 0
        ael_variables[38][9] = 0
        ael_variables[39][9] = 0
        ael_variables[40][9] = 0
        ael_variables[41][9] = 0
    return fieldValues

    

def lmMode(idx, fieldValues):
    if( fieldValues[idx] == 'Stop-Loss' ):
        ael_variables[42][9] = 1
        ael_variables[43][9] = 1
        ael_variables[44][9] = 1
        ael_variables[45][9] = 1
        ael_variables[46][9] = 1
        ael_variables[47][9] = 1 
        ael_variables[48][9] = 1
        ael_variables[49][9] = 1
        ael_variables[50][9] = 1
        ael_variables[51][9] = 1
        ael_variables[52][9] = 1
    else:
        ael_variables[42][9] = 0
        ael_variables[43][9] = 0
        ael_variables[44][9] = 0
        ael_variables[45][9] = 0
        ael_variables[46][9] = 0 
        ael_variables[47][9] = 0 
        ael_variables[48][9] = 0
        ael_variables[49][9] = 0
        ael_variables[50][9] = 0
        ael_variables[51][9] = 0
        ael_variables[52][9] = 0
    return fieldValues
    
    
    
# GUI parameters ----------------------------

ael_variables = [
    ['timetorun', 'Time to run (s)', 'int', ['5', '10', '15', '30', '60', '120', '180', '300'], '5',  1, 0, 'How long to run', None, None], 
    ['drawgraph', 'Draw graph', 'int', ['1', '0'], 0, 1, 0, 'Draw a graph of the order flow', None, 0],
    ['graphinterval', 'Graph interval (s)', 'int', ['1', '2', '5', '10', '60'], '1', 1, 0, 'Time between meassurements',  None, 0],
    ['throttle', 'Throttle', 'int', ['1', '0'], 0, 1, 0, 'Draw a graph of the order flow', cbThrottle, None],
    ['throttleinterval', 'Throttle interval (ms)', 'int', ['500', '1000', '1500', '2000', '5000', '10000', '20000', '60000'], 1000, 1, 0, 'Time between checks', None, None],
    ['throttlewait', 'Max wait(ms)', 'int', ['100', '200', '300', '400', '500', '1000', '1500', '2000', '2500', '500'], 300, 1, 0, 'Max time for an order to complete', None, None],
    ['staticseed', 'Static seed ', 'int', ['1', '0'], 0, 1, 0, 'Override default seed', cbStaticSeed, None],
    ['seed', 'Seed value', 'int', ['10', '20', '30', '40', '50', '100', '150', '200', '250', '500'], None, 0, 0, 'Seed value to use for random generator', None, None],

    # id 8  -- arrival parameters
    ['arrivalTimeMean', 'Mean arrival time (ms)_Arrival', 'int', ['500', '750', '1000'], '1000', 1, 0, 'Mean time between orders', None, None],
    ['x4', 'Intensity_Arrival', 'int', ['500', '750', '1000'], '500', 1, 0, 'Mean time between orders', None, 0],
    
    # id 10 -- volume parameters
    ['volumeMethod', 'Volume method_Volume',  'string',  ['rectangular', 'gaussian'],  'gaussian',  1, 0, 'What volume selection method to use', lmVolumeMethod, None],
    ['volumeMean', 'Mean volume (round lots)_Volume', 'int', ['1', '5', '10', '15', '25', '50', '75', '100'], '50', 1, 0, 'Mean size of orders', None, None],
    ['volumeStd', 'Standard deviation (round lots)_Volume', 'int', ['1', '2', '3', '4', '5', '10', '15'], '5', 1, 0, 'Standard deviation in order sizes', None, None],
    ['volumeMin', 'Min size (round lots)_Volume', 'int', ['1', '5', '10', '15', '25', '50', '75', '100'], '1', 1, 0, 'Min size of an order', None, None],
    ['volumeMax', 'Max size (round lots)_Volume', 'int', ['1', '5', '10', '15', '25', '50', '75', '100'], '100', 1, 0, 'Max size of an order', None, None],
    
    # id 15 -- price parameters
    ['priceMethod', 'Pricing method_Price',  'string',  ['rectangular', 'gaussian'],  'rectangular',  1, 0, 'What side selection method to use', lmPriceMethod, None],
    ['priceDefault', 'Default price_Price', 'int', ['10', '20', '30', '40', '50', '100', '150', '200', '250', '500'], '20', 1, 0, 'Default price to use if orderbook is empty and last price is 1.00', None, None],
    ['priceDefaultSpread', 'Default spread (ticks)_Price', 'int', ['1', '2', '3', '4', '5', '10', '15'], '4', 1, 0, 'Default spread if one of the sides is empty', None, None],
    ['priceRange', 'Price range_Price', 'double', ['0.1', '0.3', '0.5', '1', '1.25', '1.50'], '0.5', 1, 0, '   ', None, None],
    ['priceStd', 'Price standard deviation_Price', 'double', ['1', '2', '3', '4', '5', '10', '15', '20'], '2', 1, 0, '   ', None, None],
    ['priceBidAgg', 'Bid aggressivness (0.5 = middle)_Price', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'Aggressiveness', None, None],
    ['priceAskAgg', 'Ask aggressivness (0.5 = middle)_Price', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'Aggressiveness', None, None],
     
    # id 22 -- direction parameters
    ['sideMethod', 'Side method_Direction',  'string',  ['toggle', 'random', 'bias'],  'random',  1, 0, 'What side selection method to use', lmDirectionMethod, None],
    ['sideRandom', 'Random parameter (0.5 = middle)_Direction', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'Aggressiveness', None, None],
    ['sideBias', 'Bias_Direction', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50'], '0.10', 1, 0, 'Aggressiveness', None, None],
    
    # id 25 -- imballance parameters
    ['imMethod', 'Method_Market Impact', 'string',  ['disable', 'spread_level (fast)', 'transaction_level (slow)'],  'spread_level (fast)',  1, 0, 'What side selection method to use', lmImballance, None],
    ['imQuantity', 'Threshold Quantity (ask/bid or bid/ask)_Market Impact', 'double', ['1.50', '2.00', '2.50', '3.00', '3.50', '4.00', '4.50', '5.00', '5.50'], '4.00', 1, 0, 'Market Impact threshold', None, None],
    ['imShift', 'Shift_Market Impact', 'double', ['0.10', '0.20', '0.25', '0.50', '0.75', '1.00', '1.25', '1.50', '1.75', '2.00', '2.25', '2.50', '2.75', '3.00'], '1.0', 1, 0, 'Price depth to include in market impact dedection', None, None],
    ['imAggSameSide', 'Aggression same side_Market Impact', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'How long the order should be available on the market', None, None],
    ['imAggOpposideSide', 'Aggression opposite side_Market Impact', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'How long the order should be available on the market', None, None],
    ['imDuration', 'Duration_Market Impact', 'int', ['0', '10', '20', '50', '75', '100', '125', '150', '175', '200', '225', '250', '275'], '100', 1, 0, 'Duration in iterations', None, None],
    ['imDirection', 'Direction_Market Impact', 'double', ['0.10', '0.20', '0.30', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.90', 1, 0, 'How long the order should be available on the market', None, None],
    ['imSmooth', 'Smooth reduction_Market Impact', 'int', ['1', '0'], 0, 1, 0, 'Smoothly reduce the responce as time goes by', None, None],
    ['imSlidingWindow', 'Moving average window size_Market Impact', 'int', ['20', '40', '60', '80', '100', '200', '300', '400', '500', '1000', '2000', '3000', '4000'], '100', 1, 0, 'Moving average window', None, None],
    ['imSensitivity', 'Sensitivity (make v. small:)_Market Impact', 'double', ['0.00010', '0.00020', '0.00030', '0.00050', '0.00060', '0.00070', '0.00080', '0.00090'], '0.00010', 1, 0, '', None, None],
      
    # id 35 -- mode
    ['mode', 'Mode_Mode',  'string',  ['Normal', 'Turbo', 'Stop-Loss', 'None'],  'Normal',  1, 0, 'What mode to use', lmMode, None],
    
    # id 36 -- mode (send-n-cancel)
    ['sac', 'Send-&-Cancel_Mode', 'int', ['1', '0'], 0, 1, 0, 'Sends orders then immediatly withdraws', cbSendAndCancel, None],
    ['sacArrivalRate', 'Arrival Rate_Mode', 'int', ['1', '5', '10', '15', '25', '50', '75', '100'], '1000', 1, 0, 'Arrival rate', None, None],
    ['sacMarketExposure', 'Exposure time (ms)_Mode', 'int', ['0', '100', '150', '250', '500', '750', '1000'], '100', 1, 0, 'How long the order should be available on the market', None, None],
    ['sacDirection', 'Direction_Mode', 'string', ['Toggle', 'Bid', 'Ask'], 'Toggle', 1, 0, 'Direction of send-and-cancel orders', None, None],
    ['sacDefaultBid', 'Default Bid_Mode', 'double', ['1.00', '10.00', '20.00', '50.00', '100.00', '200.00', '300.00'], '10', 1, 0, 'Default price if order book is empty', None, None],
    ['sacDefaultAsk', 'Default Ask_Mode', 'double', ['1.00', '10.00', '20.00', '50.00', '100.00', '200.00', '300.00'], '20', 1, 0, 'Default price if order book is empty', None, None],
    
    # id 42 -- mode (stop-loss)
    ['slTriggerTime', 'Trigger time (s)_Mode', 'int', ['1', '5', '10', '15', '25', '50', '75', '100'], '10', 1, 0, 'Arrival rate', None, None],
    ['slBidSeverity', 'Trigger bid aggression_Mode', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.90', 1, 0, 'How long the order should be available on the market', None, None],
    ['slAskSeverity', 'Trigger ask aggression_Mode', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'How long the order should be available on the market', None, None],
    ['slDuration', 'Duration_Mode', 'int', ['0', '10', '20', '50', '75', '100', '125', '150', '175', '200', '225', '250', '275'], '100', 1, 0, 'Duration in iterations', None, None],
    ['slDirection', 'Direction_Mode', 'double', ['0.10', '0.20', '0.30', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.90', 1, 0, 'How long the order should be available on the market', None, None],
    ['slProgressive', 'Smoth reduction_Mode', 'int', ['1', '0'], 0, 1, 0, 'Smoothly reduce the responce as time goes by', None, None],
    
    # id 48 -- mode (overshoot)
    ['slOvershoot', 'overshoot_Mode', 'int', ['1', '0'], 0, 1, 0, 'Sends orders then immediatly withdraws', cbOverShoot, None],
    ['slOvershootBidAgg', 'Overshoot bid aggression_Mode', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.90', 1, 0, 'How long the order should be available on the market', None, None],
    ['slOvershootAskAgg', 'Overshoot ask aggression_Mode', 'double', ['0.10', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.50', 1, 0, 'How long the order should be available on the market', None, None],
    ['slOvershootDuration', 'Overshoot duration(iterations)_Mode', 'int', ['0', '10', '20', '50', '75', '100', '125', '150', '175', '200', '225', '250', '275'], '100', 1, 0, 'Duration in iterations', None, None],
    ['slOvershootDirection', 'Direction_Mode', 'double', ['0.10', '0.20', '0.30', '0.50', '0.60', '0.70', '0.80', '0.90'], '0.90', 1, 0, 'How long the order should be available on the market', None, None],
    
    # id 53     
    ['verbose', 'Verbose ', 'int', ['1', '0'], 0, 1, 0, 'Printout details to log window', None, None]
]


#--------------------------------------------    

def ael_main_ex(parameter, addData):

    global glActive
    glActive = True

    
    # add data to one giant dictionary
    customDataDict = addData.At('customData') # ob(s)
    newlist = copy.deepcopy(parameter)        # params
    
    # set random seed
    if( newlist['staticseed'] ):
        random.seed(newlist['seed'])
    else:
        random.seed()
        

    # create timer
    timer = Timer(newlist['timetorun'])
    timerThread = acm.FThread()
    timerThread.Name('timerThread')
    timerThread.Run(timer.start, ['junk']) 

    
    # create spray object for each orderbook   
    sprayObj = []
    for ob in customDataDict:
    
        # check mode and create spray
        if( newlist['mode'] == 'Turbo' ):
            print ('Turbo mode')
            spray = Spray(newlist, timer, ob)
            sprayObj.append( spray )  # needed for throttle
            sprayThread = acm.FThread()
            sprayThread.Name('turboThread')
            sprayThread.Run(spray.startTurbo, ['junk'])  
        
        elif( newlist['mode'] == 'Normal' ):
            print ('Normal mode')
            spray = Spray(newlist, timer, ob)
            sprayObj.append( spray ) # needed for throttle
            sprayThread = acm.FThread()
            sprayThread.Name('sprayThread')
            sprayThread.Run(spray.startNormal, ['junk'])
            
        elif( newlist['mode'] == 'Stop-Loss' ):
            print ('Stop-Loss mode')
            spray = Spray(newlist, timer, ob)
            sprayObj.append( spray ) # needed for throttle
            sprayThread = acm.FThread()
            sprayThread.Name('sprayThread')
            sprayThread.Run(spray.startStopLoss, ['junk']) 
            
        elif( newlist['mode'] == 'None' ):
            print ('None')
  
            
        # send-and-cancel mode
        if( newlist['sac'] ):
            print ('Send-and-Cancel activated')
            diablo = Diablo(newlist, timer, ob)
            diabloSACThread = acm.FThread()
            diabloSACThread.Name('diabloSACThread')
            diabloSACThread.Run(diablo.startSendAndCancel, ['junk'])  
        

    # create throttle
    if( newlist['throttle'] ):
        print ('Throttle activated')
        throttle = Throttle(newlist['throttleinterval'], newlist['throttlewait'], sprayObj, timer)
        throttleThread = acm.FThread()                            
        throttleThread.Name('throttleThread')
        throttleThread.Run(throttle.start, ['junk']) 
        
        
    # create graph
    if( newlist['drawgraph'] ):
        print ('Graph result')
        graph = Graph(timer, newlist['graphinterval']*1000, customDataDict)
        graphThread = acm.FThread()                            
        graphThread.Name('graphThread') # add some more soon...
        graphThread.Run(graph.start, ['junk']) 
        
        
    
        
    
    
          
# *************************************************************************
#-------------------------------- Classes ---------------------------------
# *************************************************************************

class Diablo:
    """Add *evil* modes that interfer with regular orderflow"""
     
    def __init__(self, dict, timer, ob):
        #self.ob = dict['ob']
        self.ob = ob
        self.dict = dict
        self.timer = timer
        self.side = random.randint(0, 1)   # initial side
        self.tradingSession = acm.FTradingSession(acm.FTradingSessionCustomInterface(self))
        
        
    #------------------------                
    def startSendAndCancel(self, junk):
        """sends an order and then withdraw it after being 
           exposed for 'sacMarketExposure' ms"""

        # step 1: create order of min quantity and 1 tick below opposite best price
        # step 2: send to market
        # step 3: withdraw order after k ms exposure
            
        # i = 0 # just in case to prevent infinite loop during testing (to remove later)

        arrival = self.dict['sacArrivalRate']
        sleep = self.dict['sacMarketExposure']
        side = 0
        
        while( self.timer.active and glActive ):
            
            acm.Sleep(arrival)

            # 1) create order
            # 1.1) side
            # 1.2) volume
            # 1.3) price
            
            # 1.1)
            if( self.dict['sacDirection'] == 'Bid' ):
                side = BID
            elif( self.dict['sacDirection'] == 'Ask' ):
                side = ASK
            elif( self.dict['sacDirection'] == 'Toggle' ):
                side = not side
            
            # 1.2)
            volume = self.ob.RoundLot()
            
            # 1.3)
            if( side == ASK):
                bestBid = self.ob.BestBidPrice().Get().Number()
                if( isEmpty(bestBid) ):
                    #price = self.ob.LastPrice().Get().Number()
                    bestBid = self.dict['sacDefaultBid']
                price = self.ob.RoundTickUp(bestBid + 0.01)
            else:
                bestAsk = self.ob.BestAskPrice().Get().Number()
                if( isEmpty(bestAsk) ):
                    #price = self.ob.LastPrice().Get().Number()
                    bestAsk = self.dict['sacDefaultAsk']
                price = self.ob.RoundTickDown(bestAsk - 0.01)
                
                
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            acm.PollDbEvents()
            
            # 3) expose and withdraw
            if( sleep > 0 ): 
                acm.Sleep(sleep)
            
            # withdraw order
            j = 0
            # don't withdraw before order has reached market
            while( (not order.IsOrderActive() ) and j < 200 ):
                j += 1
                acm.Sleep(1)
            order.Cancel()

            acm.PollDbEvents()

            # some printing
            if( self.dict['verbose'] ):
                print ('diabloSAC: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
            
        print ('DONE: diabloSAC --> ob: %s, timer: %s' % (self.ob.Name(), self.timer.active))
  


# Graph -------------------------------------

class Graph:
    """graph spread"""
    
    # graph constants
    FILENAME                = "result.png"
    LAST_PRICE_COLOUR       = 0x800000      #0x333399
    BEST_BID_COLOUR         = 0x990000
    #BEST_ASK_COLOUR        = 0x9999ff 
    BEST_ASK_COLOUR         = 0x000000
    #SPREAD_COLOUR          = 0x809999ff
    SPREAD_COLOUR           = 0xcccccc
    MANUAL_SCALING          = False
    Y_SCALE_TOP             = 11
    Y_SCALE_BOTTOM          = 7
    Y_TICK_SIZE             = 1
    
    #------------------------
    def __init__(self, timer, interval, obs):
        self.timer     = timer
        self.interval  = interval
        self.obs       = obs
        self.asks       = []    # lowest ask price
        self.bids       = []    # highest bid price
    
    #------------------------
    def start(self, junk):
    
        # only draw graph for first selected orderbook     
        ob = self.obs[0]

        while( self.timer.active and glActive ):

            acm.Sleep(self.interval)

            bestBidPrice = ob.BestBidPrice().Get().Number()
            bestAskPrice = ob.BestAskPrice().Get().Number()
            
            # set empty vars to 0
            if( isEmpty(bestBidPrice) ):
                bestBidPrice = 0
            if( isEmpty(bestAskPrice) ):
                bestAskPrice = 0
            
            while( bestBidPrice >= bestAskPrice and bestBidPrice != 0 and bestAskPrice != 0 ):
                # wait, order book needs to be updated
                acm.Sleep(20)
                bestBidPrice = ob.BestBidPrice().Get().Number()
                bestAskPrice = ob.BestAskPrice().Get().Number()
        
                if( isEmpty(bestBidPrice) ):
                    bestBidPrice = 0
                if( isEmpty(bestAskPrice) ):
                    bestAskPrice = 0
        
            # record current data pts
            self.bids.append(bestBidPrice)
            self.asks.append(bestAskPrice)    
        
        self.draw()
        
        
    #------------------------
    def draw(self):
    
        # create a XYChart object of size 600 x 300 pixels, with a white (0xffffff)
        # background, a black border, and 1 pixel 3D border effect.
        #c = XYChart(800, 600, 0xffffff, 0x000000, 1)
        c = XYChart(800, 500, 0xffffff, 0x000000, 1)
        
        # set the plotarea at (55, 50) and of size 520 x 205 pixels, with white
        # background. Turn on both horizontal and vertical grid lines with light grey
        # color (0xc0c0c0)
        #c.setPlotArea(55, 50, 720, 505, 0xffffff, -1, -1, 0xcccccc, 0xc0c0c0)
        c.setPlotArea(55, 50, 720, 405, 0xffffff, -1, -1, 0xcccccc, 0xc0c0c0)

        # add a legend box at (w, h) (top of the chart) using horizontal layout and 8 pts
        # Arial font Set the background and border color to Transparent.
        c.addLegend(75, 52, 0, "", 8).setBackground(Transparent)
        
        
        if( self.MANUAL_SCALING):
            #use manually scaling of y axis
            c.yAxis().setLinearScale(self.Y_SCALE_BOTTOM, self.Y_SCALE_TOP, self.Y_TICK_SIZE)
        
        
        # add a title to y-axis.
        c.yAxis().setTitle("price level")
    
        # add a title to the bottom x axis
        c.xAxis().setTitle("Time")
        
        # add the lowest ask line
        layer1 = c.addStepLineLayer()
        layer1.addDataSet(self.asks, self.BEST_ASK_COLOUR, "Lowest Ask")
        layer1.setLineWidth(2)

        # add the highest bid line
        layer2 = c.addStepLineLayer()
        layer2.addDataSet(self.bids, self.BEST_BID_COLOUR, "Highest Bid")
        layer2.setLineWidth(2)
        
        # color the region between the spread lines
        c.addInterLineLayer(layer1.getLine(), layer2.getLine(), self.SPREAD_COLOUR)

        # add a title to the chart using 12 points Ariel Bold font. The title is
        # white (0xffffff) on a red background, with a 1 pixel 3D border.
        c.addTitle("Stock Spread: " + str(self.obs[0].Name()), "arielb.ttf", 12, 0xffffff).setBackground(0x990000, -1, 1)
        
        # set the labels on the x axis.
        # c.xAxis().setLabels(timeLabel)

        # display 1 out of 2 labels on the x-axis.
        c.xAxis().setLabelStep(2)

        # output chart
        c.makeChart(self.FILENAME)
        
        # display chart
        os.system('start ' + self.FILENAME)
        
        
        
# Moving average ----------------------------      
  
class MovAvgWindow:
    """mov average between buy vs. sell initated initiated transactions"""
   
    def __init__(self, size):
        # create an array of length 'size'
        # filled with 0's
        self.arr = array('f', [])
        self.sum = 0.0 # to guarantee float division
        self.oldMid = 0
        for i in range(0, size):
            self.arr.append(0)

    #------------------------
    def average(self):
        return self.sum / len(self.arr)
        
    #------------------------
    def add(self, newValue):
        # add new value to array and
        # remove the oldest value
        oldValue = self.arr.pop(0)
        self.arr.append(newValue)
        self.sum += newValue - oldValue
    
    #------------------------
    def addTicker(self, ticker, midprice):
        # count the total signed volume of
        # transactions (buys - sells initiated)
        elements = ticker.Elements()
        if( len(elements) > 0 ):
            vol = 0
            for i in elements:
                price = i.Price()
                quantity = i.Quantity()
                if( i.Price() > midprice ):
                    vol += i.Quantity()
                elif( i.Price() < midprice ):
                    vol -= i.Quantity()
                elif( i.Price() == midprice ):
                    # use prev. midprice
                    if( self.oldMid != 0 ):
                        if( i.Price() > self.oldMid ):
                            vol += i.Quantity()
                        elif( i.Price() < self.oldMid ):
                            vol -= i.Quantity()    
            self.add(vol)
        self.oldMid = midprice

    #------------------------
    def getAverage(self, ticker, midprice):
        # get average signed volume
        self.addTicker(ticker, midprice)
        return self.sum / len(self.arr)
            
    #------------------------
    def printout(self):
        for i in range(0, len(self.arr) ):
            print (i, self.arr[i])
    
    #------------------------
    def size(self):
        # size of window
        return len(self.arr)
                
        
        
# Throttle ----------------------------------

class Throttle:
    """autoadjust order flow"""
    
    def __init__(self, interval, responseTime, sprayObj, timer):
        self.interval = interval
        self.responseTime = responseTime
        self.sprayObj = sprayObj
        self.timer = timer
    
    #------------------------
    def start(self, junk):
    
        # don't continue until all selected OBs 
        # have at least one sent order
        for i in self.sprayObj:
            while( i.sentOrder == 'empty' ):
                acm.Sleep(50)
            
        while( self.timer.active and glActive ):
            
            # check order status of obs
            for i in self.sprayObj:
            
                order = i.sentOrder
                           
                acm.Sleep(self.responseTime)
                
                orderIsActive = order.IsOrderActive()
                if( not orderIsActive ):
                    if( i.throttle < 100 ):
                        i.throttle = i.throttle + 100.0
                    else:
                        i.throttle = i.throttle + 10.0
                    
                elif( orderIsActive or order.IsOrderDone() ):
                    if( i.throttle >= 11.0 ):
                        i.throttle = i.throttle - 10.0
                        
            acm.Sleep( self.interval )
            
        

# Timer -------------------------------------

class Timer:
    """flags when time is up"""
    
    def __init__(self, time):
        self.time = time
        self.active = True
  
    #------------------------
    def start(self, junk):
        tstart = time.time()
        acm.Sleep(self.time)
        
        # sleep-in if awoken early
        while( (time.time() < tstart + self.time) and glActive ):
            snooze = ( tstart + self.time - time.time() ) * 1000
            if( snooze > 0 ):
                acm.Sleep( snooze )
                
        # flag to die 
        self.active = False

    #------------------------
    def active(self):
        return self.active



# Spray -------------------------------------

class Spray:
    """add orders to orderbook"""
     
    def __init__(self, dict, timer, ob):
        #self.ob = dict['ob']
        self.ob = ob
        self.dict = dict
        self.timer = timer
        self.side = random.randint(0, 1)   # initial side
        self.sentOrder = 'empty'
        self.throttle = 1.0
        self.bBidPrice0 = 0
        self.bAskPrice0 = 99999999999999
        self.tradingSession = acm.FTradingSession(acm.TradingSessionCustomInterface(self))

   #------------------------
    def obImballance(self):
        """changes behaviour if the order book is imballanced"""

        priceChange = self.dict['imShift']



        # check between three modes: 
        # 1: disabled
        # 2: spread_level (fast)
        # 3: transaction_level (slow)
        
        # 1) -- method disabled
        if( self.dict['imMethod'] == 'disable' ):
            return False
            
        # 2) -- spread_level    
        if( self.dict['imMethod'] == 'spread_level (fast)' ):
            bBidPrice1 = self.ob.BestBidPrice().Get().Number()
            bAskPrice1 = self.ob.BestAskPrice().Get().Number()
                         
            # cancel if 
            # 1: orderbook not fully updated
            # 2: orderbook not complete
        
            # 1) -- orderbook not fully updated
            if( bBidPrice1 >= bAskPrice1 ):
                self.bBidPrice0 = 0
                self.bAskPrice0 = 99999999999999
                return False

            # 2) -- orderbook not complete
            if( isEmpty(bBidPrice1) or isEmpty(bAskPrice1) ):
                self.bBidPrice0 = 0
                self.bAskPrice0 = 99999999999999
                return False

   
            # check for market imbalance (bid side)
            if(bBidPrice1 > self.bAskPrice0 and (bBidPrice1 > self.bBidPrice0 + priceChange)  ):
                i = 0
                bidAgg = self.dict['imAggSameSide']
                askAgg = self.dict['imAggOpposideSide']
        
                while( self.timer.active and glActive and i < self.dict['imDuration'] ):
                    i += i
                
                    # smooth out if 'smooth' mode enabled
                    if( self.dict['imSmooth'] ):
                        bidAgg = self.dict['imAggSameSide'] + i * (self.dict['priceBidAgg'] - self.dict['imAggSameSide'])/self.dict['imDuration']
                        askAgg = self.dict['imAggOpposideSide'] + i * (self.dict['priceAskAgg'] - self.dict['imAggOpposideSide'])/self.dict['imDuration']
                                       
                    # config new order
                    arrival = self.selectArrivalTime() / 2    # double order arrivals
                    acm.Sleep( arrival * self.throttle )
                    side = self.selectDirectionMI( self.dict['imDirection'] )
                    volume = self.selectVolume()
                    price = self.selectPrice( side, bidAgg, askAgg)
            
                    # create order
                    order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
                    # throttle
                    self.sentOrder = order
            
                    # some printing (verbose)
                    if( self.dict['verbose'] ):
                        print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
                        
                # disable impact trigger for next generated order
                self.bBidPrice0 = 0
                self.bAskPrice0 = 99999999999999                        
                        
                return False

            # check for market imbalance (ask side)
            elif(bAskPrice1 < self.bBidPrice0 and (bAskPrice1 < self.bAskPrice0 - priceChange) ):
                i = 0
                bidAgg = self.dict['imAggSameSide']
                askAgg = self.dict['imAggOpposideSide']
        
                while( self.timer.active and glActive and i < self.dict['imDuration'] ):
                    i += i
                
                    # smooth out if 'smooth' mode enabled
                    if( self.dict['imSmooth'] ):
                        bidAgg = self.dict['imAggOpposideSide'] + i * (self.dict['priceBidAgg'] - self.dict['imAggOpposideSide'])/self.dict['imDuration']
                        askAgg = self.dict['imAggSameSide'] + i * (self.dict['priceAskAgg'] - self.dict['imAggSameSide'])/self.dict['imDuration']
                    
                    
                    # config new order
                    arrival = self.selectArrivalTime() / 2    # double order arrivals
                    acm.Sleep( arrival * self.throttle )
                    side = self.selectDirectionMI( 1.0 - self.dict['imDirection'] )
                    volume = self.selectVolume()
                    price = self.selectPrice( side, bidAgg, askAgg)
            
                    # create order
                    order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
                    # throttle
                    self.sentOrder = order
            
                    # some printing (verbose)
                    if( self.dict['verbose'] ):
                        print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))

                # disable impact trigger for next generated order
                self.bBidPrice0 = 0
                self.bAskPrice0 = 99999999999999

                return False

            # no order imballance detected
            else:
                # update prev. prices
                self.bBidPrice0 = bBidPrice1
                self.bAskPrice0 = bAskPrice1 
                return False  
            
            
        # 3) -- transaction_level   
        if( self.dict['imMethod'] == 'transaction_level (slow)' ):
            i = 0

            # create ticker here
            fArray = acm.FArray()
            fArray.Add(self.ob)
            tf = acm.FTradeFilter()
            tf.OrderBooks( fArray )
        
            maw = MovAvgWindow( self.dict['imSlidingWindow'] )
            ticker = tf.CreateSource(True)
            
            
            # loop until time is out
            while(  self.timer.active and glActive ):
        
                i += 1
            
                arrival = self.selectArrivalTime()
                acm.Sleep( arrival * self.throttle )
                side = self.selectDirection()
                volume = self.selectVolume()
            
                # determine price                
                midpoint = self.ob.SpreadAveragePrice().Get().Number()
                average = maw.getAverage(ticker, midpoint)
                tf.DestroySource(ticker)
                ticker = tf.CreateSource(True) # reset ticker                
                bidAgg = self.dict['priceBidAgg'] + average * self.dict['imSensitivity']
                askAgg = self.dict['priceAskAgg'] - average * self.dict['imSensitivity']
                price = self.selectPrice( side, bidAgg, askAgg )
            
                # create order
                order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
                # throttle
                self.sentOrder = order
                                
                if( bidAgg < -0.1 or askAgg < -0.1 ):
                    # nervous market - halt and reset
                    maw = MovAvgWindow( self.dict['imSlidingWindow'] )
                    acm.Sleep( 1000 )
            
                # some printing...
                # print ("average =", average)
                # print ("bidAgg =", bidAgg)
                # print ("askAgg =", askAgg)
                # print ("-------")
            
            
                # some printing (verbose)
                if( self.dict['verbose'] ):
                    print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
        
            # final words...
            print ('DONE: Spray --> ob:', self.ob.Name(), '  i:', i, '  timer:', self.timer.active, '  throttle:', self.throttle)

            return False

    
    
   #------------------------
    def selectArrivalTime(self):
        """arrival time when order arrives (in seconds)"""

        # provides a random sample from an exponential 
        # distribution with rate parameter lamb. Inside this 
        # method a single random (0,1) variate, U, is generated 
        # and then X = -(1.0/lambd)*ln(U) is returned. This 
        # gives a random sample from the exponential distribution 
        # with mean 1.0/lambd. We must specify the rate parameter 
        # lambd. lambd is 1.0/mean of the distribution.
        if( self.dict['arrivalTimeMean'] == 0 ):
            return 1
        else:
            t = random.expovariate(1.0/self.dict['arrivalTimeMean'])                
    
        return int( t )



    #------------------------
    def selectDirection(self):
        """select side (bid/ask) of next order"""

        if( self.dict['sideMethod'] == 'toggle' ):
            if( self.side == ASK ):
                self.side = BID
            else:
                self.side = ASK
                
        elif( self.dict['sideMethod'] == 'random' ):
            # random float: 0.0 <= number < 1.0
            if( self.dict['sideRandom'] > random.random() ):
                self.side = BID
            else:
                self.side = ASK
            
        elif( self.dict['sideMethod'] == 'bias' ):
            if( self.side == ASK ):
                bias = self.dict['sideBias']
            else:
                bias = - self.dict['sideBias']
        
            if( self.dict['sideRandom'] >= random.random() + bias ):
                self.side = BID
            else:
                self.side = ASK
        
        else:
            print ("ERROR: invalid side selection method name")
            
        return self.side
       



    #------------------------
    def selectDirectionMI(self, bidProb):
        """select side (bid/ask) of next order"""

        # random float: 0.0 <= number < 1.0
        if( bidProb > random.random() ):
            self.side = BID
        else:
            self.side = ASK
            
        return self.side
       


    #------------------------
    def selectPrice(self, direction, bidAgg, askAgg):
        """select price of order"""
        
        
        # **********************************************
        # ************ select price for bid ************
        # **********************************************
        # 101        
        # 100 <--- - - - - - - - - - - - - - - - 
        # 099                                  |
        # 098                                  |
        # 097                                  |
        # 086                                  |
        # 095 <--- - - - - - - - - -   bid aggressivness (1.0)
        # 094                      |           |
        # 093 <--- best ask        |           |
        # 092                      |           |
        # 091 <--- - - - - - - - - + - - - - - + - - - - 
        # 090 <--- midpt    price range (10) - -       |
        # 089                      |                   |
        # 088                      |                   |
        # 087 <--- best bid        |                   |
        # 086 <--- m               |         bid aggressivness (0.1)   m: ( midpt + (agg - 0.5)range )
        # 085 <--- - - - - - - - - -                   | 
        # 084                                          |
        # 083                                          |
        # 082                                          |
        # 081 <--- - - - - - - - - - - - - - - - - - - - 
        # 080
        
        
        bestBidPrice = self.ob.BestBidPrice().Get().Number()
        bestAskPrice = self.ob.BestAskPrice().Get().Number()
        lastPrice    = self.ob.LastPrice().Get().Number()
        
        while( bestBidPrice >= bestAskPrice ):
           # wait, order book needs to be updated
           acm.Sleep(20)
           bestBidPrice = self.ob.BestBidPrice().Get().Number()
           bestAskPrice = self.ob.BestAskPrice().Get().Number()
           
           
        # calculate midpoint (4 scenarious):
        # 1) full order book
        # 2) empty order book (both sides)
        # 3) empty bid side 
        # 4) empty ask side
        
        # first case
        midpoint = self.ob.SpreadAveragePrice().Get().Number()
        if( not isEmpty(midpoint) ):
            pass
            
        # second case
        if( isEmpty(bestBidPrice) and isEmpty(bestAskPrice) ):
                if (not isEmpty(lastPrice)) and ( int(lastPrice) != 1):
                    # use last price (if one exists)
                    midpoint = lastPrice
                else:
                    # use default price
                    midpoint = self.dict['priceDefault'] 
        
        # third case
        elif( isEmpty(bestBidPrice) ):
            #midpoint = bestAskPrice - DEFAULT_TICKS_SPR/2
            midpoint = bestAskPrice
            ticks = self.dict['priceDefaultSpread']/2 
            list = self.ob.TickSizeList()
            for i in range(ticks):
                midpoint = list.PrevTick(midpoint)
            
        # forth case
        elif( isEmpty(bestAskPrice) ):
            #midpoint = bestBidPrice + DEFAULT_TICKS_SPR/2
            midpoint = bestBidPrice
            ticks = self.dict['priceDefaultSpread']/2 
            list = self.ob.TickSizeList()
            for i in range(ticks):
                midpoint = list.NextTick(midpoint)
            
            
            
        # get new price
            # 1) calculate m'
            # 2) calculate price 
            # 3) round to tick price        
    
        price = 0
    
        if( self.dict['priceMethod'] == 'rectangular' ):
            # rectangular price method
            
            r = self.dict['priceRange']
            if( direction == BID ):
                m = midpoint + (bidAgg - 0.5) * r
            else:
                m = midpoint - (askAgg - 0.5) * r
            
            # calculate hi and low price points
            hi  = m + r/2.0
            low = m - r/2.0
            
            price = random.uniform(hi, low)
            
            
        elif( self.dict['priceMethod']== 'gaussian' ):
            # gaussian price method
        
            r = self.dict['priceStd'] * 2
            if( direction == BID ):
                m = midpoint + (self.dict['priceBidAgg'] - 0.5) * r
            else:
                m = midpoint - (self.dict['priceAskAgg'] - 0.5) * r
        
            price = random.gauss(m, self.dict['priceStd'])
            if( price < 0 ):
                price = 0
        else:
            # invalid price method
            print ('Error: invalid pricing method')
            price = 0

        return self.ob.RoundTick( price )
        
        

    #------------------------
    def selectVolume(self):
        """select size of order"""
    
        # generate gaussian random numbers
        # rounded to Round Lot sizes
        
        if( self.dict['volumeMethod'] == 'gaussian' ):
            volume = int( random.gauss(self.dict['volumeMean'], self.dict['volumeStd']) ) * self.ob.RoundLot()
        elif( self.dict['volumeMethod'] == 'rectangular' ):
            volume = int( random.uniform(self.dict['volumeMin'], self.dict['volumeMax'] + 1) ) * self.ob.RoundLot()
            
        if( volume <= 0 ):
            volume = self.ob.RoundLot()
        
        return volume
               
               

    #------------------------
    def startNormal(self, junk):
                
        i = 0 

        while(  self.timer.active and glActive ):
        
            i += 1
            
            self.obImballance()
            
            arrival = self.selectArrivalTime()
            acm.Sleep( arrival * self.throttle )
            side = self.selectDirection()
            volume = self.selectVolume()
            price = self.selectPrice( side, self.dict['priceBidAgg'], self.dict['priceAskAgg'] )
            
            # create order
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
            # throttle
            self.sentOrder = order
            
            # some printing (verbose)
            if( self.dict['verbose'] ):
                print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
        
        # final words...
        print ('DONE: Spray --> ob:', self.ob.Name(), '  i:', i, '  timer:', self.timer.active, '  throttle:', self.throttle)



    #------------------------
    def startTurbo(self, junk):
        """sends orders as fast as possible, ignoring 
           market impact pheonomon and arrival time processes"""        
            
        i = 0 
        while( self.timer.active and glActive ):
            
            print ("turbo...")
            i += 1
            arrival = 10 
            acm.Sleep(arrival)
            side = self.selectDirection()
            volume = self.selectVolume()
            price = self.selectPrice( side, self.dict['priceBidAgg'], self.dict['priceAskAgg'] )
            
            # create order
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
        
            # throttle
            self.sentOrder = order
                        
            acm.Sleep( 10 * self.throttle)
            print ("step 11...")
            # some printing
            if( self.dict['verbose'] ):
                print ('ob: %s, active: %s, side: %s, volume: %d, price: %d, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
            
            print ("step 12...")
            
        print ('STOPPED --- ob: %s, i: %d, timer: %s' % (self.ob.Name(), i, self.timer.active))
        print ('(final throttle setting: ' + str(self.throttle))
        
        
        
    #------------------------
    def startStopLoss(self, junk):
        """simulate a user defined price drop"""

        triggerTime = self.dict['slTriggerTime']
        bidSeverity = self.dict['slBidSeverity']
        askSeverity = self.dict['slAskSeverity']
        duration    = self.dict['slDuration']
        direction   = self.dict['slDirection']
        progressive = self.dict['slProgressive']
        origBidAgg  = self.dict['priceBidAgg']
        origAskAgg  = self.dict['priceAskAgg']
                
        tstart = time.time() # current time
        
        
        
        # ***********************
        # normal flow before trigger is activated
        # ***********************
        
        while( self.timer.active and glActive and ( time.time() < tstart + triggerTime ) ):
                        
            if( self.obImballance() ):
                pass
            
            # config new order
            arrival = self.selectArrivalTime()
            acm.Sleep( arrival * self.throttle )
            side = self.selectDirection()
            volume = self.selectVolume()
            price = self.selectPrice( side, self.dict['priceBidAgg'], self.dict['priceAskAgg'] )
            
            # create order
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
            # throttle
            self.sentOrder = order
            
            # some printing (verbose)
            if( self.dict['verbose'] ):
                print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
        
        
        # ***********************
        # stop loss triggered!
        # ***********************
        
        i = -1
        while( self.timer.active and glActive and i < duration):
            
            # volume remain intact, but
            # arrival time is halved and 
            # direction and aggression 
            # becomes affected (usrdefnd).
            
            i += 1
                      
            if( progressive ):
                print ("progressive!")
                bidSeverity = self.dict['slBidSeverity'] + i * (self.dict['priceBidAgg'] - self.dict['slBidSeverity'])/duration
                askSeverity = self.dict['slAskSeverity'] + i * (self.dict['priceAskAgg'] - self.dict['slAskSeverity'])/duration
                print ("bidSeverity", bidSeverity )
                print ("askSeverity", askSeverity )
                print ("-----------")
            

            # config new order
            arrival = self.selectArrivalTime() / 2    # double order arrivals
            acm.Sleep( arrival * self.throttle )
            side = self.selectDirectionMI( direction )
            volume = self.selectVolume()
            price = self.selectPrice( side, bidSeverity, askSeverity)
            
            # create order
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
            # throttle
            self.sentOrder = order
            
            # some printing (verbose)
            if( self.dict['verbose'] ):
                print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))

  
        # ***********************
        # overshoot
        # ***********************
        
        overshoot           = self.dict['slOvershoot']
        overshootDuration   = self.dict['slOvershootDuration']
        overshootBid        = self.dict['slOvershootBidAgg']
        overshootAsk        = self.dict['slOvershootAskAgg']
        overshootDirection  = self.dict['slOvershootDirection']
    
        i = -1 
        while( self.timer.active and glActive and i < overshootDuration and overshoot):
            i += 1
            print (" ** overshoot **")
            # config new order
            arrival = self.selectArrivalTime() / 2    # double order arrivals
            acm.Sleep( arrival * self.throttle )
            side = self.selectDirectionMI( overshootDirection )
            volume = self.selectVolume()
            price = self.selectPrice( side, overshootBid, overshootAsk)
            
            # create order
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
            # throttle
            self.sentOrder = order
            
            # some printing (verbose)
            if( self.dict['verbose'] ):
                print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
  
    
        # ***********************
        # return to normal again
        # ***********************
                
        while( self.timer.active and glActive ):
            
            if( self.obImballance() ):
                pass
            
            # config new order
            arrival = self.selectArrivalTime()
            acm.Sleep( arrival * self.throttle )
            side = self.selectDirection()
            volume = self.selectVolume()
            price = self.selectPrice( side, self.dict['priceBidAgg'], self.dict['priceAskAgg'] )
            
            # create order
            order = createAndSendOrder(self.tradingSession, self.ob, side, price, volume)
            
            # throttle
            self.sentOrder = order
            
            # some printing (verbose)
            if( self.dict['verbose'] ):
                print ('ob: %s, active: %s, side: %s, volume: %d, price: %F, t: %d' % (self.ob.Name(), self.timer.active, side, volume, price, arrival))
                
        print ('STOPPED stopLoss mode --- ob: %s, timer: %s' % (self.ob.Name(), self.timer.active))


