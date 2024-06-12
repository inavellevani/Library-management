from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from library_service.models import Book, Author, Genre, BookBorrowHistory


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BookBorrowHistoryInline(admin.TabularInline):
    model = BookBorrowHistory
    extra = 0
    fields = ('book', 'borrowed_by', 'borrowed_date', 'returned_date', 'reservation_date')
    readonly_fields = ('reservation_date',)  # reservation_date should be read-only


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_genres', 'publication_date', 'stock_count', 'times_borrowed',
                    'available_count', 'borrowed_count')

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Genres'

    list_filter = ('author', 'genre')
    search_fields = ('title', 'author__name', 'genre__name')
    inlines = [BookBorrowHistoryInline]

    def times_borrowed(self, obj):
        return obj.bookborrowhistory_set.count()
    times_borrowed.short_description = 'Times Borrowed'

    def available_count(self, obj):
        return obj.stock_count - obj.borrowed_count
    available_count.short_description = 'Available Count'

    def borrowed_count(self, obj):
        return obj.bookborrowhistory_set.filter(returned_date__isnull=True).count()
    borrowed_count.short_description = 'Borrowed Count'


@admin.register(BookBorrowHistory)
class BookBorrowHistoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrowed_by_link', 'borrowed_date', 'returned_date', 'reservation_date')
    list_filter = ('book', 'borrowed_by', 'borrowed_date', 'returned_date', 'reservation_date')
    search_fields = ('book__title', 'borrowed_by__email')
    fields = ('book', 'borrowed_by', 'borrowed_date', 'returned_date', 'reservation_date')

    def borrowed_by_link(self, obj):
        url = reverse('admin:users_customuser_change', args=[obj.borrowed_by.id])
        return mark_safe(f'<a href="{url}">{obj.borrowed_by.email}</a>')
    borrowed_by_link.short_description = 'Borrowed By'
