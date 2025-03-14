import streamlit as st
import asyncio
import nest_asyncio  
import pandas as pd
from sqlmodel import Field, SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, connect_args={"ssl": True})

# Book model
class Book(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}  # Add this line
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    genre: str
    read: bool

# Database initialization
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Async database operations
async def add_book(title: str, author: str, year: int, genre: str, read: bool):
    async with AsyncSession(engine) as session:
        book = Book(
            title=title.title(),
            author=author.title(),
            year=year,
            genre=genre.title(),
            read=read
        )
        session.add(book)
        await session.commit()

async def delete_books(book_ids: list[int]):
    async with AsyncSession(engine) as session:
        for book_id in book_ids:
            book = await session.get(Book, book_id)
            if book:
                await session.delete(book)
        await session.commit()

async def search_books(search_type: str, query: str):
    async with AsyncSession(engine) as session:
        if search_type == "title":
            stmt = select(Book).where(Book.title.ilike(f"%{query}%"))
        else:
            stmt = select(Book).where(Book.author.ilike(f"%{query}%"))
        
        result = await session.exec(stmt)
        return result.all()

async def get_all_books():
    async with AsyncSession(engine) as session:
        result = await session.exec(select(Book))
        return result.all()

async def get_stats():
    async with AsyncSession(engine) as session:
        total = await session.scalar(select(func.count(Book.id)))
        read = await session.scalar(select(func.count(Book.id)).where(Book.read))
        return total, (read/total)*100 if total > 0 else 0

# Streamlit UI
def main():
    st.set_page_config(page_title="Personal Library Manager", layout="wide")
    nest_asyncio.apply() 

    asyncio.run(init_db())

    # Sidebar
    with st.sidebar:
        st.title("Library Manager")
        menu = st.radio("Menu", [
            "Add Book", 
            "Remove Book", 
            "Search Books", 
            "View All Books", 
            "Statistics"
        ])

    # Main content
    if menu == "Add Book":
        st.header("Add New Book")
        with st.form("add_form"):
            title = st.text_input("Title", key="add_title")
            author = st.text_input("Author", key="add_author")
            year = st.number_input("Year", min_value=1800 , key="add_year")
            genre = st.text_input("Genre", key="add_genre")
            read = st.checkbox("Read", key="add_read")
            
            if st.form_submit_button("Add Book"):
                if title and author and genre:
                    asyncio.run(add_book(title, author, year, genre, read))
                    st.success("Book added successfully!")
                else:
                    st.error("Please fill all required fields")

    elif menu == "Remove Book":
        st.header("Remove Book")
        search_term = st.text_input("Enter book title to search", key="remove_search_term")
        
        if st.button("Search"):
            books = asyncio.run(search_books("title", search_term))
            st.session_state.remove_books_found = books

        if "remove_books_found" in st.session_state:
            books = st.session_state.remove_books_found
            if books:
                df = pd.DataFrame([{
                    "ID": b.id,
                    "Title": b.title,
                    "Author": b.author,
                    "Year": b.year
                } for b in books])
                st.dataframe(df)
                selected = st.multiselect("Select books to delete", df["ID"].tolist(), key="remove_selected")
                if st.button("Delete Selected"):
                    # take names of books to be deleted
                    deleted_titles = [b.title for b in books if b.id in selected]
                    asyncio.run(delete_books(selected))
                    st.success(f"Deleted books: {', '.join(deleted_titles)}")
                    del st.session_state.remove_books_found
            else:
                st.warning("No books found")

    elif menu == "Search Books":
        st.header("Search Books")
        col1, col2 = st.columns([1,3])
        with col1:
            search_type = st.radio("Search by", ["title", "author"])
            search_query = st.text_input("Search term")
        
        if st.button("Search"):
            books = asyncio.run(search_books(search_type, search_query))
            if books:
                df = pd.DataFrame([{
                    "Title": b.title,
                    "Author": b.author,
                    "Year": b.year,
                    "Genre": b.genre,
                    "Read": "Yes" if b.read else "No"
                } for b in books])
                st.dataframe(df)
            else:
                st.info("No books found")

    elif menu == "View All Books":
        st.header("All Books")
        books = asyncio.run(get_all_books())
        if (books):
            df = pd.DataFrame([{
                "Title": b.title,
                "Author": b.author,
                "Year": b.year,
                "Genre": b.genre,
                "Read": "Yes" if b.read else "No"
            } for b in books])
            st.dataframe(df)
        else:
            st.info("Your library is empty")

    elif menu == "Statistics":
        st.header("Library Statistics")
        total, percentage = asyncio.run(get_stats())
        col1, col2 = st.columns(2)
        col1.metric("Total Books", total)
        col2.metric("Read Percentage", f"{percentage:.1f}%")

if __name__ == "__main__":
    main()