from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import SummaryCreationSerializer, SummarizedTextSerializer


class TextSummarizationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SummaryCreationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)

        s_obj = serializer.save()

        response_serializer = SummarizedTextSerializer(instance=s_obj)
        response_data = response_serializer.data

        print(response_data)
        return Response(data=response_data)

text_summarization_view = TextSummarizationView.as_view()
