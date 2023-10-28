from fastapi import APIRouter, Body, Depends
from starlette import status

from datetime import datetime
from typing import List, Dict, Annotated

from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.db.setup import session, get_db, get_session
from src.infrastructure.api import schemas
from src.application import services
from sqlalchemy.orm import Session
from logging import getLogger
from uuid import uuid4

logger = getLogger(__name__)

router = APIRouter()



