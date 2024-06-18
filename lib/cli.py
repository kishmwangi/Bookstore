import click
from database import Database

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', required=True)
@click.option('--email', required=True)
def add_user(name, email):
    db = Database('data/database.db')
    db.connect()
    db.create_tables()
    user_id = db.insert_user(name, email)
    click.echo(f'User added with ID {user_id}')
    db.close()

@cli.command()
@click.option('--title', required=True)
@click.option('--content', required=True)
@click.option('--author', required=True)
def add_post(title, content, author):
    db = Database('data/database.db')
    db.connect()
    db.create_tables()
    author_id = db.insert_user(author, f'{author}@example.com')
    post_id = db.insert_post(title, content, author_id)
    click.echo(f'Post added with ID {post_id}')
    db.close()

@cli.command()
def list_posts():
    db = Database('data/database.db')
    db.connect()
    posts = db.get_posts()
    for post in posts:
        click.echo(f'{post.title} by {post.author.name}')
    db.close()

if __name__ == '__main__':
    cli()