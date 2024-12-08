# Library Management System API

This project is a simple Flask-based API for a Library Management System that supports CRUD operations for books and members. It also includes optional search functionality for books by title or author, as well as pagination and token-based authentication.

## Features

1. **CRUD operations** for books and members.
2. **Search functionality** to search books by title or author.
3. **Pagination** for listing books or members.
4. **Token-based authentication** for secure access.

## Design Choices

- **Flask Framework**: A lightweight and simple web framework for Python, chosen for its simplicity and scalability.
- **SQLite Database**: Chosen as the database to keep things simple and easy to set up.
- **Token-based Authentication**: To ensure that only authenticated users can perform certain operations (CRUD for books and members).

## Assumptions and Limitations

1. The database is stored in an SQLite file, and it is not meant for production use. For a production environment, an RDBMS like PostgreSQL or MySQL would be more appropriate.
2. Authentication tokens are not refreshed in this application. Tokens expire after a certain period, and users need to log in again to generate a new one.
3. No third-party libraries for ORM or database migration were used in this project to meet the project constraints.

## How to Run the Project

### Prerequisites

1. Python 3.8 or above.
2. SQLite (should be included with Python by default).

### Steps
   ```bash

  # Clone the repository
   git clone https://github.com/yourusername/library-management-system.git

  # Navigate inside the folder
   cd folder_name

# Create a virtual environment
py -m venv _name_of_virtual_environment_ (Windows)
python -m venv _name_of_virtual_environment_ (Unix/MacOS)

# Activate the virtual environment
_name_of_virtual_environment_\Scripts\activate (Windows)
source _name_of_virtual_environment_/bin/activate (Unix/MacOS)

# Install requirements
pip install -r requirements.txt

# run tests:
pytest

# ___ IMPORTANT___
# Create a .env file and add SECRET_KEY eg: SECRET_KEY=e9b1d04b6fba3a9856f73a04eae7a839f03b2b8e5d6d6cf792302e9e9c9d123f
# The authentication credentials for admin are static, i.e. :
  username: "admin"
  password: "admin"
```
## Authentication

All member endpoints are protected with token-based authentication. To access the endpoints, you must first log in and obtain a token.

### Login Endpoint

