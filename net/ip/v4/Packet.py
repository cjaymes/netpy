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

import bitstring
from bitstring import BitStream
import logging
import ipaddress

from net.Structure import Structure

logger = logging.getLogger(__name__)
class Packet(Structure):
    _FORMAT = (
        ('version', 'uint:4'),
        ('ihl', 'uint:4'),
        ('dscp', 'uint:6'),
        ('ecn', 'uint:2'),
        ('total_length', 'uint:16'),
        ('ident', 'uint:16'),
        ('flag_reserved', 'bool'),
        ('flag_dont_fragment', 'bool'),
        ('flag_more_fragments', 'bool'),
        ('fragment_offset', 'uint:13'),
        ('time_to_live', 'uint:8'),
        ('protocol', 'uint:8'),
        ('header_checksum', 'uint:16'),
        ('source', 'uint:32'),
        ('destination', 'uint:32'),
    )

    @classmethod
    def from_bytes(cls, buf):
        pkt = super(cls, cls).from_bytes(buf)

        # TODO The checksum field is the 16 bit one's complement of the one's
        # complement sum of all 16 bit words in the header.  For purposes of
        # computing the checksum, the value of the checksum field is zero.

        if pkt.ihl == 5:
            pkt.options = None
        elif pkt.ihl >= 6 and pkt.ihl <= 15:
            pkt.options = []
            # TODO
        else:
            raise RuntimeError('Invalid IHL value for packet: ' + str(pkt.ihl))

        pkt.data = buf[(pkt.ihl * 4):]

        return pkt

    def _set_field_value(self, name, value):
        if name == 'source' or name == 'destination':
            setattr(self, name, ipaddress.IPv4Address(value))
        else:
            return super()._set_field_value(name, value)

    def _get_field_value(self, name):
        if name == 'source' or name == 'destination':
            return int(getattr(self, name))
        else:
            return super()._get_field_value(name)

    def to_bytes(self):
        # # TODO ip options
        return super().to_bytes() + self.data

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
