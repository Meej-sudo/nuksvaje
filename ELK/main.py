from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi_versioning import VersionedFastAPI, version
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List

from models import Base, Item as ItemModel
from database import engine, SessionLocal

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging
import json
import time
import os
import uuid
from pathlib import Path
from logging.handlers import RotatingFileHandler
from starlette.middleware.base import BaseHTTPMiddleware


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "service": "items-app",
            "message": record.getMessage(),
        }

        extra_fields = [
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "client_ip",
            "event",
            "item_id",
            "error_type",
        ]

        for field in extra_fields:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


LOG_FILE = os.getenv("APP_LOG_FILE", "logs/items-app.log")
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("items-app")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=3,
    )
    file_handler.setFormatter(JsonFormatter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            response = await call_next(request)

            duration_ms = round((time.time() - start_time) * 1000, 2)

            logger.info(
                "HTTP request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "client_ip": request.client.host if request.client else None,
                    "event": "http_request",
                },
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as exc:
            duration_ms = round((time.time() - start_time) * 1000, 2)

            logger.exception(
                "Unhandled exception during HTTP request",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "duration_ms": duration_ms,
                    "client_ip": request.client.host if request.client else None,
                    "event": "http_exception",
                    "error_type": type(exc).__name__,
                },
            )

            raise


app = FastAPI()

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemRead(ItemCreate):
    id: int

    class Config:
        orm_mode = True


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@app.get("/")
@version(1)
def read_root():
    return "Items app"


@app.post("/items/", response_model=ItemRead)
@version(1)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    db_item = ItemModel(name=item.name, description=item.description)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    logger.info(
        "Item created",
        extra={
            "event": "item_created",
            "item_id": db_item.id,
        },
    )

    return db_item


@app.get("/items/", response_model=List[ItemRead])
@version(1)
async def read_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ItemModel))
    return result.scalars().all()


@app.get("/items/{item_id}", response_model=ItemRead)
@version(1)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ItemModel).where(ItemModel.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        logger.warning(
            "Item not found",
            extra={
                "event": "item_not_found",
                "item_id": item_id,
                "status_code": 404,
            },
        )
        raise HTTPException(status_code=404, detail="Item not found")

    logger.info(
        "Item read",
        extra={
            "event": "item_read",
            "item_id": item_id,
        },
    )

    return item


@app.put("/items/{item_id}", response_model=ItemRead)
@version(1)
async def update_item(
    item_id: int,
    item: ItemCreate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalar_one_or_none()

    if not db_item:
        logger.warning(
            "Item not found for update",
            extra={
                "event": "item_update_not_found",
                "item_id": item_id,
                "status_code": 404,
            },
        )
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    await session.commit()
    await session.refresh(db_item)

    logger.info(
        "Item updated",
        extra={
            "event": "item_updated",
            "item_id": item_id,
        },
    )

    return db_item


@app.delete("/items/{item_id}")
@version(1)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalar_one_or_none()

    if not db_item:
        logger.warning(
            "Item not found for delete",
            extra={
                "event": "item_delete_not_found",
                "item_id": item_id,
                "status_code": 404,
            },
        )
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(db_item)
    await session.commit()

    logger.info(
        "Item deleted",
        extra={
            "event": "item_deleted",
            "item_id": item_id,
        },
    )

    return {"detail": "Item deleted"}


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
)

# Optional, but do not use "/"
app.mount("/static", StaticFiles(directory="."), name="static")
