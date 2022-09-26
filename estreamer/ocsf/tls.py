
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
from estreamer.ocsf import DigitialCertificate

class TLS( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data ):

        self.certificate = ""
        self.certificate_chain = ""
        self.cipher = ""
        self.client_ciphers = ""
        self.alert = ""
        self.extension_list = ""
        self.handshake_dur = ""
        self.ja3_fingerprint = ""
        self.ja3s_fingerprint = ""
        self.ja3s_string = ['']
        self.key_length = 0
        self.profiles = ['']
        self.server_ciphers = ['']
        self.sni = ""
        self.sans = ""
        self.version = "1.0.0"
