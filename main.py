import asyncio
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Database URL for Neon PostgreSQL database
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create an asynchronous engine
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": True}
)


# Define the Book model
class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    genre: str
    read: bool

# Initialize the database
async def init_db():
    """
    Initialize the database by creating the 'books' table if it does not exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Print the menu
def print_menu():
    """
    Print the menu options for the library manager.
    """
    print("\nWelcome to your Personal Library Manager!")
    print("1. Add book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics (total books, percentage read)")
    print("6. Exit")

# Add a book
async def add_book():
    """
    Add a new book to the library database.
    """
    title = input("Enter book name: ").strip()
    author = input("Enter the author name: ").strip()
    while True:
        try:
            year = int(input("Enter the publication year: ").strip())
            break
        except ValueError:
            print("Invalid year. Please enter a number.")
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = read_input == 'yes'

    book = Book(title=title.title(), author=author.title(), year=year, genre=genre.title(), read=read)
    async with AsyncSession(engine) as session:
        session.add(book)
        await session.commit()
    print("Book added successfully!")

# Remove a book
async def remove_book():
    """
    Remove a book from the library database by title.
    """
    title = input("Enter the title of the book to remove: ").strip()
    async with AsyncSession(engine) as session:
        statement = select(Book).where(Book.title.ilike(title))
        results = await session.exec(statement)
        books = results.all()
        if not books:
            print(f"Book '{title}' not found in the library.")
        else:
            for book in books:
                await session.delete(book)
            await session.commit()
            print(f"Book '{title}' removed successfully!")

# Search for books
async def search_books():
    """
    Search for books in the library database by title or author.
    """
    print("Search by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice: ").strip()
    if choice not in ("1", "2"):
        print("Invalid choice.")
        return
    search_term = input(f"Enter { 'Book Title' if choice == '1' else 'Author Name'}: ").strip()
    async with AsyncSession(engine) as session:
        if choice == "1":
            statement = select(Book).where(Book.title.ilike(f"%{search_term}%"))
        else:
            statement = select(Book).where(Book.author.ilike(f"%{search_term}%"))
        results = await session.exec(statement)
        books = results.all()
        if not books:
            print("No matching books found.")
        else:
            print("Matching Books:")
            for i, book in enumerate(books, 1):
                status = "Read" if book.read else "Unread"
                print(f"{i}. Name: {book.title} by {book.author} ({book.year}) - ({book.genre}) - ({status})")

# Display all books
async def display_books():
    """
    Display all books in the library database.
    """
    async with AsyncSession(engine) as session:
        statement = select(Book)
        results = await session.exec(statement)
        books = results.all()
        if not books:
            print("Your library is empty.")
        else:
            print("\nYour Library:\n")
            for i, book in enumerate(books, 1):
                status = "Read" if book.read else "Unread"
                print(f"{i}. Name: {book.title} by {book.author} ({book.year}) - ({book.genre}) - ({status})")

# Display library statistics
async def display_statistics():
    """
    Display statistics about the library, including total books and percentage read.
    """
    async with AsyncSession(engine) as session:
        total_statement = select(Book)
        total_results = await session.exec(total_statement)
        total = len(total_results.all())
        read_statement = select(Book).where(Book.read == True)
        read_results = await session.exec(read_statement)
        read_count = len(read_results.all())
        print(f"Total books: {total}")
        if total == 0:
            print("Percentage read: 0.0%")
        else:
            percentage = (read_count / total) * 100
            print(f"Percentage read: {percentage:.1f}%")

# Main application loop
async def main():
    """
    Main function to run the library manager application with Neon database using SQLModel.
    """
    await init_db()
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            await add_book()
        elif choice == "2":
            await remove_book()
        elif choice == "3":
            await search_books()
        elif choice == "4":
            await display_books()
        elif choice == "5":
            await display_statistics()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    asyncio.run(main())