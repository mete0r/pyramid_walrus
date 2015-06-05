# -*- coding: utf-8 -*-
#
#   pyramid_walrus : a walrus integration for pyramid
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import logging


__version__ = '0.1.2'


logger = logging.getLogger(__name__)


def includeme(config):
    from .backends import get_backend_factory

    settings = config.registry.settings

    factory = get_backend_factory(settings)
    factory = wrap_factory(factory)
    config.add_request_method(factory, 'walrus_db', reify=True)


def wrap_factory(factory):
    def get_database_for_request(request):
        db = factory(request)
        assert db is not None
        return db
    return get_database_for_request
