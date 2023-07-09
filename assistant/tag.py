import os
import uuid
from tabulate import tabulate
from . import db


def create_tag(word, link_id, active=True):
    # Create a new Tag instance
    new_tag = db.Tag(
        word=word,
        link_id=link_id,
        active=active
    )

    # Insert the tag into the database
    db.session.add(new_tag)
    db.session.commit()

    print("Tag created successfully.")