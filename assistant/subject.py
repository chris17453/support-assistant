import os
import uuid
from tabulate import tabulate
from . import db


def insert_subject(description, link_id, active=True):
    # Create a new Subject instance
    new_subject = db.Subject(
        description=description,
        link_id=link_id,
        active=active
    )

    # Insert the subject into the database
    db.session.add(new_subject)
    db.session.commit()

    print("Subject created successfully.")