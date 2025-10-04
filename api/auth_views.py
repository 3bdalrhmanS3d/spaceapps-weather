from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: OpenApiTypes.OBJECT, 400: OpenApiResponse(description="Validation error")},
        examples=[OpenApiExample(
            "Register Body",
            value={"username":"tester","password":"P@ssw0rd123","email":"t@example.com"},
            request_only=True
        )],
        description="Create a user and return an auth token.",
    )
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        username = s.validated_data["username"]
        password = s.validated_data["password"]
        email = s.validated_data.get("email", "")

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": {"id": user.id, "username": user.username, "email": user.email}},
                        status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiResponse(description="Invalid credentials")},
        examples=[OpenApiExample(
            "Login Body",
            value={"username":"tester","password":"P@ssw0rd123"},
            request_only=True
        )],
        description="Authenticate and return an auth token.",
    )
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        user = authenticate(request, username=s.validated_data["username"], password=s.validated_data["password"])
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        data = {"token": token.key, "user": {"id": user.id, "username": user.username, "email": user.email}}
        return Response(data)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserSerializer}, description="Return the authenticated user info.")
    def get(self, request):
        u = request.user
        return Response({"id": u.id, "username": u.username, "email": u.email})
