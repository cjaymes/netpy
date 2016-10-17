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

from bitstring import BitStream
import logging
import ipaddress

from net.ip.IPPacket import IPPacket

logger = logging.getLogger(__name__)
class IPv4Packet(IPPacket):
    IP_OPTION_CLASS_CONTROL = 0
    # (reserved) = 1
    IP_OPTION_CLASS_DEBUG_MEASURE = 2
    # (reserved) = 3

    # IP_OPTION_CLASS_CONTROL
    IP_OPTION_NUMBER_END_OF_OPTION_LIST = 0
    IP_OPTION_NUMBER_NO_OPERATION = 1
    IP_OPTION_NUMBER_SECURITY = 2
    IP_OPTION_NUMBER_LOOSE_SOURCE_ROUTING = 3
    IP_OPTION_NUMBER_RECORD_ROUTE = 7
    IP_OPTION_NUMBER_STREAM_ID = 8
    IP_OPTION_NUMBER_STRICT_SOURCE_ROUTING = 9

    # IP_OPTION_CLASS_DEBUG_MEASURE
    IP_OPTION_NUMBER_INTERNET_TIMESTAMP = 4

    @staticmethod
    def from_bytes(buf):
        bs = BitStream(bytes=buf)
        pkt = IPv4Packet()

        pkt.version = bs.read('uint:4')
        pkt.ihl = bs.read('uint:4')
        pkt.dscp = bs.read('uint:6')
        pkt.ecn = bs.read('uint:2')
        pkt.total_length = bs.read('uint:16')
        pkt.ident = bs.read('uint:16')
        pkt.flag_reserved = bs.read('bool')
        pkt.flag_dont_fragment = bs.read('bool')
        pkt.flag_more_fragments = bs.read('bool')
        pkt.fragment_offset = bs.read('uint:13')
        pkt.time_to_live = bs.read('uint:8')
        pkt.protocol = bs.read('uint:8')
        # TODO The checksum field is the 16 bit one's complement of the one's
        # complement sum of all 16 bit words in the header.  For purposes of
        # computing the checksum, the value of the checksum field is zero.
        pkt.header_checksum = bs.read('uint:16')
        pkt.source = ipaddress.IPv4Address(bs.read('uint:32'))
        pkt.destination = ipaddress.IPv4Address(bs.read('uint:32'))

        if pkt.ihl == 5:
            pkt.options = None
        elif pkt.ihl >= 6 and pkt.ihl <= 15:
            pkt.options = []
            while(True):
                if bs.bytepos >= pkt.ihl * 4:
                    break
                #TODO padding (always ends on 32 bit boundary; implicit end of list)
                option = {}
                option['copy'] = bs.read('bool')
                option['class'] = bs.read('uint:2')
                option['number'] = bs.read('uint:5')

                if option['class'] == IPv4Packet.IP_OPTION_CLASS_CONTROL:
                    if option['number'] == IPv4Packet.IP_OPTION_NUMBER_END_OF_OPTION_LIST:
                        # end of options list
                        # no length or data
                        break
                    elif option['number'] == IPv4Packet.IP_OPTION_NUMBER_NO_OPERATION:
                        # no operation
                        # no length or data
                        pass
                    elif option['number'] == IPv4Packet.IP_OPTION_NUMBER_SECURITY:
                        # Security RFC 791
                        # 11 octet length
                        option['length'] = bs.unpack('uint:8')
                        if option['length'] != 11:
                            raise RuntimeError('Security IP Option with length other than 11')
                        option['data'] = bs.unpack('bytes:' + str(option['length'] - 2))
                    elif option['number'] == IPv4Packet.IP_OPTION_NUMBER_LOOSE_SOURCE_ROUTING:
                        # Loose Source Routing
                        # var octet length
                        option['length'] = bs.unpack('uint:8')
                        option['data'] = bs.unpack('bytes:' + str(option['length'] - 2))
                    elif option['number'] == IPv4Packet.IP_OPTION_NUMBER_RECORD_ROUTE:
                        # Record Route
                        # var octet length
                        option['length'] = bs.unpack('uint:8')
                        option['data'] = bs.unpack('bytes:' + str(option['length'] - 2))
                    elif option['number'] == IPv4Packet.IP_OPTION_NUMBER_STREAM_ID:
                        # Stream ID
                        # 4 octet length
                        option['length'] = bs.unpack('uint:8')
                        if option['length'] != 4:
                            raise RuntimeError('Stream ID IP Option with length other than 4')
                        option['data'] = bs.unpack('bytes:' + str(option['length'] - 2))
                    elif option['number'] == IPv4Packet.IP_OPTION_NUMBER_STRICT_SOURCE_ROUTING:
                        # Strict Source Routing
                        # var octet length
                        option['length'] = bs.unpack('uint:8')
                        option['data'] = bs.unpack('bytes:' + str(option['length'] - 2))
                    else:
                        raise RuntimeError('Unknown IP option: ' \
                            + 'class: ' + str(option['class'] \
                            + ', number: ' + str(option['number'])))
                elif option['class'] == IPv4Packet.IP_OPTION_CLASS_DEBUG_MEASURE:
                    if option['number'] == IPv4Packet.IP_OPTION_NUMBER_INTERNET_TIMESTAMP:
                        # Internet Timestamp
                        # var octet length
                        option['length'] = bs.unpack('uint:8')
                        option['data'] = bs.unpack('bytes:' + str(option['length'] - 2))
                    else:
                        raise RuntimeError('Unknown IP option: ' \
                            + 'class: ' + str(option['class'] \
                            + ', number: ' + str(option['number'])))
                else:
                    raise RuntimeError('Unknown IP option class: ' + str(option['class']))

        else:
            raise RuntimeError('Invalid IHL value for packet: ' + str(pkt.ihl))

        pkt.data = buf[(pkt.ihl * 4):]

        return pkt

    def __str__(self):
        return 'IP Packet Version: ' + str(self.version) \
            + ', IHL: ' + str(self.ihl) \
            + ', DSCP: ' + str(self.dscp) \
            + ', ECN: ' + str(self.ecn) \
            + ', Total Length: ' + str(self.total_length) \
            + ', Flags: [' \
            +   ('RESERVED,' if self.flag_reserved else 'Reserved,') \
            +   ('Don\'t Fragment,' if self.flag_dont_fragment else 'May Fragment,') \
            +   ('More Fragments]' if self.flag_more_fragments else 'Last Fragment]') \
            + ', Identification: ' + str(self.ident) \
            + ', Fragment Offset: ' + str(self.fragment_offset) \
            + ', Time To Live: ' + str(self.time_to_live) \
            + ', Protocol: ' + str(self.protocol) \
            + ', Header Checksum: ' + self.header_checksum.hex \
            + ', Source IP Address: ' + self.source \
            + ', Destination IP Address: ' + self.destination \
            + (', Options: ' + str(self.options) if self.ihl > 5 else '')
