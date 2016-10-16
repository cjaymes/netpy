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
import logging

logger = logging.getLogger(__name__)
class Message():
    BYTE_ORDER_NATIVE = 0
    BYTE_ORDER_LITTLE_ENDIAN = 1
    BYTE_ORDER_BIG_ENDIAN = 2
    BYTE_ORDER_NETWORK = BYTE_ORDER_BIG_ENDIAN

    def __init__(self, buf=None):
        self._buffer = buf
        self._byte_offset = 0
        self._bit_offset = 0

    def __set_byte_offset(self, off):
        if off > len(self._buffer):
            raise IndexError('Tried skipping beyond end of buffer; len ' + str(len(self._buffer)))

        self._byte_offset = off

    def __set_bit_offset(self, off):
        if int(off / 8) > 0:
            new_byte_offset = self._byte_offset + int(off / 8)
            if new_byte_offset > len(self._buffer):
                raise IndexError('Tried skipping beyond end of buffer; len ' + str(len(self._buffer)))
            new_bit_offset = off % 8
            if new_byte_offset == len(self._buffer) \
                and new_bit_offset > 0:
                raise IndexError('Tried skipping beyond end of buffer; len ' + str(len(self._buffer)))

            self._byte_offset = new_byte_offset
            self._bit_offset = new_bit_offset
        else:
            new_bit_offset = off
            if self._byte_offset == len(self._buffer) \
                and new_bit_offset > 0:
                raise IndexError('Tried skipping beyond end of buffer; len ' + str(len(self._buffer)))

            self._bit_offset = new_bit_offset

    def __align(self):
        if self._bit_offset != 0:
            self.__set_bit_offset(0)
            self.__set_byte_offset(self._byte_offset + 1)

    def _skip_bytes(self, length):
        self.__align()
        self.__set_byte_offset(self._byte_offset + length)

    def _skip_bits(self, length):
        self.__set_bit_offset(self._bit_offset + length)

    def _unpack_bytes(self, length):
        self.__align()

        start_offset = self._byte_offset
        end_offset = self._byte_offset + length

        value = self._buffer[start_offset:end_offset]

        self.__set_byte_offset(end_offset)

        return value

    def _unpack_string(self, length):
        self.__align()

        fmt = '=' + str(length) + 's'
        logger.debug('Format: ' + fmt)

        try:
            (value,) = struct.unpack_from(fmt, self._buffer, self._byte_offset)
        except struct.error as e:
            raise IndexError(e)
        logger.debug('Unpacked: ' + str(value))

        value = value.decode()
        logger.debug('Decoded: ' + value)

        self.__set_byte_offset(self._byte_offset + length)

        return value

    def _unpack_pascal_string(self):
        self.__align()

        try:
            (value,) = struct.unpack_from('=B', self._buffer, self._byte_offset)
        except struct.error as e:
            raise IndexError(e)
        logger.debug('Unpacked: ' + str(value))

        try:
            (value,) = struct.unpack_from('=' + str(value + 1) + 'p', self._buffer, self._byte_offset)
        except struct.error as e:
            raise IndexError(e)
        logger.debug('Unpacked: ' + str(value))

        value = value.decode()
        logger.debug('Decoded: ' + value)

        self.__set_byte_offset(self._byte_offset + len(value) + 1)

        return value

    def _unpack_terminated_string(self, terminator='\x00'):
        if len(terminator) != 1:
            raise ValueError('Terminator must be a 1 byte string')
        self.__align()

        terminator = ord(terminator[0])
        value = ''
        i = self._byte_offset
        while(True):
            if i == len(self._buffer):
                raise IndexError('Reached end of buffer without finding terminator ' + str(terminator))
            if self._buffer[i] == terminator:
                break
            # TODO add unicode support
            value += chr(self._buffer[i])
            i += 1
        logger.debug('Unpacked: ' + str(value))

        self.__set_byte_offset(i)

        return value

    def _unpack_signed_integer(self, bits=8, byte_order=BYTE_ORDER_NATIVE):
        pass

    def _unpack_unsigned_integer(self, bits=8, byte_order=BYTE_ORDER_NATIVE):
        logger.debug('Capturing ' + str(bits) + ' in byte order ' + str(byte_order))
        logger.debug('Initial offsets: bit: ' + str(self._bit_offset) \
            + ', byte: ' + str(self._byte_offset))

        if byte_order == Message.BYTE_ORDER_NATIVE:
            fmt = '='
        elif byte_order == Message.BYTE_ORDER_LITTLE_ENDIAN:
            fmt = '<'
        elif byte_order == Message.BYTE_ORDER_BIG_ENDIAN:
            fmt = '>'
        else:
            raise ValueError('Unknown byte order: ' + str(byte_order))
        logger.debug('Format after byte order: ' + fmt)

        value_width = None
        if bits <= 0:
            raise ValueError('Cannot unpack <= 0 bit integer value')
        elif bits <= 8:
            fmt += 'B'
            value_width = 8
            mask = 0xff
        elif bits <= 16:
            fmt += 'H'
            value_width = 16
            mask = 0xffff
        elif bits <= 32:
            fmt += 'I'
            value_width = 32
            mask = 0xffffffff
        elif bits <= 64:
            fmt += 'Q'
            value_width = 64
            mask = 0xffffffffffffffff
        else:
            raise ValueError('Cannot unpack integer value greater than 64 bits (try float/double)')
        logger.debug('Format after bits: ' + fmt)
        bin_fmt = '0' + str(value_width) + 'b'

        try:
            (value,) = struct.unpack_from(fmt, self._buffer, self._byte_offset)
        except struct.error as e:
            raise IndexError(e)
        logger.debug('Unpacked value:                   0b' + format(value, bin_fmt) + '(' + hex(value) + ')')

        if self._bit_offset != 0:
            # mask off the offset bits
            mask = mask >> self._bit_offset
            logger.debug('Offset mask:                      0b' + format(mask, bin_fmt) + '(' + hex(mask) + ')')
        value = value & mask
        logger.debug('Value after bit offset masking:   0b' + format(value, bin_fmt) + '(' + hex(value) + ')')

        remaining_bits = value_width - (self._bit_offset + (bits % 8))
        value = value >> remaining_bits
        logger.debug('Value after shifting:             0b' + format(value, bin_fmt) + '(' + hex(value) + ')')

        self.__set_bit_offset(self._bit_offset + bits)

        logger.debug('Final offsets: bit: ' + str(self._bit_offset) \
            + ', byte: ' + str(self._byte_offset))

        return value

    def _unpack_bool(self, bits=8):
        pass

    def _unpack_float(self):
        self.__align()
        pass

    def _unpack_double(self):
        self.__align()
        pass
