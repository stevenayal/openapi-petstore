from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.routers import pet, store, user
from app.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="MascotasAPI — PetStore Paraguay",
    description=(
        "¡Ndaje! El mejor PetStore del mundo ahora desde Asunción del Paraguay. "
        "Esta API te permite gestionar mascotas, órdenes y usuarios "
        "al estilo paraguayo. Usá la api_key `special-key` para auth."
    ),
    version="1.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
    contact={
        "name": "PetStore Paraguay",
        "url": "https://github.com/anomalyco/openapi-petstore",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pet.router)
app.include_router(store.router)
app.include_router(user.router)
