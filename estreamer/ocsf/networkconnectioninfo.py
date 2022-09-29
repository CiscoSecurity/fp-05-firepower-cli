
#********************************************************************
#      File:    networkactivity.py
#      Author:  Seyed Khadem
#
#      Description:
#       Packet helper class
#
#      Copyright (c) 2022 by Cisco Systems, Inc.
#
#       ALL RIGHTS RESERVED. THESE SOURCE FILES ARE THE SOLE PROPERTY
#       OF CISCO SYSTEMS, Inc. AND CONTAIN CONFIDENTIAL  AND PROPRIETARY
#       INFORMATION.  REPRODUCTION OR DUPLICATION BY ANY MEANS OF ANY
#       PORTION OF THIS SOFTWARE WITHOUT PRIOR WRITTEN CONSENT OF
#       CISCO SYSTEMS, Inc. IS STRICTLY PROHIBITED.
#
#*********************************************************************/
from __future__ import absolute_import
import binascii
import struct

class NetworkConnectionInfo( object ):
    """
    Helper class for OCSF network activity classes
    """
    def __getDirection( self, data ):
        directions = {
            0: 'Unknown',
            1: 'Inbound',
            2: 'Outbound'
        }

        if direction in data:
            self.direction_id = directions.index(direction)

            return direction
        else :
            self.direction_id = 0

            return directions.index(0)


    def __init__( self, data ):
        self.activity = data.activity


        # https://schema.ocsf.io/classes/network_activity?extensions=, -1 to 6, for Secure Firewall Default is  Network Traffic
        # todo:  helper function to determine network activity classification
        self.uid = ""
        self.direction = __getDirection(data)
        self.direction_id = 0
        self.protocol_ver = ""
        self.protocol_ver_id = 0
        self.profiles = ['']
        self.protocol_name = "" 
        self.protocol_num = -1 #todo
        self.tcp_flags = "" 
        self.traffic_path = "Unknown"
        self.traffic_path_id = 0
