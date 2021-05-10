#----------------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module provides MQ details to connect to MQ to be able to send and receive xml messages.
#  Department and Desk : Front Arena BTB/RTB
#  Requester           : Fonnt Arena  BTB/RTB
#  CR Number           : 587810
#----------------------------------------------------------------------------------------------------------------------


#-------------- Midas MQ Connection Settings ------------#

#******************* DEV Settings ***********************#
'''
MidasMQChannel       = 'ABFJB.CLIENTS.00'
MQSecExit            = 'BCPKIJCExit_60R(SECSEND)'
MidasMQQueueManager  = 'MQFJBD02'
MidasMQHostName      = 'jbmwfarm02-dev(1422)'

MidasMQSenderQueue   = 'OUTFRONTARENA.ABSAFX.D02.JB.00'
MidasMQReceiverQueue = 'INFRONTARENA.ABSAFX.D02.JB.00'
'''
#******************* UAT Settings ***********************#
'''
MidasMQChannel       = 'ABFJB.CLIENTS.00'
MQSecExit            = 'BCPKIJCExit_60R(SECSEND)'
MidasMQQueueManager  = 'MQFJBD02'
MidasMQHostName      = 'jbmwfarm02-dev(1422)'

MidasMQSenderQueue   = 'OUTFRONTARENA.ABSAFX.D02.JB.01'
MidasMQReceiverQueue = 'INFRONTARENA.ABSAFX.D02.JB.01'
'''
#****************** PROD Settings ***********************#
#'''
MidasMQChannel       = 'FAAJB.CLIENTS.00'
MQSecExit            = 'BCPKIJCExit_60R(SECSEND)'
MidasMQQueueManager  = 'MQFJBL01'
MidasMQHostName      = 'jbmwfarm01-live(1421)'

MidasMQSenderQueue   = 'OUTABSAFX.FRONTARENA.LIVE.JB.00'
MidasMQReceiverQueue = 'INABSAFX.FRONTARENA.LIVE.JB.00'
#'''
