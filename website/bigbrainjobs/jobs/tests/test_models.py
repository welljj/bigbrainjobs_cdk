from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import TestCase
from jobs.models import Company


@patch("jobs.models.get_location_point", lambda x: Point(0, 0))
class CompanyTestCase(TestCase):
    @classmethod
    @patch("jobs.models.get_location_point", lambda x: Point(0, 0))
    def setUpTestData(cls):
        cls.user_a = get_user_model().objects.create_user(
            username="user_a", email="user_a@test.com", password="password"
        )
        Company.objects.create(
            manager=cls.user_a,
            name="Company A",
            address="217 E 70th St",
            city="New York",
            state="NY",
            zip_code="10021",
            about="TEST ABOUT",
        )
        cls.user_b = get_user_model().objects.create_user(
            username="user_b", email="user_b@test.com", password="password"
        )
        Company.objects.create(
            manager=cls.user_b,
            name="Company B",
            address="7101 S Central Ave",
            city="Los Angeles",
            state="CA",
            zip_code="90001",
            about="TEST ABOUT 2",
        )
        cls.user_c = get_user_model().objects.create_user(
            username="user_c", email="user_c@test.com", password="password"
        )

    def test_company_primary_key(self):
        company_a = Company.objects.get(name="Company A")
        company_b = Company.objects.get(name="Company B")
        self.assertEqual(company_a.pk, 1)
        self.assertEqual(company_b.pk, 2)

    def test_company_has_location(self):
        company_a = Company.objects.get(name="Company A")
        company_b = Company.objects.get(name="Company B")
        self.assertTrue(company_a.location)
        self.assertTrue(company_b.location)
        self.assertTrue(company_a.location.equals(Point(0, 0)))
        self.assertTrue(company_b.location.equals(Point(0, 0)))

    def test_company_change_manager_to_taken_manager(self):
        company_a = Company.objects.get(name="Company A")
        company_a.manager = self.user_b
        self.assertRaises(IntegrityError, company_a.save)

    def test_company_change_manager(self):
        self.assertRaises(ObjectDoesNotExist, lambda: self.user_c.company)
        company_a = Company.objects.get(name="Company A")
        company_a.manager = self.user_c
        company_a.save()
        self.user_c.save()
        self.user_a.save()
        company_a = Company.objects.get(name="Company A")
        self.assertEqual(company_a.manager, self.user_c)
        self.assertEqual(company_a, self.user_c.company)
        self.assertNotEqual(company_a, self.user_a.company)
        self.assertRaises(ObjectDoesNotExist, lambda: self.user_a.company)
