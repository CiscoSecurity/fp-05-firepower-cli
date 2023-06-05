
#********************************************************************
#      File:    eventrate.py
#      Author:  Sam Strachan
#
#      Description:
#       Manages reading and writing to a bookmark file
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
import json
import os
import io
import estreamer.crossprocesslogging as logging

class EventRate( object ):
    """The bookmark class abstracts reading, writing and managing bookmarks"""
    def __init__( self, filepath ):
        self.store = {}
        self.logger = logging.getLogger( self.__class__.__name__ )
        self.filepath = filepath
        self.isDirty = False

        if not os.path.exists( filepath ):
            self.logger.info('Event Rate file {0} does not exist.'.format( filepath ))

        else:
            with io.open( filepath, 'r' ) as reader:
                try:
                    self.store = json.loads( reader.read() )
                    self.logger.info('Opening event rate file {0}.'.format( filepath ))
                except ValueError:
                    self.logger.info(
                        'Event Rate file {0} in unexpected format.'.format( filepath ))

                    self.store = {}

            # Just in case someone has put something weird in the file
            if not isinstance( self.store, dict ):
                self.store = {}



    def save( self , data):
        """Saves the current event rate"""
        try:
            with io.open( self.settings.eventRateFilepath(), 'a' ) as eventRateFile:
                json.dump( {
                    'event': data
                }, eventRateFile )

        except Exception as ex:
            self.logger.info('Filo I/O Error - Attemping to save status to disk')
            self.logger.exception( ex )


    def read( self ):
        """Reads the time from a specified source"""
        eventRatePath = self.settings.eventRateFilepath()

        try:
            with io.open( eventRateFilepath, 'r' ) as eventRateFile:
                self.store = json.load( eventRateFile )
                #self. = status['state']['id']
                #stateDescription = status['state']['description']

        except Exception as ex:
            self.logger.info('Filo I/O Error - Attemping to save status to disk')
            self.logger.exception( ex )


        return 0
