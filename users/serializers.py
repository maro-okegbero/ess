from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    serializer for registering admins
    """
    id = serializers.CharField(max_length=255, required=False, write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['is_administrator'] = True
        user = User.objects.create_user(**validated_data)

        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token', 'is_administrator')


class CreateUserSerializer(RegisterSerializer):
    """
    serializer for creating users
    """

    def create(self, validated_data):
        """
        serializer.save() calls this function
        """
        validated_data['email'] = validated_data['email'].lower()
        validated_data['is_administrator'] = False
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(read_only=True)
    date_of_birth = serializers.DateTimeField(read_only=True)

    image = serializers.URLField(read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid" information. In the case of logging a
        # user in, this means validating that they've provided a username
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email').lower()
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username
            authenticated_user = authenticate(username=username, password=password)

            if authenticated_user is None:
                raise serializers.ValidationError(
                    'A user with this email and password was not found.'
                )

            if not authenticated_user.is_active:
                raise serializers.ValidationError(
                    'This user has been deactivated.'
                )
        except Exception as e:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        serializer = UserSerializer(user)
        data = serializer.data
        return data

    def create(self, validated_data):
        return super(LoginSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(LoginSerializer, self).update(validated_data=validated_data, instance=instance)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', "is_administrator"]
