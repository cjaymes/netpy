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

PROTOCOLS = {
    0:      'IPv6 Hop-by-Hop Option (HOPOPT)',               # RFC 2460
    1:      'Internet Control Message Protocol (ICMP)',      # RFC 792
    2:      'Internet Group Management Protocol (IGMP)',     # RFC 1112
    3:      'Gateway-to-Gateway Protocol (GGP)',             # RFC 823
    4:      'IP in IP',                                      # RFC 2003
    5:      'Internet Stream Protocol (ST)',                 # RFC 1190, RFC 1819
    6:      'Transmission Control Protocol (TCP)',           # RFC 793
    7:      'Core-based trees (CBT)', # RFC 2189
    8:      'Exterior Gateway Protocol (EGP)', # RFC 888
    9:      'Interior Gateway Protocol (any private interior gateway (used by Cisco for their IGRP)) (IGP)', #
    10:      'BBN RCC Monitoring (BBN-RCC-MON)', #
    11:      'Network Voice Protocol (NVP-II)', # RFC 741
    12:      'Xerox PUP (PUP)', #
    13:      'ARGUS (ARGUS)', #
    14:      'EMCON (EMCON)', #
    15:      'Cross Net Debugger (XNET)', # IEN 158
    16:      'Chaos (CHAOS)', #
    17:      'User Datagram Protocol (UDP)', # RFC 768
    18:      'Multiplexing (MUX)', # IEN 90
    19:      'DCN Measurement Subsystems (DCN-MEAS)', #
    20:      'Host Monitoring Protocol (HMP)', # RFC 869
    21:      'Packet Radio Measurement (PRM)', #
    22:      'XEROX NS IDP (XNS-IDP)', #
    23:      'Trunk-1 (TRUNK-1)', #
    24:      'Trunk-2 (TRUNK-2)', #
    25:      'Leaf-1 (LEAF-1)', #
    26:      'Leaf-2 (LEAF-2)', #
    27:      'Reliable Datagram Protocol (RDP)', # RFC 908
    28:      'Internet Reliable Transaction Protocol (IRTP)', # RFC 938
    29:      'ISO Transport Protocol Class 4 (ISO-TP4)', # RFC 905
    30:      'Bulk Data Transfer Protocol (NETBLT)', # RFC 998
    31:      'MFE Network Services Protocol (MFE-NSP)', #
    32:      'MERIT Internodal Protocol (MERIT-INP)', #
    33:      'Datagram Congestion Control Protocol (DCCP)', # RFC 4340
    34:      'Third Party Connect Protocol (3PC)', #
    35:      'Inter-Domain Policy Routing Protocol (IDPR)', # RFC 1479
    36:      'Xpress Transport Protocol (XTP)', #
    37:      'Datagram Delivery Protocol (DDP)', #
    38:      'IDPR Control Message Transport Protocol (IDPR-CMTP)', #
    39:      'TP++ Transport Protocol (TP++)', #
    40:      'IL Transport Protocol (IL)', #
    41:      'IPv6 Encapsulation (IPv6)', # RFC 2473
    42:      'Source Demand Routing Protocol (SDRP)', # RFC 1940
    43:      'Routing Header for IPv6 (IPv6-Route)', # RFC 2460
    44:      'Fragment Header for IPv6 (IPv6-Frag)', # RFC 2460
    45:      'Inter-Domain Routing Protocol (IDRP)', #
    46:      'Resource Reservation Protocol (RSVP)', # RFC 2205
    47:      'Generic Routing Encapsulation (GRE)', # RFC 2784, RFC 2890
    48:      'Mobile Host Routing Protocol (MHRP)', #
    49:      'BNA (BNA)', #
    50:      'Encapsulating Security Payload (ESP)', # RFC 4303
    51:      'Authentication Header (AH)', # RFC 4302
    52:      'Integrated Net Layer Security Protocol (I-NLSP)', # TUBA
    53:      'SwIPe (SWIPE)', # IP with Encryption
    54:      'NBMA Address Resolution Protocol (NARP)', # RFC 1735
    55:      'IP Mobility (Min Encap) (MOBILE)', # RFC 2004
    56:      'Transport Layer Security Protocol (using Kryptonet key management) (TLSP)', #
    57:      'Simple Key-Management for Internet Protocol (SKIP)', # RFC 2356
    58:      'ICMP for IPv6 (IPv6-ICMP)', # RFC 4443, RFC 4884
    59:      'No Next Header for IPv6 (IPv6-NoNxt)', # RFC 2460
    60:      'Destination Options for IPv6 (IPv6-Opts)', # RFC 2460
    61:      'Any host internal protocol ()', #
    62:      'CFTP (CFTP)', #
    63:      'Any local network ()', #
    64:      'SATNET and Backroom EXPAK (SAT-EXPAK)', #
    65:      'Kryptolan (KRYPTOLAN)', #
    66:      'MIT Remote Virtual Disk Protocol (RVD)', #
    67:      'Internet Pluribus Packet Core (IPPC)', #
    68:      'Any distributed file system ()', #
    69:      'SATNET Monitoring (SAT-MON)', #
    70:      'VISA Protocol (VISA)', #
    71:      'Internet Packet Core Utility (IPCU)', #
    72:      'Computer Protocol Network Executive (CPNX)', #
    73:      'Computer Protocol Heart Beat (CPHB)', #
    74:      'Wang Span Network (WSN)', #
    75:      'Packet Video Protocol (PVP)', #
    76:      'Backroom SATNET Monitoring (BR-SAT-MON)', #
    77:      'SUN ND PROTOCOL-Temporary (SUN-ND)', #
    78:      'WIDEBAND Monitoring (WB-MON)', #
    79:      'WIDEBAND EXPAK (WB-EXPAK)', #
    80:      'International Organization for Standardization Internet Protocol (ISO-IP)', #
    81:      'Versatile Message Transaction Protocol (VMTP)', # RFC 1045
    82:      'Secure Versatile Message Transaction Protocol (SECURE-VMTP)', # RFC 1045
    83:      'VINES (VINES)', #
    84:      'TTP (TTP)', #
    84:      'Internet Protocol Traffic Manager (IPTM)', #
    85:      'NSFNET-IGP (NSFNET-IGP)', #
    86:      'Dissimilar Gateway Protocol (DGP)', #
    87:      'TCF (TCF)', #
    88:      'EIGRP (EIGRP)', #
    89:      'Open Shortest Path First (OSPF)', # RFC 1583
    90:      'Sprite RPC Protocol (Sprite-RPC)', #
    91:      'Locus Address Resolution Protocol (LARP)', #
    92:      'Multicast Transport Protocol (MTP)', #
    93:      'AX.25 (AX.25)', #
    94:      'KA9Q NOS compatible IP over IP tunneling (OS)', #
    95:      'Mobile Internetworking Control Protocol (MICP)', #
    96:      'Semaphore Communications Sec. Pro (SCC-SP)', #
    97:      'Ethernet-within-IP Encapsulation (ETHERIP)', # RFC 3378
    98:      'Encapsulation Header (ENCAP)', # RFC 1241
    99:      'Any private encryption scheme ()', #
    100:      'GMTP (GMTP)', #
    101:      'Ipsilon Flow Management Protocol (IFMP)', #
    102:      'PNNI over IP (PNNI)', #
    103:      'Protocol Independent Multicast (PIM)', #
    104:      'IBM\'s ARIS (Aggregate Route IP Switching) Protocol (ARIS)', #
    105:      'SCPS (Space Communications Protocol Standards) (SCPS)', # SCPS-TP[2]
    106:      'QNX (QNX)', #
    107:      'Active Networks (A/N)', #
    108:      'IP Payload Compression Protocol (IPComp)', # RFC 3173
    109:      'Sitara Networks Protocol (SNP)', #
    110:      'Compaq Peer Protocol (Compaq-Peer)', #
    111:      'IPX in IP (IPX-in-IP)', #
    112:      'Virtual Router Redundancy Protocol, Common Address Redundancy Protocol (not IANA assigned) (VRRP)', # VRRP:RFC 3768
    113:      'PGM Reliable Transport Protocol (PGM)', # RFC 3208
    114:      'Any 0-hop protocol ()', #
    115:      'Layer Two Tunneling Protocol Version 3 (L2TP)', # RFC 3931
    116:      'D-II Data Exchange (DDX) (DDX)', #
    117:      'Interactive Agent Transfer Protocol (IATP)', #
    118:      'Schedule Transfer Protocol (STP)', #
    119:      'SpectraLink Radio Protocol (SRP)', #
    120:      'Universal Transport Interface Protocol (UTI)', #
    121:      'Simple Message Protocol (SMP)', #
    122:      'Simple Multicast Protocol (SM)', # draft-perlman-simple-multicast-03
    123:      'Performance Transparency Protocol (PTP)', #
    124:      'Intermediate System to Intermediate System (IS-IS) Protocol over IPv4 (IS-IS over IPv4)', # RFC 1142 and RFC 1195
    125:      'Flexible Intra-AS Routing Environment (FIRE)', #
    126:      'Combat Radio Transport Protocol (CRTP)', #
    127:      'Combat Radio User Datagram (CRUDP)', #
    128:      'Service-Specific Connection-Oriented Protocol in a Multilink and Connectionless Environment (SSCOPMCE)', # ITU-T Q.2111 (1999)
    129:      'IPLT', #
    130:      'Secure Packet Shield (SPS)', #
    131:      'Private IP Encapsulation within IP (PIPE)', # Expired I-D draft-petri-mobileip-pipe-00.txt
    132:      'Stream Control Transmission Protocol (SCTP)', #
    133:      'Fibre Channel (FC)', #
    134:      'Reservation Protocol (RSVP) End-to-End Ignore (RSVP-E2E-IGNORE)', # RFC 3175
    135:      'Mobility Extension Header for IPv6 (Mobility Header)', # RFC 6275
    136:      'Lightweight User Datagram Protocol (UDPLite)', # RFC 3828
    137:      'Multiprotocol Label Switching Encapsulated in IP (MPLS-in-IP)', # RFC 4023
    138:      'MANET Protocols (manet)', # RFC 5498
    139:      'Host Identity Protocol (HIP)', # RFC 5201
    140:      'Site Multihoming by IPv6 Intermediation (Shim6)', # RFC 5533
    141:      'Wrapped Encapsulating Security Payload (WESP)', # RFC 5840
    142:      'Robust Header Compression (ROHC)', # RFC 5856

    253:      'Use for experimentation and testing', # RFC 3692
    254:      'Use for experimentation and testing', # RFC 3692
    255:      'Reserved for extra',
}
for i in range(143,252+1):
    PROTOCOLS[i] = 'UNASSIGNED'

def from_bytes(buf):
    # parse the version
    (version,) = struct.unpack_from('>B', buf)
    version = version >> 4
    logger.debug('Parsing IP packet version: ' + str(version))
    if version == 4:
        from net.ip.v4.Packet import Packet as IPv4Packet
        return IPv4Packet.from_bytes(buf)
    elif version == 6:
        from net.ip.v6.Packet import Packet as IPv6Packet
        return IPv6Packet.from_bytes(buf)
    else:
        raise NotImplementedError("IP version " + str(version) + ' has not been implemented')
