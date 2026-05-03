from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        total_price=request.total_price,
        tracking_number=request.tracking_number,
        order_status=request.order_status,
        promo_code=request.promo_code,
        discount_total=request.discount_total,
        customer_id=request.customer_id,
        order_type=request.order_type
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
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def apply_promo(db: Session, order_id: int, promo_code: str):
    from ..models import promotions as promo_model
    from datetime import datetime, timezone

    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error finding your order!")
        promo = db.query(promo_model.Promotion).filter(promo_model.Promotion.promotion_code == promo_code).first()
        if not promo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code is not valid!")
        if promo.expiration_date < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code is outdated!")

        discount_amount = (float(order.total_price) * (float(promo.discount_value) / 100))
        order.promo_code = promo_code
        order.discount_total = float(order.total_price) - discount_amount
        db.commit()
        db.refresh(order)

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order