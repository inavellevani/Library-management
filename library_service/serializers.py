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
    class Meta:
        model = Book
        fields = '__all__'


class BookBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrowHistory
        fields = '__all__'
