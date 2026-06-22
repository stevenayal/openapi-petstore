import json
import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Category, Pet, Tag
from app.schemas import ApiResponse, PetSchema

router = APIRouter(tags=["pet"])


def _pet_to_schema(pet: Pet) -> PetSchema:
    return PetSchema(
        id=pet.id,
        category={"id": pet.category.id, "name": pet.category.name} if pet.category else None,
        name=pet.name,
        photoUrls=json.loads(pet.photo_urls) if isinstance(pet.photo_urls, str) else pet.photo_urls,
        tags=[{"id": t.id, "name": t.name} for t in pet.tags] if pet.tags else [],
        status=pet.status,
    )


@router.put(
    "/pet",
    summary="Update an existing pet",
    operation_id="updatePet",
    response_model=PetSchema,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Pet not found"},
        405: {"description": "Validation exception"},
    },
)
def update_pet(
    pet_data: PetSchema,
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    if pet_data.id is None:
        raise HTTPException(status_code=400, detail="Pet ID is required")
    pet = db.query(Pet).filter(Pet.id == pet_data.id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    pet.name = pet_data.name
    if pet_data.category and pet_data.category.name:
        cat = db.query(Category).filter(Category.name == pet_data.category.name).first()
        if not cat:
            cat = Category(name=pet_data.category.name)
            db.add(cat)
            db.flush()
        pet.category_id = cat.id
    pet.photo_urls = json.dumps(pet_data.photo_urls)
    pet.status = pet_data.status
    if pet_data.tags is not None:
        pet.tags.clear()
        for t in pet_data.tags:
            if t.name:
                tag = db.query(Tag).filter(Tag.name == t.name).first()
                if not tag:
                    tag = Tag(name=t.name)
                    db.add(tag)
                    db.flush()
                pet.tags.append(tag)
    db.commit()
    db.refresh(pet)
    return _pet_to_schema(pet)


@router.post(
    "/pet",
    summary="Add a new pet to the store",
    operation_id="addPet",
    response_model=PetSchema,
    response_model_by_alias=True,
    responses={405: {"description": "Invalid input"}},
)
def add_pet(
    pet_data: PetSchema,
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    cat = None
    if pet_data.category and pet_data.category.name:
        cat = db.query(Category).filter(Category.name == pet_data.category.name).first()
        if not cat:
            cat = Category(name=pet_data.category.name)
            db.add(cat)
            db.flush()

    pet = Pet(
        name=pet_data.name,
        category_id=cat.id if cat else None,
        photo_urls=json.dumps(pet_data.photo_urls),
        status=pet_data.status or "available",
    )
    db.add(pet)
    db.flush()

    if pet_data.tags:
        for t in pet_data.tags:
            if t.name:
                tag = db.query(Tag).filter(Tag.name == t.name).first()
                if not tag:
                    tag = Tag(name=t.name)
                    db.add(tag)
                    db.flush()
                pet.tags.append(tag)

    db.commit()
    db.refresh(pet)
    return _pet_to_schema(pet)


@router.get(
    "/pet/findByStatus",
    summary="Finds Pets by status",
    operation_id="findPetsByStatus",
    response_model=List[PetSchema],
    response_model_by_alias=True,
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid status value"},
    },
)
def find_pets_by_status(
    status: List[str] = Query(..., description="Status values to filter by"),
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    valid_statuses = {"available", "pending", "sold"}
    for s in status:
        if s not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status: {s}")
    pets = db.query(Pet).filter(Pet.status.in_(status)).all()
    return [_pet_to_schema(p) for p in pets]


@router.get(
    "/pet/findByTags",
    summary="Finds Pets by tags",
    operation_id="findPetsByTags",
    response_model=List[PetSchema],
    response_model_by_alias=True,
    deprecated=True,
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid tag value"},
    },
)
def find_pets_by_tags(
    tags: List[str] = Query(..., description="Tags to filter by"),
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    pets = (
        db.query(Pet)
        .join(Pet.tags)
        .filter(Tag.name.in_(tags))
        .distinct()
        .all()
    )
    return [_pet_to_schema(p) for p in pets]


@router.get(
    "/pet/{pet_id}",
    summary="Find pet by ID",
    operation_id="getPetById",
    response_model=PetSchema,
    response_model_by_alias=True,
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Pet not found"},
    },
)
def get_pet_by_id(
    pet_id: int,
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return _pet_to_schema(pet)


@router.post(
    "/pet/{pet_id}",
    summary="Updates a pet in the store with form data",
    operation_id="updatePetWithForm",
    response_model=PetSchema,
    response_model_by_alias=True,
    responses={405: {"description": "Invalid input"}},
)
def update_pet_with_form(
    pet_id: int,
    name: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if name:
        pet.name = name
    if status:
        pet.status = status
    db.commit()
    db.refresh(pet)
    return _pet_to_schema(pet)


@router.delete(
    "/pet/{pet_id}",
    summary="Deletes a pet",
    operation_id="deletePet",
    responses={400: {"description": "Invalid pet value"}},
)
def delete_pet(
    pet_id: int,
    api_key: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"message": "Pet deleted successfully"}


UPLOAD_DIR = "./uploads"


@router.post(
    "/pet/{pet_id}/uploadImage",
    summary="uploads an image",
    operation_id="uploadFile",
    response_model=ApiResponse,
    response_model_by_alias=True,
    responses={200: {"description": "successful operation"}},
)
async def upload_file(
    pet_id: int,
    file: UploadFile = File(None),
    additional_metadata: Optional[str] = Form(None, alias="additionalMetadata"),
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    msg = f"File upload for pet {pet_id}"
    if additional_metadata:
        msg += f" | metadata: {additional_metadata}"
    if file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        ext = os.path.splitext(file.filename or "image")[1] if file.filename else ".jpg"
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
        msg += f" | file saved: {filename} ({len(content)} bytes)"
    return ApiResponse(code=200, type="success", message=msg)
