from pydantic import BaseModel


class Joke(BaseModel):
    id: str
    joke: str
