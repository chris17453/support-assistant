import os
import uuid
from tabulate import tabulate
from . import db


def create_tag_net(subject_id, tag_id, link_id, active=True):
    # Create a new TagNet instance
    new_tag_net = db.TagNet(
        subject_id=subject_id,
        tag_id=tag_id,
        link_id=link_id,
        active=active
    )

    # Insert the tag_net into the database
    db.session.add(new_tag_net)
    db.session.commit()

    print("TagNet created successfully.")