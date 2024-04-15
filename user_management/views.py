from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer
from authentication.models import CustomUser

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Retrieve user profile information',
        responses={200: UserSerializer},
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        description='Update user profile information',
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description='Delete user account',
        responses={204: None},
    )
    def delete(self):
        user = CustomUser.objects.get(username = self.request.user.username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
