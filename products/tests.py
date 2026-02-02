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


class GuitarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Test Brand')
        cls.guitar_type = GuitarType.objects.create(guitar_type_name='Acoustic')
        cls.guitar1 = Guitar.objects.create(
            name='Acoustic Guitar',
            description='A beautiful acoustic guitar',
            price=1000,
            string_num=6,
            brand=cls.brand,
            guitar_type=cls.guitar_type,
            model='Model A',
            handedness='right',
            stock=10,
            image='guitars/acoustic.jpg'
        )
        cls.guitar2 = Guitar.objects.create(
            name='Electric Guitar',
            description='A powerful electric guitar',
            price=1500,
            string_num=6,
            brand=cls.brand,
            guitar_type=cls.guitar_type,
            model='Model E',
            handedness='left',
            stock=5,
            image='guitars/electric.jpg'
        )

    def test_guitar_list_view_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_guitar_list_view_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'guitar_list.html')

    def test_guitar_list_view_context(self):
        response = self.client.get('/')
        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_guitar_list_search_by_name(self):
        response = self.client.get('/?q=Acoustic')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acoustic Guitar')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_guitar_list_search_by_description(self):
        response = self.client.get('/?q=powerful')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electric Guitar')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_guitar_list_search_no_results(self):
        response = self.client.get('/?q=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)


class GuitarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Test Brand')
        cls.guitar_type = GuitarType.objects.create(guitar_type_name='Acoustic')
        cls.guitar = Guitar.objects.create(
            name='Detail Test Guitar',
            description='A guitar for detail view testing',
            price=1200,
            string_num=6,
            brand=cls.brand,
            guitar_type=cls.guitar_type,
            model='Model D',
            handedness='right',
            stock=8,
            image='guitars/detail.jpg'
        )

    def test_guitar_detail_view_status_code(self):
        response = self.client.get(self.guitar.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_guitar_detail_view_template(self):
        response = self.client.get(self.guitar.get_absolute_url())
        self.assertTemplateUsed(response, 'guitar_detail.html')

    def test_guitar_detail_view_context(self):
        response = self.client.get(self.guitar.get_absolute_url())
        self.assertEqual(response.context['object'], self.guitar)

    def test_guitar_detail_view_content(self):
        response = self.client.get(self.guitar.get_absolute_url())
        self.assertContains(response, 'Detail Test Guitar')
        self.assertContains(response, 'A guitar for detail view testing')
        self.assertContains(response, '1200')


class AccessoriesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Accessory Brand')
        cls.accessory1 = Accessory.objects.create(
            name='Guitar Strap',
            description='A comfortable guitar strap',
            price=50,
            stock=20,
            brand=cls.brand,
            image='accessories/strap.jpg'
        )
        cls.accessory2 = Accessory.objects.create(
            name='Guitar Pick',
            description='Durable guitar picks pack',
            price=10,
            stock=100,
            brand=cls.brand,
            image='accessories/pick.jpg'
        )

    def test_accessories_list_view_status_code(self):
        response = self.client.get('/accessories/')
        self.assertEqual(response.status_code, 200)

    def test_accessories_list_view_template(self):
        response = self.client.get('/accessories/')
        self.assertTemplateUsed(response, 'accessory_list.html')

    def test_accessories_list_view_context(self):
        response = self.client.get('/accessories/')
        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_accessories_list_search_by_name(self):
        response = self.client.get('/accessories/?q=Strap')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Guitar Strap')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_accessories_list_search_by_description(self):
        response = self.client.get('/accessories/?q=Durable')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Guitar Pick')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_accessories_list_search_no_results(self):
        response = self.client.get('/accessories/?q=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)


class AccessoryDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Accessory Brand')
        cls.accessory = Accessory.objects.create(
            name='Detail Test Accessory',
            description='An accessory for detail view testing',
            price=75,
            stock=15,
            brand=cls.brand,
            image='accessories/detail.jpg'
        )

    def test_accessory_detail_view_status_code(self):
        response = self.client.get(self.accessory.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_accessory_detail_view_template(self):
        response = self.client.get(self.accessory.get_absolute_url())
        self.assertTemplateUsed(response, 'accessory_detail.html')

    def test_accessory_detail_view_context(self):
        response = self.client.get(self.accessory.get_absolute_url())
        self.assertEqual(response.context['object'], self.accessory)

    def test_accessory_detail_view_content(self):
        response = self.client.get(self.accessory.get_absolute_url())
        self.assertContains(response, 'Detail Test Accessory')
        self.assertContains(response, 'An accessory for detail view testing')
        self.assertContains(response, '75')
