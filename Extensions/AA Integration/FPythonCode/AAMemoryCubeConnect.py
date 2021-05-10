""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAMemoryCubeConnect.py"
"""----------------------------------------------------------------------------
Module
    AAMemoryCubeConnect

DESCRIPTION
----------------------------------------------------------------------------"""


import clr
import sys
sys.path.append('C:\Program Files\FIS\Adaptiv Analytics')

import SunGard.Adaptiv.MemoryCube.RanetInProcessConnector
cubeConnection = None

def CubeConnection():

    global cubeConnection
    if not cubeConnection:
        adaptivMemoryCubeConnectionFactory = SunGard.Adaptiv.MemoryCube.RanetInProcessConnector.AdaptivMemoryCubeConnectionFactory()
        connStr="ConnectionType=AdaptivMemoryCube;Provider=AdaptivODBO;Initial Catalog=Market Risk;Pooling=false;Data Source=localpipe" # for connection to in-process cube
        #connStr="Initial Catalog=Market Risk" # for connection to the service
        cubeConnection = adaptivMemoryCubeConnectionFactory.Create(connStr, connStr)
        cubeConnection.Open()
    
    return cubeConnection
