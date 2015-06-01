##############
pyramid_walrus
##############

a `walrus`_ integration for pyramid


To install::

        $ pip install pyramid_walrus

In your configuration::

        [app:main]

        ...

        pyramid.includes =
            pyramid_walrus


In your views::

        def my_view(request):
            db = request.walrus_db
            db.incr('my_counter')


Backend-specific configurations
===============================


`walrus`_ can be configured to use several `redis`_-like backends.


`Redis`_ (default)
------------------

::

        $ pip install redis

::

        pyramid_walrus.backend = redis
        pyramid_walrus.backend.redis.url = redis://@localhost:6379/0
        pyramid_walrus.backend.redis.max_connections = 10


`Rlite`_
--------

::

        $ pip install hirlite

::

        pyramid_walrus.backend = rlite
        pyramid_walrus.backend.rlite.filename = :memory:
        pyramid_walrus.backend.rlite.encoding = utf-8

`Vedis`_
--------

::

        $ pip install vedis

::

        pyramid_walrus.backend = vedis
        pyramid_walrus.backend.vedis.filename = :memory:

`LedisDB`_
----------

::

        $ pip install ledis

::

        pyramid_walrus.backend = ledis
        pyramid_walrus.backend.ledis.url = ledis://@localhost:6380/0
        pyramid_walrus.backend.ledis.max_connections = 10


Custom
------

::

        pyramid_walrus.backend = myapp.get_walrus_backend_from_settings


and define your custom factory function::

        # myapp.py

        def get_walrus_backend_from_settings(settings):
            def get_database_for_request(request):
                ...
                return db
            return get_database_for_request

.. _walrus: https://pypi.python.org/pypi/walrus
.. _redis: http://redis.io
.. _rlite: https://github.com/seppo0010/rlite
.. _Vedis: http://vedis.symisc.net/
.. _LedisDB: http://ledisdb.com/

