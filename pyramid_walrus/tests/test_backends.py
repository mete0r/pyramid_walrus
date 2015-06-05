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
from __future__ import unicode_literals
from unittest import TestCase
import os.path

from ..backends import get_backend_factory
from ..backends import RedisFactory
from ..backends import RLiteFactory
from ..backends import VedisFactory
from ..backends import LedisFactory


class get_backend_factory_Test(TestCase):

    def get_db(self, settings):
        factory = get_backend_factory(settings)
        request = None
        return factory(request)

    def test_default(self):
        from walrus import Database
        settings = {}
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, Database))

    def test_redis(self):
        from walrus import Database
        settings = {
            'pyramid_walrus.backend': 'redis'
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, Database))
        self.assertEquals(10, db.connection_pool.max_connections)

    def test_rlite(self):
        from walrus.tusks.rlite import WalrusLite
        settings = {
            'pyramid_walrus.backend': 'rlite'
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusLite))

    # XXX: disabled
    def xxx_test_vedis(self):
        from walrus.tusks.vedisdb import WalrusVedis
        settings = {
            'pyramid_walrus.backend': 'vedis'
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusVedis))

    # XXX: disabled for broken walrus-0.3.1 + ledis-0.0.1 in PyPI
    def xxx_test_ledis(self):
        from walrus.tusks.ledisdb import WalrusLedis
        settings = {
            'pyramid_walrus.backend': 'ledis'
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusLedis))
        self.assertEquals(10, db.connection_pool.max_connections)

    def test_custom(self):
        settings = {
            'pyramid_walrus.backend':
            'pyramid_walrus.tests.test_backends.get_custom_backend_factory'
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, CustomDatabase))


def get_custom_backend_factory(settings):
    def get_database_for_request(request):
        return CustomDatabase()
    return get_database_for_request


class CustomDatabase(object):
    pass


class RedisFactoryTest(TestCase):

    def get_db(self, settings):
        get_database_for_request = RedisFactory(settings)
        db = get_database_for_request(None)
        return db

    def test_db1(self):
        from redis.connection import Connection
        from redis.connection import BlockingConnectionPool
        from walrus import Database
        settings = {
            'pyramid_walrus.backend.redis.url': 'redis://@127.0.0.1:6379/1',
            'pyramid_walrus.backend.redis.max_connections': '5',
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, Database))

        connection_pool = db.connection_pool
        self.assertTrue(isinstance(connection_pool, BlockingConnectionPool))
        self.assertEquals(5, connection_pool.max_connections)

        kwargs = connection_pool.connection_kwargs
        self.assertEquals('127.0.0.1', kwargs['host'])
        self.assertEquals(6379, kwargs['port'])
        self.assertEquals(1, kwargs['db'])
        self.assertEquals(None, kwargs['password'])
        self.assertEquals(Connection, connection_pool.connection_class)

    def test_unixsocket(self):
        from redis.connection import UnixDomainSocketConnection
        from redis.connection import BlockingConnectionPool
        from walrus import Database
        settings = {
            'pyramid_walrus.backend.redis.url': 'unix://@/redis.sock?db=1'
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, Database))

        connection_pool = db.connection_pool
        self.assertTrue(isinstance(connection_pool, BlockingConnectionPool))

        kwargs = connection_pool.connection_kwargs
        self.assertEquals(1, kwargs['db'])
        self.assertEquals(None, kwargs['password'])
        self.assertEquals(UnixDomainSocketConnection,
                          connection_pool.connection_class)


class RLiteFactoryTest(TestCase):

    def setUp(self):
        self.diskfilename = self.id()
        if os.path.exists(self.diskfilename):
            os.unlink(self.diskfilename)

    def get_db(self, settings):
        get_database_for_request = RLiteFactory(settings)
        db = get_database_for_request(None)
        return db

    def test_memory(self):
        from walrus.tusks.rlite import WalrusLite
        settings = {
            'pyramid_walrus.backend.rlite.filename': ':memory:',
            'pyramid_walrus.backend.rlite.encoding': 'utf-8',
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusLite))
        self.assertEquals(':memory:', db._filename)
        self.assertEquals('utf-8', db._encoding)

    def test_diskfile(self):
        from walrus.tusks.rlite import WalrusLite
        settings = {
            'pyramid_walrus.backend.rlite.filename': self.diskfilename,
            'pyramid_walrus.backend.rlite.encoding': 'utf-8',
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusLite))
        self.assertEquals(self.diskfilename, db._filename)
        self.assertEquals('utf-8', db._encoding)


# XXX VedisFactoryTest(TestCase): disabled
class VedisFactoryTest(object):

    def setUp(self):
        self.diskfilename = self.id()
        if os.path.exists(self.diskfilename):
            os.unlink(self.diskfilename)

    def get_db(self, settings):
        get_database_for_request = VedisFactory(settings)
        db = get_database_for_request(None)
        return db

    def test_memory(self):
        from walrus.tusks.vedisdb import WalrusVedis
        settings = {
            'pyramid_walrus.backend.vedis.filename': ':memory:',
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusVedis))
        self.assertEquals(':memory:', db._filename)

    def test_diskfile(self):
        from walrus.tusks.vedisdb import WalrusVedis
        settings = {
            'pyramid_walrus.backend.vedis.filename': self.diskfilename,
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusVedis))
        self.assertEquals(self.diskfilename, db._filename)


# XXX LedisFactoryTest(TestCase): broken walrus-0.3.1 + ledis-0.0.1 in PyPI
class LedisFactoryTest(object):

    def get_db(self, settings):
        get_database_for_request = LedisFactory(settings)
        db = get_database_for_request(None)
        return db

    def test_db1(self):
        from ledis.connection import Connection
        from ledis.connection import BlockingConnectionPool
        from walrus.tusks.ledisdb import WalrusLedis
        settings = {
            'pyramid_walrus.backend.ledis.url': 'ledis://@127.0.0.1:6380/1',
            'pyramid_walrus.backend.ledis.max_connections': '5',
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusLedis))

        connection_pool = db.connection_pool
        self.assertTrue(isinstance(connection_pool, BlockingConnectionPool))
        self.assertEquals(5, connection_pool.max_connections)

        kwargs = connection_pool.connection_kwargs
        self.assertEquals('127.0.0.1', kwargs['host'])
        self.assertEquals(6380, kwargs['port'])
        self.assertEquals(1, kwargs['db'])
        self.assertEquals(None, kwargs['password'])
        self.assertEquals(Connection, connection_pool.connection_class)

    def test_unixsocket(self):
        from ledis.connection import UnixDomainSocketConnection
        from ledis.connection import BlockingConnectionPool
        from walrus.tusks.ledisdb import WalrusLedis
        settings = {
            'pyramid_walrus.backend.ledis.url': 'unix://@/redis.sock?db=1',
        }
        db = self.get_db(settings)
        self.assertTrue(isinstance(db, WalrusLedis))

        connection_pool = db.connection_pool
        self.assertTrue(isinstance(connection_pool, BlockingConnectionPool))

        kwargs = connection_pool.connection_kwargs
        self.assertEquals(1, kwargs['db'])
        self.assertEquals(None, kwargs['password'])
        self.assertEquals(UnixDomainSocketConnection,
                          connection_pool.connection_class)
