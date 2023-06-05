
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

class NetworkProxy( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data ):

        # https://schema.ocsf.io/classes/network_activity?extensions=, -1 to 6, for Secure Firewall Default is  Network Traffic
        # todo:  helper function to determine network activity classification
        self.hostname = data['hostIpAddr']
        self.ip = data['originalClientIpAddress']
        self.port = data['initiatorPort']
        self.profiles = [''] 
