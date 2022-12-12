from unittest import TestCase

from django.contrib.gis.geos import Point
from jobs.utils import get_location_point
from unittest.mock import patch


class CompanyTestCase(TestCase):
    @patch(
        "googlemaps.Client.geocode",
        lambda x, y: [{"geometry": {"location": {"lat": 0, "lng": 0}}}],
    )
    def test_get_location_point_is_point(self):
        self.assertIsInstance(
            get_location_point("1600 Amphitheatre Parkway, Mountain View, CA"), Point
        )

    @patch("googlemaps.Client.geocode", lambda x, y: [])
    def test_get_location_point_bad_address(self):
        self.assertRaises(
            IndexError, get_location_point, "uhgeowuyegbowbegouybweugbwuebguweuyfbkyu"
        )
