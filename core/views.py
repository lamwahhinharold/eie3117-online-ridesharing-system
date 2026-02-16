from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout


from django.db import transaction
from .models import Route, Booking
from .serializers import (
    RouteSerializer, BookingSerializer, UserSerializer, UserProfileSerializer,
    UserCreateSerializer,
)


class LoginRateThrottle(ScopedRateThrottle):
    """5 requests/minute for login attempts (uses 'login' scope from settings)."""
    scope = 'login'


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Public endpoint to get CSRF token.
    This ensures the csrftoken cookie is set.
    """
    return Response({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    Public registration endpoint (replaces djoser).
    """
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'detail': 'Account created successfully'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginRateThrottle])
def login_view(request):
    """
    Session-based login using cookies (as per requirement).
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'detail': 'Login successful'
        })
    else:
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Session-based logout, deletes cookie (as per requirement).
    """
    logout(request)
    return Response({'detail': 'Logged out successfully'})


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """
    Get current logged-in user info or update profile.
    """
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # Use profile serializer that excludes is_driver and username (read-only)
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return full user data for the frontend store
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('driver').prefetch_related('bookings__rider').order_by('-date', '-time')
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter routes by status via ?status= query param.
        Values: 'available' (not full and not expired), 'expired', 'full', or omit for all.
        """
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter == 'available':
            from django.utils import timezone
            import datetime
            now = timezone.now()
            qs = qs.filter(
                date__gte=now.date(),
            ).exclude(
                # Exclude routes whose date is today but time has already passed
                date=now.date(),
                time__lt=now.time(),
            )
            # Exclude fully booked routes (remaining_seats <= 0)
            from django.db.models import Count, F
            qs = qs.annotate(booked=Count('bookings')).filter(booked__lt=F('capacity'))
        elif status_filter == 'expired':
            from django.utils import timezone
            now = timezone.now()
            from django.db.models import Q
            qs = qs.filter(
                Q(date__lt=now.date()) |
                Q(date=now.date(), time__lt=now.time())
            )
        elif status_filter == 'full':
            from django.db.models import Count, F
            qs = qs.annotate(booked=Count('bookings')).filter(booked__gte=F('capacity'))
        return qs

    def perform_create(self, serializer):
        # Only drivers can advertise routes
        if not self.request.user.is_driver:
            raise PermissionDenied("Only drivers can advertise routes.")
        serializer.save(driver=self.request.user)

    def perform_update(self, serializer):
        # Only the route's driver can update it
        if serializer.instance.driver != self.request.user:
            raise PermissionDenied("You can only edit your own routes.")
        serializer.save()

    def perform_destroy(self, instance):
        # Only the route's driver can delete it
        if instance.driver != self.request.user:
            raise PermissionDenied("You can only delete your own routes.")
        instance.delete()

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        # Only riders (non-drivers) can reserve seats
        if request.user.is_driver:
            return Response(
                {"error": "Drivers cannot reserve seats. Please use a rider account."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Use transaction + select_for_update to prevent race conditions
        with transaction.atomic():
            route = Route.objects.select_for_update().get(pk=pk)
            user = request.user

            if not route.is_available:
                return Response(
                    {"error": "No seats available"}, status=status.HTTP_400_BAD_REQUEST
                )

            if Booking.objects.filter(route=route, rider=user).exists():
                return Response(
                    {"error": "Already joined this route"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Booking.objects.create(route=route, rider=user)

        return Response(
            {"status": "joined successfully"}, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["get"])
    def my_advertisements(self, request):
        """
        Endpoint: GET /api/routes/my_advertisements/
        Returns only the routes created by the logged-in driver.
        """
        routes = Route.objects.filter(driver=request.user).select_related('driver').prefetch_related('bookings__rider')
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)


class BookingViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Handles Rider reservations (list + cancel only).
    GET /api/bookings/ -> List only current user's reservations.
    DELETE /api/bookings/{id}/ -> Cancel a reservation.
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Riders only see their own bookings
        return Booking.objects.filter(rider=self.request.user).select_related('route', 'route__driver').prefetch_related('route__bookings__rider')
