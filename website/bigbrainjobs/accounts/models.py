from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass

# TODO: Upload Resume, Add Favorites, Allow Applying to job, interface to see all favorites and applications