from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from .models import VerificationKey, ContactSupport
User = get_user_model()


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainSerializer, cls).get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        try:
            user = User.objects.get(email=attrs.get('email'))
        except:
            data = {'details': 'No active account found with the given credentials'}
            return data
        data = super().validate(attrs)
        if user.verified is True:
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
        else:
            data = {
                'error': 'you should verify this account first before you login'
            }
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'username', 'profile_picture', 'country', 'phone_number']
        read_only_fields = ['username']
        extra_kwargs = {
            'profile_picture': {'required': False},
            'phone_number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserImageUpdateSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField(max_length=300)

    class Meta:
        fields = ['profile_picture']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class SetNewPassword(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            token = attrs.get('token', '')
            uidb64 = attrs.get('uidb64', '')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('the link is invalid', 401)
            user.set_password(password)
            user.save()
        except:
            raise AuthenticationFailed('the link is invalid', 401)
        return super().validate(attrs)


class VerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationKey
        fields = ['code', 'user']
        read_only_fields = ['user']


class ContactSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactSupport
        fields = ['user', 'name', 'subject', 'message']
        read_only_fields = ['user']
