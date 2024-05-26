from django.contrib import admin
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
