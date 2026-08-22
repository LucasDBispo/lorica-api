from fastapi import FastAPI

from app.features.auth.router import router as auth_router
from app.features.users.router import router as users_router

app = FastAPI(title="Lorica API", docs_url="/")

app.include_router(auth_router)
app.include_router(users_router)
