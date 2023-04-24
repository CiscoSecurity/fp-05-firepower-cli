"""
Transforms to and from JSON and a dict
"""
#********************************************************************
#      File:    netwitness.py
#      Author:  Sam Strachan
#
#      Description:
#       Netwitness adapter
#
#      Copyright (c) 2023 by Cisco Systems, Inc.
#
#       ALL RIGHTS RESERVED. THESE SOURCE FILES ARE THE SOLE PROPERTY
#       OF CISCO SYSTEMS, Inc. AND CONTAIN CONFIDENTIAL  AND PROPRIETARY
#       INFORMATION.  REPRODUCTION OR DUPLICATION BY ANY MEANS OF ANY
#       PORTION OF THIS SOFTWARE WITHOUT PRIOR WRITTEN CONSENT OF
#       CISCO SYSTEMS, Inc. IS STRICTLY PROHIBITED.
#
#*********************************************************************/

from __future__ import absolute_import
import json
import socket
import estreamer
import time
import os

class UTF8Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)

def loads( line ):
    """Converts a json line back into a dict"""
    return json.loads( line )

def dumps( data , settings):
    """Serializes the incoming object as a json string"""
    priority = "<22>"
    application = "estreamer"
    timestamp = ""
    pid = os.getpid()
    host = socket.gethostname()

    if 'archiveTimestamp' in data :
        timestamp = estreamer.common.convert.toIso8601( data['archiveTimestamp'] )

    return "{0} {1} {2} {3} {4} {5}".format( priority, timestamp, host, application, pid, json.dumps(data,cls=UTF8Encoder))
