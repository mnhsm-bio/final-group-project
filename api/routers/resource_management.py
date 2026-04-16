from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import resource_management as controller
from ..schemas import resource_management as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Resource Management'],
    prefix="/resource-management"
)


@router.post("/", response_model=schema.Resource_Management)
def create(request: schema.Resource_ManagementCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Resource_Management])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Resource_Management)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Resource_Management)
def update(item_id: int, request: schema.Resource_ManagementUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)