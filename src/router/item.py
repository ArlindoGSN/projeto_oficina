from datetime import datetime
from pathlib import Path
from http import HTTPStatus
import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select

from src.router.annotated import T_Session, T_User
from src.schemas import ItemDetails
from src.models import File

router = APIRouter()

UPLOAD_DIR = 'files/'

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=ItemDetails)
async def create_item(file: UploadFile, session: T_Session, current_user: T_User):
    
    name, extensao = os.path.splitext(file.filename)
    
    file_name = f'{name}_{datetime.now().strftime("%Y%m%d%H%M%S%f")}{extensao}'
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    
    db_file = File(
        filename=file_name,
        filepath=file_path,
        user_id=current_user.id
    )

    session.add(db_file)
    await session.commit()
    await session.refresh(db_file)
    
    return db_file

@router.get('/{id}', response_model=ItemDetails)
async def get_item_details_by_id(item_id: int, session: T_Session, current_user: T_User):
    db_file = await session.scalar(select(File).where(File.id==item_id, File.user_id==current_user.id))
    
    if not db_file:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=('Item not found.'))
    
    return db_file

@router.get('/', response_model=list[ItemDetails])
async def list_item(session: T_Session, current_user: T_User):
    db_files = await session.scalars(select(File).where(File.user_id==current_user.id))
    
    return db_files

@router.get('/download/{id}')
async def download_item_by_id(item_id: int, session: T_Session, current_user: T_User):
    db_file = await session.scalar(select(File).where(File.id==item_id, File.user_id==current_user.id))
    
    if not db_file:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=('Item not found.'))
    
    if not os.path.exists(db_file.filepath):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail= (f'Item with ID: {item_id} not found in directory'))
    
    return FileResponse(path=db_file.filepath, headers={'Content-Disposition': 'attachment'}, filename=db_file.filename)

@router.delete('/{id}')
async def delete_item_by_id(item_id: int, session: T_Session, current_user: T_User):
    db_file = await session.scalar(select(File).where(File.id==item_id, File.user_id==current_user.id))
    
    if not db_file:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=('Item not found.'))
    
    if os.path.exists(db_file.filepath):
        os.remove(db_file.filepath)
    
    await session.delete(db_file)
    await session.commit()
    
    return {'Item deleted.'}