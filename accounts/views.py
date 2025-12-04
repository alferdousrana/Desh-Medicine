# accounts/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer,
)
from .models import UserProfile


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/accounts/login/
    body: {"login": "<email or username>", "password": "..."}
    """
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """
    POST /api/accounts/logout/
    If using refresh token, client sends refresh and we blacklist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        return Response({"detail": "Logged out successfully."})


class MeProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/accounts/profile/me/
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ProfileDetailView(generics.RetrieveAPIView):
    """
    GET /api/accounts/profile/<slug>/
    slug based profile detail (public view)
    """
    queryset = UserProfile.objects.select_related("user")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
