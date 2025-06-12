from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from hiremebackend.database_module import Base, engine
from hiremebackend.routers import users, deliveries, coupons
from hiremebackend.routers import auth_router
from hiremebackend import models

# Auto-create tables
Base.metadata.create_all(bind=engine)


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins, adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI to add JWT Bearer auth to Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hire Me API",
        version="1.0.0",
        description="API docs for Hire Me app",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply BearerAuth security requirement globally to all paths
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include your routers
app.include_router(users.router)
app.include_router(auth_router.router)
app.include_router(deliveries.router)
app.include_router(coupons.router)

@app.get("/")
def read_root():
    return {"message": "Hire Me API is running"}
