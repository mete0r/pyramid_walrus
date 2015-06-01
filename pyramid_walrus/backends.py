# -*- coding: utf-8 -*-
#
#   pyramid_walrus : a walrus integration for pyramid
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import unicode_literals
import logging

from pyramid.path import DottedNameResolver

logger = logging.getLogger(__name__)


def get_backend_factory(settings):
    backend = settings.get('pyramid_walrus.backend', 'redis')
    if backend == 'redis':
        return RedisFactory(settings)
    elif backend == 'ledis':
        return LedisFactory(settings)
    elif backend == 'rlite':
        return RLiteFactory(settings)
    elif backend == 'vedis':
        return VedisFactory(settings)

    # custom factory
    resolver = DottedNameResolver()
    custom_factory = resolver.resolve(backend)
    return custom_factory(settings)


def RedisFactory(settings):
    from redis import BlockingConnectionPool
    from walrus import Walrus

    default = get_settings('pyramid_walrus.backend.redis.', settings, {
        'url': 'redis://@localhost:6379/0',
        'max_connections': '10',
    })

    connection_url = default['url']
    max_connection = default['max_connections']
    max_connection = int(max_connection) if max_connection else None
    connection_pool = BlockingConnectionPool.from_url(
        url=connection_url,
        max_connections=max_connection)
    logger.debug('connection_pool: %r', connection_pool)

    def get_database_for_request(request):
        return Walrus(connection_pool=connection_pool)
    return get_database_for_request


def LedisFactory(settings):
    from ledis import BlockingConnectionPool
    from walrus.tusks.ledisdb import WalrusLedis

    default = get_settings('pyramid_walrus.backend.ledis.', settings, {
        'url': 'ledis://@localhost:6380/0',
        'max_connections': '10',
    })
    connection_url = default['url']
    max_connection = default['max_connections']
    max_connection = int(max_connection) if max_connection else None
    connection_pool = BlockingConnectionPool.from_url(
        url=connection_url,
        max_connections=max_connection)
    logger.debug('connection_pool: %r', connection_pool)

    def get_database_for_request(request):
        return WalrusLedis(connection_pool=connection_pool)
    return get_database_for_request


def RLiteFactory(settings):
    from walrus.tusks.rlite import WalrusLite

    default = get_settings('pyramid_walrus.backend.rlite.', settings, {
        'filename': ':memory:',
        'encoding': 'utf-8',
    })
    db = WalrusLite(**default)

    def get_database_for_request(request):
        return db
    return get_database_for_request


def VedisFactory(settings):
    from walrus.tusks.vedisdb import WalrusVedis

    default = get_settings('pyramid_walrus.backend.vedis.', settings, {
        'filename': ':memory:',
    })
    db = WalrusVedis(**default)

    def get_database_for_request(request):
        return db
    return get_database_for_request


def get_settings(prefix, settings, default):
    for k in default:
        if prefix + k in settings:
            default[k] = settings[prefix + k]

    return default
