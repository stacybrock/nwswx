# nwswx

A Python 3 client for retrieving data from the [NWS Weather Forecast API](https://forecast-v3.weather.gov/documentation).

## Installation

```
pip install nwswx
```

## Requirements

* Python 3.4+
* [Requests](http://docs.python-requests.org)

### Package Build Requirements

The full list of packages required to build this module can be found in `requirements.txt`

## Documentation

Full documentation, including examples and an API reference: http://nwswx.readthedocs.io

## Examples

Get forecast for a point in GeoJSON format:
```
>>> import nwswx
>>> nws = nwswx.WxAPI('your@email.com')
>>> forecast = nws.point_forecast(39.0693, -94.6716)
>>> print(forecast)
{
    "@context": [
        "https://raw.githubusercontent.com/geojson/geojson-ld/master/contexts/geojson-base.jsonld",
        {
            "wx": "https://api.weather.gov/ontology#",
            "geo": "http://www.opengis.net/ont/geosparql#",
            "unit": "http://codes.wmo.int/common/unit/",
            "@vocab": "https://api.weather.gov/ontology#"
        }
    ], ...
```

Get forecast for a point in JSON-LD format:
```
>>> import nwswx
>>> nws = nwswx.WxAPI('your@email.com')
>>> forecast = nws.point_forecast(39.0693, -94.6716, return_format=nwswx.formats.JSONLD)
>>> print(forecast['periods'])
[{'number': 1, 'name': 'Tonight', 'startTime': '2019-01-13T22:00:00-08:00', 'endTime':
'2019-01-14T06:00:00-08:00', 'isDaytime': False, 'temperature': 28, 'temperatureUnit':
'F', 'temperatureTrend': None, 'windSpeed': '2 to 6 mph', 'windDirection': 'N',
'icon': 'https://api.weather.gov/icons/land/night/few?size=medium', 'shortForecast':
'Mostly Clear', 'detailedForecast': 'Mostly clear, with a low around 28. North wind 2
to 6 mph.'}, ...
```

Get an hourly forecast for a point in JSON-LD format:
```
>>> import nwswx
>>> nws = nwswx.WxAPI('your@email.com')
>>> forecast = nws.point_hourly_forecast(39.0693, -94.6716, return_format=nwswx.formats.JSONLD)
>>> print(forecast['periods'])
[{'number': 1, 'name': '', 'startTime': '2019-01-16T19:00:00-08:00', 'endTime':
'2019-01-16T20:00:00-08:00', 'isDaytime': False, 'temperature': 42,
'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '10 mph', 'windDirection':
'NE', 'icon': 'https://api.weather.gov/icons/land/night/rain,90?size=small',
'shortForecast': 'Light Rain', 'detailedForecast': ''}, ...
```

Get active weather alerts for a point in ATOM format:
```
>>> import nwswx
>>> nws = nwswx.WxAPI('your@email.com')
>>> alerts = nws.active_alerts({'point': '39.0693,-94.6716'}, return_format=nwswx.formats.ATOM)
>>> print(alerts)
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:cap="urn:oasis:names:tc:emergency:cap:1.2">
 <id>https://api.weather.gov/alerts?point=39.0693%2C-94.6716&amp;active=1&amp;zone=KSZ104%2CKSC209</id>
 <generator>NWS CAP Server</generator>
 <updated>2019-01-17T06:04:28+00:00</updated>
 <author>
  <name>w-nws.webmaster@noaa.gov</name>
 </author>
 <title>current watches, warnings, and advisories for 39.0693 N, 94.6716 W</title>
 <link rel="self" href="https://api.weather.gov/alerts?point=39.0693%2C-94.6716&amp;active=1&amp;zone=KSZ104%2CKSC209"/>
 <entry>
  <id>https://api.weather.gov/alerts/NWS-IDP-PROD-3320294-2901037</id>
  <link rel="alternate" href="https://api.weather.gov/alerts/NWS-IDP-PROD-3320294-2901037"/>
  <updated>2019-01-16T14:52:00-06:00</updated>
  <published>2019-01-16T14:52:00-06:00</published>
  <author>
   <name>NWS</name>
  </author>
  <title>Winter Weather Advisory issued January 16 at 2:52PM CST expiring January 17 at 9:00AM CST by NWS Kansas City/Pleasant HIll MO</title>
...
```

## Limitations, of Which There Are Many

The following list of endpoints have not been implemented:

* `/stations`
* `/stations/{stationId}`
* `/stations/{stationId}/observations`
* `/stations/{stationId}/observations/current`
* `/stations/{stationId}/observations/{recordId}`
* `/products/{productId}`
* `/products/types`
* `/products/types/{typeId}`
* `/products/types/{typeId}/locations`
* `/products/types/{typeId}/locations/{locationId}`
* `/products/locations`
* `/products/locations/{locationId}/types`
* `/offices/{officeId}`
* `/zones/{type}/{zoneId}`
* `/zones/{type}/{zoneId}/forecast`
* `/alerts/active/count`
* `/alerts/active/zone/{zoneId}`
* `/alerts/active/area/{area}`
* `/alerts/active/region/{region}`
