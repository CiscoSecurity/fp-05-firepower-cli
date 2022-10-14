
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
from array import array
import binascii
import copy
import time
import socket
import estreamer
import estreamer.adapters.kvpair
import estreamer.definitions as definitions
import estreamer.common
import estreamer.adapters.json
from estreamer.ocsf import Cloud
from estreamer.ocsf import NetworkActivity
from estreamer.ocsf import NetworkEndpoint
from estreamer.ocsf import NetworkProxy
from estreamer.ocsf import NetworkTraffic
from estreamer.ocsf import Metadata
from estreamer.ocsf import User
from estreamer.ocsf import TLS
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
OCSF_DEV_VERSION = '7.1'

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

def __networkType ( data ) :
    networkObj = NetworkActivity( data )
    members = [attr for attr in vars(networkObj) if not callable(getattr(networkObj, attr)) and not attr.startswith("__")]

    network_attr = {}
    for m in members :
        network_attr[m] = getattr(networkObj, m)

    return __nonEmptyValues(network_attr)


def __ipv6( ipAddress ):
    if ipAddress == '::':
        return ''

    elif ipAddress.startswith('::ffff:'):
        return ''

    elif ipAddress.find(':') > -1:
        return ipAddress

    return ''

def __profiles(data) :

   profiles = []
   if data['recordType'] == 71 :
      profiles.append("user")

   return profiles["user"]

def __nonEmptyValues( data ) :

    return {k: v for k, v in data.items() if v != ""}


MAPPING = {

    # 71
    definitions.RECORD_RNA_CONNECTION_STATISTICS: {

        'network': lambda rec : __networkType(rec) ,

        'lambdas': {
            'dst_endpoint': lambda rec : __nonEmptyValues ( vars ( NetworkEndpoint ( rec, rec['responderIpAddress'], rec['responderPort']) ) ),
            'metadata': lambda rec : __nonEmptyValues(vars( Metadata(rec) ) ),
            'src_endpoint': lambda rec : __nonEmptyValues ( vars ( NetworkEndpoint ( rec, rec['initiatorIpAddress'], rec['initiatorPort']) ) ),
            'tls': lambda rec : __nonEmptyValues ( vars ( TLS(rec) ) )
        },

        'fields': {
            'protocol': 'proto',
            'clientApplicationId': 'app_id',
            'connectionCounter': 'count', 
            'lastPacketTimestamp': '', 
            'initiatorTransmittedBytes': 'bytesOut',
            'responderTransmittedBytes': 'bytesIn',
            'userId': 'user',
            'applicationId': 'app',
            'securityIntelligenceList1': 'sec_intel_events',
        },

        'viewdata': {
            View.PROTOCOL: 'proto'
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
        self.network = {}

        if 'recordType' in self.record:
            if self.record['recordType'] in MAPPING:
                self.mapping = MAPPING[ self.record['recordType'] ]
                self.output = {}
               

    @staticmethod
    def __networkType ( data ) :
        networkObj = NetworkActivity( data )
        members = [attr for attr in vars(networkObj) if not callable(getattr(networkObj, attr)) and not attr.startswith("__")]

        network_attr = {}
        for m in members :
            network_attr[m] = getattr(networkObj, m)

        return network_attr


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
                unmapped[target] = self.record[source] 

        self.output['unmapped'] = unmapped

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


        function = self.mapping['network']
        self.network = function (self.record)

        keys = list(self.output.keys())
        for key in keys:
            if isinstance( self.output[ key ], six.string_types) and len( self.output[ key ] ) == 0:
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
        self.output = self.output | self.network
        data = Ocsf.__sanitize( self.output )

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


