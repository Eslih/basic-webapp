from fastapi import APIRouter, Depends, HTTPException

from .. import actions
from ..schemas.joke import Joke

joke_router = APIRouter()


@joke_router.get("/", response_model=Joke, tags=["joke"])
def get_random_joke() -> Joke:
    return actions.joke.get()
