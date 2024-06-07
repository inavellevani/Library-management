from django.urls import path
from library_service.views import BookListCreateView, BookDetailView, AuthorCreateView, \
    GenreCreateView, BookBorrowReservationView, BookListView, BookDetailViewUser, \
    UserProfileView, TopPopularBooksView, BorrowCountLastYearView, TopLateReturnsView, TopLateUsersView

urlpatterns = [
    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/authors/', AuthorCreateView.as_view(), name='author-create'),
    path('api/genres/', GenreCreateView.as_view(), name='genre-create'),
    path('api/reservations/', BookBorrowReservationView.as_view(), name='book-reservation'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('book/', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', BookDetailViewUser.as_view(), name='book-detail'),
    path('api/stats/popular-books/', TopPopularBooksView.as_view(), name='top-popular-books'),
    path('api/stats/borrow-count-last-year/', BorrowCountLastYearView.as_view(), name='borrow-count-last-year'),
    path('api/stats/late-returns/', TopLateReturnsView.as_view(), name='top-late-returns'),
    path('api/stats/late-users/', TopLateUsersView.as_view(), name='top-late-users'),
]


