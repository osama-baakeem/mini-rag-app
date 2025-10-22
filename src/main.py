from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

async def startup_db_client():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_providers_factory = LLMProviderFactory(settings)

    # generation clinet
    app.generation_client = llm_providers_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id= settings.GENERATION_MODEL_ID)

    # embedding clinet
    app.embedding_client = llm_providers_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id= settings.EMBEDDING_MODEL_ID,
                                             embedding_size= settings.EMBEDDING_MODEL_SIZE)

async def shoutdown_db_client():
    app.mongo_conn.close()

app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shoutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)



