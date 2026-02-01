from django.test import TestCase
from .models import Guitar, Accessory, Brand, GuitarType

# Create your tests here.

class GuitarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Test Brand')
        cls.guitar_type = GuitarType.objects.create(guitar_type_name='Acoustic')
        cls.guitar = Guitar.objects.create(
            name='Test Guitar',
            description='A guitar for testing',
            price=1000,
            string_num=6,
            brand=cls.brand,
            guitar_type=cls.guitar_type,
            model='Model X',
            handedness='right',
            stock=10,
            image='guitars/test.jpg'
        )

    def test_guitar_creation(self):
        guitar = Guitar.objects.get(name='Test Guitar')
        self.assertEqual(guitar.description, 'A guitar for testing')
        self.assertEqual(guitar.price, 1000)
        self.assertEqual(guitar.string_num, 6)
        self.assertEqual(guitar.stock, 10)

    def test_guitar_detail_view(self):
        response = self.client.get(self.guitar.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Guitar')


class AccessoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Test Accessory Brand')
        cls.accessory = Accessory.objects.create(
            name='Test Accessory',
            description='An accessory for testing',
            price=50,
            stock=20,
            brand=cls.brand,
            image='accessories/test.jpg'
        )

    def test_accessory_creation(self):
        accessory = Accessory.objects.get(name='Test Accessory')
        self.assertEqual(accessory.description, 'An accessory for testing')
        self.assertEqual(accessory.price, 50)
        self.assertEqual(accessory.stock, 20)

    def test_accessory_detail_view(self):
        response = self.client.get(self.accessory.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Accessory')