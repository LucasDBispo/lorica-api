from fastapi import FastAPI

from app.features.auth.router import router as auth_router
from app.features.users.router import router as users_router
from app.features.vehicles.router import router as vehicles_router

app = FastAPI(title="Lorica API", docs_url="/")

routers = [auth_router, users_router, vehicles_router]

for router in routers:
    app.include_router(router)
