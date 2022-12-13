from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase
from jobs.models import Company


@patch("jobs.models.get_location_point", lambda x: Point(0, 0))
class CompanyTestCase(TestCase):
    @patch("jobs.models.get_location_point", lambda x: Point(0, 0))
    def setUp(self):
        self.user_a = get_user_model().objects.create_user(
            username="user_a", email="user_a@test.com", password="password"
        )
        Company.objects.create(
            manager=self.user_a,
            name="Company A",
            address="217 E 70th St",
            city="New York",
            state="NY",
            zip_code="10021",
            about="TEST ABOUT",
        )
        self.user_b = get_user_model().objects.create_user(
            username="user_b", email="user_b@test.com", password="password"
        )
        Company.objects.create(
            manager=self.user_b,
            name="Company B",
            address="7101 S Central Ave",
            city="Los Angeles",
            state="CA",
            zip_code="90001",
            about="TEST ABOUT 2",
        )
        self.user_c = get_user_model().objects.create_user(
            username="user_c", email="user_c@test.com", password="password"
        )

    def test_company_has_location(self):
        """Company location is created."""
        company_a = Company.objects.get(name="Company A")
        company_b = Company.objects.get(name="Company B")
        self.assertTrue(company_a.location)
        self.assertTrue(company_b.location)
        self.assertTrue(company_a.location.equals(Point(0, 0)))
        self.assertTrue(company_b.location.equals(Point(0, 0)))

    def test_company_change_manager_to_taken_manager(self):
        """Each Company should have a unique manager."""
        company_a = Company.objects.get(name="Company A")
        company_a.manager = self.user_b
        self.assertRaises(IntegrityError, company_a.save)

    def test_company_change_manager(self):
        """Changing manager on Company should be reflected in users."""
        company_a = Company.objects.get(name="Company A")
        self.assertEqual(company_a.manager, self.user_a)
        self.assertEqual(company_a, self.user_a.manager_of)
        self.assertRaises(ObjectDoesNotExist, lambda: self.user_c.manager_of)
        company_a.manager = self.user_c
        company_a.save()
        company_a.refresh_from_db()
        self.user_c.refresh_from_db()
        self.user_a.refresh_from_db()
        self.assertEqual(company_a.manager, self.user_c)
        self.assertEqual(company_a, self.user_c.manager_of)
        self.assertRaises(ObjectDoesNotExist, lambda: self.user_a.manager_of)

    def test_delete_company(self):
        """Deleting a company removes Users manager_of"""
        company_a = Company.objects.get(name="Company A")
        self.assertEqual(company_a, self.user_a.manager_of)
        company_a.delete()
        self.assertRaises(
            ObjectDoesNotExist, lambda: Company.objects.get(name="Company A")
        )
        self.user_a.refresh_from_db()
        self.assertRaises(ObjectDoesNotExist, lambda: self.user_a.manager_of)

    def test_delete_company_manager_user(self):
        """Deleting a User that is a manager raises a ProtectedError"""
        company_a = Company.objects.get(name="Company A")
        self.assertRaises(ProtectedError, self.user_a.delete)
        company_a.manager = self.user_c
        company_a.save()
        self.assertEqual(self.user_a.delete(), (1, {"accounts.CustomUser": 1}))

    def test_delete_company_manager_field(self):
        """Removing the manager from a field is not allowed"""
        company_a = Company.objects.get(name="Company A")
        company_a.manager = None
        self.assertRaises(IntegrityError, company_a.save)
