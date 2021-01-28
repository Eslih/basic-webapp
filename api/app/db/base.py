from typing import Any

# https://github.com/jaraco/inflect
# inflect.py - Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words.
# Otherwise table names will be singular (e.g. user vs. users)
import inflect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

p = inflect.engine()


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically in plural form.
    # e.g. 'User' model will generate table name 'users'
    @declared_attr
    def __tablename__(cls) -> str:
        return p.plural(cls.__name__.lower())
