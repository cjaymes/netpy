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

from net.dcerpc.ndr.FormatLabel import FormatLabel

TEST1 = b'\x00\x00\x00\x00'

def test_from_bytes():
    lbl = FormatLabel.from_bytes(TEST1)
    assert(lbl.int_repr == FormatLabel.CHAR_FORMAT_ASCII)
    assert(lbl.char_repr == FormatLabel.BYTE_ORDER_BIG_ENDIAN)
    assert(lbl.float_repr == FormatLabel.FLOAT_FORMAT_IEEE)

def test_to_bytes():
    lbl = FormatLabel.from_bytes(TEST1)
    assert(lbl.to_bytes() == TEST1)
