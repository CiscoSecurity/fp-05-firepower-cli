
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
import json

class NetworkActivity( object ):
    """
    Helper class for OCSF network activity classes
    """

    ACTIVITIES = {
        -1: 'Other',
        0 : 'Unknown',
        1 : 'Established',
        2 : 'Closed',
        3 : 'Reset',
        4 : 'Failed',
        5 : 'Refused',
        6 : 'Traffic'
    }

    TYPES =  {
        -1 : 'Network Activity: Other',
        400100 : 'Network Activity: Unknown',
        400101 : 'Network Activity: Established',
        400102 : 'Network Activity: Closed',
        400103 : 'Network Activity: Reset',
        400104 : 'Network Activity: Failed',
        400105 : 'Network Activity: Refused',
        400106 : 'Network Activity: Traffic'
    }

    SEVERITIES = {
        -1: 'Other',
        0 : 'Unknown',
        1 : 'Information',
        2 : 'Low',
        3 : 'Medium',
        4 : 'High',
        5 : 'Critical',
        6 : 'Fatal'
    }

    STATUSES = {
        -1: 'Other',
        0 : 'Unknown',
        1 : 'Success',
        2 : 'Failure'
    }

    @staticmethod
    def activityMap ( activity ):

        if activity == 'Allow' :
           activity = 'Established'

        if activity in NetworkActivity.ACTIVITIES:
            return activity

        return "Unknown"

    @staticmethod
    def activityMapId ( activity ):

        item = NetworkActivity.activityMap( activity ) 

        for k, v in NetworkActivity.ACTIVITIES.items() :
            if v == item :
                return k

        return -1

    @staticmethod
    def newtworkTypeName ( id ):

        if id in NetworkActivity.TYPES.keys() :
            return NetworkActivity.TYPES[id]

        return "Network Activity: Other"

    @staticmethod
    def activityMapIdName ( self, id ):

        if id in NetworkActivity.TYPES.keys():
            return NetworkAcitivity.TYPE.get(id)

        return -1

    @staticmethod
    def statusMap ( status ):

        if status in NetworkActivity.STATUSES:
            return status

        return "Unknown"

    @staticmethod
    def statusMapId ( status ):

        for k, v in NetworkActivity.STATUSES.items():
            if status == v:
                return k

        return -1

    @staticmethod
    def nonEmptyValues( data ) :

        return {k: v for k, v in data.items() if v}


    def __init__( self, data ):

        #todo: add checks for null data
        self.activity = NetworkActivity.activityMap( data['firewallRuleAction'] )
        self.activity_id = NetworkActivity.activityMapId( data['firewallRuleAction'] ) #todo
        self.app_name = data['@computed.clientApplication']
        self.category_name = "Network Activity"
        self.category_uid = 4
        self.class_name = "Network Activity"
        self.class_uid = 4001
        self.count = data['connectionCounter']
        self.duration = int(data['lastPacketTimestamp'])  - int(data['firstPacketTimestamp'] )
        self.end_time = int(data['lastPacketTimestamp']) * 1000
        self.time = int(data['firstPacketTimestamp']) * 1000
        self.message = str(data['recordTypeDescription'] != "")
#        self.observables = ""
        self.profiles = []
#        self._raw_data = ""
#        self.ref_event_code = ""
        self.ref_event_name = "Connection Event"
        self.ref_time = str(data['firstPacketTimestamp'] * 1000)
        self.severity = "Unknown" #todo is there a mapping for connection events?
        self.severity_id = 0 #todo
        self.start_time = data['firstPacketTimestamp'] * 1000
        self.status = NetworkActivity.statusMap( data['@computed.sslFlowStatus'] )  #todo what statuses are available for generic connection events
        self.status_code = str(NetworkActivity.statusMapId ( data['@computed.sslFlowStatus'] )) #is there an equivalent ssl network class we should use?
#        self.status_detail = ""
        self.status_id = NetworkActivity.statusMapId( data['@computed.sslFlowStatus'] )
        self.timezone_offset = 0
        self.type_uid = 400100 + self.activity_id
        self.type_name = NetworkActivity.newtworkTypeName( self.type_uid )

