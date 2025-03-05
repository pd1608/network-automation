#!/usr/bin/env python3

import NMtcpdump
NMtcpdump.checkmacadd("midtermcapturev6.pcap")
import NMdhcpserver
NMdhcpserver.connect()
import NMsnmp
import NMgithub