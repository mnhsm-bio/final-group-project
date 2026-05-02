from .dependencies.database import SessionLocal
from .models import sandwiches as sandwich_model
from .models import resources as resource_model
from .models import recipes as recipe_model



def seed():
    db = SessionLocal()
    try:
        # Resources
        ingredient_names = ["Bread", "Salami", "Lettuce", "Cheese", "Tomato", "Bacon"]

        resources = {}
        for name in ingredient_names:
            existing = db.query(resource_model.Resource).filter(
                resource_model.Resource.item == name
            ).first()
            if not existing:
                resource = resource_model.Resource(item=name, amount=100)
                db.add(resource)
                db.flush()
                resources[name] = resource
            else:
                resources[name] = existing

        db.commit()

        # Sandwiches
        sandwich_data = [
            {
                "sandwich_name": "Italian",
                "price": 9.99,
                "calories": 520,
                "food_category": "Main",
                "ingredients": [
                    ("Bread", 2),
                    ("Salami", 5),
                    ("Lettuce", 2),
                    ("Cheese", 2),
                ],
            },
            {
                "sandwich_name": "Vegetarian",
                "price": 8.49,
                "calories": 380,
                "food_category": "Vegetarian",
                "ingredients": [
                    ("Bread", 2),
                    ("Lettuce", 3),
                    ("Tomato", 3),
                    ("Cheese", 3),
                ],
            },
            {
                "sandwich_name": "BLT",
                "price": 8.99,
                "calories": 450,
                "food_category": "Main",
                "ingredients": [
                    ("Bread", 2),
                    ("Bacon", 3),
                    ("Lettuce", 2),
                    ("Tomato", 2),
                ],
            },
        ]

        for s_data in sandwich_data:
            existing = db.query(sandwich_model.Sandwich).filter(
                sandwich_model.Sandwich.sandwich_name == s_data["sandwich_name"]
            ).first()

            if not existing:
                sandwich = sandwich_model.Sandwich(
                    sandwich_name=s_data["sandwich_name"],
                    price=s_data["price"],
                    calories=s_data["calories"],
                    food_category=s_data["food_category"],
                )
                db.add(sandwich)
                db.flush()
            else:
                sandwich = existing

            #Recipes
            has_recipes = db.query(recipe_model.Recipe).filter(
                recipe_model.Recipe.sandwich_id == sandwich.id
            ).first()

            if not has_recipes:
                for ingredient_name, amount in s_data["ingredients"]:
                    recipe = recipe_model.Recipe(
                        sandwich_id=sandwich.id,
                        resource_id=resources[ingredient_name].id,
                        amount=amount,
                    )
                    db.add(recipe)

        db.commit()
        print("Seed completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()