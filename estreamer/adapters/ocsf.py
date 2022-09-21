
#********************************************************************
#      File:    ocsf.py
#      Author:  Seyed Khadem
#
#      Description:
#       OCSF adapter
#
#      Copyright (c) 2022 by Cisco Systems, Inc.
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
from estreamer.metadata import View
import six
import enum
import json


# OCSF header field values
OCSF_VERSION     = 0
OCSF_DEV_VENDOR  = 'Cisco'
OCSF_DEV_PRODUCT = 'Firepower'
OCSF_DEV_VERSION = '6.0'

# Packet truncation length
PACKET_LENGTH_MAX = 1022

# Output encoding: ascii / utf8 or hex
PACKET_ENCODING = 'ascii'

class UTF8Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)


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
        'sig_id': lambda rec: 'RNA:4100:1',

        'name': lambda rec: 'NETWORK ACTIVITY',

        'constants': {
            'cs1Label': 'fwPolicy',
            'cs2Label': 'fwRule',
            'cs3Label': 'ingressZone',
            'cs4Label': 'egressZone',
            'cs5Label': 'secIntelCategory'
        },

        'lambdas': {
            'rt': lambda rec: rec['firstPacketTimestamp'] * 1000,
            'category_name': "network_activity",
            'activity_id': lambda rec: ____activityMap( rec['firewallRuleAction'] ),
            'start': lambda rec: rec['firstPacketTimestamp'] * 1000,
            'end': lambda rec: rec['lastPacketTimestamp'] * 1000,
            'src': lambda rec: __ipv4( rec['initiatorIpAddress'] ),
            'dst': lambda rec: __ipv4( rec['responderIpAddress'] ),
            'c6a2': lambda rec: __ipv6( rec['initiatorIpAddress'] ),
            'c6a3': lambda rec: __ipv6( rec['responderIpAddress'] ),
            'deviceExternalId': lambda rec: rec['deviceId'],
        },

        # the following qualification needs to be in place for mapping
        # names must be unique
        # duplicate object types must have the parent declared, ex.
        # classname.fieldname

        'fields': {
            'applicationId': 'app',
            'clientApplicationId': 'requestClientApplication',
            'clientApplicationVersion': '',
            'clientApplication': 'networkactivity.app_name',
            'clientUrl.data': 'request',
            'connectionCounter': 'externalId',
            'destinationAutonomousSystem': '',
            'destinationMask': '',
            'destinationTos': '',
            'dnsQuery.data': 'destinationDnsDomain',
            'deviceId': 'dvchost',
            'dnsRecordType': '',
            'dnsResponseType': '',
            'dnsTtl': '',
            'egressInterface': 'deviceOutboundInterface',
            'egressZone': 'cs4',
            'endpointProfileId': '',
            'eventDescription.data': 'networkactivity.activity',
            'fileEventCount': '',
            'firewallRuleAction': 'networkactivity.activity_id',
            'firstPacketTimestamp': '', # Used to generate rt and start
            'httpReferrer': '',
            'httpResponse': '',
            'ingressInterface': 'deviceInboundInterface',
            'ingressZone': 'cs3',
            'initiatorBytesDropped': '',
            'initiatorCountry': '',
            'initiatorIpAddress': 'networkactivity.dst_endpoint.networkendpoint.ip',
            'initiatorPacketsDropped': '',
            'initiatorPort': 'spt',
            'initiatorTransmittedBytes': 'bytesOut',
            'initiatorTransmittedPackets': '',
            'instanceId': 'dvcpid',
            'intrusionEventCount': '',
            'iocNumber': '',
            'lastPacketTimestamp': '', # Used to generate end
            'locationIpv6': '',
            'monitorRules1': '',
            'monitorRules2': '',
            'monitorRules3': '',
            'monitorRules4': '',
            'monitorRules5': '',
            'monitorRules6': '',
            'monitorRules7': '',
            'monitorRules8': '',
            'netbios': '',
            'netflowSource': '',
            'networkAnalysisPolicyRevision': '',
            'originalClientCountry': '',
            'originalClientIpAddress': '',
            'policyRevision': 'cs1',
            'protocol': 'proto',
            'qosAppliedInterface': '',
            'qosRuleId': '',
            'referencedHost': '',
            'responderBytesDropped': '',
            'responderCountry': '',
            'responderIpAddress': 'networkactivity.src_endpoint.networkendpoint.ip',
            'responderPacketsDropped': '',
            'responderPort': 'dpt',
            'responderTransmittedBytes': 'bytesIn',
            'responderTransmittedPackets': '',
            'ruleAction': 'act',
            'ruleId': 'cs2',
            'ruleReason': 'reason',
            'securityContext': '',
            'securityGroupId': '',
            'securityIntelligenceLayer': '',
            'securityIntelligenceList1': 'cs5',
            'securityIntelligenceList2': '',
            'securityIntelligenceSourceDestination': '',
            'sinkholeUuid': '',
            'snmpIn': '',
            'snmpOut': '',
            'sourceAutonomousSystem': '',
            'sourceMask': '',
            'sourceTos': '',
            'sslActualAction': '',
            'sslCertificateFingerprint': '',
            'sslCipherSuite': '',
            'sslExpectedAction': '',
            'sslFlowError': '',
            'sslFlowFlags': '',
            'sslFlowMessages': '',
            'sslFlowStatus': '',
            'sslPolicyId': '',
            'sslRuleId': '',
            'sslServerCertificateStatus': '',
            'sslServerName': '',
            'sslSessionId': '',
            'sslSessionIdLength': '',
            'sslTicketId': '',
            'sslTicketIdLength': '',
            'sslUrlCategory': '',
            'sslVersion': '',
            'tcpFlags': '',
            'tunnelRuleId': '',
            'urlCategory': '',
            'urlReputation': '',
            'userAgent': '',
            'userId': 'suser',
            'vlanId': '',
            'webApplicationId': '',
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
            View.CLIENT_APP: 'requestClientApplication',
        },
    },

   
}


