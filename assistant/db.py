from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, inspect, UniqueConstraint, DateTime, func, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from  tabulate import tabulate

from . import settings
# Create the database engine
engine = create_engine(f"sqlite:///{settings.database_file}")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def initialize_database():
    Base.metadata.create_all(engine)
    print("Database initialized.")

def describe_database():
    # Create an inspector to inspect the database
    inspector = inspect(engine)

    # Get a list of all table names
    table_names = inspector.get_table_names()

    # Print the table names and their table schemas
    for table_name in table_names:
        print(f"Table Name: {table_name}")
        print("Table Schema:")
        for column in inspector.get_columns(table_name):
            is_primary_key = column['primary_key']
            
            if is_primary_key:
                pk="(Primary Key)"
            else:
                pk=""
            print(f"  - {column['name']}: {column['type']} {pk}")
        for constraint in inspector.get_unique_constraints(table_name):
                print(" - Constraint: "+",".join(constraint['column_names']))
        
        print("-----------------------")


def data_describe(data):
    if isinstance(data, list):
         for item in data:
            data_describe_single(item)
    else:
        data_describe_single(data)

def list_cli(db_base_t):
    # Fetch the avatars from the table
    
    data = session.query(db_base_t).all()
    if len(data) == 0:
        print("No data found.")
        return
    headers = data[0].__table__.columns.keys()
    rows = [[getattr(obj, column) for column in headers] for obj in data]
    output=tabulate(rows, headers=headers, tablefmt="grid")
    print("-----------------------")
    print(output)
    print("End Table")



def data_describe_single(data):
    try:
        columns = data.__table__.columns.keys()
        print("\nTable: {0}".format(data.__table__.name))
        maxlen=0
        for column in columns:
            if len(column)>maxlen:
                maxlen=len(column)
        maxlen+=2
        for column in columns:
            print ("  - {0:<{maxlen}}: {1}".format(column,data.__dict__[column],maxlen=maxlen))
        

    except Exception as ex:
        print(ex)
        print("No data found")

# Define the table classes
class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,unique=True)
    description = Column(String)
    active = Column(Boolean)

class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    description = Column(String)
    __table_args__ = (UniqueConstraint('name', 'owner_id'),)
    active = Column(Boolean)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    link_id = Column(Integer, ForeignKey('link.id'))
    __table_args__ = (UniqueConstraint('description', 'link_id'),)
    active = Column(Boolean)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, unique=True)
    link_id = Column(Integer, ForeignKey('link.id'))
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('word', 'link_id'),)

class TagNet(Base):
    __tablename__ = 'tag_net'
    primary_key=True
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subject.id'), )
    tag_id = Column(Integer, ForeignKey('tags.id'), )
    link_id = Column(Integer, ForeignKey('link.id'),)
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('tag_id', 'subject_id', 'link_id'),)

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    endpoint = Column(String)
    api_key = Column(String)
    json = Column(String)
    platform = Column(String)
    link_id = Column(Integer, ForeignKey('link.id'))
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('name', 'link_id'),)


class Voice(Base):
    __tablename__ = 'voice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    gender = Column(String)
    voice = Column(String,unique=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    link_id = Column(Integer, ForeignKey('link.id'))
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('name', 'link_id'),)

class Avatar(Base):
    __tablename__ = 'avatar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description  = Column(String )
    image_id = Column(Integer, ForeignKey('image.id'))
    voice_id = Column(Integer, ForeignKey('voice.id'))
    style = Column(String)
    speed = Column(Integer)
    pitch = Column(Integer)
    link_id = Column(Integer, ForeignKey('link.id'))
    uuid = Column(String)
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('name', 'link_id'),)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    image_name = Column(String)
    image_path = Column(String)
    crop = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    uuid = Column(String)
    mime = Column(String)
    link_id = Column(Integer, ForeignKey('link.id'))
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('image_name', 'image_path', 'link_id'),)

class Utterance(Base):
    __tablename__ = 'utterance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    count = Column(Integer)
    avatar_id = Column(Integer, ForeignKey('avatar.id'))
    audio_id = Column(Integer, ForeignKey('audio.id'))
    video_id = Column(Integer, ForeignKey('video.id'))
    link_id = Column(Integer, ForeignKey('link.id'))
    variance = Column(Integer)
    processed = Column(Boolean)
    created = Column(DateTime, server_default=func.now())
    finished = Column(DateTime)
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('text','avatar_id', 'link_id'),)

class Audio(Base):
    __tablename__ = 'audio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path = Column(String)
    length = Column(Numeric(precision=8, scale=2))
    uuid = Column(String, default=str(uuid.uuid4()), unique=True)
    link_id = Column(Integer, ForeignKey('link.id'))
    created = Column(DateTime, server_default=func.now())
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('name', 'path', 'link_id'),)

class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path = Column(String)
    length = Column(Numeric(precision=8, scale=2))
    uuid = Column(String, default=str(uuid.uuid4()), unique=True)
    link_id = Column(Integer, ForeignKey('link.id'))
    created = Column(DateTime, server_default=func.now())
    dub = Column(Boolean,default=False)
    active = Column(Boolean)
    __table_args__ = (UniqueConstraint('name', 'path', 'link_id'),)
