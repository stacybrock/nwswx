"""Utility functions"""

def check_format_match(input_, target):
    """Returns True if input matches target format"""
    if input_ is not None and input_.lower() == target.lower():
        return True
    else:
        return False

def is_jsonld(format_):
    """Returns True if format is JSON-LD"""
    return check_format_match(format_, 'JSON-LD')

def is_geojson(format_):
    """Returns True if format is GeoJSON"""
    return check_format_match(format_, 'GeoJSON')
