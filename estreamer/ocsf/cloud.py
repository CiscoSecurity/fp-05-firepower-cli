
#********************************************************************
#      File:    cloud.py
#      Author:  Seyed Khadem
#
#      Description:
#       Cloud object
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

class Cloud( object ):
    """
    Helper class for OCSF network activity classes
    """

    def __init__( self, data):

#        self.acount_type = data['user_id']
#        self.acount_type_id = data['user']
        self.account_uid = ""
        self.zone = ""
        self.org_uid = ""
        self.profiles = ['']
        self.project_uid = ""
        self.provider = "Cisco Secure Firewall"
        self.region = ""
        self.resource_uid = ""
