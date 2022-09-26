
#********************************************************************
#      File:    ocsf.py
#      Author:  Sam Strachan
#
#      Description:
#       ocsf adapter
#
#      Copyright (c) 2017 by Cisco Systems, Inc.
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
import copy
import time
import socket
import estreamer
import estreamer.adapters.kvpair
import estreamer.definitions as definitions
import estreamer.common
import estreamer.adapters.json
from estreamer.ocsf import NetworkActivity
from estreamer.ocsf import NetworkEndpoint
from estreamer.ocsf import NetworkProxy
from estreamer.ocsf import NetworkTraffic
from estreamer.ocsf import Metadata
from estreamer.ocsf import User
from estreamer.metadata import View
import six

# Syslog settings
SYSLOG_FACILITY_USER   = 1
SYSLOG_PRIORITY_NOTICE = 5

# Calc and save the syslog numeric (do not change, gets calculated)
SYSLOG_NUMERIC = (SYSLOG_FACILITY_USER << 3  | SYSLOG_PRIORITY_NOTICE)

# ocsf header field values
OCSF_VERSION     = 0
OCSF_DEV_VENDOR  = 'Cisco'
OCSF_DEV_PRODUCT = 'Firepower'
OCSF_DEV_VERSION = '6.0'

# Output encoding: ascii / utf8 or hex
PACKET_ENCODING = 'ascii'

def __sanitize( value ):
    value = str(value)

    value = value.replace('\"', '"')
    value = value.rstrip('"')

    return value

def __severity( priority, impact ):
    matrix = {
        1: {  # High
            1: '10',
            2: '9',
            3: '7',
            4: '8',
            5: '9'
        },
        2: {  # Medium
            1: '7',
            2: '6',
            3: '4',
            4: '5',
            5: '6'
        },
        3: {  # Low
            1: '3',
            2: '2',
            3: '0',
            4: '1',
            5: '2'
        }
    }

    if priority in matrix and impact in matrix[priority]:
        return matrix[priority][impact]

    return 5



def __ipv4( ipAddress ):
    if ipAddress.startswith('::ffff:'):
        return ipAddress[7:]

    elif ipAddress.find(':') == -1:
        return ipAddress

    return ''

def __networkActivity( data ) :
    event = NetworkActivity( data )

    return NetworkActivity.activityMap( data )

def __networkActivityId( data ) :
    event = NetworkActivity( data )

    return NetworkActivity.activityMapId( data )

def __networkActivityIdName( data ) :
    event = NetworkActivity( data )

    return NetworkActivity.activityMapIdName( data )

def __networkStatus( data ) :
    event = NetworkActivity( data )

    return NetworkActivity.statusMap( data )

def __networkStatusId( data ) :
    event = NetworkActivity( data )

    return NetworkActivity.statusMapId( data )

def __networkTypeById( data ) :
    event = NetworkActivity( data )

    return NetworkActivity.newtworkTypeById( data )

def __networkEndpoint( data , ip, port) :
    event = NetworkEndpoint( data , ip , port)
    
    return vars(event)


def __networkProxy( data ) :
    event = NetworkProxy( data )

    return vars(event)

def __networkActivity( data ) :
    return NetworkActivity( data)


def __networkTraffic( data ) :
    event = NetworkTraffic( data )

    return vars(event)

def __metadata( data ) :
    event = Metadata( data )

    return vars(event)

def __userProfile( data ) :
    event = User( data )

    return vars(event)


def __ipv6( ipAddress ):
    if ipAddress == '::':
        return ''

    elif ipAddress.startswith('::ffff:'):
        return ''

    elif ipAddress.find(':') > -1:
        return ipAddress

    return ''


