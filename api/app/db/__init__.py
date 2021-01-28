# NO Quality Assurance
# Adding # noqa to a line indicates that the linter (a program that automatically checks code quality)
# should not check this line. Any warnings that code may have generated will be ignored.
from .base import Base  # noqa

# Import all the models, so that the Base class
# has them before being imported by Alembic.
from .. import models  # noqa
