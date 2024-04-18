from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from google.cloud import vision
from google.oauth2 import service_account
import json
from environs import Env
from .models import ExtractedText
from .serializers import ExtractedTextSerializer, PostTextExtractionRequestSerializer
from image_handling.models import Image
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .exception import UnexpectedException

env = Env()
json_account_info = json.loads(env.str("GOOGLE_VISION_SERVICE_ACCOUNT"))  # convert JSON to dictionary

# Create your views here.
class TextExtraction(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PostTextExtractionRequestSerializer,
        responses={
            201: ExtractedTextSerializer,
            400: OpenApiResponse('Bad Request', description='Failed to Extract Text'),
            500: OpenApiResponse(UnexpectedException.default_code, description=UnexpectedException.default_detail),
        }
    )
    def post(self, request):
        try:
            # Setup google vision api
            credentials = service_account.Credentials.from_service_account_info(json_account_info)
            client = vision.ImageAnnotatorClient(credentials=credentials)
            image = vision.Image()

            # get image_url using the image id, then use it for the request
            user_image = Image.objects.get(image_id=request.data.get('image_id'))
            image.source.image_uri = user_image.image_url
            response = client.document_text_detection(image=image)

            paragraphs = []
            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        paragraph_text = "" 

                        for word in paragraph.words:
                            word_text = "".join([symbol.text for symbol in word.symbols])
                            if word_text[0].isalpha() or word_text[-1].isdigit():
                                word_text = " "+word_text

                            paragraph_text += word_text
                        paragraphs.append(paragraph_text.strip())

            if response.error.message:
                return Response({"error": "Google Cloud Service Account credentials error"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                extracted_text_model = ExtractedText.objects.create(
                    image = user_image, 
                    user_id = request.user,
                    extracted_text="•⌂".join(paragraphs))
                serializer = ExtractedTextSerializer(extracted_text_model)
                data=serializer.data
                data["extracted_text"] = data["extracted_text"].split("•⌂")
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExtractedTextList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: ExtractedTextSerializer(many=True),
        }
    )
    def get(self, request):
        extracted_texts = ExtractedText.objects.filter(user_id=request.user)
        serializer = ExtractedTextSerializer(extracted_texts, many=True)
        updated_data = []

        for item in serializer.data:
            item['extracted_text'] = item['extracted_text'].split('•⌂')
            updated_data.append(item)

        return Response(data=updated_data, status=status.HTTP_200_OK)        






       # extracted_text = ExtractedText.objects.get(text_id='1')
        # serializer = ExtractedTextSerializer(extracted_text)
        # print(serializer.data)