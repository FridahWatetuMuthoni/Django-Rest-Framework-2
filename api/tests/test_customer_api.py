from django.urls import reverse, resolve
from django.test import SimpleTestCase
from api.views import CustomerView
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiUrlsTests(SimpleTestCase):

    def test_get_customers_is_resolved(self):
        url = reverse('customers')
        print(resolve(url).func.view_class)
        self.assertEquals(resolve(url).func.view_class, CustomerView)


class CustomerAPIViewTests(APITestCase):
    customers_url = reverse("customers")

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_customers_authenticated(self):
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customers_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customers_url)
        self.assertEquals(response.status_code, 401)

    def test_post_customer_authenticated(self):
        data = {
            "title": "Mr",
            "first_name": "Peter",
            "last_name": "Parkerz",
            "gender": "Male",
            "status": "published"
        }
        response = self.client.post(self.customers_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(len(response.data))
        # self.assertEqual(len(response.data), 8)


class CustomerDetailAPIViewTests(APITestCase):
    customer_url = reverse('customer_detail', args=[1])
    customers_url = reverse("customers")

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Saving customer
        data = {
            "title": "Mrs",
            "first_name": "Johnson",
            "last_name": "MOrisee",
            "gender": "Female",
            "status": "published"
        }
        self.client.post(
            self.customers_url, data, format='json')

    def test_get_customer_autheticated(self):
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Johnson')

    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 401)

    def test_delete_customer_authenticated(self):
        response = self.client.delete(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
