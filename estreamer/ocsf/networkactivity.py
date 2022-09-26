
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

        if activity == 'Allow' :
           activity = 'Established'

        for k,v  in NetworkActivity.ACTIVITIES.items() :
            if v  == activity:
                return k

        return -1

    @staticmethod
    def newtworkTypeById ( id ):

        for k,v in NetworkActivity.TYPES.items() :
           if id == k :
               return v

        return -1

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

        return "Unknown"



    def __init__( self, data ):

        #self.activity = self.__activityMap(data['firewallRuleAction'])
        #self.activity_id =  self.__activityMapId(data['firewallRuleAction'])
        self.app_name = ""
        self.category_name = ""
        self.class_name = ""
        self.class_uid = ""
        self.unmapped = ['']
        self.connection_info = "" # connection_info object
        self.count = ""
        self.dst_endpoint = ""#NetworkEndpoint(data) # network_endpoint object
        self.duration = ""
        self.end_time = ""
        self.enrichments = ['']
        self._time = ""
        self.message = ""
        self.metadata = "" #Metadata(data) # metadata object
        self.observables = ""
        self.ref_time = ""
        self.product = "" # product object
        self.profiles = "" # profile objects
        self._raw_data = ""
        self.ref_event_code = ""
        self.ref_event_name = ""
        self.severity = ""
        self.severity_id = ""
        self.src_endpoint = ""#NetworkEndpoint(data) 
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

