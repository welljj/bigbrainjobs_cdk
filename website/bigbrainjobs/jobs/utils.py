import googlemaps
from django.conf import settings
from django.contrib.gis.geos import Point

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


def get_location_point(address: str) -> Point:
    geocode_result = gmaps.geocode(address)

    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]

    return Point(longitude, latitude)
