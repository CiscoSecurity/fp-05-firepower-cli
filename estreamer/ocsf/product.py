
#********************************************************************
#      File:    product.py
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

class Product( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data ):

        self.feature = ""
        self.lang = ""
        self.uid = ""
        self.name = "Secure Firewall"
        self.path = ""
        self.version = "7.1"
        self.vendor_name = "Cisco"

