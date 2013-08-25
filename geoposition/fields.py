import decimal

from django.db import models

from .forms import GeopositionField as GeopositionFormField
from django.utils.encoding import smart_unicode


class GeopositionField(models.Field):
    rel = None
    description = "A geoposition (latitude and longitude)"

    _allowed_fields = {
        models.FloatField: {'blank': True, 'null': True},
        models.DecimalField: {'blank': True, 'null': True,
                              'max_digits': 11, 'decimal_places': 6},
    }
    _allowed_types = (float, decimal.Decimal)

    def __init__(self, *args, **kwargs):
        self.lat_field_name = kwargs.pop('latitude_field', 'latitude')
        self.lon_field_name = kwargs.pop('longitude_field', 'longitude')

        self.fields_class = kwargs.pop('fields_class', models.FloatField)
        if self.fields_class not in self._allowed_fields:
            raise ValueError('"%s" is not a valid option for "fields_class"' % (
                             self.fields_class,))

        self.fields_type = kwargs.pop('fields_type', float)
        if self.fields_type not in self._allowed_types:
            raise ValueError('"%s" is not a valid option for "fields_type"' % (
                             self.fields_type,))

        self.fields_opts = self._allowed_fields[self.fields_class]
        self.fields_opts.update(kwargs.pop('fields_opts', {}))

        super(GeopositionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def contribute_to_class(self, cls, name):
        lat_field = self.fields_class(**self.fields_opts)
        lon_field = self.fields_class(**self.fields_opts)

        cls.add_to_class(self.lat_field_name, lat_field)
        cls.add_to_class(self.lon_field_name, lon_field)

        cls._meta.add_virtual_field(self)
        setattr(cls, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        if self.fields_class in (models.DecimalField, models.FloatField):
            lat = getattr(instance, self.lat_field_name)
            lon = getattr(instance, self.lon_field_name)
            return self.fields_type(lat), self.fields_type(lon)
        else:
            raise NotImplementedError('Work in progress.')

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError('"%s" must be accessed via instance.' % (
                                 self.related.opts.object_name,))
        lat, lon = None, None
        if self.fields_class in (models.DecimalField, models.FloatField):
            try:
                lat, lon = value
            except (ValueError, TypeError):
                raise ValueError('"%s" must be a list or tuple like: (lat, lon).' % (
                                 repr(value)))
            if lat and lon:
                setattr(instance, self.lat_field_name, lat)
                setattr(instance, self.lon_field_name, lon)

        else:
             raise NotImplementedError('Work in progress.')

    def formfield(self, **kwargs):
        defaults = {
            'form_class': GeopositionFormField
        }
        defaults.update(kwargs)
        return super(GeopositionField, self).formfield(**defaults)
