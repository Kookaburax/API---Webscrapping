"""API Router for Fast API."""
from fastapi import APIRouter
from src.api.routes import hello, data, parameters, model
# Import other route modules
from src.api.routes import hello, data, parameters, model

router = APIRouter()

# Include all the routers
router.include_router(hello.router, tags=["Hello"], prefix="/hello")
router.include_router(data.router, tags=["Data"], prefix="/data")
router.include_router(parameters.router, tags=["Parameters"], prefix="/parameters")
router.include_router(model.router, tags=["Model"], prefix="/model")
