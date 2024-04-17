import google.generativeai as genai
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import FlashcardCategory, Flashcard
from .serializers import FlashcardCategorySerializer, FlashcardSerializer
from image_handling.models import Image
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from environs import Env

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
    def get(self, request):
        defaults = {
            'model': 'models/text-bison-001',
            'temperature': 0.7,
            'candidate_count': 1,
            'top_k': 40,
            'top_p': 0.95,
            'max_output_tokens': 1024,
        }

        # number_of_cards = max(request.data.get('number_of_cards'), 15)
        # text = request.data.get('text')
        # category_id = request.data.get('category')

        # category = FlashcardCategory.objects.get(id=category_id)
        prompt = f"""
        Generate {10} questions, and answers for those questions from the text below. give your respose as a list of python dicts each with a question key and an answer key

        illing machines must provide a rotating spindle for the cutter and a table for fastening,
positioning, and feeding the workpart. Various machine tool designs satisfy these require￾ments. To begin with, milling machines can be classified as horizontal or vertical. A
horizontal milling machine has a horizontal spindle, and this design is well suited for
performing peripheral milling (e.g., slab milling, slotting, side and straddle milling) on
workparts that are roughly cube shaped. A vertical milling machine has a vertical spindle,
and this orientation is appropriate for face milling, end milling, surface contouring, and die￾sinking on relatively flat workparts.
Other than spindle orientation, milling machines can be classified into the following
types: (1) knee-and-column, (2) bed type, (3) planer type, (4) tracer mills, and (5) CNC
milling machines.
The knee-and-column milling machine is the basic machine tool for milling. It
derives its name from the fact that its two main components are a column that supports
the spindle, and a knee (roughly resembling a human knee) that supports the worktable.
It is available as either a horizontal or a vertical machine, as illustrated in Figure 22.23. In
the horizontal version, an arbor usually supports the cutter. The arbor is basically a shaft
that holds the milling cutter and is driven by the spindle. An overarm is provided on
FIGURE 22.23 Two basic types of knee-and-column milling machine: (a) horizontal and (b) vertical.
528 Chapter 22/Machining Operations and Machine Tools
E1C22 10/26/2009 15:27:27 Page 529
horizontal machines to support the arbor. On vertical knee-and-column machines,
milling cutters can be mounted directly in the spindle without an arbor.
One of the features of the knee-and-column milling machine that makes it so
versatile is its capability for worktable feed movement in any of the x–y–z axes. The
worktable can be moved in the x-direction, the saddle can be moved in the y-direction,
and the knee can be moved vertically to achieve the z-movement.
Two special knee-and-column machines should be identified. One is the uni￾versal milling machine, Figure 22.24(a), which has a table that can be swiveled in a
horizontal plane (about a vertical axis) to any specified angle. This facilitates the
cutting of angular shapes and helixes on workparts. Another special machine is the
ram mill, Figure 22.24(b), in which the toolhead containing the spindle is located on
the end of a horizontal ram; the ram can be adjusted in and out over the worktable to
locate the cutter relative to the work. The toolhead can also be swiveled to achieve an
angular orientation of the cutter with respect to the work. These features provide
considerable versatility in machining a variety of work shapes.
Bed-type milling machines are designed for high production. They are con￾structed with greater rigidity than knee-and-column machines, thus permitting them to
achieve heavier feed rates and depths of cut needed for high material removal rates. The
characteristic construction of the bed-type milling machine is shown in Figure 22.25.
FIGURE 22.24 Special types of knee-and-column milling machine: (a) universal—overarm, arbor, and cutter omitted
for clarity: and (b) ram type.
FIGURE 22.25 Simplex bed￾type milling machine horizontal
spindle.
Section 22.4/Milling 529
E1C22 10/26/2009 15:27:27 Page 530
The worktable is mounted directly to the bed of the machine tool, rather than using the
less rigid knee-type design. This construction limits the possible motion of the table to
longitudinal feeding of the work past the milling cutter. The cutter is mounted in a
spindle head that can be adjusted vertically along the machine column. Single spindle
bed machines are called simplex mills, as in Figure 22.25, and are available in either
horizontal or vertical models. Duplex mills use two spindle heads. The heads are usually
positioned horizontally on opposite sides of the bed to perform simultaneous operations during one feeding pass of the work. Triplex mills add a third spindle mounted
vertically over the bed to further increase machining capability.
Planer type mills are the largest milling machines. Their general appearance and
construction are those of a large planer (see Figure 22.31); the difference is that milling is
performed instead of planing. Accordingly, one or more milling heads are substituted for the
single-point cutting tools used on planers, and the motion of the work past the tool is a feed
rate motion rather than a cutting speed motion. Planer mills are built to machine very large
parts. The worktable and bed of the machine are heavy and relatively low to the ground, and
the milling heads are supported by a bridge structure that spans across the table.
A tracer mill, also called a profiling mill, is designed to reproduce an irregular part
geometry that has been created on a template. Using either manual feed by a human
operator or automatic feed by the machine tool, a tracing probe is controlled to follow the
template while a milling head duplicates the path taken by the probe to machine the desired
shape. Tracer mills are of two types: (1) x y tracing, in which the contour of a flat template
is profile milled using two-axis control; and (2) x–y–z tracing, in which the probe follows a
three-dimensional pattern using three-axis control. Tracer mills have been used for
creating shapes that cannot easily be generated by a simple feeding action of the work
against the milling cutter. Applications include molds and dies. In recent years, many of
these applications have been taken over by CNC milling machines.
        """

        response = genai.generate_text(
        **defaults,
        prompt=prompt
        )
        print(response.result)
        print(genai.list_models())
        return Response("yogata")
