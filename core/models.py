from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


class User(AbstractUser):
    # Requirements: login id (username), nick name, email, type, and profile image
    nickname = models.CharField(max_length=100, blank=True)
    is_driver = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return self.username


class Route(models.Model):
    # Requirements: driver, date, time, start, destination, car model, capacity, description
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="advertised_routes"
    )
    date = models.DateField()
    time = models.TimeField()
    start_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    car_model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    @property
    def remaining_seats(self):
        booked_count = self.bookings.count()
        return self.capacity - booked_count

    @property
    def is_available(self):
        # Route becomes unavailable if capacity is reached or route is expired
        return self.remaining_seats > 0 and not self.is_expired

    @property
    def is_expired(self):
        """True if the route's date/time is in the past."""
        route_datetime = datetime.datetime.combine(self.date, self.time)
        route_datetime = timezone.make_aware(route_datetime) if timezone.is_naive(route_datetime) else route_datetime
        return route_datetime < timezone.now()

    def __str__(self):
        return f"{self.start_location} to {self.destination} ({self.date})"


class Booking(models.Model):
    # Requirements: Rider can reserve a route
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="bookings")
    rider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_bookings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate bookings: one rider can only book a route once
        unique_together = ['route', 'rider']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rider.username} -> {self.route}"
