# peid.py - library for Liechtenstein Personenidentifikationsnummer
#
# Copyright (C) 2020 Matthias Schmid
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""PEID (Liechtenstein tax code for individuals and entities).

The Personenidentifikationsnummer (PEID) is an numeric code up to 12
digits used to identify entities and individuals residing in
Liechtenstein.

The first digits might be omitted if they correspond to the numeral
zero. Nevertheless the minimum number of digits is four.


More information:

* http://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/
* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/LIECHTENSTEIN%20TIN.pdf

>>> compact('00001234567')
'1234567'

>>> validate('1234567')  # personal number or entity number
'1234567'
>>> validate('00001234567')
'1234567'

>>> validate('00001234568913454545')
Traceback (most recent call last):
    ...
InvalidLength: The number has an invalid length.

>>> validate('568ABC91345')
Traceback (most recent call last):
    ...
InvalidFormat: The number has an invalid format.
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


# regular expression for matching Liechtenstein Personenidentifikationsnummer
_code_re = re.compile(r'^[0-9]{4,12}$')


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number).strip().lstrip('0').replace('.', '', 2)


def validate(number):
    """Check if the given fiscal code is valid. This checks the length and
    whether the check digit is correct."""
    number = compact(number)
    if len(number) < 4 or len(number) > 12:
        raise InvalidLength()
    if not _code_re.match(number):
        raise InvalidFormat()

    return number


def is_valid(number):
    """Check if the given fiscal code is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
