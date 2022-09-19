
#********************************************************************
#      File:    networkactivity.py
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
import binascii
import struct

class NetworkActivity( object ):
    """
    Helper class for OCSF network activity classes
    """
    NETWORK_TRAFFIC = 6

    def __init__( self, data ):
        self.activity = data.activity


        # https://schema.ocsf.io/classes/network_activity?extensions=, -1 to 6, for Secure Firewall Default is  Network Traffic
        # todo:  helper function to determine network activity classification
        self.activity_id = NETWORK_TRAFFIC
        self.app_name = ""
        self.category_name = ""
        self.class_name = ""
        self.class_uid = ""
        self.unmapped = ['']
        self.connection_info = "" # connection_info object
        self.count = ""
        self.dst_endpoint = "" # network_endpoint object
        self.duration = ""
        self.end_time = ""
        self.enrichments = ['']
        self._time = ""
        self.message = ""
        self.metadata = "" # metadata object
        self.observables = ""
        self.ref_time = ""
        self.product = "" # product object
        self.profiles = "" # profile objects
        self._raw_data = ""
        self.ref_event_code = ""
        self.ref_event_name = ""
        self.severity = ""
        self.severity_id = ""
        self.src_endpoint = "" # endpoint object
        self.status = ""
        self.status_code = ""
        self.status_detail = ""
        self.status_id = ""
        self.tls = ""
        self.timezone_offset = ""
        self.traffic = ""
        self.type_uid = "" #The event type ID identifies the event's semantics and structure. The value is calculated by the logging system as: class_uid * 100 + activity_id.
        self.type_name = ""
        self.unmapped = ['']


    def __getNyble( self, indexNyble ):
        byteIndex = int(indexNyble/2)
        #byte = struct.unpack( '>B', self.data[byteIndex] )[0]
        byte = self.data[byteIndex]  #Python3 read ensures this is already in a binary format
        if indexNyble % 2 == 0:
            mask = 0b11110000
            return ( byte & mask ) >> 4
        mask = 0b00001111
        return byte & mask

    def getPayloadAsBytes( self ):
        headerLengthSum = (
            Packet.LAYER2_HEADER_LENGTH +
            self.__getLayer3HeaderLength() +
            self.__getLayer4HeaderLength() )

        return self.data[headerLengthSum:]

    @staticmethod
    def createFromHex( data ):
        binData = binascii.unhexlify( data )
        return Packet( binData )
        
