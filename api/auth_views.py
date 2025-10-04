# api/auth_views.py
from django.contrib.auth.models import User
import dj_database_url 
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# ---- Serializers ----
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=False, allow_blank=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# ---- Views ----
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Created',
                        value={
                            'token': '3e3a6c9c4b2f4...',
                            'user': {'id': 1, 'username': 'tester', 'email': 't@example.com'}
                        }
                    )
                ],
            ),
            400: OpenApiResponse(description='Validation error')
        },
        examples=[
            OpenApiExample(
                'Register Body',
                value={'username': 'tester', 'password': 'P@ssw0rd123', 'email': 't@example.com'},
                request_only=True
            )
        ],
        description="Create a user and return an auth token.",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email', '')

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'OK',
                        value={
                            'token': '3e3a6c9c4b2f4...',
                            'user': {'id': 1, 'username': 'tester', 'email': 't@example.com'}
                        }
                    )
                ],
            ),
            400: OpenApiResponse(description='Invalid credentials')
        },
        examples=[
            OpenApiExample(
                'Login Body',
                value={'username': 'tester', 'password': 'P@ssw0rd123'},
                request_only=True
            )
        ],
        description="Authenticate and return an auth token.",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description="Return the authenticated user info.",
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)
