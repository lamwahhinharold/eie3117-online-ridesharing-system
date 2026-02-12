from rest_framework import serializers
from django.utils import timezone
from .models import User, Route, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "nickname", "email", "is_driver", "profile_image")
        read_only_fields = ("id", "username", "is_driver")


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile updates — only allows safe fields."""
    class Meta:
        model = User
        fields = ("nickname", "email", "profile_image")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True, min_length=1)

    class Meta:
        model = User
        fields = ("username", "nickname", "email", "password", "is_driver", "profile_image")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class RouteSerializer(serializers.ModelSerializer):
    driver_name = serializers.ReadOnlyField(source="driver.nickname")
    driver = serializers.ReadOnlyField(source="driver.id")
    remaining_seats = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    passengers = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            "id",
            "driver",
            "driver_name",
            "date",
            "time",
            "start_location",
            "destination",
            "car_model",
            "capacity",
            "remaining_seats",
            "is_available",
            "description",
            "passengers",
        )

    def get_passengers(self, obj):
        # Returns a list of nicknames of riders who booked this specific route
        return [booking.rider.nickname for booking in obj.bookings.all()]

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1.")
        if value > 50:
            raise serializers.ValidationError("Capacity cannot exceed 50.")
        return value

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Route date cannot be in the past.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    rider_name = serializers.ReadOnlyField(source="rider.nickname")
    # Nested serializer to give the frontend all route info for the "My Rides" list
    route_details = RouteSerializer(source="route", read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "route", "rider", "rider_name", "route_details", "created_at")
