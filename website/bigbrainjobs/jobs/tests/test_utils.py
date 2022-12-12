from unittest import TestCase

from jobs.utils import get_location_point


class CompanyTestCase(TestCase):
    def test_get_location_point_bad_address(self):
        self.assertRaises(
            IndexError, get_location_point, "uhgeowuyegbowbegouybweugbwuebguweuyfbkyu"
        )
