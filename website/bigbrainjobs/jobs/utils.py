import googlemaps
from django.conf import settings
from django.contrib.gis.geos import Point


def get_location_point(address: str) -> Point:
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)

    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]

    return Point(longitude, latitude)
