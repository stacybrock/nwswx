API Reference
=============

All forecast functions are accessed via an instance of the
:class:`WxAPI` class::

  import nws_wx_client
  nws = nws_wx_client.WxAPI('test@email.com')

Most functions accept a ``return_format`` parameter, which is expected to be a Content-Type string or an attribute on the friendlier, easier-to-read helper object ``nws_wx_client.formats``.

======= ================================= =============
Format  Content-Type                      Format Helper
======= ================================= =============
GeoJSON ``application/geo+json``          ``nws_wx_client.formats.GeoJSON``
JSON-LD ``application/ld+json``           ``nws_wx_client.formats.JSONLD``
DWML    ``application/vnd.noaa.dwml+xml`` ``nws_wx_client.formats.DWML``
OXML    ``application/vnd.noaa.obs+xml``  ``nws_wx_client.formats.OXML``
CAP     ``application/cap+xml``           ``nws_wx_client.formats.CAP``
ATOM    ``application/atom+xml``          ``nws_wx_client.formats.ATOM``
======= ================================= =============

The examples in this documentation will use the ``nws_wx_client.formats`` helper.

===========
WxAPI Class
===========

.. currentmodule:: nws_wx_client

.. autoclass:: nws_wx_client.WxAPI
   :members:
