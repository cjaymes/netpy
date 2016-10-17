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

from net.Structure import Structure

logger = logging.getLogger(__name__)
class FormatLabel(Structure):
    FORMAT_CHAR_ASCII = 0
    FORMAT_CHAR_EBCDIC = 1

    BYTE_ORDER_BIG_ENDIAN = 0
    BYTE_ORDER_LITTLE_ENDIAN = 1

    FORMAT_FLOAT_IEEE   = 0
    FORMAT_FLOAT_VAX    = 1
    FORMAT_FLOAT_CRAY   = 2
    FORMAT_FLOAT_IBM    = 3

    @staticmethod
    def from_bytes(buf):
        bs = BitStream(bytes=buf)
        lbl = FormatLabel()

        lbl.int_repr = bs.read('uint:4')
        lbl.char_repr = bs.read('uint:4')
        lbl.float_repr = bs.read('uint:8')
        bs.read('uint:8')   # reserved
        bs.read('uint:8')   # reserved

    def to_bytes():
        bs = bitstring.pack('uint:4, uint:4, uint:8, 0xFF, 0xFF', \
            self.int_repr, self.char_repr, self.float_repr)
        return bs.tobytes()
