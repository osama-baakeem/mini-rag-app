from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, Settings


# Define a base API router with prefix `/api/v1`
# All endpoints registered here will start with `/api/v1`
base_router = APIRouter(
    prefix="/api/v1",
    tags=["/api/v1"]  # Used for grouping endpoints in Swagger docs
)


@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    """
    Welcome endpoint (GET /api/v1/)

    Returns basic app information:
    - Application name
    - Application version

    Args:
        app_settings (Settings): Automatically injected by FastAPI's
                                 dependency system via get_settings().

    Returns:
        dict: JSON response containing app name and version.
    """
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version
    }
