
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

class Metadata( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data ):

        # https://schema.ocsf.io/classes/network_activity?extensions=, -1 to 6, for Secure Firewall Default is  Network Traffic
        # todo:  helper function to determine network activity classification
        self.correlation_uid = ""
        self.uid = ""
        self.labels = ""
        self.logged_time = ""
        self.logged_time_dt = ""
        self.modified_time = ""
        self.modified_time_dt = ""
        self.processed_time = ""
        self.processed_time_dt = ""
        self.profiles = ['']
        self.sequence = 0
        self.version = "1.0.0"
