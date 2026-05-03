from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import payment as model
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from sqlalchemy import func
from ..models import orders as order_model

def create(db: Session, request):
    new_item = model.Payment(
        order_id=request.order_id,
        payment_type=request.payment_type,
        card_id=request.card_id,
        transaction_status=request.transaction_status
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Payment).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_by_order(db: Session, order_id: int):
    try:
        item = db.query(model.Payment).filter(model.Payment.order_id == order_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No payment found for this order!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, order_id: int, request):
    try:
        item = db.query(model.Payment).filter(model.Payment.order_id == order_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No payment found for this order!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, order_id: int):
    try:
        item = db.query(model.Payment).filter(model.Payment.order_id == order_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No payment found for this order!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def read_by_date(db: Session, target_date: date):
    try:
        results = (
            db.query(model.Payment, order_model.Order.total_price)
            .join(order_model.Order, model.Payment.order_id == order_model.Order.id)
            .filter(func.date(order_model.Order.order_date) == target_date)
            .all()
        )
        payments = []
        for payment, total_price in results:
            payments.append({
                "order_id": payment.order_id,
                "payment_type": payment.payment_type,
                "card_id": payment.card_id,
                "transaction_status": payment.transaction_status,
                "total_price": total_price,
            })
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return payments