from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db
from datetime import date

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def read_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_number=tracking_number)

@router.get("/date/{begin_date}/{end_date}", response_model=list[schema.Order])
def read_by_date_range(begin_date: date, end_date: date, db: Session = Depends(get_db)):
    return controller.read_by_date_range(db, begin_date=begin_date, end_date=end_date)

@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.post("/{item_id}/apply-promo", response_model=schema.Order)
def apply_promo(item_id: int, promo_code: str, db: Session = Depends(get_db)):
    return controller.apply_promo(db=db, order_id=item_id, promo_code=promo_code)