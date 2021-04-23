__all__ = [
            "ADS_PLAYGROUND_ABCAP_HOSTNAME", 
            "ADS_PLAYGROUND_ABCAP_IP", 
            "ADS_PRODUCTION_ABCAP_IP",
            "ADS_PLAYGROUND_AFRICA_IP"
          ]

ADS_PLAYGROUND_ABCAP_IP = {
    "amba_server_ip" : "10.110.92.110:9300",
    "ads_server_ip": "10.110.92.110:9101",
    "mb_name" : "D1_CAL_ATS_RECEIVER",
    "subject_string" : "D1_CAL_AMBA/TRADE",
    "trade_system" : "ABCAP_FRONT_ARENA",
    "output_filename" : "FrontArena_SA_CAL_",
    "output_destination" : r"C:\temp",
    "output_date_format" : "%Y%m%d"
}

ADS_PLAYGROUND_ABCAP_HOSTNAME = {
    "amba_server_ip" : "jhbdsm02647:9300",
    "ads_server_ip": "jhbdsm02647:9101",
    "mb_name" : "D1_CAL_ATS_RECEIVER",
    "subject_string" : "D1_CAL_AMBA/TRADE",
    "trade_system" : "ABCAP_FRONT_ARENA",
    "output_filename" : "FrontArena_SA_CAL_",
    "output_destination" : r"/apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/CAL",
    "output_date_format" : "%Y%m%d"
}


ADS_PLAYGROUND_AFRICA_IP = {
    "amba_server_ip" : "22.36.28.61:9300", 
    "ads_server_ip": "22.36.28.61:9603",
    "mb_name" : "D1_CAL_ATS_RECEIVER",
    "subject_string" : "D1_CAL_AMBA/TRADE",
    "trade_system" : "ABCAP_FRONT_ARENA_AFRICA",
    "output_filename" : "FrontArena_Africa_CAL_",
    "output_destination" : r"C:\Temp",
    "output_date_format" : "%Y%m%d"
}

ADS_PRODUCTION_ABCAP_IP = {
    "amba_server_ip" : "10.110.92.131:9300",
    "ads_server_ip": "10.110.92.131:9101",
    "mb_name" : "P_CAL_RECEIVER",
    "subject_string" : "P_CAL_AMBA/TRADE",
    "trade_system" : "ABCAP_FRONT_ARENA",
    "output_filename" : "FrontArena_SA_CAL_",
    "output_destination" : r"/apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/CAL",
    "output_date_format" : "%Y%m%d"
}


ADS_PRODUCTION_AFRICA_IP = {
    "amba_server_ip" : "22.36.28.61:9300", #Required.
    "ads_server_ip": "22.36.28.61:9603",   #Required.
    "mb_name" : "D1_CAL_ATS_RECEIVER",      #Required.
    "subject_string" : "D1_CAL_AMBA/TRADE", #Required.
    "trade_system" : "ABCAP_FRONT_ARENA_AFRICA",
    "output_filename" : "FrontArena_Africa_CAL_",
    "output_destination" : r"C:\Temp",      #Find out from RTB.
    "output_date_format" : "%Y%m%d"
}
