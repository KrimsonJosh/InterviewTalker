from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.routes import router
from src.core.config import get_settings

settings = get_settings()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG
    )

    # Mount static files, serves files from static/ folder
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Include routers from src/api/routes
    app.include_router(router)

    return app

app = create_app() 