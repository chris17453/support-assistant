import os
import uuid
from tabulate import tabulate
from . import db


def list_cli():
    print("Accounts")
    data =  db.session.query(db.Account).all()
    if len(data) == 0:
        print("No data found.")
        return
    headers = data[0].__table__.columns.keys()
    rows = [[getattr(obj, column) for column in headers] for obj in data]
    print(tabulate(rows, headers=headers))




def insert(link_id,name,description='Default',endpoint=None,api_key=None,json=None,platform=None,active=True):

    if json:
          endpoint=None
          api_key=None

          ## load the json file location into the json arg
          with open(json, 'r') as file:
                file_contents = file.read()
          json=file_contents
    else:
          json=None

    # Create a new Account object
    new_account = db.Account(
        name=name,
        description=description,
        endpoint=endpoint,
        api_key=api_key,
        json=json,
        platform=platform,
        link_id=link_id,
        active=active,
    )

    # Add the new account to the session
    db.session.add(new_account)

    # Commit the changes to the database
    db.session.commit()
    print("Account created successfully.")

def get_by_id(id):
    record = db.session.query(db.Account).filter_by(id=id, active=True).first()
    return record


def get_by_name(link_id,name):
    record = db.session.query(db.Account).filter_by(link_id=link_id,name=name, active=True).first()
    return record
