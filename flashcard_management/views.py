import google.generativeai as genai
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import FlashcardCategory, Flashcard
from .serializers import FlashcardCategorySerializer, FlashcardSerializer, FlashcardRequestSerializer
from image_handling.models import Image
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from environs import Env
import json

env = Env()
genai.configure(api_key=env.str("GOOGLE_GEMINI_API_KEY"))

class FlashcardCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: FlashcardCategorySerializer(many=True),
        },
        description="Get a list of flashcard categories for the authenticated user.",
    )
    def get(self, request):
        categories = FlashcardCategory.objects.filter(user=request.user)
        serializer = FlashcardCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=FlashcardCategorySerializer,
        responses={
            201: FlashcardCategorySerializer,
            400: OpenApiResponse("Bad Request", description="Invalid input data."),
        },
        description="Create a new flashcard category for the authenticated user.",
    )
    def post(self, request):
        serializer = FlashcardCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FlashcardCategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("category_id", OpenApiParameter.PATH, description="ID of the flashcard category."),
        ],
        responses={
            200: FlashcardCategorySerializer,
            404: OpenApiResponse("Not Found", description="Flashcard category not found."),
        },
        description="Get a specific flashcard category for the authenticated user.",
    )
    def get(self, request, category_id):
        try:
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
        except FlashcardCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FlashcardCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("category_id", OpenApiParameter.PATH, description="ID of the flashcard category."),
        ],
        request=FlashcardCategorySerializer,
        responses={
            200: FlashcardCategorySerializer,
            400: OpenApiResponse("Bad Request", description="Invalid input data."),
            404: OpenApiResponse("Not Found", description="Flashcard category not found."),
        },
        description="Update an existing flashcard category for the authenticated user.",
    )
    def put(self, request, category_id):
        try:
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
        except FlashcardCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FlashcardCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter("category_id", OpenApiParameter.PATH, description="ID of the flashcard category."),
        ],
        responses={
            204: OpenApiResponse(
                "No Content",
                description="Flashcard category deleted successfully.",
            ),
            404: OpenApiResponse("Not Found", description="Flashcard category not found."),
        },
        description="Delete a flashcard category for the authenticated user.",
    )
    def delete(self, request, category_id):
        try:
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
        except FlashcardCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FlashcardListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: FlashcardSerializer(many=True),
        },
        description="Get a list of flashcards for the authenticated user.",
    )
    def get(self, request):
        flashcards = Flashcard.objects.filter(user=request.user)
        serializer = FlashcardSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=FlashcardSerializer,
        responses={
            201: FlashcardSerializer,
            400: OpenApiResponse("Bad Request", description="Invalid input data."),
        },
        description="Create a new flashcard for the authenticated user.",
    )
    def post(self, request):
        image_id = request.data.get('image')
        category_id = request.data.get('category')
        question = request.data.get('question')
        answer = request.data.get('answer')
        if not image_id or not category_id or not question or not answer:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category = FlashcardCategory.objects.get(id=category_id)
        image = Image.objects.get(image_id=image_id)
        new_flashcard = Flashcard.objects.create(
            category=category,
            image=image,
            user=request.user,
            question=question,
            answer=answer
        )

        serializer = FlashcardSerializer(new_flashcard)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class FlashcardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: FlashcardSerializer,
            404: OpenApiResponse("Not Found", description="Flashcard not found."),
        },
        description="Get a specific flashcard for the authenticated user.",
    )
    def get(self, request, flashcard_id):
        try:
            flashcard = Flashcard.objects.get(id=flashcard_id, user=request.user)
        except Flashcard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FlashcardSerializer(flashcard)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=FlashcardSerializer,
        responses={
            200: FlashcardSerializer,
            400: OpenApiResponse("Bad Request", description="Invalid input data."),
            404: OpenApiResponse("Not Found", description="Flashcard not found."),
        },
        description="Update an existing flashcard for the authenticated user.",
    )
    def put(self, request, flashcard_id):
        try:
            flashcard = Flashcard.objects.get(id=flashcard_id, user=request.user)
        except Flashcard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FlashcardSerializer(flashcard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(
                "No Content",
                description="Flashcard deleted successfully.",
            ),
            404: OpenApiResponse("Not Found", description="Flashcard not found."),
        },
        description="Delete a flashcard for the authenticated user.",
    )
    def delete(self, request, flashcard_id):
        try:
            flashcard = Flashcard.objects.get(id=flashcard_id, user=request.user)
        except Flashcard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GenerateFlashcards(APIView):
    permission_classes=[IsAuthenticated]


    @extend_schema(
        request=FlashcardRequestSerializer,
        responses={
            201: FlashcardSerializer(many=True),
            400: OpenApiResponse('Bad Request', description='Text and category are required.'),
            500: OpenApiResponse('Internal Server Error', description='Could not load questions. Please try again.')
        }
    )
    def post(self, request):
        number_of_cards = int(request.data.get('number_of_cards', 15))
        text = request.data.get('text')
        category_id = request.data.get('category')

        defaults = {
            'model': 'models/text-bison-001',
            'temperature': 0.5,
            'candidate_count': 1,
            'top_k': 40,
            'top_p': 0.95,
            'max_output_tokens': 1024,
        }

        if not text or not category_id:
            return Response({'error': 'Text and category are required.'}, status=status.HTTP_400_BAD_REQUEST)
        category = FlashcardCategory.objects.get(id=category_id)

        prompt = f"""
        Generate {number_of_cards} questions, and answers for those questions from the text below. Your response must be a list of python dicts each with a question key and an answer key i.e [{"{"}"question": str, "answer": str{"}"}] in json format.

        {text}
        """
        response = genai.generate_text(
        **defaults,
        prompt=prompt
        )

        results =[]
        try:
            results = json.loads(response.result)
        except ValueError:
            response = genai.generate_text(
                **defaults,
                prompt=prompt
            )
            try: 
                results = json.loads(response.result)
            except ValueError as e:
                return Response({'error': 'Could not load questions. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = []
        for result in results:
            flashcard = Flashcard.objects.create(
                category=category, 
                user = request.user, 
                question = result["question"],
                answer = result["answer"],
            )
            serializer = FlashcardSerializer(flashcard)
            response_data.append(serializer.data)
        return Response(data=response_data, status=status.HTTP_201_CREATED)
