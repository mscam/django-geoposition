import decimal

from django.test import TestCase

from test_app.models import FloatLocation, DecimalLocation, MultipleLocation


TEST_LOCATIONS = (
    (43.7666700, 11.2500000),
    (40.714623, 74.006605),
)


class GeopositionFieldTest(TestCase):
    def test_float_location(self):
        l = FloatLocation(name='test float field')
        location = TEST_LOCATIONS[0]
        l.position = location
        l.save()
        self.assertEqual(decimal.Decimal(location[0]), l.latitude)
        self.assertEqual(decimal.Decimal(location[1]), l.longitude)
        self.assertEqual(location, l.position)
        location = TEST_LOCATIONS[1]
        l.position = [float(location[0]), decimal.Decimal(unicode(location[1]))]
        l.save()
        self.assertEqual(location, l.position)

    def test_decimal_location(self):
        l = DecimalLocation(name='test decimal field')
        location = TEST_LOCATIONS[0]
        l.position = location
        l.save()
        self.assertEqual(decimal.Decimal(location[0]), l.latitude)
        self.assertEqual(decimal.Decimal(location[1]), l.longitude)
        self.assertEqual(location, l.position)
        location = TEST_LOCATIONS[1]
        l.position = [float(location[0]), decimal.Decimal(unicode(location[1]))]
        l.save()
        self.assertEqual(location, l.position)

    def test_multiple_location(self):
        l = MultipleLocation(name='test multiple field types')
        location1, location2 = TEST_LOCATIONS
        l.position1 = location1
        l.position2 = location2
        l.save()
        self.assertEqual(location1[0], l.position1_latitude)
        self.assertEqual(location1[1], l.position1_longitude)
        self.assertEqual(location1, l.position1)
        self.assertEqual(location2[0], l.position2_latitude)
        self.assertEqual(location2[1], l.position2_longitude)
        self.assertEqual(location2, l.position2)
