import jwt
from .models import Image
from authentication.models import CustomUser
from rest_framework import serializers
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from environs import Env

env = Env()
SECRET_KEY = env.str("SECRET_KEY")

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["user_id", 'image_id', 'image_url', "uploaded_at"]

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate(self, attrs):
        request = self.context.get('request')
        auth_header = get_authorization_header(request).decode('utf-8')
        if not auth_header:
            raise AuthenticationFailed('Authorization header not found')
        try:
            token = auth_header.split()[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(user_id=payload['user_id'])
            attrs['user'] = user
        except (jwt.DecodeError, CustomUser.DoesNotExist):
            raise AuthenticationFailed('Invalid token or user not found')
        return attrs