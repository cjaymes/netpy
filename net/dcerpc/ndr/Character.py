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

from net.dcerpc.ndr.Primitive import Primitive

logger = logging.getLogger(__name__)
class Character(Primitive):
    _FORMAT = (
        ('value', 'bytes:1'),
    )

    def _set_field_value(self, name, value):
        if name == 'value':
            setattr(self, name, value.decode())
        else:
            super()._set_field_value(name, value)

    def _get_field_value(self, name):
        if name == 'value':
            return getattr(self, name).encode()
        else:
            return super()._get_field_value(name)
