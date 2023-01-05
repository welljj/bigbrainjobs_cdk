import factory
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from jobs.models import Company, Job


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda x: f"john{x}")


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    manager = factory.SubFactory(UserFactory)
    name = factory.Faker("company")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip_code = factory.Faker("zipcode_plus4")
    about = factory.Faker("paragraph")
    location = Point(0, 0)


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Faker("job")
    description = factory.Faker("paragraph")
    company = factory.SubFactory(CompanyFactory)
    full_time = factory.Faker("boolean")
    hourly = factory.Faker("random_int", min=5, max=30)
    salary = factory.Faker("random_int", min=20000, max=100000)
    # applicants = factory.SubFactory(UserFactory)


jobs = JobFactory.create_batch(100)
