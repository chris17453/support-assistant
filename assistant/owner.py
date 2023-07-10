import uuid
from . import db



def list_cli():
    print("Owners")
    # List all owners
    db.list_cli(db.Owner)


def insert(name, description, active=True):
    # Generate a new UUID
    owner_uuid = str(uuid.uuid4())

    # Create a new Owner instance
    new_owner = db.Owner(
        name=name,
        description=description,
        active=active
    )

    # Insert the owner into the database
    db.session.add(new_owner)
    db.session.commit()

    print("Owner inserted successfully.")

def get_by_id(id):
    record = db.session.query(db.Owner).filter_by(id=id, active=True).first()
    return record