- **URL**: `/login`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "username": "admin",
        "password": "admin"
    }
    ```
- **Response**:
    - **Success (200 OK)**:
        ```json
        {
            "token": "your.jwt.token"
        }
        ```
    - **Error (400 Bad Request)**:
        ```json
        {
            "message": "Invalid username or password"
        }
        ```

---

## Member Endpoints

### 1. List Members
- **URL**: `/members`
- **Method**: `GET`
- **Description**: Retrieve a list of all library members with optional search and pagination.
- **Query Parameters**:
    - `search`: (optional) Search for members by name or email (string).
    - `page`: (optional) The page number for pagination (integer, default is 1).
    - `per_page`: (optional) The number of members per page (integer, default is 10).
- **Request Example**:
    ```bash
    curl -X GET "http://127.0.0.1:5000/members?search=john&page=1&per_page=5"
    ```

- **Response**:
    - **Success (200 OK)**:
        ```json
        {
            "items": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "membership_date": "2023-01-01"
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane.smith@example.com",
                    "membership_date": "2023-02-15"
                }
            ],
            "total": 50,
            "pages": 5,
            "page": 1
        }
        ```
    - **Error (400 Bad Request)**:
        ```json
        {
            "message": "Invalid page number"
        }
        ```

---

### 2. Create Member
- **URL**: `/members`
- **Method**: `POST`
- **Description**: Add a new library member.
- **Request Body**:
    ```json
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "membership_date": "2023-01-01"
    }
    ```
- **Response**:
    - **Success (201 Created)**:
        ```json
        {
            "id": 3,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "membership_date": "2023-01-01"
        }
        ```
    - **Error (400 Bad Request)**:
        ```json
        {
            "message": "Invalid input data"
        }
        ```

---

### 3. Update Member
- **URL**: `/members/<id>`
- **Method**: `PUT`
- **Description**: Update an existing member's details.
- **URL Parameters**:
    - `id`: The unique identifier of the member (integer).
- **Request Body**:
    ```json
    {
        "name": "John Updated",
        "email": "john.updated@example.com",
        "membership_date": "2023-02-01"
    }
    ```
- **Response**:
    - **Success (200 OK)**:
        ```json
        {
            "id": 1,
            "name": "John Updated",
            "email": "john.updated@example.com",
            "membership_date": "2023-02-01"
        }
        ```
    - **Error (404 Not Found)**:
        ```json
        {
            "message": "Member not found"
        }
        ```

---

### 4. Delete Member
- **URL**: `/members/<id>`
- **Method**: `DELETE`
- **Description**: Delete an existing member by their ID.
- **URL Parameters**:
    - `id`: The unique identifier of the member (integer).
- **Response**:
    - **Success (204 No Content)**: No response body, just a 204 status code indicating successful deletion.
    - **Error (404 Not Found)**:
        ```json
        {
            "message": "Member not found"
        }
        ```

---


## Example Requests

### List Members (with search and pagination)
```bash
curl -X GET "http://127.0.0.1:5000/members?search=doe&page=2&per_page=5"
```

# Books API

This API allows you to perform operations related to books, such as creating, updating, deleting, and listing books.

## Endpoints

### 1. List Books
- **URL**: `/books`
- **Method**: `GET`
- **Description**: Retrieve a list of all books with optional search and pagination.
- **Query Parameters**:
    - `search`: (optional) Search for books by title or author (string).
    - `page`: (optional) The page number for pagination (integer, default is 1).
    - `per_page`: (optional) The number of books per page (integer, default is 10).
- **Request Example**:
    ```bash
    curl -X GET "http://127.0.0.1:5000/books?search=python&page=1&per_page=5"
    ```
- **Response**:
    - **Success (200 OK)**:
        ```json
        {
            "items": [
                {
                    "id": 1,
                    "title": "Learn Python",
                    "author": "John Doe",
                    "published_date": "2023-01-01"
                },
                {
                    "id": 2,
                    "title": "Advanced Python",
                    "author": "Jane Smith",
                    "published_date": "2023-02-15"
                }
            ],
            "total": 50,
            "pages": 5,
            "page": 1
        }
        ```
    - **Error (400 Bad Request)**:
        ```json
        {
            "message": "Invalid page number"
        }
        ```

---

### 2. Create Book
- **URL**: `/books`
- **Method**: `POST`
- **Description**: Add a new book to the library.
- **Request Body**:
    ```json
    {
        "title": "New Book Title",
        "author": "Author Name",
        "published_date": "2023-04-01"
    }
    ```
- **Response**:
    - **Success (201 Created)**:
        ```json
        {
            "id": 3,
            "title": "New Book Title",
            "author": "Author Name",
            "published_date": "2023-04-01"
        }
        ```
    - **Error (400 Bad Request)**:
        ```json
        {
            "message": "Invalid input data"
        }
        ```

---

### 3. Update Book
- **URL**: `/books/<id>`
- **Method**: `PUT`
- **Description**: Update an existing book's details.
- **URL Parameters**:
    - `id`: The unique identifier of the book (integer).
- **Request Body**:
    ```json
    {
        "title": "Updated Book Title",
        "author": "Updated Author Name",
        "published_date": "2023-05-01"
    }
    ```
- **Response**:
    - **Success (200 OK)**:
        ```json
        {
            "id": 1,
            "title": "Updated Book Title",
            "author": "Updated Author Name",
            "published_date": "2023-05-01"
        }
        ```
    - **Error (404 Not Found)**:
        ```json
        {
            "message": "Book not found"
        }
        ```

---

### 4. Delete Book
- **URL**: `/books/<id>`
- **Method**: `DELETE`
- **Description**: Delete an existing book by its ID.
- **URL Parameters**:
    - `id`: The unique identifier of the book (integer).
- **Response**:
    - **Success (204 No Content)**: No response body, just a 204 status code indicating successful deletion.
    - **Error (404 Not Found)**:
        ```json
        {
            "message": "Book not found"
        }
        ```

---
