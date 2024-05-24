from django.contrib import admin
from django.db.models import Count
from users.models import CustomUser
from .models import Book, Author, Genre, BookBorrowHistory


class BookBorrowHistoryInline(admin.TabularInline):
    model = BookBorrowHistory
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_date', 'stock_count', 'times_borrowed', 'available_count',
                    'borrowed_count')
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


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
