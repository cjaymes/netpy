# Copyright 2016 Casey Jaymes

# This file is part of NetPy.
#
# NetPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NetPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NetPy.  If not, see <http://www.gnu.org/licenses/>.

import struct
import logging
import ipaddress

from net.ip.IPPacket import IPPacket

logger = logging.getLogger(__name__)
class IPv4Packet(IPPacket):
    @staticmethod
    def from_bytes(buf):
        pkt = IPv4Packet()
        (
            b1,
            b2,
            pkt.total_length,
            pkt.identification,
            i1,
            pkt.time_to_live,
            pkt.protocol,
            pkt.header_checksum,
            src,
            dest,
        ) = struct.unpack_from('>BBHHHBBHLL', buf)
        pkt.version = b1 >> 4
        pkt.ihl = b1 & 0xF
        pkt.dscp = b2 >> 2
        pkt.ecn = b2 & 0x3
        pkt.flags = i1 >> 13
        pkt.flag_reserved = (pkt.flags >> 7) == 1
        pkt.flag_dont_fragment = ((pkt.flags >> 6) & 0x1) == 1
        pkt.flag_more_fragments = ((pkt.flags >> 5) & 0x1) == 1
        pkt.fragment_offset = i1 & 0x1FFF
        pkt.source = ipaddress.IPv4Address(src)
        pkt.destination = ipaddress.IPv4Address(dest)
        if pkt.ihl == 5:
            pkt.options = None
            pkt.data = buf[20:]
        elif pkt.ihl >= 6 and pkt.ihl <= 15:
            pkt.options = buf[20:(pkt.ihl * 4)]
            pkt.data = buf[(20 + pkt.ihl * 4):]
        else:
            raise RuntimeError('Invalid IHL value for packet: ' + str(pkt.ihl))
        return pkt

    def __str__(self):
        if self.ihl > 5:
            opt = ', Options: ' + self.options
        else:
            opt = ''
        return 'IP Packet Version: ' + str(self.version) \
            + ', IHL: ' + str(self.ihl) \
            + ', DSCP: ' + str(self.dscp) \
            + ', ECN: ' + str(self.ecn) \
            + ', Total Length: ' + str(self.total_length) \
            + ', Flags: ' + str(self.flags) \
            + ', Identification: ' + str(self.identification) \
            + ', Fragment Offset: ' + str(self.fragment_offset) \
            + ', Time To Live: ' + str(self.time_to_live) \
            + ', Protocol: ' + str(self.protocol) \
            + ', Header Checksum: ' + self.header_checksum.hex \
            + ', Source IP Address: ' + self.source \
            + ', Destination IP Address: ' + self.destination \
            + opt
