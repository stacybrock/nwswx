"""Endpoint formats"""

_formats = {
    'GeoJSON': 'application/geo+json',
    'JSONLD': 'application/ld+json',
    'DWML': 'application/vnd.noaa.dwml+xml',
    'OXML': 'application/vnd.noaa.obs+xml',
    'CAP': 'application/cap+xml',
    'ATOM': 'application/atom+xml'
}

class Formats(dict):
    def __init__(self):
        super(Formats, self).__init__()

    def __repr__(self):
        return '<Formats: ' + str(self.__dict__) + '>'

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

formats = Formats()

def _init():
    for title, ctype in _formats.items():
        setattr(formats, title, ctype)
        setattr(formats, title.lower(), ctype)

_init()
