from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from library_service.filters import BookFilter
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from library_service.models import Book, Author, Genre, BookBorrowHistory
from library_service.serializers import BookSerializer, AuthorSerializer, GenreSerializer, BookBorrowSerializer
from library_service.utils import (get_top_popular_books, get_top_late_users, get_top_late_returns,
                                   get_borrow_count_last_year)
from library_service.permissions import IsEmployeePermission, IsStaffOrAdminUser


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
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of books per page
        popular_books = get_top_popular_books()
        result_page = paginator.paginate_queryset(popular_books, request)
        return paginator.get_paginated_response(result_page)


class BorrowCountLastYearView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of books per page
        borrow_counts = get_borrow_count_last_year()
        result_page = paginator.paginate_queryset(borrow_counts, request)
        return paginator.get_paginated_response(result_page)


class TopLateReturnsView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of books per page
        late_returns = get_top_late_returns()
        result_page = paginator.paginate_queryset(late_returns, request)
        return paginator.get_paginated_response(result_page)


class TopLateUsersView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of users per page
        late_users = get_top_late_users()
        result_page = paginator.paginate_queryset(late_users, request)
        return paginator.get_paginated_response(result_page)


class BookReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book')
        book = Book.objects.filter(id=book_id, stock_count__gt=0).first()
        if book:
            reservation_date = timezone.now().date() + timedelta(days=1)
            reservation_data = {
                'book': book.id,
                'borrowed_by': request.user.id,
                'reservation_date': reservation_date,
            }
            serializer = BookBorrowSerializer(data=reservation_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Book is not available for reservation'}, status=status.HTTP_400_BAD_REQUEST)


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


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'user_profile.html'
    context_object_name = 'reserved_books'
    paginate_by = 10

    def get_queryset(self):
        return BookBorrowHistory.objects.filter(borrowed_by=self.request.user, returned_date__isnull=True)


class BookListView(LoginRequiredMixin, FilterView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(genre__name__icontains=search_query)
            )
        return queryset


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
                    reservation_date=timezone.now().date(),
                    returned_date=None
                )
                # Decrease stock count by one
                book.stock_count -= 1
                book.save(update_fields=['stock_count'])
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
                book.save(update_fields=['stock_count'])
        return redirect('book-detail', pk=book.pk)



