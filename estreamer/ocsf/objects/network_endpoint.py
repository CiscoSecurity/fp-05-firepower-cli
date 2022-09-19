
#********************************************************************
#      File:    networkendpoint.py
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

class NetworkEndpoint( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data ):

        # https://schema.ocsf.io/classes/network_activity?extensions=, -1 to 6, for Secure Firewall Default is  Network Traffic
        # todo:  helper function to determine network activity classification
        self.location = ""
        self.domain = ""
        self.ip = ""
        self.instance_uid = ""
        self.mac = ""
        self.name = ""
        self.interface_uid = "" 
        self.port = ""
        self.profiles = [''] 
        self.svc_name = ""
        self.subnet_uid = ""

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
        
