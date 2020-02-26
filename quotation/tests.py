from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group

class UserViewTestCate(APITestCase):
  def test_create_user_without_username(self):
    request = self.client.post('/user/', {
      "email": "email@gmail.com",
      "password": "supersecret",
      "first_name": "Finxi",
      "last_name": "User"
    })
    
    self.assertEqual(request.data, {
      "username": [
        "This field is required."
      ]
    })

class UserGroupViewTestCate(APITestCase):
  def setUp(self):
    User.objects.create_user(
      username='admin_f',
      email='email@gmail.com',
      password='password123',
      first_name='Finxi',
      last_name='Adm',
      is_active=True,
      is_superuser=True,
      is_staff=True,
    )

    User.objects.create_user(
      username='administrator',
      email='email@gmail.com',
      password='password123',
      first_name='Finxi',
      last_name='Administrator',
      is_active=True,
      is_superuser=False,
      is_staff=True,
    )

    User.objects.create_user(
      username='advertiser',
      email='email@gmail.com',
      password='password123',
      first_name='Finxi',
      last_name='Advertiser',
      is_active=True,
      is_superuser=False,
      is_staff=False,
    )
  
  def makeLogin(self, username, password):
    return self.client.post('/auth/token/login/', {
      "username": username,
	    "password": password
    })
  
  def setToken(self, username, password):
    request = self.makeLogin(username, password)
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + request.data['auth_token'])

  def test_associate_user_to_group_advertiser_with_superuser(self):
    # Get user to get id
    user = User.objects.get(username='advertiser')
    group = Group.objects.get(name='advertiser')

    # Set Token
    self.setToken('admin_f', 'password123')

    request = self.client.post('/user/'+str(user.id)+'/group/', {
      "group_name": "advertiser"
    })

    self.assertEqual(request.data, {
      "user_id": user.id,
      "username": user.username,
      "group": {
        "id": group.id,
        "name": group.name
      }
    })

    # Reset credential
    self.client.credentials()
  
  def test_associate_user_to_group_advertiser_with_user_login(self):
    # Get user to get id
    user = User.objects.get(username='advertiser')
    group = Group.objects.get(name='advertiser')

    # Set Token
    self.setToken('advertiser', 'password123')

    request = self.client.post('/user/'+str(user.id)+'/group/', {
      "group_name": "advertiser"
    })

    self.assertEqual(request.data, {
      "user_id": user.id,
      "username": user.username,
      "group": {
        "id": group.id,
        "name": group.name
      }
    })

    # Reset credential
    self.client.credentials()
  
  def test_associate_user_to_group_administrator_without_superuser(self):
    # Get user to get id
    user = User.objects.get(username='advertiser')
    group = Group.objects.get(name='administrator')

    # Set Token
    self.setToken('advertiser', 'password123')

    request = self.client.post('/user/'+str(user.id)+'/group/', {
      "group_name": "administrator"
    })

    self.assertEqual(request.data, {
      'message': "Not authorized to associate to this group"
    })

    # Reset credential
    self.client.credentials()
  
  def test_associate_another_user_to_group_administrator_without_superuser(self):
    # Get user to get id
    user = User.objects.get(username='advertiser')
    group = Group.objects.get(name='administrator')

    # Set Token
    self.setToken('advertiser', 'password123')

    request = self.client.post('/user/1/group/', {
      "group_name": "administrator"
    })

    self.assertEqual(request.data, {
      'message': "Can't assign to that user, with this level of authentication"
    })

    # Reset credential
    self.client.credentials()
