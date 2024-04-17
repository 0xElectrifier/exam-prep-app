from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.FlashcardCategoryListView.as_view(), name='flashcard_category_list'),
    path('categories/<int:category_id>/', views.FlashcardCategoryDetailView.as_view(), name='flashcard_category_detail'),
    path('', views.FlashcardListView.as_view(), name='flashcard_list'),
    path('<int:flashcard_id>/', views.FlashcardDetailView.as_view(), name='flashcard_detail'),
    path('generate/', views.GenerateFlashcards.as_view(), name='generate_flashcard'),
]