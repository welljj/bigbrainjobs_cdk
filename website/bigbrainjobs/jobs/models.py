from django.contrib.gis.db import models
from django.conf import settings
from .utils import get_location_point


class Company(models.Model):
    class USStates(models.TextChoices):
        ALABAMA = "AL"
        ALASKA = "AK"
        ARIZONA = "AZ"
        ARKANSAS = "AR"
        CALIFORNIA = "CA"
        COLORADO = "CO"
        CONNECTICUT = "CT"
        DELAWARE = "DE"
        DISTRICT_OF_COLUMBIA = "DC"
        FLORIDA = "FL"
        GEORGIA = "GA"
        HAWAII = "HI"
        IDAHO = "ID"
        ILLINOIS = "IL"
        INDIANA = "IN"
        IOWA = "IA"
        KANSAS = "KS"
        KENTUCKY = "KY"
        LOUISIANA = "LA"
        MAINE = "ME"
        MARYLAND = "MD"
        MASSACHUSETTS = "MA"
        MICHIGAN = "MI"
        MINNESOTA = "MN"
        MISSISSIPPI = "MS"
        MISSOURI = "MO"
        MONTANA = "MT"
        NEBRASKA = "NE"
        NEVADA = "NV"
        NEW_HAMPSHIRE = "NH"
        NEW_JERSEY = "NJ"
        NEW_MEXICO = "NM"
        NEW_YORK = "NY"
        NORTH_CAROLINA = "NC"
        NORTH_DAKOTA = "ND"
        OHIO = "OH"
        OKLAHOMA = "OK"
        OREGON = "OR"
        PENNSYLVANIA = "PA"
        RHODE_ISLAND = "RI"
        SOUTH_CAROLINA = "SC"
        SOUTH_DAKOTA = "SD"
        TENNESSEE = "TN"
        TEXAS = "TX"
        UTAH = "UT"
        VERMONT = "VT"
        VIRGINIA = "VA"
        WASHINGTON = "WA"
        WEST_VIRGINIA = "WV"
        WISCONSIN = "WI"
        WYOMING = "WY"

    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="manager_of"
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=USStates.choices)
    zip_code = models.CharField(max_length=10)
    location = models.PointField()
    about = models.TextField()

    def save(self, *args, **kwargs):
        if not self.location:
            full_address = f"{self.address}, {self.city}, {self.state} {self.zip_code}"
            self.location = get_location_point(full_address)
        super().save(*args, **kwargs)


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    full_time = models.BooleanField()
    hourly = models.PositiveSmallIntegerField()
    salary = models.PositiveIntegerField()
    applicants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
