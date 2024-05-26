import django_filters
from library_service.models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author__name = django_filters.CharFilter(lookup_expr='icontains')
    genre__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author__name', 'genre__name']
