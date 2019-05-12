from geotext import GeoText

def process_locations(title, description, location):
    cities = GeoText(title + ' ' + description + ' ' + location).cities
    if len(cities) == 0:
        cities.append('N/A')
    return keep_unique(cities)

def keep_unique(items):
    return list(set(items))