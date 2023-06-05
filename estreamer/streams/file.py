
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
import sys

import pyarrow.parquet as pq
import pandas as pd
import json as json1
import estreamer.adapters.json as json2
from pyarrow import json

from estreamer.streams.base import Base

class FileStream( Base ):
    """Class for writing output to a rotated log file"""
    def __init__( self, directory, threshold, rotate, s3, region, awssource, accountId, filename = None, encoding = 'utf-8' ):
        self.file = None
        self.lines = 0
        self.directory = os.path.abspath( directory )
        self.threshold = threshold
        self.rotate = rotate
        self.filename = FileStream._sanitiseFilename( filename )
        self.encoding = encoding
        self.currtime = None 
        self.prevtime = time.time()
        self.size = 0
        self.s3 = boto3.resource('s3')
        self.awssource = awssource

        self.logger = estreamer.crossprocesslogging.getLogger(
            self.__class__.__name__ )

        self.bucket = s3
        self.account = accountId
        self.region = region
        self.aws_data = []
        self.logger.info("Initializing File Stream")



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

    def _saveS3Response( self, filename, result):
        """Saves the status to disk"""

        """{element:{data dict}, element{data dict}}}"""
        try:

            path =  '/ocsf/fp-05-firepower-cli/s3responses.dat'

            append = True if os.stat(path).st_size == 0 else False

            with io.open( path, 'w+', encoding='utf-8') as s3File:

                if(append) :
                    s3File.seek(-1, os.SEEK_END)
                    filehandle.truncate()
                    s3File.write(',')
                else :
                   s3File.write('{')

                self.logger.info(result)

                json1.dump( { result['ResponseMetadata']['RequestId'] : {
                    'HostId': result['ResponseMetadata']['HostId'],
                    'RequestId': result['ResponseMetadata']['RequestId'],
                    'Filename': filename.split("/")[-1],
                    'S3Parition': filename,
                    'HTTPStatus': str(result['ResponseMetadata']['HTTPStatusCode']),
                    'Transmitted': result['ResponseMetadata']['HTTPHeaders']['date'],
                    'Server': result['ResponseMetadata']['HTTPHeaders']['server'],
                    'eTag': str(result['ResponseMetadata']['HTTPHeaders']['etag']).strip('\"') }}
                , s3File)
                 
                s3File.write('}')


        except Exception as ex:
            self.logger.info('Filo I/O Error - Attemping to save status to disk')
            self.logger.exception( ex )

    def close( self ):
        if self.file is not None and not self.file.closed:
            self.file.close()
            self.onFileClose()

    def _writeToS3(self, data) :

        event_day = "{0}{1}{2}".format(self.currtime.month, self.currtime.day, self.currtime.year)
# ext/CISCOFIREWALL/region=us-east-1/accountId=411546959149/eventDay=1201970/ext/CISCOFIREWALL/region=us-east-1/accountId=411546959149/eventDay=1201970/1682103

        s3_dir = "ext/{3}/region={0}/accountId={1}/eventDay={2}/".format(self.region, self.account, event_day, self.awssource)
        filename = '{0}{1}'.format(s3_dir, str(self.currtime))
        format = "parquet"

        self.logger.info("Writing to S3 with partition - {0}{1}".format(self.bucket, filename))

        if format == 'parquet':
            out_buffer = BytesIO()

            if (self.aws_data is not None) :
                filename += '.gz.parquet'

#                aws_data =[{"unmapped": {"proto": 17, "app_id": 0, "count": 29502, "bytesOut": 42, "bytesIn": 0, "user": 9999997, "app": 0, "sec_intel_events": 0}, "dst_endpoint": {"ip": "192.168.0.255", "port": 31257}, "metadata": {"profiles": [], "product": {"name": "Secure Firewall", "version": "7.1", "vendor_name": "Cisco"}, "sequence": 0, "version": "1.0.0"}, "src_endpoint": {"ip": "10.1.80.89", "port": 44046}, "tls": {"client_ciphers": ["TLS_NULL_WITH_NULL_NULL"], "server_ciphers": ["Not Checked"], "version": "Unknown"}, "activity_name": "Unknown", "activity_id": 0, "app_name": "Unknown", "category_name": "Network Activity", "category_uid": 4, "class_name": "Network Activity", "class_uid": 4001, "count": 29502, "duration": 0, "end_time": 1677523290000, "time": 1677523290000, "message": "True", "severity": "Unknown", "severity_id": 0, "start_time": 1677523290000, "status": "Unknown", "status_code": "0", "status_id": 0, "timezone_offset": 0, "type_uid": 400100, "type_name": "Network Activity: Unknown"},{"unmapped": {"proto": 17, "app_id": 0, "count": 29502, "bytesOut": 42, "bytesIn": 0, "user": 9999997, "app": 0, "sec_intel_events": 0}, "dst_endpoint": {"ip": "192.168.0.255", "port": 31257}, "metadata": {"profiles": [], "product": {"name": "Secure Firewall", "version": "7.1", "vendor_name": "Cisco"}, "sequence": 0, "version": "1.0.0"}, "src_endpoint": {"ip": "10.1.80.89", "port": 44046}, "tls": {"client_ciphers": ["TLS_NULL_WITH_NULL_NULL"], "server_ciphers": ["Not Checked"], "version": "Unknown"}, "activity_name": "Unknown", "activity_id": 0, "app_name": "Unknown", "category_name": "Network Activity", "category_uid": 4, "class_name": "Network Activity", "class_uid": 4001, "count": 29502, "duration": 0, "end_time": 1677523290000, "time": 1677523290000, "message": "True", "severity": "Unknown", "severity_id": 0, "start_time": 1677523290000, "status": "Unknown", "status_code": "0", "status_id": 0, "timezone_offset": 0, "type_uid": 400100, "type_name": "Network Activity: Unknown"}]
                df = pd.json_normalize(data, max_level=0)
                df.to_parquet(out_buffer, index=False, compression='gzip')
#               modified to new security lake s3://
#                object = self.s3.Object(self.bucket, filename)
                object = self.s3.Object(self.bucket, filename)
                result = object.put(Body=out_buffer.getvalue())
                self._saveS3Response(filename, result)
                self.logger.info("Sent to S3 with response: {0}".format(result))

        self.lines = 0
        self.prevtime = time.time()

    def write( self, data):
        """Writes to the underlying stream"""

        self.lines += 1
        try :
            _byte = data.encode("utf-8")
            self.size += len(_byte) / 1024 / 1024 
            jdata = json2.loads(data) 

        except Exception as ex:
            self.logger.info("Error in JSON decode data: {0}".format(data))
            self.logger.exception( ex )

        limit = self.lines

        try :

            if 'start_time' in jdata : 
                epoch = int(jdata['start_time'])
                self.currtime = datetime.datetime.fromtimestamp(epoch)

                time_buffer = time.time() - self.prevtime

                if self.size < 256 and time_buffer < 60 :
                    self.aws_data.append(jdata)
                else :
                    self.prevtime = time.time()
                    self._writeToS3(self.aws_data)
                    self.aws_data.clear()
                    self.size = 0
                    self.aws_data.append(jdata)
            else :
                self._writeToS3(jdata)
                self.aws_data.clear()

        except :
              raise estreamer.EncoreException('Unable to Write to S3 Bucket')

#        self._ensureRotation(data)
