from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Route, Booking


# Register the custom User model
class CustomUserAdmin(UserAdmin):
    model = User
    # Add custom fields (nickname, is_driver, profile_image) to the Admin forms
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("nickname", "is_driver", "profile_image")}),
    )
    # Add custom fields to the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("nickname", "is_driver", "profile_image")}),
    )
    # Fields to display in the list view
    list_display = ["username", "nickname", "email", "is_driver", "is_staff"]
    list_filter = ["is_driver", "is_staff", "is_superuser"]


# Register Route model with a nice list view
class RouteAdmin(admin.ModelAdmin):
    list_display = [
        "start_location",
        "destination",
        "driver",
        "date",
        "time",
        "capacity",
        "get_remaining",
    ]
    list_filter = ["date", "start_location", "destination"]
    search_fields = ["start_location", "destination", "car_model"]

    def get_remaining(self, obj):
        return obj.remaining_seats

    get_remaining.short_description = "Seats Left"


# Register Booking model
class BookingAdmin(admin.ModelAdmin):
    list_display = ["route", "rider", "created_at"]
    list_filter = ["created_at"]


# Register all models to the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Booking, BookingAdmin)
