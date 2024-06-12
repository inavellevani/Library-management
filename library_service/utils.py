from django.db.models import Count, Q, F, ExpressionWrapper, DateField, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from library_service.models import Book, BookBorrowHistory
from users.models import CustomUser


def get_top_popular_books():
    popular_books = Book.objects.annotate(borrow_count=Count('bookborrowhistory')).order_by('-borrow_count')[:10]
    return list(popular_books.values('title', 'borrow_count'))


def get_borrow_count_last_year():
    one_year_ago = timezone.now().date() - timedelta(days=365)
    book_borrow_counts = []
    for book in Book.objects.all():
        borrow_count = BookBorrowHistory.objects.filter(book=book, borrowed_date__gte=one_year_ago).count()
        book_borrow_counts.append({
            'title': book.title,
            'borrow_count': borrow_count
        })
    return book_borrow_counts


def get_top_late_returns():
    late_returns_subquery = BookBorrowHistory.objects.filter(
        returned_date__gt=Coalesce(F('borrowed_date'), timezone.now().date()),
        book=OuterRef('pk')
    ).order_by().values('book').annotate(
        late_count=Count('id')
    ).values('late_count')

    late_returns = Book.objects.annotate(
        late_count=Subquery(late_returns_subquery)
    ).order_by('-late_count').values('title', 'late_count')[:100]

    return list(late_returns)


def get_top_late_users():
    late_users = CustomUser.objects.annotate(
        late_count=Count('bookborrowhistory', filter=Q(bookborrowhistory__returned_date__gt=F('bookborrowhistory__borrowed_date')))
    ).order_by('-late_count').values('email', 'late_count')[:100]
    return list(late_users)
