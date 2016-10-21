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

from net.dcerpc.ndr.Character import Character

def test_from_bytes():
    val = Character.from_bytes(b'a')
    assert(val == 'a')
    val = Character.from_bytes(b'A')
    assert(val == 'A')
    val = Character.from_bytes(b'5')
    assert(val == '5')
    val = Character.from_bytes(b'.')
    assert(val == '.')

def test_to_bytes():
    val = Character('a')
    assert(val.to_bytes() == b'a')
    val = Character('!')
    assert(val.to_bytes() == b'!')
