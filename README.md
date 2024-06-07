# Library Management System

This is a Django-based Library Management System that allows users to browse and borrow books from the library. It also provides administrative features for managing books, authors, genres, and user accounts.

<br>

## Features

- User Registration and Authentication
- Book Listing and Filtering
- Book Reservation and Borrowing
- Author and Genre Management (Staff Only)
- Book Management (Staff Only)
- Analytics for Popular Books, Borrow Counts, Late Returns, and Late Users (Admin Only)


## Installation

### Clone the repository
git clone https://github.com/your-username/library-management-system.git

### Create a virtual environment and activate it
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`

### Install the required packages
`pip install -r requirements.txt`

### Apply database migrations
`python manage.py migrate`

### (Optional) Load sample data
`python populate_books.py`

### Create a superuser (admin)
`python manage.py createsuperuser`

### Start the development server
`python manage.py runserver`


# Usage

## User Registration and Login

- Visit /register to create a new user account.
- Visit /login to log in with an existing account.

## Book Listing and Filtering

- Visit /books to view a list of available books.
- Use the filter options to narrow down the results based on title, author, genre, or publication date.

## Book Reservation and Borrowing

- Click on a book to view its details.
- If the book is available, click the "Reserve Book" button to borrow it.
- Visit /profile to view your borrowed books.

## Admin Features

- Log in with a staff or superuser account.
- Visit /admin to access the Django admin interface.
- Manage authors, genres, books, and user accounts from the admin interface.
- Visit /top-popular-books to view the most popular books (based on borrowing count).
- Visit /borrow-count-last-year to view the borrow count for the last year.
- Visit /top-late-returns to view the books with the most late returns.
- Visit /top-late-users to view the users with the most late returns.