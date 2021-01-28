from pydantic import BaseModel, AnyUrl


class Cat(BaseModel):
    name: str
    url: AnyUrl
