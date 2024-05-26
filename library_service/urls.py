from django.urls import path
from library_service.views import BookListCreateView, BookDetailView, AuthorCreateView, \
    GenreCreateView  # Import the updated view


urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorCreateView.as_view(), name='author-create'),
    path('genres/', GenreCreateView.as_view(), name='genre-create'),
]
