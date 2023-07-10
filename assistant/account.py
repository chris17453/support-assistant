import os
import uuid
from . import db
from sqlalchemy import delete



def list_cli():
    print("Accounts")
    db.list_cli(db.Account)
    



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


def delete_by_name(link_id, name):
    stmt = delete(db.Account).where(db.Account.name == name, db.Account.link_id == link_id)
    db.session.execute(stmt)
    db.session.commit()

def delete_by_id(link_id, account_id):
    stmt = delete(db.Account).where(db.Account.id == account_id, db.Account.link_id == link_id)
    db.session.execute(stmt)
    db.session.commit()

