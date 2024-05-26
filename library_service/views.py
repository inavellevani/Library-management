from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from library_service.filters import BookFilter
from rest_framework import permissions, status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from library_service.models import Book, Author, Genre, BookBorrowHistory
from library_service.serializers import BookSerializer, AuthorSerializer, GenreSerializer, BookBorrowSerializer
from library_service.utils import (get_top_popular_books, get_top_late_users, get_top_late_returns,
                                   get_borrow_count_last_year)


class IsEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsStaffOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsEmployeePermission]


class GenreCreateView(generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsEmployeePermission]


class BookListCreateView(APIView):
    permission_classes = [IsEmployeePermission]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of books per page
        books = Book.objects.order_by('id')  # Ordering by book id, replace with desired field
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [IsEmployeePermission]

    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopPopularBooksView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        popular_books = get_top_popular_books()
        return Response(popular_books)


class BorrowCountLastYearView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        borrow_counts = get_borrow_count_last_year()
        return Response(borrow_counts)


class TopLateReturnsView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        late_returns = get_top_late_returns()
        return Response(late_returns)


class TopLateUsersView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        late_users = get_top_late_users()
        return Response(late_users)


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'user_profile.html'
    context_object_name = 'reserved_books'
    paginate_by = 10

    def get_queryset(self):
        return BookBorrowHistory.objects.filter(borrowed_by=self.request.user, returned_date__isnull=True)


class BookListView(FilterView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    filterset_class = BookFilter


class BookDetailViewUser(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        user = self.request.user
        # Check if the user has an active reservation for the book
        context['user_has_borrowed_book'] = BookBorrowHistory.objects.filter(
            book=book,
            borrowed_by=user,
            returned_date__isnull=True  # Only check active reservations
        ).exists()
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if 'reserve_book' in request.POST:
            if book.stock_count > 0:
                # Create a borrow history entry
                BookBorrowHistory.objects.create(
                    book=book,
                    borrowed_by=request.user,
                    borrowed_date=timezone.now().date(),
                    returned_date=None
                )
                # Decrease stock count by one
                book.stock_count -= 1
                book.save()
        elif 'cancel_reservation' in request.POST:
            # Cancel reservation
            reservation = BookBorrowHistory.objects.filter(
                book=book,
                borrowed_by=request.user,
                returned_date__isnull=True
            ).first()
            if reservation:
                # Delete the reservation entry
                reservation.delete()
                # Increase stock count by one
                book.stock_count += 1
                book.save()
        return redirect('book-detail', pk=book.pk)


class BookBorrowReservationView(generics.CreateAPIView):
    permission_classes = [IsEmployeePermission]
    queryset = BookBorrowHistory.objects.all()
    serializer_class = BookBorrowSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        book = Book.objects.filter(id=book_id, stock_count__gt=0).first()
        if book:
            book.stock_count -= 1
            book.save()
            reservation_data = {
                'book': book.id,
                'borrowed_by': request.user.id,
                'borrowed_date': timezone.now().date(),
                'returned_date': None
            }
            serializer = self.get_serializer(data=reservation_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'Book is not available for reservation'}, status=status.HTTP_400_BAD_REQUEST)
