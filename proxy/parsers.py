# AmigoProxy
#
# Copyright (c) 2011-2015 AmigoCloud Inc., All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library.

from bs4 import BeautifulSoup


class BaseParser(object):
    """ All parsers must be base classes of BaseParsers. """

    def get_id(self, request_body):
        return None


class MoovboxParser(BaseParser):
    """ Parse Moovbox XML requests. """

    def get_id(self, request_body):
        gps = BeautifulSoup(request_body).find('gps')
        return gps.attrs.get('id') if gps else None


all_parsers = [MoovboxParser]
