API Reference
=============

All forecast functions are accessed via an instance of the
:class:`WxAPI` class::

  import nwswx
  nws = nwswx.WxAPI('test@email.com')

Most functions accept a ``return_format`` parameter, which is expected to be a Content-Type string or an attribute on the friendlier, easier-to-read helper object ``nwswx.formats``.

======= ================================= =============
Format  Content-Type                      Format Helper
======= ================================= =============
GeoJSON ``application/geo+json``          ``nwswx.formats.GeoJSON``
JSON-LD ``application/ld+json``           ``nwswx.formats.JSONLD``
DWML    ``application/vnd.noaa.dwml+xml`` ``nwswx.formats.DWML``
OXML    ``application/vnd.noaa.obs+xml``  ``nwswx.formats.OXML``
CAP     ``application/cap+xml``           ``nwswx.formats.CAP``
ATOM    ``application/atom+xml``          ``nwswx.formats.ATOM``
======= ================================= =============

The examples in this documentation will use the ``nwswx.formats`` helper.

===========
WxAPI Class
===========

.. currentmodule:: nwswx

.. autoclass:: nwswx.WxAPI
   :members:
