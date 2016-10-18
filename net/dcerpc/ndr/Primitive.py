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
class Primitive(Structure):
    def __init__(self, val=None):
        if val is not None:
            self.value = val

    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other
