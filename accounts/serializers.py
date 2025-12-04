# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "date_joined"]
        read_only_fields = ["id", "date_joined", "role"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "slug",
            "first_name",
            "last_name",
            "profile_picture",
            "gender",
            "date_of_birth",
            "address",
            "phone",
            "city",
            "area",
            "zip_code",
            "bio",
            "medical_history",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
        )

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login with email OR username.
    Request body:
    {
      "login": "<email or username>",
      "password": "..."
    }
    """

    login = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make email optional because we are using "login" instead
        self.fields["email"].required = False

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")

        if not login or not password:
            raise serializers.ValidationError({"detail": "Login and password required."})

        # Find user by email or username
        user = None
        if "@" in login:
            user = User.objects.filter(email__iexact=login).first()
        if user is None:
            user = User.objects.filter(username__iexact=login).first()

        if user is None:
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        # set email in attrs so parent validate() can work normally
        attrs["email"] = user.email

        # call parent to actually create tokens (it uses email + password)
        data = super().validate(attrs)

        # include user info in response
        from .serializers import UserSerializer  # avoid circular at top
        data["user"] = UserSerializer(user).data

        return data