MAPPING = {

    # 71
    definitions.RECORD_RNA_CONNECTION_STATISTICS: {

        'name': lambda rec: 'CONNECTION STATISTICS',

        'severity_id': lambda rec: 3 if rec['ruleAction'] < 4 else 7,

        'constants': {
            'message': 'eventDescription',
            'initiatorPort': 'spt',
            'responderPort': 'dpt',
            'cs3Label': 'ingressZone',
            'cs4Label': 'egressZone',
            'cs5Label': 'secIntelCategory'
        },

        'lambdas': {
            'time': lambda rec: rec['firstPacketTimestamp'] * 1000,
            'activity': lambda rec: 'connection',
            'activity_id': lambda rec : __networkActivityId( rec ),
            'category_name': lambda rec: 'NETWORK ACTIVITY',
            'category_uid': lambda rec: 4,
            'class_name': lambda rec: 'network_activity',
            'class_uid': lambda rec: 4001,
            'dst_endpoint': lambda rec : __networkEndpoint ( rec , rec['responderIpAddress'], rec['responderPort']),
            'duration': lambda rec: ( rec['lastPacketTimestamp']  - rec['firstPacketTimestamp'] ),
            'end_time': lambda rec: rec['lastPacketTimestamp'] * 1000,
            'metadata': lambda rec : __metadata(rec),
            'proxy': lambda rec : "" if rec['originalClientIpAddress'] != "::" else __networkProxy(rec),
            'ref_time': lambda rec: rec['firstPacketTimestamp'] * 1000,
            'ref_event_name': lambda rec : "Connection Event",
            'severity': lambda rec :  'Low' , #for connection events??
            'severity_id': lambda rec: 3 if rec['ruleAction'] < 4 else 7,
            'src_endpoint': lambda rec : __networkEndpoint ( rec , rec['initiatorIpAddress'], rec['initiatorPort']),
            'start_time': lambda rec: rec['firstPacketTimestamp'] * 1000,
            'status_id': lambda rec : __networkStatus( rec['sslFlowStatus'] ),
             #'tls': lambda rec: __tls(rec),
            'timezone_offset': lambda rec: 0,
            'traffic': lambda rec: __networkTraffic(rec),
            'type_uid': lambda rec: 400100 + int(__networkActivityId( rec['firewallRuleAction'] )),
            'type_name': lambda rec: __networkTypeById(400100 + int(__networkActivityId( rec['firewallRuleAction'] ))),
            'user': lambda rec: __userProfile(rec),  #todo:  function to determine what profiles are available then append them to record
        },

        'fields': {
            'ingressZone': 'inbound',
            'egressZone': 'outbound',
            'ingressInterface': 'deviceInboundInterface',
            'egressInterface': 'deviceOutboundInterface',
            'policyRevision': 'policy_rev',
            'ruleId': 'rule_id',
            'tunnelRuleId': '',
            'ruleAction': 'act',
            'ruleReason': 'reason',
            'protocol': 'proto',
            'netflowSource': '',
            'instanceId': 'dvcpid',
            'connectionCounter': 'count', # ocsf network_activity.count
            'firstPacketTimestamp': '', 
            'lastPacketTimestamp': '', # Used to generate end
            'initiatorTransmittedPackets': '',
            'responderTransmittedPackets': '',
            'initiatorTransmittedBytes': 'bytesOut',
            'responderTransmittedBytes': 'bytesIn',
            'initiatorPacketsDropped': '',
            'responderPacketsDropped': '',
            'initiatorBytesDropped': '',
            'responderBytesDropped': '',
            'qosAppliedInterface': '',
            'qosRuleId': '',
            'userId': 'suser',
            'applicationId': 'app',
            'urlCategory': '',
            'urlReputation': '',
            'clientApplicationId': 'app_name',
            'webApplicationId': '',
            'clientUrl.data': 'request',
            'netbios': '',
            'clientApplicationVersion': '',
            'monitorRules1': '',
            'monitorRules2': '',
            'monitorRules3': '',
            'monitorRules4': '',
            'monitorRules5': '',
            'monitorRules6': '',
            'monitorRules7': '',
            'monitorRules8': '',
            'securityIntelligenceSourceDestination': '',
            'securityIntelligenceLayer': '',
            'fileEventCount': '',
            'intrusionEventCount': '',
            'initiatorCountry': '',
            'responderCountry': '',
            'originalClientCountry': '',
            'iocNumber': '',
            'sourceAutonomousSystem': '',
            'destinationAutonomousSystem': '',
            'snmpIn': '',
            'snmpOut': '',
            'sourceTos': '',
            'destinationTos': '',
            'sourceMask': '',
            'destinationMask': '',
            'securityContext': '',
            'vlanId': '',
            'referencedHost': '',
            'userAgent': '',
            'httpReferrer': '',
            'sslCertificateFingerprint': '',
            'sslPolicyId': '',
            'sslRuleId': '',
            'sslCipherSuite': '',
            'sslVersion': '',
            'sslServerCertificateStatus': '',
            'sslActualAction': '',
            'sslExpectedAction': '',
            'sslFlowStatus': 'status',
            'sslFlowError': '',
            'sslFlowMessages': '',
            'sslFlowFlags': '',
            'sslServerName': '',
            'sslUrlCategory': '',
            'sslSessionId': '',
            'sslSessionIdLength': '',
            'sslTicketId': '',
            'sslTicketIdLength': '',
            'networkAnalysisPolicyRevision': '',
            'endpointProfileId': '',
            'securityGroupId': '',
            'locationIpv6': '',
            'httpResponse': '',
            'dnsQuery.data': 'destinationDnsDomain',
            'dnsRecordType': '',
            'dnsResponseType': '',
            'dnsTtl': '',
            'sinkholeUuid': '',
            'securityIntelligenceList1': 'sec_intel_events',
            'securityIntelligenceList2': ''
        },

        'viewdata': {
            View.SENSOR: 'dvchost',
            View.SEC_ZONE_INGRESS: 'cs3',
            View.SEC_ZONE_EGRESS: 'cs4',
            View.SEC_INTEL_LIST1: 'cs5',
            View.IFACE_INGRESS: 'deviceInboundInterface',
            View.IFACE_EGRESS: 'deviceOutboundInterface',
            View.FW_POLICY: 'cs1',
            View.FW_RULE: 'cs2',
            View.FW_RULE_ACTION: 'act',
            View.FW_RULE_REASON: 'reason',
            View.PROTOCOL: 'proto',
            View.USER: 'suser',
            View.APP_PROTO: 'app',
            View.CLIENT_APP: 'app_name',
        },
    },

}


