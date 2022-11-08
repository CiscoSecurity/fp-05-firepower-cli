
#********************************************************************
#      File:    network_endpoint.py
#      Author:  Seyed Khadem
#
#      Description:
#       Packet helper class
#
#      Copyright (c) 2018 by Cisco Systems, Inc.
#
#       ALL RIGHTS RESERVED. THESE SOURCE FILES ARE THE SOLE PROPERTY
#       OF CISCO SYSTEMS, Inc. AND CONTAIN CONFIDENTIAL  AND PROPRIETARY
#       INFORMATION.  REPRODUCTION OR DUPLICATION BY ANY MEANS OF ANY
#       PORTION OF THIS SOFTWARE WITHOUT PRIOR WRITTEN CONSENT OF
#       CISCO SYSTEMS, Inc. IS STRICTLY PROHIBITED.
#
#*********************************************************************/
from __future__ import absolute_import
import estreamer.crossprocesslogging as logging
import binascii
import struct
import random

class NetworkEndpoint( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data , ip, port):

        self.location = ""
        self.domain = ""
        self.ip = ip
        self.instance_uid = ""
        self.mac = ""
        self.name = ""
        self.interface_uid = "" 
        self.port = port
        self.svc_name = ""
        self.subnet_uid = ""

        
