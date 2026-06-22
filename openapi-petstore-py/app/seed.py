from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models import Category, Tag, Pet, Order, User


PARAGUAYAN_PETS = [
    {"name": "Tobái", "category": "Perro", "tags": ["amigable", "juguetón"], "status": "available"},
    {"name": "Sapukái", "category": "Perro", "tags": ["guardian", "fiel"], "status": "available"},
    {"name": "Jagua", "category": "Perro", "tags": ["cazador", "leal"], "status": "available"},
    {"name": "Mbopi", "category": "Gato", "tags": ["tranquilo", "cariñoso"], "status": "available"},
    {"name": "Mburika", "category": "Gato", "tags": ["juguetón", "curioso"], "status": "pending"},
    {"name": "Kavaju", "category": "Caballo", "tags": ["rápido", "fuerte"], "status": "available"},
    {"name": "Taguato", "category": "Caballo", "tags": ["domado", "noble"], "status": "available"},
    {"name": "Vaka", "category": "Vaca", "tags": ["lechera", "mansa"], "status": "available"},
    {"name": "Ryguasu", "category": "Gallina", "tags": ["ponedora", "tranquila"], "status": "sold"},
    {"name": "Kure", "category": "Cerdo", "tags": ["glotón", "simpático"], "status": "available"},
    {"name": "Pira", "category": "Pez", "tags": ["colorido", "tranquilo"], "status": "available"},
    {"name": "Guyra", "category": "Pájaro", "tags": ["cantor", "alegre"], "status": "pending"},
]

PARAGUAYAN_FOOD = [
    "Sopa paraguaya",
    "Chipa guazú",
    "Mbeju",
    "Pastel mandi'o",
    "Vori vori",
    "Payagua mascada",
    "Lampreado",
    "Kivevé",
    "Chicharó trenzado",
    "Borí borí",
]

PARAGUAYAN_USERS = [
    {"username": "jperez", "first_name": "Juan", "last_name": "Pérez", "email": "jperez@example.com", "phone": "+595 981 123456", "user_status": 1},
    {"username": "mgonzalez", "first_name": "María", "last_name": "González", "email": "mgonzalez@example.com", "phone": "+595 982 234567", "user_status": 1},
    {"username": "cbenitez", "first_name": "Carlos", "last_name": "Benítez", "email": "cbenitez@example.com", "phone": "+595 983 345678", "user_status": 2},
    {"username": "lramirez", "first_name": "Leticia", "last_name": "Ramírez", "email": "lramirez@example.com", "phone": "+595 984 456789", "user_status": 2},
    {"username": "focampo", "first_name": "Federico", "last_name": "Ocampo", "email": "focampo@example.com", "phone": "+595 985 567890", "user_status": 3},
]


def seed_database(db: Session):
    existing = db.query(Category).count()
    if existing > 0:
        return

    categories = {}
    for pet_data in PARAGUAYAN_PETS:
        cat_name = pet_data["category"]
        if cat_name not in categories:
            cat = Category(name=cat_name)
            db.add(cat)
            db.flush()
            categories[cat_name] = cat

    tag_map = {}
    for pet_data in PARAGUAYAN_PETS:
        for tag_name in pet_data["tags"]:
            if tag_name not in tag_map:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
                tag_map[tag_name] = tag

    for i, pet_data in enumerate(PARAGUAYAN_PETS):
        pet = Pet(
            id=i + 1,
            name=pet_data["name"],
            category_id=categories[pet_data["category"]].id,
            photo_urls=f'["https://example.com/photos/{pet_data["name"].lower()}.jpg"]',
            status=pet_data["status"],
        )
        db.add(pet)
        db.flush()
        for tag_name in pet_data["tags"]:
            pet.tags.append(tag_map[tag_name])

    for i, food in enumerate(PARAGUAYAN_FOOD):
        order = Order(
            id=i + 1,
            pet_id=(i % 12) + 1,
            quantity=(i % 5) + 1,
            ship_date=datetime.now(timezone.utc),
            status=["placed", "approved", "delivered"][i % 3],
            complete=(i % 3 == 2),
        )
        db.add(order)

    for i, user_data in enumerate(PARAGUAYAN_USERS):
        user = User(
            id=i + 1,
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password="XXXXXXXXXXX",
            phone=user_data["phone"],
            user_status=user_data["user_status"],
        )
        db.add(user)

    db.commit()
