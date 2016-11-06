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
    _FORMAT = (
        ('int_repr', 'uint:4'),
        ('char_repr', 'uint:4'),
        ('float_repr', 'uint:8'),
        ('reserved0', 'pad:8'),
        ('reserved1', 'pad:8'),
    )

    CHAR_FORMAT_ASCII = 0
    CHAR_FORMAT_EBCDIC = 1

    BYTE_ORDER_BIG_ENDIAN = 0
    BYTE_ORDER_LITTLE_ENDIAN = 1

    FLOAT_FORMAT_IEEE   = 0
    FLOAT_FORMAT_VAX    = 1
    FLOAT_FORMAT_CRAY   = 2
    FLOAT_FORMAT_IBM    = 3
