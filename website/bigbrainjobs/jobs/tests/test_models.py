from django.contrib.auth import get_user_model
from django.test import TestCase
from jobs.models import Company


class CompanyTestCase(TestCase):
    @classmethod
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

    def test_company_has_location(self):
        company_a = Company.objects.get(name="Company A")
        company_b = Company.objects.get(name="Company B")
        self.assertTrue(company_a.location)
        self.assertFalse(company_b.location)
