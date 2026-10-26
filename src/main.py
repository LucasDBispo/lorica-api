from fastapi import FastAPI

from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as users_router
from src.api.routes.vehicles import router as vehicles_router

app = FastAPI(title="Lorica API", docs_url="/")

routers = [auth_router, users_router, vehicles_router]

for router in routers:
    app.include_router(router)
