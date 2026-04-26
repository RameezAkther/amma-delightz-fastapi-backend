from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import admin, auth, chat, favorites, recipes, users

app = FastAPI(title="Amma Delightz FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(favorites.router)
app.include_router(recipes.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Amma Delightz API"}
