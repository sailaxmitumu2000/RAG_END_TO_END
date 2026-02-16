import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Save an uploaded file to the uploads folder.
    """
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    contents = await upload_file.read()  # async-safe
    with open(file_path, "wb") as f:
        f.write(contents)
    return file_path
