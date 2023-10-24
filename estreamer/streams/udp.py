
#********************************************************************
#      File:    udp.py
#      Author:  Sam Strachan
#
#      Description:
#       This writes to a udp port with a stream interface
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

import socket
import time
import estreamer.crossprocesslogging as logging
from estreamer.common.convert import isInt
from estreamer.streams.base import Base

# See: # https://wiki.python.org/moin/UdpCommunication

class UdpStream( Base ):
    """Creates a UDP socket and sends messages to it"""
    def __init__( self, host, port, encoding = 'utf-8' ):
        self.host = host
        self.port = port

        # If there's a problem with the host or port, fail fast.
        if len( self.host.strip() ) == 0:
            raise Exception('UdpStream must have a host specified.')

        if not isInt( self.port ):
            raise Exception('UdpStream must have an integer port specified.')

        self.encoding = encoding
        self.socket = None

        self.logger = logging.getLogger( self.__class__.__name__ )

    def __connect( self ):


        while True :
            try:

                self.logger.debug('Connecting to {0}:{1}'.format(self.host, self.port ))

                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.socket.connect((self.host,self.port))
                break

            except OSError as ose :

                self.logger.error(  "Socket Connection Error [{2}] - Cannot connect to host {0}:{1} - Retrying ...".format(self.host,self.port, ose))
                time.sleep(2)

    def close( self ):
        try:
            self.socket.shutdown( socket.SHUT_RDWR )
            self.socket.close()
            self.socket = None

        except AttributeError:
            pass

    def write( self, data ):

        while True :
            if self.socket is None:
                self.__connect()

            else :
                try:
                    self.logger.debug('Sending {2} to {0}:{1}'.format(self.host, self.port , data))
                    self.socket.sendall( data.encode( self.encoding ) )
                    break

                except OSError as ex: 
                    self.logger.error("Error [{0}] writing to endpoint {1}:{2} -- Retrying...".format(ex, self.host, self.port))
                    time.sleep(1)
                    self.socket = None

