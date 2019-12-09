============
Tahm
============

Requirements
------------

* Python 3.5+
* Redis >= 2.8
* ``Scrapy`` >= 1.0
* ``redis-py`` >= 2.10

Usage
-----

Use the following settings in your project:

.. code-block:: python

 # Enables scheduling storing requests queue in redis.
  SCHEDULER = "scrapy_redis.scheduler.Scheduler"

.. note::


