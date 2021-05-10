""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkToolTips.py"

start_time = "Minutes after midnight in H:MM/H.MM or HH:MM/HH.MM format, specifies when a subscription becomes active."

stop_time = "Minutes after midnight in H:MM/H.MM or HH:MM/HH.MM format, specifies when a subscription becomes inactive."

distributor_type = "Name of distributor company."

use_entitlement = "Specifies whether entitlement should be used for distributor."

utc_offset = "Use this value as on Offset from Coordinated Universal Time (UTC) in minutes."

use_utc_offset = "If checked, utc_offset will be used for calculating start and stop time as minutes after UTC midnight."

update_interval = "The time interval in seconds (explicitly can also be specified in millisecond (e.g. 0.001)) for the price updates, \
if a price update is received within the interval pricefeed does not send it to the ADS."

discard_zero_price = "If checked, zero prices are discarded for all the price \
fields of the price record, that is, bid, ask, last, open, high, low, and settle."

discard_zero_quantity = "If checked, zero quantities are discarded for quantity \
fields of the price record, that is, n_bid, n_ask, volume_last, volume_nbr, and available."

discard_negative_price = "If checked, negative prices will be discarded, \
that is, will not be written to the ADS."

force_update = "If checked, prices are always updated, although \
there are no changes in values other than the timestamp. \
If not checked, the prices are updated only if there is a difference in any of the \
values other than the timestamp."

error_msg = "Specifies the error message reported by APH/AMPH."

instrument = "Reference to the instrument to which this price link definition applies."

instrument_type = "Refers to instrument type. Instruments of this type will be populated in instrument option box."

instrument_fetch = "Change the instrument for the selected Price Link."

instrument_filter = "Filters the Price Links in the Listbox based on instrument name. Valid examples: *USD*, *, USD, *USD, USD*"

currency = "Reference to an instrument of type 'Curr', denoting the currency of this price link definition."

distributor = "Name of price distributor the selected price link belongs to."

market = "Reference to a party of type 'Market', which is the source of this price link definition."

idp_code = "Market Specific Code used by the APH/AMPH for subscription."

not_active = "If checked the price subscription will be inactive."

semantic = "Specifies which semantic type to be used by APH for subscription."

service = "Specifies which service to be used by APH for subscription."

start_time_pld = "Minutes after midnight in H:MM/H.MM or HH:MM/HH.MM format, specifies when a subscription becomes active. \
If it is blank, it uses default value from price_distributor."

stop_time_pld = "Minutes after midnight in H:MM/H.MM or HH:MM/HH.MM format, specifies when a subscription becomes inactive. \
If it is blank, it uses default value from price_distributor."

contineous_subscription = "If checked, subscription becomes active round the clock."

update_interval_pld = "The time interval in seconds (explicitly can also be specified in millisecond (e.g. 0.001)) for the price updates, \
If a price update is received within the interval pricefeed does not send it to the ADS. \
if it is blank, it uses default value from price_distributor."

last_follow_interval_pld = "If an update interval is set, update interval can be applied for update of last price by setting last_follow_interval to true, else it uses default value from price_distributor."

last_follow_interval = "If an update interval is set, update interval can be applied for update of last price by setting last_follow_interval to true."

discard_zero_price_pld = "If set to True, zero prices are discarded for all the price \
fields of the price record, that is, bid, ask, last, open, \
high, low, and settle. If value is set to blank, default value from price_distributor is used."

discard_zero_quantity_pld = "If set to True, zero quantities are discarded for quantity \
fields of the price record, that is, n_bid, n_ask, \
volume_last, volume_nbr, and available. If value is set to blank, default value from price_distributor is used."

discard_negative_price_pld = "If set to True, negative prices will be discarded, \
that is, will not be written to the ADS. If value is set to blank, default value from price_distributor is used."

force_update_pld = "If set to True, prices are always updated, although \
there are no changes in values other than the timestamp. \
If set to False, the prices are updated only if there is a difference in any of the \
values other than the timestamp. If value is set to blank, default value from price_distributor is used."

addition_addend = "Prices are added by this value before being admitted \
to the ADS by pricefeed."

multiplication_factor = "Prices are multiplied by this value before being admitted \
to the ADS by pricefeed."

log_price = "Log price for this PLD in APH/AMPH log file."

use_default_setting = "If checked, the default values from price_distributor is used."

select_all = "If checked, all the below reset fields will be checked."

force_reset = "If checked, all reset fields will reset at APH start."

reset_bid = "If checked, the BID field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_ask = "If checked, the ASK field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_bidsize = "If checked, the N_BID field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_asksize = "If checked, the N_ASK field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_last = "If checked, the LAST field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_high = "If checked, the HIGH field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_low = "If checked, the LOW field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_open = "If checked, the OPEN field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_settle = "If checked, the SETTLE field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_diff = "If checked, the DIFF field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_timelast ="If checked, the TIME_LAST field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_volumelast = "If checked, the VOLUME_LAST field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_volumenumber = "If checked, the VOLUME_NBR field of price record will be reset by APH/AMPH before sending first update to ADS."

reset_available = "If checked, the AVAILABLE field of price record will be reset by APH/AMPH before sending first update to ADS."

xml_data = "Default values for future use."

is_delayed_pld = "The indication that a price is delayed or not, If value is set to blank, default value from price_distributor is used."

is_delayed = "The indication that a price is delayed or not."

ignore_clear_price = "If checked, the APH will not clear price entry on clear price message from data provider."

ignore_clear_price_pld = "If True, the APH will not clear price entry on clear price message from data provider, \
If value is set to blank, default value from price_distributor is used."

