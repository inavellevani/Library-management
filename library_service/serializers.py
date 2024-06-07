from rest_framework import serializers
from library_service.models import Book, Author, Genre, BookBorrowHistory


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='name', queryset=Author.objects.all())
    genre = serializers.SlugRelatedField(slug_field='name', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = '__all__'


class BookBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrowHistory
        fields = ('id', 'book', 'borrowed_by', 'borrowed_date', 'returned_date', 'reservation_date')
        read_only_fields = ('borrowed_date',)
