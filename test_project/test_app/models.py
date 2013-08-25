from django.db import models

from geoposition.fields import GeopositionField


class Location(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        abstract = True


class FloatLocation(Location):
    position = GeopositionField(
        fields_class=models.FloatField
    )


class DecimalLocation(Location):
    position = GeopositionField(
        fields_class=models.DecimalField
    )


class MultipleLocation(Location):
    position1 = GeopositionField(
        latitude_field = 'position1_latitude',
        longitude_field = 'position1_longitude',
    )
    position2 = GeopositionField(
        latitude_field = 'position2_latitude',
        longitude_field = 'position2_longitude',
    )
