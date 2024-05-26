from django.urls import path
from library_service.views import BookListCreateView, BookDetailView, AuthorCreateView, \
    GenreCreateView, BookBorrowReservationView, BookListView, BookDetailViewUser, \
    UserProfileView


urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorCreateView.as_view(), name='author-create'),
    path('genres/', GenreCreateView.as_view(), name='genre-create'),
    path('reservations/', BookBorrowReservationView.as_view(), name='book-reservation'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('book/', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', BookDetailViewUser.as_view(), name='book-detail')


]


