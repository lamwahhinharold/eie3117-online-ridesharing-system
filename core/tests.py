from django.test import TestCase, override_settings
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Route, Booking
from datetime import date, time, timedelta


# Disable throttling during tests so rate limits don't interfere
TEST_REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}


@override_settings(REST_FRAMEWORK=TEST_REST_FRAMEWORK)
class AuthTests(TestCase):
    """Tests for registration, login, logout, and session persistence."""

    def setUp(self):
        cache.clear()  # Reset throttle state between tests
        self.client = APIClient()
        # Fetch CSRF token first
        self.client.get('/api/csrf/')

    def _get_csrf(self):
        cookies = self.client.cookies
        return cookies.get('csrftoken').value if cookies.get('csrftoken') else ''

    def test_register_rider(self):
        resp = self.client.post('/api/register/', {
            'username': 'rider1',
            'password': 'testpass123',
            'nickname': 'Rider One',
            'email': 'rider1@test.com',
            'is_driver': False,
        }, HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='rider1').exists())
        user = User.objects.get(username='rider1')
        self.assertFalse(user.is_driver)

    def test_register_driver(self):
        resp = self.client.post('/api/register/', {
            'username': 'driver1',
            'password': 'testpass123',
            'nickname': 'Driver One',
            'email': 'driver1@test.com',
            'is_driver': True,
        }, HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='driver1')
        self.assertTrue(user.is_driver)

    def test_register_missing_fields(self):
        resp = self.client.post('/api/register/', {
            'username': 'bad',
        }, HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        resp = self.client.post('/api/register/', {
            'username': 'user1',
            'password': 'short',
            'nickname': 'Test',
            'email': 'test@test.com',
        }, HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(username='user1', password='testpass123', nickname='U1', email='u@t.com')
        resp = self.client.post('/api/login/', {
            'username': 'user1',
            'password': 'testpass123',
        }, HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('user', resp.json())

    def test_login_failure(self):
        resp = self.client.post('/api/login/', {
            'username': 'nonexistent',
            'password': 'wrong',
        }, HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        User.objects.create_user(username='user1', password='testpass123')
        self.client.login(username='user1', password='testpass123')
        resp = self.client.post('/api/logout/', HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # After logout, accessing user should fail
        resp = self.client.get('/api/user/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_current_user(self):
        User.objects.create_user(username='user1', password='pass12345', nickname='Nick', email='n@t.com')
        self.client.login(username='user1', password='pass12345')
        resp = self.client.get('/api/user/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['username'], 'user1')
        self.assertEqual(resp.json()['nickname'], 'Nick')

    def test_update_profile(self):
        User.objects.create_user(username='user1', password='pass12345', nickname='Old', email='old@t.com')
        self.client.login(username='user1', password='pass12345')
        resp = self.client.patch('/api/user/', {
            'nickname': 'NewNick',
            'email': 'new@t.com',
        }, format='json', HTTP_X_CSRFTOKEN=self._get_csrf())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['nickname'], 'NewNick')
        self.assertEqual(resp.json()['email'], 'new@t.com')


@override_settings(REST_FRAMEWORK=TEST_REST_FRAMEWORK)
class RouteTests(TestCase):
    """Tests for route CRUD and listing."""

    def setUp(self):
        cache.clear()  # Reset throttle state between tests
        self.client = APIClient()
        self.client.get('/api/csrf/')
        self.driver = User.objects.create_user(
            username='driver1', password='testpass123',
            nickname='Driver', email='d@t.com', is_driver=True,
        )
        self.rider = User.objects.create_user(
            username='rider1', password='testpass123',
            nickname='Rider', email='r@t.com', is_driver=False,
        )
        self.future_date = date.today() + timedelta(days=7)

    def _csrf(self):
        cookies = self.client.cookies
        return cookies.get('csrftoken').value if cookies.get('csrftoken') else ''

    def _create_route(self, **overrides):
        defaults = {
            'date': str(self.future_date),
            'time': '10:00:00',
            'start_location': 'PolyU',
            'destination': 'Central',
            'car_model': 'Tesla Model 3',
            'capacity': 3,
            'description': 'Test route',
        }
        defaults.update(overrides)
        return self.client.post('/api/routes/', defaults, HTTP_X_CSRFTOKEN=self._csrf())

    def test_driver_can_create_route(self):
        self.client.login(username='driver1', password='testpass123')
        resp = self._create_route()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 1)

    def test_rider_cannot_create_route(self):
        self.client.login(username='rider1', password='testpass123')
        resp = self._create_route()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_routes_public(self):
        Route.objects.create(
            driver=self.driver, date=self.future_date, time=time(10, 0),
            start_location='A', destination='B', car_model='Car', capacity=2,
        )
        resp = self.client.get('/api/routes/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json().get('results', resp.json())
        self.assertEqual(len(results), 1)

    def test_retrieve_route(self):
        route = Route.objects.create(
            driver=self.driver, date=self.future_date, time=time(10, 0),
            start_location='A', destination='B', car_model='Car', capacity=2,
        )
        resp = self.client.get(f'/api/routes/{route.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['start_location'], 'A')

    def test_driver_can_update_own_route(self):
        self.client.login(username='driver1', password='testpass123')
        route = Route.objects.create(
            driver=self.driver, date=self.future_date, time=time(10, 0),
            start_location='A', destination='B', car_model='Car', capacity=2,
        )
        resp = self.client.patch(f'/api/routes/{route.id}/', {
            'destination': 'Tsim Sha Tsui',
        }, format='json', HTTP_X_CSRFTOKEN=self._csrf())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['destination'], 'Tsim Sha Tsui')

    def test_driver_cannot_update_others_route(self):
        driver2 = User.objects.create_user(
            username='driver2', password='testpass123', is_driver=True,
        )
        route = Route.objects.create(
            driver=driver2, date=self.future_date, time=time(10, 0),
            start_location='A', destination='B', car_model='Car', capacity=2,
        )
        self.client.login(username='driver1', password='testpass123')
        resp = self.client.patch(f'/api/routes/{route.id}/', {
            'destination': 'Hacked',
        }, format='json', HTTP_X_CSRFTOKEN=self._csrf())
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_driver_can_delete_own_route(self):
        self.client.login(username='driver1', password='testpass123')
        route = Route.objects.create(
            driver=self.driver, date=self.future_date, time=time(10, 0),
            start_location='A', destination='B', car_model='Car', capacity=2,
        )
        resp = self.client.delete(f'/api/routes/{route.id}/', HTTP_X_CSRFTOKEN=self._csrf())
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Route.objects.count(), 0)

    def test_my_advertisements(self):
        self.client.login(username='driver1', password='testpass123')
        Route.objects.create(
            driver=self.driver, date=self.future_date, time=time(10, 0),
            start_location='A', destination='B', car_model='Car', capacity=2,
        )
        resp = self.client.get('/api/routes/my_advertisements/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        self.assertEqual(len(results), 1)

    def test_date_in_past_rejected(self):
        self.client.login(username='driver1', password='testpass123')
        resp = self._create_route(date=str(date.today() - timedelta(days=1)))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_capacity_validation(self):
        self.client.login(username='driver1', password='testpass123')
        resp = self._create_route(capacity=0)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp = self._create_route(capacity=51)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(REST_FRAMEWORK=TEST_REST_FRAMEWORK)
class BookingTests(TestCase):
    """Tests for joining routes, cancelling, and capacity enforcement."""

    def setUp(self):
        cache.clear()  # Reset throttle state between tests
        self.client = APIClient()
        self.client.get('/api/csrf/')
        self.driver = User.objects.create_user(
            username='driver1', password='testpass123',
            nickname='Driver', email='d@t.com', is_driver=True,
        )
        self.rider = User.objects.create_user(
            username='rider1', password='testpass123',
            nickname='Rider', email='r@t.com', is_driver=False,
        )
        self.route = Route.objects.create(
            driver=self.driver, date=date.today() + timedelta(days=7),
            time=time(10, 0), start_location='PolyU', destination='Central',
            car_model='Car', capacity=2,
        )

    def _csrf(self):
        cookies = self.client.cookies
        return cookies.get('csrftoken').value if cookies.get('csrftoken') else ''

    def test_rider_can_join_route(self):
        self.client.login(username='rider1', password='testpass123')
        resp = self.client.post(
            f'/api/routes/{self.route.id}/join/',
            HTTP_X_CSRFTOKEN=self._csrf(),
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_driver_cannot_join_route(self):
        self.client.login(username='driver1', password='testpass123')
        resp = self.client.post(
            f'/api/routes/{self.route.id}/join/',
            HTTP_X_CSRFTOKEN=self._csrf(),
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_join_twice(self):
        self.client.login(username='rider1', password='testpass123')
        self.client.post(f'/api/routes/{self.route.id}/join/', HTTP_X_CSRFTOKEN=self._csrf())
        resp = self.client.post(f'/api/routes/{self.route.id}/join/', HTTP_X_CSRFTOKEN=self._csrf())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_join_full_route(self):
        rider2 = User.objects.create_user(username='rider2', password='testpass123', is_driver=False)
        rider3 = User.objects.create_user(username='rider3', password='testpass123', is_driver=False)
        Booking.objects.create(route=self.route, rider=self.rider)
        Booking.objects.create(route=self.route, rider=rider2)
        # Route capacity is 2, now full
        self.client.login(username='rider3', password='testpass123')
        resp = self.client.post(f'/api/routes/{self.route.id}/join/', HTTP_X_CSRFTOKEN=self._csrf())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remaining_seats(self):
        self.assertEqual(self.route.remaining_seats, 2)
        Booking.objects.create(route=self.route, rider=self.rider)
        self.assertEqual(self.route.remaining_seats, 1)

    def test_is_available(self):
        rider2 = User.objects.create_user(username='rider2', password='testpass123', is_driver=False)
        self.assertTrue(self.route.is_available)
        Booking.objects.create(route=self.route, rider=self.rider)
        Booking.objects.create(route=self.route, rider=rider2)
        self.assertFalse(self.route.is_available)

    def test_cancel_booking(self):
        self.client.login(username='rider1', password='testpass123')
        booking = Booking.objects.create(route=self.route, rider=self.rider)
        resp = self.client.delete(
            f'/api/bookings/{booking.id}/',
            HTTP_X_CSRFTOKEN=self._csrf(),
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

    def test_list_my_bookings(self):
        self.client.login(username='rider1', password='testpass123')
        Booking.objects.create(route=self.route, rider=self.rider)
        resp = self.client.get('/api/bookings/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json().get('results', resp.json())
        self.assertEqual(len(results), 1)

    def test_cannot_see_others_bookings(self):
        rider2 = User.objects.create_user(username='rider2', password='testpass123', is_driver=False)
        Booking.objects.create(route=self.route, rider=self.rider)
        self.client.login(username='rider2', password='testpass123')
        resp = self.client.get('/api/bookings/')
        results = resp.json().get('results', resp.json())
        self.assertEqual(len(results), 0)

    def test_unique_booking_constraint(self):
        """Database-level unique constraint prevents duplicate bookings."""
        Booking.objects.create(route=self.route, rider=self.rider)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Booking.objects.create(route=self.route, rider=self.rider)
