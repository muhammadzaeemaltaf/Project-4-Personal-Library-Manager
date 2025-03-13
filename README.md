# Personal Library Manager

A command-line tool to manage your personal book collection using a Neon PostgreSQL database.

## Features
- Add books with title, author, year, genre, and read status.
- Remove books by title.
- Search books by title or author (partial, case-insensitive matching).
- Display all books in the library.
- View statistics: total books and percentage read.
- Exit the application.

## Prerequisites
- Python 3.13+
- A Neon PostgreSQL database account

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-manager.git
   cd library-manager

2. Set up a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies:
    ```bash
    pip install sqlmodel asyncpg python-dotenv

4. Configure the environment:
    - Create a .env file in the project root.
    - Add your Neon database URL:

    
    ```
    DATABASE_URL=postgresql+asyncpg://your_username:your_password@your_host/your_db

## Usage

1. Run the application:
    ```bash
    python main.py

2. Choose from the menu:

    1. Add book: Enter book details.
    2. Remove a book: Enter the title to remove.
    3. Search for a book: Search by title or author.
    4. Display all books: View your library.
    5. Display statistics: See totals and percentages.
    6. Exit: Quit the app.

## Database

- Uses a Neon PostgreSQL database.
- The books table is created automatically on first run.

## Code Structure

- **main.py**: Core application code.  
- **.env**: Stores the database URL (keep this file private).  