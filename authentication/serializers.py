from dj_rest_auth.serializers import LoginSerializer as _LoginSerializer


class LoginSerializer(_LoginSerializer):
    """
    Custom serializer to remove 'email' field from LoginSerializer.
    """
    email = None
