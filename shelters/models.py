from django.db import models
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="shelters")


class Address(models.Model):
    street = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)

    longitude = models.FloatField()
    latitude = models.FloatField()

    def _get_coords_by_city(self):
        location = geolocator.geocode(self.city)
        return location.longitude, location.latitude

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.longitude and not self.latitude:
            self.longitude, self.latitude = self._get_coords_by_city()

        return super().save(force_insert, force_update, using, update_fields)
