from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Image
from authentication.models import CustomUser
from .serialaizers import ImageSerializer, ImageUploadSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from .serialaizers import ImageUploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from environs import Env
import cloudinary

env = Env()
CLOUDINARY_API_SECRET = env.str("CLOUDINARY_API_SECRET")
CLOUDINARY_API_KEY = env.str("CLOUDINARY_API_KEY")
CLOUDINARY_CLOUD_NAME = env.str("CLOUDINARY_CLOUD_NAME")

cloudinary.config( 
  cloud_name = CLOUDINARY_CLOUD_NAME, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET,
  secure = True
)

import cloudinary.uploader

class ImageUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ImageUploadSerializer,
        responses={
            201: ImageSerializer,
            400: OpenApiResponse('Bad Request', description='Failed to upload image')
        }
    )
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        image_file = serializer.validated_data['image']
        upload_result = cloudinary.uploader.upload(image_file)

        # Save uploaded image details to the database
        uploaded_image = Image.objects.create(
            image_id=upload_result['public_id'],
            image_url=upload_result['secure_url'],
            user_id=serializer.validated_data['user']
        )
        serializer = ImageSerializer(uploaded_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ImageDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse('OK', description='Image deleted successfully'),
            400: OpenApiResponse('Bad Request', description='Failed to delete image')
        }
    )
    def delete(self, request, image_id):
        # Validate for if the image belongs to the current user before deletion
        image = Image.objects.get(image_id=image_id)
        if image.user_id != request.user:
            return Response({'message': 'Failed to delete image'}, status=status.HTTP_400_BAD_REQUEST)

        delete_result = cloudinary.uploader.destroy(image_id)
        if delete_result.get('result') == 'ok':
            # Delete the image from the database as well
            Image.objects.filter(image_id=image_id).delete()
            return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to delete image'}, status=status.HTTP_400_BAD_REQUEST)

