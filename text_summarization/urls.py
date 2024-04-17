from django.urls import include, path

from text_summarization.views import text_summarization_view


urlpatterns = [
    path('', text_summarization_view, name="summarize_text_view"),
    # path('test-vertexai/', TextExtraction.as_view()),
]
