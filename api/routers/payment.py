from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import payment as controller
from ..schemas import payment as schema
from ..dependencies.database import get_db
from datetime import date

router = APIRouter(
    tags=["Payment"],
    prefix="/payment",
)

@router.post("/{order_id}", response_model=schema.Payment)
def create(order_id: int, request: schema.PaymentCreate, db: Session = Depends(get_db)):
    request.order_id = order_id
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Payment])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/date/{target_date}", response_model=list[schema.PaymentWithTotal])
def read_by_date(target_date: date, db: Session = Depends(get_db)):
    return controller.read_by_date(db, target_date=target_date)

@router.get("/{order_id}", response_model=schema.Payment)
def read_by_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_by_order(db, order_id=order_id)

@router.put("/{order_id}", response_model=schema.Payment)
def update(order_id: int, request: schema.PaymentUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)

@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, order_id=order_id)