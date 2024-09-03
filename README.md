[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/Lobby "Gitter chat")

# End of Life (EOL)

The Encore CLI project is currently EOL (Effective 7/1/2024), as alternative we have several different eventing export options for customers and partners using this code base.

Alternative #1 - Splunk Customers

Cisco Security Cloud App - https://splunkbase.splunk.com/app/7404

The Cisco Security Cloud application offers a seamless integration experience for connecting your Cisco devices with Splunk, providing a rich and uniform interface. The application is equipped with detailed instructions to facilitate every step of the setup process and assists with monitoring to ensure that your data pipelines maintain their operational integrity.

The Cisco Security Cloud app combines the concept of both TA and Splunk App into a single offering to help improve the efficiency and effectiveness of your data analysis within Splunk, providing a more powerful and comprehensive solution for your monitoring and analytics needs.

As of June 5th, 2024, the application has been released as a BETA version and will receive ongoing updates, including new Cisco integrations and feature sets as the current Cisco Splunk integrations approach their end of life (EOL). The present version supports the following core application features:

Baseline Core Application Features

    -  Performance Monitoring, Resource Utilization and Error Handling
    -  Data Integrity and Observability
    -  Modular Application UX Configuration Setup 
    -  Baseline Analytics to showcase product integration and detections
    -  CIM 5.x coverage for bulk majority of event types in Secure Firewall, including IDS events
    
Alternative #2 - Non-Splunk Customers

eStreamer SDK - https://www.cisco.com/c/en/us/td/docs/security/firepower/741/api/FQE/secure_firewall_estreamer_fqe_guide_740/c_introduction_estreamer.html

The Secure Firewall System Event Streamer (eStreamer) uses a message-oriented protocol to stream events and host profile information to your client application. Your client can request fully-qualified events from a Management Center. Only connection events, intrusion events, intrusion event packets, and file events are available as fully-qualified events.

Your client application initiates the data stream by submitting request messages, which specify the data to be sent, and then controls the message flow from the Management Center or managed device after streaming begins. 

# License

Copyright (c) 2017 by Cisco Systems, Inc.

[Cisco EULA](http://www.cisco.com/c/en/us/about/legal/cloud-and-software/software-terms.html)

    ALL RIGHTS RESERVED. THESE SOURCE FILES ARE THE SOLE PROPERTY
    OF CISCO SYSTEMS, Inc. AND CONTAIN CONFIDENTIAL  AND PROPRIETARY
    INFORMATION.  REPRODUCTION OR DUPLICATION BY ANY MEANS OF ANY
    PORTION OF THIS SOFTWARE WITHOUT PRIOR WRITTEN CONSENT OF
    CISCO SYSTEMS, Inc. IS STRICTLY PROHIBITED.

# eStreamer eNcore
The Cisco eStreamer client. 

The Cisco Event Streamer (also known as eStreamer) allows you to stream System intrusion,
discovery, and connection data from Firepower Management Center or managed device (also
referred to as the eStreamer server) to external client applications.

eStreamer responds to client requests with terse, compact, binary encoded messages – this
keeps it fast.

eNcore is a new all-purpose client which requests all possible events from eStreamer, parses
the binary content and outputs events in various formats to support other SIEMs.

# Support
This is a beta version of eNcore. Before the General Availability release this will be
updated with details of paying for and receiving support.

Detailed setup instructions for the CLI are included here, the specific implementation correspondences to Microsoft Sentinel integration but the CLI is the same setup
https://www.cisco.com/c/en/us/td/docs/security/firepower/70/api/eNcore/eNcore_Operations_Guide_v08.html

# Python3

The 4.x branches of this project correspond to Python3 support, files use the future library as well as python3 executable, you may have to import the python3 equivalent of pip for openssl support

# Quick install
* Run eNcore: `./encore.sh`
* Run a connectivity test: `./encore.sh test` (and enter the pkcs12 password)
* View the log output `tail -f estreamer.log`
* `./encore.sh foreground` - run in the foreground
* `./encore.sh start` - starts a background task
* `./encore.sh stop` - this will stop the background task
* `./encore.sh restart` - this will restart the background task
