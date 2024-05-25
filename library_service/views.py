from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from library_service.models import Book
from library_service.serializers import BookSerializer


class IsEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class BookListCreateView(APIView):
    permission_classes = [IsEmployeePermission]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


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
