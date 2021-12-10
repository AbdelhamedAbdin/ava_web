# from django.test import TestCase
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
# ## App Imports ##
# from .serivces import generate_token
#
# ## External Apps Imports ##
#
# # Create your tests here.
# class RegistrationTestCases(APITestCase):
#     BASE_URL = '/api/authentication/register/'
#     VALID_REGISTRATION = {
#         "email": "me@admin.com",
#         "password": "12346789",
#         "name": "Mina"
#     }
#     ALREADY_USED_EMAIL_REGISTRATION = {
#         "email": "test@gmail.com",
#         "password": "12346789",
#         "name": "Mina"
#     }
#     MISSING_REGISTRATION = {
#         "email": "me@admin.com",
#         "name": "Mina"
#     }
#     LESS_THAN_8_CHAR_PASS = {
#         "email": "me@admin.com",
#         "password": "1239",
#         "name": "Mina"
#     }
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         User.objects.create_user(email='test@gmail.com', password="MinaRoger00")
#
#     def test_registration_valid_data(self):
#         response = self.client.post(self.BASE_URL, data=self.VALID_REGISTRATION)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_registration_used_email(self):
#         response = self.client.post(self.BASE_URL, data=self.ALREADY_USED_EMAIL_REGISTRATION)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_registration_less_than_8_password(self):
#         response = self.client.post(self.BASE_URL, data=self.LESS_THAN_8_CHAR_PASS)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_registration_missing_data(self):
#         response = self.client.post(self.BASE_URL, data=self.MISSING_REGISTRATION)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class ObtainTokenTestCases(APITestCase):
#     BASE_URL = '/api/authentication/token/obtain/'
#     VALID_AUTHENTICATION = {
#         "email": "test@gmail.com", "password": "MinaRoger00"}
#     INVALID_AUTHENTICATION = {
#         "email": "test@gmail.com", "password": "12345678"}
#     MISSING_AUTHENTICATION = {
#         "email": "test@gmail.com"}
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         User.objects.create_user(email='test@gmail.com', password="MinaRoger00")
#
#     def test_obtain_token_valid_data(self):
#         response = self.client.post(self.BASE_URL, data=self.VALID_AUTHENTICATION)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_obtain_token_invalid_data(self):
#         response = self.client.post(self.BASE_URL, data=self.INVALID_AUTHENTICATION)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_obtain_token_missing_data(self):
#         response = self.client.post(self.BASE_URL, data=self.MISSING_AUTHENTICATION)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class RefreshTokenTestCases(APITestCase):
#     refresh = ""
#     VALID_AUTHENTICATION = {
#         "email": "test@gmail.com", "password": "MinaRoger00"}
#     BASE_URL = '/api/authentication/token/refresh/'
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         user = User.objects.create_user(email='test@gmail.com', password="MinaRoger00")
#         tokens = generate_token(user)
#         cls.refresh = tokens['refresh']
#
#     def test_refresh_token_valid_refresh(self):
#         response = self.client.post(self.BASE_URL, {"refresh": self.refresh})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_refresh_token_invalid_refresh(self):
#         response = self.client.post(self.BASE_URL, {"refresh": "123"})
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_refresh_token_missing_refresh(self):
#         response = self.client.post(self.BASE_URL, {})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class BlackListTokenTestCases(APITestCase):
#     BASE_URL = "/api/authentication/blacklist/"
#     refresh_token = ""
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         user = User.objects.create_user(email='test@gmail.com', password="MinaRoger00")
#         tokens = generate_token(user)
#         cls.refresh_token = tokens['refresh']
#
#     def test_black_list_token(self):
#         data = {"refresh": self.refresh_token}
#         response = self.client.post(self.BASE_URL, data=data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
#
#     def test_black_list_token_invalid(self):
#         data = {"refresh" : "asdsadsadsad"}
#         response = self.client.post(self.BASE_URL, data=data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
