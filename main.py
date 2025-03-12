import json
import os

library_file = "library.json"

library = []


def load_library():
    global library
    if os.path.exists(library_file):
        try:
            with open(library_file, "r") as file:
                library = json.load(file)
        except json.JSONDecodeError:
            library = []
    else:
        library = []

def save_library():
    with open(library_file, "w") as file:
        json.dump(library, file, indent=4)

def print_menu():
    print("\nWelcome to your Personal Library Manager!")
    print("1. Add book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics (total books, percentage read)")
    print("6. Exit")

def add_book():
    title = input("Enter book name: ").strip()
    author = input("Enter the auther name: ").strip()

    while True:
        try:
            year = int(input("Enter the publication year: ").strip())
            break
        except ValueError:
            print("Invalid year. Please enter a number.")
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = read_input == 'yes'

    book = {
        "title": title.title(),
        "author": author.title(),
        "year": year,
        "genre": genre.title(),
        "read": read
    }

    library.append(book)
    print("Book Add Successfully")

def remove_book():
    title = input("Enter the title of the book to remove: ").strip()

    for book in library:
        if book['title'].lower() == title.lower():
            library.remove(book)
            print(f"Book '{title}' removed successfully!")
            return  
    
    print(f"Book '{title}' not found in the library.")

def search_books():
    print("Search by:")
    print("1. Title")
    print("2. Author")

    choice = input("Enter your choice: ").strip()

    if choice not in ("1", "2"):
        print("Invalid choice.")
        return
    
    search_term = input(f"Enter { "Book Title" if choice == "1" else "Author Name"}: ").strip()
    result = []

    if choice == "1":
        for book in library:
            if book['title'].lower() == search_term.lower():
                result.append(book)
    else:
        for book in library:
            if book["author"].lower() == search_term.lower():
               result.append(book)

    if not result:
        print("No matching books found.")

    else:
        print("Matching Books:")
        for i, book in enumerate(result, 1):
            status = "Read" if book["read"] else "Unread"
            print(f"{i}. Name: {book['title']} by {book['author']} ({book['year']}) - ({book['genre']}) - ({status})")

def display_books():
    if not library:
        print("Your library is empty.")
        return
    print("\nYour Library:\n")
    for i, book in enumerate(library, 1):
        status = "Read" if book["read"] else "Unread"
        print(f"{i}. Name: {book['title']} by {book['author']} ({book['year']}) - ({book['genre']}) - ({status})")

def display_statistics():
    total = len(library)
    print(f"Total books: {total}")

    if total == 0:
        print("Percentage read: 0.0%")
        return
    
    read_count = sum(1 for book in library if book["read"])
    percentage = (read_count / total) * 100
    print(f"Percentage read: {percentage:.1f}%")

def main():
    
    load_library()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()

        if choice == "2":
            remove_book()
        
        if choice == "3":
            search_books()
        
        if choice == "4":
            display_books()
        
        if choice == "5":
            display_statistics()
        
        if choice == "6":
            print("Saving library and exiting...")
            save_library()  
            break


if __name__ == "__main__":
    main()