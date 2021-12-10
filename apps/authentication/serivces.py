from .serializers import TokenObtainSerializer


def generate_token(user):
    token_serializer = TokenObtainSerializer()
    refresh = token_serializer.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

