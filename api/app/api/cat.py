from fastapi import APIRouter, Depends, HTTPException
from .. import actions
from ..schemas.cat import Cat

cat_router = APIRouter()


@cat_router.get("/", response_model=Cat, tags=["cat"])
def get_random_cat() -> Cat:
    return actions.cat.get()
