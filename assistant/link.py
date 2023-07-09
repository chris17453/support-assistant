import os
from tabulate import tabulate
from . import db


def list_cli():
    print("Links")
    links = db.session.query(db.Link).all()
    link_table = []
    for link in links:
        link_table.append([link.id, link.name, link.owner_id, link.description, link.active])

    headers = ['ID', 'Name', 'Owner ID', 'Description', 'Active']
    print(tabulate(link_table, headers, tablefmt='grid'))

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
