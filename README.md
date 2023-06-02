[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/Lobby "Gitter chat")

# Update Friday, June 2nd, 2023
A New Cloud Formation script will be posted Monday, June 5th, 2023 for Cisco Live which includes the latest updates including:
  * UI Management portal to view event activity and monitor data between Firepower and AWS Security Lake
  * Support for additional event types, including Malware and IDS Events
  * Enhanced Automation script to capture additional parameters to automate FMC connectivity

# License

Copyright (c) 2021 by Cisco Systems, Inc.

[Cisco EULA](http://www.cisco.com/c/en/us/about/legal/cloud-and-software/software-terms.html)

    ALL RIGHTS RESERVED. THESE SOURCE FILES ARE THE SOLE PROPERTY
    OF CISCO SYSTEMS, Inc. AND CONTAIN CONFIDENTIAL  AND PROPRIETARY
    INFORMATION.  REPRODUCTION OR DUPLICATION BY ANY MEANS OF ANY
    PORTION OF THIS SOFTWARE WITHOUT PRIOR WRITTEN CONSENT OF
    CISCO SYSTEMS, Inc. IS STRICTLY PROHIBITED.

# eStreamer eNcore
The Cisco eStreamer client for Open Cyber Security Framework (OCSF) 

The Cisco Event Streamer (also known as eStreamer) allows you to stream System intrusion,
discovery, and connection data from Firepower Management Center or managed device (also
referred to as the eStreamer server) to external client applications.

eStreamer responds to client requests with terse, compact, binary encoded messages – this
keeps it fast.

eNcore is a new all-purpose client which requests all possible events from eStreamer, parses
the binary content and outputs events in various formats to support other SIEMs.

This edition of eStreamer has been specificially tailored to provide OCSF compliant Network Activity events in both json and parquet


# Support
This is a beta version of eNcore. Before the General Availability release this will be
updated with details of paying for and receiving support.

Detailed setup instructions for the CLI are included here, the specific implementation correspondences to Microsoft Sentinel integration but the CLI is the same setup
https://www.cisco.com/c/en/us/td/docs/security/firepower/70/api/eNcore/eNcore_Operations_Guide_v08.html


# Quick install on AWS ec2

* Upload ./eNcoreCloudFormation.yaml to AWS Cloud Formation
  - Configure the FMC IP
  - Server size (defaults to t4.large)
  - S3 Bucket - this is the s3 path that will host paritioned data, the /ext/SOURCE_NAME needs to be provided in addition to the root s3 bucket location (ex. us-east-2-accountid/ex/MYSOURCE)
  - AWS Account Id

* Run eNcore: `./encore.sh`
* Run a connectivity test: `./encore.sh test` (and enter the pkcs12 password)
* View the log output `tail -f estreamer.log`
* `./encore.sh foreground` - run in the foreground
* `./encore.sh start` - starts a background task
* `./encore.sh stop` - this will stop the background task
* `./encore.sh restart` - this will restart the background task
