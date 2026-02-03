from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .models import Route, Booking
from .serializers import RouteSerializer, BookingSerializer, UserSerializer


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
        # Allow updating nickname, email, and profile_image
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the driver to the current logged-in user
        serializer.save(driver=self.request.user)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        route = self.get_object()
        user = request.user

        # Business Logic Check
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
        routes = Route.objects.filter(driver=request.user)
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    Handles Rider reservations.
    GET /api/bookings/ -> List only current user's reservations.
    DELETE /api/bookings/{id}/ -> Cancel a reservation.
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Riders only see their own bookings
        return Booking.objects.filter(rider=self.request.user)
