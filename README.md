# nws-wx-client

A simple Python 3 client for retrieving data from the [NWS Weather Forecast API](https://forecast-v3.weather.gov/documentation).

## Requirements

* Python 3.6+
* `requirements.txt`

## Examples

Get forecast for a point in GeoJSON format:
```
>>> import nws_wx_client
>>> nws = nws_wx_client.WxAPI('your@email.com')
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
>>> import nws_wx_client
>>> nws = nws_wx_client.WxAPI('your@email.com')
>>> forecast = nws.point_forecast(39.0693, -94.6716, return_format='JSON-LD')
>>> print(forecast)
[{'number': 1, 'name': 'Tonight', 'startTime': '2019-01-13T22:00:00-08:00', 'endTime': '2019-01-14T06:00:00-08:00', 'isDaytime': False, 'temperature': 28, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '2 to 6 mph', 'windDirection': 'N', 'icon': 'https://api.weather.gov/icons/land/night/few?size=medium', 'shortForecast': 'Mostly Clear', 'detailedForecast': 'Mostly clear, with a low around 28. North wind 2 to 6 mph.'}, ...
```

## Limitations, of Which There Are Many

* Most endpoints remain unimplemented and are on the TODO list.
