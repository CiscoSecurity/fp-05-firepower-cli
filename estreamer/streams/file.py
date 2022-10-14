
#********************************************************************
#      File:    file.py
#      Author:  Sam Strachan
#
#      Description:
#       This file encapsulates a file output stream and takes care of
#       creation, closing and rotating to new files
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
import os
import time
import datetime
import estreamer 
import io
import boto3
import uuid

import pyarrow.parquet as pq
import pandas as pd
import json

from estreamer.streams.base import Base

class FileStream( Base ):
    """Class for writing output to a rotated log file"""
    def __init__( self, directory, threshold, rotate, filename = None, encoding = 'utf-8' ):
        self.file = None
        self.lines = 0
        self.directory = os.path.abspath( directory )
        self.threshold = threshold
        self.rotate = rotate
        self.filename = FileStream._sanitiseFilename( filename )
        self.encoding = encoding
        self.currtime = None 
        self.prevtime = None
        self.s3 = boto3.resource('s3')
        self.bucket = "moose-secure-firewall-demo-v1"
        self.account = "645424132307"
        self.region = "us-east-1"
        self.location = "us"
        self.aws_data = ""



    @staticmethod
    def _sanitiseFilename( filename ):
        """Returns a clean filename - incase someone is trying to inject a path"""
        if filename is None or filename == '':
            filename = 'log{0}'

        elif filename.find('/') > -1:
            filename = filename.replace('/', '')

        return filename



    def _ensureFile( self ):
        if not self.file:
            millis = int( time.time() )
            if not os.path.exists( self.directory ):
                os.makedirs( self.directory )

            filename = self.directory + '/' + self.filename.format( millis )

            if os.path.exists( filename ):
                # This is so unlikely in the real world, but just incase
                var = str( millis ) + '-' + str( uuid.uuid4() )
                filename = self.directory + '/' + self.filename.format( var )

            self.lines = 0
            self.file = io.open( filename, 'w+' )



    def onFileClose( self ):
        """Event handler for when a file is closed"""
        pass



    def _ensureRotation( self , data):
        if self.rotate:
            if self.lines >= self.threshold:
                self.file.close()
                self.onFileClose()
                self.file = None

        
        if self.currtime is not None and self.prevtime is not None:

            diff = self.currtime - self.prevtime

            #“<source location>/region=<region>/AWS_account=<accountid>/eventhour=<yyyyMMddHH>/“
            event_hour = "{0}{1}{2}{3}".format(self.currtime.year, self.currtime.month, self.currtime.day, self.currtime.hour)

            s3_dir = "/region={0}/AWS_account={1}/eventhour={2}/".format(self.region, self.account, event_hour)

            if self.currtime.hour != self.prevtime.hour and 'time' in data and 'type_uid' in data:


#                data_dict = json.loads(self.aws_data)

#                for key, value in data_dict.items():
#                    data_dict[key] = [value]

#                df = pd.DataFrame(data_dict)
                object = self.s3.Object(self.bucket, '{0}data.log'.format(s3_dir))
                
                result = object.put(Body=self.aws_data.encode('utf-8'))

                self.aws_data = ""
                self.file.close()
                self.onFileClose()
                self.file = None


    def close( self ):
        if self.file is not None and not self.file.closed:
            self.file.close()
            self.onFileClose()



    def write( self, data ):
        """Writes to the underlying stream"""
        self._ensureFile()
        self.file.write( data.encode( self.encoding ).decode('utf-8') )
        #.decode('utf-8')
        self.file.flush()
        self.lines += 1

        if "time" in data and "type_uid" in data :
            self.prevtime = self.currtime

            pos = data.find('"time"')
            offset = 8
            #fixed characters for epoch time, offset
            #pos -3 since datetime doesn't support finer than millis
            try :
                self.currtime = datetime.datetime.fromtimestamp(int(data[pos+8:pos+18]))
                self.aws_data += data 
            except :
                 raise estreamer.EncoreException('Unrecognised value: {0} in {1}'.format( data[pos+8:pos+18], data) )

        self._ensureRotation(data)
