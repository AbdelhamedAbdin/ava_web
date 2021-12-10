from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_str, smart_bytes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from .utils import token_generator
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .serializers import VerificationCodeSerializer, ContactSupportSerializer
from django.template.loader import render_to_string
from .models import ContactSupport

## App Imports ##
from .models import VerificationKey
from . import serializers

User = get_user_model()


# Create your views here.
class ObtainTokenPairWithColorView(TokenObtainPairView):
    """
    This view obtains takes the user login info to create an access and refresh tokens.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.TokenObtainSerializer


# Logout + place expiration tokens into black-list
class LogoutAndBlacklistRefreshTokenForUserView(generics.GenericAPIView):
    """
    This endpoint blacklists a user token, it is used to log out.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Register
class RegistrationView(generics.GenericAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            # activate view
            link = reverse('apps.authentication:activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

            verification_code_numbers = VerificationKey.objects.get(user=user)
            activate_url = request.scheme + "://%s%s" % (domain, link)
            email_subject = 'Activate your account'
            email_body = 'Hi %s please use this link to verify your account\n%s\nyour code is: %s' % (user.username, activate_url, verification_code_numbers.code)
            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user]
            )
            email_message.send(fail_silently=False)
            return Response(data={'user_created': '(%s) has been created verify your account by email' % user.email}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


# Verification code
class Verification(generics.GenericAPIView):
    serializer_class = VerificationCodeSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if user.verified is True:
                return Response({'invalid_token': 'User has been verified'}, status=status.HTTP_400_BAD_REQUEST)

            if not token_generator.check_token(user, token):
                return Response({'invalid_token': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'token': token,
                'uidb64': uidb64
            }, status=status.HTTP_200_OK)
        except:
            return Response({'invalid_token': 'Token is out dated'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        verification_code = VerificationKey.objects.get(user=user)

        if verification_code.code == int(request.data.get('code')):
            user.verified = True
            user.save()
            return Response({'success': 'your account has been verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'verification key number is incorrect'}, status=status.HTTP_406_NOT_ACCEPTABLE)


# Update image for user
class UpdateImageView(generics.GenericAPIView):
    serializer_class = serializers.UserImageUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self, queryset=None, **kwargs):
        user = get_object_or_404(self.queryset.filter(username=self.kwargs["username"]))
        if user is not None and self.request.user == user:
            return user
        elif user is not None and self.request.user != user:
            raise PermissionDenied('You Have No Permission To Access this User')
        else:
            raise PermissionDenied('Bad Request')

    def post(self, request, username=None):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(request.data.get('profile_picture'))
            user.profile_picture = request.data.get('profile_picture')
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


# Send token to email to edit password
class PasswordResetRequest(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetRequestSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)  # token
            current_site = get_current_site(request=request).domain  # domain
            email_subject = 'Reset your password'
            relative_link = reverse('apps.authentication:password_reset_confirm', kwargs={
                'uidb64': uidb64, 'token': token
            })
            absurl = 'http://' + current_site + relative_link
            email_body = f'Hi {user.username}, use link below to reset your password with the following domain:{absurl}'

            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user]
            )
            email_message.send(fail_silently=False)
            return Response({'success': 'check your email to reset your password'}, status=status.HTTP_200_OK)
        return Response("This email doesn't exist", status=status.HTTP_404_NOT_FOUND)


# View credentials
class PasswordReset(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token})
        except DjangoUnicodeDecodeError as error:
            pass


# Field to set a new password
class SetNewPassword(generics.GenericAPIView):
    serializer_class = serializers.SetNewPassword
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Passowrd reset success'}, status=status.HTTP_200_OK)


# Contact Support
class ContactSupportView(generics.GenericAPIView):
    serializer_class = ContactSupportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.filter(email=self.request.user.email)
        if not user.exists():
            return Response(data={'error': 'This user doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
        if user.get() and user.get().email == self.request.user.email:
            request.data['user'] = user
            serializer = self.serializer_class(data=request.data, instance=user.get())

            if serializer.is_valid(raise_exception=True):
                contact = ContactSupport(
                    name=request.data.get('name'),
                    subject=request.data.get('subject'),
                    message=request.data.get('message')
                )
                contact.user = user.get()
                contact.save()

                subject = request.data.get('subject')
                name = request.data.get('name')
                context = {
                    'name': request.data.get('name'),
                    "subject": request.data.get('subject'),
                    "message": request.data.get('message')
                }
                html_message = render_to_string("contact.html", context)

                send_mail(
                    subject=subject,
                    message=name,
                    from_email=self.request.user.email,
                    recipient_list=['Info@avafinance.app'],
                    fail_silently=False,
                    html_message=html_message
                )
                return Response({"success": "message has been sent"}, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied('You Have No Permission To Access this page')
        return Response({"error": "Invalid request!"}, status=status.HTTP_400_BAD_REQUEST)
