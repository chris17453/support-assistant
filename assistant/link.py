import os
from . import db


def list_cli():
    print("Links")
    # Retrieve all links from the database
    db.list_cli(db.Link)

def insert(owner_id, name,  description, active=True):
    # Create a new Link instance
    new_link = db.Link(
        name=name,
        description=description,
        owner_id=owner_id,
        active=active
    )

    # Insert the link into the database
    db.session.add(new_link)
    db.session.commit()

    print("Link created successfully.")

def get_by_id(id):
    record = db.session.query(db.Link).filter_by(id=id, active=True).first()
    return record
