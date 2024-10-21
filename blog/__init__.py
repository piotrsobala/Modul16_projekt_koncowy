# blog/__init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
from faker import Faker
from datetime import datetime  # Add this import

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'bardzo-tajny-klucz'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from blog import routes, models  # Import routes and models after initializing db

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Entry": models.Entry  # Access Entry from models
    }

@app.cli.command("generate-entries")
@click.option('--how-many', default=10, help='Number of entries to generate.')

def generate_entries(how_many=10):
    fake = Faker()

    for i in range(how_many):
        post = models.Entry(  # Access Entry from models
            title=fake.sentence(),
            body='\n'.join(fake.paragraphs(15)),
            is_published=True,
            pub_date=datetime.utcnow()  # Add pub_date with current datetime
        )
        db.session.add(post)
    db.session.commit()
    print(f"{how_many} fake entries generated successfully.")
