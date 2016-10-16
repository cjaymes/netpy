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

from net.Message import Message

################ Skipping ################
def test_skip_bytes_without_bits():
    msg = Message(b'\x00\x00\x33')
    msg._skip_bytes(2)
    assert(msg._unpack_bytes(1) == b'\x33')

def test_skip_bytes_with_bits():
    msg = Message(b'\x00\x00\x33')
    msg._skip_bits(4)
    assert(msg._byte_offset == 0)
    assert(msg._bit_offset == 4)
    msg._skip_bytes(1)
    assert(msg._byte_offset == 2)
    assert(msg._bit_offset == 0)
    assert(msg._unpack_bytes(1) == b'\x33')

def test_skip_bytes_beyond_end():
    msg = Message(b'\x00\x00\x33')
    with pytest.raises(IndexError):
        msg._skip_bytes(9)

def test_skip_bits_within_byte():
    msg = Message(b'\x13')
    msg._skip_bits(4)
    assert(msg._byte_offset == 0)
    assert(msg._bit_offset == 4)
    assert(msg._unpack_unsigned_integer(bits=4) == 3)

def test_skip_bits_between_byte():
    msg = Message(b'\x12\x34\x56\x78\x9A')
    msg._skip_bits(9)
    assert(msg._byte_offset == 1)
    assert(msg._bit_offset == 1)
    assert(msg._unpack_unsigned_integer(bits=7) == 0x34)

def test_skip_bits_beyond_end():
    msg = Message(b'\x12')
    with pytest.raises(IndexError):
        msg._skip_bits(9)

################ Unpacking ################
def test_unpack_bytes_1():
    msg = Message(b'\x33')
    assert(msg._unpack_bytes(1) == b'\x33')

def test_unpack_bytes_3():
    msg = Message(b'\x11\x22\x33')
    assert(msg._unpack_bytes(3) == b'\x11\x22\x33')

def test_unpack_string():
    msg = Message(b'\x48\x65\x6c\x6c\x6f\x33')
    assert(msg._unpack_string(5) == 'Hello')

def test_unpack_string_beyond_end():
    msg = Message(b'\x48\x65\x6c\x6c\x6f\x33')
    with pytest.raises(IndexError):
        msg._unpack_string(9)

def test_unpack_pascal_string():
    msg = Message(b'\x05\x48\x65\x6c\x6c\x6f\x33')
    assert(msg._unpack_pascal_string() == 'Hello')

def test_unpack_pascal_string_beyond_end():
    msg = Message(b'\x09\x48\x65\x6c\x6c\x6f\x33')
    with pytest.raises(IndexError):
        msg._unpack_pascal_string()

# def test_unpack_terminated_string():
#     assert(False)
#
# def test_unpack_unterminated_string():
#     assert(False)
#
# def test_unpack_big_endian_byte_order():
#     assert(False)
#
# def test_unpack_little_endian_byte_order():
#     assert(False)
#
# def test_unpack_native_byte_order():
#     assert(False)
#
# def test_unpack_signed_integer_8bit():
#     assert(False)
#
# def test_unpack_signed_integer_16bit():
#     assert(False)
#
# def test_unpack_signed_integer_32bit():
#     assert(False)
#
# def test_unpack_signed_integer_64bit():
#     assert(False)
#
# def test_unpack_unsigned_integer_8bit():
#     assert(False)
#
# def test_unpack_unsigned_integer_16bit():
#     assert(False)
#
# def test_unpack_unsigned_integer_32bit():
#     assert(False)
#
# def test_unpack_unsigned_integer_64bit():
#     assert(False)
#
# def test_unpack_bool_8bit():
#     assert(False)
#
# def test_unpack_bool_1bit():
#     assert(False)
#
# def test_unpack_float():
#     assert(False)
#
# def test_unpack_double():
#     assert(False)

################ Packing ################

# def test_pack_bytes():
#     assert(False)
#
# def test_pack_string():
#     assert(False)
#
# def test_pack_string_beyond_end():
#     assert(False)
#
# def test_pack_sized_string():
#     assert(False)
#
# def test_pack_sized_string_beyond_end():
#     assert(False)
#
# def test_pack_terminated_string():
#     assert(False)
#
# def test_pack_big_endian_byte_order():
#     assert(False)
#
# def test_pack_little_endian_byte_order():
#     assert(False)
#
# def test_pack_native_byte_order():
#     assert(False)
#
# def test_pack_signed_integer_8bit():
#     assert(False)
#
# def test_pack_signed_integer_16bit():
#     assert(False)
#
# def test_pack_signed_integer_32bit():
#     assert(False)
#
# def test_pack_signed_integer_64bit():
#     assert(False)
#
# def test_pack_unsigned_integer_8bit():
#     assert(False)
#
# def test_pack_unsigned_integer_16bit():
#     assert(False)
#
# def test_pack_unsigned_integer_32bit():
#     assert(False)
#
# def test_pack_unsigned_integer_64bit():
#     assert(False)
#
# def test_pack_bool_8bit():
#     assert(False)
#
# def test_pack_bool_1bit():
#     assert(False)
#
# def test_pack_float():
#     assert(False)
#
# def test_pack_double():
#     assert(False)
#
