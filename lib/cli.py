import click
from bookstore.database import init_db, get_db
from bookstore.models import Book, Author
from sqlalchemy.orm import Session

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized.")

@cli.command()
@click.argument('name')
def add_author(name):
    """Add a new author."""
    db = next(get_db())
    author = Author(name=name)
    db.add(author)
    db.commit()
    click.echo(f"Author {name} added.")

@cli.command()
@click.argument('title')
@click.argument('author_id')
def add_book(title, author_id):
    """Add a new book."""
    db = next(get_db())
    book = Book(title=title, author_id=author_id)
    db.add(book)
    db.commit()
    click.echo(f"Book {title} added.")

@cli.command()
def list_authors():
    """List all authors."""
    db = next(get_db())
    authors = db.query(Author).all()
    for author in authors:
        click.echo(f"{author.id}: {author.name}")

@cli.command()
def list_books():
    """List all books."""
    db = next(get_db())
    books = db.query(Book).all()
    for book in books:
        click.echo(f"{book.id}: {book.title} (Author ID: {book.author_id})")

if __name__ == '__main__':
    cli()
