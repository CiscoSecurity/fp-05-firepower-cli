
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
from io import BytesIO
import boto3
import uuid

import pyarrow.parquet as pq
import pandas as pd
import json as json1
import estreamer.adapters.json as json2
from pyarrow import json

from estreamer.streams.base import Base

class FileStream( Base ):
    """Class for writing output to a rotated log file"""
    def __init__( self, directory, threshold, rotate, s3, region, accountId, filename = None, encoding = 'utf-8' ):
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

        self.bucket = s3
        self.account = accountId
        self.region = region
        self.aws_data = []



    @staticmethod
    def _sanitiseFilename( filename ):
        """Returns a clean filename - incase someone is trying to inject a path"""
        if filename is None or filename == '':
            filename = 'log{0}'

        elif filename.find('/') > -1:
            filename = filename.replace('/', '')

        return filename



    def _ensureFile( self , awsdir, awsname):

        directory = self.directory + '/'+ awsdir

        if not os.path.exists( directory ):
            os.makedirs( directory )

            #filename represents the latest timestamp
        filename = directory + awsname

        self.lines = 0
        self.file = io.open( filename, 'w+', encoding='utf-8')

    def onFileClose( self ):
        """Event handler for when a file is closed"""
        pass



    def _ensureRotation( self , data):
        if self.rotate:
            if self.lines >= self.threshold:
                self.file.close()
                self.onFileClose()
                self.file = None

    def close( self ):
        if self.file is not None and not self.file.closed:
            self.file.close()
            self.onFileClose()

    def _writeToS3(self, data) :

        event_hour = self.prevtime.strftime('%Y%m%d%H')
        s3_dir = "ext/CISCOFIREWALL/region={0}/accountId={1}/eventHour={2}/".format(self.region, self.account, event_hour)
        #local_dir = "ext\/CISCOFIREWALL\/region={0}\/accountId={1}\/eventHour={2}\/".format(self.region, self.account, event_hour)
        filename = '{0}{1}'.format(s3_dir, event_hour)
        format = "parquet"

        if format == 'parquet':
            out_buffer = BytesIO()

            if (self.aws_data is not None) :
                filename += '.gz.parquet'

                df = pd.json_normalize(self.aws_data)
                df.to_parquet(out_buffer, index=False, compression='gzip')
                object = self.s3.Object(self.bucket, filename)

                result = object.put(Body=out_buffer.getvalue())


        elif format == 'json':
            filename += '.json'
            object = self.s3.Object(self.bucket, filename)

            #convert string list to str then encode
            str_array = ""
            for elem in self.aws_data :
                str_array += elem

            result = object.put(Body=str_array.encode('utf-8'))


        local_file = '{0}.json'.format(event_hour)

        self._ensureFile(s3_dir, local_file)

        self.file.write("[")

        for item in self.aws_data :
            self.file.write( json2.dumps(item) )
            self.file.write("\n")
            if self.lines != len(self.aws_data) - 1:
                self.file.write(",")
            self.lines += 1

        self.file.write("]")

         #resume with the next parition element at 00 hour
        self.file.flush()
        self.lines = 0
        self.aws_data = []
        self.aws_data.append(data)

    def write( self, data):
        """Writes to the underlying stream"""

#        self._ensureFile()
#        self.file.write( data.encode( self.encoding ).decode('utf-8') )
#        self.file.flush()
#        self.lines += 1

        pos = data.find('"time": ')
        if pos != -1:

            offset = 8
            #fixed characters for epoch time, offset
            #pos -3 since datetime doesn't support finer than millis
            try :
                self.prevtime = self.currtime
                self.currtime = datetime.datetime.fromtimestamp(int(data[pos+8:pos+18]))

                if self.prevtime is not None :
                    if self.prevtime.hour != self.currtime.hour:
                        self._writeToS3(json2.loads(data))
                    else :
                        #self.aws_data += data
                        self.aws_data.append(json2.loads(data))

                else :
                    #self.aws_data = data
                    self.aws_data.append(data)

            except :
                 raise estreamer.EncoreException('Unrecognised value: {0} in {1}'.format( data[pos+8:pos+18], data) )

#        self._ensureRotation(data)
