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

import inspect
import struct

class Message():
    BYTE_ORDER_NATIVE = 0
    BYTE_ORDER_LITTLE_ENDIAN = 1
    BYTE_ORDER_BIG_ENDIAN = 2
    BYTE_ORDER_NETWORK = BYTE_ORDER_BIG_ENDIAN

    def __init__(self, buf=None):
        self._buffer = buf
        self._byte_offset = 0
        self._bit_offset = 0

    def __align(self):
        if self._bit_offset != 0:
            self._bit_offset = 0
            self._byte_offset += 1

    def _skip_padding_bytes(self, length):
        self.__align()
        self._byte_offset += length

    def _skip_padding_bits(self, length):
        if int(length / 8) > 0:
            self._byte_offset += int(length / 8)
            self._bit_offset += length % 8
        else:
            self._bit_offset += length

    def _unpack_bytes(self, count):
        self.__align()

        start_offset = self._byte_offset
        end_offset = self._byte_offset + count

        value = self._buffer[start_offset:end_offset]

        self._byte_offset = end_offset

        return value

    def _unpack_string(self, count=1):
        self.__align()
        pass

    def _unpack_sized_string(self):
        self.__align()
        pass

    def _unpack_terminated_string(self, terminator='\0'):
        self.__align()
        pass

    def _unpack_signed_integer(self, bits=8, byte_order=BYTE_ORDER_NATIVE):
        pass

    def _unpack_unsigned_integer(self, bits=8, byte_order=BYTE_ORDER_NATIVE):
        if byte_order == Message.BYTE_ORDER_NATIVE:
            fmt = '='
        elif byte_order == Message.BYTE_ORDER_LITTLE_ENDIAN:
            fmt = '<'
        elif byte_order == Message.BYTE_ORDER_BIG_ENDIAN:
            fmt = '>'
        else:
            raise ValueError('Unknown byte order: ' + str(byte_order))

        if bits <= 0:
            raise ValueError('Cannot unpack <= 0 bit integer value')
        elif bits <= 8:
            fmt += 'B'
        elif bits <= 16:
            fmt += 'H'
        elif bits <= 32:
            fmt += 'I'
        elif bits <= 64:
            fmt += 'Q'
        else:
            raise ValueError('Cannot unpack integer value greater than 64 bits (try float/double)')

        (value,) = struct.unpack_from(fmt, self._buffer, self._byte_offset)

        if self._bit_offset != 0:
            # mask off the offset bits
            mask = 0xFF >> (8 - self._bit_offset)
            value = value & mask

        remaining_bits = 8 - (self._bit_offset + (bits % 8))
        value = value >> remaining_bits

        self._bit_offset += bits
        if int(self._bit_offset / 8) > 0:
            self._byte_offset += int(self._bit_offset / 8)
            self._bit_offset = self._bit_offset % 8

        return value

    def _unpack_bool(self, bits=8):
        pass

    def _unpack_float(self):
        self.__align()
        pass

    def _unpack_double(self):
        self.__align()
        pass
