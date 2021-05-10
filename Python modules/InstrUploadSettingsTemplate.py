""" Trade_Allocation:1.2.5 """

'''-----------------------------------------------------------------------------
 MODULE
     InstrUploadSettings - Defines what instrument checks that shall be performed
     when instruments are uploaded from the external exchanges, and defines
     how to find the isin code of the underlying instrument to a derivative if
     you wish to replace the underlying received from the market with another
     underlying instrument.
     
     (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.
     
 DESCRIPTION
     The FMessageAdaptations module allows the user to define a different
     underlying for a derivative compared to what is sent from AMAS. The 
     mapping rules are defined in the map_underlying_isin_dict dictionary
     below. The FMessageAdaptations module also allows the user to set a
     number of collision prevensions to avoid instruments from different
     markets to overwrite one another.

     Mapping rules are defined as follows:
     =====================================

     In the map_underlying_isin_dict dictionary you define your general rules.
     A typical example would be to use a common EquityIndex as underlying for
     both futures and options. 
     
     A python dictionary is created on the format: 'old_isin':'new_isin'
     
     Example:
     
     Eurex sends out the ISIN: DE0008469495, as underlying for futures on the DAX. 
     Eurex sends out the ISIN: DE0008469594, as underlying for options on the DAX.
     The desired underlying ISIN for derivatives on DAX is: DE0008469008.
     
     If desired to have the EquityIndex with "true" ISIN as underlying for 
     derivatives, the dictionary would look as follows:

     map_underlying_isin_dict={
     'DE0008469594':'DE0008469008',
     'DE0008469495':'DE0008469008'
     }     
      

 DATA-PREP
     The module FMessageAdaptations can check so that:

     1. Currencies are not overwritten by other instruments with the same INSID.
     2. Instruments with the same insid but different isin are not overwritten. In
        this case the market name is appended to the INSID.
     3. We ensure that SWX long name are unique the short name is appended to the
        long name if needed.
     4. Instruments with the same ISIN but different INSID or CURRENCIES are not
        overwritten. The instrument section of the message is deleted, the orderbook
        and all other related information is created though.
     5. Bonds that already has expired are not inserted into the ADS. This may
        happen on SWX.
     6. Replace incoming 00000000 in leg start_day with today's date.
     7. Replace underlying instrument as specified in InstrUploadSettings.
     8. Equity index futures are inserted to the page: hedgeChoice.
     9. CombinationLinks are created for Basis instruments traded on Xetra (EUREX BONDS).
     10. Equity index are inserted to the page: NonSplitIndexes.
     11. Equity index are inserted to the page: betaIndexChoice.
  
 REFERENCES
     Regular expressions in python:

     http://www.python.org/doc/current/lib/module-re.html
 

 ENDDESCRIPTION
-----------------------------------------------------------------------------'''
check_swx_long = 1     # If same SWX long name append short name to long name
check_insid = 1        # If same INSID but different ISIN append market name to INSID.
check_isin = 1         # If same ISIN but different INSID or CURR, only create orderbook.
check_currency = 1     # If same INSID but existing instrument is of type CURR. Delete message.
check_der_und = 1      # If the value of UND_INSADDR.ISIN exist in the left column in the
                       # map_underlying_isin_dict below, then replace it whith the ISIN
                       # in the right column. 
check_expired_bond = 1 # Delete message if Bond has expired.
check_start_day_leg =	1 # If START_DAY = 00000000, then START_DAY=TODAY.
create_xetra_basis_comb_link = 1 # Create CombinationLinks for Basis instruments on Xetra.
insert_eq_index_fut_into_hedgechoice = 1 # Automatically insert future into hedgeChoice.
insert_eq_index_into_nonsplitindexes = 1 # Automatically insert EqIndex into NonSplitIndexes.
insert_eq_index_into_betaindexchoice = 1 # Automatically insert EqIndex into betaIndexChoice.

map_underlying_isin_dict={
     'DE0008469594':'DE0008469008',
     'DE0008469495':'DE0008469008',
     'CH0008616432':'CH0009980894',
     'CH0008616382':'CH0009980894'
}
