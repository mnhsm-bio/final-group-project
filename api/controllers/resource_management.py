from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import resource_management as model
from ..models import resources as resource_model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    if request.resource_id is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="resource_id is required")

    resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == request.resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id: {request.resource_id}, does not exist"
        )

    if request.resource_amount > resource.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested amount: {request.resource_amount}, exceeds available stock {resource.amount} for resource '{resource.item}'"
        )

    new_item = model.Resource_Management(
        resource_id=request.resource_id,
        resource_amount=request.resource_amount,
        unit=request.unit
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
        result = db.query(model.Resource_Management).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Resource_Management).filter(model.Resource_Management.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found.")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item_query = db.query(model.Resource_Management).filter(model.Resource_Management.id == item_id)
        current_item = item_query.first()
        if not current_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found.")

        update_data = request.dict(exclude_unset=True)

        if update_data.get("resource_id") is not None or update_data.get("resource_amount") is not None:
            target_resource_id = update_data.get("resource_id", current_item.resource_id)
            resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == target_resource_id).first()
            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resource with id: {target_resource_id}, does not exist"
                )

            requested_amount = update_data.get("resource_amount", current_item.resource_amount)
            if requested_amount > resource.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Requested amount: {requested_amount}, exceeds available stock {resource.amount} for resource '{resource.item}'"
                )

        item_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item_query.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Resource_Management).filter(model.Resource_Management.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)