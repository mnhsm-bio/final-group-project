from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import sandwiches as model
from ..models import recipes as recipe_model
from ..models import resources as resource_model
from ..schemas.sandwiches import IngredientDetail
from sqlalchemy.exc import SQLAlchemyError


def _attach_ingredients(db: Session, sandwich):
    recipes = (
        db.query(recipe_model.Recipe)
        .filter(recipe_model.Recipe.sandwich_id == sandwich.id)
        .all()
    )
    ingredients = []
    for recipe in recipes:
        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == recipe.resource_id
        ).first()
        if resource:
            ingredients.append(IngredientDetail(name=resource.item, amount=recipe.amount))
    sandwich.ingredients = ingredients
    return sandwich


def create(db: Session, request):
    new_item = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price,
        calories=request.calories,
        food_category=request.food_category,
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    new_item.ingredients = []
    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return [_attach_ingredients(db, s) for s in result]


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return _attach_ingredients(db, item)


def read_by_category(db: Session, food_category: str):
    try:
        result = (
            db.query(model.Sandwich)
            .filter(model.Sandwich.food_category.ilike(food_category))
            .all()
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No sandwiches found in category '{food_category}'"
        )
    return [_attach_ingredients(db, s) for s in result]


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return _attach_ingredients(db, item.first())


def delete(db: Session, item_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)