class Ocsf( object ):
    """ocsf adapter class to contain implementation"""
    def __init__( self, source ):
        self.source = source
        self.record = estreamer.common.Flatdict( source, True )
        self.output = None
        self.mapping = None

        if 'recordType' in self.record:
            if self.record['recordType'] in MAPPING:
                self.mapping = MAPPING[ self.record['recordType'] ]
                self.output = {}
               



    @staticmethod
    def __sanitize( value ):
        value = str(value)
        
        singleQuote = "'"
        doubleQuote = '"'
        ## Escape \ " ]
        value = value.replace('\\\"', '"')
        value = value.replace('"{', '{')
        value = value.replace('}"', '}')
        value = value.replace(singleQuote, doubleQuote)
        value = value.replace('\"', '"')
        value = value.replace('\\"', '"')
        value = value.replace('\\\"', '"')
        value = value.replace('\"{', '{')
        value = value.replace('}\"', '}')

        return value



    def __convert( self ):
        """Writes the self.output dictionary"""

        unmapped = {}
        # Do the fields first (mapping)
        for source in self.mapping['fields']:
            target = self.mapping['fields'][source]
            if len(target) > 0:
#                unmapped[target] = Ocsf.__sanitize( self.record[source] )
                unmapped[target] = self.record[source] 

        self.output['unmapped'] = unmapped

        # Now the constants (hard coded values)
        for target in self.mapping['constants']:
            self.output[target] = self.mapping['constants'][target]
        # Lambdas

        lambdas = {}
        for target in self.mapping['lambdas']:
            function = self.mapping['lambdas'][target]
            self.output[target] = function( self.record  )

        # View data last
        for source in self.mapping['viewdata']:
            key = '{0}.{1}'.format( View.OUTPUT_KEY, source )
            value = self.record[key]
            if value is not None:
                target = self.mapping['viewdata'][source]
                self.output[target] = Ocsf.__sanitize( value )

        keys = list(self.output.keys())
        for key in keys:
            if isinstance( self.output[ key ], six.string_types) and len( self.output[ key ] ) == 0:
                del self.output[ key ]

            elif self.output[ key ] == 0:
                del self.output[ key ]

            else: 

                self.output[ key ] = Ocsf.__sanitize( self.output[ key ] )



    def __ocsfMessage( self ):
        """Takes a transformed dictionary and converts it to a ocsf message"""
        # my ($sig_id, $name, $severity, $message) = @_;

        # my $hostname = hostname();
        # $hostname =~ s/\.+$//;
        hostname = socket.gethostname()

        # http://search.cpan.org/~dexter/POSIX-strftime-GNU-0.02/lib/POSIX/strftime/GNU.pm
        # # Get syslog-style timestamp: MAR  1 16:23:11
        # my $datetime = strftime('%b %e %T', localtime(time()));
        now = time.strftime('%b %d %X')

#        data = estreamer.adapters.json.dumps(self.output)
        data = Ocsf.__sanitize( self.output )
        # Special fields
        name = self.mapping['name']( self.record )

        message = u'{0}'.format(
            data
        )

        return message



    def dumps( self ):
        """Dumps the current record to a ocsf message (or None)"""
        if self.mapping is None:
            return None

        self.__convert()
        message = self.__ocsfMessage()

        return message



def dumps( source ):
    """Converts a source record into a ocsf message"""
    ocsfAdapter = Ocsf( source )
    return ocsfAdapter.dumps()


