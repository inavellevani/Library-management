import os
import django
import random
from faker import Faker
from datetime import date, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()
from library_service.models import Book, Author, Genre

fake = Faker()


def generate_author_name():
    return fake.name()


def generate_genre_name():
    return fake.word()


def generate_book_title():
    return fake.sentence(nb_words=4)


def generate_publication_date():
    start_date = date(1900, 1, 1)
    end_date = date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date


def generate_stock_count():
    return random.randint(1, 10)


def generate_books():
    authors = [Author.objects.create(name=generate_author_name()) for _ in range(50)]
    genres = [Genre.objects.create(name=generate_genre_name()) for _ in range(20)]

    for _ in range(1000):
        author = random.choice(authors)
        book_genres = random.sample(genres, random.randint(1, 3))
        book = Book.objects.create(
            author=author,
            title=generate_book_title(),
            publication_date=generate_publication_date(),
            stock_count=generate_stock_count()
        )
        book.genre.set(book_genres)


if __name__ == '__main__':
    generate_books()