class Ocsf( object ):
    """Ocsf adapter class to contain implementation"""
    def __init__( self, source ):
        self.source = source
        self.record = estreamer.common.Flatdict( source, True )
        self.output = None
        self.mapping = None

        if 'recordType' in self.record:
            if self.record['recordType'] in MAPPING:
                self.mapping = MAPPING[ self.record['recordType'] ]
                self.output = {}

    def __convert( self ):
        """Writes the self.output dictionary"""

        # Do the fields first (mapping)
        for source in self.mapping['fields']:
            target = self.mapping['fields'][source]
            if len(target) > 0:
                self.output[target] = self.record[source]

        # Now the constants (hard coded values)
        for target in self.mapping['constants']:
            self.output[target] = self.mapping['constants'][target]

        # Lambdas
        for target in self.mapping['lambdas']:
            function = self.mapping['lambdas'][target]
            self.output[target] = function( self.record )

        # View data last
        for source in self.mapping['viewdata']:
            key = '{0}.{1}'.format( View.OUTPUT_KEY, source )
            value = self.record[key]
            if value is not None:
                target = self.mapping['viewdata'][source]
                self.output[target] = value

        keys = list(self.output.keys())
        for key in keys:
            if isinstance( self.output[ key ], six.string_types) and len( self.output[ key ] ) == 0:
                del self.output[ key ]

            elif self.output[ key ] == 0:
                del self.output[ key ]

            else:
                self.output[ key ] = ocsf.__sanitize( self.output[ key ] )



    def __ocsfMessage( self ):
        """Takes a transformed dictionary and converts it to a OCSF message"""
        # my ($sig_id, $name, $severity, $message) = @_;

        # my $hostname = hostname();
        # $hostname =~ s/\.+$//;
        hostname = socket.gethostname()

        # http://search.cpan.org/~dexter/POSIX-strftime-GNU-0.02/lib/POSIX/strftime/GNU.pm
        # # Get syslog-style timestamp: MAR  1 16:23:11
        # my $datetime = strftime('%b %e %T', localtime(time()));
        now = time.strftime('%b %d %X')

        # Key value pairs
        data = estreamer.adapters.kvpair.dumps(
            self.output,
            delimiter = ' ',
            quoteSpaces = False,
            sort = True )

        #return nested json object
        message = u'OCSF'

        #json.dumps(data,cls=UTF8Encoder)
        return message


    def dumps( self ):
        """Dumps the current record to a OCSF message (or None)"""
        if self.mapping is None:
            return None

        self.__convert()
        message = self.__ocsfMessage()

        return message

def dumps( source ):
    """Converts a source record into a OCSF message"""
    ocsfAdapter = Ocsf( source )
    return ocsfAdapter.dumps()


