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

import sys
import os
sys.path.insert(0, os.path.abspath("."))
import logging
logging.basicConfig(level=logging.DEBUG)
import pytest
import ipaddress

import net.ip

TEST1 = b'\x45\x00\
\x01\x94\x4f\x92\x00\x00\x80\x11\x77\xcc\xac\x16\xb2\xea\x0a\x0a\
\x08\xf0\x00\x43\x00\x43\x01\x80\x72\x0e\x02\x01\x06\x01\x77\x71\
\xcf\x85\x00\x0a\x00\x00\x00\x00\x00\x00\x0a\x0a\x08\xeb\xac\x16\
\xb2\xea\x0a\x0a\x08\xf0\x00\x0e\x86\x11\xc0\x75\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x02\x01\x04\xff\
\xff\xff\x00\x36\x04\xac\x16\xb2\xea\x33\x04\x00\x00\xa8\xc0\x03\
\x04\x0a\x0a\x08\xfe\x06\x08\x8f\xd1\x04\x01\x8f\xd1\x05\x01\x42\
\x0e\x31\x37\x32\x2e\x32\x32\x2e\x31\x37\x38\x2e\x32\x33\x34\x78\
\x05\x01\xac\x16\xb2\xea\x3d\x10\x00\x6e\x61\x74\x68\x61\x6e\x31\
\x63\x6c\x69\x65\x6e\x74\x69\x64\x5a\x1f\x01\x01\x00\xc8\x78\xc4\
\x52\x56\x40\x20\x81\x31\x32\x33\x34\x8f\xe0\xcc\xe2\xee\x85\x96\
\xab\xb2\x58\x17\xc4\x80\xb2\xfd\x30\x52\x16\x01\x14\x20\x50\x4f\
\x4e\x20\x31\x2f\x31\x2f\x30\x37\x2f\x30\x31\x3a\x31\x2e\x30\x2e\
\x31\xff'

def test_from_bytes():
    pkt = net.ip.from_bytes(TEST1)
    assert(pkt.version == 4)
    assert(pkt.ihl == 5)
    assert(pkt.dscp == 0)
    assert(pkt.ecn == 0)
    assert(pkt.total_length == 404)
    assert(pkt.ident == 0x4f92)
    assert(not pkt.flag_reserved)
    assert(not pkt.flag_dont_fragment)
    assert(not pkt.flag_more_fragments)
    assert(pkt.fragment_offset == 0)
    assert(pkt.time_to_live == 128)
    assert(pkt.header_checksum == 0x77cc)
    assert(pkt.source == ipaddress.IPv4Address('172.22.178.234'))
    assert(pkt.destination == ipaddress.IPv4Address('10.10.8.240'))

def test_to_bytes():
    pkt = net.ip.from_bytes(TEST1)
    assert(pkt.to_bytes() == TEST1)
