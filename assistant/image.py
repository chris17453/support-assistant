import os
import uuid
from PIL import Image as PILImage
from . import db
from . import settings


def list_cli():
    print("Image")
    db.list_cli(db.Image)




def get_image_type(image_path):
    with PILImage.open(image_path) as img:
        return img.format

def get_extension(image_type):
    img_extensions = {
        'JPEG': '.jpg',
        'JPG': '.jpg',
        'PNG': '.png',
        'BMP': '.bmp',
        'GIF': '.gif',
        'TIFF': '.tiff',
    }
    return img_extensions.get(image_type.upper(), '')




def insert(link_id,name, description,  file_path,  crop=None, active=True):
    # Split the file path into name and path
    image_name = os.path.basename(file_path)
    image_path = os.path.dirname(file_path)

    # Validate if the file exists
    if not os.path.isfile(file_path):
        raise ValueError("File does not exist.")

    # Validate the data
    if not image_name or not image_path:
        raise ValueError("Invalid file path.")

    image_type = get_image_type(file_path)
    extension = get_extension(image_type)

    # Generate a new UUID
    image_uuid = str(uuid.uuid4())

    new_image_name=image_uuid+extension
    new_file_path=os.path.join(settings.image_directory,new_image_name)
    resize_image(file_path,new_file_path,0.5)

    # Get the image's width and height
    with PILImage.open(new_file_path) as img:
        width, height = img.size
        mime_type = img.format.lower()


    # Create a new Image instance
    new_image = db.Image(
        name=name,
        description=description,
        image_name=new_image_name,
        image_path=settings.image_directory,
        crop=crop,
        width=width,
        height=height,
        uuid=image_uuid,
        mime=mime_type,
        link_id=link_id,
        active=active
    )

    # Insert the image into the database
    db.session.add(new_image)
    db.session.commit()

    print("Image inserted successfully.")
    return new_image

def get_by_id(id):
    record = db.session.query(db.Image).filter_by(id=id, active=True).first()
    return record
    
def get_by_uuid(uuid):
    record = db.session.query(db.Image).filter_by(uuid=uuid, active=True).first()
    return record
    



def resize_image(input_image_path, output_image_path, size):
    original_image = PILImage.open(input_image_path)
    width, height = original_image.size
    resized_image = original_image.resize((int(width * size), int(height * size)))
    resized_image.save(output_image_path)
