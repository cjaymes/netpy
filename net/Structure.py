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
import inspect
import logging

logger = logging.getLogger(__name__)
class Structure():
    @classmethod
    def from_bytes(cls, buf):
        if not hasattr(cls, '_FORMAT') or not isinstance(cls._FORMAT, tuple):
            raise NotImplementedError(inspect.stack()[0][3] + '() has not been implemented in subclass: ' + cls.__name__)

        bs = BitStream(bytes=buf)
        obj = cls()
        for field in cls._FORMAT:
            name, fmt = field
            obj._set_field_value(name, bs.read(fmt))

        return obj

    def _set_field_value(self, name, value):
        setattr(self, name, value)

    def _get_field_value(self, name):
        return getattr(self, name)

    def to_bytes(self):
        if not hasattr(self.__class__, '_FORMAT') or not isinstance(self.__class__._FORMAT, tuple):
            raise NotImplementedError(inspect.stack()[0][3] + '() has not been implemented in subclass: ' + self.__class__.__name__)

        fmts = []
        values = {}
        for field in self.__class__._FORMAT:
            name, fmt = field
            fmts.append(fmt + '=' + name)
            values[name] = self._get_field_value(name)
            logger.debug('Packing ' + str(values[name]) + ' for ' + name + ' field as ' + fmt)

        bs = bitstring.pack(','.join(fmts), **values)

        return bs.tobytes()
