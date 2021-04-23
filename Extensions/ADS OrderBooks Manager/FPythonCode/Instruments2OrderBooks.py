""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ADSOrderBooksManager/./etc/Instruments2OrderBooks.py"
"""----------------------------------------------------------------------------------------------------------
MODULE
    Instruments2OrderBooks - This scripts generates order books for instruments based on user input.
    
DESCRIPTION
    This script generates order books for instruments and currency pairs present in database.
    The order book attributes are mapped based on the input provided by the user in the GUI. For example TickSizeList,
    Round Lot, DayCount. For currency pairs order books, these attributes are mapped from the data dictionary 'curr_pair_orderbook_data'
    defined in the script.
    
    The script also creates order book reference data in the database if such structures do not exist a priori, e.g. MarketPlace, MarketSegment, TickSizeList.
    
USER CUSTOMIZATION

    The user should maintain the data for Currency Pairs, TickSizeList, Market Capability in the script. 
    Refer to the doc string 'Data list to be maintained / extended by user' in this module.

VERSION
    2015.3.009
-------------------------------------------------------------------------------------------------------------"""
 
import acm
import FRunScriptGUI
from DealCaptureSetup import AddInfoSetUp
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger(name='Instruments2OrderBooks')


def StartDialog(eii):
    acm.RunModuleWithParameters("Instruments2OrderBooks", acm.GetDefaultContext())  


