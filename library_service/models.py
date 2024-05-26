from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    # Add other relevant fields

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    # Add other relevant fields

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    genre = models.ManyToManyField(Genre, verbose_name=_('Genre'))
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    publication_date = models.DateField(verbose_name=_('Publication Date'))
    stock_count = models.PositiveIntegerField(verbose_name=_('Stock Count'))

    @property
    def borrowed_count(self):
        return self.bookborrowhistory_set.filter(returned_date__isnull=True).count()

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')


class BookBorrowHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    borrowed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Borrowed By'))
    borrowed_date = models.DateField(auto_now_add=True, verbose_name=_('Borrowed Date'))
    returned_date = models.DateField(null=True, blank=True, verbose_name=_('Returned Date'))

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrowed_by.email}"

    class Meta:
        verbose_name = _('Book Borrow History')
        verbose_name_plural = _('Book Borrow Histories')
