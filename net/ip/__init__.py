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

import logging
import struct

from net.ip.IPv4Packet import IPv4Packet
from net.ip.IPv6Packet import IPv6Packet

logger = logging.getLogger(__name__)

IPV4_BLOCK_CURRENT = '0.0.0.0/8'
IPV4_BLOCK_PRIVATE_CLASS_A = '10.0.0.0/8'
IPV4_BLOCK_SHARED_ADDRESS_SPACE = '100.64.0.0/10'
IPV4_BLOCK_LOOPBACK = '127.0.0.0/8'
IPV4_BLOCK_LINK_LOCAL = '169.254.0.0/16'
IPV4_BLOCK_PRIVATE_CLASS_B = '172.16.0.0/12'
IPV4_BLOCK_IETF_PROTOCOL_ASSIGNMENTS = '192.0.0.0/24'
IPV4_BLOCK_TEST_NET_1 = '192.0.2.0/24'
IPV4_BLOCK_IPV6_TO_IPV4_RELAY = '192.88.99.0/24'
IPV4_BLOCK_PRIVATE_CLASS_C = '192.168.0.0/16'
IPV4_BLOCK_NETWORK_BENCHMARK = '198.18.0.0/15'
IPV4_BLOCK_TEST_NET_2 = '198.51.100.0/24'
IPV4_BLOCK_TEST_NET_3 = '203.0.113.0/24'
IPV4_BLOCK_MULTICAST = '224.0.0.0/4'
IPV4_BLOCK_RESERVED = '240.0.0.0/4'
IPV4_BLOCK_BROADCAST = '255.255.255.255'

def from_bytes(buf):
    # parse the version
    (version,) = struct.unpack_from('>B', buf)
    version = version >> 4
    logger.debug('Parsing IP packet version: ' + str(version))
    if version == 4:
        return IPv4Packet.from_bytes(buf)
    elif version == 6:
        return IPv6Packet.from_bytes(buf)
    else:
        raise NotImplementedError("IP version " + str(version) + ' has not been implemented')