"""--------------------------------------------------------------------------------------------------------------------
Data list to be maintained / extended by user
--------------------------------------------------------------------------------------------------------------------"""
market_capability_list = ['01', '03', '04', '05', '06', '07', '12', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '52', '53', '54', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']


orderbook_tiering_level = [1, 2, 3, 4, 5, 6, 7, 8, 9]
orderbook_quotefactor = 1
orderbook_tradingstatus = 'NormalTrading'
orderbook_valuedate = 0
orderbook_migrationstatus = 0
orderbook_feedname = 'test'


tick_size_list_data = [
            {'TickSizeListId': '0025', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.0025},
            {'TickSizeListId': '00001', 'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.00001},
            {'TickSizeListId': '0001', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.0001},
            {'TickSizeListId': '00005', 'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.00005},
            {'TickSizeListId': '01', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.01},
            {'TickSizeListId': '0005', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.0005},
            {'TickSizeListId': '001', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.001},
            {'TickSizeListId': '10', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.10},
            {'TickSizeListId': '005', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.005},
            {'TickSizeListId': '5', 	'MinPrice':0, 	'MaxPrice':10000000000000, 	'TickSize':0.5},
        ]
curr_pair_orderbook_data = [
            {'Name': 'BAG/USD', 	'RoundLotSize':25000, 	        'TickSizeListId': '0025'},
            {'Name': 'XAG/USD', 	'RoundLotSize':25000, 	        'TickSizeListId': '0025'},
            {'Name': 'EUR/USD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'ZAU/EUR', 	'RoundLotSize':100, 	        'TickSizeListId': '01'},
            {'Name': 'CAD/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'USD/PLN', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'EUR/SEK', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'SAU/USD', 	'RoundLotSize':100, 	        'TickSizeListId': '10'},
            {'Name': 'USD/BRL', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'LZD/USD', 	'RoundLotSize':200, 	        'TickSizeListId': '01'},
            {'Name': 'ZAU/USD', 	'RoundLotSize':100, 	        'TickSizeListId': '01'},
            {'Name': 'BKQ/RUB', 	'RoundLotSize':100000, 	        'TickSizeListId': '0001'},
            {'Name': 'USQ/CAD', 	'RoundLotSize':100000, 	        'TickSizeListId': '00001'},
            {'Name': 'EUR/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '005'},
            {'Name': 'USD/KZA', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'EUR/PLN', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'USD/CNH', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'EUR/USA', 	'RoundLotSize':1000000, 	'TickSizeListId': '00001'},
            {'Name': 'AUQ/JPY', 	'RoundLotSize':100000, 	        'TickSizeListId': '001'},
            {'Name': 'ZAG/USD', 	'RoundLotSize':1000, 	        'TickSizeListId': '001'},
            {'Name': 'EUQ/USD', 	'RoundLotSize':100000, 	        'TickSizeListId': '00001'},
            {'Name': 'NZD/USD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'EUR/RUB', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'EUR/CAD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'USD/RUB', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'USD/HKD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00001'},
            {'Name': 'USD/JPA', 	'RoundLotSize':1000000, 	'TickSizeListId': '001'},
            {'Name': 'USD/SGD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00001'},
            {'Name': 'USD/KZT', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'AUD/CHF', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'EUQ/RUB', 	'RoundLotSize':100000, 	        'TickSizeListId': '0001'},
            {'Name': 'LZT/USD', 	'RoundLotSize':200, 	        'TickSizeListId': '01'},
            {'Name': 'GBP/NZD', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'CAD/CNH', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'GBP/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'GBP/AUD', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'EUQ/CHF', 	'RoundLotSize':100000, 	        'TickSizeListId': '00001'},
            {'Name': 'BKT/RUB', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'CNH/HKD', 	'RoundLotSize':5000000, 	'TickSizeListId': '0001'},
            {'Name': 'EUR/DKK', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'AUD/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'EUR/AUD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'GBP/USD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'USD/CAD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'GBP/CAD', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'GBP/USA', 	'RoundLotSize':1000000, 	'TickSizeListId': '00001'},
            {'Name': 'AUD/NZD', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'EUR/CZK', 	'RoundLotSize':1000000, 	'TickSizeListId': '001'},
            {'Name': 'USD/TRY', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'EUR/NZD', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'GBQ/USD', 	'RoundLotSize':100000, 	        'TickSizeListId': '00001'},
            {'Name': 'EUQ/JPY', 	'RoundLotSize':100000, 	        'TickSizeListId': '001'},
            {'Name': 'LPD/USD', 	'RoundLotSize':500, 	        'TickSizeListId': '5'},
            {'Name': 'USD/CHF', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'USD/NOK', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'AUD/CNH', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'SGD/CNH', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'USQ/JPY', 	'RoundLotSize':100000, 	        'TickSizeListId': '001'},
            {'Name': 'AUQ/USD', 	'RoundLotSize':100000, 	        'TickSizeListId': '00001'},
            {'Name': 'USD/KWD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00001'},
            {'Name': 'NZD/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'EUR/CHF', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'EUR/GBP', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'LPT/USD', 	'RoundLotSize':500, 	        'TickSizeListId': '5'},
            {'Name': 'NZD/CAD', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'XAU/USD', 	'RoundLotSize':1000, 	        'TickSizeListId': '10'},
            {'Name': 'GBP/CNH', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'USD/ILS', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'CNH/JPY', 	'RoundLotSize':5000000, 	'TickSizeListId': '0001'},
            {'Name': 'USD/SAR', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'CHF/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '01'},
            {'Name': 'AUD/CAD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'EUR/NOK', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'GBP/CHF', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'EUR/CNH', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'USQ/RUB', 	'RoundLotSize':100000, 	        'TickSizeListId': '0001'},
            {'Name': 'SAG/USD', 	'RoundLotSize':5000, 	        'TickSizeListId': '0025'},
            {'Name': 'EUR/RON', 	'RoundLotSize':1000000, 	'TickSizeListId': '0001'},
            {'Name': 'CAD/CHF', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'AUD/USD', 	'RoundLotSize':1000000, 	'TickSizeListId': '00005'},
            {'Name': 'USQ/CHF', 	'RoundLotSize':100000, 	        'TickSizeListId': '00001'},
            {'Name': 'CNH/MXN', 	'RoundLotSize':5000000, 	'TickSizeListId': '0001'},
            {'Name': 'USD/SEK', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'AUD/USA', 	'RoundLotSize':1000000, 	'TickSizeListId': '00001'},
            {'Name': 'USD/MXN', 	'RoundLotSize':1000000, 	'TickSizeListId': '0005'},
            {'Name': 'EUR/HUF', 	'RoundLotSize':1000000, 	'TickSizeListId': '001'},
            {'Name': 'SAU/EUR', 	'RoundLotSize':100, 	        'TickSizeListId': '10'},
            {'Name': 'USD/JPY', 	'RoundLotSize':1000000, 	'TickSizeListId': '005'},
        ]


     
class InsToOrderBook():
    """This class generates OrderBooks for Instruments specifed by user"""
    
    def __init__(self, market_place, market_segment, market_capability, default_tick_size_list, \
                        default_round_lot, default_day_counting, amas_location, amas_port, stored_query, external_id_type, orderbook_action, tiering_level):
        self.round_lot = default_round_lot
        self.day_count = default_day_counting
        self.tick_size_list = default_tick_size_list 
        self.market_place = market_place
        self.market_segment = market_segment
        self.market_capability = market_capability
        self.amas_location = amas_location
        self.amas_port = amas_port
        self.stored_query = stored_query
        self.external_id_type = external_id_type
        self.tiering_level = tiering_level
        self.db_ops = DBOperations()    
        self.commit_orderbook = orderbook_action[0]
        self.update_orderbook = orderbook_action[1]       

        
    def get_instruments_to_generate_orderbooks(self, stored_query):
        instruments = []
        if stored_query:
            instruments = self.db_ops.get_instruments_from_stored_query(self.stored_query)
        else:
            logger.ELOG("No query selected")  #maybe we should not give customer this option, if he wants that really, he will create a query for that. this avoids mistakes.
            #logger.DLOG("No stored query specified, selecting all instrumets from db")
            #instruments = acm.FInstrument.Select('')
        return instruments
        
    def define_orderbook_name(self, instrument, external_id_type):
        orderbook_name = None
        # Get data from instrumetn to map orderbook ExternalID
        external_id = self.db_ops.generate_orderbook_external_id(instrument, external_id_type)
        logger.DLOG("Orderbook:  %s=%s"%(external_id_type, external_id))
        if not external_id:
            logger.ELOG("Cannot generate Orderbook, as no data found to map orderbook name")
            return None
        
        orderbook_name = self.market_capability + external_id
       
        if len(str(orderbook_name)) >= 19:
            orderbook_name = str(orderbook_name)[:19]
            logger.WLOG("Orderbook ExternalID for instrument <%s> exceed 19 characters, trucating it to %s"%(instrument.Name(), orderbook_name))
        if self.tiering_level:
            logger.DLOG("Adding tiering level to orderbook name")
            orderbook_name = orderbook_name[:18] + str(self.tiering_level)
        return orderbook_name
        
    def get_orderbook_data(self, instrument):
        tick_size_list, round_lot, day_count = self.db_ops.get_data_from_orderbook(instrument)
        
        if not tick_size_list:
            tick_size_list = self.tick_size_list
        if not round_lot:
            round_lot = self.round_lot
        if not day_count:
            day_count = self.day_count
            
        return tick_size_list, round_lot, day_count
       
    def generate_orderbooks(self):
        """Generate orderbooks for selected instruments"""
        logger.DLOG("Generating orderbooks...")
        # Create marketplace in db if not exist
        market_place = self.db_ops.insert_market_place(self.market_place, self.amas_location, self.amas_port, self.commit_orderbook)
        # Create market segment in db if not exist
        market_segment = self.db_ops.insert_market_segment(self.market_place, self.market_segment, self.commit_orderbook) # no creation of new market segment if update
        
            
        if market_place and market_segment:
            # Get instruments to generate orderbooks for
            instruments = self.get_instruments_to_generate_orderbooks(self.stored_query)
            
            if not instruments:
                logger.ELOG("no instrument selected in query'%s'"%(self.stored_query))

            for each_instrument in instruments:
            
                orderbook_currency = each_instrument.Currency().Name()                
                orderbook_name = self.define_orderbook_name(each_instrument, self.external_id_type)
                if not orderbook_name:
                    logger.ELOG("**Cannot** generate Orderbook, as no ExternalId found to map")
                    continue

                # Check orderbook exist for instrument in db
                existing_orderbook = self.db_ops.get_orderbook_from_marketplace(each_instrument, market_place, orderbook_currency)
                if existing_orderbook:                    
                    
                    if self.update_orderbook:    
                        # update existing orderbook in database with new values or/and new leaf (market segment)
                        self.db_ops.update_orderbook(existing_orderbook, each_instrument, market_place, market_segment, self.market_capability, self.tick_size_list, \
                                    self.round_lot, self.day_count, orderbook_name, self.tiering_level, orderbook_currency)                        
                    
                    if self.commit_orderbook:
                        #this is for creating the a new leaf, if customer wants an orderbook to be listed in another leaf
                        group_map = self.db_ops.get_list_leaf(existing_orderbook, market_segment) 
                        if group_map and existing_orderbook.GroupMaps().IndexOf(group_map) <0 :
                            existing_orderbook.GroupMaps().Add(group_map) 
                            existing_orderbook.GroupMaps().Commit()   
                    
                else:
                    #This parts doesnt allow an orderbook to exist in in two different market segments on the same market. while for an organisational pupose
                    #traders needs to add it on two different segments. but the same orderbook same physicalMarketSegment but another leaf
                    # Check if same orderbook name is used for any other instrument orderbook
                    #orderbook_name_in_use = self.db_ops.check_orderbook_name_already_in_use(orderbook_name, market_place)
                    #if orderbook_name_in_use:
                    #    logger.LOG("**Cannot** create OrderBook. Orderbook ExternalID <%s> is already used for instrument <%s> in MarketPlace <%s>"%(orderbook_name, orderbook_name_in_use.Instrument().Name(), market_place.Name()))
                    #    continue
                    
                    if self.commit_orderbook or (not self.commit_orderbook and not self.update_orderbook):
                        logger.DLOG("Order book **does not exist** for instrument <%s>, MarketPlace <%s>.Creating it..."%(each_instrument.Name(), market_place.Name()))
                        # Get tick size, round lot and day count from another existing orderbook for same instrument
                        tick_size_list, round_lot, day_count = self.get_orderbook_data(each_instrument)
                        
                        self.db_ops.insert_orderbook(each_instrument, market_place, market_segment, self.market_capability, tick_size_list, \
                                        round_lot, day_count, orderbook_name, self.commit_orderbook, self.tiering_level, orderbook_currency)
                    
                    if self.update_orderbook and not self.commit_orderbook:
                        logger.WLOG("**Cannot** update orderbook for <%s> as it does not exist in database."%each_instrument.Name())     
    
                   
        else:
            if not market_place:logger.WLOG("Market place doesnt exist") 
            if not market_segment:logger.WLOG("Market segment doesnt exist") 
            


        
    def delete_orderbooks(self):
        """Delete orderbook for instruments that no longer exist to the selected stored query"""
        counter = 0 
        orderbooksListlen = 0 
        if self.stored_query:
            queryInstruments = self.db_ops.get_instruments_from_stored_query(self.stored_query)
        else:
            logger.LOG("If deleting all order books on all instruments, please write and quiery for that. You should be sure of what you are doing.")
         
        if queryInstruments:
            logger.DLOG("Deleting order books for instruments in market segment <%s> in the stored query <%s>"%(self.market_segment, self.stored_query))
            
            orderbooksList = []   
            if self.market_segment and self.market_place:
                for ob in acm.FOrderBook.Select("marketPlace='%s' "%(self.market_place)):#instrument, marketPlace, currency, externalType are indexes that can be used, the Oid also, but it s unique key index
                    for gmp in ob.GroupMaps():#check if there is a leaf on this orderbook                         
                        if gmp.Group().Name() == self.market_segment: 
                            orderbooksList.append(ob)
            orderbooksListlen =len(orderbooksList)
            if not orderbooksList:
                logger.LOG("No OrderBooks on Segment:'%s' and Market:'%s'"%(self.market_segment, self.market_place))            
            else:
                for each_orderbook in orderbooksList: 
                    if queryInstruments.Includes(each_orderbook.Instrument()):  
                        isDeleted = self.db_ops.Delete_SingleOrderBookWithReference(each_orderbook, self.market_segment)
                        if isDeleted:                            
                            counter=counter+1
                            
        logger.DLOG("**%s order books** were deleted for the following including '%s' instruments: %s"%(str(counter), str(orderbooksListlen), queryInstruments))
            
        
class FxToOrderBook():
    """This class generates OrderBooks for CurrencyPairs from database"""
    
    fx_pair_orderbook_type = ['EBS Market', 'EBS Direct']
        
    def __init__(self, market_place, market_segment, market_capability, default_tick_size_list, \
                            default_round_lot, default_day_counting, amas_location, amas_port, fx_orderbook_type, orderbook_action):
        self.fx_orderbook_type = fx_orderbook_type
        self.round_lot = default_round_lot
        self.day_count = default_day_counting
        self.tick_size_list = default_tick_size_list 
        self.market_place = market_place
        self.market_segment = market_segment
        self.market_capability = market_capability
        self.amas_location = amas_location
        self.amas_port = amas_port
        self.tiering_level = None
        self.db_ops = DBOperations()    
        self.commit_orderbook = orderbook_action[0] #bool
        self.update_orderbook = orderbook_action[1]
        
    def define_orderbook_name(self, curr_pair):
        order_book_name = None
        instrument = curr_pair.Currency1()
        instrument_curr = curr_pair.Currency2().Name()
        orderbook_curr = instrument_curr
        orderbook_id = instrument.Name() + '/' + orderbook_curr
        
        order_book_name = self.market_capability + orderbook_id + orderbook_curr
        if self.fx_orderbook_type == 'EBS Direct':
            order_book_name = self.market_capability + orderbook_id[0:(len(orderbook_id)-1)]+'Z' + \
                                orderbook_curr[0:(len(orderbook_curr)-1)]+'Z'
        return order_book_name
        
    def get_orderbook_data(self, curr_pair):
        instrument = curr_pair.Currency1()
        instrument_curr = curr_pair.Currency2().Name()
        orderbook_id = instrument.Name() + '/' + instrument_curr
        round_lot = None
        tick_size_list = None
        day_count = None
        for each_pair in curr_pair_orderbook_data:
            if each_pair['Name'] == orderbook_id:
                round_lot = each_pair['RoundLotSize'] 
                tick_size_list = self.market_capability + each_pair['TickSizeListId']
        if not round_lot:
            round_lot = self.round_lot
        if not tick_size_list:
            tick_size_list = self.tick_size_list
        if not day_count:
            day_count = self.day_count
        return tick_size_list, round_lot, day_count
                                          
    def generate_orderbooks(self):
        #create marketplace in db if not exist
        market_place = self.db_ops.insert_market_place(self.market_place, self.amas_location, self.amas_port, self.commit_orderbook)
        #create market segment in db if not exist
        market_segment = self.db_ops.insert_market_segment(self.market_place, self.market_segment, self.commit_orderbook)
    
        currency_pairs = self.db_ops.get_currency_pairs()
        
        for each_pair in currency_pairs:
            orderbook_ins = each_pair.Currency1()
            orderbook_currency = each_pair.Currency2().Name()
            
            orderbook_name = self.define_orderbook_name(each_pair)
            if not orderbook_name:
                continue
                
            # Get tick size, round lot and day count from another existing orderbook for same instrument
            tick_size_list, round_lot, day_count = self.get_orderbook_data(each_pair)
        
            # Check orderbook exist for instrument in db
            existing_orderbook = self.db_ops.get_orderbook_from_marketplace(orderbook_ins, market_place, orderbook_currency)
            if existing_orderbook:
                if self.update_orderbook:
                    # update existing orderbook in database
                    self.db_ops.update_orderbook(existing_orderbook, orderbook_ins, market_place, market_segment, self.market_capability, tick_size_list, \
                                round_lot, day_count, orderbook_name, self.tiering_level, orderbook_currency)
                                
                if self.commit_orderbook:
                    #this is for creating the a new leaf, if customer wants an orderbook to be listed in another leaf
                    group_map = self.db_ops.get_list_leaf(existing_orderbook, market_segment) 
                    if group_map and existing_orderbook.GroupMaps().IndexOf(group_map) <0 :
                        existing_orderbook.GroupMaps().Add(group_map) 
                        existing_orderbook.GroupMaps().Commit()   
                            
            else:
                # Check if same orderbook name is used for any other instrument orderbook
                #orderbook_name_in_use = self.db_ops.check_orderbook_name_already_in_use(orderbook_name, market_place)
                #if orderbook_name_in_use:
                #    logger.LOG("Cannot create OrderBook. Orderbook ExternalID <%s> is already in use in MarketPlace <%s>"%(orderbook_name,  market_place.Name()))
                #    continue
                    
                if self.commit_orderbook or (not self.commit_orderbook and not self.update_orderbook):
                    logger.DLOG("Order book does not exist for instrument <%s>, MarketPlace <%s>"%(orderbook_ins.Name(), market_place.Name()))
                    self.db_ops.insert_orderbook(orderbook_ins, market_place, market_segment, self.market_capability, tick_size_list, \
                                    round_lot, day_count, orderbook_name, self.commit_orderbook, self.tiering_level, orderbook_currency)
                                    
                if self.update_orderbook and not self.commit_orderbook:
                    logger.WLOG("Cannot update orderbook for <%s> as it does not exist in database."%orderbook_ins.Name())

    def delete_orderbooks(self):
        """Delete orderbook for instruments that no longer exist to the selected stored query"""
        logger.DLOG("Deleting all FX order books for instruments in market segment <%s>"%(self.market_segment))
        counter = 0 
        orderbooksList = []   
        if self.market_segment and self.market_place:
            for ob in acm.FOrderBook.Select("marketPlace='%s' "%(self.market_place)):#instrument, marketPlace, currency, externalType are indexes that can be used, the Oid also, but it s unique key index
                for gmp in ob.GroupMaps():#check if there is a leaf on this orderbook                         
                    if gmp.Group().Name() == self.market_segment:
                        orderbooksList.append(ob)
        if not orderbooksList:
            logger.LOG("No OrderBooks on Segment:'%s' and Market:'%s'"%(self.market_segment, self.market_place))            
        else:
            for each_orderbook in orderbooksList:  
                isDeleted = self.db_ops.Delete_SingleOrderBookWithReference(each_orderbook, self.market_segment)
                if isDeleted:                            
                    counter=counter+1
                            
        logger.DLOG("**%s order books** were deleted fron the market segment leaf: %s"%(str(counter), self.market_segment))
    
        
class DBOperations():
    def __init__(self):
        pass
        
    def get_market_places(self):
        market_list = []
        for party in acm.FParty.Select("type=5"):
            market_list.append(party.Name())
        market_list.sort()
        return market_list
        
    def get_market_segments(self, market_place=None,market_segment=None):  
        #indexes: oid  superGroup name, primary keys: oid
        segment_list = []
        
        if not market_place and not market_segment:
            selection = acm.FMarketSegment.Select('')
        elif not market_place:
            selection = acm.FMarketSegment.Select("name='%s'" %(market_segment))
        elif not market_segment:
            selection = acm.FMarketSegment.Select("superGroup='%s'" %(market_place))
        else:
            selection = acm.FMarketSegment.Select("superGroup='%s' and name='%s'" %(market_place, market_segment))        

        for each_segment in selection:
            segment_list.append(each_segment.Name())

        return sorted(segment_list)
        
    def get_instruments_from_stored_query(self, stored_query):
        logger.DLOG("Getting instruments from query <%s>..." % stored_query)
        instruments = acm.FArray()
        acm_query = acm.FStoredASQLQuery[stored_query]
        if acm_query:
            if acm_query.SubType() == 'FInstrument':
                instruments = acm_query.Query().Select()
            if acm_query.SubType() == 'FOrderBook':
                orderbooks = acm_query.Query().Select()
                for each_orderbook in orderbooks:
                    instruments.Add(each_orderbook.Instrument())
        return instruments
        
    def get_stored_queries(self):
        list_queries_str = []
        for sq in acm.FStoredASQLQuery.Select('cid=30 and subType = FInstrument')[:]:
            list_queries_str.append(sq.Name())
        for sq in acm.FStoredASQLQuery.Select('cid=30 and subType = FOrderBook')[:]:
            list_queries_str.append(sq.Name())
        list_queries_str.sort()
        return  list_queries_str
    
    def get_currency_pairs(self):
        currency_pairs = None
        currency_pairs = acm.FCurrencyPair.Select('')
        return currency_pairs
        
    def get_data_from_orderbook(self, instrument):
        """Get ticksizelist, roundlot and daycount from an alrady existing orderbook for an Instrument"""
        logger.DLOG("Getting ticksize, roundlot and daycount from other existing order book for instrument %s" %instrument.Name())
        orderbook = acm.FOrderBook.Select('instrument=%s' % instrument.Oid())
        if orderbook:
            temp_orderbook = orderbook[0]
            logger.DLOG("Reading data from already existing order book <%s> for Instrument <%s>" %(temp_orderbook.Name(), instrument.Name()))
            return temp_orderbook.TickSizeList().Name(), temp_orderbook.RoundLot(), temp_orderbook.DayCounting()
        return None, None, None
        
    def get_round_lot(self, instrument, round_lot):
        if instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']:
            round_lot = instrument.ContractSize()
        return round_lot
        
    def generate_orderbook_external_id(self, instrument, external_id_type):
        logger.DLOG("Getting external id type <%s> data for order book" % external_id_type)
        id_name = None
        
        if str(external_id_type).upper() == 'INSID':
            id_name = instrument.Name()
            
        elif str(external_id_type).upper() == 'ISIN':
            if instrument.Isin():
                id_name =  instrument.Isin()
            else:
                logger.ELOG("**No Isin found** for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name())
                
        elif str(external_id_type).upper() == 'EXTERN_ID1':
            if instrument.ExternalId1():
                id_name =  instrument.ExternalId1()
            else:
                logger.ELOG("**No ExternalId1** found for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name())
                
        elif str(external_id_type).upper() == 'EXTERN_ID2':
            if instrument.ExternalId2():
                id_name = instrument.ExternalId2()
            else:
                logger.ELOG("**No ExternalId2** found for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name())
                
        elif str(external_id_type).upper() == 'ISIN + CURRENCY':
            if instrument.Isin():
                id_name = instrument.Isin() + instrument.Currency().Name()
            else:
                logger.ELOG("**No Isin** found for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name())
                
        elif str(external_id_type).upper() == 'BB_UNIQUE + CURRENCY':
            for t in instrument.Aliases():
                if t.Type().Name() == 'BB_UNIQUE' and t.Alias():
                    id_name = t.Alias() + instrument.Currency().Name()  
            if id_name == None:
                logger.ELOG("**No BB_UNIQUE** found for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name()) 
 
        elif str(external_id_type).upper() == 'BB_GLOBAL + CURRENCY':
            for t in instrument.Aliases():
                if t.Type().Name() == 'BB_GLOBAL' and t.Alias():
                    id_name = t.Alias() + instrument.Currency().Name()   
            if id_name == None:
                logger.ELOG("**No BB_GLOBAL** alias found for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name()) 
                
        elif str(external_id_type).upper() == 'BB_TICKER + CURRENCY':
            for t in instrument.Aliases():
                if t.Type().Name() == 'BB_TICKER' and t.Alias():
                    id_name = t.Alias() + instrument.Currency().Name()   
            if id_name == None:
                logger.ELOG("**No BB_TICKER** alias found for Instrument <%s>, Cannot map Orderbook ExternalId"%instrument.Name()) 

        return id_name
        
    def get_tick_size_list(self, tick_size_list, market_capability ):
        """Get specified tick size list from database. If tick size list not specified, return all tick size lists from database"""
        logger.DLOG("Retrieving tick size list %s" % tick_size_list)
        tick_size_list_in_db = None
        
        if tick_size_list:
            tick_size_list_in_db = acm.FTickSizeList.Select01("name='%s'" % int(tick_size_list), 'tick size list not found')
            if not tick_size_list_in_db:
                logger.WLOG("TickSizeList %s not found in database."%tick_size_list)
                new_tick_size_list = self.insert_tick_size_list(tick_size_list)
                if new_tick_size_list:
                    self.insert_tick_size_interval(new_tick_size_list, market_capability)
                    return new_tick_size_list.Name()
                else:
                    return tick_size_list.Name()
            else:
                return tick_size_list_in_db.Name()
        else:
            for tick_size in acm.FTickSizeList.Select(''):
                tick_size_list.append(tick_size.Name())
            tick_size_list.sort()
            return tick_size_list
            
    def insert_market_place(self, market_place, location, data_source, commit_new = False):
        market = None
        if market_place:
            acm_market_place = acm.FMarketPlace[market_place]
            if not acm_market_place and commit_new:
                logger.WLOG("**Market %s not found** in db" % str(market_place))
                new_market = acm.FMarketPlace()
                new_market.Name  = market_place
                new_market.Location  = location
                new_market.DataSource  = data_source
                new_market.Commit()
                market = new_market
                logger.LOG("*Created* Market Place %s" %(market_place))
            else:
                logger.DLOG("Market place %s *found* in db.Updating.."%market_place)
                clone_market = acm_market_place.Clone()
                clone_market.Location  = location
                clone_market.DataSource  = data_source
                acm_market_place.Apply(clone_market)
                acm_market_place.Commit()
                market = acm_market_place
                
        return market
        
    def insert_market_segment(self, market_place, market_segment, create_new = False):
        segment = None
        if market_segment and market_place:
            acm_market_segment = self.get_market_segments(market_place, market_segment)
            if not acm_market_segment and create_new: # indexes: oid   superGroup name   foreign keys: marketPlace superGroup
                logger.WLOG("MarketSegment <%s> with Market <%s> *not found* in db. Creating new.."% (market_segment, market_place))
                page_group = None
                if not acm.FPageGroup[market_place]:
                    new_page_group = acm.FPageGroup()
                    new_page_group.Name = market_place
                    new_page_group.Commit()
                    page_group = new_page_group
                    logger.LOG("Created page group %s" %(market_place))
                else:
                    page_group = acm.FPageGroup[market_place]
                    
                if page_group:
                    new_market_segment = acm.FMarketSegment()
                    new_market_segment.Name = market_segment
                    new_market_segment.SuperGroup = page_group
                    new_market_segment.MarketPlace = market_place
                    new_market_segment.Terminal(True) 
                    new_market_segment.Commit()
                    logger.LOG("Created market segment %s" %(market_segment))
                    segment = new_market_segment
            else:
                logger.DLOG("Market segment %s *found* in db"%market_segment)
                segment = acm.FMarketSegment.Select01("superGroup='%s' and name='%s'" %(market_place, market_segment), 'market segment not found')
        return segment
        
    def insert_tick_size_interval(self, tick_size_list, market_capability):
        tick_size_interval_max = 10000000000000
        tick_size_interval_min = 0
        increment = 0.01
        tick_size_list_id = []
        
        tick_size_list_db = acm.FTickSizeList.Select01("oid=%s"%tick_size_list.Oid(), 'TickSizeList not found')
        if tick_size_list_db:
            for tick_size_data in tick_size_list_data:
                tick_size_list_id = market_capability + tick_size_data['TickSizeListId']
                if  tick_size_list_id == tick_size_list_db.Name():
                    tick_size_interval_min = tick_size_data['MinPrice']
                    tick_size_interval_max = tick_size_data['MaxPrice']
                    increment = tick_size_data['TickSize']
                    break

            acm_obj = acm.FTickSizeInterval()
            acm_obj.Max = float(tick_size_interval_max)
            acm_obj.Min = float(tick_size_interval_min)
            acm_obj.TickSize = float(increment)
            acm_obj.TickSizeList = tick_size_list_db
            try:
                acm_obj.Commit()
                logger.LOG('Committed TickSizeInterval')
            except Exception as e:
                logger.ELOG("Cannot commit TickSizeInterval %s" %str(e))
                
    def get_tick_size_lists(self):
        tick_size_list = []
        for ln in acm.FTickSizeList.Select(''):
            tick_size_list.append(ln.Name())
        tick_size_list.sort()
        return tick_size_list
                
    def insert_tick_size_list(self, tick_size_list_name):
        #Create new acm TickSizeList 
        acm_obj = acm.FTickSizeList()
        acm_obj.Name = int(tick_size_list_name)
        try:
            acm_obj.Commit()
            logger.LOG('Created new TickSizeList %s'%tick_size_list_name)
            return acm_obj
        except Exception as e:
            logger.ELOG('Error while creating new TickSizeList %s : %s'%(tick_size_list_name, str(e)))
            return None
            
    def check_orderbook_name_already_in_use(self, orderbook_name, market_place):
        existing_orderbook = None
        # Check if same ExtrenalId orderbook exist in database within selected market place
        if market_place and orderbook_name:
            logger.DLOG("Checking if order book exists with ExternalId <%s> within market place <%s>"%(orderbook_name, market_place.Name()))
            for orderbook in market_place.OrderBooks():
                if orderbook.ExternalId() == orderbook_name:
                    existing_orderbook = orderbook
                    
        return existing_orderbook
            
    def get_orderbook_from_marketplace(self, instrument, market, currency):
        existing_orderbook = None
        if market and instrument:
            logger.DLOG("Checking if an order book exists in the db for the instrument <%s> within the MarketPlace <%s>"%(instrument.Name(), market.Name()))
            orderbook = acm.FOrderBook.Select("instrument=%s and marketPlace='%s'" % (instrument.Oid(), market.Name())) #no physicalMarketSegment should be used. explanation is later in the processing.
            if orderbook:
                for each_orderbook in orderbook:
                    if each_orderbook.Currency().Name() == currency:
                        existing_orderbook = each_orderbook
                        break
            if existing_orderbook:
                logger.LOG("An order book *exists* for the instrument <%s> in the  MarketPlace <%s>"%(instrument.Name(), market.Name()))

        return existing_orderbook
        
        
    def insert_orderbook(self, instrument, market_place, market_segment, market_capability, tick_size_list, \
                                            round_lot, day_counting, orderbook_name, commit_orderbook, tiering_level, orderbook_curr=None):
        """Create new orderbooks in database based on provided data"""
        logger.DLOG("Insert orderbook...")  
        try:
            new_ob_obj = acm.FOrderBook()
            new_ob_obj.Instrument = instrument
            if orderbook_curr:
                new_ob_obj.Currency = orderbook_curr
            else:
                new_ob_obj.Currency = instrument.Currency()
                
            new_ob_obj.Quotation = instrument.Quotation()                
            new_ob_obj.TickSizeList = self.get_tick_size_list(tick_size_list, market_capability)
            new_ob_obj.RoundLot = self.get_round_lot(instrument, round_lot)
            new_ob_obj.DayCounting = day_counting
            new_ob_obj.MarketPlace = market_place
            new_ob_obj.PhysicalMarketSegment(market_segment)
            new_ob_obj.Cid = 504
            new_ob_obj.QuoteFactor = orderbook_quotefactor
            new_ob_obj.TradingStatus = orderbook_tradingstatus
            new_ob_obj.ValueDate = orderbook_valuedate
            new_ob_obj.MigrationStatus = orderbook_migrationstatus
            new_ob_obj.FeedName = orderbook_feedname
            new_ob_obj.ExternalId = orderbook_name
            new_ob_obj.ExternalType = market_capability
            if str(tiering_level):
                new_ob_obj.ExternalType = tiering_level
                
            if commit_orderbook:
                new_ob_obj.Commit()
                group_map = self.get_list_leaf(new_ob_obj, market_segment)
                new_ob_obj.GroupMaps().Add(group_map)   
                new_ob_obj.GroupMaps().Commit()
                
            logger.LOG("**Successfully** commited orderbook <%s> for Instrument <%s>"%(orderbook_name, instrument.Name()))
        except Exception as e:
            logger.ELOG("**Cannot commit** orderbook for Instrument <%s>"%instrument.Name())
            logger.ELOG("**Error**:%s"%str(e), exc_info=1)
       
    def get_list_leaf_existance(self, orderbook, virtual_market_segment=None):
        """
            This will mostly get a single item list of the unique leaf correspondant to the virtual market segment if virtual_market_segment is given
            otherwise will return the whole list of leafs on a market where the orderbook is created
        """
        if virtual_market_segment and virtual_market_segment != "" :
            all_insGroupMaps =acm.FInstrGroupMap.Select("instrument='%s' and orderBook='%s' and group='%s' "%(orderbook.Instrument().Oid(), orderbook.Oid(), virtual_market_segment)) #oid, group, instrument, orderBook are unique indexes
        else:
            all_insGroupMaps =acm.FInstrGroupMap.Select("instrument='%s' and orderBook='%s'"%(orderbook.Instrument().Oid(), orderbook.Oid()))

        if len(all_insGroupMaps) == 0:
            leaf_exists = 0
        elif len(all_insGroupMaps) == 1:    
            leaf_exists = 1
        elif len(all_insGroupMaps) >  1 :       
            leaf_exists = 2
            
        return (leaf_exists, all_insGroupMaps)
    
    
    def get_list_leaf(self, orderbook, virtual_market_segment):
        """this function will mostly create a new leaf or just get the only one existant"""
        
        leaf = None
        for gmp in orderbook.GroupMaps():#check if there is a leaf on this orderbook
            if gmp.Group().Name() == virtual_market_segment.Name():
                leaf  = gmp         
                break                          
                       
        if not leaf:
            try:               
                leaf = acm.FInstrGroupMap()                
                leaf.Instrument(orderbook.Instrument())
                leaf.Group(virtual_market_segment)
                leaf.OrderBook(orderbook)
                #leaf.Commit()
                logger.LOG("Leaf %s *Successfully* created  for  order book <%s>"%(virtual_market_segment.Name(), orderbook.Name()))
            except Exception as e:
                logger.ELOG('**Error** while creating a leaf for the order book %s on market segment %s : %s'%(orderbook.Name(), virtual_market_segment.Name(), e))
        else: 
            logger.DLOG("Sending first match of an FInstrGroupMap for MarketSegment '%s' (FInstrGroupMap) for the order book '%s'."%(virtual_market_segment.Name(), orderbook.Name()))  
        
        return leaf


    def Delete_SingleOrderBookWithReference(self, orderbook, virtual_market_segment):
        """
        Deleting market segment leaf (not the physical one), if all are deleted. delete the orderbook record.
        """
        deleted=0 
        (leaf_exists, all_insGroupMaps)=self.get_list_leaf_existance(orderbook)

        try:        
            if leaf_exists == 1:
                insGroupMap =all_insGroupMaps[0]                
                insGroupMap.Delete()
                orderbook.Delete()
                orderbook.Changed()
                deleted=1
                logger.LOG("Reference deleted for orderbookId:'%s' on leaf market segment: %s"%(orderbook.Name(), virtual_market_segment))           
                logger.LOG("**Deleted order book** <%s> for instrument <%s>"%(orderbook.Name(), orderbook.Instrument().Name()))
            elif leaf_exists ==0:         
                orderbook.Delete()
                orderbook.Changed()
                deleted=1
                logger.DLOG("No market segment (FInstrGroupMap) reference associated with orderbook:'%s'."%(orderbook.Name()))
                logger.LOG("**Deleted order book** <%s> for instrument <%s>"%(orderbook.Name(), orderbook.Instrument().Name()))
            else: #Take the exact match now , with market segment
                (leaf_exists, all_insGroupMaps)=self.get_list_leaf_existance(orderbook, virtual_market_segment)
                insGroupMap =all_insGroupMaps[0]
                insGroupMap.Delete()
                deleted=1
                logger.LOG("**Deleted** reference for orderbook <%s> for instrument <%s> on the market %s"%(orderbook.Name(), orderbook.Instrument().Name(), virtual_market_segment))
                
        except Exception as e:                     
            logger.ELOG("Could not delete  the orderbook %s record. Error:%s"%(orderbook.Name(), e))
   
        return deleted
        
    def update_orderbook(self, existing_orderbook_obj, instrument, market_place, market_segment, market_capability, \
                        tick_size_list, round_lot, day_count, orderbook_name, tiering_level, orderbook_curr=None):
        """Update already existing orderbooks in database"""
        logger.DLOG("Updating orderbook...") 
        clone_obj = existing_orderbook_obj.Clone()
        clone_obj.Instrument = instrument
        if orderbook_curr:
            clone_obj.Currency = orderbook_curr
        else:
            clone_obj.Currency = instrument.Currency()
        clone_obj.Quotation = instrument.Quotation()
        clone_obj.MarketPlace = market_place
        clone_obj.RoundLot = self.get_round_lot(instrument, round_lot)
        #clone_obj.PhysicalMarketSegment(market_segment)
        clone_obj.Name = orderbook_name
        clone_obj.QuoteFactor = 1
        clone_obj.TickSizeList = self.get_tick_size_list(tick_size_list, market_capability)
        if str(tiering_level):
            clone_obj.ExternalType = tiering_level
        clone_obj.ExternalId = orderbook_name

        try: 
            existing_orderbook_obj.Apply(clone_obj)
            existing_orderbook_obj.Commit()  
            
            #group_map = self.get_list_leaf(clone_obj,market_segment) 
            #if group_map and clone_obj.GroupMaps().IndexOf(group_map) <0 :
            #    clone_obj.GroupMaps().Add(group_map) 
            #    clone_obj.GroupMaps().Commit()   
         
            logger.LOG("**Successfully** updated orderbook information: <%s> for instrument <%s>"%(orderbook_name, instrument.Name()))
        except Exception as e:
            logger.ELOG('**Error** while updating OrderBook %s : %s'%(orderbook_name, e))
               
            
class OrderBookAelVariables(FRunScriptGUI.AelVariablesHandler):
    """This class defines the ael_variables to create a GUI for user input"""
    field_mandatory_index = 5
    tt_market_place = """Select market place for order book creation. If you type in an entry, it will be created with corresponding parameters (AMAS Port and Location)"""
    tt_market_segments = """Select market segment for order book creation. If you type in an entry, a new market segment will be created. Note that more than one order book cannot exist on the same market with different market segments."""
    tt_capability = """The market capability to use. By default, 16 (AMAS-FIXToolkit2)."""
    tt_round_lot = """The default order book round lot. By default, 1"""
    tt_day_count = """The default order book day counting. By default, 0."""
    tt_tick_size = """The default order book tick size list. By default, 1000."""
    
    tt_amas_port = """The AMS port for the selected market place"""
    tt_amas_location = """The AMS location (host) for the selected market place. """
    tt_gen_bbg_addfields = """Generate additional info fields on order books to be used for Bloomberg contributions' \
                              '(Row number, Sub page number, Page number, Page id). Only available when market capability is set to 76-FIX_CONTRIBUTION."""
    tt_stored_query = """Select an ASQL query from the set of stored queries. \n \n Instrument queries will generate order books for instruments in the query. Order book queries will fetch instruments from orderbooks defined in the query and it will specifically generate orderbooks for the same instruments in selected MarketPlace and Marktet Segment."""
    tt_external_id = """Select order book external ID type. ExternalId Type refers to AMB OrderBookId. The market capability will be added to the beginning of the external ID.\n \n
                            
                            *INSID : Instrument name is used to generate order book external ID type.                                             \
                            *ISIN : Instrument ISIN is used to generate order book external ID type.                                              \
                            *EXTERNAL_ID1 : Instrument ExternalID1 is used to generate order book external ID type.                               \
                            *EXTERNAL_ID2 : Instrument ExternalID2 is used to generate order book external ID type.                               \
                            *ISIN + CURRENCY : Instrument ISIN along with the currency is used to generate order book external ID type."""
                            
    
    tt_fx_orderbook = """Create order books for currency pairs in database. When generating order books for currency pairs the tick size list and round lot are mapped from data dictionary 'curr_pair_orderbook_data' defined in the script."""
    tt_fx_orderbook_type = """The type of order books to create for FX pairs. Only applicable when Create FX Orderbooks is toggled."""
    tt_logging_level = """The verbosity level of log messages."""
    
    tt_log_to_file = """Select this check box to write the log output to a file."""
    tt_log_file_path = """The path to the output file. Only available when the Log to File check box is selected"""
    tt_tiering = """Select this check box if tiering should be mapped to the order books."""
    tt_tiering_level = """The order book tiering level. The tiering number will be suffixed to the order book name and will also be mapped as the order book external type. Only available when tiering is selected."""
    
    tt_commit_orderbooks = """Select this check box to commit the order books in the database if they do not exist."""
    tt_update_orderbooks = """Select this check box to update the order books if they already exist in the database."""
    tt_delete_orderbooks = """Select this check box to delete order books (from the specified market segment) for instruments that no longer are a part of the selected stored query."""   
    
    def set_market_segements(self, index, fieldValues):
        market_segments = self.db_ops.get_market_segments(fieldValues[index])
        self.ael_variables.segment[3] = market_segments
        self.ael_variables.segment.set(fieldValues, '')
        
        if fieldValues[index]:
            acm_market_place = acm.FMarketPlace[fieldValues[index]]
            if acm_market_place:
                self.ael_variables.location.set(fieldValues, acm_market_place.Location())
                self.ael_variables.data_source.set(fieldValues, acm_market_place.DataSource())

        return fieldValues
        
    def enable_disable_fx_fields(self, index, fieldValues):
        enable = str(fieldValues[index]) != 'false'
        
        # Enable FX Orderbook Type
        self.ael_variables.fx_orderbook_type.enable(enable)
        self.ael_variables.commit_fx_ob.enable(enable)
        self.ael_variables.update_fx_ob.enable(enable)
        
        # Disable instrument tab fields
        self.ael_variables.stored_query.enable(not(enable))
        self.ael_variables.commit_ob.enable(not(enable))
        self.ael_variables.update_ob.enable(not(enable))
        self.ael_variables.delete_ob.enable(not(enable))
        self.ael_variables.external_id_type.enable(not(enable))
        
        self.ael_variables.enable_tiering.enable(not(enable))
        if enable:
            self.ael_variables.enable_tiering.set(fieldValues, not(enable))
            self.enable_disable_tiering_fields(self.ael_variables.enable_tiering.sequenceNumber, fieldValues)
        
        return fieldValues 
        
    def enable_disable_tiering_fields(self, index, fieldValues):
        enable = str(fieldValues[index]) not in ['false', 'False']
        self.ael_variables.tiering_number.enable(enable)
        
        return fieldValues
        
    def enable_disable_log_file(self, index, fieldValues):
        enable = str(fieldValues[index]) not in ['false', 'False']
        self.ael_variables.log_to_file.enable(enable)
        
        return fieldValues

    def enable_disable_commit_ob(self, index, fieldValues):
    
        if fieldValues[index] == 'true' :
            self.ael_variables.delete_ob.set(fieldValues, False)           

        return fieldValues

    def enable_disable_update_ob(self, index, fieldValues):
    
        if fieldValues[index] == 'true' :
            self.ael_variables.delete_ob.set(fieldValues, False)          

        return fieldValues

    def enable_disable_delete_ob(self, index, fieldValues):
        if fieldValues[index] == 'true' :
            self.ael_variables.commit_ob.set(fieldValues, False)   
            self.ael_variables.update_ob.set(fieldValues, False)   
        
        return fieldValues

    def enable_disable_commit_fx_ob(self, index, fieldValues):
    
        if fieldValues[index] == 'true' :
            self.ael_variables.delete_fx_ob.set(fieldValues, False)           

        return fieldValues

    def enable_disable_update_fx_ob(self, index, fieldValues):
    
        if fieldValues[index] == 'true' :
            self.ael_variables.delete_fx_ob.set(fieldValues, False)          

        return fieldValues

    def enable_disable_delete_fx_ob(self, index, fieldValues):
        if fieldValues[index] == 'true' :
            self.ael_variables.commit_fx_ob.set(fieldValues, False)   
            self.ael_variables.update_fx_ob.set(fieldValues, False)   
        
        return fieldValues

    def enable_disable_bbg_specifics(self, index, fieldValues):
    
        if fieldValues[index] == '76-FIX_CONTRIBUTION' :     
            self.ael_variables.gen_bbg_addfields.enable(True)
        else:
            self.ael_variables.gen_bbg_addfields.enable(False)
            
        return fieldValues
        
    def external_id_types(self):
        external_id_list = []
        external_id_list.append('ISIN + CURRENCY') 
        external_id_list.append('INSID')       
        external_id_list.append('ISIN')                  
        external_id_list.append('EXTERNAL_ID1')        
        external_id_list.append('EXTERNAL_ID2') 
        external_id_list.append('BB_UNIQUE + CURRENCY')
        external_id_list.append('BB_GLOBAL + CURRENCY')
        external_id_list.append('BB_TICKER + CURRENCY')
        return external_id_list
        
    def __init__(self):
        self.db_ops = DBOperations()
        variables = [
                ['market_capability', 'Market Capability_Market', 'string', market_capability_list, '16', 1, 0, self.tt_capability, self.enable_disable_bbg_specifics],
                ['market_place', 'Market Place_Market', 'string', self.db_ops.get_market_places(), '', 1, 0, self.tt_market_place, self.set_market_segements],
                ['segment', 'Market Segment_Market', 'string', [], '', 1, 0, self.tt_market_segments, None, 1],                
                ['default_round_lot', 'Default Round Lot_Market', 'int', None, 1, 1, '', self.tt_round_lot],
                ['default_day_counting', 'Default Day Counting_Market', 'int', None, 0, 1, '', self.tt_day_count],
                ['default_tick_size_list', 'Default Tick Size List_Market', 'string', self.db_ops.get_tick_size_lists(), 1000, 1, 0, self.tt_tick_size, None, 1],
                ['data_source', 'AMS Port_Market', 'int', None, '', 1, 0, self.tt_amas_port, None, 1],
                ['location', 'AMS Location_Market', 'string', None, '', 1, 0, self.tt_amas_location, None, 1],
                ['gen_bbg_addfields', 'Generate BBG Additional Info Fields_Market', 'bool', [True, False], False, 0, 0, self.tt_gen_bbg_addfields],                
                ['stored_query', 'Stored Query_Instrument', 'string', self.db_ops.get_stored_queries(), '', 1, 0, self.tt_stored_query, None, 1],
                ['external_id_type', 'External ID Type_Instrument', 'string', self.external_id_types(), self.external_id_types()[0], 1, 0, self.tt_external_id, 0, 1],
                ['enable_tiering', 'Tiering_Instrument', 'bool', [True, False], False, 0, 0, self.tt_tiering, self.enable_disable_tiering_fields],
                ['tiering_number', 'Tiering Level_Instrument', 'int', orderbook_tiering_level, 1, 1, 0, self.tt_tiering_level, 0, 0],
                ['commit_ob', 'Create Order Books_Instrument', 'bool', [True, False], True, 0, 0, self.tt_commit_orderbooks, self.enable_disable_commit_ob, 1],
                ['update_ob', 'Update Order Books_Instrument', 'bool', [True, False], False, 0, 0, self.tt_update_orderbooks, self.enable_disable_update_ob, 1],
                ['delete_ob', 'Delete Order Books_Instrument', 'bool', [True, False], False, 0, 0, self.tt_delete_orderbooks, self.enable_disable_delete_ob, 1],
                ['create_fx_orderbooks', 'Create FX Order Books_FX Pairs', 'bool', [True, False], False, 0, 0, self.tt_fx_orderbook, self.enable_disable_fx_fields],
                ['fx_orderbook_type', 'FX Orderbook Type_FX Pairs', 'string', FxToOrderBook.fx_pair_orderbook_type, FxToOrderBook.fx_pair_orderbook_type[0], 1, 0, self.tt_fx_orderbook_type, 0, 0],
                ['commit_fx_ob', 'Commit Order Books_FX Pairs', 'bool', [True, False], True, 0, 0, self.tt_commit_orderbooks, self.enable_disable_commit_fx_ob, 1],
                ['update_fx_ob', 'Update Order Books_FX Pairs', 'bool', [True, False], 0, 0, 0, self.tt_update_orderbooks, self.enable_disable_update_fx_ob, 1],
                ['delete_fx_ob', 'Delete Order Books_FX Pairs', 'bool', [True, False], False, 0, 0, self.tt_delete_orderbooks, self.enable_disable_delete_fx_ob, 1],
                ['log_level', 'Log Level_Logging', 'string', ['INFO', 'WARN', 'ERROR', 'DEBUG',], 'INFO', 0, 0, self.tt_logging_level, None, 1],
                ['enable_log_to_file', 'Log to File_Logging', 'bool', [True, False], False, 0, 0, self.tt_log_to_file, self.enable_disable_log_file],
                ['log_to_file', 'Log to File_Logging', 'string', '', 'C:\\temp\\OrderbookCreationReport.txt', 0, 0, self.tt_log_file_path, None, 1],
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)
       
ael_variables = OrderBookAelVariables()

def ael_main(params):
    logger.LOG('Starting instrument to order book generation procedures...')
    logger_levels = {'INFO':1, 'DEBUG':2, 'WARN':3, 'ERROR':4}
    market_place = str(params['market_place'])
    market_capability = params['market_capability']
    external_id_type = params['external_id_type']
    market_segment = str(params['segment'])
    amas_location = str(params['location'])
    amas_port = int(params['data_source'])
    gen_bbg_addfields = bool(params['gen_bbg_addfields'])
    stored_query = str(params['stored_query'])    
    default_tick_size_list = str(params['default_tick_size_list'])
    default_round_lot = int(params['default_round_lot'])
    default_day_counting = int(params['default_day_counting'])
    create_fx_orderbooks = bool(params['create_fx_orderbooks'])
    fx_orderbook_type = str(params['fx_orderbook_type'])
    enable_tiering = bool(params['enable_tiering'])
    if params.get('tiering_number', None):
        tiering_level = int(params['tiering_number'])
    
    commit_ob = bool(params['commit_ob'])
    update_ob = bool(params['update_ob'])
    delete_orderbook = bool(params['delete_ob'])
    
    commit_fx_ob = bool(params['commit_fx_ob'])
    update_fx_ob = bool(params['update_fx_ob'])
    delete_fx_ob = bool(params['delete_fx_ob'])
    
    
    
    # setting logger
    logging_level = str(params['log_level'])
    log_level = logger_levels.get(logging_level)
    enable_log_file = bool(params['enable_log_to_file'])
    log_to_file = str(params['log_to_file'])
    if not log_to_file or  not enable_log_file :
        log_to_file = None
   
    logger.Reinitialize(level = log_level, logToFileAtSpecifiedPath = log_to_file)
    
    if create_fx_orderbooks:
        orderbook_action = [commit_fx_ob, update_fx_ob]
        fx_pairs_obj = FxToOrderBook(market_place, market_segment, market_capability, default_tick_size_list, \
                            default_round_lot, default_day_counting, amas_location, amas_port, fx_orderbook_type, orderbook_action)
       
        
        if commit_fx_ob or update_fx_ob or (not commit_fx_ob and not update_fx_ob and not delete_fx_ob):
            fx_pairs_obj.generate_orderbooks()
        if delete_fx_ob:
            fx_pairs_obj.delete_orderbooks()
            
                
    else:
        orderbook_action = [commit_ob, update_ob]
        if not enable_tiering:
            tiering_level = None

        if gen_bbg_addfields:
            for field in ["BBGpageID", "BBGpageNumber", "BBGpageSubID", "BBGRowNum"]:
                newAddInfo = AddInfoSetUp( "OrderBook", field, "Integer", "Bloomberg Contribution Specific field", "Standard", [], "", False)
                if newAddInfo._GetExisting() == None:
                    newAddInfo._CreateNew() 
                    
        order_book_obj = InsToOrderBook(market_place, market_segment, market_capability, default_tick_size_list, \
                            default_round_lot, default_day_counting, amas_location, amas_port, stored_query, external_id_type, orderbook_action, tiering_level)
                            
        if commit_ob or update_ob or (not commit_ob and not update_ob and not delete_orderbook):
            order_book_obj.generate_orderbooks()
        if delete_orderbook:
            order_book_obj.delete_orderbooks()
            
    logger.LOG('Finished instrument to order book generation procedures. \n \n \n \n \n \n ')









